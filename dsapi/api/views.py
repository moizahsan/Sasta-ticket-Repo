import time

from dsapi.util import log_api_hit
from flask import Blueprint, current_app, jsonify, g
from flask_restful import Api
from marshmallow import ValidationError

from dsapi.api.resources import (
    FCQuoteResource,
    FCQuoteCreateResource,
    QuoteCollectionResource,
    QuoteCollectionCreateResource,
    FCQuoteResourceV11,
    FCQuoteCreateResourceV11,
    QuoteCollectionResourceV11,
    QuoteCollectionCreateResourceV11,
    DCQuoteResourceV11,
    DCQuoteCreateResourceV11,
)
from dsapi.api.schemas import QuoteSchema, QuoteCollectionSchema
from dsapi.extensions import apispec

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

blueprintv11 = Blueprint("api_v11", __name__, url_prefix="/api/v1.1")
apiv11 = Api(blueprintv11)

# api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
# api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(
    QuoteCollectionResource, "/fc/quotes/<int:id>", endpoint="quote_collection_by_id"
)
api.add_resource(
    QuoteCollectionCreateResource, "/fc/quotes", endpoint="create_quote_collection"
)
api.add_resource(FCQuoteResource, "/fc/<int:id>", endpoint="fcquote_by_id")
api.add_resource(FCQuoteCreateResource, "/fc", endpoint="create_fcquote")

apiv11.add_resource(
    QuoteCollectionResourceV11,
    "/fc/quotes/<int:id>",
    endpoint="quote_fc_collection_by_id_v11",
)
apiv11.add_resource(
    QuoteCollectionCreateResourceV11,
    "/fc/quotes",
    endpoint="create_fc_quote_collection_v11",
)

apiv11.add_resource(FCQuoteResourceV11, "/fc/<int:id>", endpoint="fcquote_by_id_v11")
apiv11.add_resource(FCQuoteCreateResourceV11, "/fc", endpoint="create_fcquote_v11")
apiv11.add_resource(DCQuoteResourceV11, "/dc/<int:id>", endpoint="dcquote_by_id_v11")
apiv11.add_resource(DCQuoteCreateResourceV11, "/dc", endpoint="create_dcquote_v11")

@blueprint.before_app_first_request
def register_views():
    # apispec.spec.components.schema("UserSchema", schema=UserSchema)
    # apispec.spec.path(view=UserResource, app=current_app)
    # apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.components.schema(
        "QuoteCollectionSchema", schema=QuoteCollectionSchema
    )
    apispec.spec.components.schema("QuoteSchema", schema=QuoteSchema)
    apispec.spec.path(view=QuoteCollectionCreateResource, app=current_app)
    apispec.spec.path(view=QuoteCollectionResource, app=current_app)
    apispec.spec.path(view=FCQuoteResource, app=current_app)
    apispec.spec.path(view=FCQuoteCreateResource, app=current_app)


@blueprintv11.before_app_first_request
def register_views_v11():
    apispec.spec.path(view=QuoteCollectionCreateResourceV11, app=current_app)
    apispec.spec.path(view=QuoteCollectionResourceV11, app=current_app)
    apispec.spec.path(view=FCQuoteResourceV11, app=current_app)
    apispec.spec.path(view=FCQuoteCreateResourceV11, app=current_app)
    apispec.spec.path(view=DCQuoteResourceV11, app=current_app)
    apispec.spec.path(view=DCQuoteCreateResourceV11, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400


@blueprintv11.errorhandler(ValidationError)
def handle_marshmallow_error_v11(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400


@blueprint.before_request
@blueprintv11.before_request
def start_timer():
    g.start = time.time()


@blueprint.after_request
@blueprintv11.after_request
def log_request(response):
    log_api_hit(response)
    return response
