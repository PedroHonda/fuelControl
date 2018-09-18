# Script made to create the database for the API
import sqlite3

class myDB:

    def __init__(self, dbName):
        self.connection = sqlite3.connect(dbName)
        self.cursor = self.connection.cursor()
        self.tables = {}


    def createTable (self, tables):
        """
Input: table - dictionary with table's name and its parameter as list of tuples  with parameter type as option
    Example of table:
{
    'Car' : [
                {
                    'Name' : 'Column Name1',
                    'Type' : 'Column Type1'
                }        
            ],
            [
                {
                    'Name' : 'Column Name2',
                    'Type' : 'Column Type2'
                }
            ],
    'Cellphone' : [
                {
                    'Name' : 'Column Name1',
                    'Type' : 'Column Type1'
                }        
            ],
            [
                {
                    'Name' : 'Column Name2',
                    'Type' : 'Column Type2'
                }
            ],

}
    

    Example of CREATE command:
    CREATE TABLE Car (date DATE, mileage INTEGER, pricePerLitre REAL, litreTotal INTEGER, payTotal REAL, fuelType VARCHAR(20), mileageDiff INTEGER, efficiency REAL, pricePerKm REAL, comments);
        """
        for tableName in tables:
            sqlCREATE = "CREATE TABLE " + tableName + " ("
            for column in tables[tableName]:
                sqlCREATE += column['Name'] + " " + column['Type'] + ","
            sqlCREATE = sqlCREATE[:-1] + ');'
            self.cursor.execute(sqlCREATE)


    def insertValues(self, tableName, columns, values):
        """
Input:  tableName - table's name in which you want to insert the values
        columns - tuple containing the column's names
        values - tuple containing the values associated to each column
            NOTE: column and values must have the same length

    Example of ISERT command:
    INSERT INTO Car(date, mileage, pricePerLitre, litreTotal) VALUES ('2018/09/16', 100000, 4.39, 40);
    In Python, it is suggested that you use:
        sql = 'INSERT INTO Car(date, mileage, pricePerLitre, litreTotal) VALUES (?,?,?,?)'
        cursor.execute(sql, ['2018/09/16', 100000, 4.39, 40])
        connection.commit()
        """
        if len(columns) != len(values):
            return 'Error!\n\tColumns and Values inputs should have the same number of elements'
        sqlINPUT = "INSERT INTO " + tableName + "("
        for column in columns:
            sqlINPUT += column + ", "
        sqlINPUT = sqlINPUT[:-2] + ") VALUES ("
        for i in (0,len(values)):
            sqlINPUT += "?,"
        sqlINPUT = sqlINPUT[:-1] + ")"
        self.cursor.execute(sqlINPUT, values)
        self.connection.commit()

    def selectCommands(self, cmd, condition=False):
        '''

    Example of SELECT command:
    SELECT rowID,* From Car WHERE date='2018-09-17';
        sql = 'SELECT rowID,* From Car WHERE date=?'
        cursor.execute(sql, '2018-09-17')
        return cursor.fetchall()
        '''
        self.sqlCommand(cmd, condition)
        return self.cursor.fetchall()

    def sqlCommand(self, cmd, condition=False):
        if condition:
            self.cursor.execute(cmd, condition)
        else:
            self.cursor.execute(cmd)
