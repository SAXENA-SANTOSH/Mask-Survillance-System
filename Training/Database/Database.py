
import sys
import mysql.connector

class Database:

    def __init__(self, host, user, password, logger):
        try:
            self.logger = logger
            self.host = host
            self.user = user
            self.password = password
        
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in initialization")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))

        
    def create_database(self, database_name):
        try:
            self.logger.add_in_logs("chk","Creating database method initialized")
            self.db = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password
                )
            if(self.db):
                self.logger.add_in_logs("inf","connection done successfully")
            else:
                self.logger.add_in_logs("inf","connectoion failed")
                raise("Connection failed")
            cursor = self.db.cursor(buffered=True)
            cursor.execute("show databases")

            db_already_exists = False
            for i in cursor:
                if(i[0] == database_name):
                    db_already_exists = True
                else:
                    continue
            
            if( not db_already_exists):
                self.logger.add_in_logs("inf","Database does not exists")
                self.logger.add_in_logs("inf","Creating a new database")
                cursor.execute("create database " + str(database_name))
            else:
                self.logger.add_in_logs("inf","Database exists")
                self.logger.add_in_logs("inf","Using same database")
        
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in initialization")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
    
    def connect_database(self, database_name):
        try:
            self.logger.add_in_logs("inf","connecting to the database")
            self.db = mysql.connector.connect(
                      host = self.host, 
                      user = self.user,
                      password = self.password,
                      database = database_name, 
            )
            if(self.db):
                self.logger.add_in_logs("inf","connection successfull")
            else:
                self.logger.add_in_logs("inf","connection failed")
                raise("connection failed")

            return self.db.cursor(buffered=True)
        
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in initialization")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
    
    def create_table(self, mycursor ,table_name , columns , columns_type , num , features = [], primary_key = [], foreign_key = [], reference = []):
        """
        This is a function to generate a query for creating a table

        Input : basic inputs to generate queries
        Output : Table in database

        """
                
        try:
            if(columns == [] or columns_type == [] and mycursor == ""):
                raise("ERR","attributes are missing")
            else:
                string = "create table if not exists " + table_name + "("
                for i,j,k in zip(columns, columns_type, num):
                    if(j == "float"):
                        k = ""
                    else:
                        k = "("+str(k) +")"
                    string = string + i+" "+j  + str(k) 
                    if(features != []):
                        string = string + features.pop(0) + ","
                    else:
                        string = string + ","
                if(primary_key != []):
                    string = string + "primary key(" + primary_key.pop(0) + ")," 
                for i,j in zip(foreign_key, reference):
                    string = string + "foreign key (" + i + ") " + "references " + j+","
                string = string[0:len(string) - 1]
                string = string + ")"
                mycursor.execute(string)
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in create table")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))


    def insert_into_table(self, mycursor,table_name=[], values=[]):
        """
        This is a function to generate a query for insertion of observation into database table 

        Input : observations to add in database
        Output : observation in a database table
        """
        
        try:
            if(table_name == [] or values == []):
                raise("parameters of table are missing")
            else:
                string = "insert into "+table_name 
                mycursor.execute("desc " + table_name)
                string = string + "("
                for i in mycursor:
                    string = string + i[0] +","
                string = string[0: len(string) - 1]
                string = string + ")"
                string = string + " values("
                for i in values:
                    if(type(i) == str):
                        string = string + "'"
                        string = string + "{}".format(i)
                        string = string + "',"
                    else:
                        string = string + "{}".format(i)
                        string = string + ","
            string = string[0:len(string)-1]
            string = string + ")"
            mycursor.execute(string)
        except Exception as e:
            self.logger.add_in_logs("ERR" , "database in insert into table")
            self.logger.add_in_logs("LIN" , "Error on line number : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.add_in_logs("TYP" , str(e))
    