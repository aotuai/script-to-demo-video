import os
import sys
import json
import shutil
import logging
import argparse
import subprocess
import asyncio
import time
import warnings

# --- Dependency Check ---
try:
    import edge_tts
    import soundfile as sf
    from kokoro import KPipeline
    from pydub import AudioSegment
except ImportError as e:
    # Extract the name of the missing module from the error message
    missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
    print(f"\n❌ Missing required Python library: {missing_module}")
    print("Please make sure your virtual environment is activated, then run:")
    print("    pip install -r requirements.txt\n")
    sys.exit(1)

# Suppress messy PyTorch warnings and third-party network logs
warnings.filterwarnings('ignore')
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

# Clean, timestamp-free log format
logging.basicConfig(level=logging.INFO, format='%(message)s')

# --- Helper Functions ---

async def display_voices():
    """Lists all available voices from edge-tts in a readable format and exits."""
    print("\n--- Available TTS Voices (Edge-TTS) ---")
    print("Use the 'ShortName' with the --voice flag for precise selection.\n")
    try:
        voices = await edge_tts.list_voices()
        voices = sorted(voices, key=lambda v: (v['Locale'], v['Gender'], v['ShortName']))
        for voice in voices:
            print(f"  - {voice.get('ShortName', 'N/A'):<28} | {voice.get('Gender', 'N/A'):<7} | {voice.get('Locale')}")
    except Exception as e:
        logging.error(f"❌ Could not retrieve voice list from edge-tts: {e}")
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
    return matching_voices[0]['Name'] if matching_voices else None

def check_ffmpeg_installed():
    """Checks if ffmpeg is accessible in the system's PATH."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.error("❌ FFmpeg not found. Please install ffmpeg and add it to your system's PATH.")
        return False

def create_temp_directory(name="video_temp"):
    """Creates a clean temporary directory for intermediate files."""
    if os.path.exists(name):
        shutil.rmtree(name)
    os.makedirs(name)
    return name

def validate_media_paths(script_data, script_dir):
    """Checks if all media files referenced in the script exist before starting."""
    all_found = True
    for i, section in enumerate(script_data):
        media_path = section.get('media') or section.get('image')
        if not media_path:
            continue
        if not os.path.exists(os.path.join(script_dir, media_path)):
            logging.error(f"❌ File not found for Section {i+1}: {media_path}")
            all_found = False
    return all_found

def create_ass_file(text, duration, ass_path, font_size=12, color_choice="lightgray"):
    """Generates an Advanced SubStation (.ass) file with strict, clean styling."""
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    centiseconds = int((duration % 1) * 100)
    end_time = f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
    
    # Map simple color names to ASS format (&HAABBGGRR)
    colors = {
        "black": "&H00000000",
        "white": "&H00FFFFFF",
        "darkgray": "&H00333333",
        "lightgray": "&H00CCCCCC"
    }
    primary_color = colors.get(color_choice.lower(), "&H00CCCCCC") # Default to lightgray
    
    # Increased wrap length since the font defaults to a smaller size
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 > 85:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1
    if current_line:
        lines.append(" ".join(current_line))
        
    wrapped_text = "\\N".join(lines)

    ass_content = f"""[Script Info]
ScriptType=v4.00+
PlayResX=1920
PlayResY=1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,{font_size},{primary_color},&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,10,10,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{end_time},Default,,0,0,0,,{wrapped_text}
"""
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ass_content)

async def generate_audio(text, engine, voice, volume, output_path, pipeline=None):
    """Generates audio using either edge-tts or kokoro."""
    if engine == 'edge':
        try:
            communicate = edge_tts.Communicate(text, voice, volume=volume)
            await communicate.save(output_path)
            return True
        except Exception as e:
            logging.error(f"❌ Edge-TTS generation failed: {e}")
            return False
    elif engine == 'kokoro':
        try:
            generator = pipeline(text, voice=voice, speed=1.0)
            full_audio = []
            for _, _, audio_chunk in generator:
                full_audio.extend(audio_chunk)
            sf.write(output_path, full_audio, 24000)
            return True
        except Exception as e:
            logging.error(f"❌ Kokoro generation failed: {e}")
            return False

def get_audio_duration_seconds(audio_path):
    """Measures the duration of an audio file in seconds."""
    try:
        sound = AudioSegment.from_file(audio_path)
        return len(sound) / 1000.0
    except Exception as e:
        logging.error(f"❌ Could not read audio file duration: {e}")
        return None

def create_video_from_image(image_path, duration, output_path, resolution="1920x1080", captions_file=None, verbose=False):
    width, height = resolution.split('x')
    video_filter = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad=width={width}:height={height}:x=(ow-iw)/2:y=(oh-ih)/2:color=black"
    
    if captions_file:
        video_filter += f",subtitles={captions_file}"
        
    command = [
        'ffmpeg', '-nostdin', '-loop', '1', '-i', image_path, '-c:v', 'libx264', '-tune', 'stillimage',
        '-vf', video_filter, '-pix_fmt', 'yuv420p', '-t', str(duration), '-y', output_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        if verbose: logging.error(e.stderr.decode('utf-8', errors='ignore'))
        return False

def create_video_from_video(input_video_path, duration, output_path, resolution="1920x1080", captions_file=None, verbose=False):
    width, height = resolution.split('x')
    video_filter = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad=width={width}:height={height}:x=(ow-iw)/2:y=(oh-ih)/2:color=black"
    
    if captions_file:
        video_filter += f",subtitles={captions_file}"

    command = [
        'ffmpeg', '-nostdin', '-stream_loop', '-1', '-i', input_video_path, 
        '-vf', video_filter, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 
        '-an', '-t', str(duration), '-y', output_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        if verbose: logging.error(e.stderr.decode('utf-8', errors='ignore'))
        return False

def combine_video_and_audio(video_path, audio_path, output_path, verbose=False):
    command = [
        'ffmpeg', '-nostdin', '-i', video_path, '-i', audio_path, '-c:v', 'copy',
        '-c:a', 'aac', '-shortest', '-y', output_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        if verbose: logging.error(e.stderr.decode('utf-8', errors='ignore'))
        return False

def concatenate_videos(video_paths, output_path, temp_dir, verbose=False):
    filelist_path = os.path.join(temp_dir, "filelist.txt")
    with open(filelist_path, 'w') as f:
        for path in video_paths:
            safe_path = os.path.abspath(path).replace("'", "'\\''")
            f.write(f"file '{safe_path}'\n")
    command = [
        'ffmpeg', '-nostdin', '-f', 'concat', '-safe', '0', '-i', os.path.abspath(filelist_path),
        '-c', 'copy', '-y', output_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        if verbose: logging.error(e.stderr.decode('utf-8', errors='ignore'))
        return False

async def main():
    total_start_time = time.time()
    
    parser = argparse.ArgumentParser(
        description="Generate a narrated video from a text script and media (images/videos).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("script_file", nargs='?', default=None)
    parser.add_argument("output_video", nargs='?', default=None)
    parser.add_argument("--engine", choices=['edge', 'kokoro'], default='kokoro')
    parser.add_argument("--captions", action="store_true", help="Enable beautiful, styled slide-level captions.")
    parser.add_argument("--font-size", type=int, default=12, help="Font size for the on-screen captions (default: 12).")
    parser.add_argument("--caption-color", choices=['black', 'white', 'darkgray', 'lightgray'], default='lightgray', help="Color of the caption text (default: darkgray).")
    parser.add_argument("--lang", default="en-US")
    parser.add_argument("--gender", choices=['male', 'female'], default='male')
    parser.add_argument("--volume", default="+0%")
    parser.add_argument("--voice", default=None)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--list-voices", action="store_true")
    
    args = parser.parse_args()

    if args.list_voices:
        if args.engine == 'edge':
            await display_voices()
        else:
            print("\n--- Available TTS Voices (Kokoro Local) ---")
            print("American Male:   am_fenrir, am_adam, am_echo, am_eric, am_liam, am_michael")
            print("American Female: af_heart, af_alloy, af_aoede, af_bella, af_jessica, af_river")
        sys.exit(0)
    
    if not args.script_file:
        parser.error("The 'script_file' argument is required.")

    if not args.output_video:
        args.output_video = f"{os.path.splitext(args.script_file)[0]}.mp4"

    output_video_path = args.output_video
    if not any(output_video_path.lower().endswith(ext) for ext in ['.mp4', '.mov', '.mkv', '.avi', '.webm']):
        output_video_path += '.mp4'
    
    if not check_ffmpeg_installed():
        sys.exit(1)

    pipeline = None
    if args.engine == 'edge':
        selected_voice = args.voice
        if not selected_voice:
            selected_voice = await find_voice(args.gender, args.lang)
    else:
        logging.info("⚙️  Initializing Kokoro local pipeline mapping...")
        pipeline = KPipeline(lang_code='a')
        selected_voice = args.voice if args.voice else 'am_fenrir'
    
    logging.info(f"🚀 ENGINE: {args.engine.upper()} | VOICE: {selected_voice} | CAPTIONS: {'ON (Size ' + str(args.font_size) + ', ' + args.caption_color + ')' if args.captions else 'OFF'}")

    try:
        with open(args.script_file, 'r') as f:
            script_data = json.load(f)
    except Exception as e:
        logging.error(f"❌ Failed to parse script file: {e}")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(args.script_file))
    if not validate_media_paths(script_data, script_dir):
        sys.exit(1)

    temp_dir = create_temp_directory()
    slides_export_dir = os.path.join(os.path.dirname(os.path.abspath(output_video_path)), f"{os.path.splitext(os.path.basename(output_video_path))[0]}_slides")
    os.makedirs(slides_export_dir, exist_ok=True)
    
    logging.info(f"📂 Slide Exports Target: {slides_export_dir}\n")
    
    narrated_clips = []
    full_script_text = []
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.webm')
    
    ass_filename = "temp_caption.ass"
    
    try:
        for i, section in enumerate(script_data):
            slide_start = time.time()
            text = section.get('text')
            media_path = section.get('media') or section.get('image')

            if not text or not media_path:
                continue
            
            full_script_text.append(text)
            
            print(f"\n🔷 [Section {i+1}/{len(script_data)}]")
            print(f"   📖 Text:  \"{text[:65]}...\"")
            print(f"   🖼️  Media: {media_path}")
            
            media_abs_path = os.path.join(script_dir, media_path)
            audio_ext = ".mp3" if args.engine == 'edge' else ".wav"
            audio_path = os.path.join(temp_dir, f"audio_{i}{audio_ext}")
            silent_video_path = os.path.join(temp_dir, f"silent_video_{i}.mp4")
            narrated_clip_path = os.path.join(temp_dir, f"narrated_clip_{i}.mp4")

            if not await generate_audio(text, args.engine, selected_voice, args.volume, audio_path, pipeline):
                raise RuntimeError("Audio synthesis failed.")
            
            duration = get_audio_duration_seconds(audio_path)
            if duration is None:
                raise RuntimeError("Audio length tracking failed.")
            
            print(f"   🔊 Audio: {duration:.2f} seconds")
            section['duration'] = duration
            
            if args.captions:
                create_ass_file(text, duration, ass_filename, font_size=args.font_size, color_choice=args.caption_color)
                captions_arg = ass_filename
            else:
                captions_arg = None

            is_video = media_abs_path.lower().endswith(video_extensions)
            if is_video:
                success = create_video_from_video(media_abs_path, duration, silent_video_path, captions_file=captions_arg, verbose=args.verbose)
            else:
                success = create_video_from_image(media_abs_path, duration, silent_video_path, captions_file=captions_arg, verbose=args.verbose)
                
            if os.path.exists(ass_filename):
                os.remove(ass_filename)

            if not success or not combine_video_and_audio(silent_video_path, audio_path, narrated_clip_path, verbose=args.verbose):
                raise RuntimeError("FFmpeg compositing processing error.")

            slide_filename = f"slide_{i+1:02d}.mp4"
            shutil.copy2(narrated_clip_path, os.path.join(slides_export_dir, slide_filename))
            narrated_clips.append(narrated_clip_path)

            slide_elapsed = time.time() - slide_start
            print(f"   ⚡ Done:   {slide_filename} (Processed in {slide_elapsed:.2f}s)")

        if narrated_clips:
            print("\n🎬 Sewing all generated slides into final showcase...")
            if concatenate_videos(narrated_clips, output_video_path, temp_dir, verbose=args.verbose):
                with open(args.script_file, 'w') as f:
                    json.dump(script_data, f, indent=4)
                
                base_video_name = os.path.splitext(output_video_path)[0]
                script_txt_path = f"{base_video_name}_script.txt"
                with open(script_txt_path, 'w', encoding='utf-8') as f:
                    f.write("\n\n".join(full_script_text))
                
                total_elapsed = time.time() - total_start_time
                print("=========================================================")
                print(f"✅ SUCCESS: Final video exported to -> {output_video_path}")
                print(f"📄 Script text exported to -> {script_txt_path}")
                print(f"⏱️  TOTAL PROCESSING TIME: {total_elapsed:.2f} seconds")
                print("=========================================================")

    except Exception as e:
        logging.error(f"\n❌ Critical Pipeline Interrupt: {e}")
        if os.path.exists(ass_filename):
            os.remove(ass_filename)
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    asyncio.run(main())
