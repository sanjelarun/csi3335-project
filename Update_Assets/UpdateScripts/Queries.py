# Create a "queries" table that stores stats about the user

def createQueries(cursor):
    print("Creating Queries table...")

    sql = '''
        CREATE TABLE IF NOT EXISTS queries (
            query_ID INT(12) AUTO_INCREMENT PRIMARY KEY,
            user_ID INT(12) NOT NULL,
            q_TEAM VARCHAR(255) NULL,
            q_YEAR INT(6) NULL,
            q_QUESTIONS VARCHAR(255) NULL,
            q_SOLUTIONS VARCHAR(255) NULL
        );
        '''

    cursor.execute(sql)