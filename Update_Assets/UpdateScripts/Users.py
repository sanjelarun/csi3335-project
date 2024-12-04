# Create a "user" table that stores stats about the user

def createUsers(cursor):
    print("Creating User table...")

    sql = '''
        CREATE TABLE IF NOT EXISTS users (
            user_ID INT(12) AUTO_INCREMENT PRIMARY KEY,
            u_USER VARCHAR(64) NOT NULL,
            u_EMAIL VARCHAR(64) NOT NULL,
            u_PASSHASH VARCHAR(255) NOT NULL,
            u_ADMIN BOOLEAN NOT NULL,
            u_ACTIVE BOOLEAN NOT NULL
        );
        '''

    cursor.execute(sql)