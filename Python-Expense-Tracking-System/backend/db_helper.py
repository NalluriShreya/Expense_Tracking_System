import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger("db_helper")

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Snal@190805",
        database="expense_manager"
    )

    if connection.is_connected():
        print("Connection successful")
    else:
        print("Failed in connecting to a database")
    cursor = connection.cursor(dictionary=True)

    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses where expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with {expense_date, amount, category, notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start_date: {start_date} and end_date: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute('''SELECT category, sum(amount) as Total FROM expenses 
                       WHERE expense_date BETWEEN %s and %s 
                       GROUP BY category''',
                       (start_date, end_date)
                       )
        data = cursor.fetchall()
        return data

def fetch_expense_summary_by_months():
    logger.info("fetch_expense_summary_by_months called")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT month(expense_date) AS Month, sum(amount) AS Expenses FROM expenses group by month(expense_date)")
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    # expenses = fetch_expenses_for_date("2024-08-25")
    # print(expenses)
    # insert_expense("2024-08-25", "40", "Food", "Eat ice-cream")
    # delete_expenses_for_date("2024-08-25")
    # data = fetch_expense_summary("2024-08-01", "2024-08-05")
    # print(data)
    data = fetch_expense_summary_by_months()
    print(data)