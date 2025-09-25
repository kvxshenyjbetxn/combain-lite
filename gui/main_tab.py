import flet as ft
import time
from collections import defaultdict

def get_main_tab(lang_manager, char_counter, text_input, video_title_input, page=None):

    stages_main_container = ft.Column()
    # Змінюємо контейнер на ResponsiveRow для горизонтального розташування карток
    tasks_container = ft.ResponsiveRow(spacing=10, run_spacing=10)

    stages_state = defaultdict(lambda: {
        "stage_translation": True, "stage_images": True, "stage_voiceover": True,
        "stage_subtitles": True, "stage_montage": True, "stage_description": True,
        "stage_preview": True
    })

    def on_stage_click(e):
        lang = e.control.data["lang"]
        stage_key = e.control.data["stage"]
        stages_state[lang][stage_key] = e.control.value
        print(f"Етап '{stage_key}' для мови '{lang}' змінено на: {e.control.value}")

    def create_stages_menu(language_code):
        stages_keys = [
            "stage_translation", "stage_images", "stage_voiceover", "stage_subtitles",
            "stage_montage", "stage_description", "stage_preview"
        ]
        
        stage_checkboxes = [
            ft.Checkbox(
                label=lang_manager.get_text(stage),
                data={"lang": language_code, "stage": stage},
                on_change=on_stage_click,
                value=stages_state[language_code][stage]
            ) for stage in stages_keys
        ]
        
        controls_in_row = [
            ft.Text(f"{lang_manager.get_text('stages_label')} ({language_code}):", weight=ft.FontWeight.BOLD, size=14)
        ]
        controls_in_row.extend(stage_checkboxes)

        return ft.Container(
            content=ft.Row(
                controls=controls_in_row,
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            padding=15,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(top=10),
            opacity=0,
            animate_opacity=ft.Animation(duration=400, curve=ft.AnimationCurve.EASE_IN),
        )

    def update_ui_elements(e=None):
        selected_languages = [cb.label for cb in language_checkboxes if cb.value]
        
        for menu in stages_main_container.controls:
            menu.opacity = 0
        if page: page.update()
        time.sleep(0.4)

        stages_main_container.controls.clear()
        for lang_code in selected_languages:
            stages_main_container.controls.append(create_stages_menu(lang_code))

        if page: page.update()
        time.sleep(0.05)
        for menu in stages_main_container.controls:
            menu.opacity = 1
        
        can_submit = (video_title_input.value or "").strip() and any(cb.value for cb in language_checkboxes)
        main_submit_button.disabled = not can_submit
        
        if page: page.update()

    def create_task_card(title, languages_with_stages):
        """Створює нову картку завдання з новою структурою."""
        
        # Створюємо вертикальний список етапів
        content_column = ft.Column(spacing=15, visible=False) # Спочатку прихований
        for lang, stages in languages_with_stages.items():
            stages_list = ft.Column(spacing=5)
            for stage, active in stages.items():
                if active:
                    stages_list.controls.append(
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN_500, size=16),
                            ft.Text(lang_manager.get_text(stage), size=14)
                        ])
                    )
            
            # Якщо для мови є активні етапи, додаємо блок
            if stages_list.controls:
                content_column.controls.append(
                    ft.Column([
                        ft.Text(lang, weight=ft.FontWeight.BOLD, size=16),
                        ft.Container(content=stages_list, padding=ft.padding.only(left=10))
                    ])
                )
        
        # Заголовок картки
        header = ft.ListTile(
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            trailing=ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN),
        )

        # Основний контейнер картки
        card_container = ft.Container(
            content=ft.Column([
                header,
                ft.Container(
                    content=content_column,
                    padding=ft.padding.only(left=15, right=15, bottom=15, top=5),
                    # Анімація для плавного розгортання
                    animate_size=ft.Animation(150, ft.AnimationCurve.DECELERATE),
                )
            ]),
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=ft.border_radius.all(8),
        )
        
        def toggle_card_expansion(e):
            """Функція для розгортання/згортання картки."""
            content_column.visible = not content_column.visible
            header.trailing.name = ft.Icons.KEYBOARD_ARROW_UP if content_column.visible else ft.Icons.KEYBOARD_ARROW_DOWN
            card_container.update()

        # Робимо весь контейнер клікабельним
        card_container.on_click = toggle_card_expansion

        # Обгортаємо картку в адаптивну колонку для ResponsiveRow
        return ft.Column(
            col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
            controls=[card_container]
        )

    def on_submit_click(e):
        title = video_title_input.value.strip()
        text = text_input.value or ""
        selected_languages = [cb.label for cb in language_checkboxes if cb.value]

        if not title or not selected_languages:
            return

        task_data = {lang: stages_state[lang] for lang in selected_languages}
        
        new_card = create_task_card(title, task_data)
        tasks_container.controls.insert(0, new_card)

        text_input.value = ""
        video_title_input.value = ""
        for cb in language_checkboxes:
            cb.value = False
        
        stages_state.clear()
        
        update_ui_elements()
        text_input.update()
        video_title_input.update()
        
        char_counter.value = lang_manager.get_text("characters_count", 0)
        char_counter.update()

        snack_bar = ft.SnackBar(
            content=ft.Text(lang_manager.get_text("submit_message", len(text))),
            action=lang_manager.get_text("submit_ok"),
        )
        if page:
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
    
    video_title_input.on_change = update_ui_elements

    tab_content = ft.Column(
        [
            ft.Text(lang_manager.get_text("main_tab_title"), size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20),
            video_title_input,
            char_counter,
            text_input,
            ft.Text(lang_manager.get_text("translation_languages_label"), size=16),
            languages_row,
            stages_main_container,
            ft.Container(height=15),
            ft.Row([main_submit_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20),
            tasks_container,
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