"""
Доменные важные значения.
"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Language:
    """
    Язык перевода.
    """
    code: str


    def __post_init__(self):
        if not re.match(r'^[a-z]{2}$', self.code):
            raise ValueError(
                f"Invalid language code: '{self.code}'. "
                f"Must be exactly 2 lowercase latin letters (e.g., 'ru', 'en')"
            )
    
    def __str__(self) -> str:
        return self.code


@dataclass(frozen=True)
class XPath:
    """
    Адрес элемента в XML документе.
    """
    path: str
    is_attribute: bool = False


    def __post_init__(self):
        if not self.path or not self.path.strip():
            raise ValueError("XPath cannot be empty")

    def __str__(self) -> str:
        prefix = "@" if self.is_attribute else ""
        return f"{prefix}{self.path}"


@dataclass(frozen=True)
class TranslationPair:
    """
    Пара "оригинал -> перевод" с привязкой к месту в XML.
    """
    original: str
    translated: str
    xpath: XPath


    def is_translated(self) -> bool:
        """
        Переведен ли текст.
        """
        return bool(self.translated and self.translated.strip())

    def __post_init__(self):
        if not self.original or not self.original.strip():
            raise ValueError("Original value cannot be empty")

    def __str__(self) -> str:
        return f"'{self.original}' -> '{self.translated}'"