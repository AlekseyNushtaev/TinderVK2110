import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    vk_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=60))
    age = sq.Column(sq.Integer)
    sex = sq.Column(sq.SMALLINT, nullable=False)
    city_id = sq.Column(sq.Integer)


class Partner(Base):
    __tablename__ = "partner"

    vk_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=60))
    link = sq.Column(sq.String, nullable=False)
    photo_id = sq.Column(sq.String)


class User_partner(Base):
    __tablename__ = "user_partner"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("user.vk_id"), nullable=False)
    partner_id = sq.Column(sq.Integer, sq.ForeignKey("partner.vk_id"), nullable=False)
    seen = sq.Column(sq.SMALLINT, nullable=False)
    like = sq.Column(sq.SMALLINT, nullable=False)

    user = relationship(User, backref="user_partner")
    partner = relationship(Partner, backref="user_partner")


def create_table(engine):
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)