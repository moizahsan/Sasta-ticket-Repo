from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from dsapi.api.schemas import QuoteCollectionSchema, QuoteCollectionSchemaV11
from dsapi.models import QuoteCollection
from dsapi.extensions import db
from dsapi.services.calculate_premium import calculate_multi_premiums


class QuoteCollectionResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - Quote Collection
      summary: Get a quote collection object
      description: Get a single quote collection object by ID which contains multiple quotes
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  data: QuoteCollectionSchema
                  success:
                    type: boolean
                    description: Boolean for successful or unsuccesful request
                  message:
                    type: string
                    description: Operation Successful / Unsuccesful
        404:
          description: quote collection does not exists

    """
    method_decorators = [jwt_required()]

    def get(self, id):
        schema = QuoteCollectionSchema()
        quotecollection = QuoteCollection.query.get_or_404(id)
        return {
            "data": schema.dump(quotecollection),
            "success": True,
            "message": "Operation Successful"
            }, 200


class QuoteCollectionCreateResource(Resource):
    """ Single object resource

    post:
      tags:
        - Quote Collection
      summary: Create a quote collection object
      description: Create a new quote collection object with multiple quotes
      requestBody:
        content:
          application/json:
            schema:
              QuoteCollectionSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    quote collection created
                  data: QuoteCollectionSchema
                  success:
                    type: boolean
                    description: Boolean for successful or unsuccesful request
                  message:
                    type: string
                    description: Operation Successful / Unsuccesful
    """
    method_decorators = [jwt_required()]

    def post(self):
        schema = QuoteCollectionSchema()
        quote_collection_schema = schema.load(request.json)
        quote_collection_obj = QuoteCollection(quote_type=quote_collection_schema['quote_type'])
        quote_collection_obj = calculate_multi_premiums(quote_collection_obj, quote_collection_schema, 1)

        return {
            "data": schema.dump(quote_collection_obj),
            "success": True,
            "message": "Operation Successful"
            }, 201


class QuoteCollectionResourceV11(Resource):
    """Single object resource

    ---
    get:
      tags:
        - Quote Collection
      summary: Get a quote collection object
      description: Get a single quote collection object by ID which contains multiple quotes
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  data: QuoteCollectionSchema
                  success:
                    type: boolean
                    description: Boolean for successful or unsuccesful request
                  message:
                    type: string
                    description: Operation Successful / Unsuccesful
        404:
          description: quote collection does not exists

    """
    method_decorators = [jwt_required()]

    def get(self, id):

        schema = QuoteCollectionSchemaV11()
        quotecollection = QuoteCollection.query.get_or_404(id)
        return {
            "data": schema.dump(quotecollection),
            "success": True,
            "message": "Operation Successful"
            }, 200


class QuoteCollectionCreateResourceV11(Resource):
    """ Single object resource

    post:
      tags:
        - Quote Collection
      summary: Create a quote collection object
      description: Create a new quote collection object with multiple quotes
      requestBody:
        content:
          application/json:
            schema:
              QuoteCollectionSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    quote collection created
                  data: QuoteCollectionSchema
                  success:
                    type: boolean
                    description: Boolean for successful or unsuccesful request
                  message:
                    type: string
                    description: Operation Successful / Unsuccesful
    """
    method_decorators = [jwt_required()]

    def post(self):

        schema = QuoteCollectionSchemaV11()
        quote_collection_schema = schema.load(request.json)
        quote_collection_obj = QuoteCollection(quote_type=quote_collection_schema['quote_type'])
        quote_collection_obj = calculate_multi_premiums(quote_collection_obj, quote_collection_schema)

        return {
            "data": schema.dump(quote_collection_obj),
            "success": True,
            "message": "Operation Successful"
            }, 201
