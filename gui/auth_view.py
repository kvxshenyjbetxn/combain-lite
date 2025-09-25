import flet as ft
from firebase_auth import auth
import json
import os

# Назва файлу, де будуть зберігатися дані для входу
AUTH_CACHE_FILE = "auth_cache.json"

def get_auth_view(on_login_success):
    """
    Створює та повертає Flet Control з формою входу/реєстрації.
    :param on_login_success: Функція, яка буде викликана після успішного входу. 
                             Вона приймає один аргумент - дані користувача.
    """

    def save_credentials(email, password):
        """Зберігає логін та пароль у файл."""
        try:
            with open(AUTH_CACHE_FILE, "w") as f:
                json.dump({"email": email, "password": password}, f)
            print("Дані для входу збережено.")
        except Exception as e:
            print(f"Помилка збереження даних: {e}")

    def clear_credentials():
        """Видаляє файл зі збереженими даними."""
        if os.path.exists(AUTH_CACHE_FILE):
            os.remove(AUTH_CACHE_FILE)
            print("Збережені дані для входу видалено.")

    def load_credentials():
        """Завантажує дані з файлу та заповнює поля."""
        if os.path.exists(AUTH_CACHE_FILE):
            try:
                with open(AUTH_CACHE_FILE, "r") as f:
                    creds = json.load(f)
                    email_input.value = creds.get("email", "")
                    password_input.value = creds.get("password", "")
                    remember_me_checkbox.value = True # Ставимо галочку, якщо є дані
            except Exception as e:
                print(f"Помилка завантаження даних: {e}")


    def login_or_register(e):
        email = email_input.value
        password = password_input.value

        if not email or not password:
            show_error("Будь ласка, введіть email та пароль")
            return

        try:
            if e.control.text == "Увійти":
                user = auth.sign_in_with_email_and_password(email, password)
                print("Успішний вхід!")
            else:  # Реєстрація
                user = auth.create_user_with_email_and_password(email, password)
                print("Успішна реєстрація!")
            
            # Логіка збереження паролю
            if remember_me_checkbox.value:
                save_credentials(email, password)
            else:
                clear_credentials()

            # Викликаємо callback функцію з даними користувача
            on_login_success(user)

        except Exception as ex:
            try:
                error_json = ex.args[1]
                error_message = eval(error_json)['error']['message']
                if error_message == "EMAIL_EXISTS":
                    show_error("Користувач з таким email вже існує.")
                elif error_message == "EMAIL_NOT_FOUND" or error_message == "INVALID_PASSWORD":
                    show_error("Неправильний email або пароль.")
                else:
                    show_error("Сталася помилка. Спробуйте ще раз.")
            except:
                show_error("Не вдалося підключитися до сервера.")

    def show_error(message):
        error_text.value = message
        error_text.visible = True
        error_text.update()

    email_input = ft.TextField(label="Email", width=300)
    password_input = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=300)
    error_text = ft.Text(visible=False, color=ft.Colors.RED)
    
    # Створюємо галочку
    remember_me_checkbox = ft.Checkbox(label="Запам'ятати мене", value=False)
    
    # Створюємо контейнер
    auth_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Вхід або Реєстрація", size=24, weight=ft.FontWeight.BOLD),
                email_input,
                password_input,
                remember_me_checkbox, # Додаємо галочку на форму
                ft.Row(
                    [
                        ft.ElevatedButton("Увійти", on_click=login_or_register, width=145),
                        ft.ElevatedButton("Реєстрація", on_click=login_or_register, width=145)
                    ],
                    spacing=10
                ),
                error_text,
            ],
            spacing=15, # Трохи змінив відступ для краси
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )
    
    # Одразу при створенні форми намагаємося завантажити дані
    load_credentials()
    
    return auth_container