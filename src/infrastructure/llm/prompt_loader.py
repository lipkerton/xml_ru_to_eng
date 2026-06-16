"""
Загрузчик промптов из YAML файлов.
"""
"""
Загрузчик промптов из YAML файлов.

Позволяет:
- Загружать промпты один раз при старте приложения
- Форматировать промпты с переменными
- Кешировать загруженные промпты в памяти
- Валидировать наличие обязательных промптов
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional

import yaml

logger = logging.getLogger(__name__)


class PromptLoader:
    """
    Загрузчик и менеджер промптов.
    """
    
    def __init__(self, prompts_dir: str = "prompts"):
        self._prompts_dir = Path(prompts_dir)
        self._cache: Dict[str, Any] = {}
        self._load_all_prompts()
    
    def _load_all_prompts(self) -> None:
        """Загружает все YAML файлы из директории промптов"""
        if not self._prompts_dir.exists():
            raise FileNotFoundError(
                f"Prompts directory not found: {self._prompts_dir}"
            )
        
        for yaml_file in self._prompts_dir.glob("*.yaml"):
            self._load_yaml_file(yaml_file)
        
        logger.info(f"Loaded prompts from {len(self._cache)} files")
    
    def _load_yaml_file(self, file_path: Path) -> None:
        """
        Загружает один YAML файл в кеш.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if data:
                self._cache.update(data)
                logger.debug(f"Loaded prompts from: {file_path}")
            else:
                logger.warning(f"Empty prompts file: {file_path}")
                
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse {file_path}: {e}")
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
    
    def get_prompt(self, path: str) -> str:
        """
        Получает промпт по пути через точку.
        """
        keys = path.split('.')
        value = self._cache
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                raise KeyError(
                    f"Cannot navigate into '{key}' at path '{path}'"
                )
            
            if value is None:
                raise KeyError(f"Prompt not found: '{path}'")
        
        return str(value)
    
    def format_prompt(self, path: str, **kwargs) -> str:
        """
        Получает промпт и форматирует его с переменными.
        """
        prompt_template = self.get_prompt(path)
        
        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            logger.error(
                f"Missing variable in prompt '{path}': {e}"
            )
            raise ValueError(
                f"Missing required variable {e} for prompt '{path}'"
            )
    
    def reload(self) -> None:
        """
        Перезагружает все промпты из файлов.
        """
        self._cache.clear()
        self._load_all_prompts()
        logger.info("Prompts reloaded")
    
    @property
    def available_prompts(self) -> list[str]:
        """
        Возвращает список всех доступных промптов.
        """
        prompts = []
        
        def _flatten(d: dict, prefix: str = "") -> None:
            for key, value in d.items():
                full_path = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    _flatten(value, full_path)
                else:
                    prompts.append(full_path)
        
        _flatten(self._cache)
        return prompts