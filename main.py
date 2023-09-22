import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from database import Database
from vk_find_data import VkFindData

token = "vk1.a.sy-nvNdG8zquv3VFsGb1c3iFKAsej_S0euQ4EtVHhe0OMZUJwlkSe2Ip8PzXEqhMrMr71uu4NEFmREbAb2ttyTil0pMEibPW7bvEX63qCZJIF43isSlotABVTJEJbOalYQwKWyTck_NKGjPjSq8CZqC3hKXXZE3u2ZGAjz5hteVqlBR3cLScB48GMFXrjrf_fSlfD5GmIfo3zGE267XK5A"
token_owner = ""

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
vk_find = VkFindData(token=token_owner)
db = Database(db_login="", db_pass="", db_name="")

def write_msg(user_id, p_id, first_name, last_name, link, photo_id):
    params = {
        "user_id": user_id,
        "message": f"{first_name} {last_name}\n{link}",
        "attachment": f"photo{p_id}_{photo_id[0]},photo{p_id}_{photo_id[1]},photo{p_id}_{photo_id[2]}",
        "random_id": 0
    }
    vk.method("messages.send", params)
# def send_partner:
            #photo_ids = search_photo(take_partner)
            #write_msg(event.user_id, 1, "Павел", "Дуров", "https://vk.com/durov", photo_ids)
            #add_photo_links(photo_ids)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()

        if request == "start" and db.user_not_in_db(event.user_id):
            user_dict = vk_find.get_user_info(event.user_id)
            partners_list = vk_find.search_partners(user_dict['age'], user_dict['sex'], user_dict['city_id'])
            db.add_user_partners(event.user_id, user_dict, partners_list)
            # send_partner
        #elif request == "start" and user_id in BD:
            #write_msg('Вам уже нашли партнеров, наберите команду next')
        elif request == "next":
            pass
            #change_seen
            # if count(seen=0)>0:
            #send_partner
            # else:
                #for i in list(seen=1):
                      #change_seen
                #send_partner
        elif request == "like":
            pass
            #change_like
        elif request == "list":
            pass
            # write_msg('Список избранных')
            # for person in get_like_list:
                 #write_msg
