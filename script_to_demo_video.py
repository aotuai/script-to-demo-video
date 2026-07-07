import os
import sys
import json
import shutil
import logging
import argparse
import subprocess
import asyncio
import edge_tts
from pydub import AudioSegment

# --- Configuration ---
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# --- Helper Functions ---

# --- NEW FUNCTION ---
async def display_voices():
    """Lists all available voices from edge-tts in a readable format and exits."""
    print("--- Available TTS Voices ---")
    print("Use the 'ShortName' with the --voice flag for precise selection.")
    print("Or, use the 'Locale' and 'Gender' with the --lang and --gender flags.\n")
    try:
        voices = await edge_tts.list_voices()
        # Sort voices by locale, then gender, then shortname for consistency
        voices = sorted(voices, key=lambda v: (v['Locale'], v['Gender'], v['ShortName']))
        
        for voice in voices:
            short_name = voice.get('ShortName', 'N/A')
            gender = voice.get('Gender', 'N/A')
            locale = voice.get('Locale', 'N/A')
            print(f"  - Voice: {short_name:<28} | Gender: {gender:<7} | Locale: {locale}")
            
    except Exception as e:
        logging.error(f"Could not retrieve voice list from edge-tts: {e}")
        sys.exit(1)

async def find_voice(gender: str, lang: str):
    """Finds a suitable voice from edge-tts based on gender and language."""
    voices = await edge_tts.list_voices()
    target_gender = "Male" if gender.lower() == 'male' else "Female"
    
    matching_voices = [
        v for v in voices 
        if v['ShortName'].lower().startswith(lang.lower() + '-') 
        and v['Gender'] == target_gender
    ]
    
    if not matching_voices:
        return None
        
    return matching_voices[0]['Name']

def check_ffmpeg_installed():
    """Checks if ffmpeg is accessible in the system's PATH."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        logging.info("✅ FFmpeg is installed and accessible.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.error("❌ FFmpeg not found. Please install ffmpeg and ensure it's in your system's PATH.")
        return False

def create_temp_directory(name="video_temp"):
    """Creates a clean temporary directory for intermediate files."""
    if os.path.exists(name):
        shutil.rmtree(name)
    os.makedirs(name)
    logging.info(f"Temporary directory '{name}' created.")
    return name

def validate_image_paths(script_data, script_dir):
    """Checks if all image files referenced in the script exist before starting."""
    logging.info("--- Pre-flight Check: Validating all image paths... ---")
    all_found = True
    for i, section in enumerate(script_data):
        image_path = section.get('image')
        if not image_path:
            logging.warning(f"⚠️  Skipping section {i+1} in check: missing 'image' key.")
            continue
        
        full_path = os.path.join(script_dir, image_path)
        if not os.path.exists(full_path):
            logging.error(f"❌ FATAL: Image not found for section {i+1}: {full_path}")
            all_found = False
            
    if all_found:
        logging.info("✅ All image files were found.")
    else:
        logging.error("Please correct the paths in your JSON file before proceeding.")
    return all_found

async def generate_audio_from_text(text, voice, volume, output_path):
    """Generates an MP3 audio file from text using edge-tts."""
    try:
        logging.info(f"Generating audio for: '{text[:50]}...' using voice '{voice}' and volume '{volume}'")
        communicate = edge_tts.Communicate(text, voice, volume=volume)
        await communicate.save(output_path)
        return True
    except Exception as e:
        logging.error(f"Failed to generate audio with edge-tts: {e}")
        return False

def get_audio_duration_seconds(audio_path):
    """Measures the duration of an audio file in seconds."""
    try:
        sound = AudioSegment.from_mp3(audio_path)
        duration = len(sound) / 1000.0
        logging.info(f"Audio duration: {duration:.2f} seconds.")
        return duration
    except Exception as e:
        logging.error(f"Could not read audio file duration: {e}")
        return None

def create_video_from_image(image_path, duration, output_path, resolution="1920x1080", verbose=False):
    """Creates a silent video clip from a static image for a specific duration."""
    logging.info(f"Creating video from '{image_path}' for {duration:.2f} seconds.")
    
    width, height = resolution.split('x')
    video_filter = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad=width={width}:height={height}:x=(ow-iw)/2:y=(oh-ih)/2:color=black"

    command = [
        'ffmpeg', '-loop', '1', '-i', image_path, '-c:v', 'libx264', '-tune', 'stillimage',
        '-vf', video_filter, '-pix_fmt', 'yuv420p', '-t', str(duration), '-y', output_path
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg failed to create video from image. Command: {' '.join(command)}")
        stderr_output = e.stderr.decode('utf-8', errors='ignore')
        logging.error(f"\n--- FFmpeg Error Output ---\n{stderr_output}\n---------------------------\n")
        return False

def combine_video_and_audio(video_path, audio_path, output_path, verbose=False):
    """Merges a silent video clip with an audio file."""
    logging.info(f"Combining '{os.path.basename(video_path)}' and '{os.path.basename(audio_path)}'.")
    command = [
        'ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy',
        '-c:a', 'aac', '-shortest', '-y', output_path
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg failed to combine video and audio. Command: {' '.join(command)}")
        stderr_output = e.stderr.decode('utf-8', errors='ignore')
        logging.error(f"\n--- FFmpeg Error Output ---\n{stderr_output}\n---------------------------\n")
        return False

def concatenate_videos(video_paths, output_path, temp_dir, verbose=False):
    """Stitches multiple video clips together into a single video."""
    logging.info(f"Concatenating {len(video_paths)} clips into final video...")
    
    filelist_path = os.path.join(temp_dir, "filelist.txt")
    with open(filelist_path, 'w') as f:
        for path in video_paths:
            safe_path = os.path.abspath(path).replace("'", "'\\''")
            f.write(f"file '{safe_path}'\n")

    command = [
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', os.path.abspath(filelist_path),
        '-c', 'copy', '-y', output_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)
        logging.info(f"✅ Final video successfully created at '{output_path}'")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg failed to concatenate videos. Command: {' '.join(command)}")
        stderr_output = e.stderr.decode('utf-8', errors='ignore')
        logging.error(f"\n--- FFmpeg Error Output ---\n{stderr_output}\n---------------------------\n")
        return False

async def main():
    """Main function to parse arguments and run the video creation pipeline."""
    parser = argparse.ArgumentParser(
        description="Generate an introduction video from a text script and screenshots.",
        formatter_class=argparse.RawTextHelpFormatter # Use RawTextHelpFormatter for better help text formatting
    )
    # --- MODIFIED ARGUMENTS ---
    # Positional args are now optional, we will validate them manually later
    parser.add_argument("script_file", nargs='?', default=None, help="Path to the JSON file containing the script and image paths.")
    parser.add_argument("output_video", nargs='?', default=None, help="Path for the final output video file (e.g., 'intro_video.mp4').")
    
    parser.add_argument("--lang", default="en-US", help="Language-locale code for the voice (e.g., 'en-GB', 'es-MX').\nUsed if --voice is not set.")
    parser.add_argument("--gender", choices=['male', 'female'], default='male', help="Gender of the voice. Used if --voice is not set.")
    parser.add_argument("--volume", default="+0%", help="Volume adjustment for the voice (e.g., '+10%%', '-5%%').")
    parser.add_argument("--voice", default=None, help="Exact voice name to use (e.g., 'en-GB-RyanNeural').\nOverrides --lang and --gender.")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output from FFmpeg commands.")
    # --- NEW ARGUMENT ---
    parser.add_argument("--list-voices", action="store_true", help="List all available voices from edge-tts and exit.")
    
    args = parser.parse_args()

    # --- NEW LOGIC: Handle --list-voices flag ---
    if args.list_voices:
        await display_voices()
        sys.exit(0)
    
    # If not listing voices, the positional arguments are required.
    if not args.script_file or not args.output_video:
        parser.error("The following arguments are required when not using --list-voices: script_file, output_video")
    # --- END NEW LOGIC ---

    output_video_path = args.output_video
    known_extensions = ['.mp4', '.mov', '.mkv', '.avi', '.webm']
    if not any(output_video_path.lower().endswith(ext) for ext in known_extensions):
        output_video_path += '.mp4'
        logging.warning(f"Output filename did not have a standard extension. Appending '.mp4'. Final output will be: '{output_video_path}'")
    
    if not check_ffmpeg_installed():
        sys.exit(1)

    selected_voice = args.voice
    if not selected_voice:
        logging.info(f"Searching for a '{args.gender}' voice in language '{args.lang}'...")
        selected_voice = await find_voice(args.gender, args.lang)
        if not selected_voice:
            logging.error(f"Could not find an edge-tts voice for gender='{args.gender}' and lang='{args.lang}'.")
            logging.error("Please try a different combination or run 'edge-tts --list-voices' to see available options.")
            sys.exit(1)
    
    logging.info(f"✅ Voice selected: {selected_voice}")

    try:
        with open(args.script_file, 'r') as f:
            script_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Could not read or parse the script file '{args.script_file}': {e}")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(args.script_file))
    
    if not validate_image_paths(script_data, script_dir):
        sys.exit(1)

    temp_dir = create_temp_directory()
    narrated_clips = []
    
    try:
        for i, section in enumerate(script_data):
            logging.info(f"--- Processing Section {i+1}/{len(script_data)} ---")
            text = section.get('text')
            image_path = section.get('image')

            if not text or not image_path:
                logging.warning(f"Skipping section {i+1} due to missing 'text' or 'image' key.")
                continue
            
            image_abs_path = os.path.join(script_dir, image_path)
            audio_path = os.path.join(temp_dir, f"audio_{i}.mp3")
            silent_video_path = os.path.join(temp_dir, f"silent_video_{i}.mp4")
            narrated_clip_path = os.path.join(temp_dir, f"narrated_clip_{i}.mp4")

            if not await generate_audio_from_text(text, selected_voice, args.volume, audio_path):
                raise RuntimeError("Failed during audio generation.")
            
            duration = get_audio_duration_seconds(audio_path)
            if duration is None:
                raise RuntimeError("Failed to get audio duration.")
            
            # --- NEW: Save duration back to the current section ---
            section['duration'] = duration
            
            if not create_video_from_image(image_abs_path, duration, silent_video_path, verbose=args.verbose):
                raise RuntimeError("Failed to create video from image.")
            
            if not combine_video_and_audio(silent_video_path, audio_path, narrated_clip_path, verbose=args.verbose):
                raise RuntimeError("Failed to combine video and audio.")

            narrated_clips.append(narrated_clip_path)

        if narrated_clips:
            success = concatenate_videos(narrated_clips, output_video_path, temp_dir, verbose=args.verbose)
            
            # --- NEW: Write updated JSON data back to file ---
            if success:
                logging.info(f"Updating '{args.script_file}' with calculated durations...")
                try:
                    with open(args.script_file, 'w') as f:
                        json.dump(script_data, f, indent=4)
                    logging.info("✅ JSON file successfully updated.")
                except Exception as e:
                    logging.error(f"Failed to write updated JSON to '{args.script_file}': {e}")
        else:
            logging.warning("No clips were generated to concatenate.")

    except (RuntimeError, FileNotFoundError) as e:
        logging.error(f"A critical error occurred: {e}")
    finally:
        logging.info(f"Cleaning up temporary directory '{temp_dir}'...")
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    asyncio.run(main())
