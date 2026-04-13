import http.client
import json
import ssl
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Union


API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
API_HOST = "integrate.api.nvidia.com"
API_PATH = "/v1/chat/completions"


@dataclass
class ChatResult:
    content: str
    raw: Dict[str, Any]


class ChatNVIDIA:
    """
    Minimal compatibility wrapper for the ChatNVIDIA constructor pattern used in this project.
    It calls NVIDIA's OpenAI-compatible chat completions endpoint directly via urllib.
    """

    def __init__(
        self,
        model: str,
        api_key: str,
        temperature: float = 1.0,
        top_p: float = 1.0,
        max_tokens: int = 16384,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: int = 120,
        min_interval_seconds: float = 1.6,
    ) -> None:
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.extra_body = extra_body or {}
        self.timeout = timeout
        self.min_interval_seconds = min_interval_seconds
        self._last_request_ts = 0.0
        self._ssl_context = ssl.create_default_context()

    def _normalize_messages(self, messages: Union[str, List[Dict[str, str]], Iterable[Dict[str, str]]]):
        if isinstance(messages, str):
            return [{"role": "user", "content": messages}]
        return list(messages)

    def _rate_limit(self) -> None:
        elapsed = time.time() - self._last_request_ts
        if elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)

    def invoke(self, messages: Union[str, List[Dict[str, str]], Iterable[Dict[str, str]]]) -> ChatResult:
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY is required.")
        payload = {
            "model": self.model,
            "messages": self._normalize_messages(messages),
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
        }
        payload.update(self.extra_body)
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        self._rate_limit()
        connection = None
        try:
            connection = http.client.HTTPSConnection(API_HOST, timeout=self.timeout, context=self._ssl_context)
            connection.request("POST", API_PATH, body=data, headers=headers)
            response = connection.getresponse()
            response_bytes = response.read()
            if response.status >= 400:
                body_text = response_bytes.decode("utf-8", errors="replace")
                raise RuntimeError(f"HTTP {response.status}: {body_text}")
            raw = json.loads(response_bytes.decode("utf-8"))
        finally:
            self._last_request_ts = time.time()
            try:
                connection.close()
            except Exception:
                pass

        content = raw["choices"][0]["message"]["content"]
        return ChatResult(content=content, raw=raw)

    def invoke_with_retries(
        self,
        messages: Union[str, List[Dict[str, str]], Iterable[Dict[str, str]]],
        max_retries: int = 5,
    ) -> ChatResult:
        delay = 4.0
        last_error = None
        for attempt in range(max_retries):
            try:
                return self.invoke(messages)
            except RuntimeError as exc:
                message = str(exc)
                last_error = exc
                retriable = any(message.startswith(f"HTTP {code}:") for code in ["429", "500", "502", "503", "504"])
                if retriable and attempt < max_retries - 1:
                    time.sleep(delay)
                    delay = min(delay * 2, 60.0)
                    continue
                raise
            except Exception as exc:
                last_error = exc
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay = min(delay * 2, 60.0)
                    continue
                raise
        raise last_error if last_error else RuntimeError("NVIDIA request failed.")
