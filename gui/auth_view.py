import flet as ft
from firebase_auth import auth

def get_auth_view(on_login_success):
    """
    Створює та повертає Flet Control з формою входу/реєстрації.
    :param on_login_success: Функція, яка буде викликана після успішного входу. 
                             Вона приймає один аргумент - дані користувача.
    """
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

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Вхід або Реєстрація", size=24, weight=ft.FontWeight.BOLD),
                email_input,
                password_input,
                ft.Row(
                    [
                        ft.ElevatedButton("Увійти", on_click=login_or_register, width=145),
                        ft.ElevatedButton("Реєстрація", on_click=login_or_register, width=145)
                    ],
                    spacing=10
                ),
                error_text,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )