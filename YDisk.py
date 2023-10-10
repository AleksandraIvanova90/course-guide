import json

import data
import requests
from tqdm import tqdm


class Yandex:
    url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.token = token


    def common_headers(self):
        return {"Authorization": self.token}

    def checking_the_folder(self, data):
        params = {'path': f'{list(data.keys())[0]}'}
        response = requests.get(self.url, params=params, headers=self.common_headers())
        return response.status_code

    def folder(self, data):
        params = {'path': f'{list(data.keys())[0]}'}
        response = requests.put(self.url, params=params, headers=self.common_headers())
        return response.status_code

    def new_folder(self, data):
        list_uploaded_photos = []
        for i in tqdm(list(data.values())[0], desc='Загрузка фотографий на Яндекс.Диск'):
            size = list(i.values())[2]
            photo = list(i.values())[1]
            name = list(i.values())[0]
            self.update(data, name, photo)
            list_uploaded_photos.append({'file_name': name, 'size': size})
            pass
        with open('Uploaded photos.json', 'w') as file:
            json.dump(list_uploaded_photos, file, ensure_ascii=False, indent=4)


    def delete_a_folder(self, data):
        params = {'path': f'{list(data.keys())[0]}'}
        response = requests.delete(self.url, params=params, headers=self.common_headers())
        return response.status_code

    def update(self, data,  n, p):
        params = {'path': f'{list(data.keys())[0]}/{n}',
                  'url': p
                  }
        res = requests.post(f'{self.url}/upload', params=params, headers=self.common_headers())
        path_to_upload = res.json().get('href','')
        response = requests.put(path_to_upload)
        return response


    def auto_save_photos(self, data):
        if self.checking_the_folder(data) != 404:
            if self.delete_a_folder(data) != 423:
                while self.delete_a_folder(data) == 202:
                    self.delete_a_folder(data)
                else:
                    if self.delete_a_folder(data) == 423:
                        print('Код 423. Технические работы. Попробуйте запустить программу еще раз.')
                    else:
                        self.folder(data)
                        self.new_folder(data)
            else:
                print('Код 423. Технические работы. Попробуйте запустить программу еще раз.')
        else:
            self.folder(data)
            self.new_folder(data)
