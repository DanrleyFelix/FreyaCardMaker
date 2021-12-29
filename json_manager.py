from os.path import isfile
from json import dump, load


dir_1 = {

  "dir_load_file": "",
  "dir_save_file": "",
  "dir_upload_image": "",
  "dir_save_image": "",
  "upload_web":"0"

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

dir_3 = {

    "card_name_font": "Whitney-SemiboldItalicSC.ttf",
    "card_name_size": 25,
    "card_id_font": "FreeSerifBold.ttf",
    "card_id_size": 20,
    "card_points_font": "FreeSerifBold.ttf",
    "card_points_size": 23,
    "Card_effect_font": "source-sans-pro.light-italic.ttf",
    "Card_effect_size": 18,
    "Card_mp_font": "source-sans-pro.light-italic.ttf",
    "Card_mp_size": 18,
    "Card_race_font": "source-sans-pro.light-italic.ttf",
    "Card_race_size": 15

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
jmanager.createJson('fonts//card_fonts.json',dir_3)