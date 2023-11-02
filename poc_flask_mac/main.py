from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import database as db
import add_to_do as add
import csv
import io


app = Flask(__name__)

CORS(app)


# add todo
@app.route("/add", methods=["POST"])
def add_to_do():
    user_data = request.json
    title = user_data.get("title")
    description = user_data.get("description")
    completed = user_data.get("completed", False)

    # Ensure completed is a boolean value (True or False)
    if completed in [True, False]:
        # If completed is already a boolean, no change is needed
        pass
    elif completed.lower() == "true":
        completed = True
    elif completed.lower() == "false":
        completed = False
    else:
        # If it's neither a boolean nor a string representing a boolean, set it to False
        completed = False
    add.save_todo(title, description, completed)
    return "added", 201


# get all todo
@app.route("/")
def get_all_todo():
    connection = db.create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM public.todo ORDER BY id ASC;")
    all_todo = cursor.fetchall()
    formatted_data = [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "completed": row[3],
            "created_date": row[4],
        }
        for row in all_todo
    ]

    return jsonify(formatted_data)


# get all completed todo
@app.route("/completed")
def get_all_completed_todo():
    connection = db.create_db_connection()
    cursor = connection.cursor()
    cursor.execute("select * from public.todo  where completed = true ORDER BY id ASC;")
    all_todo = cursor.fetchall()
    formatted_data = [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "completed": row[3],
            "created_date": row[4],
        }
        for row in all_todo
    ]

    return jsonify(formatted_data)


# get all pending todo
@app.route("/pending")
def get_all_pending_todo():
    connection = db.create_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "select * from public.todo  where completed = false ORDER BY id ASC;"
    )
    all_todo = cursor.fetchall()
    formatted_data = [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "completed": row[3],
            "created_date": row[4],
        }
        for row in all_todo
    ]

    return jsonify(formatted_data)


# update a todo
@app.route("/update", methods=["PUT"])
def update_a_todo():
    connection = db.create_db_connection()
    cursor = connection.cursor()
    user_data = request.json
    id = user_data.get("id")
    title = user_data.get("title")
    description = user_data.get("description")
    completed = user_data.get("completed")

    cursor.execute("SELECT * FROM todo WHERE id = %s", (id,))
    todo = cursor.fetchone()

    if not todo:
        cursor.close()
        connection.close()
        return jsonify({"message": "Todo not found"}), 404

    new_title = title if title is not None else todo[1]
    new_description = description if description is not None else todo[2]
    new_completed = completed if completed is not None else todo[3]

    update_query = (
        """UPDATE todo SET title = %s, description = %s, completed = %s WHERE id = %s"""
    )
    cursor.execute(update_query, (new_title, new_description, new_completed, id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Todo updated"}), 200


# delete by id
@app.route("/deleted/<int:id>", methods=["DELETE"])
def deleteToDo(id):
    connection = db.create_db_connection()
    cursor = connection.cursor()

    delete_query = """DELETE FROM todo WHERE id = %s"""
    cursor.execute(delete_query, (id,))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Todo Deleted"})


# mark as done
@app.route("/done/<int:id>", methods=["PUT"])
def changeCompletedStatus(id):
    connection = db.create_db_connection()
    cursor = connection.cursor()

    update_query = """UPDATE public.todo SET completed = true WHERE id = %s;"""
    cursor.execute(update_query, (id,))
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"message": "Todo updated"})


# export as csv
@app.route("/export-csv")
def export_csv():
    connection = db.create_db_connection()
    cursor = connection.cursor()

    # Execute a SELECT query to retrieve all data from your table
    cursor.execute("SELECT * FROM public.todo")
    data = cursor.fetchall()

    # Define the response headers to specify a CSV content type
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "title", "description", "completed", "created_date"])

    for row in data:
        writer.writerow(row)

    response = Response(output.getvalue(), content_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=todo.csv"

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    return response


# upload a csv file
@app.route("/upload-csv", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        csv_file = request.files["csv_file"]
        if csv_file:
            try:
                # Read the uploaded CSV file in text mode
                csv_data = csv.reader(
                    csv_file.stream.read().decode("UTF-8").splitlines()
                )
                header = next(csv_data)  # Read the header row

                # Determine the index of each column based on the header
                title_index = header.index("title")
                description_index = header.index("description")
                completed_index = header.index("completed")

                # Connect to the database
                connection = db.create_db_connection()
                cursor = connection.cursor()

                for row in csv_data:
                    # Find values using header indices
                    title = row[title_index]
                    description = row[description_index]
                    completed = (
                        True if row[completed_index].lower() == "true" else False
                    )

                    insert_query = "INSERT INTO todo (title, description, completed) VALUES (%s, %s, %s);"
                    cursor.execute(insert_query, (title, description, completed))

                # Commit the changes and close the database connection
                connection.commit()
                cursor.close()
                connection.close()

                return "Data from CSV file has been saved to the database."

            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return "No CSV file was provided."


# find by title method
@app.route("/find/<value>", methods=["GET"])
def find_value(value):
    connection = db.create_db_connection()
    cursor = connection.cursor()

    search_query = (
        "SELECT * FROM public.todo WHERE title ILIKE %s OR description ILIKE %s;"
    )
    cursor.execute(search_query, ("%" + value + "%", "%" + value + "%"))

    result = cursor.fetchall()
    todo_list = [
        {"id": row[0], "title": row[1], "description": row[2], "completed": row[3]}
        for row in result
    ]

    cursor.close()
    connection.close()

    return jsonify(todo_list)


# main driver function
if __name__ == "__main__":
    app.run(debug=True)
