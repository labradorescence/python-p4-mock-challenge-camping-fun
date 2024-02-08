from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship("Signup",
                              cascade="all, delete",
                              back_populates="activity"
                            )

    # Add serialization rules
    serialize_rules = ("-signups.activity", )

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship("Signup", 
                              back_populates="camper",
                              cascade="all, delete")
   
    # Add serialization rules
    serialize_rules = ("-signups.camper", )

    # Add validation
    @validates('name', 'age')
    def validate_attribute(self, key, value):
        print( f' checking {key} validation ')
        if key == 'name':
            if not value or len(value) < 1:
                raise ValueError("Camper must have a name")
            return value 
        if key == 'age':
            if not 8 <= value <= 18:
                raise ValueError("Age must be between 8 and 18")
            return value


    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    # Add relationships
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))

    activity = db.relationship("Activity",
                               back_populates="signups")
    camper = db.relationship("Camper",
                             back_populates="signups")
   
    # Add serialization rules
    serialize_rules = ("-activity.signups", "-camper.signups", )
   
    # Add validation
    @validates('time')
    def validate_time(self, key, time):
        if not 0 <= time <=23:
            raise ValueError("time must be between 0 and 23--- :D")
        return time

    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.