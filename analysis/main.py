#!/usr/bin/python
import os

import requests
import json
from datetime import datetime
import zipfile
from nested_lookup import nested_lookup

USERS_PROJECT_BASE_URL = "https://api.scratch.mit.edu/users/%s/projects/"
OUTPUT_PATH = "/Users/isa/Documents/Arbeit/Online-Kurs-Scratch/Scratch-Script/Scratch-Programme"

users = [
    'UPSchueler01','UPSchueler02','UPSchueler03','UPSchueler04','UPSchueler05','UPSchueler06','UPSchueler07','UPSchueler08','UPSchueler09','UPSchueler10',
    'UPSchueler11','UPSchueler12','UPSchueler13','UPSchueler14','UPSchueler15','UPSchueler16','UPSchueler17','UPSchueler18','UPSchueler19','UPSchueler20',
    'UPSchueler21','UPSchueler22','UPSchueler23','UPSchueler24','UPSchueler25','UPSchueler26','UPSchueler27','UPSchueler28','glaslos_kuchen','UPSchueler30',
    'UPSchueler31','UPSchueler32','UPSchueler33','UPSchueler34','UPSchueler35','UPSchueler36','UPSchueler37','UPSchueler38','UPSchueler39','UPSchueler40',
    'UPSchueler41','UPSchueler42','UPSchueler43','UPSchueler44','UPSchueler45','UPSchueler46','UPSchueler47','UPSchueler48','UPSchueler49','UPSchueler50',
    'UPSchueler51','UPSchueler52','UPSchueler53','UPSchueler54','UPSchueler55','UPSchueler56','UPSchueler57','UPSchueler58','UPSchueler59','UPSchueler60',
    'UPSchueler61','UPSchueler62','UPSchueler63','UPSchueler64','UPSchueler65','UPSchueler66','UPSchueler67','UPSchueler68','UPSchueler70','UPSchueler71',
    'Minecraft_TNT2010','UPSchueler73','UPSchueler74','UPSchueler75','UPSchueler76','UPSchueler77','UPSchueler78','UPSchueler79',
    'UPSchueler80','UPSchueler81','UPSchueler82','UPSchueler83','UPSchueler84','UPSchueler85','UPSchueler86','UPSchueler87','UPSchueler88','UPSchueler89',
    'UPSchueler92','UPSchueler93','UPSchueler94','UPSchueler96', 'UPSchueler99'
]


def download_projects_for_user(user_name):
    out_folder = os.path.join(OUTPUT_PATH, user_name)
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    response = requests.get(USERS_PROJECT_BASE_URL % user_name)
    projects_json = response.json()
    for project in projects_json:
        download_project(project.get('id'), out_folder)


# Download project json and all assets and put into zip (.sb3) archive
def download_project(id, out_folder):
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36"}

    print("URL: %s" % ("https://projects.scratch.mit.edu/%d" % id))
    response = requests.get("https://projects.scratch.mit.edu/%d" % id, headers=headers)
    project = response.json()

    print('generate ZIP...')
    timestamp = str(datetime.now().strftime("%d-%m-%Y%H%M%S"))
    zipfile_name = '%d_%s.sb3' % (id, timestamp)
    zipfile_out = os.path.join(out_folder, zipfile_name)
    print(zipfile_out)
    try:
        sb3 = zipfile.ZipFile(zipfile_out, 'w')
        sb3.writestr('project.json', json.dumps(project).encode())
        assets = set()
        assets.update(nested_lookup("md5", project))
        assets.update(nested_lookup("baseLayerMD5", project))
        assets.update(nested_lookup("penLayerMD5", project))
        assets.update(nested_lookup("textLayerMD5", project))
        assets.update(nested_lookup("md5ext", project))

        for md5 in assets:
            asset = "https://assets.scratch.mit.edu/internalapi/asset/%s/get/" % md5
            print("Downloading %s" % asset)
            dependency = requests.get(asset, headers=headers)
            sb3.writestr(md5, dependency.content)
        sb3.close()
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    for user in users:
        download_projects_for_user(user)

