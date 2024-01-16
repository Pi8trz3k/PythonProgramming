from flask import Flask, url_for, render_template, request, redirect, jsonify
from flask_wtf import FlaskForm, CSRFProtect
from werkzeug.exceptions import BadRequest
from wtforms import Form, FloatField, validators, IntegerField
from wtforms.csrf.session import SessionCSRF
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:po$tgreSQL@localhost:5432/dataPointsDB"
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# csrf = CSRFProtect(app)

class Iris(db.Model):
    __tablename__ = 'irises'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    iris_class = db.Column(db.Integer, nullable=False)

    def __init__(self, sepal_length, sepal_width, petal_length, petal_width, iris_class):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.iris_class = iris_class

    def __str__(self):
        return (f"sepal_length {self.sepal_length}, sepal_width: {self.sepal_width}, petal_length: {self.petal_length},"
                f" petal_width: {self.petal_width}, iris_class: {self.iris_class}")

# class DataPointForm(FlaskForm):
#     sepal_length = FloatField('sepal_length', [validators.InputRequired()])
#     sepal_width = FloatField('sepal_width', [validators.InputRequired()])
#     petal_length = FloatField('petal_length', [validators.InputRequired()])
#     petal_width = FloatField('petal_width', [validators.InputRequired()])
#     iris_class = IntegerField('iris_class', [validators.InputRequired(), validators.NumberRange(1,3)])

@app.route('/')
def index():
    irises  = Iris.query.all()
    return render_template('index.html', irises=irises)

@app.route('/add', methods = ['GET','POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        try:
            sepal_length = float(request.form['sepal_length'])
            sepal_width = float(request.form['sepal_width'])
            petal_length = float(request.form['petal_length'])
            petal_width = float(request.form['petal_width'])
            iris_class = int(request.form['iris_class'])
        except ValueError:
            return render_template('400_error.html', form={'title' : 'Value Error - bad value entered into form'}), 400

        validate = validate_fields(sepal_length, sepal_width, petal_length, petal_width, iris_class)
        if validate == 1:
            iris = Iris(sepal_length, sepal_width, petal_length, petal_width, iris_class)
            db.session.add(iris)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('400_error.html', form=validate), 400

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    iris = db.session.get(Iris, record_id)

    if iris:
        db.session.delete(iris)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('404_error.html', form = {'title' : 'Record not found'}), 404

@app.route('/api/data', methods=['GET'])
def get_all_api():
    irises = db.session.query(Iris).all()

    result_json = []

    for iris in irises:
        result_json.append(
            {
                "id": iris.id,
                "sepal_length": iris.sepal_length,
                "sepal_width": iris.sepal_width,
                "petal_length": iris.petal_length,
                "petal_width": iris.petal_width,
                "iris_class": iris.iris_class,
            }
        )

    return jsonify(result_json)

@app.route('/api/data', methods=['POST'])
def add_new_iris_api():
    form = request.json

    sepal_length = form['sepal_length']
    sepal_width = form['sepal_width']
    petal_length = form['petal_length']
    petal_width = form['petal_width']
    iris_class = form['iris_class']

    validate = validate_fields(sepal_length, sepal_width, petal_length, petal_width, iris_class)

    if validate == 1:
        iris = Iris(sepal_length, sepal_width, petal_length, petal_width, iris_class)
        db.session.add(iris)
        db.session.commit()
        response = {
            'message': 'Added record id',
            'id' : iris.id
        }
        return jsonify(response)
    else:
        return jsonify(validate), 400


@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def delete_api(record_id):
    iris = db.session.get(Iris, record_id)

    if iris is None:
        return jsonify({'title': 'Record not found'}), 404

    db.session.delete(iris)
    db.session.commit()
    return jsonify({'deleted_record_id': record_id})

def validate_fields(sepal_length, sepal_width, petal_length, petal_width, iris_class):
    message_error = []
    if sepal_length < 0:
        # message_error.append({'title' : 'Required float type have value below 0'})
        # return message_error
        return {'title' : 'Required sepal length type have value below 0'}
    if sepal_width < 0:
        # message_error.append({'title' : 'Required float type have value below 0'})
        # return message_error
        return {'title' : 'Required sepal width type have value below 0'}
    if petal_length < 0:
        # message_error.append({'title' : 'Required float type have value below 0'})
        # return message_error
        return {'title' : 'Required petal length type have value below 0'}
    if petal_width < 0:
        # message_error.append({'title' : 'Required float type have value below 0'})
        # return message_error
        return {'title' : 'Required petal width type have value below 0'}
    if iris_class < 0 or iris_class > 3:
        # message_error.append({'title' : 'Required int type have value not between 1-3'})
        # return message_error
        return {'title' : 'Required iris class type have value not between 1-3'}

    return 1

if __name__ == '__main__':
    app.run(debug=True)