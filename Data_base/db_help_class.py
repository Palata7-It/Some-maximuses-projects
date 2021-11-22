import re
import sqlite3


class db_help:
    def __init__(self, db_name):
        """Method to init database"""

        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    def add_info(self, question, table='question', column='our_question'):
        """Method to add new question into our table"""

        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO '{table}'({column}) VALUES ({quest})".format(table=table, column=column,
                                                                                    quest=question))
        except:
            self.cursor.execute(
                "INSERT OR IGNORE INTO '{table}'({column}) VALUES ('{quest}')".format(table=table, column=column,
                                                                                      quest=question))

            self.conn.commit()

    def update(self):
        """Method to make new database with new questions"""

        try:
            self.cursor.execute("DROP TABLE answer")
        except:
            pass
        self.a = ''
        for i in self.cursor.execute("SELECT our_question FROM question").fetchall():
            for j in i:
                if self.a == '':
                    self.a = j + " CHAR(20)"
                else:
                    self.a += ", " + j + " CHAR(20)"
        prog = re.compile(r'\?|!|\.')
        self.b = prog.split(self.a)
        print(self.a)
        print(self.b)
        self.a = ''
        for i in self.b:
            self.a += i
        print(self.a)
        try:
            self.cursor.execute("CREATE TABLE answer ({})".format(self.a))
        except:
            self.cursor.execute("CREATE TABLE answer (Id)")
        self.conn.commit()

    def clear_questions(self):
        """Method to delete all questions from table questions"""

        self.cursor.execute("DELETE FROM 'question'")
        self.conn.commit()

    def take_an_answer(self):
        """Method to add answers to the table"""

        self.a = []
        self.answer = []
        self.column = ''
        for i in self.cursor.execute("SELECT our_question FROM question").fetchall():
            for j in i:
                self.a.append(j)
        for i in self.a:
            self.answer.append(input(i + ' '))
            self.column += i + ', '
        self.add_info(str(self.answer)[1:-1], 'answer', self.column[:-2])
        self.conn.commit()
        return str(self.answer)[1:-1], 'answer', self.column[:-2]

    def return_info(self, where, what='*'):
        """This method is counting percent of '+'"""

        return self.cursor.execute("SELECT {what} FROM {where}".format(what=what, where=where)).fetchall()

    def close(self):
        if (self.conn):
            self.conn.close()

    def add_info_full(self, question, table='question'):
        """Method to add new question into our table"""

        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO '{table}'  VALUES ({quest})".format(table=table, quest=question))
        except:
            self.cursor.execute(
                "INSERT OR IGNORE INTO '{table}' VALUES ('{quest}')".format(table=table, quest=question))
        self.conn.commit()
