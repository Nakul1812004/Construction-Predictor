from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import requests
from PySide6.QtGui import QIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI-Based Price Prediction System")
        self.setGeometry(100, 100, 1200, 750)
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: white; font-family: Arial; }
            QFrame { background-color: #1e1e1e; border-radius: 10px; }
            QPushButton {
                background-color: #2e7dff;
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #5596ff; }
            QLineEdit {
                background-color: #2a2a2a;
                padding: 6px;
                border-radius: 6px;
            }
        """)

        main_layout = QHBoxLayout()

        # ================= LEFT PANEL =================
        left = QFrame()
        left.setFixedWidth(250)
        left_layout = QVBoxLayout()

        # ---------------- LOGO + TITLE ----------------
        logo_layout = QVBoxLayout()

        logo = QLabel()
        logo_pixmap = QPixmap("assets/logo.png")
        logo.setPixmap(logo_pixmap.scaled(250, 250, Qt.KeepAspectRatio))
        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("AI-Based \n"
                       "Price Prediction System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
            letter-spacing:1px;
        """)

        logo_layout.addWidget(logo)
        logo_layout.addWidget(title)

        self.area = QLineEdit()
        self.area.setPlaceholderText("In sqft")

        self.floors = QLineEdit()
        self.floors.setPlaceholderText("Integer Value")

        self.year = QLineEdit()
        self.year.setPlaceholderText("Starting Year")

        self.btn = QPushButton("Predict")
        self.btn.clicked.connect(self.predict)

        left_layout.addLayout(logo_layout)
        left_layout.addSpacing(20)
        left_layout.addWidget(QLabel("Plot Area"))
        left_layout.addWidget(self.area)
        left_layout.addWidget(QLabel("No. of Floors"))
        left_layout.addWidget(self.floors)
        left_layout.addWidget(QLabel("Construction Year"))
        left_layout.addWidget(self.year)
        left_layout.addSpacing(20)
        left_layout.addWidget(self.btn)
        left_layout.addStretch()

        left.setLayout(left_layout)

        # ================= RIGHT STACK =================
        self.right_stack = QStackedLayout()

        # -------- WELCOME SCREEN --------
        welcome = QWidget()
        wl = QVBoxLayout()

        logo = QLabel()
        logo.setPixmap(QPixmap("assets/logo.png").scaled(400,400, Qt.KeepAspectRatio))
        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome to AI-Based Price Prediction System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:20px; font-weight:bold;")

        desc = QLabel(
            "Plan your construction smartly using AI.\n"
            "Get cost estimation, best time to build, and detailed material insights instantly."

        )
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color:#bbbbbb;")

        wl.addStretch()
        wl.addWidget(logo)
        wl.addWidget(title)
        wl.addWidget(desc)
        wl.addStretch()

        welcome.setLayout(wl)

        # -------- OUTPUT SCREEN --------
        output = QWidget()
        output_layout = QVBoxLayout()

        # ===== KPI (TOP) =====
        kpi_layout = QHBoxLayout()

        self.cost = QLabel("₹ 0\nTotal Cost")
        self.month = QLabel("Best Month\n--")
        self.duration = QLabel("Duration\n--")

        for c in [self.cost, self.month, self.duration]:
            c.setAlignment(Qt.AlignCenter)
            c.setStyleSheet("""
                background:#2a2a2a;
                padding:20px;
                border-radius:10px;
                font-size:16px;
                font-weight:bold;
            """)
            kpi_layout.addWidget(c)

        output_layout.addLayout(kpi_layout)

        # ===== LOWER SECTION =====
        lower_layout = QHBoxLayout()

        # LEFT → GRAPH
        graph_layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        graph_layout.addWidget(self.canvas)

        # RIGHT → BREAKDOWN
        breakdown_panel = QFrame()
        breakdown_panel.setFixedWidth(300)

        bl = QVBoxLayout()

        title = QLabel("Cost Breakdown")
        title.setStyleSheet("font-size:16px; font-weight:bold;")

        self.breakdown_text = QLabel()
        self.breakdown_text.setAlignment(Qt.AlignTop)
        self.breakdown_text.setWordWrap(True)

        self.breakdown_text.setStyleSheet("""
            background:#2a2a2a;
            padding:10px;
            border-radius:8px;
            line-height:150%;
        """)

        bl.addWidget(title)
        bl.addWidget(self.breakdown_text)

        breakdown_panel.setLayout(bl)

        lower_layout.addLayout(graph_layout, 7)
        lower_layout.addWidget(breakdown_panel, 3)

        output_layout.addLayout(lower_layout)

        output.setLayout(output_layout)

        self.right_stack.addWidget(welcome)
        self.right_stack.addWidget(output)

        right_container = QFrame()
        right_container.setLayout(self.right_stack)

        main_layout.addWidget(left)
        main_layout.addWidget(right_container)

        self.setLayout(main_layout)

    # ================= FUNCTION =================
    def predict(self):
        try:
            res = requests.post(
                "http://127.0.0.1:8000/predict",
                json={
                    "area": float(self.area.text()),
                    "floors": int(self.floors.text()),
                    "year": int(self.year.text())
                }
            ).json()

            self.right_stack.setCurrentIndex(1)

            # KPI UPDATE
            self.cost.setText(f"Total Cost:\n\n₹ {res['total_cost']} L")
            self.month.setText(f"Best Month:\n\n{res['best_month']}")
            self.duration.setText(f"Duration:\n\n{res['duration']} Months\n")

            # BREAKDOWN TEXT
            text = f"""
======== MATERIAL REQUIRED ========

Cement      : {res['materials']['cement']} bags
Steel       : {res['materials']['steel']} kg
Sand        : {res['materials']['sand']} cft
Aggregate   : {res['materials']['aggregate']} cft
Bricks      : {res['materials']['brick']} units

======== COST BREAKDOWN ========

Civil:
   Material : ₹{res['civil']['material']}
   Labour   : ₹{res['civil']['labour']}
   Total    : ₹{res['civil']['total']}

Electrical:
   Material : ₹{res['electrical']['material']}
   Labour   : ₹{res['electrical']['labour']}
   Total    : ₹{res['electrical']['total']}

Plumbing:
   Material : ₹{res['plumbing']['material']}
   Labour   : ₹{res['plumbing']['labour']}
   Total    : ₹{res['plumbing']['total']}

Tiles:
   Material : ₹{res['tiles']['material']}
   Labour   : ₹{res['tiles']['labour']}
   Total    : ₹{res['tiles']['total']}

Paint:
   Material : ₹{res['paint']['material']}
   Labour   : ₹{res['paint']['labour']}
   Total    : ₹{res['paint']['total']}
"""
            self.breakdown_text.setText(text)

            # GRAPH
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            months = res["months"]
            costs = res["costs"]
            best = res["best_month"]

            ax.plot(months, costs, marker='o')

            if best in months:
                i = months.index(best)
                ax.scatter(months[i], costs[i], s=120)
                ax.annotate("Best", (months[i], costs[i]),
                            textcoords="offset points", xytext=(0,10), ha='center')

            ax.set_title("Cost vs Month")
            ax.set_xlabel("Month")
            ax.set_ylabel("Cost (Lakhs)")

            self.canvas.draw()

        except Exception as e:
            print("Error:", e)