import psycopg2

db_name = "usersListDB"
db_user = "newDB_user"
db_password = "nafizml"
db_host = "localhost"

def create_connection():
        connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_password,host=db_host)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        list_of_users = cursor.fetchall()
        cursor.close()
        connection.close()
        return list_of_users

list_of_users = create_connection()
print(list_of_users[1])
        