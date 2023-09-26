import configparser
from database import Database
from vk_find_data import VkFindData
from vk_chat_bot import VkChatBot

config = configparser.ConfigParser()
config.read("config.ini")

vk_chat = VkChatBot(config["Vk_group"]["token"])
vk_find = VkFindData(config["Vk_user"]["token"])
db = Database(config["Db"]["login"], config["Db"]["password"], config["Db"]["name"])

for event in vk_chat.longpoll.listen():

    if event.type == vk_chat.vkevent and event.to_me:
        request = event.text.lower()

        if request == "find":

            if not db.user_in_db(event.user_id):
                user_dict = vk_find.get_user_info(event.user_id)
                partners_list = vk_find.search_partners(user_dict['age'], user_dict['sex'], user_dict['city_id'])
                db.add_user_partners(event.user_id, user_dict, partners_list)
            else:
                p_dict = db.take_partner(event.user_id)
                db.change_seen(event.user_id, p_dict['id'])

            if db.all_seen(event.user_id):
                db.delete_seen(event.user_id)

            p_dict = db.take_partner(event.user_id)
            photo_ids = vk_find.search_photos(p_dict['id'])
            db.add_photo_id(p_dict['id'], photo_ids)
            vk_chat.write_partner(event.user_id, p_dict['id'], p_dict['first_name'], p_dict['last_name'],
                                  p_dict['link'], photo_ids)

        elif request == "like":
            if db.user_in_db(event.user_id):
                if db.change_like(event.user_id):
                    vk_chat.write_msg(event.user_id, "Выбранный человек уже в списке, выполните команду find или list", [])
                else:
                    p_dict = db.take_partner(event.user_id)
                    vk_chat.write_msg(event.user_id, f"{p_dict['first_name']} {p_dict['last_name']}"
                                                     f" добавлен(а) в список избранных", [])
            else:
                vk_chat.write_msg(event.user_id, "Для начала выполните команду find - выполните поиск человека", [])

        elif request == "list":
            if db.user_in_db(event.user_id):
                vk_chat.write_msg(event.user_id, "Список избранных:\n", db.get_like_list(event.user_id))
            else:
                vk_chat.write_msg(event.user_id, "Для начала выполните команду find - выполните поиск человека и добавьте "
                                                 "его в список избранных командой like", [])

        else:
            message = ("Список доступных команд:\n1. find - поиск человека.\n"
                       "2. like - добавить в список избранных.\n3. list - вывести список избранных.", [])
            vk_chat.send_keyboard(event.user_id, message)


