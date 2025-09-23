import flet as ft

def get_main_tab(lang_manager, char_counter, text_input, submit_button=None, page=None):

    # Контейнер для динамічного додавання меню етапів
    stages_main_container = ft.Column()

    def on_stage_click(e):
        # Функція-заглушка для обробки кліку по етапу
        print(f"Етап '{e.control.label}' для мови '{e.control.data}' змінено на: {e.control.value}")

    def create_stages_menu(language_code):
        """Створює СУВОРО ГОРИЗОНТАЛЬНЕ меню етапів для вказаної мови."""
        stages = [
            "stage_translation", "stage_images", "stage_voiceover", "stage_subtitles",
            "stage_montage", "stage_description", "stage_preview"
        ]
        
        # Створюємо чекбокси з увімкненим станом за замовчуванням
        stage_checkboxes = [
            ft.Checkbox(
                label=lang_manager.get_text(stage),
                data=language_code,
                on_change=on_stage_click,
                value=True  # Чекбокси увімкнені за замовчуванням
            ) for stage in stages
        ]
        
        # Об'єднуємо заголовок та чекбокси в один горизонтальний ряд
        controls_in_row = [
            ft.Text(f"{lang_manager.get_text('stages_label')} ({language_code}):", weight=ft.FontWeight.BOLD, size=14)
        ]
        controls_in_row.extend(stage_checkboxes)

        # Створюємо візуально відокремлений блок для кожної мови
        return ft.Container(
            # Вся магія тут: Row без переносу, обгорнутий у контейнер з прокруткою
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=controls_in_row,
                        spacing=15,
                    )
                ],
                # Вмикаємо горизонтальну прокрутку, якщо контент не вміщується
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            padding=15,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(top=10)
        )

    def update_stages_menus(e):
        """Оновлює видимість та вміст меню етапів на основі вибраних мов."""
        stages_main_container.controls.clear()
        for cb in language_checkboxes:
            if cb.value:
                stages_main_container.controls.append(create_stages_menu(cb.label))
        stages_main_container.update()

    # Створюємо чекбокси для мов
    languages = ["UA", "RO", "PL"]
    language_checkboxes = [
        ft.Checkbox(label=lang, on_change=update_stages_menus) for lang in languages
    ]
    languages_row = ft.Row(controls=language_checkboxes)
    
    main_submit_button = ft.ElevatedButton(
        text=lang_manager.get_text("submit_button"),
        icon=ft.Icons.SEND,
        bgcolor=ft.Colors.GREEN_500,
        color=ft.Colors.WHITE,
        width=240,
        height=50,
        on_click=submit_button.on_click if submit_button else None
    )
    
    # Основний контент вкладки, обгорнутий в колонку з прокруткою
    tab_content = ft.Column(
        [
            ft.Text(lang_manager.get_text("main_tab_title") if lang_manager.get_text("main_tab_title") != "main_tab_title" else lang_manager.get_text("main_tab"), size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20),
            char_counter,
            text_input,
            ft.Text(lang_manager.get_text("translation_languages_label"), size=16),
            languages_row,
            stages_main_container,
            ft.Container(height=15),
            ft.Row([main_submit_button], alignment=ft.MainAxisAlignment.CENTER),
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