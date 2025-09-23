import flet as ft
import json
import os
from language_manager import LanguageManager
from gui.main_tab import get_main_tab
from gui.settings_tab import get_settings_tab
from gui.image_tab import get_image_tab

# Глобальний менеджер мов
lang_manager = LanguageManager()

def main(page: ft.Page):
    page.title = lang_manager.get_text("app_title")
    page.window_width = 1920
    page.window_height = 1080
    page.padding = 20
    # Встановлюємо тему з конфігу
    if lang_manager.get_theme() == "dark":
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    
    # Лічильник символів
    char_counter = ft.Text(
        lang_manager.get_text("characters_count", 0),
        size=14,
        color=ft.Colors.GREY_700
    )
    
    # Поле для вводу тексту (змінено)
    text_input = ft.TextField(
        label=lang_manager.get_text("enter_text"),
        multiline=True,
        min_lines=15,  # Збільшено початковий розмір
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_600,
        expand=True,  # Дозволяє розтягуватись по висоті
        # max_lines приберемо, щоб дозволити вільне розтягування
    )

    # Функція для оновлення лічильника символів
    def update_char_count(e):
        text = text_input.value or ""
        char_counter.value = lang_manager.get_text("characters_count", len(text))
        char_counter.update()
    
    # Прив'язуємо функцію до зміни тексту
    text_input.on_change = update_char_count
    
    # Функція для кнопки відправки
    def on_submit_click(e):
        text = text_input.value or ""
        print(lang_manager.get_text("submit_processing", len(text)))
        # Тут можна додати будь-яку логіку обробки

        # Очищаємо поле
        text_input.value = ""
        text_input.update()
        char_counter.value = lang_manager.get_text("characters_count", 0)
        char_counter.update()

        # Створюємо snack bar та додаємо його на сторінку
        snack_bar = ft.SnackBar(
            content=ft.Text(lang_manager.get_text("submit_message", len(text))),
            action=lang_manager.get_text("submit_ok"),
            action_color=ft.Colors.BLUE
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
    
    # Кнопка відправки
    submit_button = ft.ElevatedButton(
        text=lang_manager.get_text("submit_button"),
        icon=ft.Icons.SEND,
        on_click=on_submit_click,
        bgcolor=ft.Colors.BLUE_400,
        color=ft.Colors.WHITE,
        width=200,
        height=40
    )
    
    # Функція для зміни теми
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_switch.text = lang_manager.get_text("light_theme")
            lang_manager.set_theme("dark")
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_switch.text = lang_manager.get_text("dark_theme")
            lang_manager.set_theme("light")
        page.update()
    
    # Перемикач теми
    theme_switch = ft.ElevatedButton(
        text=lang_manager.get_text("dark_theme"),
        icon=ft.Icons.DARK_MODE,
        on_click=change_theme,
        bgcolor=ft.Colors.GREY_600,
        color=ft.Colors.WHITE,
        width=150,
        height=40
    )
    
    # Функція для зміни мови
    def change_language(e):
        selected_lang = language_dropdown.value
        if selected_lang and lang_manager.set_language(selected_lang):
            # Оновлюємо заголовок сторінки
            page.title = lang_manager.get_text("app_title")

            # Оновлюємо всі текстові елементи
            update_ui_texts()
    
    # Dropdown для вибору мови
    language_dropdown = ft.Dropdown(
        label=lang_manager.get_text("language_interface"),
        value=lang_manager.get_current_language(),
        options=[
            ft.dropdown.Option(key=code, text=name) 
            for code, name in lang_manager.get_available_languages().items()
        ],
        on_change=change_language,
        width=200
    )
    # Підсказка про перезапуск
    language_hint = ft.Text(
        lang_manager.get_text("restart_required"),
        size=12,
        color=ft.Colors.RED_400,
        italic=True
    )
    
    # Функція для оновлення всіх текстів UI
    def update_ui_texts():
        # Оновлюємо лічильник символів
        text = text_input.value or ""
        char_counter.value = lang_manager.get_text("characters_count", len(text))

        # Оновлюємо поле введення
        text_input.label = lang_manager.get_text("enter_text")

        # Оновлюємо кнопку відправки
        submit_button.text = lang_manager.get_text("submit_button")

        # Оновлюємо кнопку теми
        if page.theme_mode == ft.ThemeMode.LIGHT:
            theme_switch.text = lang_manager.get_text("dark_theme")
        else:
            theme_switch.text = lang_manager.get_text("light_theme")

        # Оновлюємо dropdown мови
        language_dropdown.label = lang_manager.get_text("language_interface")

        # Оновлюємо вкладки
        main_tab.text = lang_manager.get_text("main_tab")
        image_tab.text = lang_manager.get_text("image_tab")
        settings_tab.text = lang_manager.get_text("settings_tab")

        # Оновлюємо тексти в налаштуваннях
        settings_title.value = lang_manager.get_text("settings_title")
        theme_label.value = lang_manager.get_text("theme_interface")
        app_info_title.value = lang_manager.get_text("app_info")
        version_text.value = lang_manager.get_text("version")
        author_text.value = lang_manager.get_text("author")
        description_text.value = lang_manager.get_text("description")

        # Оновлюємо заголовок додатка
        app_title.value = lang_manager.get_text("app_title")

        # Оновлюємо всю сторінку
        page.update()
    
    # Створюємо текстові елементи для налаштувань
    settings_title = ft.Text(
        lang_manager.get_text("settings_title"),
        size=20,
        weight=ft.FontWeight.BOLD
    )
    
    theme_label = ft.Text(lang_manager.get_text("theme_interface"), size=16)
    app_info_title = ft.Text(
        lang_manager.get_text("app_info"),
        size=16,
        weight=ft.FontWeight.BOLD
    )
    version_text = ft.Text(lang_manager.get_text("version"), size=14)
    author_text = ft.Text(lang_manager.get_text("author"), size=14)
    description_text = ft.Text(lang_manager.get_text("description"), size=14)
    
    # Заголовок додатка
    app_title = ft.Text(
        lang_manager.get_text("app_title"),
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800
    )
    
    # Вкладка з основним функціоналом
    main_tab = get_main_tab(lang_manager, char_counter, text_input, submit_button, page)
    # Вкладка з налаштуваннями
    settings_tab = get_settings_tab(
        lang_manager,
        settings_title,
        theme_label,
        theme_switch,
        language_dropdown,
        language_hint,
        app_info_title,
        version_text,
        author_text,
        description_text
    )
    # Вкладка генерації зображень
    image_tab = get_image_tab(lang_manager, page)

    # Створюємо tabs
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[main_tab, image_tab, settings_tab],
        expand=True
    )
    
    # Додаємо всі елементи на сторінку
    page.add(
        ft.Column([
            app_title,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            tabs
        ], 
        spacing=0,
        alignment=ft.MainAxisAlignment.START,
        expand=True
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
