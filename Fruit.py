from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class add(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        fruit_content = request.form['content']
        new_fruit = add(content=fruit_content)

        try:
            db.session.add(new_fruit)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an an error."
    else:
        fruits = add.query.order_by(add.date_created).all()
        return render_template('index.html', fruits=fruits)

@app.route('/delete/<int:id>')
def delete(id):
    fruit_to_delete = add.query.get_or_404(id)

    try:
        db.session.delete(fruit_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error"


if __name__ == "__main__":
    app.run(debug=True)