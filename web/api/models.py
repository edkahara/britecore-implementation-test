from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Product(db.Model):
    """
    Product model. Defines columns and relationships for the product table.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    requests = db.relationship("Request", backref='product', lazy=True)

    def __repr__(self):
        return f"<Request(name='{self.name}')>"


class Client(db.Model):
    """
    Client model. Defines columns and relationships for the client table.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    requests = db.relationship(
        "Request", backref='client', order_by="Request.priority", lazy=True
    )

    def __repr__(self):
        return f"<Request(name='{self.name}')>"


class Request(db.Model):
    """
    Client model. Defines columns and relationships for the request table.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    clientId = db.Column(db.Integer, db.ForeignKey("client.id"))
    priority = db.Column(db.Integer)
    productId = db.Column(db.Integer, db.ForeignKey("product.id"))
    targetDate = db.Column(db.Date)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"<Request(\
            title='{self.title}',client='{self.clientId}',priority='{self.priority}'\
        )>"
