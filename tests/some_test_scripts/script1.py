from src.domain.entities import XMLDocument
from src.domain.value_objects import Language
from src.infrastructure.xml.parser import LXMLParser


with open('tests/fixtures/sample1.xml', 'r', encoding='utf-8') as f:
    xml_content = f.read()

document = XMLDocument(
    raw_content=xml_content,
    source_language=Language("ru"),
    target_language=Language("en")
)

parser = LXMLParser()
pairs = parser.extract_translatable_texts(document)

print(f'Найдено фрагментов: {len(pairs)}')
print()
for i, pair in enumerate(pairs, 1):
    print(f'{i}. [{pair.xpath}]')
    print(f'   Оригинал: {pair.original}')
    print(f'   Переведён: {pair.is_translated}')
    print()