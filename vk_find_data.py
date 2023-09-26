import requests
from datetime import datetime


class VkFindData:
    def __init__(self, token) -> None:
        self.token = token
    
    def get_user_info(self, user_id: int=None) -> dict:
        URL = 'https://api.vk.com/method/users.get'

        params = {
            'user_id': user_id,
            'fields': 'bdate, sex, city',
            'access_token': self.token,
            'v': '5.131'
        }

        response = requests.get(URL, params=params)
        data = response.json()['response'][0]

        try:
            bdate = data['bdate']
        except KeyError:
            bdate = ''

        try:
            city_id = data['city']['id']
        except KeyError:
            city_id = None
        
        return {'first_name': data['first_name'], 
                'last_name': data['last_name'], 
                'age': self.bdate_to_age(bdate), 
                'sex': data['sex'], 
                'city_id': city_id}

    def search_partners(self, age: int, sex: int, city_id: int) -> list[dict]:
        partner_sex = 1 if sex == 2 else 2

        URL = 'https://api.vk.com/method/users.search'

        params = {
            'sex': partner_sex,
            'has_photo': 1,
            'count': 1000,
            'fields': 'bdate, city, sex, domain, is_friend',
            'access_token': self.token,
            'v': '5.131'
        }

        if age:
            age_from = int(0.75 * age)
            age_to = int(1.25 * age)
            params['age_from'] = age_from
            params['age_to'] = age_to

        if city_id:
            params['city'] = city_id

        response = requests.get(URL, params=params)
        data = response.json()['response']['items']

        partners_list = []
        for partner in data:
            if city_id:
                try:
                    if partner['city']['id'] == city_id and not partner['is_friend'] \
                        and not partner['is_closed']:

                        partners_list.append({
                            'id': partner['id'],
                            'first_name': partner['first_name'],
                            'last_name': partner['last_name'],
                            'link': f"vk.com/{partner['domain']}"
                        })
                        
                except KeyError:
                    continue
            else:
                if not partner['is_friend'] and not partner['is_closed']:
                    partners_list.append({
                            'id': partner['id'],
                            'first_name': partner['first_name'],
                            'last_name': partner['last_name'],
                            'link': f"vk.com/{partner['domain']}"
                        })

        return partners_list

    def search_photos(self, partner_id: int) -> list:
        URL = 'https://api.vk.com/method/photos.get'

        params = {
            'user_id': partner_id,
            'album_id': 'profile',
            'extended': 'likes',
            'access_token': self.token,
            'v': '5.131',
            'fields': 'bdate, sex, city'
        }

        response = requests.get(URL, params=params)
        data = response.json()['response']['items']

        likes_id = []
        for photo in data:
            likes_id.append((photo['likes']['count'], photo['id']))

        return [like_id[1] for like_id in sorted(likes_id, reverse=True)[:3]]

    def bdate_to_age(self, bdate: str) -> int:
        today = datetime.now()
        try:
            birth_date = datetime.strptime(bdate, '%d.%m.%Y')
            return (today - birth_date).days // 365
        except ValueError:
            return None