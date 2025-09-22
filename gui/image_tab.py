import flet as ft

def get_image_tab(lang_manager):
    return ft.Tab(
        text=lang_manager.get_text("image_tab"),
        icon=ft.Icons.IMAGE,
        content=ft.Container(
            content=ft.Column([
                ft.Text(lang_manager.get_text("image_tab_title"), size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                ft.Text(lang_manager.get_text("image_tab_desc"), size=14),
                # Тут можна додати поля для генерації зображень
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            expand=True),
            padding=20
        )
    )
