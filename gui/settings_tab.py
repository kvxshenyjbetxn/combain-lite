import flet as ft

def get_settings_tab(lang_manager, settings_title, theme_label, theme_switch, language_dropdown, language_hint, app_info_title, version_text, author_text, description_text, on_logout=None, results_path_input=None, on_browse_click=None):
    return ft.Tab(
        text=lang_manager.get_text("settings_tab"),
        icon=ft.Icons.SETTINGS,
        content=ft.Container(
            content=ft.Column([
                ft.Container(height=20),
                settings_title,
                ft.Divider(height=30),
                ft.Row([
                    ft.Icon(ft.Icons.PALETTE, size=30),
                    theme_label,
                ], spacing=10),
                ft.Container(height=10),
                theme_switch,
                ft.Container(height=20),
                ft.Row([
                    ft.Icon(ft.Icons.LANGUAGE, size=30),
                    ft.Text(lang_manager.get_text("language_interface"), size=16),
                ], spacing=10),
                ft.Container(height=10),
                language_dropdown,
                language_hint,
                ft.Container(height=20),
                ft.Row([
                    ft.Icon(ft.Icons.FOLDER_OPEN, size=30),
                    ft.Text(lang_manager.get_text("results_path_label"), size=16),
                ], spacing=10),
                ft.Container(height=10),
                ft.Row([
                    results_path_input,
                    ft.ElevatedButton(lang_manager.get_text("browse_button"), icon=ft.Icons.FOLDER_OPEN, on_click=on_browse_click)
                ]),
                ft.Container(height=30),
                app_info_title,
                ft.Container(height=10),
                version_text,
                author_text,
                description_text,
                ft.Container(height=30),
                ft.ElevatedButton(
                    text=lang_manager.get_text("logout_button"),
                    icon=ft.Icons.LOGOUT,
                    on_click=on_logout,
                    bgcolor=ft.Colors.RED_ACCENT_700,
                    color=ft.Colors.WHITE
                ),
            ], 
            spacing=5,
            alignment=ft.MainAxisAlignment.START,
            expand=True
            ),
            padding=20
        )
    )
