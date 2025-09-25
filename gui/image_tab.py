import flet as ft
import os
import random

def get_image_tab(lang_manager, page=None):
    gallery_data = {}
    gallery_container = ft.Column(
        scroll=ft.ScrollMode.ADAPTIVE, 
        expand=True
    )

    def close_dialog(dialog):
        dialog.open = False
        if page:
            page.update()
            if dialog in page.overlay:
                page.overlay.remove(dialog)

    def add_image_for_language(language_code: str):
        # Визначаємо шлях до кореневої папки проекту (на один рівень вище від папки 'gui')
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        image_folder = os.path.join(project_root, "image")
        if not os.path.exists(image_folder): os.makedirs(image_folder)
        
        image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        image_path = random.choice(image_files) if image_files else None

        if language_code not in gallery_data:
            gallery_data[language_code] = []
        
        gallery_data[language_code].append({"path": image_path})
        build_gallery_from_data()

    def delete_image(lang, image_index):
        if lang in gallery_data and 0 <= image_index < len(gallery_data[lang]):
            del gallery_data[lang][image_index]
            build_gallery_from_data()

    def open_regenerate_prompt_dialog(lang, image_index):
        prompt_input = ft.TextField(label=lang_manager.get_text("regenerate_prompt_label"), multiline=True)

        def on_regenerate_confirm(e, _lang, _image_index):
            dialog_to_close = dialog
            print(f"Перегенерація для мови '{_lang}' з промптом: '{prompt_input.value}'")
            if _lang in gallery_data and 0 <= _image_index < len(gallery_data[_lang]):
                del gallery_data[_lang][_image_index]
            # Визначаємо шлях до кореневої папки проекту (на один рівень вище від папки 'gui')
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            image_folder = os.path.join(project_root, "image")
            image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            image_path = random.choice(image_files) if image_files else None
            if _lang not in gallery_data:
                gallery_data[_lang] = []
            gallery_data[_lang].append({"path": image_path})
            build_gallery_from_data()
            close_dialog(dialog_to_close)

        dialog = ft.AlertDialog(
            modal=True, title=ft.Text(lang_manager.get_text("regenerate_dialog_title").format(lang=lang)),
            content=prompt_input,
            actions=[
                ft.TextButton(lang_manager.get_text("cancel"), on_click=lambda _, d=dialog: close_dialog(d)),
                ft.ElevatedButton(lang_manager.get_text("regenerate"), on_click=lambda e, l=lang, i=image_index: on_regenerate_confirm(e, l, i), bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        if page:
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
    
    def build_gallery_from_data():
        gallery_container.controls.clear()
        for lang_code, images in gallery_data.items():
            if not images: continue
            
            image_layout = ft.ResponsiveRow(spacing=5, run_spacing=5)

            for i, img_data in enumerate(images):
                image_path = img_data["path"]

                if image_path:
                    image_widget = ft.Container(
                        content=ft.Image(src=image_path, fit=ft.ImageFit.COVER, border_radius=ft.border_radius.all(8)),
                        on_click=lambda _, p=image_path: show_image_dialog(p),
                        height=180,
                        border_radius=ft.border_radius.all(8),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.Colors.BLACK26, offset=ft.Offset(0, 2)),
                    )
                else:
                    image_widget = ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.IMAGE, size=50, color=ft.Colors.ON_SURFACE_VARIANT),
                            ft.Text(lang_manager.get_text("demo_image"), size=14, color=ft.Colors.ON_SURFACE_VARIANT)
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        height=180,
                        bgcolor="surfaceVariant",
                        border_radius=ft.border_radius.all(8),
                        on_click=show_placeholder_dialog
                    )
                
                buttons_row = ft.Row([
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_400, tooltip=lang_manager.get_text("delete"), on_click=lambda _, l=lang_code, idx=i: delete_image(l, idx)),
                    ft.IconButton(icon=ft.Icons.REFRESH, icon_color=ft.Colors.BLUE_400, tooltip=lang_manager.get_text("regenerate_tooltip"), on_click=lambda _, l=lang_code, idx=i: open_regenerate_prompt_dialog(l, idx)),
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)

                # ВИПРАВЛЕНО: Змінено налаштування колонок для кращої адаптивності
                image_layout.controls.append(
                    ft.Column(
                        # 1 в ряд (моб) -> 2 -> 3 -> 4 -> 6 (дуже широкі екрани)
                        col={"xs": 12, "sm": 6, "md": 4, "lg": 3, "xl": 2},
                        controls=[
                            ft.Container(
                                content=ft.Column([image_widget, buttons_row], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=ft.padding.all(5)
                            )
                        ]
                    )
                )
            
            language_section = ft.Column(
                [
                    ft.Row([ft.Icon(ft.Icons.LANGUAGE), ft.Text(lang_manager.get_text("language_label").format(lang=lang_code), size=18, weight=ft.FontWeight.BOLD)]),
                    ft.Container(
                        content=image_layout, 
                        border=ft.border.all(1, ft.Colors.OUTLINE),
                        border_radius=ft.border_radius.all(8), padding=10, margin=ft.margin.only(bottom=20)
                    )
                ]
            )
            gallery_container.controls.append(language_section)
        if page: page.update()

    def open_language_selection_dialog(e):
        languages = ["UA", "RO", "PL"]
        language_radio_group = ft.RadioGroup(content=ft.Column([ft.Radio(value=lang, label=lang) for lang in languages]))
        
        def on_add(e):
            if language_radio_group.value:
                add_image_for_language(language_radio_group.value)
        
        dialog = ft.AlertDialog(
            modal=True, title=ft.Text(lang_manager.get_text("select_language_dialog_title")), content=language_radio_group,
            actions=[
                ft.TextButton(lang_manager.get_text("close"), on_click=lambda _: close_dialog(dialog)),
                ft.ElevatedButton(lang_manager.get_text("add"), on_click=on_add, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
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
            modal=True, title=ft.Text(lang_manager.get_text("info")),
            content=ft.Text(lang_manager.get_text("demo_image_not_found"), text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton(lang_manager.get_text("ok"), on_click=lambda _: close_dialog(dialog))
            ]
        )
        if page:
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

    add_button = ft.ElevatedButton(lang_manager.get_text("add_demo_images"), icon=ft.Icons.ADD_A_PHOTO, on_click=open_language_selection_dialog, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, height=40)
    clear_button = ft.ElevatedButton(lang_manager.get_text("clear_gallery"), icon=ft.Icons.CLEAR_ALL, on_click=lambda e: (gallery_data.clear(), build_gallery_from_data()), bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE, height=40)
    
    return ft.Tab(
        text=lang_manager.get_text("image_tab"), icon=ft.Icons.IMAGE,
        content=ft.Container(
            content=ft.Column([
                ft.Text(lang_manager.get_text("image_tab_title"), size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10),
                ft.Row([add_button, clear_button], spacing=10),
                ft.Divider(height=10),
                ft.Container(content=gallery_container, expand=True, border_radius=ft.border_radius.all(8), padding=10)
            ], spacing=10, alignment=ft.MainAxisAlignment.START, expand=True),
            padding=20
        )
    )