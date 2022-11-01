from dsapi.extensions import ma, db
from dsapi.models import QuoteCollection, QuoteModel
from dsapi.api.schemas.quote import QuoteSchema, QuoteSchemaV11


class QuoteCollectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuoteCollection
        fields = ['id','quote_type','fcquotes']

    fcquotes = ma.Nested(QuoteSchema, many=True)


class QuoteCollectionSchemaV11(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuoteCollection
        fields = ['id','quote_type','fcquotes']

    fcquotes = ma.Nested(QuoteSchemaV11, many=True)
