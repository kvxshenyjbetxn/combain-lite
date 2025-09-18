import flet as ft


def main(page: ft.Page):
    page.title = "Combain"
    page.window_width = 600
    page.window_height = 500
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
        min_lines=10,
        max_lines=15,
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
        
        # Показуємо повідомлення користувачу
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(f"Текст відправлено на обробку! ({len(text)} символів)"),
                action="OK",
                action_color=ft.Colors.BLUE
            )
        )
    
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
    
    # Додаємо всі елементи на сторінку
    page.add(
        ft.Column([
            ft.Text(
                "Програма-пустишка",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            char_counter,
            ft.Container(height=5),  # Невеликий відступ
            text_input,
            ft.Container(height=15),  # Відступ між полем та кнопкою
            ft.Row([
                submit_button
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], 
        spacing=0,
        alignment=ft.MainAxisAlignment.START
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
