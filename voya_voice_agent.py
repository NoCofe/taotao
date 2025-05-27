# coding: utf-8
"""Voya Voice Agent: convert voice commands into browser actions.

This script demonstrates a desktop voice assistant that listens for speech,
transcribes it with faster-whisper, resolves the text into an intent, and
executes the corresponding browser action via Selenium.

Dependencies (see README for versions):
    - faster-whisper
    - sounddevice
    - numpy
    - selenium
    - pyttsx3 (optional for TTS)

The code is organized into small helper classes:
    Recorder         - handle microphone recording using sounddevice
    ASRStream        - use faster-whisper to transcribe audio frames
    IntentResolver   - map spoken text to an Intent object
    FunctionDispatcher - execute the intent via BrowserFunctions
    BrowserFunctions - open URLs or perform web searches via Selenium
    TTSFeedback      - optional text-to-speech output

Potential improvements:
    * Integrate with a full-featured LLM to resolve intents dynamically.
    * Replace Selenium with mobile-specific logic (e.g., ADB commands).
    * Add UI or hotkey integration to fit different environments.
"""

from __future__ import annotations

import queue
import threading
import time
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

import numpy as np

try:
    import sounddevice as sd
except ImportError:  # pragma: no cover - optional dependency check
    sd = None

try:
    from faster_whisper import WhisperModel
except ImportError:  # pragma: no cover - optional dependency check
    WhisperModel = None

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
except ImportError:  # pragma: no cover - optional dependency check
    webdriver = None

try:
    import pyttsx3
except ImportError:  # pragma: no cover - optional dependency check
    pyttsx3 = None


@dataclass
class Intent:
    name: str
    args: Dict[str, str]


class Recorder:
    """Record audio from microphone when start_stream is called."""

    def __init__(self, samplerate: int = 16000, channels: int = 1):
        self.samplerate = samplerate
        self.channels = channels
        self._q: queue.Queue[np.ndarray] = queue.Queue()
        self._stream: Optional[sd.InputStream] = None

    def start_stream(self) -> None:
        if sd is None:
            raise RuntimeError("sounddevice is required for recording")

        self._q = queue.Queue()
        self._stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype="int16",
            callback=self._callback,
        )
        self._stream.start()

    def _callback(self, indata, frames, time_info, status):
        if status:
            print("Recorder status:", status)
        self._q.put(indata.copy())

    def stop_stream(self) -> np.ndarray:
        if self._stream is None:
            return np.array([], dtype=np.int16)
        self._stream.stop()
        self._stream.close()
        self._stream = None
        frames = []
        while not self._q.empty():
            frames.append(self._q.get())
        if not frames:
            return np.array([], dtype=np.int16)
        return np.concatenate(frames, axis=0)


class ASRStream:
    """Stream audio to faster-whisper for transcription."""

    def __init__(self, model_size: str = "tiny"):
        if WhisperModel is None:
            raise RuntimeError("faster-whisper is required for ASR")
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, frames: np.ndarray) -> str:
        if frames.size == 0:
            return ""
        audio = frames.astype(np.float32) / np.iinfo(np.int16).max
        segments, _ = self.model.transcribe(
            audio,
            beam_size=1,
            vad_filter=True,
            word_timestamps=False,
        )
        text = " ".join(s.text.strip() for s in segments)
        return text.strip()


class IntentResolver:
    """Resolve raw text into an Intent object."""

    ALIAS = {
        "谷歌": "https://www.google.com",
        "百度": "https://www.baidu.com",
    }

    @classmethod
    def resolve(cls, text: str) -> Intent:
        text = text.strip()
        if not text:
            return Intent("NONE", {})

        if text.startswith(("打开", "帮我打开", "进入", "go to")):
            key = text
            for token in ("打开", "帮我", "进入", "go to"):
                key = key.replace(token, "")
            key = key.strip()
            url = cls.ALIAS.get(key, f"https://{key}")
            return Intent("OPEN_SITE", {"url": url})
        else:
            return Intent("SEARCH_WEB", {"query": text})


class BrowserFunctions:
    """Wrapper around Selenium to control Chrome."""

    def __init__(self):
        if webdriver is None:
            raise RuntimeError("selenium is required for browser control")
        self.driver = webdriver.Chrome()

    def open_url(self, url: str) -> str:
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        return f"已为你打开 {url}"

    def search_web(self, query: str) -> str:
        url = f"https://www.google.com/search?q={query}"
        return self.open_url(url)


class FunctionDispatcher:
    """Dispatch intent to the appropriate browser function."""

    def __init__(self, browser: BrowserFunctions):
        self.browser = browser
        self._map = {
            "OPEN_SITE": self.browser.open_url,
            "SEARCH_WEB": self.browser.search_web,
        }

    def dispatch(self, intent: Intent) -> str:
        func = self._map.get(intent.name)
        if func is None:
            return "Unknown command"
        return func(**intent.args)


class TTSFeedback:
    """Optional text-to-speech feedback using pyttsx3."""

    def __init__(self):
        if pyttsx3 is None:
            raise RuntimeError("pyttsx3 is required for TTS")
        self.engine = pyttsx3.init()

    def speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()


def space_pressed() -> bool:
    """Check if spacebar is currently pressed.

    This simple implementation polls input() to start/stop recording.
    For a production app, integrate with keyboard events or GUI hooks.
    """

    try:
        # Non-blocking check: input() used for simplicity.
        # User should press Enter/Return to simulate space.
        return input() == ""
    except EOFError:
        return False


def main():
    print("按空格说话 (press Enter)...")
    recorder = Recorder()
    asr = ASRStream()
    browser = BrowserFunctions()
    dispatcher = FunctionDispatcher(browser)
    tts = TTSFeedback() if pyttsx3 is not None else None

    while True:
        if space_pressed():
            recorder.start_stream()
            print("Recording... press Enter again to stop.")
            space_pressed()  # Wait for release
            frames = recorder.stop_stream()
            print("Transcribing...")
            text = asr.transcribe(frames)
            print("You said:", text)
            intent = IntentResolver.resolve(text)
            result = dispatcher.dispatch(intent)
            print("Done:", result)
            if tts is not None:
                tts.speak(result)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
