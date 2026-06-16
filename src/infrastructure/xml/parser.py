"""
Реализация парсера XML на базе lxml.
"""
import logging
from typing import List

from lxml import etree

from src.domain.entities import XMLDocument
from src.domain.value_objects import TranslationPair, XPath
from src.domain.interfaces import XMLParser
from src.domain.exceptions import XMLParseError


logger = logging.getLogger(__name__)


class LXMLParser(XMLParser):
    """
    Парсер на базе библиотеки lxml.
    """
    RUSSIAN_CHARS = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

    def extract_translatable_texts(self, document: XMLDocument) -> List[TranslationPair]:
        """
        Извлекает все фрагменты теста на русском языке из XML.
        """
        try:
            root = self._parse_xml(document.raw_content)
            pairs = self._extract_text(root)
            logger.info(
                f"Document {document.id}: extracted {len(pairs)} translatable segments"
            )
            return pairs
        except etree.XMLSyntaxError as e:
            logger.error(f"XML parsing failed: {e}")
            raise XMLParseError(f"Invalid XML format: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during XML parsing: {e}")
            raise XMLParseError(f"Failed to parse XML: {str(e)}")

    def _parse_xml(self, xml_string: str) -> etree._Element:
        """
        Парсит XML-строку в корневой элемент.
        """
        parser = etree.XMLParser(
            remove_blank_text=True,
            encoding="utf-8"
        )
        root = etree.fromstring(xml_string.encode("utf-8"), parser)
        return root

    def _extract_text(self, root: etree._Element) -> List[TranslationPair]:
        """
        Обходит XML дерево и извлекает все тексты с кириллицей.
        """
        tree = root.getroottree()
        pairs = list()

        for element in root.iter():

            self._extract_element_text(element, tree, pairs)
            self._extract_element_attributes(element, tree, pairs)

        return pairs

    def _extract_element_text(
        self,
        element: etree._Element,
        tree: etree._ElementTree,
        pairs: List[TranslationPair],
    ) -> None:
        if element.text and self._contains_russian(element.text):
            text = element.text.strip()
            xpath = tree.getpath(element)
            logger.debug(f"Found text: '{text[:50]}...' at {xpath}")

            pair = TranslationPair(
                original=text,
                translated="",
                xpath=XPath(path=xpath)
            )
            pairs.append(pair)
    
    def _extract_element_attributes(
        self,
        element: etree._Element,
        tree: etree._ElementTree,
        pairs: List[TranslationPair]
    ) -> None:
        """
        Проверяет значения атрибутов элемента на наличие кириллицы.
        """
        for attr_name, attr_value in element.attrib.items():
            if self._contains_russian(attr_value):
                text = attr_value.strip()

                element_path = tree.getpath(element)
                attr_xpath = f"{element_path}/@{attr_name}"

                logger.debug(f"Found attribute: '{attr_name}={text[:50]}...' at {attr_xpath}")
                
                pair = TranslationPair(
                    original=text,
                    translated="",
                    xpath=XPath(path=attr_xpath, is_attribute=True)
                )
                pairs.append(pair)
    
    def _contains_russian(self, text: str) -> bool:
        """
        Проверяет содержит ли текст хотя бы одну букву кириллицы.
        """
        return any(char.lower() in self.RUSSIAN_CHARS for char in text)