"""
Доменные сущности.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID, uuid4

from src.domain.value_objects import Language, TranslationPair


@dataclass
class XMLDocument:
    """
    XML документ, который нужно перевести.
    """
    raw_content: str
    source_language: Language
    target_language: Language
    id: UUID = field(default_factory=uuid4)


    def __post_init__(self):
        if not self.raw_content or not self.raw_content.strip():
            raise ValueError("XML content cannot be empty")


@dataclass
class TranslationTask:
    """
    Задача на перевод XML документа.
    """
    document: XMLDocument
    pairs: List[TranslationPair] = field(default_factory=list)
    error: Optional[str] = None
    id: UUID = field(default_factory=uuid4)


    def __add__(self, pair: TranslationPair) -> 'List[TranslationPair]':
        self.pairs.append(pair)
        return self.pairs
