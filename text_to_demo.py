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
import re

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

# --- Voice Dictionary ---
KOKORO_VOICES = {
    "🇺🇸 American English": {
        "Female": ["af_heart (default)", "af_alloy", "af_aoede", "af_bella", "af_jessica", "af_kore", "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky"],
        "Male": ["am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael", "am_onyx", "am_puck", "am_santa"]
    },
    "🇬🇧 British English": {
        "Female": ["bf_alice", "bf_emma", "bf_isabella", "bf_lily"],
        "Male": ["bm_daniel", "bm_fable", "bm_george", "bm_lewis"]
    },
    "🇪🇸 Spanish": {
        "Female": ["ef_dora"],
        "Male": ["em_alex", "em_santa"]
    },
    "🇫🇷 French": {
        "Female": ["ff_siwis"],
        "Male": []
    },
    "🇮🇳 Hindi": {
        "Female": ["hf_alpha", "hf_beta"],
        "Male": ["hm_omega", "hm_psi"]
    },
    "🇮🇹 Italian": {
        "Female": ["if_sara"],
        "Male": ["im_nicola"]
    },
    "🇯🇵 Japanese (Requires misaki[ja])": {
        "Female": ["jf_alpha", "jf_gongitsune", "jf_nezumi", "jf_tebukuro"],
        "Male": ["jm_kumo"]
    },
    "🇧🇷 Brazilian Portuguese": {
        "Female": ["pf_dora"],
        "Male": ["pm_alex", "pm_santa"]
    },
    "🇨🇳 Mandarin Chinese (Requires misaki[zh])": {
        "Female": ["zf_xiaobei", "zf_xiaoni", "zf_xiaoxiao", "zf_xiaoyi"],
        "Male": ["zm_yunjian", "zm_yunxi", "zm_yunxia", "zm_yunyang"]
    }
}

# --- Helper Functions ---

def format_timestamp(seconds):
    """Converts raw seconds into MM:SS or HH:MM:SS format for YouTube chapters."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

async def display_voices():
    """Lists all available voices from edge-tts in a readable table format and exits."""
    
    # Map Edge-TTS locale codes to human-readable names with flags
    FLAG_MAP = {
        "af-ZA": "South Africa 🇿🇦", "am-ET": "Ethiopia 🇪🇹", "ar-AE": "UAE 🇦🇪",
        "ar-BH": "Bahrain 🇧🇭", "ar-DZ": "Algeria 🇩🇿", "ar-EG": "Egypt 🇪🇬",
        "ar-IQ": "Iraq 🇮🇶", "ar-JO": "Jordan 🇯🇴", "ar-KW": "Kuwait 🇰🇼",
        "ar-LB": "Lebanon 🇱🇧", "ar-LY": "Libya 🇱🇾", "ar-MA": "Morocco 🇲🇦",
        "ar-OM": "Oman 🇴🇲", "ar-QA": "Qatar 🇶🇦", "ar-SA": "Saudi Arabia 🇸🇦",
        "ar-SY": "Syria 🇸🇾", "ar-TN": "Tunisia 🇹🇳", "ar-YE": "Yemen 🇾🇪",
        "az-AZ": "Azerbaijan 🇦🇿", "bg-BG": "Bulgaria 🇧🇬", "bn-BD": "Bangladesh 🇧🇩",
        "bn-IN": "India 🇮🇳", "bs-BA": "Bosnia 🇧🇦", "ca-ES": "Spain 🇪🇸",
        "cs-CZ": "Czechia 🇨🇿", "cy-GB": "United Kingdom 🇬🇧", "da-DK": "Denmark 🇩🇰",
        "de-AT": "Austria 🇦🇹", "de-CH": "Switzerland 🇨🇭", "de-DE": "Germany 🇩🇪",
        "el-GR": "Greece 🇬🇷", "en-AU": "Australia 🇦🇺", "en-CA": "Canada 🇨🇦",
        "en-GB": "United Kingdom 🇬🇧", "en-HK": "Hong Kong 🇭🇰", "en-IE": "Ireland 🇮🇪",
        "en-IN": "India 🇮🇳", "en-KE": "Kenya 🇰🇪", "en-NG": "Nigeria 🇳🇬",
        "en-NZ": "New Zealand 🇳🇿", "en-PH": "Philippines 🇵🇭", "en-SG": "Singapore 🇸🇬",
        "en-TZ": "Tanzania 🇹🇿", "en-US": "United States 🇺🇸", "en-ZA": "South Africa 🇿🇦",
        "es-AR": "Argentina 🇦🇷", "es-BO": "Bolivia 🇧🇴", "es-CL": "Chile 🇨🇱",
        "es-CO": "Colombia 🇨🇴", "es-CR": "Costa Rica 🇨🇷", "es-CU": "Cuba 🇨🇺",
        "es-DO": "Dominican Rep. 🇩🇴", "es-EC": "Ecuador 🇪🇨", "es-ES": "Spain 🇪🇸",
        "es-GQ": "Equatorial Guinea 🇬🇶", "es-GT": "Guatemala 🇬🇹", "es-HN": "Honduras 🇭🇳",
        "es-MX": "Mexico 🇲🇽", "es-NI": "Nicaragua 🇳🇮", "es-PA": "Panama 🇵🇦",
        "es-PE": "Peru 🇵🇪", "es-PR": "Puerto Rico 🇵🇷", "es-PY": "Paraguay 🇵🇾",
        "es-SV": "El Salvador 🇸🇻", "es-US": "United States 🇺🇸", "es-UY": "Uruguay 🇺🇾",
        "es-VE": "Venezuela 🇻🇪", "et-EE": "Estonia 🇪🇪", "fa-IR": "Iran 🇮🇷",
        "fi-FI": "Finland 🇫🇮", "fil-PH": "Philippines 🇵🇭", "fr-BE": "Belgium 🇧🇪",
        "fr-CA": "Canada 🇨🇦", "fr-CH": "Switzerland 🇨🇭", "fr-FR": "France 🇫🇷",
        "ga-IE": "Ireland 🇮🇪", "gl-ES": "Spain 🇪🇸", "gu-IN": "India 🇮🇳",
        "he-IL": "Israel 🇮🇱", "hi-IN": "India 🇮🇳", "hr-HR": "Croatia 🇭🇷",
        "hu-HU": "Hungary 🇭🇺", "id-ID": "Indonesia 🇮🇩", "is-IS": "Iceland 🇮🇸",
        "it-IT": "Italy 🇮🇹", "ja-JP": "Japan 🇯🇵", "jv-ID": "Indonesia 🇮🇩",
        "ka-GE": "Georgia 🇬🇪", "kk-KZ": "Kazakhstan 🇰🇿", "km-KH": "Cambodia 🇰🇭",
        "kn-IN": "India 🇮🇳", "ko-KR": "South Korea 🇰🇷", "lo-LA": "Laos 🇱🇦",
        "lt-LT": "Lithuania 🇱🇹", "lv-LV": "Latvia 🇱🇻", "mk-MK": "North Macedonia 🇲🇰",
        "ml-IN": "India 🇮🇳", "mn-MN": "Mongolia 🇲🇳", "mr-IN": "India 🇮🇳",
        "ms-MY": "Malaysia 🇲🇾", "mt-MT": "Malta 🇲🇹", "my-MM": "Myanmar 🇲🇲",
        "nb-NO": "Norway 🇳🇴", "ne-NP": "Nepal 🇳🇵", "nl-BE": "Belgium 🇧🇪",
        "nl-NL": "Netherlands 🇳🇱", "pl-PL": "Poland 🇵🇱", "ps-AF": "Afghanistan 🇦🇫",
        "pt-BR": "Brazil 🇧🇷", "pt-PT": "Portugal 🇵🇹", "ro-RO": "Romania 🇷🇴",
        "ru-RU": "Russia 🇷🇺", "si-LK": "Sri Lanka 🇱🇰", "sk-SK": "Slovakia 🇸🇰",
        "sl-SI": "Slovenia 🇸🇮", "so-SO": "Somalia 🇸🇴", "sq-AL": "Albania 🇦🇱",
        "sr-RS": "Serbia 🇷🇸", "su-ID": "Indonesia 🇮🇩", "sv-SE": "Sweden 🇸🇪",
        "sw-KE": "Kenya 🇰🇪", "sw-TZ": "Tanzania 🇹🇿", "ta-IN": "India 🇮🇳",
        "ta-LK": "Sri Lanka 🇱🇰", "ta-MY": "Malaysia 🇲🇾", "ta-SG": "Singapore 🇸🇬",
        "te-IN": "India 🇮🇳", "th-TH": "Thailand 🇹🇭", "tr-TR": "Turkey 🇹🇷",
        "uk-UA": "Ukraine 🇺🇦", "ur-IN": "India 🇮🇳", "ur-PK": "Pakistan 🇵🇰",
        "uz-UZ": "Uzbekistan 🇺🇿", "vi-VN": "Vietnam 🇻🇳", "zh-CN": "China 🇨🇳",
        "zh-CN-liaoning": "China 🇨🇳", "zh-CN-shaanxi": "China 🇨🇳", "zh-HK": "Hong Kong 🇭🇰",
        "zh-TW": "Taiwan 🇹🇼", "zu-ZA": "South Africa 🇿🇦"
    }

    try:
        voices = await edge_tts.list_voices()
        voices = sorted(voices, key=lambda v: (v['Locale'], v['Gender'], v['ShortName']))
        
        print("Voice                            | Gender  | Locale   | Country / Language")
        print("---------------------------------|---------|----------|-------------------")
        
        for voice in voices:
            short_name = voice.get('ShortName', 'N/A')
            gender = voice.get('Gender', 'N/A')
            locale = voice.get('Locale', 'N/A')
            
            # Lookup the flag/country from our map, fallback to Microsoft's FriendlyName, then locale
            if locale in FLAG_MAP:
                country = FLAG_MAP[locale]
            else:
                friendly = voice.get('FriendlyName', '')
                if " - " in friendly:
                    country = friendly.split(" - ")[-1].strip()
                else:
                    country = locale
                
            print(f"{short_name:<32} | {gender:<7} | {locale:<8} | {country}")
            
        print("\nUse the exact 'Voice' name with the --voice flag (e.g., --voice en-US-AriaNeural)\n")
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
    
    colors = {
        "black": "&H00000000",
        "white": "&H00FFFFFF",
        "darkgray": "&H00333333",
        "lightgray": "&H00CCCCCC"
    }
    primary_color = colors.get(color_choice.lower(), "&H00CCCCCC") 
    
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
    
    video_filter = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad=width={width}:height={height}:x=(ow-iw)/2:y=(oh-ih)/2:color=black,fps=30"
    
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

def create_video_from_video(input_video_path, duration, output_path, resolution="1920x1080", captions_file=None, keep_audio=False, verbose=False):
    width, height = resolution.split('x')
    
    video_filter = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad=width={width}:height={height}:x=(ow-iw)/2:y=(oh-ih)/2:color=black,fps=30,tpad=stop_mode=clone:stop=-1"
    
    if captions_file:
        video_filter += f",subtitles={captions_file}"

    command = [
        'ffmpeg', '-nostdin', '-i', input_video_path, 
        '-vf', video_filter, '-c:v', 'libx264', '-pix_fmt', 'yuv420p'
    ]
    
    if not keep_audio:
        command.append('-an')
    else:
        command.extend(['-c:a', 'aac', '-b:a', '192k'])

    command.extend(['-t', str(duration), '-y', output_path])
    
    try:
        subprocess.run(command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        if verbose: logging.error(e.stderr.decode('utf-8', errors='ignore'))
        return False

def combine_video_and_audio(video_path, audio_path, output_path, mix_audio=False, media_volume=1.0, verbose=False):
    """Merges video and audio without stretching. Sample rates normalized to 44.1kHz."""
    if mix_audio:
        command = [
            'ffmpeg', '-nostdin', '-i', video_path, '-i', audio_path, 
            '-filter_complex', 
            f'[0:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={media_volume}[bg];'
            f'[1:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=2.0[tts];'
            f'[bg][tts]amix=inputs=2:duration=longest[aout]', 
            '-map', '0:v:0', '-map', '[aout]', 
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', '-shortest', '-y', output_path
        ]
    else:
        command = [
            'ffmpeg', '-nostdin', '-i', video_path, '-i', audio_path, 
            '-map', '0:v:0', '-map', '1:a:0',
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', '-shortest', '-y', output_path
        ]
        
    try:
        subprocess.run(command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        if mix_audio:
            logging.warning("\n   ⚠️  Audio mix failed (source video likely has no audio track). Falling back to TTS only.")
            fallback_command = [
                'ffmpeg', '-nostdin', '-i', video_path, '-i', audio_path, 
                '-map', '0:v:0', '-map', '1:a:0',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', '-shortest', '-y', output_path
            ]
            try:
                subprocess.run(fallback_command, check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError as e2:
                if verbose: logging.error(e2.stderr.decode('utf-8', errors='ignore'))
                return False
        else:
            if verbose: logging.error(e.stderr.decode('utf-8', errors='ignore'))
            return False

def concatenate_videos(video_paths, output_path, temp_dir, verbose=False):
    """Concatenates all slides into a final video. Re-encodes the final timeline to completely eliminate A/V sync drift."""
    filelist_path = os.path.join(temp_dir, "filelist.txt")
    with open(filelist_path, 'w') as f:
        for path in video_paths:
            safe_path = os.path.abspath(path).replace("'", "'\\''")
            f.write(f"file '{safe_path}'\n")
            
    command = [
        'ffmpeg', '-nostdin', '-f', 'concat', '-safe', '0', '-i', os.path.abspath(filelist_path),
        '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '192k', '-y', output_path
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
    parser.add_argument("--caption-color", choices=['black', 'white', 'darkgray', 'lightgray'], default='lightgray', help="Color of the caption text.")
    parser.add_argument("--media-volume", type=float, default=1.0, help="Global volume level for background media when mixed (default: 1.0).")
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
            print("Voice                            | Gender  | Locale   | Country / Language")
            print("---------------------------------|---------|----------|-------------------")
            
            # Helper mapping for the table visualization
            locale_mapping = {
                "🇺🇸 American English": ("en-US", "United States 🇺🇸"),
                "🇬🇧 British English": ("en-GB", "United Kingdom 🇬🇧"),
                "🇪🇸 Spanish": ("es-ES", "Spain 🇪🇸"),
                "🇫🇷 French": ("fr-FR", "France 🇫🇷"),
                "🇮🇳 Hindi": ("hi-IN", "India 🇮🇳"),
                "🇮🇹 Italian": ("it-IT", "Italy 🇮🇹"),
                "🇯🇵 Japanese (Requires misaki[ja])": ("ja-JP", "Japan 🇯🇵 (Needs misaki[ja])"),
                "🇧🇷 Brazilian Portuguese": ("pt-BR", "Brazil 🇧🇷"),
                "🇨🇳 Mandarin Chinese (Requires misaki[zh])": ("zh-CN", "China 🇨🇳 (Needs misaki[zh])")
            }
            
            for lang_key, genders in KOKORO_VOICES.items():
                locale, country = locale_mapping.get(lang_key, ("N/A", lang_key))
                for gender, voices in genders.items():
                    for voice in voices:
                        print(f"{voice:<32} | {gender:<7} | {locale:<8} | {country}")
                        
            print("\nUse the exact 'Voice' name with the --voice flag (e.g., --voice bf_emma)\n")
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
        selected_voice = args.voice if args.voice else 'am_fenrir'
        # Detect the language dynamically based on the selected voice
        lang_code = selected_voice[0].lower() if selected_voice else 'a'
        pipeline = KPipeline(lang_code=lang_code, repo_id='hexgrad/Kokoro-82M')
    
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
    # Updated to save to a _chapters directory
    chapters_export_dir = os.path.join(os.path.dirname(os.path.abspath(output_video_path)), f"{os.path.splitext(os.path.basename(output_video_path))[0]}_chapters")
    os.makedirs(chapters_export_dir, exist_ok=True)
    
    logging.info(f"📂 Chapter Exports Target: {chapters_export_dir}\n")
    
    narrated_clips = []
    full_script_text = []
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.webm')
    current_video_time = 0.0  
    
    ass_filename = "temp_caption.ass"
    
    try:
        for i, section in enumerate(script_data):
            slide_start = time.time()
            text = section.get('text')
            media_path = section.get('media') or section.get('image')
            
            # Inject chapter index back into the JSON object
            section['chapter'] = i + 1

            if not text or not media_path:
                continue
            
            mix_audio_flag = section.get('mix_audio', section.get('media_audio_enabled', False))
            current_media_volume = section.get('media_volume', args.media_volume)
            
            print(f"\n🔷 [Chapter {i+1}/{len(script_data)}]")
            print(f"   📖 Text:  \"{text[:65]}...\"")
            print(f"   🖼️  Media: {media_path}")
            if mix_audio_flag:
                print(f"   🎵 Mixing: Original Media Audio Enabled (Volume: {current_media_volume})")
            
            pause_tags = re.findall(r'\[PAUSE.*?\]', text)
            if pause_tags:
                print(f"   ⏱️  Padding: {len(pause_tags)} [PAUSE] tag(s) detected")
            
            media_abs_path = os.path.join(script_dir, media_path)
            audio_ext = ".mp3" if args.engine == 'edge' else ".wav"
            audio_path = os.path.join(temp_dir, f"audio_{i}{audio_ext}")
            processed_video_path = os.path.join(temp_dir, f"processed_video_{i}.mp4")
            narrated_clip_path = os.path.join(temp_dir, f"narrated_clip_{i}.mp4")

            # --- Dynamic Text Chunking & Pause Injection ---
            parts = re.split(r'(\[PAUSE.*?\])', text)
            full_audio = AudioSegment.empty()
            
            chunk_idx = 0
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                
                if part.startswith('[PAUSE'):
                    match = re.search(r'\[PAUSE\s*([\d\.]+)\]', part)
                    if match:
                        pause_duration = float(match.group(1))
                    else:
                        pause_duration = 1.0
                    full_audio += AudioSegment.silent(duration=int(pause_duration * 1000))
                else:
                    chunk_path = os.path.join(temp_dir, f"chunk_{i}_{chunk_idx}{audio_ext}")
                    if not await generate_audio(part, args.engine, selected_voice, args.volume, chunk_path, pipeline):
                        raise RuntimeError(f"Audio synthesis failed on chunk: {part}")
                    
                    chunk_seg = AudioSegment.from_file(chunk_path)
                    full_audio += chunk_seg
                    chunk_idx += 1
                
            export_format = "mp3" if args.engine == 'edge' else "wav"
            full_audio.export(audio_path, format=export_format)

            duration = get_audio_duration_seconds(audio_path)
            if duration is None:
                raise RuntimeError("Audio length tracking failed.")
            
            print(f"   🔊 Audio: {duration:.2f} seconds")
            section['duration'] = duration
            
            # --- YouTube Chapter Timestamp Generation ---
            start_time_str = format_timestamp(current_video_time)
            end_time_str = format_timestamp(current_video_time + duration)
            clean_text_for_export = re.sub(r'\[PAUSE.*?\]', '', text).replace('  ', ' ').strip()
            
            # Formatted text script with Chapter tags included
            full_script_text.append(f"Chapter {i+1}: {start_time_str} - {end_time_str} | {clean_text_for_export}")
            
            current_video_time += duration
            
            if args.captions:
                display_text = re.sub(r'\[PAUSE.*?\]', '', text).replace('  ', ' ').strip()
                create_ass_file(display_text, duration, ass_filename, font_size=args.font_size, color_choice=args.caption_color)
                captions_arg = ass_filename
            else:
                captions_arg = None

            is_video = media_abs_path.lower().endswith(video_extensions)
            
            if not is_video:
                mix_audio_flag = False

            if is_video:
                success = create_video_from_video(media_abs_path, duration, processed_video_path, captions_file=captions_arg, keep_audio=mix_audio_flag, verbose=args.verbose)
            else:
                success = create_video_from_image(media_abs_path, duration, processed_video_path, captions_file=captions_arg, verbose=args.verbose)
                
            if os.path.exists(ass_filename):
                os.remove(ass_filename)

            if not success or not combine_video_and_audio(processed_video_path, audio_path, narrated_clip_path, mix_audio=mix_audio_flag, media_volume=current_media_volume, verbose=args.verbose):
                raise RuntimeError("FFmpeg compositing processing error.")

            # Renamed exports to chapter_XX.mp4
            chapter_filename = f"chapter_{i+1:02d}.mp4"
            shutil.copy2(narrated_clip_path, os.path.join(chapters_export_dir, chapter_filename))
            narrated_clips.append(narrated_clip_path)

            slide_elapsed = time.time() - slide_start
            print(f"   ⚡ Done:   {chapter_filename} (Processed in {slide_elapsed:.2f}s)")

        if narrated_clips:
            print("\n🎬 Sewing all generated chapters into final showcase...")
            if concatenate_videos(narrated_clips, output_video_path, temp_dir, verbose=args.verbose):
                with open(args.script_file, 'w') as f:
                    json.dump(script_data, f, indent=4)
                
                base_video_name = os.path.splitext(output_video_path)[0]
                script_txt_path = f"{base_video_name}_script.txt"
                with open(script_txt_path, 'w', encoding='utf-8') as f:
                    f.write("\n".join(full_script_text))
                
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