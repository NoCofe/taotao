# coding: utf-8
"""Simple LLM Agent skeleton using the voice-browser system prompt.

This module defines stub implementations of the native browser APIs and a
basic agent structure that can handle user messages and return either a tool
call JSON or a natural language response.

All tool implementations return mock data for demonstration purposes.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


class BrowserAPI:
    """Mock implementations of browser native APIs."""

    @staticmethod
    def open_url(url: str) -> Dict[str, Any]:
        print(f"[MOCK] open_url called with url={url}")
        return {"status": "success", "action": "open_url", "url": url}

    @staticmethod
    def search_web(query: str) -> Dict[str, Any]:
        print(f"[MOCK] search_web called with query={query}")
        return {"status": "success", "action": "search_web", "query": query}

    @staticmethod
    def go_back() -> Dict[str, Any]:
        print("[MOCK] go_back called")
        return {"status": "success", "action": "go_back"}

    @staticmethod
    def go_forward() -> Dict[str, Any]:
        print("[MOCK] go_forward called")
        return {"status": "success", "action": "go_forward"}

    @staticmethod
    def reload_page() -> Dict[str, Any]:
        print("[MOCK] reload_page called")
        return {"status": "success", "action": "reload_page"}

    @staticmethod
    def new_tab(url: Optional[str] = None) -> Dict[str, Any]:
        print(f"[MOCK] new_tab called with url={url}")
        return {"status": "success", "action": "new_tab", "url": url}

    @staticmethod
    def close_tab(tab_id: int) -> Dict[str, Any]:
        print(f"[MOCK] close_tab called with tab_id={tab_id}")
        return {"status": "success", "action": "close_tab", "tab_id": tab_id}

    @staticmethod
    def scroll(direction: str, amount: Optional[str] = None) -> Dict[str, Any]:
        print(f"[MOCK] scroll called with direction={direction}, amount={amount}")
        return {
            "status": "success",
            "action": "scroll",
            "direction": direction,
            "amount": amount,
        }

    @staticmethod
    def summarize_content(style: str = "bullet") -> Dict[str, Any]:
        print(f"[MOCK] summarize_content called with style={style}")
        return {"status": "success", "action": "summarize_content", "style": style}

    @staticmethod
    def translate_content(target_lang: str) -> Dict[str, Any]:
        print(f"[MOCK] translate_content called with target_lang={target_lang}")
        return {
            "status": "success",
            "action": "translate_content",
            "target_lang": target_lang,
        }

    @staticmethod
    def generate_audio(format: str = "mp3") -> Dict[str, Any]:
        print(f"[MOCK] generate_audio called with format={format}")
        return {"status": "success", "action": "generate_audio", "format": format}

    @staticmethod
    def save_bookmark(title: Optional[str] = None, folder: Optional[str] = None) -> Dict[str, Any]:
        print(f"[MOCK] save_bookmark called with title={title}, folder={folder}")
        return {
            "status": "success",
            "action": "save_bookmark",
            "title": title,
            "folder": folder,
        }

    @staticmethod
    def add_to_reading_list(mode: str) -> Dict[str, Any]:
        print(f"[MOCK] add_to_reading_list called with mode={mode}")
        return {"status": "success", "action": "add_to_reading_list", "mode": mode}

    @staticmethod
    def create_note(content: str, source_url: Optional[str] = None, tags: Optional[list[str]] = None) -> Dict[str, Any]:
        print(f"[MOCK] create_note called with content={content}, source_url={source_url}, tags={tags}")
        return {
            "status": "success",
            "action": "create_note",
            "content": content,
            "source_url": source_url,
            "tags": tags,
        }

    @staticmethod
    def speak(text: str) -> Dict[str, Any]:
        print(f"[MOCK] speak called with text={text}")
        return {"status": "success", "action": "speak", "text": text}

    @staticmethod
    def get_context() -> Dict[str, Any]:
        print("[MOCK] get_context called")
        return {"status": "success", "action": "get_context", "context": {}}

    @staticmethod
    def set_clipboard(text: str) -> Dict[str, Any]:
        print(f"[MOCK] set_clipboard called with text={text}")
        return {"status": "success", "action": "set_clipboard", "text": text}


def call_model(messages: list[dict]) -> Dict[str, Any]:
    """Placeholder for calling an LLM to generate a response.

    Parameters
    ----------
    messages: list[dict]
        Chat history in OpenAI format.

    Returns
    -------
    dict
        Either a tool call JSON or a text response.
    """
    # In a real implementation, this function would invoke an LLM.
    # Here we return a fixed tool call as mock behaviour.
    print("[MOCK] call_model invoked")
    return {"name": "search_web", "arguments": {"query": "example search"}}


@dataclass
class LLMAgent:
    """Basic agent orchestrating model calls and tool execution."""

    system_prompt: str

    def handle_message(self, user_message: str) -> Any:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        model_reply = call_model(messages)
        if isinstance(model_reply, dict) and "name" in model_reply:
            func_name = model_reply["name"]
            args = model_reply.get("arguments", {})
            func = getattr(BrowserAPI, func_name, None)
            if func is None:
                raise ValueError(f"Unknown function: {func_name}")
            return func(**args)
        return model_reply


SYSTEM_PROMPT = """You are Voya Browser Voice-Agent. Use available functions to fulfill the user's request if possible."""


def demo():
    agent = LLMAgent(system_prompt=SYSTEM_PROMPT)
    user_input = input("User: ")
    result = agent.handle_message(user_input)
    print("Agent result:", json.dumps(result, indent=2))


if __name__ == "__main__":
    demo()
