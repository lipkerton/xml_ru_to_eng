"""
Адаптер для DeepSeek API через Ollama.
"""
import logging
from typing import Optional

import httpx

from src.domain.interfaces import LLMTranslator
from src.domain.exceptions import LLMCallError


logger = logging.getLogger(__name__)


class DeepSeekAdapter(LLMTranslator)