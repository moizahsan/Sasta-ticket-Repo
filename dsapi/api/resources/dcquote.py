from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from dsapi.api.schemas import QuoteSchema, QuoteSchemaV11
from dsapi.models import QuoteModel
from dsapi.extensions import db
from dsapi.services.calculate_premium import calculate_premium


class DCQuoteResourceV11(Resource):
    """Single object resource

    ---
    get:
      tags:
        - DC Quote
      summary: Get a date change quotation object
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
          description: date change quotation does not exists

    """
    method_decorators = [jwt_required()]

    def get(self, id):
        schema = QuoteSchemaV11()
        dcquote = QuoteModel.query.get_or_404(id)
        return {
            "data": schema.dump(dcquote),
            "success": True,
            "message": "Operation Successful"
            }, 200



class DCQuoteCreateResourceV11(Resource):
    """ Single object resource

    post:
      tags:
        - DC Quote
      summary: Create a date change quotation object
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
        dcquote_schema = schema.load(request.json)
        dcquote_obj = QuoteModel(flight_number = request.json['flight_number'],
                                 quote_type='dc', param = request.json['param'])
        dcquote_obj = calculate_premium(dcquote_obj)

        return {
            "data": schema.dump(dcquote_obj),
            "success": True,
            "message": "Operation Successful"
            }, 201
