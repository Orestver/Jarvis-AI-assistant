from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout,QLineEdit,QFileDialog,QHBoxLayout
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer, pyqtSlot
import sys
from elevenlabsspeach import speak
import asyncio
from FIleSummariser import read_file
from model_with_UI_con import summarize_text
import playsound, os
import urllib.parse

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # коли запаковано в .exe
    except AttributeError:
        base_path = os.path.abspath(".")  # коли просто скрипт
    return os.path.join(base_path, relative_path)

class Jarvis_UI(QWidget):
    text_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.text_signal.connect(self.type_text_effect)
        self.init_window()
        self.init_UI()
        self.init_voice()
        self.text_UI()
        self.init_user_input()
        self.init_file_input()

        self._printed_text = "" 
        self.recent_lines = []       # останні 5 рядків для відображення
        self.printed_lines = []
        
    def init_window(self):
        self.setWindowTitle("Jarvis")
        self.setGeometry(800, 300, 400, 600)
        self.setStyleSheet("background-color: black;" \
        "border: 3px solid navy;" \
        "border-radius: 8px;"
        )
        self.setWindowIcon(QIcon(("frontend/LOGO (2).jpg")))
        self.setWindowFlags(Qt.Window |
                            Qt.WindowMinimizeButtonHint |
                            Qt.WindowCloseButtonHint)

    def init_UI(self):
        # 1. GIF у вигляді статичного кадру
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(0, 0, 400, 400)
        self.movie = QMovie("frontend/V2 Jarvis.gif")
        self.movie.setScaledSize(QSize(400, 400))
        self.gif_label.setMovie(self.movie)

        self.gif_label.show()
        self.gif_label.raise_()
        self.movie.start()
        # 2. Окремий прозорий контейнер поверх для кнопки
        self.overlay = QWidget(self)
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        self.btn = QPushButton("Запустити GIF")
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #222;
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
            }
        """)
        layout.addStretch()
        self.close_btn = QPushButton("Зупинити GIF")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #222;
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
            }
        """)
        

    def init_voice(self):
        self.voice_label = QLabel(self)
        self.voice_label.setGeometry(80,400,200,100)
        self.movie_voice = QMovie("frontend/Jarvis speak.gif")
        self.movie_voice.setScaledSize(QSize(400, 400))
        self.voice_label.setMovie(self.movie_voice)
        self.movie_voice.jumpToFrame(0)  
        self.movie_voice.stop()          
        self.voice_label.show()

    def start_voice(self):
        self.voice_label.show()
        self.voice_label.raise_()
        self.movie_voice.start()
        
    def stop_voice(self):
        self.gif_label.show()
        self.gif_label.raise_()
        self.movie_voice.stop()

    def text_UI(self):
        self.text_label = QLabel(self)
        self.text_label.setGeometry(0, 400, 400, 200)
        self.text_label.setStyleSheet(""" 
            QLabel{ 
                background: #4b4f57;
                border-radius: 8px;
                padding: 6px 12px;
                border: 3px solid navy;
                color: lightblue;
            }
        """)
        self.text_label.setText("")
        self.text_label.setWordWrap(True)
        self._full_text = ""
        self._typed_text = ""
        self._type_index = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._append_next_char)

        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self.cleanup_old_lines)
        self.cleanup_timer.start(5000)  # кожні 5 секунд


    def type_text_effect(self, text):
        self.recent_lines.append(text)

        # Підготувати до друку лише новий рядок
        self._full_text = text
        self._typed_text = ""
        self._type_index = 0
        self._timer.start(40)



    def _append_next_char(self):
        if self._type_index < len(self._full_text):
            self._typed_text += self._full_text[self._type_index]
            combined_text = "\n".join(self.printed_lines + [self._typed_text])
            self.text_label.setText(combined_text)
            self._type_index += 1
        else:
            self.printed_lines.append(self._full_text)  # Додаємо завершений рядок
            self._timer.stop()


    def cleanup_old_lines(self):
        if len(self.recent_lines) >= 5:
            self.recent_lines.pop(0)
        if len(self.printed_lines) >= 5:
            self.printed_lines.pop(0)

        combined_text = "\n".join(self.printed_lines)
        self.text_label.setText(combined_text)


    def init_user_input(self):
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(10, 570, 280, 30)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #222;
                color: white;
                border-radius: 6px;
                padding: 4px 8px;
            }
        """)
        self.input_field.setPlaceholderText("You: ")

        self.send_button = QPushButton("OK", self)
        self.send_button.setGeometry(300, 570, 80, 30)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #82a6e0;
                color: white;
                border-radius: 6px;
            }
        """)
        self.send_button.setHidden(True)  # приховуємо кнопку до активації
        self.input_field.setHidden(True)  # поле вводу вимкнено до активації
        self.send_button.clicked.connect(self.handle_input)
        self.input_field.returnPressed.connect(self.send_button.click)
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)


    def handle_input(self):
        user_text = self.input_field.text().strip().lower()
        if not user_text:
            return

        self.text_signal.emit(f"🧑‍💻: {user_text}")
        self.disable_input() 
        self.input_field.clear()

        if self.awaiting_input == "file_type":
            if user_text in ["pdf", "txt", "docx"]:
                self.collected_data["type"] = user_text
                self.awaiting_input = "file_name" 
                self.text_signal.emit("🤖: Please enter the name of the file.")
                playsound.playsound(resource_path("Jarvis_voice_commands/command_responses/Please enter the name of the file you want to create..mp3"))
                self.enable_input()
            else:
                self.text_signal.emit("🤖: Invalid type. Please enter PDF, TXT, or DOCX.")
                playsound.playsound(resource_path("Jarvis_voice_commands/command_responses/Invalid file type. Please try again..mp3"))

        elif self.awaiting_input == "file_name":
            from pathlib import Path

            self.collected_data["filename"] = user_text
            file_type = self.collected_data["type"]
            filename = user_text

            # Додати правильне розширення, якщо його нема
            if not filename.endswith(f".{file_type}"):
                filename += f".{file_type}"

            # Отримати шлях до папки "Завантаження"
            downloads_path = Path.home() / "Downloads"
            downloads_path.mkdir(parents=True, exist_ok=True)

            # Повний шлях до файлу
            full_path = downloads_path / filename
            self.collected_data["full_filename"] = str(full_path)

            self.awaiting_input = "file_confirm"

            # Спроба створити файл
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    pass
                self.text_signal.emit(f"✅ File '{filename}' created in Downloads.")
                speak(f"File {filename} created successfully in your Downloads folder.", self)

                # Питаємо, чи редагувати
                self.awaiting_input = "edit_file"
                self.text_signal.emit("🤖: Do you want to write something in this file? (yes/no)")
                speak("Do you want to write something in this file?", self)
                self.enable_input()
            except Exception as e:
                self.awaiting_input = None
                self.text_signal.emit(f"⚠️ Error creating file: {e}")
                speak(f"An error occurred while creating the file: {e}", self)

        elif self.awaiting_input == "edit_file":
            if "yes" in user_text or "так" in user_text:
                filename = self.collected_data["full_filename"]
                os.system(f'start "" "{filename}"')  # Windows-friendly відкриття файлу
                self.text_signal.emit("📂 File opened for editing.")
                speak("You can write in the file now.", self)
            else:
                self.text_signal.emit("🤖: File created without content.")
                speak("File created without any content.", self)

            self.awaiting_input = None
            self.disable_input()
            self.send_button.setHidden(True)
            self.input_field.setHidden(True)

        elif self.awaiting_input == "song_name":
            self.collected_data["songname"] = user_text
            songname = user_text
            self.awaiting_input = "song_link"
            self.text_signal.emit("Please enter the YouTube link for the song.") 
            playsound.playsound(resource_path("Jarvis_voice_commands/command_responses/Please enter the YouTube link for the song..mp3"))
            
            self.enable_input()
            
        elif self.awaiting_input == "song_link":
            self.collected_data["songlink"] = user_text
            songlink = user_text
            songname = self.collected_data["songname"]

            import os
            import json
            import shutil

            musics = {}  # початкове значення

            # Завантаження існуючого файлу, якщо він є
            if os.path.exists('musics.json') and os.path.getsize('musics.json') > 0:
                try:
                    with open('musics.json', 'r') as file:
                        musics = json.load(file)
                except json.JSONDecodeError:
                    print("⚠️ musics.json містить некоректний JSON. Починаємо з порожнього словника.")
                    musics = {}
            else:
                print("ℹ️ musics.json не існує або порожній. Створюємо новий.")

            # Перевірка на валідний ввід
            if songname and songlink:
                musics[songname] = songlink

                # Збереження резервної копії перед перезаписом
                if os.path.exists('musics.json'):
                    try:
                        shutil.copy('musics.json', 'musics_backup.json')
                        print("🗂 Резервну копію збережено як musics_backup.json.")
                    except Exception as e:
                        print(f"⚠️ Не вдалося створити бекап: {e}")

                # Запис нового JSON у файл
                with open('musics.json', 'w') as file:
                    json.dump(musics, file, indent=4)

                print("✅ Список музики збережено в musics.json.")
                self.text_signal.emit(f"Song '{songname}' added successfully.")
                speak(f"Song '{songname}' added successfully.", self)
                self.awaiting_input = None
                self.disable_input()
                self.send_button.setHidden(True)
                self.input_field.setHidden(True)
            else:
                self.text_signal.emit("Invalid input. Please try again.")
                speak("Invalid input. Please try again.", self)
                print("⚠️ Invalid input. Please try again.")
            self.send_button.setHidden(True)
            self.input_field.setHidden(True)
            

        elif self.awaiting_input == "city_name":
            self.collected_data['city_name'] = user_text
            city_name = user_text
            from weather_forecast import WeatherForecast
            weather = WeatherForecast()
            loop = asyncio.get_event_loop()
            weather_message = loop.run_until_complete(weather.get_weather(city_name))
            if weather_message:
                self.text_signal.emit(weather_message)
                speak(weather_message, self)
                self.awaiting_input = None
                self.disable_input()
            else:
                self.text_signal.emit("❌ Could not retrieve weather data.")
                speak("Could not retrieve weather data.", self)
                self.disable_input()
                self.awaiting_input = None
            self.send_button.setHidden(True)
            self.input_field.setHidden(True)
        elif self.awaiting_input == "route_destination":
            self.collected_data['route_destination'] = user_text
            destination = user_text
            if destination:
                self.text_signal.emit(f"🗺️ Opening route to {destination}...")
                speak(f"Opening route to {destination}.", self)
                import webbrowser
                url = f"https://www.google.com/maps/dir/?api=1&destination={urllib.parse.quote(destination)}"
                webbrowser.open(url)
                self.awaiting_input = None
                self.disable_input()
            else:
                self.text_signal.emit("❌ Please enter a valid destination.")
                speak("Please enter a valid destination.", self)
            self.send_button.setHidden(True)
            self.input_field.setHidden(True)

    def init_file_input(self):
        # Створюємо кнопку для drag and drop
        self.file_button = QPushButton("📥", self)
        self.file_button.setToolTip("Drag and drop file here or click to load")
        self.file_button.setGeometry(self.width() - 60, self.height() - 100, 50, 50)
        self.file_button.setStyleSheet("""
            QPushButton {
                background-color: #3a3f4b;
                color: white;
                border-radius: 8px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #4f5b6e;
            }
        """)
        self.file_button.clicked.connect(self.load_file)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_button.setText("📄")  # Змінити іконку на файл
        self.file_button.setToolTip(f"Selected: {self.file_path}")

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose the file", "", "Documents (*.txt *.pdf *.docx)")
        if path:
            self.file_path = path
            self.file_button.setText("📄")
            self.file_button.setToolTip(f"Selected: {self.file_path}")
        else:
            self.file_path = None  # Явно обнуляємо, якщо нічого не вибрано

    def summarize_loaded_file(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            self.text_signal.emit("❌ File not loaded.")
            speak("File not loaded.", self)
            return "❌ File not loaded."

        text = read_file(self.file_path)
        if not text:
            return "❌ Could not read the file."
        else:
            summary = summarize_text(text, self)
            return "🧠 Here is a short summary of the file:\n\n" + summary

    
    def enable_input(self):
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()  # курсор одразу у полі

    def disable_input(self):
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)

    def resizeEvent(self, event):
        # При зміні розміру адаптуємо
        self.gif_label.setGeometry(0, 0, self.width(), 400)
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)
        self.file_button.move(self.width() - self.file_button.width() - 10, self.height() - self.file_button.height() - 40)

def main():
    app = QApplication(sys.argv)
    window = Jarvis_UI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
