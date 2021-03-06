import sqlite3
from pathlib import Path


class InvalidPath(Exception):
    def __init__(self, path, message="Invalid path. Can't open database"):
        self.path = path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Invalid path. Can't create/open database with path {self.path}"

class EmptyValue(Exception):
    def __init__(self, message="Values are empty! Please give atleast one value. Use AllValues to read all values"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "Values are empty! Please give atleast one value. Use AllValues to read all values"

class InvalidType(Exception):
    def __init__(self, keyword, message="Wrong type!"):
        self.keyword = keyword
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Wrong type at keyword {self.keyword}"

class AllValues:
    """Used to select all values from a table"""
    def __init__(self):
        pass

class Database:
    """
    Main class of EliteD.\n
    Represents a SQLite Database
    """
    def __init__(self, path):
        self.path = path
        if Path(path).is_file() is False:
            raise InvalidPath(path)
        try:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
            self.connection.close()
        except:
            raise InvalidPath(path)

    def insert_value(self, table: str, values: tuple):
        """
        Insert values in the given table
        --------------
        Arguments:
        -table: The table to insert the values
        -values: The values to insert
        """
        if table.isspace():
            raise EmptyValue
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        execution = f"INSERT INTO {table} VALUES ("
        for value in values:
            if values.index(value) != 0:
                execution += ", "
            execution += "?"
        execution += ")"
        print(execution)
        try:
            cursor.execute(execution, values)
            connection.commit()
            connection.close()
        except Exception as e:
            connection.close()
            raise e


    def read_value(self, table: str, values: list, conditions: dict = {}):
        """
        Read a value of the given table
        --------------
        Arguments:
        -table: The table to read the values
        -values: The values to read. Use EliteD.AllValues() to read all values
        -conditions: The conditions which values should be edited. Should be like this: {"name of row": "value when to edit"}
        """
        if table.isspace():
            raise EmptyValue
        if len(values) == 0:
            raise EmptyValue
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        execution = f"SELECT "
        for value in values:
            if type(value) == AllValues:
                execution = "SELECT *"
                break
            elif type(value) != str:
                connection.close()
                raise InvalidType("values")
            if value != values[-1]:
                execution += f"{value}, "
            else:
                execution += value
        execution += f" FROM {table}"
        for condition in conditions:
            if list(conditions).index(condition) == 0:
                execution += f" WHERE {condition}={conditions[condition]}"
            else:
                execution += f"AND {condition}={conditions[condition]}"
        try:
            cursor.execute(execution)
        except Exception as error:
            connection.close()
            raise error
        else:
            data = cursor.fetchall()
            if len(data) == 1:
                for element in data:
                    data=element
            connection.close()
            return data

    def create_table(self, name: str, columns: list):
        """
        Create a table in a database. 
        If the inserted database doesn't exsist, it will be created automatically
        ------------------
        Arguments:
        -name: the name of the new table
        -columns: list with all columns of the database. Should look like this [{"type": int, "name": "name"}]
        Possible types are int and str
        """
        if len(columns) == 0:
            raise EmptyValue
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        types = {int: "INT", str: "TEXT"}
        execute_statement = f"CREATE TABLE {name} ("
        for column in columns:
            try:
                if column == columns[-1]:
                    execute_statement += f"{column['name']} {types[column['type']]}"
                else:
                    f"{column['name']} {column['type']}, "
            except:
                connection.close()
                raise InvalidType("columns")
        execute_statement += ")"
        try:
            cursor.execute(execute_statement)
            connection.commit()
            connection.close()
        except Exception as error:
            connection.rollback()
            connection.close()
            raise error

    def delete_table(self, name: str):
        """
        Deletes a table from the database
        -------------
        Arguments:
        -name: name of the table that should be deleted
        """
        if name.isspace():
            raise EmptyValue
        else:
            connection = sqlite3.connect(self.path)
            cursor = connection.cursor()
            try:
                cursor.execute(f"DROP TABLE {name}")
                connection.commit()
                connection.close()
            except Exception as error:
                connection.rollback()
                connection.close()
                raise error

    def update_value(self, table: str, row: str, new_value: str, conditions: dict = {}):
        """
        Update a value of the given table
        --------------
        Arguments:
        -table: The table to edit a value
        -row: The row to edit
        -new_value: The value to set as new value
        -conditions: The conditions which values should be edited. Should be like this: {"name of row": "value when to edit"}
        """
        if str(table).isspace() or str(row).isspace() or str(new_value).isspace():
            raise EmptyValue
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        execution = f"UPDATE {table} SET {row}={new_value}"
        for condition in conditions:
            if list(conditions).index(condition) == 0:
                execution += f" WHERE {condition}={conditions[condition]}"
            else:
                execution += f"AND {condition}={conditions[condition]}"
        try:
            cursor.execute(execution)
            connection.commit()
            connection.close()
        except Exception as error:
            connection.rollback()
            connection.close()
            raise error

    def delete_value(self, table: str, conditions: dict = {}):
        """
        Deletes all values from the given table that matches the conditions
        --------------
        Arguments:
        -table: The table to delete a value
        -conditions: The conditions which values should be deleted. Should be like this: {"name of row": "value when to edit"}
        """
        if str(table).isspace():
            raise EmptyValue
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        execution = f"DELETE FROM {table}"
        for condition in conditions:
            if list(conditions).index(condition) == 0:
                execution += f" WHERE {condition}={conditions[condition]}"
            else:
                execution += f"AND {condition}={conditions[condition]}"
        try:
            cursor.execute(execution)
            connection.commit()
            connection.close()
        except Exception as error:
            connection.rollback()
            connection.close()
            raise error


def create_database(name: str, path: str) -> Database:
    """
    Create a database.
    -------------------
    Arguments:
    -name: Name of the database
    -path: The path to the folder where the database should be created in
    """
    try:
        connection = sqlite3.connect(f"{path}/{name}")
        cursor = connection.cursor()
    except:
        connection.close()
        raise InvalidPath(f"{path}/{name}")
    else:
        connection.close()
        return Database(f"{path}/{name}")
    