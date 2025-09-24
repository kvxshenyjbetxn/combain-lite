import flet as ft
import os
import random

def get_image_tab(lang_manager, page=None):
    gallery_data = {}
    gallery_container = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)

    def close_dialog(dialog):
        """Універсальна функція для закриття діалогових вікон."""
        dialog.open = False
        if page:
            page.update()
            if dialog in page.overlay:
                page.overlay.remove(dialog)

    def add_image_for_language(language_code: str):
        """Додає дані про нове зображення до моделі та оновлює UI."""
        image_folder = os.path.join(os.getcwd(), "image")
        if not os.path.exists(image_folder): os.makedirs(image_folder)
        
        image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        image_path = random.choice(image_files) if image_files else None

        if language_code not in gallery_data:
            gallery_data[language_code] = []
        
        gallery_data[language_code].append({"path": image_path})
        build_gallery_from_data()

    def delete_image(lang, image_index):
        """Видаляє дані про зображення з моделі."""
        if lang in gallery_data and 0 <= image_index < len(gallery_data[lang]):
            del gallery_data[lang][image_index]
            build_gallery_from_data()

    def open_regenerate_prompt_dialog(lang, image_index):
        """Відкриває діалог для вводу промпту."""
        prompt_input = ft.TextField(label="Введіть промт для перегенерації", multiline=True)

        def on_regenerate_confirm(e):
            """
            ВИПРАВЛЕНО: Змінено порядок операцій, щоб уникнути конфлікту оновлень UI.
            Спочатку всі операції з даними, потім оновлення галереї, і в кінці закриття діалогу.
            """
            dialog_to_close = dialog
            print(f"Перегенерація для мови '{lang}' з промптом: '{prompt_input.value}'")
            
            # КРОК 1: Маніпуляції з даними (без оновлення UI)
            # Видаляємо старі дані
            if lang in gallery_data and 0 <= image_index < len(gallery_data[lang]):
                del gallery_data[lang][image_index]
            
            # Додаємо нові дані
            image_folder = os.path.join(os.getcwd(), "image")
            image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            image_path = random.choice(image_files) if image_files else None
            if lang not in gallery_data:
                gallery_data[lang] = []
            gallery_data[lang].append({"path": image_path})

            # КРОК 2: Оновлюємо галерею на основі нових даних
            build_gallery_from_data()
            
            # КРОК 3: Закриваємо діалогове вікно
            close_dialog(dialog_to_close)
            
        dialog = ft.AlertDialog(
            modal=True, title=ft.Text(f"Перегенерація для мови: {lang}"),
            content=prompt_input,
            actions=[
                ft.TextButton("Скасувати", on_click=lambda _: close_dialog(dialog)),
                ft.ElevatedButton("Перегенерувати", on_click=on_regenerate_confirm, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        if page:
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
    
    def build_gallery_from_data():
        """Повністю перебудовує всю галерею на основі моделі даних."""
        gallery_container.controls.clear()
        for lang_code, images in gallery_data.items():
            if not images: continue
            
            gallery_grid = ft.GridView(
                runs_count=5, max_extent=320, child_aspect_ratio=1.4,
                spacing=15, run_spacing=15,
                padding=ft.padding.all(10),
            )

            for i, img_data in enumerate(images):
                image_path = img_data["path"]

                if image_path:
                    image_widget = ft.Container(
                        content=ft.Image(src=image_path, width=300, height=180, fit=ft.ImageFit.COVER, border_radius=ft.border_radius.all(8)),
                        on_click=lambda _, p=image_path: show_image_dialog(p),
                        width=300, height=180, border_radius=ft.border_radius.all(8), clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.Colors.BLACK26, offset=ft.Offset(0, 2)),
                    )
                else:
                    image_widget = ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.IMAGE, size=50, color=ft.Colors.ON_SURFACE_VARIANT),
                            ft.Text("Demo Image", size=14, color=ft.Colors.ON_SURFACE_VARIANT)
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        width=300, height=180, bgcolor=ft.Colors.SURFACE_VARIANT, border_radius=ft.border_radius.all(8),
                        border=ft.border.all(1, ft.Colors.OUTLINE), on_click=show_placeholder_dialog
                    )

                buttons_row = ft.Row([
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_400, tooltip="Видалити", on_click=lambda _, l=lang_code, idx=i: delete_image(l, idx)),
                    ft.IconButton(icon=ft.Icons.REFRESH, icon_color=ft.Colors.BLUE_400, tooltip="Перегенерувати", on_click=lambda _, l=lang_code, idx=i: open_regenerate_prompt_dialog(l, idx)),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)

                gallery_grid.controls.append(
                    ft.Container(
                        content=ft.Column([image_widget, buttons_row], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.all(5)
                    )
                )

            language_section = ft.Column([
                ft.Row([ft.Icon(ft.Icons.LANGUAGE), ft.Text(f"Мова: {lang_code}", size=18, weight=ft.FontWeight.BOLD)]),
                ft.Container(
                    content=gallery_grid, border=ft.border.all(1, ft.Colors.OUTLINE),
                    border_radius=ft.border_radius.all(8), padding=10, margin=ft.margin.only(bottom=20)
                )
            ])
            gallery_container.controls.append(language_section)
        if page: page.update()

    def open_language_selection_dialog(e):
        languages = ["UA", "RO", "PL"]
        language_radio_group = ft.RadioGroup(content=ft.Column([ft.Radio(value=lang, label=lang) for lang in languages]))
        
        def on_add(e):
            if language_radio_group.value:
                add_image_for_language(language_radio_group.value)
        
        dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Виберіть мову для генерації"), content=language_radio_group,
            actions=[
                ft.TextButton("Закрити", on_click=lambda _: close_dialog(dialog)),
                ft.ElevatedButton("Додати", on_click=on_add, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        if page:
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

    def show_image_dialog(image_path):
        if not page: return
        window_width, window_height = page.window.width - 40, page.window.height - 100
        
        dialog = ft.AlertDialog(
            modal=True, inset_padding=ft.padding.all(20), content_padding=0,
            content=ft.Container(
                content=ft.Stack([
                    ft.Image(src=image_path, width=window_width - 20, height=window_height - 20, fit=ft.ImageFit.CONTAIN),
                    ft.Row([ft.IconButton(icon=ft.Icons.CLOSE, icon_color=ft.Colors.WHITE, on_click=lambda _: close_image_viewer())], alignment=ft.MainAxisAlignment.END)
                ]),
                width=window_width, height=window_height, bgcolor=ft.Colors.BLACK87, border_radius=ft.border_radius.all(10)
            )
        )
        
        def close_image_viewer():
            close_dialog(dialog)
            page.on_keyboard_event = None
        
        def on_keyboard(e: ft.KeyboardEvent):
            if e.key == "Escape": close_image_viewer()

        page.on_keyboard_event = on_keyboard
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def show_placeholder_dialog(e):
        dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Інформація"),
            content=ft.Text("Демо зображення не знайдені.\nДодайте їх до папки 'image' в корені проекту.", text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton("Зрозуміло", on_click=lambda _: close_dialog(dialog))
            ]
        )
        if page:
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

    add_button = ft.ElevatedButton("Додати демо зображення", icon=ft.Icons.ADD_A_PHOTO, on_click=open_language_selection_dialog, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, height=40)
    clear_button = ft.ElevatedButton("Очистити галерею", icon=ft.Icons.CLEAR_ALL, on_click=lambda e: (gallery_data.clear(), build_gallery_from_data()), bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE, height=40)
    
    return ft.Tab(
        text=lang_manager.get_text("image_tab"), icon=ft.Icons.IMAGE,
        content=ft.Container(
            content=ft.Column([
                ft.Text(lang_manager.get_text("image_tab_title"), size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10),
                ft.Row([add_button, clear_button], spacing=10),
                ft.Divider(height=10),
                ft.Container(content=gallery_container, expand=True, border=ft.border.all(1, ft.Colors.OUTLINE), border_radius=ft.border_radius.all(8), padding=10)
            ], spacing=10, alignment=ft.MainAxisAlignment.START, expand=True),
            padding=20
        )
    )