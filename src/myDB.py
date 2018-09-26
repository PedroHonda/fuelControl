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


    def insertValues(self, tableName, data):
        """
Input:  tableName - table's name in which you want to insert the values
        data - dictionary containing the columns as keys associated to each column
            Example:
            data = {"date":"2018-09-25","mileage":11000,"pricePerLitre":4.40}

    Example of ISERT command:
    INSERT INTO Car(date, mileage, pricePerLitre, litreTotal) VALUES ('2018/09/16', 100000, 4.39, 40);
    In Python, it is suggested that you use:
        sql = 'INSERT INTO Car(date, mileage, pricePerLitre, litreTotal) VALUES (?,?,?,?)'
        cursor.execute(sql, ['2018/09/16', 100000, 4.39, 40])
        connection.commit()
        """
        values = []
        sqlINPUT = "INSERT INTO " + tableName + "("
        for d in data:
            sqlINPUT += d + ", "
            values.append(data[d])
        sqlINPUT = sqlINPUT[:-2] + ") VALUES ("
        for i in range(0,len(data)):
            sqlINPUT += "?,"
        sqlINPUT = sqlINPUT[:-1] + ")"
        self.cursor.execute(sqlINPUT, values)
        self.connection.commit()

    def getTables(self):
        '''
        Since sqlite3 does not support entries like ".dump" or ".tables", this function queries this database's schema to get table Names

        '''
        tables = []
        schema = self.selectCommand("select sql from sqlite_master where type = 'table';")
        for s in schema:
            if "CREATE" in s[0]:
                tables.append(s[0].split("TABLE")[1].split("(")[0].strip())
        return tables

    def selectCommand(self, cmd, condition=False):
        '''

    Example of SELECT command:
    SELECT rowID,* From Car WHERE date='2018-09-17';
        sql = 'SELECT rowID,* From Car WHERE date=?'
        cursor.execute(sql, '2018-09-17')
        return cursor.fetchall()
        '''
        self.sqlCommand(cmd, condition)
        return self.cursor.fetchall()
    
    def deleteTable(self, tableName):
        sqlDROP = "DROP TABLE " + tableName
        self.cursor.execute(sqlDROP)

    def sqlCommand(self, cmd, args=False):
        if args:
            self.cursor.execute(cmd, args)
        else:
            self.cursor.execute(cmd)
