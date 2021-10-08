# EliteD
EliteD is a package to make database usage easier!
Create database easily and read and update them.


### Installing
To install the package you just need to execute the following in your command line:

    pip3 install EliteD


## Using the package
This is how you create and setup a Database
 ```py
 import EliteD #importing the package
database = EliteD.create_database("user.db", "/path/to/db")
database.create_table("test", [{"type": int, "name": "test"}]) 
```
The second line would create the database "user.db" at the given path
The last line creates the table "test" in the database with the column "test" with integer as values. You can add as many columns as you want

If you already have a database, you can open the database like this: 
```py
import EliteD #import the module
database = EliteD.Database("/path/to/db") #Opens the database
```
If you need to delete a created table, you can do it like this:
```py
import EliteD
database = EliteD.Database("/path/to/db")
database.delete_table("name of the table")
```

### Reading and changing values of a database
To read a value of a database, you can use the `read_value ` method:
```py
import EliteD
database = EliteD.Database("/path/to/db")
read = database.read_value(table="test", values=["test"], conditions={"test": 0})
```
`values` is the row you want to read from the table. You can give multiple values. To read out all values, you can use the `EliteD.AllValues()` class. Conditions can be specified when you only want to read out the values when a row (`test` in this case)  has the specified value (`0` in this case).
To change database values, you can use `update_value` method:
```py
import EliteD
database = EliteD.Database("/path/to/db")
database.update_value(table="test", row="roaw", new_value=2, conditions={"roawaaa": 1})
```
This would change every value of the row `roaw` from the table `test` to `2` if the value of `roawaaa` is `1`