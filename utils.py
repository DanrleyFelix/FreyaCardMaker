from glob import glob

attributes = ['Darkness', 'Earth', 'Fire And Water', 'Fire', 'Forest', 'Light And Darkness', 'Light', 'Lightning',
 'Neutral', 'Water', 'Wind']

icons_attributes = ['interface//icons_attributes//darkness.png', 'interface//icons_attributes//earth.png',
 'interface//icons_attributes//fire and water.png', 'interface//icons_attributes//fire.png', 
 'interface//icons_attributes//forest.png', 'interface//icons_attributes//light and darkness.png',
'interface//icons_attributes//light.png', 'interface//icons_attributes//lightning.png',
 'interface//icons_attributes//neutral.png', 'interface//icons_attributes//water.png', 
 'interface//icons_attributes//wind.png']

ratings = ['⭐','⭐⭐','⭐⭐⭐','⭐⭐⭐⭐','⭐⭐⭐⭐⭐']

ranks = ['D-','D+','C-','C+','B-','B+','A-','A+','S-','S+','R-','R+']

card_points = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85',
 '90', '95', '100', '105', '110', '115', '120', '125', '130', '135', '140', '145', '150', '155', '160', '165', '170', 
 '175', '180', '185', '190', '195', '200']

mp = ['0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90',
  '95', '100', '105', '110', '115', '120', '125', '130', '135', '140', '145', '150', '155', '160', '165', '170', '175',
   '180', '185', '190', '195', '200', '205', '210', '215', '220', '225', '230', '235', '240', '245', '250', '255', '260',
    '265', '270', '275', '280', '285', '290', '295', '300']

races = ['Human', 'Servant', 'Magus', 'Goddess', 'Renard', 'God', 'Pallum', 'Elf', 'Amazon.', 'Dwarf',
        'Werewolf', 'Boaz', 'Dark elf', 'Chienth.', 'H. Bunny', 'Creature', 'Cat People', 'Half Elf', 'Spirit',
        'Semi-serv.', 'Flügel', 'Imanity', 'Ex-Machina', 'Warbeasts', 'Old God', 'Demon', 'Angel', 'Shinigami']

backgrounds = glob('card backgrounds\\*.png')
new_backgrounds = []
for background in backgrounds:
  a = background.replace('card backgrounds\\','')
  new_backgrounds.append(a)
backgrounds = new_backgrounds

def label_distance(start:int,stop:int,step:int):

  dist = []
  for i in range(start,stop,step):
    dist.append(i)
  return dist


