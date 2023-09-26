import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_db import create_table, User, Partner, User_partner

class Database():
    '''Класс для взаимодействия с базой данных'''

    def __init__(self, login_db: str, pass_db: str, name_db: str):
        '''Метод для инициализации класса Database (создание подключение к БД, открытие сессии)'''
        DSN = f'postgresql://{login_db}:{pass_db}@localhost:5432/{name_db}'
        self.engine = sqlalchemy.create_engine(DSN)
        create_table(engine=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def user_in_db(self, vk_id: int) -> bool:
        """Метод проверяет наличие пользователя в базе данных"""
        return (vk_id,) in self.session.query(User.vk_id).all()

    def add_user_partners(self, vk_id: int, data_user: dict, list_partners: list):
        """Метод добавляет нового пользователя и его партнеров"""
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
        """Метод позволяет получить данные о партнере"""
        p = self.session.query(Partner).join(User_partner).\
            filter(User_partner.seen == 0, User_partner.user_id == vk_id).order_by(User_partner.id).first()

        data_partner = {
            'first_name': p.first_name,
            'id': p.vk_id,
            'last_name': p.last_name,
            'link': p.link,
            'photo_id': p.photo_id
        }
        return data_partner

    def change_seen(self, u_vk_id: int, p_vk_id: int):
        """Метод меняет значение seen"""
        u_p_seen = self.session.query(User_partner).filter(User_partner.user_id == u_vk_id,
                                                           User_partner.partner_id == p_vk_id).first()
        u_p_seen.seen = 1
        self.session.commit()

    def change_like(self, u_vk_id: int) -> bool:
        """Метод меняет значение like"""
        u_p_like = self.session.query(User_partner).filter(User_partner.user_id == u_vk_id,
                                                           User_partner.seen == 0).order_by(User_partner.id).first()
        if u_p_like.like == 1:
            return True
        u_p_like.like = 1
        self.session.commit()
        return False

    def add_photo_id(self, vk_id: int, list_photo_id: list):
        """Метод добавляет id фото партнера"""
        str_photo_id = ','.join(map(str, list_photo_id))
        self.session.query(Partner).filter(Partner.vk_id == vk_id).update({'photo_id': str_photo_id})
        self.session.commit()

    def get_like_list(self, vk_id: int) -> list:
        """Метод возвращает список понравившихся партнеров"""
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
        """Метод обнуляет значение переменной seen"""
        self.session.query(User_partner).filter(User_partner.user_id == vk_id).update({'seen': 0})
        self.session.commit()

    def all_seen(self, vk_id) -> bool:
        """Метод проверяет наличие переменной seen с нулевым значением"""
        return self.session.query(User_partner).filter(User_partner.user_id == vk_id,
                                                       User_partner.seen == 0).count() == 0
