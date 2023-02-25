import sqlite3
import tkinter.messagebox as messageBox


class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS sales(
            "transaction_id" INTEGER PRIMARY KEY UNIQUE,
            "total_fee" text NOT NULL,
            "payment" text NOT NULL,
            "change" text NOT NULL
            )
        """
        self.cur.execute(sql)
        self.con.commit()

    # Insert Function
    def insert(self, transaction_id, total_fee, payment, change):
        self.cur.execute("insert into sales values (?,?,?,?)",
                         (transaction_id, total_fee, payment, change))
        self.con.commit()

    # Fetch All Data from DB
    def fetch(self):
        self.cur.execute("SELECT * FROM sales")
        rows = self.cur.fetchall()
        # print(rows)
        return rows

    # Delete a Record in DB
    def remove(self, transaction_id):
        self.cur.execute(
            "delete from sales where transaction_id=?", (transaction_id,))
        self.con.commit()

    def purge(self):
        self.cur.execute("DELETE FROM sales;",)
        str = f"We have deleted {self.cur.rowcount} records from the table."
        messageBox.showinfo("PURGED", str)

        self.con.commit()

    # Update a Record in DB
    def update(self, transaction_id, total_fee, payment, change):
        self.cur.execute(
            "update sales set total_fee=?, payment=?, change=? where transaction_id=?",
            (total_fee, payment, change, transaction_id))
        self.con.commit()

    def search(self, transaction_id, total_fee, payment, change):
        self.cur.execute(
            "SELECT * FROM sales WHERE transaction_id=?", (transaction_id))
        rows = self.cur.fetchall()
        self.con.commit()
        return rows
