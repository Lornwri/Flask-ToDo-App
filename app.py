from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import flask_sqlalchemy
from datetime import datetime

# Create a new Flask
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define ToDo Model Class (models a to do list item that is stored in the database)
# Defines the columns (attributes) for the class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    done = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)


    # Add the repr method
    # A special method that returns a string representing the object
    def __repr__(self):
        return f'<todo id="{self.id}" title="{self.title}" done="{self.done}" created_at="{self.created_at}">'


# Create the database and table to hold the "To Do"s
with app.app_context():
    db.create_all()

# Create a home route that displays the To Do list
@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

# Create a route for adding a new To Do item to the database
@app.route('/add', methods=['POST'])
def add():

    # Get the title of the to do item from the HTML form on the web page
    title = request.form.get('title')

    # If the title IS NOT NULL, then create a new To Do List item record in the database
    # Else redirect the user to the index page (home page)
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

# Create a route for marking a To Do List item as done
@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    # Update the database record and mark the To Do List item as done 
    # If something goes wrong and the To Do List item doesn't exist, display a 404 error
    todo = Todo.query.get_or_404(todo_id)
    # Mark the To Do list item as done in the database
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))

# Create a route to delete the To Do item
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # Check if a database record exists with the id number
    # and if there is no matching record, show a 404 error
    todo = Todo.query.get_or_404(todo_id)
    # Delete the record in the database for the Todo item
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# Start the Flask app in debug mode
# Flask provides a debugger that shows a stack trace if an error occurs
# Debug mode reloads the page automatically
# Do not need to restart server when making changes to the code
if __name__ == '__main__':
    app.run(debug=True)