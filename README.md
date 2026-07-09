# text-to-demo

A Python CLI utility that turns text and media files (slides, screenshots, screen recordings or video clips) into a fully narrated, perfectly timed demo video.

Built for IT professionals, sysadmins, and support teams who want to treat instructional videos like infrastructure-as-code. Stop manually recording screen captures and voiceovers every time a UI element changes. Update the script, swap the media, re-compile your video, and publish it on YouTube and other video platforms.

You can now choose between Microsoft's high-speed cloud TTS (edge-tts) or a 100% local, private, and open-source neural TTS model (kokoro) as your voice narrative engine.

## Available TTS Voices
### Kokoro Local (Default)
A fully private, on-device engine featuring high-quality voices.

Voice                            | Gender  | Locale   | Country / Language
---------------------------------|---------|----------|-------------------
af_heart (default)               | Female  | en-US    | United States 🇺🇸
af_alloy                         | Female  | en-US    | United States 🇺🇸
af_aoede                         | Female  | en-US    | United States 🇺🇸
af_bella                         | Female  | en-US    | United States 🇺🇸
af_jessica                       | Female  | en-US    | United States 🇺🇸
af_kore                          | Female  | en-US    | United States 🇺🇸
af_nicole                        | Female  | en-US    | United States 🇺🇸
af_nova                          | Female  | en-US    | United States 🇺🇸
af_river                         | Female  | en-US    | United States 🇺🇸
af_sarah                         | Female  | en-US    | United States 🇺🇸
af_sky                           | Female  | en-US    | United States 🇺🇸
am_adam                          | Male    | en-US    | United States 🇺🇸
am_echo                          | Male    | en-US    | United States 🇺🇸
am_eric                          | Male    | en-US    | United States 🇺🇸
am_fenrir                        | Male    | en-US    | United States 🇺🇸
am_liam                          | Male    | en-US    | United States 🇺🇸
am_michael                       | Male    | en-US    | United States 🇺🇸
am_onyx                          | Male    | en-US    | United States 🇺🇸
am_puck                          | Male    | en-US    | United States 🇺🇸
am_santa                         | Male    | en-US    | United States 🇺🇸
bf_alice                         | Female  | en-GB    | United Kingdom 🇬🇧
bf_emma                          | Female  | en-GB    | United Kingdom 🇬🇧
bf_isabella                      | Female  | en-GB    | United Kingdom 🇬🇧
bf_lily                          | Female  | en-GB    | United Kingdom 🇬🇧
bm_daniel                        | Male    | en-GB    | United Kingdom 🇬🇧
bm_fable                         | Male    | en-GB    | United Kingdom 🇬🇧
bm_george                        | Male    | en-GB    | United Kingdom 🇬🇧
bm_lewis                         | Male    | en-GB    | United Kingdom 🇬🇧
ef_dora                          | Female  | es-ES    | Spain 🇪🇸
em_alex                          | Male    | es-ES    | Spain 🇪🇸
em_santa                         | Male    | es-ES    | Spain 🇪🇸
ff_siwis                         | Female  | fr-FR    | France 🇫🇷
hf_alpha                         | Female  | hi-IN    | India 🇮🇳
hf_beta                          | Female  | hi-IN    | India 🇮🇳
hm_omega                         | Male    | hi-IN    | India 🇮🇳
hm_psi                           | Male    | hi-IN    | India 🇮🇳
if_sara                          | Female  | it-IT    | Italy 🇮🇹
im_nicola                        | Male    | it-IT    | Italy 🇮🇹
jf_alpha                         | Female  | ja-JP    | Japan 🇯🇵 (Needs misaki[ja])
jf_gongitsune                    | Female  | ja-JP    | Japan 🇯🇵 (Needs misaki[ja])
jf_nezumi                        | Female  | ja-JP    | Japan 🇯🇵 (Needs misaki[ja])
jf_tebukuro                      | Female  | ja-JP    | Japan 🇯🇵 (Needs misaki[ja])
jm_kumo                          | Male    | ja-JP    | Japan 🇯🇵 (Needs misaki[ja])
pf_dora                          | Female  | pt-BR    | Brazil 🇧🇷
pm_alex                          | Male    | pt-BR    | Brazil 🇧🇷
pm_santa                         | Male    | pt-BR    | Brazil 🇧🇷
zf_xiaobei                       | Female  | zh-CN    | China 🇨🇳 (Needs misaki[zh])
zf_xiaoni                        | Female  | zh-CN    | China 🇨🇳 (Needs misaki[zh])
zf_xiaoxiao                      | Female  | zh-CN    | China 🇨🇳 (Needs misaki[zh])
zf_xiaoyi                        | Female  | zh-CN    | China 🇨🇳 (Needs misaki[zh])
zm_yunjian                       | Male    | zh-CN    | China 🇨🇳 (Needs misaki[zh])
zm_yunxi                         | Male    | zh-CN    | China 🇨🇳 (Needs misaki[zh])
zm_yunxia                        | Male    | zh-CN    | China 🇨🇳 (Needs misaki[zh])
zm_yunyang                       | Male    | zh-CN    | China 🇨🇳 (Needs misaki[zh])

### Edge-TTS (Microsoft Cloud)
Use the --engine edge flag to access a massive library of high-speed, multilingual voices.

Voice                            | Gender  | Locale   | Country / Language
---------------------------------|---------|----------|-------------------
af-ZA-AdriNeural                 | Female  | af-ZA    | South Africa 🇿🇦
af-ZA-WillemNeural               | Male    | af-ZA    | South Africa 🇿🇦
am-ET-MekdesNeural               | Female  | am-ET    | Ethiopia 🇪🇹
am-ET-AmehaNeural                | Male    | am-ET    | Ethiopia 🇪🇹
ar-AE-FatimaNeural               | Female  | ar-AE    | UAE 🇦🇪
ar-AE-HamdanNeural               | Male    | ar-AE    | UAE 🇦🇪
ar-BH-LailaNeural                | Female  | ar-BH    | Bahrain 🇧🇭
ar-BH-AliNeural                  | Male    | ar-BH    | Bahrain 🇧🇭
ar-DZ-AminaNeural                | Female  | ar-DZ    | Algeria 🇩🇿
ar-DZ-IsmaelNeural               | Male    | ar-DZ    | Algeria 🇩🇿
ar-EG-SalmaNeural                | Female  | ar-EG    | Egypt 🇪🇬
ar-EG-ShakirNeural               | Male    | ar-EG    | Egypt 🇪🇬
ar-IQ-RanaNeural                 | Female  | ar-IQ    | Iraq 🇮🇶
ar-IQ-BasselNeural               | Male    | ar-IQ    | Iraq 🇮🇶
ar-JO-SanaNeural                 | Female  | ar-JO    | Jordan 🇯🇴
ar-JO-TaimNeural                 | Male    | ar-JO    | Jordan 🇯🇴
ar-KW-NouraNeural                | Female  | ar-KW    | Kuwait 🇰🇼
ar-KW-FahedNeural                | Male    | ar-KW    | Kuwait 🇰🇼
ar-LB-LaylaNeural                | Female  | ar-LB    | Lebanon 🇱🇧
ar-LB-RamiNeural                 | Male    | ar-LB    | Lebanon 🇱🇧
ar-LY-ImanNeural                 | Female  | ar-LY    | Libya 🇱🇾
ar-LY-OmarNeural                 | Male    | ar-LY    | Libya 🇱🇾
ar-MA-MounaNeural                | Female  | ar-MA    | Morocco 🇲🇦
ar-MA-JamalNeural                | Male    | ar-MA    | Morocco 🇲🇦
ar-OM-AyshaNeural                | Female  | ar-OM    | Oman 🇴🇲
ar-OM-AbdullahNeural             | Male    | ar-OM    | Oman 🇴🇲
ar-QA-AmalNeural                 | Female  | ar-QA    | Qatar 🇶🇦
ar-QA-MoazNeural                 | Male    | ar-QA    | Qatar 🇶🇦
ar-SA-ZariyahNeural              | Female  | ar-SA    | Saudi Arabia 🇸🇦
ar-SA-HamedNeural                | Male    | ar-SA    | Saudi Arabia 🇸🇦
ar-SY-AmanyNeural                | Female  | ar-SY    | Syria 🇸🇾
ar-SY-LaithNeural                | Male    | ar-SY    | Syria 🇸🇾
ar-TN-ReemNeural                 | Female  | ar-TN    | Tunisia 🇹🇳
ar-TN-HediNeural                 | Male    | ar-TN    | Tunisia 🇹🇳
ar-YE-MaryamNeural               | Female  | ar-YE    | Yemen 🇾🇪
ar-YE-SalehNeural                | Male    | ar-YE    | Yemen 🇾🇪
az-AZ-BanuNeural                 | Female  | az-AZ    | Azerbaijan 🇦🇿
az-AZ-BabekNeural                | Male    | az-AZ    | Azerbaijan 🇦🇿
bg-BG-KalinaNeural               | Female  | bg-BG    | Bulgaria 🇧🇬
bg-BG-BorislavNeural             | Male    | bg-BG    | Bulgaria 🇧🇬
bn-BD-NabanitaNeural             | Female  | bn-BD    | Bangladesh 🇧🇩
bn-BD-PradeepNeural              | Male    | bn-BD    | Bangladesh 🇧🇩
bn-IN-TanishaaNeural             | Female  | bn-IN    | India 🇮🇳
bn-IN-BashkarNeural              | Male    | bn-IN    | India 🇮🇳
bs-BA-VesnaNeural                | Female  | bs-BA    | Bosnia 🇧🇦
bs-BA-GoranNeural                | Male    | bs-BA    | Bosnia 🇧🇦
ca-ES-JoanaNeural                | Female  | ca-ES    | Spain 🇪🇸
ca-ES-EnricNeural                | Male    | ca-ES    | Spain 🇪🇸
cs-CZ-VlastaNeural               | Female  | cs-CZ    | Czechia 🇨🇿
cs-CZ-AntoninNeural              | Male    | cs-CZ    | Czechia 🇨🇿
cy-GB-NiaNeural                  | Female  | cy-GB    | United Kingdom 🇬🇧
cy-GB-AledNeural                 | Male    | cy-GB    | United Kingdom 🇬🇧
da-DK-ChristelNeural             | Female  | da-DK    | Denmark 🇩🇰
da-DK-JeppeNeural                | Male    | da-DK    | Denmark 🇩🇰
de-AT-IngridNeural               | Female  | de-AT    | Austria 🇦🇹
de-AT-JonasNeural                | Male    | de-AT    | Austria 🇦🇹
de-CH-LeniNeural                 | Female  | de-CH    | Switzerland 🇨🇭
de-CH-JanNeural                  | Male    | de-CH    | Switzerland 🇨🇭
de-DE-AmalaNeural                | Female  | de-DE    | Germany 🇩🇪
de-DE-KatjaNeural                | Female  | de-DE    | Germany 🇩🇪
de-DE-SeraphinaMultilingualNeural | Female  | de-DE    | Germany 🇩🇪
de-DE-ConradNeural               | Male    | de-DE    | Germany 🇩🇪
de-DE-FlorianMultilingualNeural  | Male    | de-DE    | Germany 🇩🇪
de-DE-KillianNeural              | Male    | de-DE    | Germany 🇩🇪
el-GR-AthinaNeural               | Female  | el-GR    | Greece 🇬🇷
el-GR-NestorasNeural             | Male    | el-GR    | Greece 🇬🇷
en-AU-NatashaNeural              | Female  | en-AU    | Australia 🇦🇺
en-AU-WilliamMultilingualNeural  | Male    | en-AU    | Australia 🇦🇺
en-CA-ClaraNeural                | Female  | en-CA    | Canada 🇨🇦
en-CA-LiamNeural                 | Male    | en-CA    | Canada 🇨🇦
en-GB-LibbyNeural                | Female  | en-GB    | United Kingdom 🇬🇧
en-GB-MaisieNeural               | Female  | en-GB    | United Kingdom 🇬🇧
en-GB-SoniaNeural                | Female  | en-GB    | United Kingdom 🇬🇧
en-GB-RyanNeural                 | Male    | en-GB    | United Kingdom 🇬🇧
en-GB-ThomasNeural               | Male    | en-GB    | United Kingdom 🇬🇧
en-HK-YanNeural                  | Female  | en-HK    | Hong Kong 🇭🇰
en-HK-SamNeural                  | Male    | en-HK    | Hong Kong 🇭🇰
en-IE-EmilyNeural                | Female  | en-IE    | Ireland 🇮🇪
en-IE-ConnorNeural               | Male    | en-IE    | Ireland 🇮🇪
en-IN-NeerjaExpressiveNeural     | Female  | en-IN    | India 🇮🇳
en-IN-NeerjaNeural               | Female  | en-IN    | India 🇮🇳
en-IN-PrabhatNeural              | Male    | en-IN    | India 🇮🇳
en-KE-AsiliaNeural               | Female  | en-KE    | Kenya 🇰🇪
en-KE-ChilembaNeural             | Male    | en-KE    | Kenya 🇰🇪
en-NG-EzinneNeural               | Female  | en-NG    | Nigeria 🇳🇬
en-NG-AbeoNeural                 | Male    | en-NG    | Nigeria 🇳🇬
en-NZ-MollyNeural                | Female  | en-NZ    | New Zealand 🇳🇿
en-NZ-MitchellNeural             | Male    | en-NZ    | New Zealand 🇳🇿
en-PH-RosaNeural                 | Female  | en-PH    | Philippines 🇵🇭
en-PH-JamesNeural                | Male    | en-PH    | Philippines 🇵🇭
en-SG-LunaNeural                 | Female  | en-SG    | Singapore 🇸🇬
en-SG-WayneNeural                | Male    | en-SG    | Singapore 🇸🇬
en-TZ-ImaniNeural                | Female  | en-TZ    | Tanzania 🇹🇿
en-TZ-ElimuNeural                | Male    | en-TZ    | Tanzania 🇹🇿
en-US-AnaNeural                  | Female  | en-US    | United States 🇺🇸
en-US-AriaNeural                 | Female  | en-US    | United States 🇺🇸
en-US-AvaMultilingualNeural      | Female  | en-US    | United States 🇺🇸
en-US-AvaNeural                  | Female  | en-US    | United States 🇺🇸
en-US-EmmaMultilingualNeural     | Female  | en-US    | United States 🇺🇸
en-US-EmmaNeural                 | Female  | en-US    | United States 🇺🇸
en-US-JennyNeural                | Female  | en-US    | United States 🇺🇸
en-US-MichelleNeural             | Female  | en-US    | United States 🇺🇸
en-US-AndrewMultilingualNeural   | Male    | en-US    | United States 🇺🇸
en-US-AndrewNeural               | Male    | en-US    | United States 🇺🇸
en-US-BrianMultilingualNeural    | Male    | en-US    | United States 🇺🇸
en-US-BrianNeural                | Male    | en-US    | United States 🇺🇸
en-US-ChristopherNeural          | Male    | en-US    | United States 🇺🇸
en-US-EricNeural                 | Male    | en-US    | United States 🇺🇸
en-US-GuyNeural                  | Male    | en-US    | United States 🇺🇸
en-US-RogerNeural                | Male    | en-US    | United States 🇺🇸
en-US-SteffanNeural              | Male    | en-US    | United States 🇺🇸
en-ZA-LeahNeural                 | Female  | en-ZA    | South Africa 🇿🇦
en-ZA-LukeNeural                 | Male    | en-ZA    | South Africa 🇿🇦
es-AR-ElenaNeural                | Female  | es-AR    | Argentina 🇦🇷
es-AR-TomasNeural                | Male    | es-AR    | Argentina 🇦🇷
es-BO-SofiaNeural                | Female  | es-BO    | Bolivia 🇧🇴
es-BO-MarceloNeural              | Male    | es-BO    | Bolivia 🇧🇴
es-CL-CatalinaNeural             | Female  | es-CL    | Chile 🇨🇱
es-CL-LorenzoNeural              | Male    | es-CL    | Chile 🇨🇱
es-CO-SalomeNeural               | Female  | es-CO    | Colombia 🇨🇴
es-CO-GonzaloNeural              | Male    | es-CO    | Colombia 🇨🇴
es-CR-MariaNeural                | Female  | es-CR    | Costa Rica 🇨🇷
es-CR-JuanNeural                 | Male    | es-CR    | Costa Rica 🇨🇷
es-CU-BelkysNeural               | Female  | es-CU    | Cuba 🇨🇺
es-CU-ManuelNeural               | Male    | es-CU    | Cuba 🇨🇺
es-DO-RamonaNeural               | Female  | es-DO    | Dominican Rep. 🇩🇴
es-DO-EmilioNeural               | Male    | es-DO    | Dominican Rep. 🇩🇴
es-EC-AndreaNeural               | Female  | es-EC    | Ecuador 🇪🇨
es-EC-LuisNeural                 | Male    | es-EC    | Ecuador 🇪🇨
es-ES-ElviraNeural               | Female  | es-ES    | Spain 🇪🇸
es-ES-XimenaNeural               | Female  | es-ES    | Spain 🇪🇸
es-ES-AlvaroNeural               | Male    | es-ES    | Spain 🇪🇸
es-GQ-TeresaNeural               | Female  | es-GQ    | Equatorial Guinea 🇬🇶
es-GQ-JavierNeural               | Male    | es-GQ    | Equatorial Guinea 🇬🇶
es-GT-MartaNeural                | Female  | es-GT    | Guatemala 🇬🇹
es-GT-AndresNeural               | Male    | es-GT    | Guatemala 🇬🇹
es-HN-KarlaNeural                | Female  | es-HN    | Honduras 🇭🇳
es-HN-CarlosNeural               | Male    | es-HN    | Honduras 🇭🇳
es-MX-DaliaNeural                | Female  | es-MX    | Mexico 🇲🇽
es-MX-JorgeNeural                | Male    | es-MX    | Mexico 🇲🇽
es-NI-YolandaNeural              | Female  | es-NI    | Nicaragua 🇳🇮
es-NI-FedericoNeural             | Male    | es-NI    | Nicaragua 🇳🇮
es-PA-MargaritaNeural            | Female  | es-PA    | Panama 🇵🇦
es-PA-RobertoNeural              | Male    | es-PA    | Panama 🇵🇦
es-PE-CamilaNeural               | Female  | es-PE    | Peru 🇵🇪
es-PE-AlexNeural                 | Male    | es-PE    | Peru 🇵🇪
es-PR-KarinaNeural               | Female  | es-PR    | Puerto Rico 🇵🇷
es-PR-VictorNeural               | Male    | es-PR    | Puerto Rico 🇵🇷
es-PY-TaniaNeural                | Female  | es-PY    | Paraguay 🇵🇾
es-PY-MarioNeural                | Male    | es-PY    | Paraguay 🇵🇾
es-SV-LorenaNeural               | Female  | es-SV    | El Salvador 🇸🇻
es-SV-RodrigoNeural              | Male    | es-SV    | El Salvador 🇸🇻
es-US-PalomaNeural               | Female  | es-US    | United States 🇺🇸
es-US-AlonsoNeural               | Male    | es-US    | United States 🇺🇸
es-UY-ValentinaNeural            | Female  | es-UY    | Uruguay 🇺🇾
es-UY-MateoNeural                | Male    | es-UY    | Uruguay 🇺🇾
es-VE-PaolaNeural                | Female  | es-VE    | Venezuela 🇻🇪
es-VE-SebastianNeural            | Male    | es-VE    | Venezuela 🇻🇪
et-EE-AnuNeural                  | Female  | et-EE    | Estonia 🇪🇪
et-EE-KertNeural                 | Male    | et-EE    | Estonia 🇪🇪
fa-IR-DilaraNeural               | Female  | fa-IR    | Iran 🇮🇷
fa-IR-FaridNeural                | Male    | fa-IR    | Iran 🇮🇷
fi-FI-NooraNeural                | Female  | fi-FI    | Finland 🇫🇮
fi-FI-HarriNeural                | Male    | fi-FI    | Finland 🇫🇮
fil-PH-BlessicaNeural            | Female  | fil-PH   | Philippines 🇵🇭
fil-PH-AngeloNeural              | Male    | fil-PH   | Philippines 🇵🇭
fr-BE-CharlineNeural             | Female  | fr-BE    | Belgium 🇧🇪
fr-BE-GerardNeural               | Male    | fr-BE    | Belgium 🇧🇪
fr-CA-SylvieNeural               | Female  | fr-CA    | Canada 🇨🇦
fr-CA-AntoineNeural              | Male    | fr-CA    | Canada 🇨🇦
fr-CA-JeanNeural                 | Male    | fr-CA    | Canada 🇨🇦
fr-CA-ThierryNeural              | Male    | fr-CA    | Canada 🇨🇦
fr-CH-ArianeNeural               | Female  | fr-CH    | Switzerland 🇨🇭
fr-CH-FabriceNeural              | Male    | fr-CH    | Switzerland 🇨🇭
fr-FR-DeniseNeural               | Female  | fr-FR    | France 🇫🇷
fr-FR-EloiseNeural               | Female  | fr-FR    | France 🇫🇷
fr-FR-VivienneMultilingualNeural | Female  | fr-FR    | France 🇫🇷
fr-FR-HenriNeural                | Male    | fr-FR    | France 🇫🇷
fr-FR-RemyMultilingualNeural     | Male    | fr-FR    | France 🇫🇷
ga-IE-OrlaNeural                 | Female  | ga-IE    | Ireland 🇮🇪
ga-IE-ColmNeural                 | Male    | ga-IE    | Ireland 🇮🇪
gl-ES-SabelaNeural               | Female  | gl-ES    | Spain 🇪🇸
gl-ES-RoiNeural                  | Male    | gl-ES    | Spain 🇪🇸
gu-IN-DhwaniNeural               | Female  | gu-IN    | India 🇮🇳
gu-IN-NiranjanNeural             | Male    | gu-IN    | India 🇮🇳
he-IL-HilaNeural                 | Female  | he-IL    | Israel 🇮🇱
he-IL-AvriNeural                 | Male    | he-IL    | Israel 🇮🇱
hi-IN-SwaraNeural                | Female  | hi-IN    | India 🇮🇳
hi-IN-MadhurNeural               | Male    | hi-IN    | India 🇮🇳
hr-HR-GabrijelaNeural            | Female  | hr-HR    | Croatia 🇭🇷
hr-HR-SreckoNeural               | Male    | hr-HR    | Croatia 🇭🇷
hu-HU-NoemiNeural                | Female  | hu-HU    | Hungary 🇭🇺
hu-HU-TamasNeural                | Male    | hu-HU    | Hungary 🇭🇺
id-ID-GadisNeural                | Female  | id-ID    | Indonesia 🇮🇩
id-ID-ArdiNeural                 | Male    | id-ID    | Indonesia 🇮🇩
is-IS-GudrunNeural               | Female  | is-IS    | Iceland 🇮🇸
is-IS-GunnarNeural               | Male    | is-IS    | Iceland 🇮🇸
it-IT-ElsaNeural                 | Female  | it-IT    | Italy 🇮🇹
it-IT-IsabellaNeural             | Female  | it-IT    | Italy 🇮🇹
it-IT-DiegoNeural                | Male    | it-IT    | Italy 🇮🇹
it-IT-GiuseppeMultilingualNeural | Male    | it-IT    | Italy 🇮🇹
iu-Cans-CA-SiqiniqNeural         | Female  | iu-Cans-CA | Inuktitut (Syllabics, Canada)
iu-Cans-CA-TaqqiqNeural          | Male    | iu-Cans-CA | Inuktitut (Syllabics, Canada)
iu-Latn-CA-SiqiniqNeural         | Female  | iu-Latn-CA | Inuktitut (Latin, Canada)
iu-Latn-CA-TaqqiqNeural          | Male    | iu-Latn-CA | Inuktitut (Latin, Canada)
ja-JP-NanamiNeural               | Female  | ja-JP    | Japan 🇯🇵
ja-JP-KeitaNeural                | Male    | ja-JP    | Japan 🇯🇵
jv-ID-SitiNeural                 | Female  | jv-ID    | Indonesia 🇮🇩
jv-ID-DimasNeural                | Male    | jv-ID    | Indonesia 🇮🇩
ka-GE-EkaNeural                  | Female  | ka-GE    | Georgia 🇬🇪
ka-GE-GiorgiNeural               | Male    | ka-GE    | Georgia 🇬🇪
kk-KZ-AigulNeural                | Female  | kk-KZ    | Kazakhstan 🇰🇿
kk-KZ-DauletNeural               | Male    | kk-KZ    | Kazakhstan 🇰🇿
km-KH-SreymomNeural              | Female  | km-KH    | Cambodia 🇰🇭
km-KH-PisethNeural               | Male    | km-KH    | Cambodia 🇰🇭
kn-IN-SapnaNeural                | Female  | kn-IN    | India 🇮🇳
kn-IN-GaganNeural                | Male    | kn-IN    | India 🇮🇳
ko-KR-SunHiNeural                | Female  | ko-KR    | South Korea 🇰🇷
ko-KR-HyunsuMultilingualNeural   | Male    | ko-KR    | South Korea 🇰🇷
ko-KR-InJoonNeural               | Male    | ko-KR    | South Korea 🇰🇷
lo-LA-KeomanyNeural              | Female  | lo-LA    | Laos 🇱🇦
lo-LA-ChanthavongNeural          | Male    | lo-LA    | Laos 🇱🇦
lt-LT-OnaNeural                  | Female  | lt-LT    | Lithuania 🇱🇹
lt-LT-LeonasNeural               | Male    | lt-LT    | Lithuania 🇱🇹
lv-LV-EveritaNeural              | Female  | lv-LV    | Latvia 🇱🇻
lv-LV-NilsNeural                 | Male    | lv-LV    | Latvia 🇱🇻
mk-MK-MarijaNeural               | Female  | mk-MK    | North Macedonia 🇲🇰
mk-MK-AleksandarNeural           | Male    | mk-MK    | North Macedonia 🇲🇰
ml-IN-SobhanaNeural              | Female  | ml-IN    | India 🇮🇳
ml-IN-MidhunNeural               | Male    | ml-IN    | India 🇮🇳
mn-MN-YesuiNeural                | Female  | mn-MN    | Mongolia 🇲🇳
mn-MN-BataaNeural                | Male    | mn-MN    | Mongolia 🇲🇳
mr-IN-AarohiNeural               | Female  | mr-IN    | India 🇮🇳
mr-IN-ManoharNeural              | Male    | mr-IN    | India 🇮🇳
ms-MY-YasminNeural               | Female  | ms-MY    | Malaysia 🇲🇾
ms-MY-OsmanNeural                | Male    | ms-MY    | Malaysia 🇲🇾
mt-MT-GraceNeural                | Female  | mt-MT    | Malta 🇲🇹
mt-MT-JosephNeural               | Male    | mt-MT    | Malta 🇲🇹
my-MM-NilarNeural                | Female  | my-MM    | Myanmar 🇲🇲
my-MM-ThihaNeural                | Male    | my-MM    | Myanmar 🇲🇲
nb-NO-PernilleNeural             | Female  | nb-NO    | Norway 🇳🇴
nb-NO-FinnNeural                 | Male    | nb-NO    | Norway 🇳🇴
ne-NP-HemkalaNeural              | Female  | ne-NP    | Nepal 🇳🇵
ne-NP-SagarNeural                | Male    | ne-NP    | Nepal 🇳🇵
nl-BE-DenaNeural                 | Female  | nl-BE    | Belgium 🇧🇪
nl-BE-ArnaudNeural               | Male    | nl-BE    | Belgium 🇧🇪
nl-NL-ColetteNeural              | Female  | nl-NL    | Netherlands 🇳🇱
nl-NL-FennaNeural                | Female  | nl-NL    | Netherlands 🇳🇱
nl-NL-MaartenNeural              | Male    | nl-NL    | Netherlands 🇳🇱
pl-PL-ZofiaNeural                | Female  | pl-PL    | Poland 🇵🇱
pl-PL-MarekNeural                | Male    | pl-PL    | Poland 🇵🇱
ps-AF-LatifaNeural               | Female  | ps-AF    | Afghanistan 🇦🇫
ps-AF-GulNawazNeural             | Male    | ps-AF    | Afghanistan 🇦🇫
pt-BR-FranciscaNeural            | Female  | pt-BR    | Brazil 🇧🇷
pt-BR-ThalitaMultilingualNeural  | Female  | pt-BR    | Brazil 🇧🇷
pt-BR-AntonioNeural              | Male    | pt-BR    | Brazil 🇧🇷
pt-PT-RaquelNeural               | Female  | pt-PT    | Portugal 🇵🇹
pt-PT-DuarteNeural               | Male    | pt-PT    | Portugal 🇵🇹
ro-RO-AlinaNeural                | Female  | ro-RO    | Romania 🇷🇴
ro-RO-EmilNeural                 | Male    | ro-RO    | Romania 🇷🇴
ru-RU-SvetlanaNeural             | Female  | ru-RU    | Russia 🇷🇺
ru-RU-DmitryNeural               | Male    | ru-RU    | Russia 🇷🇺
si-LK-ThiliniNeural              | Female  | si-LK    | Sri Lanka 🇱🇰
si-LK-SameeraNeural              | Male    | si-LK    | Sri Lanka 🇱🇰
sk-SK-ViktoriaNeural             | Female  | sk-SK    | Slovakia 🇸🇰
sk-SK-LukasNeural                | Male    | sk-SK    | Slovakia 🇸🇰
sl-SI-PetraNeural                | Female  | sl-SI    | Slovenia 🇸🇮
sl-SI-RokNeural                  | Male    | sl-SI    | Slovenia 🇸🇮
so-SO-UbaxNeural                 | Female  | so-SO    | Somalia 🇸🇴
so-SO-MuuseNeural                | Male    | so-SO    | Somalia 🇸🇴
sq-AL-AnilaNeural                | Female  | sq-AL    | Albania 🇦🇱
sq-AL-IlirNeural                 | Male    | sq-AL    | Albania 🇦🇱
sr-RS-SophieNeural               | Female  | sr-RS    | Serbia 🇷🇸
sr-RS-NicholasNeural             | Male    | sr-RS    | Serbia 🇷🇸
su-ID-TutiNeural                 | Female  | su-ID    | Indonesia 🇮🇩
su-ID-JajangNeural               | Male    | su-ID    | Indonesia 🇮🇩
sv-SE-SofieNeural                | Female  | sv-SE    | Sweden 🇸🇪
sv-SE-MattiasNeural              | Male    | sv-SE    | Sweden 🇸🇪
sw-KE-ZuriNeural                 | Female  | sw-KE    | Kenya 🇰🇪
sw-KE-RafikiNeural               | Male    | sw-KE    | Kenya 🇰🇪
sw-TZ-RehemaNeural               | Female  | sw-TZ    | Tanzania 🇹🇿
sw-TZ-DaudiNeural                | Male    | sw-TZ    | Tanzania 🇹🇿
ta-IN-PallaviNeural              | Female  | ta-IN    | India 🇮🇳
ta-IN-ValluvarNeural             | Male    | ta-IN    | India 🇮🇳
ta-LK-SaranyaNeural              | Female  | ta-LK    | Sri Lanka 🇱🇰
ta-LK-KumarNeural                | Male    | ta-LK    | Sri Lanka 🇱🇰
ta-MY-KaniNeural                 | Female  | ta-MY    | Malaysia 🇲🇾
ta-MY-SuryaNeural                | Male    | ta-MY    | Malaysia 🇲🇾
ta-SG-VenbaNeural                | Female  | ta-SG    | Singapore 🇸🇬
ta-SG-AnbuNeural                 | Male    | ta-SG    | Singapore 🇸🇬
te-IN-ShrutiNeural               | Female  | te-IN    | India 🇮🇳
te-IN-MohanNeural                | Male    | te-IN    | India 🇮🇳
th-TH-PremwadeeNeural            | Female  | th-TH    | Thailand 🇹🇭
th-TH-NiwatNeural                | Male    | th-TH    | Thailand 🇹🇭
tr-TR-EmelNeural                 | Female  | tr-TR    | Turkey 🇹🇷
tr-TR-AhmetNeural                | Male    | tr-TR    | Turkey 🇹🇷
uk-UA-PolinaNeural               | Female  | uk-UA    | Ukraine 🇺🇦
uk-UA-OstapNeural                | Male    | uk-UA    | Ukraine 🇺🇦
ur-IN-GulNeural                  | Female  | ur-IN    | India 🇮🇳
ur-IN-SalmanNeural               | Male    | ur-IN    | India 🇮🇳
ur-PK-UzmaNeural                 | Female  | ur-PK    | Pakistan 🇵🇰
ur-PK-AsadNeural                 | Male    | ur-PK    | Pakistan 🇵🇰
uz-UZ-MadinaNeural               | Female  | uz-UZ    | Uzbekistan 🇺🇿
uz-UZ-SardorNeural               | Male    | uz-UZ    | Uzbekistan 🇺🇿
vi-VN-HoaiMyNeural               | Female  | vi-VN    | Vietnam 🇻🇳
vi-VN-NamMinhNeural              | Male    | vi-VN    | Vietnam 🇻🇳
zh-CN-XiaoxiaoNeural             | Female  | zh-CN    | China 🇨🇳
zh-CN-XiaoyiNeural               | Female  | zh-CN    | China 🇨🇳
zh-CN-YunjianNeural              | Male    | zh-CN    | China 🇨🇳
zh-CN-YunxiNeural                | Male    | zh-CN    | China 🇨🇳
zh-CN-YunxiaNeural               | Male    | zh-CN    | China 🇨🇳
zh-CN-YunyangNeural              | Male    | zh-CN    | China 🇨🇳
zh-CN-liaoning-XiaobeiNeural     | Female  | zh-CN-liaoning | China 🇨🇳
zh-CN-shaanxi-XiaoniNeural       | Female  | zh-CN-shaanxi | China 🇨🇳
zh-HK-HiuGaaiNeural              | Female  | zh-HK    | Hong Kong 🇭🇰
zh-HK-HiuMaanNeural              | Female  | zh-HK    | Hong Kong 🇭🇰
zh-HK-WanLungNeural              | Male    | zh-HK    | Hong Kong 🇭🇰
zh-TW-HsiaoChenNeural            | Female  | zh-TW    | Taiwan 🇹🇼
zh-TW-HsiaoYuNeural              | Female  | zh-TW    | Taiwan 🇹🇼
zh-TW-YunJheNeural               | Male    | zh-TW    | Taiwan 🇹🇼
zu-ZA-ThandoNeural               | Female  | zu-ZA    | South Africa 🇿🇦
zu-ZA-ThembaNeural               | Male    | zu-ZA    | South Africa 🇿🇦

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
