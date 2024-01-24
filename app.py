from flask import Flask, url_for, render_template, request, redirect, jsonify
from model.Iris import Iris
import database
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:po$tgreSQL@localhost:5432/dataPointsDB"
database.init_app(app)
migrate = Migrate(app, database.db)

@app.route('/')
def index():
    irises = database.get_all(Iris)
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
            database.add_row(iris)
            return redirect(url_for('index'))
        else:
            return render_template('400_error.html', form=validate), 400

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    iris = database.get_row(Iris, record_id)

    if iris:
        database.delete_row(iris)
        return redirect(url_for('index'))
    else:
        return render_template('404_error.html', form = {'title' : 'Record not found'}), 404

@app.route('/api/data', methods=['GET'])
def get_all_api():
    irises = database.get_all(Iris)

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
        database.add_row(iris)
        response = {
            'message': 'Added record',
            'id' : iris.id
        }
        return jsonify(response)
    else:
        return jsonify(validate), 400

@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def delete_api(record_id):
    iris = database.get_row(Iris, record_id)

    if iris is None:
        return jsonify({'title': 'Record not found'}), 404

    database.delete_row(iris)
    return jsonify({'deleted_record_id': record_id})

def validate_fields(sepal_length, sepal_width, petal_length, petal_width, iris_class):
    message_error = []
    if sepal_length < 0:
        return {'title' : 'Required sepal length type have value below 0'}
    if sepal_width < 0:
        return {'title' : 'Required sepal width type have value below 0'}
    if petal_length < 0:
        return {'title' : 'Required petal length type have value below 0'}
    if petal_width < 0:
        return {'title' : 'Required petal width type have value below 0'}
    if iris_class < 0 or iris_class > 3:
        return {'title' : 'Required iris class type have value not between 1-3'}

    return 1

if __name__ == '__main__':
    app.run(debug=True)