import json
import os
from typing import Dict, Any


class LanguageManager:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(base_dir, "config.json")
        self.current_language = "uk"  # За замовчуванням українська
        self.theme = "light"  # За замовчуванням світла тема
        self.translations = {}
        self.available_languages = {
            "uk": "Українська",
            "en": "English", 
            "ru": "Русский"
        }
        # Завантажуємо збережені налаштування
        self.load_config()
        self.load_language(self.current_language)
    
    def load_config(self):
        """Завантажує конфігурацію з файлу"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    config = json.load(file)
                    self.current_language = config.get('language', 'uk')
                    self.theme = config.get('theme', 'light')
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Помилка завантаження конфігурації: {e}")
            self.current_language = "uk"
            self.theme = "light"
    
    def save_config(self):
        """Зберігає поточну конфігурацію в файл"""
        try:
            config = {"language": self.current_language, "theme": self.theme}
            with open(self.config_file, 'w', encoding='utf-8') as file:
                json.dump(config, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Помилка збереження конфігурації: {e}")

    def set_theme(self, theme: str):
        if theme in ("light", "dark"):
            self.theme = theme
            self.save_config()
            return True
        return False

    def get_theme(self) -> str:
        return self.theme
    
    def load_language(self, language_code: str) -> bool:
        """Завантажує переклад для вказаної мови"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "translations", f"{language_code}.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                self.translations = json.load(file)
                self.current_language = language_code
                return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Помилка завантаження мови {language_code}: {e}")
            return False
    
    def get_text(self, key: str, *args) -> str:
        """Отримує текст для вказаного ключа з підстановкою параметрів"""
        text = self.translations.get(key, key)
        if args:
            try:
                # Підстановка параметрів у текст
                return text.format(*args)
            except (IndexError, ValueError):
                return text
        return text
    
    def get_current_language(self) -> str:
        """Повертає код поточної мови"""
        return self.current_language
    
    def get_available_languages(self) -> Dict[str, str]:
        """Повертає словник доступних мов"""
        return self.available_languages
    
    def set_language(self, language_code: str) -> bool:
        """Встановлює нову мову та зберігає в конфігурації"""
        if language_code in self.available_languages:
            if self.load_language(language_code):
                self.save_config()
                return True
        return False