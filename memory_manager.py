
import json
import os

class AssistantMemory:
    def __init__(self, filename='memory.json'):
        self.filename = filename
        self.memory = {}
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    self.memory = json.load(f)
                except json.JSONDecodeError:
                    self.memory = {}
        else:
            self.memory = {}

    def save_memory(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=4, ensure_ascii=False)

    def remember(self, key, value):
        self.memory[key] = value
        self.save_memory()

    def recall(self, key, default=None):
        return self.memory.get(key, default)

    def forget(self, key):
        if key in self.memory:
            del self.memory[key]
            self.save_memory()

    # 🆕 Додаємо метод для зустрічей
    def add_meeting(self, date, time, topic):
        if "meetings" not in self.memory:
            self.memory["meetings"] = []
        self.memory["meetings"].append({
            "date": date,
            "time": time,
            "topic": topic
        })
        self.save_memory()


    def get_meetings(self):
        return self.memory.get("meetings", [])

    def clear_meetings(self):
        self.memory["meetings"] = []
        self.save_memory()