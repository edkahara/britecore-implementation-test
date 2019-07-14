from flask import Flask, Blueprint, render_template, request, redirect, jsonify
from .models import db, Request, Client, Product

fr = Blueprint("fr", __name__)


@fr.route("/")
def index():
    """
    Gets all feature requests, clients and products. Renders the index
    page with this data.
    """

    requests = Request.query.all()
    clients = Client.query.all()
    products = Product.query.all()
    return render_template(
        "index.html", requests=requests, clients=clients, products=products
    )


@fr.route("/<int:id>")
def get(id):
    """
    Gets a specific feature request. The data is then displayed
    depending on the modal. On the view modal, the title and description
    displayed. On the edit form modal, all the data is populated on the
    edit form, thereby allowing a user to edit a feature request.
    If the feature request doesn't exist, a 404 is
    returned.
    """

    feature_request = Request.query.get_or_404(id)

    return jsonify(
        id=feature_request.id,
        title=feature_request.title,
        description=feature_request.description,
        clientId=feature_request.clientId,
        priority=feature_request.priority,
        productId=feature_request.productId,
        targetDate=feature_request.targetDate
    )


@fr.route("/create", methods=["POST"])
def create():
    """
    Creates a new feature request. The data is received from the create
    request form and added to the request table.
    """

    title = request.form.get("title", None)
    description = request.form.get("description", None)
    clientId = request.form.get("clientId", None)
    priority = request.form.get("priority", None)
    productId = request.form.get("productId", None)
    targetDate = request.form.get("targetDate", None)

    if priority_taken_for_client_on_create(clientId, priority):
        reorder_priorities_for_client(clientId, priority)

    new_request = Request(
        title=title,
        description=description,
        clientId=clientId,
        priority=priority,
        productId=productId,
        targetDate=targetDate
    )

    db.session.add(new_request)
    db.session.commit()

    return redirect("/")


@fr.route("/update/<int:id>", methods=["POST"])
def update(id):
    """
    Updates a specific feature request. The feature request data is
    grabbed by its id through the /<int:id> route and populates the
    edit form.
    Upon submission of the form, the data is grabbed,
    checked against the current data and updates the database
    if changes are detected.
    """

    feature_request = Request.query.get_or_404(id)

    title = request.form.get("title", None)
    description = request.form.get("description", None)
    clientId = request.form.get("clientId", None)
    priority = request.form.get("priority", None)
    productId = request.form.get("productId", None)
    targetDate = request.form.get("targetDate", None)

    if priority_taken_for_client_on_update(id, clientId, priority):
        reorder_priorities_for_client(clientId, priority)

    if feature_request.title != title:
        feature_request.title = title

    if feature_request.description != description:
        feature_request.description = description

    if feature_request.clientId != clientId:
        feature_request.clientId = clientId

    if feature_request.priority != priority:
        feature_request.priority = priority

    if feature_request.productId != productId:
        feature_request.productId = productId

    if feature_request.targetDate != targetDate:
        feature_request.targetDate = targetDate

    db.session.commit()

    return redirect("/")


@fr.route("/delete/<int:id>")
def delete(id):
    """
    Deletes a specific feature request. The feature request is grabbed
    by id and deleted.
    If the feature request doesn't exist, a 404 is
    returned.
    """

    Request.query.get_or_404(id)

    Request.query.filter(Request.id == id).delete()
    db.session.commit()

    return redirect("/")


def priority_taken_for_client_on_create(client_id, new_priority):
    """
    Checks to see how many other feature requests for the same client
    have the same priority. If at least one does, the priorities for that
    client are re-ordered.
    """

    similar_priority_request = Request.query.filter(
        Request.clientId == client_id, Request.priority == new_priority
    ).count()
    return True if similar_priority_request else False


def priority_taken_for_client_on_update(id, client_id, new_priority):
    """
    Checks to see how many other feature requests for the same client
    have the same priority. If at least one does, the priorities for that
    client are re-ordered.
    """

    similar_priority_request = Request.query.filter(
        Request.id != id, Request.clientId == client_id,
        Request.priority == new_priority
    ).count()
    return True if similar_priority_request else False


def reorder_priorities_for_client(client_id, new_priority):
    """
    Re-orders priorities for a client. If a client's requests have
    priorities greater than or equal to those of the new or updated request,
    then those requests's priorities are incremented by 1.
    """

    Request.query.filter(
        Request.clientId == client_id, Request.priority >= new_priority
    ).update({
        Request.priority: Request.priority + 1
    })
