import flet as ft
import time
from collections import defaultdict

def get_main_tab(lang_manager, char_counter, text_input, card_title_input, page=None):

    stages_main_container = ft.Column()
    tasks_container = ft.ResponsiveRow(spacing=10, run_spacing=10)
    task_counter = 1

    stages_state = defaultdict(lambda: {
        "video_title": "",
        "stage_translation": True, "stage_images": True, "stage_voiceover": True,
        "stage_subtitles": True, "stage_montage": True, "stage_description": True,
        "stage_preview": True
    })

    def delete_card_directly(e):
        """Пряме видалення картки без діалогового вікна."""
        card_to_delete = e.control.data
        if card_to_delete in tasks_container.controls:
            tasks_container.controls.remove(card_to_delete)
            page.update()

    def on_stage_click(e):
        lang, stage_key = e.control.data["lang"], e.control.data["stage"]
        stages_state[lang][stage_key] = e.control.value

    def on_translated_title_change(e):
        stages_state[e.control.data]["video_title"] = e.control.value

    def create_stages_menu(language_code):
        stages_keys = ["stage_translation", "stage_images", "stage_voiceover", "stage_subtitles", "stage_montage", "stage_description", "stage_preview"]
        stage_checkboxes = [ft.Checkbox(label=lang_manager.get_text(stage), data={"lang": language_code, "stage": stage}, on_change=on_stage_click, value=stages_state[language_code][stage]) for stage in stages_keys]
        
        return ft.Container(
            content=ft.Column([
                ft.Text(f"{lang_manager.get_text('stages_label')} ({language_code}):", weight=ft.FontWeight.BOLD, size=14),
                ft.Row(controls=stage_checkboxes, scroll=ft.ScrollMode.ADAPTIVE),
                ft.Container(height=5),
                ft.TextField(label=f"{lang_manager.get_text('translated_video_title_label')} ({language_code})", value=stages_state[language_code]["video_title"], on_change=on_translated_title_change, data=language_code, dense=True, border_color=ft.Colors.BLUE_GREY)
            ]),
            padding=15, border=ft.border.all(1, ft.Colors.OUTLINE), border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(top=10), opacity=0, animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_IN)
        )

    def update_ui_elements(e=None):
        selected_languages = [cb.label for cb in language_checkboxes if cb.value]
        for menu in stages_main_container.controls: menu.opacity = 0
        if page: page.update()
        time.sleep(0.4)
        stages_main_container.controls.clear()
        for lang_code in selected_languages: stages_main_container.controls.append(create_stages_menu(lang_code))
        if page: page.update()
        time.sleep(0.05)
        for menu in stages_main_container.controls: menu.opacity = 1
        main_submit_button.disabled = not any(cb.value for cb in language_checkboxes)
        if page: page.update()

    def create_task_card(title, languages_with_stages):
        content_column = ft.Column(spacing=15, visible=False)
        for lang, data in languages_with_stages.items():
            translated_title = data.get("video_title", "").strip() or f"{lang} {title}"
            active_stages = {stage: active for stage, active in data.items() if stage != "video_title" and active}
            if active_stages:
                stages_list = ft.Column(spacing=5, controls=[ft.Row([ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN_500, size=16), ft.Text(lang_manager.get_text(stage_key), size=14)]) for stage_key in active_stages])
                content_column.controls.append(ft.Column([
                    ft.Text(lang, weight=ft.FontWeight.BOLD, size=16),
                    ft.Container(content=ft.Column([
                        ft.Row([ft.Text(f"{lang_manager.get_text('translated_video_title_label')}:", weight=ft.FontWeight.BOLD), ft.Text(f'"{translated_title}"')]),
                        ft.Divider(height=8, thickness=0.5),
                        ft.Text("Вибрані етапи:", italic=True, size=12),
                        stages_list
                    ]), padding=ft.padding.only(left=10))
                ]))
        
        card_container = ft.Container()
        final_card_column = ft.Column(col={"xs": 12, "sm": 6, "md": 4, "lg": 3}, controls=[card_container])
        
        def toggle_card_expansion(e):
            content_column.visible = not content_column.visible
            expand_icon.name = ft.Icons.KEYBOARD_ARROW_UP if content_column.visible else ft.Icons.KEYBOARD_ARROW_DOWN
            card_container.update()

        expand_icon = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN)
        delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_FOREVER,
            icon_color=ft.Colors.RED_500,
            tooltip="Видалити завдання",
            on_click=delete_card_directly,
            data=final_card_column
        )
        
        header_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(value=title, weight=ft.FontWeight.BOLD, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),
                    expand=True,
                    on_click=toggle_card_expansion,
                    padding=ft.padding.only(left=15)
                ),
                delete_button,
                ft.Container(content=expand_icon, on_click=toggle_card_expansion, padding=ft.padding.only(right=10))
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            height=50
        )
        
        card_container.content = ft.Column(
            controls=[
                header_row,
                ft.Container(content=content_column, padding=ft.padding.only(left=15, right=15, bottom=15, top=5), animate_size=ft.Animation(150, ft.AnimationCurve.DECELERATE))
            ],
            spacing=0
        )
        card_container.border = ft.border.all(1, ft.Colors.OUTLINE)
        card_container.border_radius = ft.border_radius.all(8)
        
        return final_card_column

    def on_submit_click(e):
        nonlocal task_counter
        title = card_title_input.value.strip() or f"Задання {task_counter}"
        if not card_title_input.value.strip(): task_counter += 1
        
        text = text_input.value or ""
        selected_languages = [cb.label for cb in language_checkboxes if cb.value]
        if not selected_languages: return

        task_data = {lang: stages_state[lang] for lang in selected_languages}
        tasks_container.controls.insert(0, create_task_card(title, task_data))

        text_input.value, card_title_input.value = "", ""
        for cb in language_checkboxes: cb.value = False
        stages_state.clear()
        
        update_ui_elements()
        text_input.update(), card_title_input.update()
        char_counter.value = lang_manager.get_text("characters_count", 0)
        char_counter.update()

        snack_bar = ft.SnackBar(content=ft.Text(lang_manager.get_text("submit_message", len(text))))
        if page: page.overlay.append(snack_bar), setattr(snack_bar, 'open', True), page.update()

    languages = ["French", "English", "Russian", "Portuguese", "Spanish", "Italian", "Ukrainian"]
    language_checkboxes = [ft.Checkbox(label=lang, on_change=update_ui_elements) for lang in languages]
    languages_row = ft.Row(controls=language_checkboxes, scroll=ft.ScrollMode.ADAPTIVE)
    main_submit_button = ft.ElevatedButton(text=lang_manager.get_text("submit_button"), icon=ft.Icons.SEND, bgcolor=ft.Colors.GREEN_500, color=ft.Colors.WHITE, width=240, height=50, on_click=on_submit_click, disabled=True)
    card_title_input.on_change = update_ui_elements

    return ft.Tab(
        text=lang_manager.get_text("main_tab"), icon=ft.Icons.EDIT,
        content=ft.Container(content=ft.Column([
            ft.Text(lang_manager.get_text("main_tab_title"), size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20),
            card_title_input, char_counter, text_input,
            ft.Text(lang_manager.get_text("translation_languages_label"), size=16),
            languages_row, stages_main_container,
            ft.Container(height=15),
            ft.Row([main_submit_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20), tasks_container,
        ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE), padding=20)
    )