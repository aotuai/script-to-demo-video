# text-to-demo

A Python CLI utility that turns text and media files (slides, screenshots, screen recordings or video clips) into a fully narrated, perfectly timed demo video.

Built for IT professionals, sysadmins, and support teams who want to treat instructional videos like infrastructure-as-code. Stop manually recording screen captures and voiceovers every time a UI element changes. Update the script, swap the media, re-compile your video, and publish it on YouTube and other video platforms.

You can now choose between Microsoft's high-speed cloud TTS (edge-tts) or a 100% local, private, and open-source neural TTS model (kokoro) as your voice narrative engine.

## Available TTS Voices
### Kokoro Local (Default)
A fully private, on-device engine featuring high-quality American voices.

- American Male: am_fenrir, am_adam, am_echo, am_eric, am_liam, am_michael
- American Female: af_heart, af_alloy, af_aoede, af_bella, af_jessica, af_river

### Edge-TTS (Microsoft Cloud)
Use the --engine edge flag to access a massive library of high-speed, multilingual voices.

voice | Gender | Local
-|-|-
af-ZA-AdriNeural             | Female  | af-ZA
 af-ZA-WillemNeural           | Male    | af-ZA
 am-ET-MekdesNeural           | Female  | am-ET
 am-ET-AmehaNeural            | Male    | am-ET
 ar-AE-FatimaNeural           | Female  | ar-AE
 ar-AE-HamdanNeural           | Male    | ar-AE
 ar-BH-LailaNeural            | Female  | ar-BH
 ar-BH-AliNeural              | Male    | ar-BH
 ar-DZ-AminaNeural            | Female  | ar-DZ
 ar-DZ-IsmaelNeural           | Male    | ar-DZ
 ar-EG-SalmaNeural            | Female  | ar-EG
 ar-EG-ShakirNeural           | Male    | ar-EG
 ar-IQ-RanaNeural             | Female  | ar-IQ
 ar-IQ-BasselNeural           | Male    | ar-IQ
 ar-JO-SanaNeural             | Female  | ar-JO
 ar-JO-TaimNeural             | Male    | ar-JO
 ar-KW-NouraNeural            | Female  | ar-KW
 ar-KW-FahedNeural            | Male    | ar-KW
 ar-LB-LaylaNeural            | Female  | ar-LB
 ar-LB-RamiNeural             | Male    | ar-LB
 ar-LY-ImanNeural             | Female  | ar-LY
 ar-LY-OmarNeural             | Male    | ar-LY
 ar-MA-MounaNeural            | Female  | ar-MA
 ar-MA-JamalNeural            | Male    | ar-MA
 ar-OM-AyshaNeural            | Female  | ar-OM
 ar-OM-AbdullahNeural         | Male    | ar-OM
 ar-QA-AmalNeural             | Female  | ar-QA
 ar-QA-MoazNeural             | Male    | ar-QA
 ar-SA-ZariyahNeural          | Female  | ar-SA
 ar-SA-HamedNeural            | Male    | ar-SA
 ar-SY-AmanyNeural            | Female  | ar-SY
 ar-SY-LaithNeural            | Male    | ar-SY
 ar-TN-ReemNeural             | Female  | ar-TN
 ar-TN-HediNeural             | Male    | ar-TN
 ar-YE-MaryamNeural           | Female  | ar-YE
 ar-YE-SalehNeural            | Male    | ar-YE
 az-AZ-BanuNeural             | Female  | az-AZ
 az-AZ-BabekNeural            | Male    | az-AZ
 bg-BG-KalinaNeural           | Female  | bg-BG
 bg-BG-BorislavNeural         | Male    | bg-BG
 bn-BD-NabanitaNeural         | Female  | bn-BD
 bn-BD-PradeepNeural          | Male    | bn-BD
 bn-IN-TanishaaNeural         | Female  | bn-IN
 bn-IN-BashkarNeural          | Male    | bn-IN
 bs-BA-VesnaNeural            | Female  | bs-BA
 bs-BA-GoranNeural            | Male    | bs-BA
 ca-ES-JoanaNeural            | Female  | ca-ES
 ca-ES-EnricNeural            | Male    | ca-ES
 cs-CZ-VlastaNeural           | Female  | cs-CZ
 cs-CZ-AntoninNeural          | Male    | cs-CZ
 cy-GB-NiaNeural              | Female  | cy-GB
 cy-GB-AledNeural             | Male    | cy-GB
 da-DK-ChristelNeural         | Female  | da-DK
 da-DK-JeppeNeural            | Male    | da-DK
 de-AT-IngridNeural           | Female  | de-AT
 de-AT-JonasNeural            | Male    | de-AT
 de-CH-LeniNeural             | Female  | de-CH
 de-CH-JanNeural              | Male    | de-CH
 de-DE-AmalaNeural            | Female  | de-DE
 de-DE-KatjaNeural            | Female  | de-DE
 de-DE-SeraphinaMultilingualNeural | Female  | de-DE
 de-DE-ConradNeural           | Male    | de-DE
 de-DE-FlorianMultilingualNeural | Male    | de-DE
 de-DE-KillianNeural          | Male    | de-DE
 el-GR-AthinaNeural           | Female  | el-GR
 el-GR-NestorasNeural         | Male    | el-GR
 en-AU-NatashaNeural          | Female  | en-AU
 en-AU-WilliamMultilingualNeural | Male    | en-AU
 en-CA-ClaraNeural            | Female  | en-CA
 en-CA-LiamNeural             | Male    | en-CA
 en-GB-LibbyNeural            | Female  | en-GB
 en-GB-MaisieNeural           | Female  | en-GB
 en-GB-SoniaNeural            | Female  | en-GB
 en-GB-RyanNeural             | Male    | en-GB
 en-GB-ThomasNeural           | Male    | en-GB
 en-HK-YanNeural              | Female  | en-HK
 en-HK-SamNeural              | Male    | en-HK
 en-IE-EmilyNeural            | Female  | en-IE
 en-IE-ConnorNeural           | Male    | en-IE
 en-IN-NeerjaExpressiveNeural | Female  | en-IN
 en-IN-NeerjaNeural           | Female  | en-IN
 en-IN-PrabhatNeural          | Male    | en-IN
 en-KE-AsiliaNeural           | Female  | en-KE
 en-KE-ChilembaNeural         | Male    | en-KE
 en-NG-EzinneNeural           | Female  | en-NG
 en-NG-AbeoNeural             | Male    | en-NG
 en-NZ-MollyNeural            | Female  | en-NZ
 en-NZ-MitchellNeural         | Male    | en-NZ
 en-PH-RosaNeural             | Female  | en-PH
 en-PH-JamesNeural            | Male    | en-PH
 en-SG-LunaNeural             | Female  | en-SG
 en-SG-WayneNeural            | Male    | en-SG
 en-TZ-ImaniNeural            | Female  | en-TZ
 en-TZ-ElimuNeural            | Male    | en-TZ
 en-US-AnaNeural              | Female  | en-US
 en-US-AriaNeural             | Female  | en-US
 en-US-AvaMultilingualNeural  | Female  | en-US
 en-US-AvaNeural              | Female  | en-US
 en-US-EmmaMultilingualNeural | Female  | en-US
 en-US-EmmaNeural             | Female  | en-US
 en-US-JennyNeural            | Female  | en-US
 en-US-MichelleNeural         | Female  | en-US
 en-US-AndrewMultilingualNeural | Male    | en-US
 en-US-AndrewNeural           | Male    | en-US
 en-US-BrianMultilingualNeural | Male    | en-US
 en-US-BrianNeural            | Male    | en-US
 en-US-ChristopherNeural      | Male    | en-US
 en-US-EricNeural             | Male    | en-US
 en-US-GuyNeural              | Male    | en-US
 en-US-RogerNeural            | Male    | en-US
 en-US-SteffanNeural          | Male    | en-US
 en-ZA-LeahNeural             | Female  | en-ZA
 en-ZA-LukeNeural             | Male    | en-ZA
 es-AR-ElenaNeural            | Female  | es-AR
 es-AR-TomasNeural            | Male    | es-AR
 es-BO-SofiaNeural            | Female  | es-BO
 es-BO-MarceloNeural          | Male    | es-BO
 es-CL-CatalinaNeural         | Female  | es-CL
 es-CL-LorenzoNeural          | Male    | es-CL
 es-CO-SalomeNeural           | Female  | es-CO
 es-CO-GonzaloNeural          | Male    | es-CO
 es-CR-MariaNeural            | Female  | es-CR
 es-CR-JuanNeural             | Male    | es-CR
 es-CU-BelkysNeural           | Female  | es-CU
 es-CU-ManuelNeural           | Male    | es-CU
 es-DO-RamonaNeural           | Female  | es-DO
 es-DO-EmilioNeural           | Male    | es-DO
 es-EC-AndreaNeural           | Female  | es-EC
 es-EC-LuisNeural             | Male    | es-EC
 es-ES-ElviraNeural           | Female  | es-ES
 es-ES-XimenaNeural           | Female  | es-ES
 es-ES-AlvaroNeural           | Male    | es-ES
 es-GQ-TeresaNeural           | Female  | es-GQ
 es-GQ-JavierNeural           | Male    | es-GQ
 es-GT-MartaNeural            | Female  | es-GT
 es-GT-AndresNeural           | Male    | es-GT
 es-HN-KarlaNeural            | Female  | es-HN
 es-HN-CarlosNeural           | Male    | es-HN
 es-MX-DaliaNeural            | Female  | es-MX
 es-MX-JorgeNeural            | Male    | es-MX
 es-NI-YolandaNeural          | Female  | es-NI
 es-NI-FedericoNeural         | Male    | es-NI
 es-PA-MargaritaNeural        | Female  | es-PA
 es-PA-RobertoNeural          | Male    | es-PA
 es-PE-CamilaNeural           | Female  | es-PE
 es-PE-AlexNeural             | Male    | es-PE
 es-PR-KarinaNeural           | Female  | es-PR
 es-PR-VictorNeural           | Male    | es-PR
 es-PY-TaniaNeural            | Female  | es-PY
 es-PY-MarioNeural            | Male    | es-PY
 es-SV-LorenaNeural           | Female  | es-SV
 es-SV-RodrigoNeural          | Male    | es-SV
 es-US-PalomaNeural           | Female  | es-US
 es-US-AlonsoNeural           | Male    | es-US
 es-UY-ValentinaNeural        | Female  | es-UY
 es-UY-MateoNeural            | Male    | es-UY
 es-VE-PaolaNeural            | Female  | es-VE
 es-VE-SebastianNeural        | Male    | es-VE
 et-EE-AnuNeural              | Female  | et-EE
 et-EE-KertNeural             | Male    | et-EE
 fa-IR-DilaraNeural           | Female  | fa-IR
 fa-IR-FaridNeural            | Male    | fa-IR
 fi-FI-NooraNeural            | Female  | fi-FI
 fi-FI-HarriNeural            | Male    | fi-FI
 fil-PH-BlessicaNeural        | Female  | fil-PH
 fil-PH-AngeloNeural          | Male    | fil-PH
 fr-BE-CharlineNeural         | Female  | fr-BE
 fr-BE-GerardNeural           | Male    | fr-BE
 fr-CA-SylvieNeural           | Female  | fr-CA
 fr-CA-AntoineNeural          | Male    | fr-CA
 fr-CA-JeanNeural             | Male    | fr-CA
 fr-CA-ThierryNeural          | Male    | fr-CA
 fr-CH-ArianeNeural           | Female  | fr-CH
 fr-CH-FabriceNeural          | Male    | fr-CH
 fr-FR-DeniseNeural           | Female  | fr-FR
 fr-FR-EloiseNeural           | Female  | fr-FR
 fr-FR-VivienneMultilingualNeural | Female  | fr-FR
 fr-FR-HenriNeural            | Male    | fr-FR
 fr-FR-RemyMultilingualNeural | Male    | fr-FR
 ga-IE-OrlaNeural             | Female  | ga-IE
 ga-IE-ColmNeural             | Male    | ga-IE
 gl-ES-SabelaNeural           | Female  | gl-ES
 gl-ES-RoiNeural              | Male    | gl-ES
 gu-IN-DhwaniNeural           | Female  | gu-IN
 gu-IN-NiranjanNeural         | Male    | gu-IN
 he-IL-HilaNeural             | Female  | he-IL
 he-IL-AvriNeural             | Male    | he-IL
 hi-IN-SwaraNeural            | Female  | hi-IN
 hi-IN-MadhurNeural           | Male    | hi-IN
 hr-HR-GabrijelaNeural        | Female  | hr-HR
 hr-HR-SreckoNeural           | Male    | hr-HR
 hu-HU-NoemiNeural            | Female  | hu-HU
 hu-HU-TamasNeural            | Male    | hu-HU
 id-ID-GadisNeural            | Female  | id-ID
 id-ID-ArdiNeural             | Male    | id-ID
 is-IS-GudrunNeural           | Female  | is-IS
 is-IS-GunnarNeural           | Male    | is-IS
 it-IT-ElsaNeural             | Female  | it-IT
 it-IT-IsabellaNeural         | Female  | it-IT
 it-IT-DiegoNeural            | Male    | it-IT
 it-IT-GiuseppeMultilingualNeural | Male    | it-IT
 iu-Cans-CA-SiqiniqNeural     | Female  | iu-Cans-CA
 iu-Cans-CA-TaqqiqNeural      | Male    | iu-Cans-CA
 iu-Latn-CA-SiqiniqNeural     | Female  | iu-Latn-CA
 iu-Latn-CA-TaqqiqNeural      | Male    | iu-Latn-CA
 ja-JP-NanamiNeural           | Female  | ja-JP
 ja-JP-KeitaNeural            | Male    | ja-JP
 jv-ID-SitiNeural             | Female  | jv-ID
 jv-ID-DimasNeural            | Male    | jv-ID
 ka-GE-EkaNeural              | Female  | ka-GE
 ka-GE-GiorgiNeural           | Male    | ka-GE
 kk-KZ-AigulNeural            | Female  | kk-KZ
 kk-KZ-DauletNeural           | Male    | kk-KZ
 km-KH-SreymomNeural          | Female  | km-KH
 km-KH-PisethNeural           | Male    | km-KH
 kn-IN-SapnaNeural            | Female  | kn-IN
 kn-IN-GaganNeural            | Male    | kn-IN
 ko-KR-SunHiNeural            | Female  | ko-KR
 ko-KR-HyunsuMultilingualNeural | Male    | ko-KR
 ko-KR-InJoonNeural           | Male    | ko-KR
 lo-LA-KeomanyNeural          | Female  | lo-LA
 lo-LA-ChanthavongNeural      | Male    | lo-LA
 lt-LT-OnaNeural              | Female  | lt-LT
 lt-LT-LeonasNeural           | Male    | lt-LT
 lv-LV-EveritaNeural          | Female  | lv-LV
 lv-LV-NilsNeural             | Male    | lv-LV
 mk-MK-MarijaNeural           | Female  | mk-MK
 mk-MK-AleksandarNeural       | Male    | mk-MK
 ml-IN-SobhanaNeural          | Female  | ml-IN
 ml-IN-MidhunNeural           | Male    | ml-IN
 mn-MN-YesuiNeural            | Female  | mn-MN
 mn-MN-BataaNeural            | Male    | mn-MN
 mr-IN-AarohiNeural           | Female  | mr-IN
 mr-IN-ManoharNeural          | Male    | mr-IN
 ms-MY-YasminNeural           | Female  | ms-MY
 ms-MY-OsmanNeural            | Male    | ms-MY
 mt-MT-GraceNeural            | Female  | mt-MT
 mt-MT-JosephNeural           | Male    | mt-MT
 my-MM-NilarNeural            | Female  | my-MM
 my-MM-ThihaNeural            | Male    | my-MM
 nb-NO-PernilleNeural         | Female  | nb-NO
 nb-NO-FinnNeural             | Male    | nb-NO
 ne-NP-HemkalaNeural          | Female  | ne-NP
 ne-NP-SagarNeural            | Male    | ne-NP
 nl-BE-DenaNeural             | Female  | nl-BE
 nl-BE-ArnaudNeural           | Male    | nl-BE
 nl-NL-ColetteNeural          | Female  | nl-NL
 nl-NL-FennaNeural            | Female  | nl-NL
 nl-NL-MaartenNeural          | Male    | nl-NL
 pl-PL-ZofiaNeural            | Female  | pl-PL
 pl-PL-MarekNeural            | Male    | pl-PL
 ps-AF-LatifaNeural           | Female  | ps-AF
 ps-AF-GulNawazNeural         | Male    | ps-AF
 pt-BR-FranciscaNeural        | Female  | pt-BR
 pt-BR-ThalitaMultilingualNeural | Female  | pt-BR
 pt-BR-AntonioNeural          | Male    | pt-BR
 pt-PT-RaquelNeural           | Female  | pt-PT
 pt-PT-DuarteNeural           | Male    | pt-PT
 ro-RO-AlinaNeural            | Female  | ro-RO
 ro-RO-EmilNeural             | Male    | ro-RO
 ru-RU-SvetlanaNeural         | Female  | ru-RU
 ru-RU-DmitryNeural           | Male    | ru-RU
 si-LK-ThiliniNeural          | Female  | si-LK
 si-LK-SameeraNeural          | Male    | si-LK
 sk-SK-ViktoriaNeural         | Female  | sk-SK
 sk-SK-LukasNeural            | Male    | sk-SK
 sl-SI-PetraNeural            | Female  | sl-SI
 sl-SI-RokNeural              | Male    | sl-SI
 so-SO-UbaxNeural             | Female  | so-SO
 so-SO-MuuseNeural            | Male    | so-SO
 sq-AL-AnilaNeural            | Female  | sq-AL
 sq-AL-IlirNeural             | Male    | sq-AL
 sr-RS-SophieNeural           | Female  | sr-RS
 sr-RS-NicholasNeural         | Male    | sr-RS
 su-ID-TutiNeural             | Female  | su-ID
 su-ID-JajangNeural           | Male    | su-ID
 sv-SE-SofieNeural            | Female  | sv-SE
 sv-SE-MattiasNeural          | Male    | sv-SE
 sw-KE-ZuriNeural             | Female  | sw-KE
 sw-KE-RafikiNeural           | Male    | sw-KE
 sw-TZ-RehemaNeural           | Female  | sw-TZ
 sw-TZ-DaudiNeural            | Male    | sw-TZ
 ta-IN-PallaviNeural          | Female  | ta-IN
 ta-IN-ValluvarNeural         | Male    | ta-IN
 ta-LK-SaranyaNeural          | Female  | ta-LK
 ta-LK-KumarNeural            | Male    | ta-LK
 ta-MY-KaniNeural             | Female  | ta-MY
 ta-MY-SuryaNeural            | Male    | ta-MY
 ta-SG-VenbaNeural            | Female  | ta-SG
 ta-SG-AnbuNeural             | Male    | ta-SG
 te-IN-ShrutiNeural           | Female  | te-IN
 te-IN-MohanNeural            | Male    | te-IN
 th-TH-PremwadeeNeural        | Female  | th-TH
 th-TH-NiwatNeural            | Male    | th-TH
 tr-TR-EmelNeural             | Female  | tr-TR
 tr-TR-AhmetNeural            | Male    | tr-TR
 uk-UA-PolinaNeural           | Female  | uk-UA
 uk-UA-OstapNeural            | Male    | uk-UA
 ur-IN-GulNeural              | Female  | ur-IN
 ur-IN-SalmanNeural           | Male    | ur-IN
 ur-PK-UzmaNeural             | Female  | ur-PK
 ur-PK-AsadNeural             | Male    | ur-PK
 uz-UZ-MadinaNeural           | Female  | uz-UZ
 uz-UZ-SardorNeural           | Male    | uz-UZ
 vi-VN-HoaiMyNeural           | Female  | vi-VN
 vi-VN-NamMinhNeural          | Male    | vi-VN
 zh-CN-XiaoxiaoNeural         | Female  | zh-CN
 zh-CN-XiaoyiNeural           | Female  | zh-CN
 zh-CN-YunjianNeural          | Male    | zh-CN
 zh-CN-YunxiNeural            | Male    | zh-CN
 zh-CN-YunxiaNeural           | Male    | zh-CN
 zh-CN-YunyangNeural          | Male    | zh-CN
 zh-CN-liaoning-XiaobeiNeural | Female  | zh-CN-liaoning
 zh-CN-shaanxi-XiaoniNeural   | Female  | zh-CN-shaanxi
 zh-HK-HiuGaaiNeural          | Female  | zh-HK
 zh-HK-HiuMaanNeural          | Female  | zh-HK
 zh-HK-WanLungNeural          | Male    | zh-HK
 zh-TW-HsiaoChenNeural        | Female  | zh-TW
 zh-TW-HsiaoYuNeural          | Female  | zh-TW
 zh-TW-YunJheNeural           | Male    | zh-TW
 zu-ZA-ThandoNeural           | Female  | zu-ZA
 zu-ZA-ThembaNeural           | Male    | zu-ZA

## Why use this?
- **Video-as-Code**: Keep your internal documentation and helpdesk videos in version control.
- **Perfectly Timed**: Automatically calculates the exact duration of the generated Text-to-Speech (TTS) audio and perfectly syncs, loops, or pads your visual media to match.
- **Iterative Screen Recording**: Automatically exports individual `.mp4` files for every slide. This allows you to listen to the generated audio for a specific step and record a screen capture that perfectly matches that exact timing.
- **AI-Friendly**: The input format is a strict JSON array, making it incredibly easy for LLMs and AI agents to generate instructional videos automatically.
- **Dual TTS Engines:** Use `edge-tts` for quick, zero-setup cloud generation, or default to `kokoro` for complete offline privacy and commercial-friendly open-source narration.

## Prerequisites
1. Python 3.8+
1. FFmpeg: Must be installed and accessible in your system's PATH.
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: `winget install ffmpeg`

## Installation
Clone the repository and install the required Python packages:

```bash
git clone https://github.com/yourusername/script-to-demo-video.git
cd script-to-demo-video
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install edge-tts pydub kokoro soundfile
```
*(Note: The first time you run the tool using the Kokoro engine, it will automatically download the 82M parameter model weights (~300MB) to your machine.)*

## Quick Start
Create a JSON file (e.g., demo.json) containing your script and media paths. Then, run the following command:

```bash
# Default: Uses Kokoro (local/private)
python script_to_demo_video.py demo.json

# Alternative: Uses edge-tts (cloud)
python script_to_demo_video.py demo.json --engine edge
```
We recommend Kooha for screen recording or OBS Studio for professionals.
```bash
flatpak install flathub io.github.seadve.Kooha
flatpak run io.github.seadve.Kooha
```
## The JSON Payload
The script expects a JSON array of objects. Each object represents one "slide" or "section" of your video.

```JSON
[
    {
        "text": "Welcome to the IT Helpdesk tutorial on using BrainFrame AI. [PAUSE 1.5] Let's begin.",
        "media": "assets/intro_slide.png"
    },
    {
        "text": "[PAUSE 2.0] First, open the BrainFrame Webclient by typing the server's IP address into your browser's address bar. Press Enter. [PAUSE]",
        "media": "assets/login_step.mp4",
        "mix_audio": true,
        "media_volume": 0.25
    }
]
```
- `text`: The exact words the TTS engine will speak. (Note: You can insert inline tags like `[PAUSE 2.0]` directly into the text to force the TTS engine to pause mid-sentence or add trailing silence at the end).
- `media`: The path to your visual asset (relative to the JSON file). Supports images (`.png`, `.jpg`) and video clips (`.mp4`, `.mov`, `.avi`, `.mkv`).
- `mix_audio`: (Optional) Boolean (true/false). Set to true to keep the original audio from your video media file and mix it underneath the TTS narration.
- `media_volume`: (Optional) Float. When mix_audio is enabled, this sets the volume level of the background media (e.g., 0.25 for 25% volume).
- (Legacy support: You can also use the key `image` instead of "media").

Note on `duration` and `chapter` keys: You do not need to provide timing & chapter number! The tool will calculate the required duration and chapter number based on the generated audio and automatically update your JSON file to append a `duration` and `chapter` keys for your reference.

## The "Perfect Timing" Workflow
This tool is designed to make recording complex screencasts easy by breaking them down into manageable, pre-timed chunks.

1. **Capture Screenshots**: Take screenshots of every screen or slide in your demo. These act as visual placeholders and help guide your script.
1. **Draft the Script**: Enter your script and the corresponding screenshot filenames into your JSON file in presentation order.
1. **Compile the Draft**: Run the tool to generate the video and audio.
1. **Review the Output**: Locate the newly created [output_name]_slides folder, which contains an individual .mp4 for each section.
1. **Record the Final Screen**: Play the generated slides (e.g., slide_02.mp4) to listen to the TTS audio. Use a screen recorder to capture your actual screen, matching your actions to the audio's pacing.
1. **Update and Re-compile**: Update the JSON with your new video recording and run the compilation script once more to finalize the video.

## Command Line Arguments
You can customize the voice, volume, and output behavior using CLI flags.

| Argument | Description | Default |
| :--- | :--- | :--- |
| `script_file` | Path to the input JSON file. | **Required** |
| `output_video` | Path to save the final stitched video. (Defaults to script filename with .mp4) | Optional |
| `--engine` | Choose the TTS engine: `edge` (cloud/fast) or `kokoro` (local/private). | `edge` |
| `--voice` | Exact voice name to use (e.g., `en-US-AriaNeural` for edge, `am_fenrir` for kokoro). | None |
| `--gender` | Target gender if searching for a voice automatically (Edge only). | `male` |
| `--lang` | Target locale if searching for a voice automatically (e.g., `en-GB`, `es-MX`) (Edge only). | `en-US` |
| `--volume` | Volume adjustment for the TTS output. Use percentages (Edge only). | `+0%` |
| `--captions` | Enables automatic subtitle generation and overlays them on the video. | `False` |
| `--font-size` | Sets the font size for the video captions (requires `--captions`). | `24` |
| `--font-color` | Sets the text color for the captions (e.g., `white`, `yellow`, `#FFFFFF`). | `white` |
| `--list-voices`| Prints a formatted list of all available TTS voices for the Edge engine and exits. | None |
| `--verbose` | Shows raw standard error output from FFmpeg for debugging. | `False` |

## Selecting a Voice
### Using Edge-TTS (Cloud)
To see all available voices, run:
`python script_to_demo_video.py --list-voices`

Once you find a voice you like, use the `ShortName` with the `--voice` flag:
`python script_to_demo_video.py demo.json --voice en-GB-RyanNeural`

### Using Kokoro (Local)
Kokoro uses specific pre-trained voice files. By default, the script falls back to `am_fenrir` (a high-quality American female voice). Some other popular Kokoro voices include:
* **Female:** `af_heart`, `af_alloy`, `af_bella`
* **Male:** `am_fenrir`, `am_michael`, `am_puck`

`python script_to_demo_video.py demo.json --engine kokoro --voice am_fenrir`

## For AI Agents
If you are an AI assistant generating a payload for this tool:
1. Always format the output as a strict JSON array.
1. Ensure the text field uses natural punctuation, as the TTS engine relies on commas and periods for proper pacing and breath pauses.
1. Use the media key for all file references.
1. Do not hallucinate the duration key; allow the Python execution environment to append it automatically.
