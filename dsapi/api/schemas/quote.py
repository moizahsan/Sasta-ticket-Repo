from dsapi.extensions import ma, db
from dsapi.models import QuoteModel


class QuoteParamSchema(ma.Schema):
    adult_pax = ma.Integer(strict=True)
    child_pax =  ma.Integer(strict=True)


class QuoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuoteModel
        fields = ['id','premium', 'flight_number','created_at','updated_at']


class QuoteSchemaV11(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuoteModel
        fields = ['id','premium', 'flight_number','created_at','updated_at', 'param']

    param = ma.Nested(QuoteParamSchema, many=False, required=False)
