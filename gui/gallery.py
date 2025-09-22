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
    prompt_field = ft.TextField(label="Промпт", multiline=True, width=300)
    def close_dialog(e):
        page.dialog.open = False
        page.update()
    def show_regen_dialog(prompt):
        prompt_field.value = prompt
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Перегенерувати зображення"),
            content=ft.Column([
                prompt_field,
                ft.ElevatedButton("Перегенерувати", icon=ft.Icons.REFRESH, on_click=close_dialog)
            ], tight=True)
        )
        page.dialog = dialog
        dialog.open = True
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
