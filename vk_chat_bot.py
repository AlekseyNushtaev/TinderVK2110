import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard

class VkChatBot:
    def __init__(self, token: str) -> None:
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)
        self.vkevent = VkEventType.MESSAGE_NEW

    def write_partner(self, user_id: int, p_id: int, first_name: str, last_name: str, link: str, photo_ids: list) -> None:
        photo_str = ''
        for photo in photo_ids:
            photo_str += f'photo{p_id}_{photo},'
        params = {
            "user_id": user_id,
            "message": f"{first_name} {last_name}\n{link}",
            "attachment": photo_str,
            "random_id": 0
        }
        self.vk.method("messages.send", params)

    def write_msg(self, user_id: int, txt, like_list: list) -> None:
        text = txt
        for index, p in enumerate(like_list):
            text += f"{index + 1}. {p['first_name']} {p['last_name']}\n{p['link']}\n"
        params = {
            "user_id": user_id,
            "message": text,
            "random_id": 0
        }
        self.vk.method("messages.send", params)

    def send_keyboard(self, user_id, message) -> None:
        keyboard = VkKeyboard()
        keyboard.add_button('find')
        keyboard.add_button('like')
        keyboard.add_button('list')

        params = {
            "user_id": user_id,
            "message": message,
            "random_id": 0,
            "keyboard": keyboard.get_keyboard()
        }
        self.vk.method('messages.send', params)