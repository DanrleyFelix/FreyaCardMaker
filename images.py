from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import requests
from io import BytesIO
from json_manager import JsonManager

jmanager = JsonManager()


class Card:

    def __init__(self):

        cardDict = jmanager.readJson('presets//last_edition.json')
        fontsDict = jmanager.readJson('fonts//card_fonts.json')
        # Inicializando os parâmetros da carta
        self.name = cardDict['Name'][:20]
        self.attribute = cardDict['Attribute']
        self.race = cardDict['Race/Class'][:20]
        self.rating = cardDict['Rating']
        self.rank = cardDict['Rank']
        self.image = cardDict['Image']
        self.cardBackground = cardDict['Background']
        self.mp = cardDict['MP']
        self.points = cardDict['Card Points']
        self.id = cardDict['ID'][:4]
        self.description = cardDict['Effect/Pack/Description 0']+\
                            ' ' + cardDict['Effect/Pack/Description 1']+\
                            ' ' + cardDict['Effect/Pack/Description 2']
        # Inicializando os parâmetros de cada fonte na carta
        self.cardNameFont = fontsDict['card_name_font']
        self.cardNameFontSize = int(fontsDict['card_name_size'])
        self.cardIdFont = fontsDict['card_id_font']
        self.cardIdFontSize = int(fontsDict['card_id_size'])
        self.cardPointsFont = fontsDict['card_points_font']
        self.cardPointsFontSize = fontsDict['card_points_size']
        self.cardEffectFont = fontsDict['card_effect_font']
        self.cardEffectFontSize = int(fontsDict['card_effect_size'])
        self.cardMpFont = fontsDict['card_mp_font']
        self.cardMpFontSize = int(fontsDict['card_mp_size'])
        self.cardRaceFont = fontsDict['card_race_font']
        self.cardRaceFontSize = int(fontsDict['card_race_size'])
       
    def uploadImages(self):
        
        self.xLimSize = 346
        self.yLimSize = 247
        base = Image.open(f'images//base.png')
        self.alpha = base.getchannel('A')
        try:
            self.im = Image.open(self.image)
        except (OSError,AttributeError):
            self.imageLink(self.image)
        self.resizeImage()
        self.imageMerge()
        self.ImageMask()
        self.mainCardImage = Image.open(f'images//raw.png')
        r,g,b = Image.open(f'card backgrounds//{self.cardBackground}').split()
        self.backgroundCardImage = Image.merge('RGBA',(r,g,b,self.alpha))
        self.backgroundCardImage.paste(self.im, (12, 131), self.mask)
        self.backgroundCardImage.alpha_composite(self.mainCardImage)
        # Rating, Rank & attribute
        cardAttribute = Image.open(f'card attributes//{self.attribute.lower()}.png')
        cardRating = Image.open(f'card rating//{self.rating.count("⭐")} stars.png')
        cardRank = Image.open(f'card ranks//{self.rank.lower()}.png')
        self.backgroundCardImage.alpha_composite(cardAttribute)
        self.backgroundCardImage.alpha_composite(cardRating)
        self.backgroundCardImage.alpha_composite(cardRank)
        # Adicionando as fontes
        self.ImageFonts()

    def imageLink(self,link):

        url = requests.get(link)
        self.im = Image.open(BytesIO(url.content))

    def resizeImage(self):
        
        newSize,_,_ = self.ImageSizeNormalize()
        newImage = self.im.resize(newSize)
        self.im = newImage
        if newImage.size[0] > 346 or newImage.size[1] > 247:
            self.imageCrop()  

    def imageCrop(self):

        imFormat = self.im.mode
        if str(imFormat) != 'RGB':
            self.im = self.im.convert('RGB')
        x_using, y_using= self.im.size
        _,x_normalized,y_normalized = self.ImageSizeNormalize()
        x_normalized = int(x_normalized+0.7)
        y_normalized = int(y_normalized+0.7)
        crops_y = [0,y_using]
        crops_x = [0,x_using]
        if y_normalized > 1:
            crops_y = [int(0.01*y_using/y_normalized),int(y_using - 0.4*(y_using/y_normalized))]
        if x_normalized > 1:
            crops_x = [int(0.1*x_using/x_normalized),int(x_using-(0.1*x_using/x_normalized))]
        self.im = self.im.crop((crops_x[0],crops_y[0],crops_x[1],crops_y[1]))
        x_using, y_using= self.im.size
        if x_using>= self.xLimSize or y_using>= self.yLimSize:
            delta_x = self. xLimSize
            delta_y = self.yLimSize
            limit_sup_x, limit_sup_y = self.im.size
            if x_using> self.xLimSize or y_using> self.yLimSize:
                x_inc = limit_sup_x - delta_x
                y_inc = limit_sup_y - delta_y
                half_x = int(x_inc / 2)
                half_y = int(y_inc / 2)
                x_inc1 = half_x
                x_inc2 = half_x
                y_inc1 = half_y
                y_inc2 = half_y
                if x_inc % 2 != 0:
                    if x_inc1 < 0:
                        x_inc2 = x_inc2 - 1
                    else:
                        x_inc2 = x_inc2 + 1
                if y_inc % 2 != 0:
                    if x_inc1 < 0:
                        y_inc2 = y_inc2 - 1
                    else:
                        y_inc2 = y_inc2 + 1
                self.im = self.im.crop((x_inc1, y_inc1, limit_sup_x - x_inc2, limit_sup_y - y_inc2))
                self.im.resize((self.xLimSize,self.yLimSize))
            
    def imageMerge(self):

        alphaMask = Image.open(f'images//alphaMask.png').resize((self.xLimSize,self.yLimSize)).getchannel('A') 
        r,g,b = self.im.split()
        self.im = Image.merge('RGBA', (r, g, b, alphaMask))

    def ImageSizeNormalize(self):

        x,y = self.im.size
        x_normalized = x/self.xLimSize
        y_normalized = y/self.yLimSize
        if x_normalized>y_normalized:
            normalize = y_normalized
        else:
            normalize = x_normalized
        newSize = int(x/normalize),int(y/normalize)
        return newSize,x_normalized,y_normalized

    def ImageMask(self):

        big_size = (self.im.size[0] * 3, self.im.size[1] * 3)
        self.mask = Image.new('L', big_size, 0)
        draw = ImageDraw.Draw(self.mask)
        draw.rectangle((0, 0) + big_size, fill=255)
        self.mask = self.mask.resize(self.im.size, Image.ANTIALIAS)
        output = ImageOps.fit(self.im, self.mask.size, bleed=0.5, centering=(0.5, 0.5))
        output.putalpha(self.mask)
        del draw

    def ImageFonts(self):

        zeros = ['000','00','0','']
        colorFonts = [(255,255,255),(255,255,255),(255,255,255),(245,227,32),(178,247,228)]
        cardNameFont = ImageFont.truetype(f'fonts//{self.cardNameFont}', self.cardNameFontSize)
        cardIdFont = ImageFont.truetype(f'fonts//{self.cardIdFont}', self.cardIdFontSize)
        cardPointsFont = ImageFont.truetype(f'fonts//{self.cardPointsFont}', self.cardPointsFontSize)
        cardMpFont = ImageFont.truetype(f'fonts//{self.cardMpFont}', self.cardMpFontSize)
        cardRaceFont = ImageFont.truetype(f'fonts//{self.cardRaceFont}', self.cardMpFontSize)
        cardEffectFont = ImageFont.truetype(f'fonts//{self.cardEffectFont}', self.cardEffectFontSize)
        draw = ImageDraw.Draw(self.backgroundCardImage)
        colorFont = colorFonts[self.rating.count("⭐")-1]
        self.kerningFont(-256,67.4,29,self.name.title(),'Sample text',cardNameFont,draw,color=colorFont)
        self.kerningFont(320,284,31,f'{zeros[len(self.id)-1]}{self.id}','Sample text',cardIdFont,draw)
        self.kerningFont(320,294,88,f'{self.points}','Sample text',cardPointsFont,draw)
        self.kerningFont(160,85,467,f'{self.mp}','Sample text',cardMpFont,draw)
        self.kerningFont(0,166,457,f'{self.race}','Sample text',cardRaceFont,draw)
        desc = self.adjustSizeFont(draw,self.description,cardEffectFont)
        draw.text((60,409),desc[0],fill='white',font=cardEffectFont)
        draw.text((60,430),desc[1],fill='white',font=cardEffectFont)

    def kerningFont(self,desired_width_of_text,xpos,ypos,header_text,text,font,draw,color=(255,255,255)):

        total_text_width, _ = draw.textsize(text,font=font)
        width_difference = desired_width_of_text-total_text_width
        gap_width = int(width_difference/((total_text_width) - 1))
        for letter in header_text:
            draw.text((xpos,ypos),letter,fill=color,font=font)
            letter_width, _ = draw.textsize(letter, font=font)
            xpos += letter_width+gap_width
    
    def adjustSizeFont(self,draw,text,font):

        texts = []
        text_list = text.split()
        txt = ''
        maxLenght = len(text_list)
        for i in range(0, maxLenght):
            txt = txt + text_list[i] + ' '
            w1_test = draw.textsize(txt,font=font)[0]
            if w1_test >= 275:
                new_txt_list = txt.split()
                new_txt_list.pop()
                txt = ' '.join(new_txt_list)
            if w1_test >= 250 or i == maxLenght-1:
                texts.append(txt)
                txt = ''
                new_txt_list = text_list[i:]
                maxLenght = len(new_txt_list)
                for j in range(0, maxLenght):
                    txt = txt + new_txt_list[j] + ' '
                    w2_test = draw.textsize(txt,font=font)[0]
                    if w2_test >= 275:
                        new_txt_list = txt.split()
                        new_txt_list.pop()
                        txt = ' '.join(new_txt_list)
                        txt = txt.strip()+'...'
                    if w2_test >= 250 or j == maxLenght-1:
                        if '.' not in txt:
                            txt = txt+'.'
                        texts.append(txt.strip())
                        return texts

    def saveImage(self,dir):

        self.backgroundCardImage.save(dir)
