import sys
import sqlite3
import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QFormLayout
)
from PyQt6.QtCore import Qt

#Import matplotlib for chart
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# DATABASE INITIALIZATION
def init_db():
    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        note TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()

# LOGIN / REGISTER WINDOW
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance App - Login")
        self.setGeometry(300, 200, 300, 180)
        
        layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")
        
        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)
        layout.addRow(self.login_btn, self.register_btn)
        self.setLayout(layout)

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        conn = sqlite3.connect("finance.db")
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            self.hide()
            self.main_window = MainWindow(user[0])
            self.main_window.show()
        else:
            self.setWindowTitle("Invalid login. Try again.")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        conn = sqlite3.connect("finance.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
            conn.commit()
            self.setWindowTitle("Registration successful! Login now.")
        except sqlite3.IntegrityError:
            self.setWindowTitle("Username already exists.")
        conn.close()

# MATPLOTLIB PIE CHART 
class PieChartCanvas(FigureCanvas):
    def __init__(self, income, expense):
        self.fig = Figure(figsize=(4, 3))
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.plot_chart(income, expense)

    def plot_chart(self, income, expense):
        labels = ['Income', 'Expense']
        values = [income, expense]

        # Avoid zero division error
        if income == 0 and expense == 0:
            self.ax.text(0.5, 0.5, 'No data yet', ha='center', va='center')
        else:
            self.ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['#6BD66B', '#FF6B6B'])
        self.ax.set_title("Income vs Expense")

# MAIN APPLICATION WINDOW
class MainWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Personal Finance Manager")
        self.setGeometry(250, 150, 700, 500)

        self.tabs = QTabWidget()
        self.dashboard_tab = QWidget()
        self.add_tab = QWidget()
        self.view_tab = QWidget()

        self.tabs.addTab(self.dashboard_tab, "🏠 Dashboard")
        self.tabs.addTab(self.add_tab, "➕ Add Transaction")
        self.tabs.addTab(self.view_tab, "📋 View Transactions")

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        self.setLayout(vbox)

        self.init_dashboard()
        self.init_add_tab()
        self.init_view_tab()

    # DASHBOARD TAB 
    def init_dashboard(self):
        self.dashboard_layout = QVBoxLayout()
        self.total_income_label = QLabel()
        self.total_expense_label = QLabel()
        self.dashboard_layout.addWidget(self.total_income_label)
        self.dashboard_layout.addWidget(self.total_expense_label)
        self.chart_canvas = None  
        self.dashboard_tab.setLayout(self.dashboard_layout)
        self.load_dashboard_data()

    def load_dashboard_data(self):
        conn = sqlite3.connect("finance.db")
        c = conn.cursor()
        current_month = datetime.date.today().strftime("%Y-%m")

        c.execute("SELECT SUM(amount) FROM transactions WHERE user_id=? AND type='income' AND date LIKE ?",
                  (self.user_id, f"{current_month}%"))
        income = c.fetchone()[0] or 0

        c.execute("SELECT SUM(amount) FROM transactions WHERE user_id=? AND type='expense' AND date LIKE ?",
                  (self.user_id, f"{current_month}%"))
        expense = c.fetchone()[0] or 0
        conn.close()

        self.total_income_label.setText(f"Total Income: ₹{income:.2f}")
        self.total_expense_label.setText(f"Total Expense: ₹{expense:.2f}")

        # Remove old chart if exists
        if self.chart_canvas:
            self.dashboard_layout.removeWidget(self.chart_canvas)
            self.chart_canvas.setParent(None)

        # Add new chart
        self.chart_canvas = PieChartCanvas(income, expense)
        self.dashboard_layout.addWidget(self.chart_canvas)

    
    # ADD TRANSACTION TAB
    def init_add_tab(self):
        layout = QFormLayout()
        self.type_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.note_input = QLineEdit()
        self.add_btn = QPushButton("Add Transaction")

        layout.addRow("Type (income/expense):", self.type_input)
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("Note:", self.note_input)
        layout.addWidget(self.add_btn)
        self.add_tab.setLayout(layout)

        self.add_btn.clicked.connect(self.add_transaction)

    def add_transaction(self):
        t_type = self.type_input.text().lower().strip()
        if t_type not in ['income', 'expense']:
            self.setWindowTitle("Type must be 'income' or 'expense'")
            return

        try:
            amount = float(self.amount_input.text())
        except ValueError:
            self.setWindowTitle("Enter valid amount")
            return

        note = self.note_input.text()
        date = datetime.date.today().strftime("%Y-%m-%d")

        conn = sqlite3.connect("finance.db")
        c = conn.cursor()
        c.execute("INSERT INTO transactions (user_id, type, amount, note, date) VALUES (?,?,?,?,?)",
                  (self.user_id, t_type, amount, note, date))
        conn.commit()
        conn.close()

        self.type_input.clear()
        self.amount_input.clear()
        self.note_input.clear()

        self.load_dashboard_data()

    # VIEW TRANSACTIONS TAB
    def init_view_tab(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.refresh_btn = QPushButton("Refresh")
        layout.addWidget(self.table)
        layout.addWidget(self.refresh_btn)
        self.view_tab.setLayout(layout)
        self.refresh_btn.clicked.connect(self.load_transactions)

    def load_transactions(self):
        conn = sqlite3.connect("finance.db")
        c = conn.cursor()
        c.execute("SELECT type, amount, note, date FROM transactions WHERE user_id=?", (self.user_id,))
        data = c.fetchall()
        conn.close()

        self.table.setRowCount(len(data))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Type", "Amount", "Note", "Date"])

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


# MAIN ENTRY POINT
if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
