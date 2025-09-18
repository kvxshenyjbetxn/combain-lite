import flet as ft


class TextProcessorApp:
    def __init__(self):
        self.text_input = None
        self.result_text = None
        
    def main(self, page: ft.Page):
        # Налаштування сторінки
        page.title = "Обробник тексту"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.padding = 20
        page.window_width = 800
        page.window_height = 700
        page.window_resizable = False
        
        # Заголовок
        title = ft.Text(
            "🔤 Обробник тексту",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700
        )
        
        # Поле для введення тексту
        self.text_input = ft.TextField(
            label="Введіть текст для обробки",
            multiline=True,
            min_lines=5,
            max_lines=8,
            hint_text="Тут можна ввести будь-який текст...",
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.GREY_50
        )
        
        # Кнопка обробки
        process_button = ft.ElevatedButton(
            text="📝 Відправити на обробку",
            on_click=self.process_text,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREEN_600,
                elevation=3,
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            height=50,
            width=300
        )
        
        # Контейнер для результату
        self.result_text = ft.Text(
            value="",
            selectable=True,
            size=14,
            color=ft.Colors.GREY_800
        )
        
        result_container = ft.Container(
            content=ft.Column([
                ft.Text("📊 Результат обробки:", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=ft.Colors.GREY_400),
                self.result_text
            ]),
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=15,
            margin=ft.margin.only(top=20),
            border=ft.border.all(1, ft.Colors.BLUE_200)
        )
        
        # Головний макет
        main_content = ft.Column([
            title,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            self.text_input,
            ft.Container(
                content=process_button,
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=20, bottom=10)
            ),
            result_container
        ], spacing=10, expand=True)
        
        # Додавання до сторінки
        page.add(main_content)
    
    def process_text(self, e):
        """Обробник натискання кнопки"""
        input_text = self.text_input.value.strip() if self.text_input.value else ""
        
        if not input_text:
            self.show_snackbar(e.page, "❌ Помилка: Будь ласка, введіть текст для обробки!", ft.Colors.RED_400)
            return
        
        # Проста обробка тексту
        processed_text = self.simple_text_processing(input_text)
        
        # Оновлення результату
        self.result_text.value = processed_text
        e.page.update()
        
        # Показати повідомлення про успіх
        self.show_snackbar(e.page, "✅ Текст успішно оброблено!", ft.Colors.GREEN_400)
    
    def simple_text_processing(self, text):
        """Проста функція обробки тексту"""
        # Підрахунок статистики
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
        word_count = len(text.split())
        line_count = len(text.split('\n'))
        
        # Перетворення тексту
        upper_text = text.upper()
        lower_text = text.lower()
        reversed_text = text[::-1]
        capitalized_text = text.title()
        
        result = f"""
📈 СТАТИСТИКА ТЕКСТУ:
┌─────────────────────────────────┐
│ Кількість символів: {char_count:>11} │
│ Символів без пробілів: {char_count_no_spaces:>8} │
│ Кількість слів: {word_count:>15} │
│ Кількість рядків: {line_count:>13} │
└─────────────────────────────────┘

🔤 ВЕРХНІЙ РЕГІСТР:
{upper_text}

🔡 нижній регістр:
{lower_text}

🎯 Заголовний Регістр:
{capitalized_text}

🔄 ЗВОРОТНИЙ ТЕКСТ:
{reversed_text}

🎨 ДОДАТКОВА ІНФОРМАЦІЯ:
• Середня довжина слова: {char_count_no_spaces/word_count:.1f} символів
• Щільність тексту: {word_count/line_count:.1f} слів на рядок
• Відсоток пробілів: {((char_count - char_count_no_spaces)/char_count*100):.1f}%
        """.strip()
        
        return result
    
    def show_snackbar(self, page, message, color):
        """Показати сповіщення внизу екрану"""
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
            duration=3000
        )
        page.snack_bar = snackbar
        snackbar.open = True
        page.update()


def main(page: ft.Page):
    app = TextProcessorApp()
    app.main(page)


if __name__ == '__main__':
    ft.app(target=main)