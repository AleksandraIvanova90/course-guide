import time
from datetime import datetime

import requests


def get_user_id(token, i):
    if i.isdigit() == True:
        id = i
        return id
    else:
        url = 'https://api.vk.com/method/utils.resolveScreenName'
        params = {
            'access_token': token,
            'screen_name': i,
            'v': '5.131'
        }
        response = requests.get(url, params)
        res = response.json()['response']['object_id']
        return res

class VK:
    def __init__(self, token, m):
        self.token = token
        self.user_id = get_user_id(token, m)

    def common_params(self):
        return {
            'access_token': self.token,
            'v': '5.131'
        }

    def get_user_data(self):
        url = 'https://api.vk.com/method/photos.getAlbums'
        params = self.common_params()
        params.update({'owner_id': self.user_id})
        response = requests.get(url, params=params)
        return response.json()

    def get_list_album(self):
        user_albums = [{i: [j['title'], j['id']]} for i, j in enumerate(self.get_user_data()['response']['items'])]
        system_albums = [{len(user_albums): ['Фотографии со стены', 'wall']},
                         {(len(user_albums) + 1): ['Фотографии профиля', 'profile']},
                         {(len(user_albums) + 2): ['Сохраненные фотографии', 'saved']}]
        list_albums = user_albums + system_albums
        return list_albums

    def get_user_list_photo(self, number_album):
        URL = 'https://api.vk.com/method/photos.get'
        params = self.common_params()
        params.update({
            'owner_id': self.user_id,
            'album_id': self.get_album(number_album)[1],
            'extended': 1,
            'photo_sizes': 1
        })
        response = requests.get(URL, params=params)
        return response.json()
    def get_album(self, number_album):
        res = self.get_list_album()[number_album - 1][number_album - 1]
        return res
    def d_t(self):
        print (f'У Вас {len(self.get_list_album())} альбомов: ')
        for i in self.get_list_album():
                for j, k in i.items():
                    print(f'{j + 1}: {k[0]}')

    def request_quantity_photos(self, number_album):
        quantity = int(input(f"В альбоме {self.get_user_list_photo(number_album)['response']['count']} фотографий. Сколько фотографий необходимо загрузить? "))
        return quantity

    def get_data_to_upload(self, number_album):
        list_data = self.get_user_list_photo(number_album)
        list = list_data['response']['items'][:-(self.request_quantity_photos(number_album)+1):-1]
        unique_list = []
        data_list = []
        for j in list:
            photo = j['sizes'][-1]['url']
            type_size = j['sizes'][-1]['type']
            name_photos = j['likes']['count']
            unix_timestamp = float(j['date'])
            local_time = datetime.fromtimestamp(unix_timestamp)
            data_upload = local_time.strftime("%d.%m.%Y")
            if f'{name_photos}.jpg' in unique_list:
                unique_list.append(f'{name_photos}({data_upload}).jpg')
                data_list.append({'file_name': f'{name_photos}({data_upload}).jpg', 'url': photo, 'size': type_size})
            else:
                unique_list.append(f'{name_photos}.jpg')
                data_list.append({'file_name': f'{name_photos}.jpg', 'url': photo, 'size': type_size})
        data_to_upload = {self.get_album(number_album)[0]: data_list}
        return data_to_upload
