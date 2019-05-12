from .models import Client, Product


def create_clients_and_products(db):
    """
    Adds clients to the client table and product areas to the product table
    if the data doesn't exist
    """

    if not Client.query.count():
        client_a = Client(name="Client A")
        client_b = Client(name="Client B")
        client_c = Client(name="Client C")

        db.session.add(client_a)
        db.session.add(client_b)
        db.session.add(client_c)

    if not Product.query.count():
        billing = Product(name="Billing")
        claims = Product(name="Claims")
        policies = Product(name="Policies")
        reports = Product(name="Reports")

        db.session.add(billing)
        db.session.add(claims)
        db.session.add(policies)
        db.session.add(reports)

    db.session.commit()
