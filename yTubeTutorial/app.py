from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'  #슬래쉬3개는 상대경로 4개는 절대경로
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #`SQLALCHEMY_TRACK_MODIFICATIONS`의 경우에는 추가적인 메모리를 필요로 하므로 꺼두는 것을 추천합니다




db = SQLAlchemy(app)

class Todo(db.Model):
    # id,content...등등이 모두 하나의 칼럼이된다
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST': #add Task버튼을눌러 post통신을 하게되면 'hello'페이지를 뿌려줌
        task_content = request.form['content'] #내가만든 content란 이름의 form을말한다 post통신중
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # 데이터생성기준으로 정렬해서 다가지고와라
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) #쿼리로 id를찾아보고 없으면 404에러
    
    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was a problem deleting that task'
          
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id) #여기서 id로 쿼리찾음

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating tour task'
    else:
        return render_template('update.html',task=task)



if __name__ == "__main__":
    app.run(debug = True) # 에러메세지를 팝으로 볼수있다