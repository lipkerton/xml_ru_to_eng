"""
Реализация сборщика XML на базе lxml.
"""
import logging
from typing import List
from copy import deepcopy

from lxml import etree # pyright: ignore[reportAttributeAccessIssue]

from src.domain.entities import XMLDocument
from src.domain.value_objects import TranslationPair
from src.domain.interfaces import XMLComposer
from src.domain.exceptions import XMLComposeError


logger = logging.getLogger(__name__)


class LXMLComposer(XMLComposer):
    """
    Сборщик XML на базе библиотеки lxml.
    """
    def apply_translations(self, document: XMLDocument, translations: List[TranslationPair]) -> str:
        """
        Вставляет переводы в оригинальный XML.
        """
        if not translations:
            logger.info(f"Document {document.id}: no translations to apply")
            return document.raw_content

        try:
            root = self._parse_xml(document.raw_content)
            applied_count = self._apply_all(root, translations)
            result = self._serialize(root)
            logger.info(
                f"Document {document.id}: "
                f"applied {applied_count}/{len(translations)} translations"
            )
            return result
        except etree.XMLSyntaxError as e:
            logger.error(f"XML composition failed. Invalid URL: {e}")
            raise XMLComposeError(f"Invalid XML format: {str(e)}")
        except Exception as e:
            logger.error(f"XML composition failed: {e}")
            raise XMLComposeError(f"Failed to compose XML: {str(e)}")

    def _parse_xml(self, xml_string: str) -> etree._Element:
        """
        Парсит XML-строку в дерево элементов.
        """
        parser = etree.XMLParser(
            remove_blank_text=True,
            encoding="utf-8"
        )
        return etree.fromstring(xml_string.encode("utf-8"), parser)

    def _apply_all(self, root: etree._Element, translations: List[TranslationPair]) -> int:
        """
        Применяет все переводы к XML дереву.
        """
        applied_count = 0

        for pair in translations:
            if not pair.is_translated:
                logger.warning(f"Skipping empty translation for {pair.xpath}")
                continue
            
            try:
                if pair.xpath.is_attribute:
                    success = self._update_attribute(root, pair)
                else:
                    success = self._update_element_text(root, pair)
                
                if success:
                    applied_count += 1
                    logger.debug(
                        f"Applied '{pair.original[:30]}...' -> "
                        f"'{pair.translated[:30]}...' at {pair.xpath}"
                    )
                else:
                    logger.warning(f"XPath not found: {pair.xpath}")
            
            except Exception as e:
                logger.error(f"Failed to apply translation at {pair.xpath}: {e}")
        
        return applied_count
    
    def _update_element_text(
        self, 
        root: etree._Element, 
        pair: TranslationPair
    ) -> bool:
        """
        Обновляет текст элемента по XPath.
        """
        elements = root.xpath(pair.xpath.path)
        
        if elements:
            elements[0].text = pair.translated
            return True
        
        return False
    
    def _update_attribute(
        self, 
        root: etree._Element, 
        pair: TranslationPair
    ) -> bool:
        """
        Обновляет значение атрибута по XPath.
        """
        path_parts = pair.xpath.path.rsplit('/@', 1)
        
        if len(path_parts) != 2:
            logger.error(f"Invalid attribute XPath: {pair.xpath.path}")
            return False
        
        element_path, attr_name = path_parts
        
        elements = root.xpath(element_path)
        
        if elements and attr_name in elements[0].attrib:
            elements[0].attrib[attr_name] = pair.translated
            return True
        
        return False
    
    def _serialize(self, root: etree._Element) -> str:
        """
        Сериализует XML дерево обратно в строку.
        """
        return etree.tostring(
            root,
            encoding='unicode',
            pretty_print=True,
            xml_declaration=True
        )