from flask import jsonify, request, make_response, abort
from service import app
from service.models import Account

@app.route("/health", methods=["GET"])
def health():
    """Health Status Endpoint"""
    return jsonify(status="OK"), 200

@app.route("/", methods=["GET"])
def index():
    """Root URL Index Page"""
    return app.send_static_file("index.html")

# ---------------------------------------------------------------------
# CREATE A NEW ACCOUNT
# ---------------------------------------------------------------------
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Creates a new Account record"""
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    return make_response(jsonify(account.serialize()), 201)

# ---------------------------------------------------------------------
# READ A SPECIFIC ACCOUNT
# ---------------------------------------------------------------------
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Reads a single Account by its unique ID"""
    app.logger.info("Request to read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with id [{account_id}] could not be found.")
    return make_response(jsonify(account.serialize()), 200)

# ---------------------------------------------------------------------
# LIST ALL ACCOUNTS
# ---------------------------------------------------------------------
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Lists all active Account records"""
    app.logger.info("Request to list all Accounts")
    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]
    return make_response(jsonify(account_list), 200)

# ---------------------------------------------------------------------
# UPDATE AN EXISTING ACCOUNT
# ---------------------------------------------------------------------
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Updates an existing Account record"""
    app.logger.info("Request to update an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with id [{account_id}] could not be found.")
    account.deserialize(request.get_json())
    account.update()
    return make_response(jsonify(account.serialize()), 200)

# ---------------------------------------------------------------------
# DELETE AN ACCOUNT
# ---------------------------------------------------------------------
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Deletes an Account record from the database"""
    app.logger.info("Request to delete an Account with id: %s", account_id)
    account = Account.find(account_id)
    if account:
        account.delete()
    return make_response("", 204)

def check_content_type(media_type):
    """Checks that the request media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(415, f"Content-Type must be {media_type}")
