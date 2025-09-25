# firebase_auth.py
import pyrebase

# ВСТАВТЕ ВАШУ КОНФІГУРАЦІЮ FIREBASE СЮДИ
# Це дані з кроку 1.4 (Project settings -> Your apps -> Web app)

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