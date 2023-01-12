import requests
from os.path import isfile
from os import stat
import pandas as pd


class Main:

    API = "https://pse.kominfo.go.id/static/json-static/"
    PSE_ASING = "ASING_TERDAFTAR"
    PSE_LOKAL = "LOKAL_TERDAFTAR"

    @classmethod
    def puller(self, type: str = PSE_ASING):
        refresh_timeout = 3
        try:
            how_much = requests.get(url=f"{self.API}{type}/0.json").json()
        except (requests.ConnectionError, requests.HTTPError) as err:
            print(f"Server PSE down, {err}")
            return
        columns = ['id', 'type']
        rows = []
        columns.extend(how_much['data'][0]['attributes'].keys())

        for a in range(how_much['meta']['page']['lastPage']):
            try:
                data = requests.get(url=f"{self.API}{type}/{a}.json")
                print(f"On Page {a}.json", end="\r")
                ab = data.json()
            
                for adf in ab['data']:
                    temp = [adf['id'], adf['type']]
                    temp.extend(adf['attributes'].values())
                    rows.append(temp)
            except (requests.ConnectionError, requests.HTTPError):
                if refresh_timeout != 0:
                    refresh_timeout -= 1
                    a -= 1
                    print(f"Failed to pull page {a}.json, trying again")
                    continue
                else:
                    print(f"Failed to pull page {a}.json, passing page")
                    continue

        df = pd.DataFrame(rows, columns=columns)
        df.to_csv(f'{type}.csv', index=False)
        

    def pse_asing(self, force_update: bool = False):
        try:
            if (isfile(self.PSE_ASING+".csv") is False or stat(self.PSE_ASING+".csv").st_size == 0) or force_update:
                print(f"Pulling {self.PSE_ASING}...")
                self.puller()
                print(f'Succefully pulled on {self.PSE_ASING}.csv')
            else:
                print(f'File already exist {self.PSE_ASING}.csv. Add param force_update=True to override it')
        except Exception as ad:
            print(ad)

    def pse_lokal(self, force_update: bool = False):
        try:
            if (isfile(self.PSE_LOKAL+".csv") is False or stat(self.PSE_LOKAL+".csv").st_size == 0) or force_update:
                print(f"Pulling {self.PSE_LOKAL}...")
                self.puller(type=self.PSE_LOKAL)
                print(f'Succefully pulled on {self.PSE_LOKAL}.csv')
            else:
                print(f'Succefully pulled on {self.PSE_LOKAL}.csv. Add param force_update=True to override it')
        except Exception as ad:
            print(ad)

ad = Main()
ad.pse_asing()
ad.pse_lokal()