import flet as ft
from gui.auth_view import get_auth_view, AUTH_CACHE_FILE # Імпортуємо назву файлу
from main import build_main_view
from firebase_auth import auth # Імпортуємо auth для авто-входу
import json
import os

def main(page: ft.Page):
    page.title = "Combain"
    page.window.width = 1280
    page.window.height = 800

    def on_login_success(user_data):
        """Ця функція викликається, коли користувач успішно увійшов."""
        print(f"Користувач {user_data.get('email', 'unknown')} увійшов. Будуємо основний інтерфейс.")
        page.clean()
        build_main_view(page, user_data)

    def show_login_screen():
        """Показує екран авторизації."""
        print("Показуємо екран входу.")
        page.clean()
        auth_control = get_auth_view(on_login_success)
        page.add(auth_control)
        page.update()

    # --- ЛОГІКА АВТОМАТИЧНОГО ВХОДУ ---
    def try_auto_login():
        """Спроба автоматичного входу при запуску програми."""
        if not os.path.exists(AUTH_CACHE_FILE):
            # Якщо файлу немає, просто показуємо екран входу
            show_login_screen()
            return

        try:
            with open(AUTH_CACHE_FILE, "r") as f:
                creds = json.load(f)
                email = creds.get("email")
                password = creds.get("password")

                if email and password:
                    print(f"Знайдено збережені дані для {email}. Спроба автоматичного входу...")
                    # Намагаємося увійти з цими даними
                    user = auth.sign_in_with_email_and_password(email, password)
                    # Якщо успішно - викликаємо головну функцію
                    on_login_success(user)
                else:
                    show_login_screen()
            
        except Exception as e:
            # Якщо сталася помилка (напр., неправильний пароль), просто показуємо екран входу
            print(f"Помилка автоматичного входу: {e}")
            show_login_screen()
    
    # Запускаємо спробу автоматичного входу
    try_auto_login()

if __name__ == "__main__":
    ft.app(target=main)