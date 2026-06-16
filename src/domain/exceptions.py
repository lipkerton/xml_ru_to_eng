"""
Доменные ошибки.
"""
class XMLParseError(Exception):
    pass


class XMLComposeError(Exception):
    pass


class LLMCallError(Exception):
    pass