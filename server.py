from flask import Flask, url_for, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:arne@localhost/CYR_DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


ma = Marshmallow(app)

class PitchTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spin = db.Column(db.String(6), unique=False)
    trajectorie = db.Column(db.String(6), unique=False)
    success = db.Column(db.Boolean, unique=False)

    def __init__(self, spin, trajectorie, success):
        self.spin = spin
        self.trajectorie = trajectorie
        self.success = success

    def __repr__(self):
        return '<PitchTask>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club = db.Column(db.String(20), unique=False)
    shape = db.Column(db.String(20), unique=False)
    type = db.Column(db.String(10), unique=False)
    success = db.Column(db.Boolean, unique=False)


    def __init__(self, club, shape, type, success):
        self.club = club
        self.shape = shape
        self.type = type
        self.success = success

    def __repr__(self):
        return '<Task>'

class TaskSchema(ma.Schema): #datentypen, beziehungen zwischen elementen, formale beschreibung einer struktur
  class Meta:
    fields = ('id', 'club', 'shape', 'type', 'success')

#class PitchTaskSchema(ma.Schema):
#    class Meta:
  #      fields: ('id', 'spin', 'trajectorie', 'success')

# Init schema
#pitch_task_schma = PitchTaskSchema()
#pitch_tasks_schema = PitchTaskSchema(many=True)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# DECORATOR
@app.route("/")
def index():
    return '<a href=' + url_for("hello", name="Hans") + '>Lass dich grüßen</a>'

@app.route("/hello/<string:name>")
def hello(name):
    return "Hello " + name + "!"

@app.route("/todb", methods=['POST'])
def post_task():
    print(request.get_json())
    club = request.json['club']
    shape = request.json['shape']
    type = request.json['type']
    success = request.json['success']


    new_task = Task(club, shape, type, success)

    db.session.add(new_task)
    db.session.commit()

    return  task_schema.jsonify(new_task)

@app.route("/post_pitch", methods=['POST'])
def post_pitch_task():
    print(request.get_json())
    spin = request.json['spin']
    trajectorie = request.json['trajectorie']
    type = request.json['type']
    success = request.json['success']


    new_pitch_task = PitchTask(club, spin, trajectorie,type, success)

    db.session.add(new_PitchTask)
    db.session.commit()

    return  task_schema.jsonify(new_PitchTask)

@app.route("/test", methods=['POST'])
def test():
    print("Taskrequest received")
    return

if __name__ == '__main__':
    app.run(port=1337, debug=True)