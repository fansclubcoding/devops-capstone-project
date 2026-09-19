"""
Account Service Routes

This microservice handles the lifecycle of Customer Accounts
"""
from flask import jsonify, request, make_response, abort
from service import app
from service.models import Account, db
from service.common import status


######################################################################
# Utility Functions
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if request.headers.get("Content-Type") != content_type:
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )


######################################################################
# Health Check Endpoint
######################################################################
@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify(status="OK"), status.HTTP_200_OK


######################################################################
# Index Endpoint
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return jsonify(
        name="Customer Account REST API Service",
        version="1.0",
        paths={
            "health": "/health",
            "accounts": "/accounts",
        },
    ), status.HTTP_200_OK


######################################################################
# Create an Account
######################################################################
@app.route("/accounts", methods=["POST"])
def create_account():
    """Creates a new Account"""
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    db.session.add(account)
    db.session.commit()
    message = account.serialize()
    location_url = f"/accounts/{account.id}"
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# List Accounts
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Lists all Accounts"""
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# Read an Account
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Reads an Account"""
    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id [{account_id}] could not be found.",
        )
    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# Update an Account
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Updates an Account"""
    check_content_type("application/json")
    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id [{account_id}] could not be found.",
        )
    account.deserialize(request.get_json())
    db.session.commit()
    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# Delete an Account
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Deletes an Account"""
    account = Account.find(account_id)
    if account:
        db.session.delete(account)
        db.session.commit()
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles 404 errors"""
    return (
        jsonify(
            status=status.HTTP_404_NOT_FOUND,
            error="Not Found",
            message=error.description,
        ),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def unsupported_media_type(error):
    """Handles 415 errors"""
    return (
        jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported Media Type",
            message=error.description,
        ),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )
