import flet as ft
from language_manager import LanguageManager
from gui.main_tab import get_main_tab
from gui.settings_tab import get_settings_tab
from gui.image_tab import get_image_tab
from firebase_auth import db # Імпорт для передачі в main_tab

# Глобальний менеджер мов
lang_manager = LanguageManager()

# Функція тепер приймає user_data та logout_callback
def build_main_view(page: ft.Page, user_data, logout_callback):
    page.title = lang_manager.get_text("app_title")
    
    page.window.maximized = False
    page.window.minimized = False
    page.window.resizable = True
    page.window.width = 1920
    page.window.height = 1080
    page.update()
    
    page.padding = 20
    
    if lang_manager.get_theme() == "dark":
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    
    char_counter = ft.Text(
        lang_manager.get_text("characters_count", 0),
        size=14,
        color=ft.Colors.GREY_700
    )
    
    text_input = ft.TextField(
        label=lang_manager.get_text("enter_text"),
        multiline=True,
        min_lines=15,
        max_lines=15,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_600,
    )

    def update_char_count(e):
        text = text_input.value or ""
        char_counter.value = lang_manager.get_text("characters_count", len(text))
        char_counter.update()
    
    text_input.on_change = update_char_count

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
    
    theme_switch = ft.ElevatedButton(
        text=lang_manager.get_text("dark_theme"),
        icon=ft.Icons.DARK_MODE,
        on_click=change_theme,
        bgcolor=ft.Colors.GREY_600,
        color=ft.Colors.WHITE,
        width=150,
        height=40
    )
    
    def change_language(e):
        selected_lang = language_dropdown.value
        if selected_lang and lang_manager.set_language(selected_lang):
            page.title = lang_manager.get_text("app_title")
            update_ui_texts()
    
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
    language_hint = ft.Text(
        lang_manager.get_text("restart_required"),
        size=12,
        color=ft.Colors.RED_400,
        italic=True
    )
    
    def update_ui_texts():
        text = text_input.value or ""
        char_counter.value = lang_manager.get_text("characters_count", len(text))
        text_input.label = lang_manager.get_text("enter_text")
        card_title_input.label = lang_manager.get_text("card_title_label")
        if page.theme_mode == ft.ThemeMode.LIGHT:
            theme_switch.text = lang_manager.get_text("dark_theme")
        else:
            theme_switch.text = lang_manager.get_text("light_theme")
        language_dropdown.label = lang_manager.get_text("language_interface")
        main_tab.text = lang_manager.get_text("main_tab")
        image_tab.text = lang_manager.get_text("image_tab")
        settings_tab.text = lang_manager.get_text("settings_tab")
        settings_title.value = lang_manager.get_text("settings_title")
        theme_label.value = lang_manager.get_text("theme_interface")
        app_info_title.value = lang_manager.get_text("app_info")
        version_text.value = lang_manager.get_text("version")
        author_text.value = lang_manager.get_text("author")
        description_text.value = lang_manager.get_text("description")
        app_title.value = lang_manager.get_text("app_title")
        page.update()
    
    settings_title = ft.Text(lang_manager.get_text("settings_title"), size=20, weight=ft.FontWeight.BOLD)
    theme_label = ft.Text(lang_manager.get_text("theme_interface"), size=16)
    app_info_title = ft.Text(lang_manager.get_text("app_info"), size=16, weight=ft.FontWeight.BOLD)
    version_text = ft.Text(lang_manager.get_text("version"), size=14)
    author_text = ft.Text(lang_manager.get_text("author"), size=14)
    description_text = ft.Text(lang_manager.get_text("description"), size=14)
    app_title = ft.Text(lang_manager.get_text("app_title"), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
    card_title_input = ft.TextField(label=lang_manager.get_text("card_title_label"), border_color=ft.Colors.BLUE_400, focused_border_color=ft.Colors.BLUE_600)

    # Передаємо user_data та db у main_tab
    main_tab = get_main_tab(lang_manager, char_counter, text_input, card_title_input, page, user_data, db)
    
    # Передаємо logout_callback у settings_tab
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
        description_text,
        on_logout=logout_callback
    )
    image_tab = get_image_tab(lang_manager, page)

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[main_tab, image_tab, settings_tab],
        expand=True
    )
    
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
    
    # Фінальне оновлення екрану
    page.update()