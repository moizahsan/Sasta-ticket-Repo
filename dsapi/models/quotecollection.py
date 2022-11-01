import datetime

from dsapi.extensions import db


class QuoteCollection(db.Model):
    __tablename__ = 'quote_collection'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quote_type = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    fcquotes = db.relationship("QuoteModel")


    def __repr__(self):
        return 'QuoteCollection(id=%s, type=%s,fcquotes=%s)' % (self.id, self.type, self.fcquotes)

    def json(self):
        return {'id': self.id, 'type': self.type, 'fcquotes': self.fcquotes}

    @classmethod
    def find_by_name(cls, name) -> "QuoteCollection":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "QuoteCollection":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
