"""
Интерфейсы доменного слоя.
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain.entities import XMLDocument, Language
from src.domain.value_objects import TranslationPair


class XMLParser(ABC):
    """
    Интерфейс для парсинга XML.
    Его задача извлечь все фрагменты текста на русском языке.
    """
    @abstractmethod
    def extract_translatable_texts(self, document: XMLDocument) -> List[TranslationPair]:
        """
        Извлекает все тексты, которые требуют перевода.
        """
        ...


class XMLComposer(ABC):
    """
    Интерфейс для сборки XML.
    """
    @abstractmethod
    def apply_translations(self, document: XMLDocument, translations: List[TranslationPair]) -> str:
        ...


class LLMTranslator(ABC):
    """
    Интерфейс для языковой модели-переводчика.
    """

    @abstractmethod
    async def translate(
        self, text: str, source_language: str, target_language: str
    ) -> str:
        """
        Переведи текст с одного языка на другой.
        """
        ...
