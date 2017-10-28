from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(120)) 
    completed = db.Column(db.Boolean)

    def __init__(self, name, body):
        self.name = name
        self.body = body
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    

    
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('blog.html',title="Build a Blog!", 
         completed_tasks=completed_tasks)


@app.route('/newpost', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        task_name = request.form['title']
        task_body = request.form['body']
        if task_name and task_body: 
            new_task = Task(task_name, task_body)
            db.session.add(new_task)
            db.session.commit()
            return render_template('postdetail.html',task_name=task_name,task_body=task_body)
        else:
            error = " We need both a name and body"    
            return render_template('newpost.html', error=error)
    else:

        return render_template('newpost.html')


if __name__ == '__main__':
    app.run()