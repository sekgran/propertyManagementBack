import enum

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy import Enum
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)
app.app_context().push()


class EnumPropertyType(enum.Enum):
    residential = 'Residential'
    commercial = 'Commercial'


class EnumPropertyStatus(enum.Enum):
    occupied = 'Occupied'
    vacant = 'Vacant'


class EnumTenantRentalPaymentStatus(enum.Enum):
    pending = 'Pending'
    paid = 'Paid'


class EnumMaintenanceStatus(enum.Enum):
    pending = 'Pending'
    in_progress = 'In Progress'
    completed = 'Completed'


class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Integer)

    def json(self):
        return {
            'id': self.id,
            'address': self.address,
            'type': self.type,
            'status': self.status,
            'purchase_date': self.purchase_date,
            'price': self.price
        }


class Tenant(db.Model):
    __tablename__ = 'tenants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact_info = db.Column(db.String, nullable=False)
    lease_term_start = db.Column(db.Date, nullable=False)
    lease_term_end = db.Column(db.Date, nullable=False)
    rental_payment_status = db.Column(Enum(EnumTenantRentalPaymentStatus))
    property_id = db.Column(db.ForeignKey("properties.id"))

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_info': self.contact_info,
            'lease_term_start': self.lease_term_start,
            'lease_term_end': self.lease_term_end,
            'rental_payment_status': self.rental_payment_status,
            'property_id': self.property_id
        }


class Maintenance(db.Model):
    __tablename__ = 'maintenance'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    maintenance_status = db.Column(Enum(EnumMaintenanceStatus))
    schedule_date = db.Column(db.Date, nullable=False)
    property_id = db.Column(db.ForeignKey("properties.id"))

    def json(self):
        return {
            'id': self.id,
            'description': self.description,
            'maintenance_status': self.maintenance_status,
            'schedule_date': self.schedule_date,
            'property_id': self.property_id
        }


db.create_all()


#create a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# create a user
@app.route('/properties', methods=['POST'])
def create_property():
    print("COUCOU", flush=True)
    try:
        print("COUCOU 2", flush=True)
        data = request.get_json()
        new_property = Property(
            address=data['address'],
            type=data['type'],
            status=data['status'],
            purchase_date=data['purchase_date'],
            price=data['price']
        )
        print(data, flush=True)
        db.session.add(new_property)
        db.session.commit()
        return make_response(jsonify({'message': 'Property created'}), 201)
    except:
        return make_response(jsonify({'message': 'Error on creating Property'}), 500)


# get all users
@app.route('/properties', methods=['GET'])
def get_properties():
    try:
        properties = Property.query.all()
        return make_response(jsonify([property.json() for property in properties]), 200)
    except:
        return make_response(jsonify({'message': 'Error getting Properties'}), 500)
