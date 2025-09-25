import pyrebase
import threading

# ВСТАВТЕ ВАШУ КОНФІГУРАЦІЮ FIREBASE СЮДИ
firebase_config = {
  "apiKey": "AIzaSyBnC3PpXsJdK8IPa5ufQfAkv88Zg1OB7sQ",
  "authDomain": "combain-server.firebaseapp.com",
  "databaseURL": "https://combain-server-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "combain-server",
  "storageBucket": "combain-server.firebasestorage.app",
  "messagingSenderId": "1075275446619",
  "appId": "1:1075275446619:web:0bed621bf9b6a4f9dac27e",
  "measurementId": "G-XYEXXRLRS1"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()


class FirebaseStreamManager:
    def __init__(self):
        self.stream = None
        self.thread = None

    def start_stream(self, ref, handler):
        # Зупиняємо старий потік, якщо він існує
        if self.thread and self.thread.is_alive():
            self.close_stream()

        def stream_runner():
            """Ця функція буде працювати у фоновому потоці."""
            try:
                self.stream = ref.stream(handler)
            except Exception as e:
                print(f"Помилка в потоці Firebase: {e}")

        # Створюємо та запускаємо потік-ДЕМОН.
        # daemon=True - ключовий параметр. Він дозволяє головній програмі закритись,
        # не чекаючи завершення цього потоку.
        self.thread = threading.Thread(target=stream_runner, daemon=True)
        self.thread.start()
        print("Firebase stream daemon thread started.")

    def close_stream(self):
        if self.stream:
            try:
                self.stream.close()
                self.stream = None
                print("Firebase stream closed on request.")
            except Exception as e:
                print(f"Error closing Firebase stream: {e}")
        self.thread = None

# Глобальний менеджер для стріму
stream_manager = FirebaseStreamManager()