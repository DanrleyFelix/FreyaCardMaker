mypath = 'C://Users//Danrl//Desktop//Freya//Freya Card Maker'

attributes = ['Darkness', 'Earth', 'Fire And Water', 'Fire', 'Forest', 'Light And Darkness', 'Light', 'Lightning',
 'Neutral', 'Water', 'Wind']

icons_attributes = ['interface//icons_attributes//darkness.png', 'interface//icons_attributes//earth.png',
 'interface//icons_attributes//fire and water.png', 'interface//icons_attributes//fire.png', 
 'interface//icons_attributes//forest.png', 'interface//icons_attributes//light and darkness.png',
'interface//icons_attributes//light.png', 'interface//icons_attributes//lightning.png',
 'interface//icons_attributes//neutral.png', 'interface//icons_attributes//water.png', 'interface//icons_attributes//wind.png']

ratings = ['⭐','⭐⭐','⭐⭐⭐','⭐⭐⭐⭐','⭐⭐⭐⭐⭐']

ranks = ['D-','D+','C-','C+','B-','B+','A-','A+','S-','S+','R-','R+']

backgrounds = ['dark-rezero 1.png', 'general-blue 1.png', 'general-blue 2.png', 'general-blue 3.png', 
'general-blue-forest 1.png', 'general-blue-forest 2.png', 'general-blue-forest 3.png', 'general-blue-white 1.png',
'general-dark 1.png', 'general-dark-isekai 1.png', 'general-forest 1.png', 'general-forest-sky 1.png', 
'general-isekai 1.png', 'general-isekai 2.png', 'general-isekai 3.png', 'general-isekai 4.png', 'general-night-sky 1.png',
'general-sky 1.png', 'general-water 1.png', 'general-water-forest 1.png', 'general-weak-dark 1.png', 'general-white-forest 1.png',
'hard-dark-fate 1.png', 'hard-dark-fate 2.png', 'hard-dark-fate 3.png', 'hard-white-fate 1.png', 'hard-white-fate 2.png',
'hard-white-fate 3.png', 'medium-dark-fate 1.png', 'medium-dark-fate 2.png', 'normal-fate 1.png', 'normal-fate 2.png',
 'Weak-dark-fate 1.png', 'Weak-dark-fate 2.png', 'yumeko 1.png']

card_points = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85',
 '90', '95', '100', '105', '110', '115', '120', '125', '130', '135', '140', '145', '150', '155', '160', '165', '170', 
 '175', '180', '185', '190', '195', '200']

mp = ['0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90',
  '95', '100', '105', '110', '115', '120', '125', '130', '135', '140', '145', '150', '155', '160', '165', '170', '175',
   '180', '185', '190', '195', '200', '205', '210', '215', '220', '225', '230', '235', '240', '245', '250', '255', '260',
    '265', '270', '275', '280', '285', '290', '295', '300']

races = ['Human', 'Servant', 'Magus', 'Goddess', 'Renard', 'God', 'Pallum', 'Elf', 'Amazoness', 'Dwarf',
        'Werewolf', 'Boaz', 'Dark elf', 'Chienthrope', 'Hume Bunny', 'Creature', 'Cat People', 'Half Elf', 'Spirit',
        'Semi-serv.', 'Flügel', 'Imanity', 'Ex-Machina', 'Warbeasts', 'Old God', 'Demon', 'Angel', 'Shinigami']

help_message = '''Upload the card's picture and try to preview it.
'''

def label_distance(start:int,stop:int,step:int):

  dist = []
  for i in range(start,stop,step):
    dist.append(i)
  return dist
