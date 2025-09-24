import flet as ft
import os
import random

def get_image_tab(lang_manager, page=None):
    # Словник для зберігання зображень по мовах
    gallery_by_language = {}
    
    # Головний контейнер для всієї галереї, який будемо оновлювати
    gallery_container = ft.Column(
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )
    
    def build_gallery_view():
        """Перебудовує відображення галереї з нуля на основі gallery_by_language."""
        gallery_container.controls.clear()
        
        for lang_code, images in gallery_by_language.items():
            if not images:
                continue

            # Створюємо GridView для поточної мови
            gallery_grid = ft.GridView(
                runs_count=5,
                max_extent=320,
                child_aspect_ratio=1.6,
                spacing=15,
                run_spacing=15,
                padding=ft.padding.all(10),
                # Важливо: не встановлюємо expand=True, бо висота має бути динамічною
            )
            gallery_grid.controls = images

            # Створюємо контейнер-розділ для мови
            language_section = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LANGUAGE),
                    ft.Text(f"Мова: {lang_code}", size=18, weight=ft.FontWeight.BOLD),
                ]),
                ft.Container(
                    content=gallery_grid,
                    border=ft.border.all(1, ft.Colors.OUTLINE),
                    border_radius=ft.border_radius.all(8),
                    padding=10,
                    margin=ft.margin.only(bottom=20)
                )
            ])
            gallery_container.controls.append(language_section)

        if page:
            page.update()

    def add_image_for_language(language_code: str):
        """Додає демо зображення для вказаної мови."""
        image_folder = os.path.join(os.getcwd(), "image")
        
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
            
        image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
        
        image_path = random.choice(image_files) if image_files else None
        
        def create_delete_button(lang, image_index):
            return ft.IconButton(
                icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_400, tooltip="Видалити",
                on_click=lambda e: delete_image(lang, image_index)
            )

        def create_regenerate_button(lang, image_index):
            return ft.IconButton(
                icon=ft.Icons.REFRESH, icon_color=ft.Colors.BLUE_400, tooltip="Перегенерувати",
                on_click=lambda e: regenerate_image(lang, image_index)
            )

        def delete_image(lang, image_index):
            if lang in gallery_by_language and 0 <= image_index < len(gallery_by_language[lang]):
                del gallery_by_language[lang][image_index]
                # Оновлюємо індекси для решти кнопок
                for i, img_container in enumerate(gallery_by_language[lang]):
                    buttons_row = img_container.content.controls[1]
                    buttons_row.controls[0].on_click = lambda e, l=lang, idx=i: delete_image(l, idx)
                    buttons_row.controls[1].on_click = lambda e, l=lang, idx=i: regenerate_image(l, idx)
                build_gallery_view()

        def regenerate_image(lang, image_index):
            add_image_for_language(lang)
            if page:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Зображення для '{lang}' перегенеровано!"))
                page.snack_bar.open = True
                page.update()

        # Створюємо віджет зображення
        if image_path:
            image_widget = ft.Container(
                content=ft.Image(src=image_path, width=300, height=180, fit=ft.ImageFit.COVER, border_radius=ft.border_radius.all(8)),
                width=300, height=180, border_radius=ft.border_radius.all(8), clip_behavior=ft.ClipBehavior.HARD_EDGE,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.Colors.BLACK26, offset=ft.Offset(0, 2)),
                on_click=lambda e: show_image_dialog(image_path)
            )
        else:
            image_widget = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.IMAGE, size=50, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Text("Demo Image", size=14, color=ft.Colors.ON_SURFACE_VARIANT)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=300, height=180, bgcolor=ft.Colors.SURFACE_VARIANT, border_radius=ft.border_radius.all(8),
                border=ft.border.all(1, ft.Colors.OUTLINE), on_click=lambda e: show_placeholder_dialog()
            )

        # Ініціалізуємо список, якщо мова нова
        if language_code not in gallery_by_language:
            gallery_by_language[language_code] = []
            
        current_index = len(gallery_by_language[language_code])

        buttons_row = ft.Row([
            create_delete_button(language_code, current_index),
            create_regenerate_button(language_code, current_index),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)

        image_container = ft.Container(
            content=ft.Column([image_widget, buttons_row], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(5)
        )

        gallery_by_language[language_code].append(image_container)
        build_gallery_view()
    
    def open_language_selection_dialog(e):
        """Відкриває діалог для вибору мови."""
        
        # Використовуємо мови з головної вкладки
        languages = ["UA", "RO", "PL"] 
        language_options = [ft.Radio(value=lang, label=lang) for lang in languages]
        
        def on_add(e):
            selected_language = language_radio_group.value
            if selected_language:
                add_image_for_language(selected_language)
                # Після додавання зображення діалог залишається відкритим
        
        language_radio_group = ft.RadioGroup(content=ft.Column(language_options))

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Виберіть мову для генерації"),
            content=language_radio_group,
            actions=[
                # Текст кнопки змінено на "Закрити" для кращого розуміння
                ft.TextButton("Закрити", on_click=lambda e: close_dialog(dialog)),
                ft.ElevatedButton("Додати", on_click=on_add, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def show_image_dialog(image_path):
        """Показує зображення на весь розмір інтерфейсу"""
        if not page: return
        
        window_width = page.window.width - 40
        window_height = page.window.height - 100
        
        close_button = ft.IconButton(
            icon=ft.Icons.CLOSE, icon_color=ft.Colors.WHITE, icon_size=30, bgcolor=ft.Colors.BLACK54,
            tooltip="Закрити (ESC)", on_click=lambda e: close_image_viewer()
        )
        
        image_widget = ft.Image(src=image_path, width=window_width - 20, height=window_height - 20, fit=ft.ImageFit.CONTAIN)
        
        viewer_container = ft.Container(
            content=ft.Stack([image_widget, ft.Row([close_button], alignment=ft.MainAxisAlignment.END)]),
            width=window_width, height=window_height, bgcolor=ft.Colors.BLACK87,
            border_radius=ft.border_radius.all(10), padding=ft.padding.all(10)
        )
        
        dialog = ft.AlertDialog(
            modal=True, content=viewer_container, content_padding=0, actions=[],
            actions_padding=0, title_padding=0, inset_padding=ft.padding.all(20),
        )
        
        def close_image_viewer():
            dialog.open = False
            page.update()
            page.overlay.remove(dialog)
            page.on_keyboard_event = None

        def on_keyboard(e: ft.KeyboardEvent):
            if e.key == "Escape": close_image_viewer()
        
        page.on_keyboard_event = on_keyboard
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def show_placeholder_dialog():
        """Показує діалог про відсутність зображень."""
        if not page: return
        dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Інформація"),
            content=ft.Text("Демо зображення не знайдені.\nДодайте їх до папки 'image' в корені проекту.", text_align=ft.TextAlign.CENTER),
            actions=[ft.TextButton("Зрозуміло", on_click=lambda e: close_dialog(dialog))]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    def close_dialog(dialog):
        dialog.open = False
        page.update()
        page.overlay.remove(dialog)
    
    add_button = ft.ElevatedButton(
        text="Додати демо зображення", icon=ft.Icons.ADD_A_PHOTO, on_click=open_language_selection_dialog,
        bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, height=40
    )
    
    clear_button = ft.ElevatedButton(
        text="Очистити галерею", icon=ft.Icons.CLEAR_ALL, on_click=lambda e: clear_gallery(),
        bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE, height=40
    )
    
    def clear_gallery():
        gallery_by_language.clear()
        build_gallery_view()
    
    return ft.Tab(
        text=lang_manager.get_text("image_tab"), icon=ft.Icons.IMAGE,
        content=ft.Container(
            content=ft.Column([
                ft.Text(lang_manager.get_text("image_tab_title"), size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10),
                ft.Row([add_button, clear_button], spacing=10),
                ft.Divider(height=10),
                ft.Container(
                    content=gallery_container,
                    expand=True,
                    border_radius=ft.border_radius.all(8),
                    border=ft.border.all(1, ft.Colors.OUTLINE),
                    padding=10
                )
            ],
            spacing=10, alignment=ft.MainAxisAlignment.START, expand=True),
            padding=20
        )
    )