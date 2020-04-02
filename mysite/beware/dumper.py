import requests
import json

class DumpInfos():
    '''
    Class used to request API services and fetch datas
    to be displayed.
    '''
    def __init__(self, query):
        self.query = query

    def __repr__(self):
        return self.query

    def get_images(self):

        resp = requests.get(f'https://api.spacexdata.com/v3/{self.query}')   
        resp = resp.json()
        name = resp[0].get('name')
        desc = resp[0].get('description')
        img_list = resp[0].get('flickr_images')
        infos = {
            'name':name,
            'img_list':img_list,
            'desc':desc
        }
        return infos
