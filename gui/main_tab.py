import flet as ft

def get_main_tab(lang_manager, char_counter, text_input, submit_button):
    return ft.Tab(
        text=lang_manager.get_text("main_tab"),
        icon=ft.Icons.EDIT,
        content=ft.Container(
            content=ft.Column([
                ft.Container(height=10),
                char_counter,
                ft.Container(height=5),
                text_input,
                ft.Container(height=15),
                ft.Row([
                    submit_button
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], 
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
            expand=True
            ),
            padding=20
        )
    )
