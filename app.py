import flet as ft
from gui.auth_view import get_auth_view, AUTH_CACHE_FILE
from main import build_main_view
from firebase_auth import auth, stream_manager
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
        build_main_view(page, user_data, logout)

    def show_login_screen():
        """Показує екран авторизації."""
        print("Показуємо екран входу.")
        page.clean()
        auth_control = get_auth_view(on_login_success)
        page.add(auth_control)
        page.update()
        
    def logout(e=None):
      """Функція виходу з акаунту."""
      print("Вихід з акаунту. Зупиняю потік Firebase...")
      stream_manager.close_stream()
      
      cache_file = AUTH_CACHE_FILE
      if os.path.exists(cache_file):
          os.remove(cache_file)
          print("Кеш авторизації очищено.")
      
      show_login_screen()

    # --- ЛОГІКА АВТОМАТИЧНОГО ВХОДУ ---
    def try_auto_login():
        """Спроба автоматичного входу при запуску програми."""
        if not os.path.exists(AUTH_CACHE_FILE):
            show_login_screen()
            return

        try:
            with open(AUTH_CACHE_FILE, "r") as f:
                creds = json.load(f)
                email = creds.get("email")
                password = creds.get("password")

                if email and password:
                    print(f"Знайдено збережені дані для {email}. Спроба автоматичного входу...")
                    user = auth.sign_in_with_email_and_password(email, password)
                    on_login_success(user)
                else:
                    show_login_screen()
            
        except Exception as e:
            print(f"Помилка автоматичного входу: {e}")
            show_login_screen()
    
    try_auto_login()

if __name__ == "__main__":
    ft.app(target=main)