import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy


database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Job
Have information for the job, such as
contact information and job specs.
'''
class Job(db.Model):  
    __tablename__ = 'Jobs'

    id = Column(db.Integer, primary_key=True)
    contact_name = Column(db.String)
    contact_phone = Column(db.String)
    address = Column(db.String)
    material = Column(db.String)
    status = Column(db.String)
    sinks = Column(db.ARRAY(db.Integer))
  
    def __init__(self, contact_name, contact_phone, address, material, sinks):
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.address = address
        self.material = material
        self.sinks = sinks


    def format(self):
        return {
        'id': self.id,
        'contact_name': self.contact_name,
        'contact_phone': self.contact_phone,
        'address': self.address,
        'material': self.material,
        'status': self.status}
    
'''
Inventory
Keep track of how many sinks we have left.
'''
class Inventory(db.Model):
    __tablename__ = "Inventory"

    id = Column(db.Integer, primary_key=True)
    sink_id = db.ForeignKey('Sinks.id')
    count = Column(db.String)

    def __init__(self, sink_id, count):
        self.sink_id = sink_id
        self.count = count


    def remove_one(self):
        self.count = self.count - 1

    def remove_multiple(self, count):
        self.count = self.count - count

    def format(self):
        return {
            'id' : self.id,
            'sink_id' : self.sink_id,
            'count' : self.count
        }


'''
Sink
'''
class Sink(db.Model):
    __tablename__ = 'Sinks'

    id = Column(db.Integer, primary_key=True)
    description = Column(db.String)

    def __init__(self, description):
        self.description = description

    def format(self):
        return {
            'id' : self.id,
            'description' : self.description
        }