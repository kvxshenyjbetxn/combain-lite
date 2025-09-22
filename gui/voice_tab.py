import flet as ft

def get_voice_tab(lang_manager):
    char_counter = ft.Text(
        lang_manager.get_text("characters_count", 0),
        size=14,
        color=ft.Colors.GREY_700
    )
    text_input = ft.TextField(
        label=lang_manager.get_text("enter_text"),
        multiline=True,
        min_lines=12,
        max_lines=18,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_600,
        expand=True
    )
    def update_char_count(e):
        text = text_input.value or ""
        char_counter.value = lang_manager.get_text("characters_count", len(text))
        char_counter.update()
    text_input.on_change = update_char_count

    def on_voice_submit(e):
        text = text_input.value or ""
        print(f"Озвучка: {len(text)} символів")
        snack_bar = ft.SnackBar(
            content=ft.Text(lang_manager.get_text("submit_message", len(text))),
            action=lang_manager.get_text("submit_ok"),
            action_color=ft.Colors.GREEN
        )
        e.page.overlay.append(snack_bar)
        snack_bar.open = True
        e.page.update()

    submit_button = ft.ElevatedButton(
        text=lang_manager.get_text("submit_button"),
        icon=ft.Icons.VOLUME_UP,
        on_click=on_voice_submit,
        bgcolor=ft.Colors.GREEN_500,
        color=ft.Colors.WHITE,
        width=240,
        height=50
    )

    return ft.Tab(
        text=lang_manager.get_text("voice_tab"),
        icon=ft.Icons.VOICE_CHAT,
        content=ft.Container(
            content=ft.Column([
                ft.Text(lang_manager.get_text("voice_tab_title"), size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                #ft.Text(lang_manager.get_text("voice_tab_desc"), size=14),
                ft.Container(height=10),
                char_counter,
                ft.Container(height=5),
                text_input,
                ft.Container(height=15),
                ft.Row([
                    submit_button
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            expand=True),
            padding=20
        )
    )
