import flet as ft


def main(page: ft.Page):
    page.title = "Combain"
    page.window_width = 700
    page.window_height = 600
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Лічильник символів
    char_counter = ft.Text(
        "Символів: 0",
        size=14,
        color=ft.Colors.GREY_700
    )
    
    # Поле для вводу тексту
    text_input = ft.TextField(
        label="Введіть текст",
        multiline=True,
        min_lines=12,
        max_lines=18,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_600,
        expand=True
    )
    
    # Функція для оновлення лічильника символів
    def update_char_count(e):
        text = text_input.value or ""
        char_counter.value = f"Символів: {len(text)}"
        page.update()
    
    # Прив'язуємо функцію до зміни тексту
    text_input.on_change = update_char_count
    
    # Функція для кнопки відправки
    def on_submit_click(e):
        text = text_input.value or ""
        print(f"Відправлено на обробку: {len(text)} символів")
        # Тут можна додати будь-яку логіку обробки
        
        # Створюємо snack bar та додаємо його на сторінку
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Текст відправлено на обробку! ({len(text)} символів)"),
            action="OK",
            action_color=ft.Colors.BLUE
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
    
    # Кнопка відправки
    submit_button = ft.ElevatedButton(
        text="Відправити на обробку",
        icon=ft.Icons.SEND,
        on_click=on_submit_click,
        bgcolor=ft.Colors.BLUE_400,
        color=ft.Colors.WHITE,
        width=200,
        height=40
    )
    
    # Функція для зміни теми
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_switch.label = "Світла тема"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_switch.label = "Темна тема"
        page.update()
    
    # Перемикач теми
    theme_switch = ft.ElevatedButton(
        text="Темна тема",
        icon=ft.Icons.DARK_MODE,
        on_click=change_theme,
        bgcolor=ft.Colors.GREY_600,
        color=ft.Colors.WHITE,
        width=150,
        height=40
    )
    
    # Вкладка з основним функціоналом
    main_tab = ft.Tab(
        text="Основна",
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
    
    # Вкладка з налаштуваннями
    settings_tab = ft.Tab(
        text="Налаштування",
        icon=ft.Icons.SETTINGS,
        content=ft.Container(
            content=ft.Column([
                ft.Container(height=20),
                ft.Text(
                    "Налаштування програми",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Divider(height=30),
                ft.Row([
                    ft.Icon(ft.Icons.PALETTE, size=30),
                    ft.Text("Тема інтерфейсу:", size=16),
                ], spacing=10),
                ft.Container(height=10),
                theme_switch,
                ft.Container(height=30),
                ft.Text(
                    "Інформація про програму:",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(height=10),
                ft.Text("Версія: 1.0", size=14),
                ft.Text("Автор: Combain Team", size=14),
                ft.Text("Опис: Програма-пустишка для обробки тексту", size=14),
            ], 
            spacing=5,
            alignment=ft.MainAxisAlignment.START,
            expand=True
            ),
            padding=20
        )
    )
    
    # Створюємо tabs
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[main_tab, settings_tab],
        expand=True
    )
    
    # Додаємо всі елементи на сторінку
    page.add(
        ft.Column([
            ft.Text(
                "Combain",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800
            ),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            tabs
        ], 
        spacing=0,
        alignment=ft.MainAxisAlignment.START,
        expand=True
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
