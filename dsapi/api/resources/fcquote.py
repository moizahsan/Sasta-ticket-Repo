from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from dsapi.api.schemas import QuoteSchema, QuoteSchemaV11
from dsapi.models import QuoteModel
from dsapi.extensions import db
from dsapi.services.calculate_premium import calculate_premium


class FCQuoteResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - FC Quote
      summary: Get a free cancellation quotation object
      description: Get a single free cancellation quotation by ID
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
                  data: QuoteSchema
                  success:
                    type: boolean
                    description: Boolean for successful or unsuccesful request
                  message:
                    type: string
                    description: Operation Successful / Unsuccesful
        404:
          description: free cancellation quotation does not exists

    """
    method_decorators = [jwt_required()]

    def get(self, id):
        schema = QuoteSchema()
        fcquote = QuoteModel.query.get_or_404(id)
        return {
            "data": schema.dump(fcquote),
            "success": True,
            "message": "Operation Successful"
            }, 200



class FCQuoteCreateResource(Resource):
    """ Single object resource

    post:
      tags:
        - FC Quote
      summary: Create a free cancellation quotation object
      description: Create a new free cancellation quotation object with premium
      requestBody:
        content:
          application/json:
            schema:
              QuoteSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    free cancellation quotation created
                  data: QuoteSchema
                  success:
                    type: boolean
                    description: Boolean for successful or unsuccesful request
                  message:
                    type: string
                    description: Operation Successful / Unsuccesful
    """
    method_decorators = [jwt_required()]

    def post(self):
        schema = QuoteSchema()
        fcquote_schema = schema.load(request.json)
        fcquote_obj = QuoteModel(flight_number = request.json['flight_number'],
                                 quote_type='fc')
        fcquote_obj = calculate_premium(fcquote_obj)

        return {
            "data": schema.dump(fcquote_obj),
            "success": True,
            "message": "Operation Successful"
            }, 201


class FCQuoteResourceV11(Resource):
    """Single object resource

    ---
    get:
      tags:
        - FC Quote
      summary: Get a free cancellation quotation object
      description: Get a single free cancellation quotation by ID
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
                  data: QuoteSchema
                  success:
                    type: boolean
                    description: Boolean for successful or unsuccesful request
                  message:
                    type: string
                    description: Operation Successful / Unsuccesful
        404:
          description: free cancellation quotation does not exists

    """
    method_decorators = [jwt_required()]

    def get(self, id):
        schema = QuoteSchemaV11()
        fcquote = QuoteModel.query.get_or_404(id)
        return {
            "data": schema.dump(fcquote),
            "success": True,
            "message": "Operation Successful"
            }, 200



class FCQuoteCreateResourceV11(Resource):
    """ Single object resource

    post:
      tags:
        - FC Quote
      summary: Create a free cancellation quotation object
      description: Create a new free cancellation quotation object with premium
      requestBody:
        content:
          application/json:
            schema:
              QuoteSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    free cancellation quotation created
                  data: QuoteSchema
                  success:
                    type: boolean
                    description: Boolean for successful or unsuccesful request
                  message:
                    type: string
                    description: Operation Successful / Unsuccesful
    """
    method_decorators = [jwt_required()]

    def post(self):
        schema = QuoteSchemaV11()
        fcquote_schema = schema.load(request.json)
        fcquote_obj = QuoteModel(flight_number = request.json['flight_number'],
                                 quote_type='fc', param = request.json['param'])
        fcquote_obj = calculate_premium(fcquote_obj)

        return {
            "data": schema.dump(fcquote_obj),
            "success": True,
            "message": "Operation Successful"
            }, 201
