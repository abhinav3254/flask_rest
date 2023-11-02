import database as db

def save_todo(title,description,completed):
    connection = db.create_db_connection()
    cursor = connection.cursor()
    create_table_query = '''
            CREATE TABLE IF NOT EXISTS TODO (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        '''
    cursor.execute(create_table_query)

    insert_data_query = '''INSERT INTO TODO(title, description, completed)
    VALUES (%s, %s, %s)
    '''

    # Assuming you have the title, description, and completed values as variables
    cursor.execute(insert_data_query, (title, description, completed))

    connection.commit()
    cursor.close()
    connection.close()

    