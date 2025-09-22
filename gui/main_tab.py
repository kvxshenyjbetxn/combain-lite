import flet as ft
from gui.gallery import GalleryDemo

def get_main_tab(lang_manager, char_counter, text_input, submit_button=None, page=None):
    # Опис як на вкладці Озвучка
    #description = ft.Text(lang_manager.get_text("main_tab_desc") if lang_manager.get_text("main_tab_desc") != "main_tab_desc" else "Введіть текст для обробки.", size=14)
    # Зелена велика кнопка
    main_submit_button = ft.ElevatedButton(
        text=lang_manager.get_text("submit_button"),
        icon=ft.Icons.SEND,
        bgcolor=ft.Colors.GREEN_500,
        color=ft.Colors.WHITE,
        width=240,
        height=50,
        on_click=submit_button.on_click if submit_button else None
    )
    return ft.Tab(
        text=lang_manager.get_text("main_tab"),
        icon=ft.Icons.EDIT,
        content=ft.Container(
            content=ft.Column([
                ft.Text(lang_manager.get_text("main_tab_title") if lang_manager.get_text("main_tab_title") != "main_tab_title" else lang_manager.get_text("main_tab"), size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                #description,
                ft.Container(height=10),
                char_counter,
                ft.Container(height=5),
                text_input,
                ft.Container(height=15),
                ft.Row([
                    main_submit_button
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=30),
                GalleryDemo(page)
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            expand=True
            ),
            padding=20
        )
    )
