import sys, asyncio, threading
from PyQt5.QtWidgets import QApplication
from UIagent import Jarvis_UI
from model_with_UI_con import run_voice_assistant

app = QApplication(sys.argv)
ui_window = Jarvis_UI()
ui_window.show()

def start_async_loop():
    asyncio.run(run_voice_assistant(ui_window=ui_window))

if __name__ == '__main__':
    threading.Thread(target=start_async_loop, daemon=True).start()
    sys.exit(app.exec_())

