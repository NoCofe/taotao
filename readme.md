# Voya Voice Agent Demo

This repository contains a simple demo showing how to control a web browser
using voice commands. It relies on `faster-whisper` for speech recognition
and `selenium` for automating Chrome.

## Requirements

```bash
pip install faster-whisper==0.10.*
pip install sounddevice==0.4.*
pip install numpy
pip install selenium==4.21.*
# optional for voice feedback
pip install pyttsx3==2.90
```

Make sure you have a matching `chromedriver` for your Chrome installation in
`$PATH`. The whisper model can be `tiny` or `base` for faster inference.

## Run

```bash
python voya_voice_agent.py
```

The console will show `按空格说话 (press Enter)...`. Press **Enter** (simulating
space) to start recording, press again to stop. The recognized text is mapped
to an intent and executed in Chrome.
