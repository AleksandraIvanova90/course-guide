import configparser
from VK import VK
from YDisk import Yandex


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    token_VK = config.get('VK', 'user_token')
    user_info_VK = config.get('VK', 'user_id_or_name')
    token_YD = config.get('Yandex', 'user_token')
    vk_client = VK(token_VK, user_info_VK)
    vk_client.d_t()
    number_album = int(input('Введите порядковый номер альбома, из которого необходимо сохранить фотографии: '))
    data = vk_client.get_data_to_upload(number_album)
    yd_client = Yandex(token_YD)
    yd_client.auto_save_photos(data)














