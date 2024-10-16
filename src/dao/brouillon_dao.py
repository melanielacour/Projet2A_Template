from db_connection import DBConnection
  
  
with DBConnection().connection as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT *                   "
            "FROM projet_2a.users;     "
        )
        res = cursor.fetchall()
print(res)


def add_user(self) -> bool:
        """
        Add an user to the database
        """
        created= False
