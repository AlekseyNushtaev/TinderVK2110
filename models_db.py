import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    user_id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    age = sq.Column(sq.Integer)
    sex = sq.Column(sq.Integer)
    city = sq.Column(sq.String(length=40))

class Partner(Base):
    __tablename__ = 'partner'

    partner_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    link = sq.Column(sq.String(length=200), nullable=False)
    photo_id = sq.Column(sq.String(length=100))

class User_partner(Base):
    __tablename__ = 'user_partner'

    user_partner_id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)
    partner_id = sq.Column(sq.Integer, sq.ForeignKey('partner.partner_id'), nullable=False)
    seen = sq.Column(sq.Integer)
    like = sq.Column(sq.Integer)

    user = relationship(User, backref='user_partner')
    partner = relationship(Partner, backref='user_partner')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
