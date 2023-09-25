import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_table, User, Partner, User_partner


class Database():

    def __init__(self, login_db: str, pass_db: str, name_db: str):
        DSN = f'postgresql://{login_db}:{pass_db}@localhost:5432/{name_db}'
        self.engine = sqlalchemy.create_engine(DSN)
        create_table(engine=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def user_in_db(self, vk_id: int) -> bool:
        return (vk_id,) in self.session.query(User.vk_id).all()

    def add_user_partners(self, vk_id: int, data_user: dict, list_partners: list):
        u = User(vk_id=vk_id, first_name=data_user['first_name'], last_name=data_user['last_name'], \
                 age=data_user['age'], sex=data_user['sex'], city_id=data_user['city_id'])
        self.session.add(u)

        for partner in list_partners:
            if (partner['id'],) not in self.session.query(Partner.vk_id).all():
                p = Partner(vk_id=partner['id'], first_name=partner['first_name'], last_name=partner['last_name'], link=
                partner['link'])
                self.session.add(p)

            self.session.add(User_partner(user_id=vk_id, partner_id=partner['id'], seen=0, like=0))
            self.session.commit()

    def take_partner(self, vk_id: int) -> dict:
        data_partner = {}
        p = self.session.query(Partner.vk_id, Partner.first_name, Partner.last_name, Partner.link, Partner.photo_id). \
            join(User_partner).filter(User_partner.seen == 0, User_partner.user_id == vk_id).first()

        data_partner = {
            'first_name': p[1],
            'id': p[0],
            'last_name': p[2],
            'link': p[3],
            'photo_id': p[4]
        }
        return data_partner

    def change_seen(self, u_vk_id: int, p_vk_id: int):
        u_p_seen = self.session.query(User_partner).filter(User_partner.user_id == u_vk_id,
                                                           User_partner.partner_id == p_vk_id).first()
        u_p_seen.seen = 1
        self.session.commit()

    def change_like(self, u_vk_id: int, p_vk_id: int):
        u_p_like = self.session.query(User_partner).filter(User_partner.user_id == u_vk_id,
                                                           User_partner.partner_id == p_vk_id).first()
        u_p_like.like = 1
        self.session.commit()

    def add_photo_id(self, vk_id: int, list_photo_id: list):
        str_photo_id = ','.join(map(str, list_photo_id))
        self.session.query(Partner).filter(Partner.vk_id == vk_id).update({'photo_id': str_photo_id})
        self.session.commit()

    def get_like_list(self, vk_id: int) -> list:
        like_list = []
        for p in self.session.query(Partner.first_name, Partner.last_name, Partner.link).join(User_partner).filter(
                User_partner.user_id == vk_id, User_partner.like == 1).all():
            like_list.append({
                'first_name': p[0],
                'last_name': p[1],
                'link': p[2]
            })
        return like_list

    def delete_seen(self, vk_id: int):
        self.session.query(User_partner).filter(User_partner.user_id == vk_id).update({'seen': 0})
        self.session.commit()

    def all_seen(self, vk_id) -> bool:
        return self.session.query(User_partner).filter(User_partner.user_id == vk_id,
                                                       User_partner.seen == 0).count() == 0


if __name__ == '__main__':
    DB = Database('postgres', 'postgres', 'tinder_VK_db')
    user_1 = {'vk_id': 1, 'first_name': 'Павел', 'last_name': 'Дуров', 'age': 38, 'sex': 2, 'city_id': 2}
    partners_1 = [
        {
            'first_name': 'Мари',
            'id': 678399665,
            'last_name': 'Поль',
            'link': 'vk.com/id678399665'
        },
        {
            'first_name': 'Кристина',
            'id': 448627024,
            'last_name': 'Агилеровна',
            'link': 'vk.com/id448627024'
        },
        {
            'first_name': 'Елена',
            'id': 631399419,
            'last_name': 'Афанасьева',
            'link': 'vk.com/id631399419'
        }
    ]
    photo_id = [273199380, 305611130, 286300295]

    # print(DB.user_in_db(1))
    # DB.add_user_partners(1, user_1, partners_1)
    # print(DB.take_partner(1))
    # DB.change_seen(1, 678399665)
    # DB.change_like(1, 448627024)
    # DB.add_photo_id(631399419, photo_id)
    # print(DB.get_like_list(1))
    # DB.delete_seen(1)
    # print(DB.all_seen(1))

    DB.session.close()
