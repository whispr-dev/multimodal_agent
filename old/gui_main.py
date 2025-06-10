import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTextEdit, QPushButton, QTabWidget, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap, QFont
from modules.llm_core import LLMEngine
from modules.memory import MemoryEngine
from modules.tts_output import speak_text, TTSEngine
from modules.audio_input import record_audio
from modules.vision import describe_image, VisionModule
from modules.emotion import detect_emotion
from modules.utils import load_identity_profile
from PyQt5.QtCore import QTimer, Qt

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

class FrenAgentGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("fren-agent :: Multimodal Companion")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("QTabWidget::pane { border: 1px solid gray; }")

        self.vision = VisionModule()
        self.init_vision_timer()

        self.llm = LLMEngine()
        self.tts = TTSEngine()
        self.memory = MemoryEngine()

        self.identity = load_identity_profile()
        self.setWindowTitle(f"{self.identity['agent_name']} :: Multimodal Companion")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_agent_tab()
        self.init_vision_tab()
        self.init_audio_tab()
        self.init_memory_tab()
        self.init_settings_tab()
        self.init_logs_tab()

    def update_vision_tab(self):
        pixmap = self.vision.get_frame_qpixmap()
    pixmap_path = "assets/agent_logo.png"
    if os.path.exists(pixmap_path):
        pixmap = QPixmap(pixmap_path)
        label.setPixmap(pixmap)
        caption = self.vision.describe_frame()
        self.scene_desc.setText(f"Scene: {caption}")


    # 🧠 Agent Interaction
    def init_agent_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Courier", 10))

        self.chat_input = QTextEdit()
        self.chat_input.setFixedHeight(60)

        send_btn = QPushButton("Say It")
        send_btn.clicked.connect(self.handle_chat)

        layout.addWidget(QLabel("Fren Chat:"))
        layout.addWidget(self.chat_display)
        layout.addWidget(QLabel("Type something:"))
        layout.addWidget(self.chat_input)
        layout.addWidget(send_btn)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "🧠 Agent")

    def handle_chat(self):
        user_input = self.chat_input.toPlainText().strip()
        if not user_input:
            return

        self.chat_display.append(f">> You: {user_input}")
        self.chat_input.clear()

        # Context memory lookup
        prior_context = self.memory.query_recent(user_input)

        # Generate reply
        reply = self.llm.respond(prior_context, "[gui_input]", user_input, "[emotion: unknown]")

        # Append to chat + speak it
        self.chat_display.append(f"<< {reply}")
        self.tts.say(reply)

        # Store interaction
        self.memory.store("[gui_input]", user_input, "[emotion: unknown]", reply)

        # Log memory and update memory tab
        self.memory_log.append(f">> {user_input}\n<< {reply}\n---")
        self.log_output.append(f"[LOG] Stored exchange: {user_input} → {reply}")

    # 👁 Vision
    def init_vision_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.cam_label = QLabel("Loading camera...")
        self.cam_label.setFixedHeight(300)
        self.cam_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.cam_label)

        self.scene_desc = QLabel("Scene: [none yet]")
        layout.addWidget(self.scene_desc)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "👁 Vision")

    def init_vision_timer(self):
        self.vision_timer = QTimer()
        self.vision_timer.timeout.connect(self.update_vision_tab)
        self.vision_timer.start(1000)  # update every 1 sec

    # 🎧 Audio
    def init_audio_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Mic status: Listening (placeholder)"))
        self.last_transcript = QTextEdit("Last transcript:\n\n")
        self.last_transcript.setReadOnly(True)
        layout.addWidget(self.last_transcript)
        layout.addWidget(QLabel("Detected mood: [calm]"))
        tab.setLayout(layout)
        self.tabs.addTab(tab, "🎧 Audio")

    # 🧵 Memory
    def init_memory_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Memory recall log (semantic search TBD)"))
        self.memory_log = QTextEdit()
        self.memory_log.setReadOnly(True)
        layout.addWidget(self.memory_log)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "🧵 Memory")

    # ⚙️ Settings
    def init_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select voice:"))
        self.voice_dropdown = QComboBox()
        self.voice_dropdown.addItems(["en_US-amy-low", "en_US-kyle-low", "en_GB-ryan-low"])
        layout.addWidget(self.voice_dropdown)

        layout.addWidget(QLabel("Select LLM Model:"))
        self.model_dropdown = QComboBox()
        self.model_dropdown.addItems(["phi-3-mini", "mistral-7b", "gpt4all"])
        layout.addWidget(self.model_dropdown)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "⚙️ Settings")

    # 📜 Logs
    def init_logs_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #111; color: #0f0;")
        layout.addWidget(self.log_output)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "📜 Logs")

    # External method to update logs
    def log(self, text):
        self.log_output.append(text)

def launch_gui():
    app = QApplication(sys.argv)
    window = FrenAgentGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()
