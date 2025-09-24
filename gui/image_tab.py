import flet as ft
import os
import random

def get_image_tab(lang_manager, page=None):
    # Список для зберігання зображень в галереї
    gallery_images = []
    
    # Контейнер для галереї з прокруткою
    gallery_grid = ft.GridView(
        expand=True,
        runs_count=3,  # Кількість колонок (менше для широкоформатних)
        max_extent=320,  # Збільшена ширина для широкоформатних
        child_aspect_ratio=1.6,  # Широкоформатне співвідношення (16:10)
        spacing=15,  # Відстань між елементами
        run_spacing=15,  # Відстань між рядками
        padding=ft.padding.all(10)
    )

    
    def add_demo_image():
        """Додає демо зображення до галереї"""
        image_folder = os.path.join(os.getcwd(), "image")
        
        if not os.path.exists(image_folder):
            # Якщо папки немає, створюємо її
            os.makedirs(image_folder)
            
        # Шукаємо зображення в папці
        image_files = []
        if os.path.exists(image_folder):
            for file in os.listdir(image_folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                    image_files.append(os.path.join(image_folder, file))
        
        if not image_files:
            # Якщо зображень немає, показуємо placeholder
            image_path = None
        else:
            # Вибираємо випадкове зображення
            image_path = random.choice(image_files)
        
        def create_delete_button(image_index):
            """Створює кнопку видалення для конкретного зображення"""
            return ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED_400,
                tooltip="Видалити",
                on_click=lambda e: delete_image(image_index)
            )

        def create_regenerate_button(image_index):
            """Створює кнопку перегенерації для конкретного зображення"""
            return ft.IconButton(
                icon=ft.Icons.REFRESH,
                icon_color=ft.Colors.BLUE_400,
                tooltip="Перегенерувати",
                on_click=lambda e: regenerate_image(image_index)
            )

        def delete_image(image_index):
            """Видаляє зображення з галереї"""
            if 0 <= image_index < len(gallery_images):
                # Видаляємо з списку та GridView
                del gallery_images[image_index]
                gallery_grid.controls.pop(image_index)
                
                # Оновлюємо індекси кнопок для решти зображень
                update_gallery_indices()
                
                if page:
                    page.update()

        def regenerate_image(image_index):
            """Перегенеровує зображення (поки що просто додає нове)"""
            if 0 <= image_index < len(gallery_images):
                add_demo_image()  # Додаємо нове демо зображення
                
                # Показуємо повідомлення
                if page:
                    snack_bar = ft.SnackBar(
                        content=ft.Text("Зображення перегенеровано!"),
                        action="OK",
                        action_color=ft.Colors.BLUE
                    )
                    page.overlay.append(snack_bar)
                    snack_bar.open = True
                    page.update()

        def update_gallery_indices():
            """Оновлює індекси кнопок після видалення зображення"""
            for i, image_container in enumerate(gallery_images):
                # Оновлюємо кнопки з новими індексами
                if hasattr(image_container.content, 'controls') and len(image_container.content.controls) > 1:
                    buttons_row = image_container.content.controls[1]
                    if hasattr(buttons_row, 'controls') and len(buttons_row.controls) >= 2:
                        # Оновлюємо кнопку видалення
                        buttons_row.controls[0].on_click = lambda e, idx=i: delete_image(idx)
                        # Оновлюємо кнопку перегенерації
                        buttons_row.controls[1].on_click = lambda e, idx=i: regenerate_image(idx)

        # Створюємо контейнер для зображення
        current_index = len(gallery_images)  # Індекс поточного зображення

        if image_path and os.path.exists(image_path):
            image_widget = ft.Container(
                content=ft.Image(
                    src=image_path,
                    width=300,
                    height=180,  # Широкоформатні розміри
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(8)
                ),
                width=300,
                height=180,
                border_radius=ft.border_radius.all(8),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=3,
                    color=ft.Colors.BLACK26,
                    offset=ft.Offset(0, 2),
                ),
                on_click=lambda e: show_image_dialog(image_path)
            )
        else:
            # Placeholder якщо немає зображення
            image_widget = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.IMAGE, size=50, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Text("Demo Image", size=14, color=ft.Colors.ON_SURFACE_VARIANT)
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=300,
                height=180,
                bgcolor=ft.Colors.SURFACE_VARIANT,
                border_radius=ft.border_radius.all(8),
                border=ft.border.all(1, ft.Colors.OUTLINE),
                on_click=lambda e: show_placeholder_dialog()
            )

        # Кнопки під зображенням
        buttons_row = ft.Row([
            create_delete_button(current_index),
            create_regenerate_button(current_index),
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5)

        # Контейнер з зображенням та кнопками
        image_container = ft.Container(
            content=ft.Column([
                image_widget,
                buttons_row
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(5)
        )

        # Додаємо зображення до галереї
        gallery_images.append(image_container)
        gallery_grid.controls.append(image_container)

        
        # Оновлюємо галерею
        if page:
            page.update()
    
    def show_image_dialog(image_path):
        """Показує зображення на весь розмір інтерфейсу"""
        if not page:
            return
        
        # Отримуємо розміри вікна (з урахуванням padding)
        window_width = page.window.width - 40  # Віднімаємо padding
        window_height = page.window.height - 100  # Віднімаємо padding та место для кнопки
        
        # Кнопка закриття
        close_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=ft.Colors.WHITE,
            icon_size=30,
            bgcolor=ft.Colors.BLACK54,
            tooltip="Закрити (ESC)",
            on_click=lambda e: close_image_viewer()
        )
        
        # Кнопка масштабування
        zoom_button = ft.IconButton(
            icon=ft.Icons.ZOOM_IN,
            icon_color=ft.Colors.WHITE,
            icon_size=25,
            bgcolor=ft.Colors.BLACK54,
            tooltip="Оригінальний розмір",
            on_click=lambda e: toggle_zoom()
        )
        
        # Стан масштабування
        is_zoomed = False
        
        def toggle_zoom():
            nonlocal is_zoomed
            if is_zoomed:
                # Повертаємо до підганяння під розмір
                image_widget.fit = ft.ImageFit.CONTAIN
                image_widget.width = window_width - 20
                image_widget.height = window_height - 60
                zoom_button.icon = ft.Icons.ZOOM_IN
                zoom_button.tooltip = "Оригінальний розмір"
                is_zoomed = False
            else:
                # Показуємо в оригінальному розмірі
                image_widget.fit = ft.ImageFit.NONE
                image_widget.width = None
                image_widget.height = None
                zoom_button.icon = ft.Icons.ZOOM_OUT
                zoom_button.tooltip = "Підганяти під розмір"
                is_zoomed = True
            
            page.update()
        
        # Зображення
        image_widget = ft.Image(
            src=image_path,
            width=window_width - 20,
            height=window_height - 60,
            fit=ft.ImageFit.CONTAIN,
        )
        
        # Контейнер з прокруткою для великих зображень
        scrollable_image = ft.Container(
            content=image_widget,
            width=window_width - 20,
            height=window_height - 60,
            alignment=ft.alignment.center,
        )
        
        # Панель управління
        control_panel = ft.Row([
            ft.Container(expand=True),  # Пустий простір зліва
            zoom_button,
            ft.Container(width=10),  # Відстань між кнопками
            close_button,
        ], 
        height=50,
        alignment=ft.MainAxisAlignment.END)
        
        # Головний контейнер
        viewer_container = ft.Container(
            content=ft.Column([
                control_panel,
                ft.Container(
                    content=scrollable_image,
                    expand=True,
                    padding=ft.padding.all(10)
                )
            ], 
            spacing=0,
            expand=True),
            width=window_width,
            height=window_height,
            bgcolor=ft.Colors.BLACK87,
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.all(10)
        )
        
        # Створюємо повноекранний діалог
        dialog = ft.AlertDialog(
            modal=True,
            content=viewer_container,
            content_padding=ft.padding.all(0),
            actions=[],  # Прибираємо стандартні actions
            actions_padding=ft.padding.all(0),
            title_padding=ft.padding.all(0),
            inset_padding=ft.padding.all(20),  # Відступ від країв екрану
        )
        
        def close_image_viewer():
            """Закриває переглядач зображень"""
            dialog.open = False
            page.update()
            page.overlay.remove(dialog)
        
        # Обробка клавіш (ESC для закриття)
        def on_keyboard(e: ft.KeyboardEvent):
            if e.key == "Escape":
                close_image_viewer()
        
        page.on_keyboard_event = on_keyboard
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    
    def show_placeholder_dialog():
        """Показує діалог з інформацією про відсутність зображень"""
        if not page:
            return
            
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Інформація"),
            content=ft.Text(
                "Демо зображення не знайдені.\n"
                "Додайте зображення до папки 'image' в корені проекту.",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton(
                    text="Зрозуміло",
                    on_click=lambda e: close_dialog(dialog)
                )
            ]
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    def close_dialog(dialog):
        """Закриває діалог"""
        dialog.open = False
        page.update()
        page.overlay.remove(dialog)
    
    # Кнопка для додавання тестових зображень
    add_button = ft.ElevatedButton(
        text="Додати демо зображення",
        icon=ft.Icons.ADD_A_PHOTO,
        on_click=lambda e: add_demo_image(),
        bgcolor=ft.Colors.BLUE_400,
        color=ft.Colors.WHITE,
        height=40
    )
    
    # Кнопка очистки галереї
    clear_button = ft.ElevatedButton(
        text="Очистити галерею",
        icon=ft.Icons.CLEAR_ALL,
        on_click=lambda e: clear_gallery(),
        bgcolor=ft.Colors.RED_400,
        color=ft.Colors.WHITE,
        height=40
    )
    
    def clear_gallery():
        """Очищає галерею"""
        gallery_images.clear()
        gallery_grid.controls.clear()
        if page:
            page.update()
    
    return ft.Tab(
        text=lang_manager.get_text("image_tab"),
        icon=ft.Icons.IMAGE,
        content=ft.Container(
            content=ft.Column([
                # Заголовок
                ft.Text(
                    lang_manager.get_text("image_tab_title"), 
                    size=20, 
                    weight=ft.FontWeight.BOLD
                ),
                ft.Divider(height=10),
                
                # Панель кнопок
                ft.Row([
                    add_button,
                    clear_button,
                ], spacing=10),
                
                ft.Divider(height=10),
                
                # Галерея зображень
                ft.Container(
                    content=gallery_grid,
                    expand=True,
                    border_radius=ft.border_radius.all(8),
                    border=ft.border.all(1, ft.Colors.OUTLINE),
                )

            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            expand=True),
            padding=20
        )
    )
