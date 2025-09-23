import flet as ft
import time

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
        
        stage_checkboxes = [
            ft.Checkbox(
                label=lang_manager.get_text(stage),
                data=language_code,
                on_change=on_stage_click,
                value=True
            ) for stage in stages
        ]
        
        controls_in_row = [
            ft.Text(f"{lang_manager.get_text('stages_label')} ({language_code}):", weight=ft.FontWeight.BOLD, size=14)
        ]
        controls_in_row.extend(stage_checkboxes)

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=controls_in_row,
                        spacing=15,
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            padding=15,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(top=10),
            
            # Налаштування анімації прозорості
            opacity=0, # Початковий стан: прозорий
            animate_opacity=ft.Animation(duration=400, curve=ft.AnimationCurve.EASE_IN),
        )

    def update_stages_menus(e):
        """Оновлює меню етапів з коректною анімацією появи та зникнення."""
        # Очищуємо контейнер і знову наповнюємо його, щоб уникнути складного управління станами
        stages_main_container.controls.clear()
        for cb in language_checkboxes:
            if cb.value:
                stages_main_container.controls.append(create_stages_menu(cb.label))
        
        # Якщо немає елементів, просто оновлюємо порожній контейнер
        if not stages_main_container.controls:
            page.update()
            return

        # 1. Перше оновлення: додає на сторінку невидимі елементи (opacity=0)
        page.update()
        
        # 2. Даємо Flet мить на обробку першого оновлення
        time.sleep(0.05)
        
        # 3. Змінюємо прозорість на 1 для всіх елементів
        for menu in stages_main_container.controls:
            menu.opacity = 1
        
        # 4. Друге оновлення: запускає анімацію проявлення
        page.update()

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