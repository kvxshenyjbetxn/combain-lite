import flet as ft
import time
from collections import defaultdict
import uuid
import os

from firebase_auth import stream_manager

# Словник для зберігання завдань, відправлених на сервер
submitted_tasks = {}

def get_main_tab(lang_manager, char_counter, text_input, card_title_input, page=None, user_data=None, db=None):

    local_tasks_queue = []
    tasks_container = ft.ResponsiveRow(spacing=10, run_spacing=10)
    
    # --- Функція для оновлення UI картки ---
    def update_task_card_ui(task_id, new_data):
        if task_id in submitted_tasks:
            card_control = submitted_tasks[task_id]['card_control']
            
            # Оновлюємо статус в UI
            status_indicator = card_control.controls[0].content.controls[0].controls[0].content.controls[1]
            status_text = new_data.get('status', 'unknown')
            
            status_map = {
                "new": (lang_manager.get_text("task_new"), ft.Colors.GREY),
                "processing": (lang_manager.get_text("task_processing"), ft.Colors.BLUE),
                "completed_translation": (lang_manager.get_text("task_completed"), ft.Colors.GREEN),
                "error": (lang_manager.get_text("task_error"), ft.Colors.RED)
            }
            
            status_display_text, status_color = status_map.get(status_text, (status_text, ft.Colors.BLACK))
            
            status_indicator.value = status_display_text
            status_indicator.color = status_color
            
            # Зберігаємо результат, якщо він є
            save_task_results(task_id, new_data)

            if page: page.update()

    # --- Функція для збереження результатів ---
    def save_task_results(task_id, task_data):
        print("\n--- ДІАГНОСТИКА ЗБЕРЕЖЕННЯ ---")
        print(f"Завдання ID: {task_id}")
        print(f"Отриманий статус: {task_data.get('status')}")

        if task_data.get('status') != 'completed_translation':
            print("Статус не 'completed_translation'. Збереження пропущено.")
            print("--- КІНЕЦЬ ДІАГНОСТИКИ ---\n")
            return
        
        print("Статус коректний. Починаю спробу збереження...")
        results_path = lang_manager.get_results_path()
        task_title = task_data.get('title', f'task_{task_id}')
        print(f"Шлях для збереження: {results_path}")
        
        selected_stages = task_data.get("selected_stages", {})
        if not selected_stages:
            print("Помилка: блок 'selected_stages' відсутній в даних.")
        
        for lang, stages in selected_stages.items():
            print(f"  - Перевірка мови: {lang}")
            translated_text = stages.get('translated_text')
            
            if translated_text:
                print(f"    > Знайдено перекладений текст! Спроба зберегти файл...")
                try:
                    lang_folder = os.path.join(results_path, lang)
                    os.makedirs(lang_folder, exist_ok=True)
                    
                    file_name = f"{task_title.replace(' ', '_')}.txt"
                    file_path = os.path.join(lang_folder, file_name)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(translated_text)
                    print(f"    > УСПІХ: Результат для '{task_title}' ({lang}) збережено в {file_path}")
                        
                except Exception as e:
                    print(f"    > ПОМИЛКА: Не вдалося зберегти файл для {lang}: {e}")
            else:
                print(f"    > Текст для перекладу для мови '{lang}' не знайдено (translated_text is None or empty).")
        
        print("--- КІНЕЦЬ ДІАГНОСТИКИ ---\n")

    # --- Створюємо глобальний слухач для всіх завдань користувача ---
    if user_data and db:
        user_id = user_data['localId']
        tasks_ref = db.child("tasks").child(user_id)

        def firebase_stream_handler(message):
            # Реагуємо тільки на подію 'patch', яка несе оновлення
            if message["event"] != "patch" or not message.get("data"):
                return

            path = message["path"]
            data = message["data"]
            
            # Визначаємо ID завдання з шляху
            path_parts = path.strip("/").split("/")
            if not path_parts:
                return
            task_id = path_parts[0]

            if not task_id or task_id not in submitted_tasks:
                return
            
            print(f"Отримано patch-оновлення для завдання {task_id}. Шлях: '{path}', Дані: {data}")

            # Отримуємо поточну локальну копію даних
            current_task_data = submitted_tasks[task_id]['data']

            # Беремо шлях ОПІСЛЯ ID завдання
            keys = path_parts[1:]
            
            # Якщо шлях порожній, оновлюємо корінь завдання
            if not keys:
                current_task_data.update(data)
            else:
                # Інакше, йдемо по вкладеному шляху
                target_dict = current_task_data
                for key in keys[:-1]:
                    target_dict = target_dict.setdefault(key, {})
                # Оновлюємо фінальний словник новими даними
                # Це може бути як один ключ, так і декілька (напр. status і text)
                target_dict[keys[-1]].update(data)

            # Зберігаємо оновлені дані та оновлюємо UI
            submitted_tasks[task_id]['data'] = current_task_data
            update_task_card_ui(task_id, current_task_data)


        stream_manager.start_stream(tasks_ref, firebase_stream_handler)

    stages_main_container = ft.Column()
    stages_state = defaultdict(lambda: {
        "video_title": "", "stage_translation": True, "stage_images": True, "stage_voiceover": True,
        "stage_subtitles": True, "stage_montage": True, "stage_description": True, "stage_preview": True
    })

    def delete_card_directly(e):
        local_id_to_delete = e.control.data['local_id']

        # Знаходимо та видаляємо завдання з черги даних
        task_to_delete = next((task for task in local_tasks_queue if task.get('local_id') == local_id_to_delete), None)
        if task_to_delete:
            local_tasks_queue.remove(task_to_delete)

        # Знаходимо та видаляємо картку з UI
        card_to_delete = next((card for card in tasks_container.controls if card.data and card.data.get('local_id') == local_id_to_delete), None)
        if card_to_delete:
            tasks_container.controls.remove(card_to_delete)

        main_submit_button.disabled = not local_tasks_queue
        page.update()

    def on_stage_click(e):
        lang, stage_key = e.control.data["lang"], e.control.data["stage"]
        stages_state[lang][stage_key] = e.control.value

    def on_translated_title_change(e):
        stages_state[e.control.data]["video_title"] = e.control.value

    def create_stages_menu(language_code):
        stages_keys = ["stage_translation", "stage_images", "stage_voiceover", "stage_subtitles", "stage_montage", "stage_description", "stage_preview"]
        stage_checkboxes = [ft.Checkbox(label=lang_manager.get_text(stage), data={"lang": language_code, "stage": stage}, on_change=on_stage_click, value=stages_state[language_code][stage]) for stage in stages_keys]
        
        return ft.Container(
            content=ft.Column([
                ft.Text(f"{lang_manager.get_text('stages_label')} ({language_code}):", weight=ft.FontWeight.BOLD, size=14),
                ft.Row(controls=stage_checkboxes, scroll=ft.ScrollMode.ADAPTIVE),
                ft.Container(height=5),
                ft.TextField(label=f"{lang_manager.get_text('translated_video_title_label')} ({language_code})", value=stages_state[language_code]["video_title"], on_change=on_translated_title_change, data=language_code, dense=True, border_color=ft.Colors.BLUE_GREY)
            ]),
            padding=15, border=ft.border.all(1, ft.Colors.OUTLINE), border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(top=10), opacity=0, animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_IN)
        )

    def create_task_card(title, languages_with_stages, task_data_ref):
        content_column = ft.Column(spacing=15, visible=False)
        for lang, data in languages_with_stages.items():
            translated_title = data.get("video_title", "").strip() or f"{lang} {title}"
            active_stages = {stage: active for stage, active in data.items() if stage != "video_title" and active}
            if active_stages:
                stages_list = ft.Column(spacing=5, controls=[ft.Row([ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN_500, size=16), ft.Text(lang_manager.get_text(stage_key), size=14)]) for stage_key in active_stages])
                content_column.controls.append(ft.Column([
                    ft.Text(lang, weight=ft.FontWeight.BOLD, size=16),
                    ft.Container(content=ft.Column([
                        ft.Row([ft.Text(f"{lang_manager.get_text('translated_video_title_label')}:", weight=ft.FontWeight.BOLD), ft.Text(f'"{translated_title}"')]),
                        ft.Divider(height=8, thickness=0.5),
                        ft.Text(lang_manager.get_text("stages_label"), italic=True, size=12),
                        stages_list
                    ]), padding=ft.padding.only(left=10))
                ]))
        
        card_container = ft.Container()
        final_card_column = ft.Column(col={"xs": 12, "sm": 6, "md": 4, "lg": 3}, controls=[card_container], data={'local_id': task_data_ref.get('local_id')})
        
        def toggle_card_expansion(e):
            content_column.visible = not content_column.visible
            expand_icon.name = ft.Icons.KEYBOARD_ARROW_UP if content_column.visible else ft.Icons.KEYBOARD_ARROW_DOWN
            card_container.update()

        expand_icon = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN)
        status_indicator = ft.Text(lang_manager.get_text("task_new"), color=ft.Colors.GREY, italic=True)
        delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_FOREVER,
            icon_color=ft.Colors.RED_500,
            tooltip=lang_manager.get_text("delete_from_queue_tooltip"),
            on_click=delete_card_directly,
            data={'local_id': task_data_ref.get('local_id')}
        )
        
        header_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(value=title, weight=ft.FontWeight.BOLD, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),
                        status_indicator,
                    ], spacing=0),
                    expand=True,
                    on_click=toggle_card_expansion,
                    padding=ft.padding.only(left=15)
                ),
                delete_button,
                ft.Container(content=expand_icon, on_click=toggle_card_expansion, padding=ft.padding.only(right=10))
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            height=50
        )
        
        card_container.content = ft.Column(
            controls=[
                header_row,
                ft.Container(content=content_column, padding=ft.padding.only(left=15, right=15, bottom=15, top=5), animate_size=ft.Animation(150, ft.AnimationCurve.DECELERATE))
            ],
            spacing=0
        )
        card_container.border = ft.border.all(1, ft.Colors.OUTLINE)
        card_container.border_radius = ft.border_radius.all(8)
        
        return final_card_column

    def add_to_queue_click(e):
        text_to_process = text_input.value or ""
        selected_languages = [cb.label for cb in language_checkboxes if cb.value]
        if not selected_languages or not text_to_process:
            return

        title = card_title_input.value.strip() or f"Завдання {len(local_tasks_queue) + 1}"

        task_data = {
            "local_id": str(uuid.uuid4()),
            "userId": user_data['localId'],
            "original_text": text_to_process,
            "title": title,
            "selected_stages": {lang: stages_state.get(lang, {}).copy() for lang in selected_languages},
            "status": "new",
        }
        local_tasks_queue.append(task_data)
        
        task_data_for_card = {lang: stages_state[lang] for lang in selected_languages}
        card_control = create_task_card(title, task_data_for_card, task_data)
        tasks_container.controls.insert(0, card_control)
        
        main_submit_button.disabled = False
        text_input.value, card_title_input.value = "", ""
        for cb in language_checkboxes: cb.value = False
        stages_state.clear()
        update_ui_elements()
        if page:
            text_input.update()
            card_title_input.update()
            char_counter.value = lang_manager.get_text("characters_count", 0)
            char_counter.update()

    def on_submit_click(e):
        if not user_data or not db or not local_tasks_queue:
            return

        submitted_cards = list(tasks_container.controls)
        
        for i, task_data in enumerate(local_tasks_queue):
            try:
                task_id = str(uuid.uuid4())
                user_id = task_data['userId']
                
                # Додаємо час створення перед відправкою
                task_data_to_send = task_data.copy()
                task_data_to_send["created_at"] = int(time.time())
                
                db.child("tasks").child(user_id).child(task_id).set(task_data_to_send)
                
                # Зберігаємо картку для майбутніх оновлень
                card_control = submitted_cards[len(local_tasks_queue) - 1 - i]
                submitted_tasks[task_id] = {
                    'data': task_data_to_send,
                    'card_control': card_control
                }
                
                # Вимикаємо кнопку видалення для відправленої картки
                delete_button = card_control.controls[0].content.controls[0].controls[1]
                delete_button.disabled = True

            except Exception as ex:
                print(f"Помилка відправки завдання '{task_data['title']}' в Firebase: {ex}")

        snack_bar = ft.SnackBar(content=ft.Text(lang_manager.get_text("queue_sent_message", len(local_tasks_queue))))
        local_tasks_queue.clear()
        main_submit_button.disabled = True
        if page:
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            
    def update_ui_elements(e=None):
        selected_languages = [cb.label for cb in language_checkboxes if cb.value]
        text_present = bool(text_input.value)

        add_to_queue_button.disabled = not (selected_languages and text_present)
        if page: add_to_queue_button.update()

        for menu in stages_main_container.controls: menu.opacity = 0
        if page: page.update()
        time.sleep(0.4)
        stages_main_container.controls.clear()
        for lang_code in selected_languages: stages_main_container.controls.append(create_stages_menu(lang_code))
        if page: page.update()
        time.sleep(0.05)
        for menu in stages_main_container.controls: menu.opacity = 1
        if page: page.update()

    languages = ["French", "English", "Russian", "Portuguese", "Spanish", "Italian", "Ukrainian"]
    language_checkboxes = [ft.Checkbox(label=lang, on_change=update_ui_elements) for lang in languages]
    languages_row = ft.Row(controls=language_checkboxes, scroll=ft.ScrollMode.ADAPTIVE)
    
    add_to_queue_button = ft.ElevatedButton(
        text=lang_manager.get_text("add_to_queue_button"), 
        icon=ft.Icons.ADD_TO_QUEUE, 
        on_click=add_to_queue_click, 
        disabled=True
    )
    
    main_submit_button = ft.ElevatedButton(
        text=lang_manager.get_text("submit_queue_button"), 
        icon=ft.Icons.SEND, 
        bgcolor=ft.Colors.GREEN_500, 
        color=ft.Colors.WHITE, 
        width=300, 
        height=50, 
        on_click=on_submit_click, 
        disabled=True
    )

    text_input.on_change = update_ui_elements
    card_title_input.on_change = update_ui_elements

    return ft.Tab(
        text=lang_manager.get_text("main_tab"), icon=ft.Icons.EDIT,
        content=ft.Container(content=ft.Column([
            ft.Text(lang_manager.get_text("main_tab_title"), size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10),
            card_title_input, 
            char_counter, 
            text_input,
            ft.Text(lang_manager.get_text("translation_languages_label"), size=16),
            languages_row, 
            stages_main_container,
            ft.Container(
                content=add_to_queue_button,
                padding=ft.padding.only(top=15)
            ),
            ft.Divider(height=20),
            ft.Text(lang_manager.get_text("submission_queue_title"), size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=tasks_container,
                padding=ft.padding.only(top=10)
            ),
            ft.Container(height=15),
            ft.Row([main_submit_button], alignment=ft.MainAxisAlignment.CENTER),
        ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE), padding=20)
    )