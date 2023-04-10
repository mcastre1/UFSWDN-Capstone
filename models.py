import os
from flask_migrate import Migrate
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
    migrate = Migrate(app, db)


'''
Job
Have information for the job, such as
contact information and job specs.
'''
class Job(db.Model):  
    __tablename__ = 'Jobs'

    id = Column(db.Integer, primary_key=True)
    job_name = Column(db.String, nullable=False)
    contact_name = Column(db.String, nullable=False)
    contact_phone = Column(db.String, nullable=False)
    address = Column(db.String, nullable=False)
    material = Column(db.String)
    status = Column(db.String, nullable=False)
    edge_finish = Column(db.String)
    sinks = Column(db.ARRAY(db.Integer))
  
    def __init__(self, job_name, contact_name, contact_phone, address, material, status, edge_finish, sinks):
        self.job_name = job_name
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.address = address
        self.material = material
        self.sinks = sinks
        self.status = status
        self.edge_finish = edge_finish


    def format(self):
        return {
        'id': self.id,
        'job_name': self.job_name,
        'contact_name': self.contact_name,
        'contact_phone': self.contact_phone,
        'address': self.address,
        'material': self.material,
        'sinks': self.sinks,
        'status': self.status,
        'edge_finish': self.edge_finish}
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
'''
Inventory
Keep track of how many sinks we have left.
'''
class Inventory(db.Model):
    __tablename__ = "Inventory"

    id = Column(db.Integer, primary_key=True)
    sink_id = Column(db.Integer, db.ForeignKey('Sinks.id'))
    sink = db.relationship("Sink", backref="sink")
    count = Column(db.String)

    def __init__(self, sink_id, count):
        self.sink_id = sink_id
        self.count = count


    def remove_one(self):
        self.count = self.count - 1

    def remove_multiple(self, count):
        self.count = self.count - count

    def format(self):
        print(self.sink)
        return {
            'id' : self.id,
            'sink_id' : self.sink_id,
            'description' : self.sink.format()['description'],
            'count' : self.count
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


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

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
