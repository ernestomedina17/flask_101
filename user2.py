import sqlite3


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # Tuple, with single item requires a comma
        row = result.fetchone()
        if row:
            user = cls(*row)
            # user = cls(row[0], row[1], row[2])  # long version of above
        else:
            user = None

        connection.close()
        return user
