from os.path import isfile
from json import dump, load


dir_1 = {

  "dir_load_file": "",
  "dir_save_file": "",
  "dir_upload_image": "",
  "dir_save_image": "",

}

dir_2 = {

  "Name": "",
  "Attribute": "Darkness",
  "Race/Class": "Human",
  "Rating": "\u2b50",
  "Rank": "D-",
  "Image": "",
  "Background": "normal-fate 1.png",
  "MP": "0",
  "Card Points": "5",
  "ID": "",
  "Effect/Pack/Description 0": "",
  "Effect/Pack/Description 1": "",
  "Effect/Pack/Description 2": ""

}


class JsonManager:

    def createJson(self, filepath, data):

        if not isfile(filepath):
            with open(filepath,'w') as f:
                dump(data,f,indent=2,separators=(',',': '))

    def readJson(self, filepath):
        if isfile(filepath):
            with open(filepath, encoding="utf8") as f:
                data = load(f)
            return data
        else:
            return False

    def updateJson(self, filepath, data):
        with open(filepath, 'w', encoding="utf8") as f:
            dump(data, f, indent=2, separators=(',',': '))


jmanager = JsonManager()
jmanager.createJson('data//data.json',dir_1)
jmanager.createJson('presets//last_edition.json',dir_2)