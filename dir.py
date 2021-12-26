from os import listdir
from os.path import isfile, join
mypath = 'C://Users//Danrl//Desktop//Freya//Freya Card Maker//interface//icons_ranks'

new = []
for a in listdir(mypath):
    new.append(f'interface//icons_ranks//{a}')
print(new)
