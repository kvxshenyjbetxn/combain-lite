import flet as ft


import os

GALLERY_PROMPTS = [
    f"Промпт для картинки {i+1}" for i in range(20)
]

# Локальні зображення
GALLERY_IMAGES = [
    os.path.join("gallery_demo", f"image_{i+1:03}.jpg") for i in range(20)
]

def GalleryDemo(page):
    # Стан для діалогу перегенерації
    prompt_field = ft.TextField(label="Промпт", multiline=True, width=480, min_lines=5, max_lines=5, expand=False)
    def close_dialog(e=None):
        dialog.open = False
        page.update()
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Перегенерувати зображення"),
        content=ft.Container(
            width=500,
            content=ft.Column([
                prompt_field,
                ft.Row([
                    ft.ElevatedButton(
                        "Скасувати",
                        icon=ft.Icons.CLOSE,
                        on_click=close_dialog,
                        width=180,
                        height=44,
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    ),
                    ft.ElevatedButton(
                        "Перегенерувати",
                        icon=ft.Icons.REFRESH,
                        width=180,
                        height=44,
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=16)
            ], tight=True)
        )
    )
    if dialog not in page.overlay:
        page.overlay.append(dialog)
    def close_dialog(e=None):
        dialog.open = False
        page.update()
    def on_regen_click(e):
        close_dialog()
    def show_regen_dialog(prompt):
        prompt_field.value = prompt
        dialog.open = True
        # dialog.content — це Container, а controls — у Column (dialog.content.content)
        if isinstance(dialog.content.content, ft.Column):
            # Row з кнопками — другий елемент
            dialog.content.content.controls[1].controls[1].on_click = on_regen_click
        page.update()

    # Галерея
    gallery = ft.GridView(
        expand=True,
        runs_count=4,
        max_extent=320,
        child_aspect_ratio=1.2,
        spacing=16,
        run_spacing=16,
        controls=[]
    )
    for idx, (img, prompt) in enumerate(zip(GALLERY_IMAGES, GALLERY_PROMPTS)):
        def make_regen_handler(p):
            return lambda e: show_regen_dialog(p)
        gallery.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Image(src=img, width=300, height=200, fit=ft.ImageFit.COVER),
                    ft.Row([
                        ft.ElevatedButton("Видалити", icon=ft.Icons.DELETE, on_click=lambda e: None, bgcolor=ft.Colors.RED_200, color=ft.Colors.RED_900),
                        ft.ElevatedButton("Перегенерувати", icon=ft.Icons.REFRESH, on_click=make_regen_handler(prompt), bgcolor=ft.Colors.BLUE_100, color=ft.Colors.BLUE_900)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                # Без білого контуру/фону
            )
        )
    return gallery
