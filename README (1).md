
# Personal finance app

The **Personal Finance Management Application** is a simple desktop app built with **Python**, **PyQt6**, **SQLite**, and **Matplotlib**.  
It allows users to **track income and expenses**, **visualize financial data** with a pie chart, and manage their monthly budgets easily.


## Features

- **Secure user registration and login** (passwords hidden with dots)  
- **Add income and expense transactions**  
- **Dashboard** showing:
  - Total income  
  - Total expense  
  - Balance  
  - Pie chart of income vs expense  
- **View all transactions** in a table  
- **Persistent storage** using SQLite database (`fin.db`)



## Database Information
The app uses **SQLite** and automatically creates a database file named **`fin.db`** in the project folder.Alternatively, you can use 'sample db.py' (if provided) to create the database manually:
     **`sample db.py`**
## Installation

1. Download Code:
   Download the project as a ZIP file from GitHub or clone the repository to your local machine using:
   git clone https://github.com/<USERNAME>/personal-finance-app.git
   Then navigate to the project folder:
   cd personal-finance-app

2. Dependencies:
   Ensure Python 3.10+ is installed on your machine.
   Install required libraries using pip:
   pip install PyQt6 matplotlib

3. Required Libraries:

   **sys** - Provides access to system-specific functions and used here to exit the application gracefully.

   **sqlite3** - Lightweight, file-based database and used to store users and transaction records persistently.

   **datetime** - Module to handle date and time; used to store transaction dates and generate monthly summaries.

    **PyQt6** - Python library for creating desktop GUI applications; used to design windows, buttons, tabs, and forms.


   **PyQt6.QtWidgets** - Contains GUI elements like windows, labels, buttons, tabs, and tables, used to build the desktop interface.

   **PyQt6.QtCore** - Provides core non-GUI functionality such as alignment, signals, and constants used in GUI elements.
   
   **Matplotlib** - Python library for data visualization, used to create pie charts showing income vs expense distribution.

   **matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg** - Allows embedding Matplotlib charts inside PyQt6 GUI windows.

   **matplotlib.figure.Figure** - Creates figure objects to draw charts, used here to plot pie charts for income vs expense visualization.

## Steps
1. Run the Application:
   - In the project folder, run the main application file:
     python finance_app.py
   - The login window will open.

2. Register or Login:
   - If you are a new user, register by creating a username and password.
   - Existing users can login with their credentials.
   - Passwords are hidden with dots for security.

3. Using the Application:
   - Dashboard Tab: Shows total income, total expense, balance, and a pie chart of income vs expenses.
   - Add Transaction Tab: Add income or expense transactions with amount, note, and type.
   - View Transactions Tab: See all your transactions in a table.