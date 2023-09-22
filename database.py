import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_db import create_tables, User, Partner, User_partner

class Database:

    def __init__(self, db_login, db_pass, db_name):
        DSN = f"postgresql://{db_login}:{db_pass}@localhost:5432/{db_name}"
        self.engine = sqlalchemy.create_engine(DSN)
        create_tables(engine=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def user_not_in_db(self, user_id):
        return (user_id,) not in self.session.query(User.user_id).all()
    def add_user_partners(self, user_id, user_dict, partners_list):
        us = User(user_id=user_id, name=user_dict['first_name'], last_name=user_dict['last_name'], age=user_dict['age'], sex=user_dict['sex'], city=user_dict['city_id'])
        self.session.add(us)
        for p in partners_list:
            if (p['id'],) not in self.session.query(Partner.partner_id).all():
                p1 = Partner(partner_id=p['id'], name=p['first_name'], last_name=p['last_name'], link=p['link'])
                self.session.add(p1)
            u_p = User_partner(user_id=user_id, partner_id=p['id'], seen=0, like=0)
            self.session.add(u_p)
        self.session.commit()