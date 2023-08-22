import requests


class API:
    def __init__(self):
        self.adr = 'http://45.155.207.232:8080/api/v2/'
        self.session = requests.Session()

    def take_group_list(self):
        return self.session.get(self.adr + 'schedule/list').json()

    def take_schedule_group(self, group):
        return self.session.get(self.adr + f'schedule/{group}').json()

    def take_fio(self, name=None):
        if name is None:
            return self.session.get(self.adr + 'fio').json()
        else:
            return self.session.get(self.adr + f'fio/{name}').json()

