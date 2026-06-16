"""
Адаптер для DeepSeek API через Ollama.
"""
import logging
from typing import Optional

import httpx

from src.domain.interfaces import LLMTranslator
from src.domain.exceptions import LLMCallError


logger = logging.getLogger(__name__)


class DeepSeekAdapter(LLMTranslator):
    """
    Клиент для DeepSeek через Ollama API.
    """
    def __init__(
        self,
        base_url: str,
        model: str = "deepseek-r1:7b",
        timeout: float = 60.0,
        max_retries: int = 3,
        temperature: float = 0.1,
        max_tokens: int = 2000,
        prompts_dir: str = "prompts"
    ):
        pass