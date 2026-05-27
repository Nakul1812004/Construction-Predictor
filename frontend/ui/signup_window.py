from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import requests
from PySide6.QtGui import QIcon

class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Signup")
        self.setGeometry(400, 150, 400, 500)
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: white; font-family: Arial; }
            QLineEdit {
                background:#1e1e1e;
                border:1px solid #333;
                padding:10px;
                border-radius:8px;
            }
            QPushButton {
                background:#2e7dff;
                padding:10px;
                border-radius:8px;
                font-weight:bold;
            }
            QPushButton:hover { background:#5596ff; }
        """)

        main_layout = QVBoxLayout()

        card = QFrame()
        card.setStyleSheet("background:#1e1e1e; border-radius:15px; padding:20px;")
        layout = QVBoxLayout()

        logo = QLabel()
        logo.setPixmap(QPixmap("assets/logo.png").scaled(150,150, Qt.KeepAspectRatio))
        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        subtitle = QLabel("Sign up to get started")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color:#aaa;")

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Password")
        self.passw.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Sign Up")
        btn.clicked.connect(self.signup)

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(logo)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(self.user)
        layout.addWidget(self.passw)
        layout.addSpacing(10)
        layout.addWidget(btn)
        layout.addWidget(self.label)

        card.setLayout(layout)

        main_layout.addStretch()
        main_layout.addWidget(card)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def signup(self):
        try:
            res = requests.post(
                "http://127.0.0.1:8000/signup",
                json={
                    "username": self.user.text().strip(),
                    "password": self.passw.text().strip()
                }
            )

            data = res.json()

            if res.status_code == 200:
                self.label.setText("✅ Account Created")
            else:
                self.label.setText(f"❌ {data.get('detail', 'Signup Failed')}")

        except Exception as e:
            self.label.setText(f"Error: {e}")