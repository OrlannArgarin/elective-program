import sqlite3


class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS sales(
            "transaction_id" text NOT NULL,
            "total_fee" text NOT NULL,
            "payment" text NOT NULL,
            "change" text NOT NULL,
            PRIMARY KEY ("transaction_id")
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
        self.cur.execute("SELECT * from sales")
        rows = self.cur.fetchall()
        # print(rows)
        return rows

    # Delete a Record in DB
    def remove(self, transaction_id):
        self.cur.execute(
            "delete from sales where transaction_id=?", (transaction_id))
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

    # def filterYearLevel(self):
    #     self.cur.execute(
    #         "select year_level_id, COUNT(year_level_id) from studentreg GROUP BY year_level_id")
    #     rows = self.cur.fetchall()
    #     # print(rows)
    #     return rows

    # def filterSports(self):
    #     self.cur.execute(
    #         "select sports_id, COUNT(sports_id) from studentreg GROUP BY sports_id")
    #     rows = self.cur.fetchall()
    #     # print(rows)
    #     return rows

    # def filterSex(self):
    #     self.cur.execute(
    #         "select sex_id, COUNT(sex_id) from studentreg GROUP BY sex_id")
    #     rows = self.cur.fetchall()
    #     # print(rows)
    #     return rows

# "sex_id" text NOT NULL,
#             "year_level_id" text NOT NULL,
#             "sports_id" text,
#             PRIMARY KEY ("student_number"),
#             FOREIGN KEY ("sex_id") REFERENCES "sex_table" ("sex") ON DELETE RESTRICT ON UPDATE RESTRICT,
#             FOREIGN KEY ("year_level_id") REFERENCES "year_level_table" ("year_level") ON DELETE RESTRICT ON UPDATE RESTRICT,
#             FOREIGN KEY ("sports_id") REFERENCES "sports_table" ("sports") ON DELETE RESTRICT ON UPDATE RESTRICT
