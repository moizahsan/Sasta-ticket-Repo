import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSON
from dsapi.extensions import db


class QuoteModel(db.Model):
    __tablename__ = 'quote'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('quote_collection.id'), nullable=True)
    # uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    quote_type = db.Column(db.String(10))
    flight_number = db.Column(db.String(10))
    premium = db.Column(db.Float(precision=5), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    param = db.Column(JSON, nullable=True)
    model_param = db.Column(JSON, nullable=True)

    # trailing_avg_order_qty = db.Column(db.Integer, nullable=True)
    # trail_weekly_tot_pax_count = db.Column(db.Integer, nullable=True)
    # order_qty = db.Column(db.Integer, nullable=True)
    # cncl_pax_count = db.Column(db.Integer, nullable=True)
    # cncl_amt = db.Column(db.Float(precision=5), nullable=True)
    # cncl_fc_pax_count = db.Column(db.Integer, nullable=True)
    # fc_pax_count = db.Column(db.Integer, nullable=True)
    # tot_pax_count = db.Column(db.Integer, nullable=True)
    # fc_exercise_rate = db.Column(db.Float(precision=5), nullable=True)
    # gen_cncl_rate = db.Column(db.Float(precision=5), nullable=True)
    # participation_rate = db.Column(db.Float(precision=5), nullable=True)
    # PTCFactor = db.Column(db.Float(precision=5), nullable=True)
    # cncl_charge = db.Column(db.Float(precision=5), nullable=True)
    # fc_participation_rate = db.Column(db.Float(precision=5), nullable=True)
    # romr = db.Column(db.Float(precision=5), nullable=True)
    # max_risk = db.Column(db.Float(precision=5), nullable=True)
    # fc_sales = db.Column(db.Float(precision=5), nullable=True)
    # ex_exercise_qty = db.Column(db.Float(precision=5), nullable=True)
    # tot_ex_cncl_charge = db.Column(db.Float(precision=5), nullable=True)
    # net_income = db.Column(db.Float(precision=5), nullable=True)
    # ex_premium_revenue = db.Column(db.Float(precision=5), nullable=True)


    def __repr__(self):
        return 'QuoteModel(id=%s, flight_number=%s,premium=%s)' % (self.id, self.flight_number, self.premium)

    def json(self):
        return {'id': self.id, 'price': self.flight_number, 'premium': self.premium}

    @classmethod
    def find_by_name(cls, name) -> "QuoteModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "QuoteModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
