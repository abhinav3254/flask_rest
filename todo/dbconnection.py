import mysql.connector

# Establish connection to MySQL database
mydb = mysql.connector.connect(
    host="localhost", user="root", password="root3254", database="flask"
)

# Create a cursor to interact with the database
mycursor = mydb.cursor()

# Create a 'todos' table (run this only once)
mycursor.execute(
    """
    CREATE TABLE IF NOT EXISTS todos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT FALSE,
        due_date DATE
    )
"""
)


# method to add a Todo to the database
def add_todo_to_db(todo):
    sql = "INSERT INTO todos (title, description, completed, due_date) VALUES (%s, %s, %s, %s)"
    val = (todo.title, todo.description, todo.completed, todo.due_date)
    mycursor.execute(sql, val)
    mydb.commit()


# method to fetch all Todos from the database
def get_todos_from_db():
    mycursor.execute("SELECT * FROM todos")
    todos = mycursor.fetchall()
    return todos


def update_todo_by_id(todo_id, updated_todo):
    sql = "UPDATE todos SET title = %s, description = %s, completed = %s, due_date = %s WHERE id = %s"
    val = (
        updated_todo.title,
        updated_todo.description,
        updated_todo.completed,
        updated_todo.due_date,
        todo_id,
    )
    mycursor.execute(sql, val)
    mydb.commit()


def delete_todo_by_id(todo_id):
    sql = "DELETE FROM todos WHERE id = %s"
    val = (todo_id,)
    mycursor.execute(sql, val)
    mydb.commit()
