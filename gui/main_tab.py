import flet as ft
import time

def get_main_tab(lang_manager, char_counter, text_input, page=None):

    stages_main_container = ft.Column()

    def on_stage_click(e):
        print(f"Етап '{e.control.label}' для мови '{e.control.data}' змінено на: {e.control.value}")

    def create_stages_menu(language_code):
        stages = [
            "stage_translation", "stage_images", "stage_voiceover", "stage_subtitles",
            "stage_montage", "stage_description", "stage_preview"
        ]
        
        stage_checkboxes = [
            ft.Checkbox(
                label=lang_manager.get_text(stage),
                data=language_code,
                on_change=on_stage_click,
                value=True
            ) for stage in stages
        ]
        
        controls_in_row = [
            ft.Text(f"{lang_manager.get_text('stages_label')} ({language_code}):", weight=ft.FontWeight.BOLD, size=14)
        ]
        controls_in_row.extend(stage_checkboxes)

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=controls_in_row,
                        spacing=15,
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            padding=15,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(top=10),
            opacity=0,
            animate_opacity=ft.Animation(duration=400, curve=ft.AnimationCurve.EASE_IN),
        )

    def update_ui_elements(e=None):
        """Оновлює меню етапів та стан кнопки відправки."""
        selected_languages = [cb.label for cb in language_checkboxes if cb.value]
        
        # Анімація зникнення
        for menu in stages_main_container.controls:
            menu.opacity = 0
        if page: page.update()
        time.sleep(0.4)

        stages_main_container.controls.clear()
        for lang_code in selected_languages:
            stages_main_container.controls.append(create_stages_menu(lang_code))

        if not stages_main_container.controls:
            if page: page.update()
        else:
            if page: page.update()
            time.sleep(0.05)
            for menu in stages_main_container.controls:
                menu.opacity = 1
            if page: page.update()
        
        main_submit_button.disabled = not any(cb.value for cb in language_checkboxes)
        if page: page.update()

    def on_submit_click(e):
        text = text_input.value or ""
        selected_languages = [cb.label for cb in language_checkboxes if cb.value]

        if not text.strip() or not selected_languages:
            return

        print(f"Відправлено на обробку: '{text}' для мов: {selected_languages}")

        # Скидання стану
        text_input.value = ""
        for cb in language_checkboxes:
            cb.value = False
        
        update_ui_elements()
        text_input.update()
        
        char_counter.value = lang_manager.get_text("characters_count", 0)
        char_counter.update()

        snack_bar = ft.SnackBar(
            content=ft.Text(lang_manager.get_text("submit_message", len(text))),
            action=lang_manager.get_text("submit_ok"),
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    languages = ["FR", "EN", "RU", "PT", "ES", "IT", "UA"]
    language_checkboxes = [
        ft.Checkbox(label=lang, on_change=update_ui_elements) for lang in languages
    ]
    languages_row = ft.Row(controls=language_checkboxes, scroll=ft.ScrollMode.ADAPTIVE)

    main_submit_button = ft.ElevatedButton(
        text=lang_manager.get_text("submit_button"),
        icon=ft.Icons.SEND,
        bgcolor=ft.Colors.GREEN_500,
        color=ft.Colors.WHITE,
        width=240,
        height=50,
        on_click=on_submit_click,
        disabled=True
    )
    
    tab_content = ft.Column(
        [
            ft.Text(lang_manager.get_text("main_tab_title") if lang_manager.get_text("main_tab_title") != "main_tab_title" else lang_manager.get_text("main_tab"), size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20),
            char_counter,
            text_input,
            ft.Text(lang_manager.get_text("translation_languages_label"), size=16),
            languages_row,
            stages_main_container,
            ft.Container(height=15),
            ft.Row([main_submit_button], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=10,
        scroll=ft.ScrollMode.ADAPTIVE,
    )

    return ft.Tab(
        text=lang_manager.get_text("main_tab"),
        icon=ft.Icons.EDIT,
        content=ft.Container(
            content=tab_content,
            padding=20
        )
    )