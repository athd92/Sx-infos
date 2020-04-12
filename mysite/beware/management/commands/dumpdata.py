from django.core.management.base import BaseCommand, CommandError
from django.db import models
from beware.models import Specifications
import time
import requests
import json
from tqdm import tqdm


class Command(BaseCommand):
    help = "Dump, or update the local database from SpaceX API"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Lancement du programme"))
        cats = tqdm(
            [
                "dragons",
                "capsules",
                "cores",
                "history",
                "info",
                "landpads",
                "launches",
                "launchpads",
                "missions",
                "payloads",
                "rockets",
                "roadster",
                "ships",
            ]
        )
        for i in cats:
            resp = requests.get(f"https://api.spacexdata.com/v3/{i}")
            resp = resp.json()
            for k in resp:
                try:
                    n = list(k.keys())[0]
                except:
                    n = i
                try:
                    datas = Specifications(name=n, all_datas=k, category=i)
                except:
                    datas = Specifications(name=i, all_datas=k, category=i)
                datas.save()

        self.stdout.write(self.style.SUCCESS("Opération terminée: [OK]"))
