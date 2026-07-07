# script-to-demo-video

A Python CLI utility that turns a simple JSON script and media files (images or video clips) into a fully narrated, perfectly timed demo video.

Built for IT professionals, sysadmins, and support teams who want to treat instructional videos like infrastructure-as-code. Stop manually recording screen captures and voiceovers every time a UI element changes. Update the script, swap the media, and re-compile your video.

## Why use this?
- Video-as-Code: Keep your internal documentation and helpdesk videos in version control.
- Perfectly Timed: Automatically calculates the exact duration of the generated Text-to-Speech (TTS) audio and perfectly syncs, loops, or pads your visual media to match.
- Iterative Screen Recording: Automatically exports individual .mp4 files for every slide. This allows you to listen to the generated audio for a specific step and record a screen capture that perfectly matches that exact timing.
- AI-Friendly: The input format is a strict JSON array, making it incredibly easy for LLMs and AI agents to generate instructional videos automatically.

## Prerequisites
1. Python 3.8+
1. FFmpeg: Must be installed and accessible in your system's PATH.
   - Ubuntu/Debian: sudo apt install ffmpeg
   - macOS: brew install ffmpeg
   - Windows: winget install ffmpeg

## Installation
Clone the repository and install the required Python packages:

```bash
git clone https://github.com/yourusername/script-to-demo-video.git
cd script-to-demo-video
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install edge-tts pydub
```

## Quick Start
Create a JSON file (e.g., demo.json) containing your script and media paths. Then, run the following command:

```bash
python script_to_demo_video.py demo.json my_demo.mp4
```
## The JSON Payload
The script expects a JSON array of objects. Each object represents one "slide" or "section" of your video.

```JSON
JSON
[
    {
        "text": "Welcome to the IT Helpdesk tutorial on connecting to the company VPN.",
        "media": "assets/intro_slide.png"
    },
    {
        "text": "First, open the BrainFrame Webclient by typing the server's IP address into your browser's address bar. Press Enter.",
        "media": "assets/login_step.mp4"
    }
]
```
- text: The exact words the TTS engine will speak.
- media: The path to your visual asset (relative to the JSON file). Supports images (.png, .jpg) and video clips (.mp4, .mov, .avi, .mkv).
- (Legacy support: You can also use the key "image" instead of "media").

Note on Durations: You do not need to provide timing! The tool will calculate the required duration based on the generated audio and automatically update your JSON file to append a "duration" key for your reference.

## The "Perfect Timing" Workflow
This tool is designed to make recording complex screencasts easy by breaking them down into manageable, pre-timed chunks.

1. Capture Screenshots: Take screenshots of every screen or slide in your demo. These act as visual placeholders and help guide your script.
1. Draft the Script: Enter your script and the corresponding screenshot filenames into your JSON file in presentation order.
1. Compile the Draft: Run the tool to generate the video and audio.
1. Review the Output: Locate the newly created [output_name]_slides folder, which contains an individual .mp4 for each section.
1. Record the Final Screen: Play the generated slides (e.g., slide_02.mp4) to listen to the TTS audio. Use a screen recorder to capture your actual screen, matching your actions to the audio's pacing. (Note: We recommend the built-in Ubuntu screen recorder if you don't need system audio, or Kooha/OBS Studio if you do.)
1. Update and Re-compile: Update the JSON with your new video recording and run the compilation script once more to finalize the video.

## Command Line Arguments
You can customize the voice, volume, and output behavior using CLI flags.

| Argument	| Description	| Default
|-|-|-
| script_file	| Path to the input JSON file.	| Required
| output_video	| Path to save the final stitched video.	| Required
| --voice	| The exact edge-tts voice shortname to use (e.g., en-US-AriaNeural). Overrides --lang and --gender.	| None
| --gender	| Target gender if searching for a voice automatically. Choices: male, female.	| male
| --lang	| Target locale if searching for a voice automatically (e.g., en-GB, es-MX).	| en-US
| --volume	| Volume adjustment for the TTS output. Use percentages.	| +0%
| --list-voices	| Prints a formatted list of all available TTS voices and exits.	| None
| --verbose	| Shows raw standard error output from FFmpeg for debugging.	| False

## Selecting a Voice
To see all available voices, run:
```Bash
python script_to_demo_video.py --list-voices
```
Once you find a voice you like, use the ShortName with the --voice flag:
```Bash
python script_to_demo_video.py demo.json demo.mp4 --voice en-GB-RyanNeural
```
## For AI Agents
If you are an AI assistant generating a payload for this tool:
1. Always format the output as a strict JSON array.
1. Ensure the text field uses natural punctuation, as the TTS engine relies on commas and periods for proper pacing and breath pauses.
1. Use the media key for all file references.
1. Do not hallucinate the duration key; allow the Python execution environment to append it automatically.
