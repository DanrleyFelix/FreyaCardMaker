from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence
import requests
from io import BytesIO
from json_manager import JsonManager
from imageio import mimsave

jmanager = JsonManager()


class Card:

    def __init__(self):

        cardDict = jmanager.readJson('presets//last_edition.json')
        fontsDict = jmanager.readJson('fonts//card_fonts.json')
        self.dirJson = jmanager.readJson('data//data.json')
        self.imFrames = []
        self.totalFrames = 0
        self.newImFrames = []
        # Inicializando os parâmetros da carta
        self.name = cardDict['Name'][:21]
        self.attribute = cardDict['Attribute']
        self.race = cardDict['Race/Class'][:10]
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
        mainCardImage = Image.open(f'images//raw.png')
        self.alpha = base.getchannel('A')
        r,g,b = Image.open(f'card backgrounds//{self.cardBackground}').split()
        self.backgroundCardImage = Image.merge('RGBA',(r,g,b,self.alpha))
        try:
            self.im = Image.open(self.image)
        except (OSError,AttributeError):
            self.im = self.imageLink(self.image)
        # Rating, Rank & attribute
        cardAttribute = Image.open(f'card attributes//{self.attribute.lower()}.png')
        cardRating = Image.open(f'card rating//{self.rating.count("⭐")} stars.png')
        cardRank = Image.open(f'card ranks//{self.rank.lower()}.png')
        self.gifHandler()
        if self.totalFrames > 1:
            self.original_duration = self.im.info['duration']
        for frame in self.imFrames:
            tempBg = self.backgroundCardImage.copy()
            new_img = self.resizeImage(frame)
            #new_img = self.imageMerge(new_img)
            new_img,mask = self.ImageMask(new_img)
            #tempBg = Image.composite(new_img, tempBg, mask)
            tempBg.paste(new_img, (12, 131), mask)
            tempBg.alpha_composite(mainCardImage)
            tempBg.alpha_composite(cardAttribute)
            tempBg.alpha_composite(cardRating)
            tempBg.alpha_composite(cardRank)
            self.ImageFonts(tempBg)
            self.newImFrames.append(tempBg)
        if self.totalFrames > 1:
            self.dirJson["last_show_image"] = 'temp.gif'
        else:
            self.dirJson["last_show_image"] = 'temp.png'
        jmanager.updateJson('data//data.json', data=self.dirJson)
        return True

    def gifHandler(self):

        for frame in ImageSequence.Iterator(self.im):
            frame = frame.convert('RGB')
            self.imFrames.append(frame)
        self.totalFrames = len(self.imFrames)

    def imageLink(self,link):
        
        url = requests.get(link)
        self.im = Image.open(BytesIO(url.content))
        return self.im

    def resizeImage(self,img):
        
        newSize,_,_ = self.ImageSizeNormalize(img)
        newImage = img.resize(newSize)
        img = newImage
        if newImage.size[0] > 346 or newImage.size[1] > 247:
            img = self.imageCrop(img)
        return img

    def imageCrop(self,img):

        imFormat = img.mode
        if str(imFormat) != 'RGB':
            img = img.convert('RGB')
        x_using, y_using= img.size
        _,x_normalized,y_normalized = self.ImageSizeNormalize(img)
        x_normalized = int(x_normalized+0.7)
        y_normalized = int(y_normalized+0.7)
        crops_y = [0,y_using]
        crops_x = [0,x_using]
        if y_normalized > 1:
            crops_y = [int(0.01*y_using/y_normalized),int(y_using - 0.4*(y_using/y_normalized))]
        if x_normalized > 1:
            crops_x = [int(0.1*x_using/x_normalized),int(x_using-(0.1*x_using/x_normalized))]
        img = img.crop((crops_x[0],crops_y[0],crops_x[1],crops_y[1]))
        x_using, y_using= img.size
        if x_using>= self.xLimSize or y_using>= self.yLimSize:
            delta_x = self. xLimSize
            delta_y = self.yLimSize
            limit_sup_x, limit_sup_y = img.size
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
                img = img.crop((x_inc1, y_inc1, limit_sup_x - x_inc2, limit_sup_y - y_inc2))
                img.resize((self.xLimSize,self.yLimSize))
        return img
            
    def imageMerge(self,img):

        alphaMask = Image.open(f'images//alphaMask.png').resize((self.xLimSize,self.yLimSize)).getchannel('A')
        r,g,b = img.split()
        img = Image.merge('RGBA', (r, g, b, alphaMask))
        return img

    def ImageSizeNormalize(self,img):

        x,y = img.size
        x_normalized = x/self.xLimSize
        y_normalized = y/self.yLimSize
        if x_normalized>y_normalized:
            normalize = y_normalized
        else:
            normalize = x_normalized
        newSize = int(x/normalize),int(y/normalize)
        return newSize,x_normalized,y_normalized

    def ImageMask(self,img):

        big_size = (img.size[0] * 3, img.size[1] * 3)
        self.mask = Image.new('L', big_size, 0)
        draw = ImageDraw.Draw(self.mask)
        draw.rectangle((0, 0) + big_size, fill=255)
        self.mask = self.mask.resize(img.size, Image.ANTIALIAS)
        output = ImageOps.fit(img, self.mask.size, bleed=0.5, centering=(0.5, 0.5))
        output.putalpha(self.mask)
        return img,self.mask

    def ImageFonts(self,bg):

        zeros = ['000','00','0','']
        colorFonts = [(255,255,255),(255,255,255),(255,255,255),(245,227,32),(178,247,228)]
        cardNameFont = ImageFont.truetype(f'fonts//{self.cardNameFont}', self.cardNameFontSize)
        cardIdFont = ImageFont.truetype(f'fonts//{self.cardIdFont}', self.cardIdFontSize)
        cardPointsFont = ImageFont.truetype(f'fonts//{self.cardPointsFont}', self.cardPointsFontSize)
        cardMpFont = ImageFont.truetype(f'fonts//{self.cardMpFont}', self.cardMpFontSize)
        cardRaceFont = ImageFont.truetype(f'fonts//{self.cardRaceFont}', self.cardMpFontSize)
        cardEffectFont = ImageFont.truetype(f'fonts//{self.cardEffectFont}', self.cardEffectFontSize)
        draw = ImageDraw.Draw(bg)
        colorFont = colorFonts[self.rating.count("⭐")-1]
        self.kerningFont(-256,67.4,29,self.name.title(),'Sample text',cardNameFont,draw,color=colorFont)
        self.kerningFont(320,284,31,f'{zeros[len(self.id)-1]}{self.id}','Sample text',cardIdFont,draw)
        self.kerningFont(320,294,88,f'{self.points}','Sample text',cardPointsFont,draw)
        self.kerningFont(160,85,467,f'{self.mp}','Sample text',cardMpFont,draw)
        self.kerningFont(0,166,457,f'{self.race}','Sample text',cardRaceFont,draw)
        desc = self.adjustSizeFont(draw,self.description,cardEffectFont)
        #print(self.description, desc)
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
        popItem = ''
        for i in range(0, maxLenght):
            txt = txt + text_list[i] + ' '
            w1_test = draw.textsize(txt,font=font)[0]
            if w1_test >= 275:
                new_txt_list = txt.split()
                popItem = new_txt_list.pop()
                txt = ' '.join(new_txt_list)
            if w1_test >= 250 or i >= maxLenght-1:
                texts.append(txt)
                txt = ''
                try:
                    new_txt_list = text_list[i+1:]
                    if len(popItem) > 0:
                        new_txt_list.insert(0,popItem)
                except IndexError:
                    new_txt_list = [popItem]
                maxLenght = len(new_txt_list)
                if maxLenght == 0:
                    texts.append('')
                else:
                    for j in range(0, maxLenght):
                        txt = txt + new_txt_list[j] + ' '
                        w2_test = draw.textsize(txt,font=font)[0]
                        if w2_test >= 275:
                            new_txt_list = txt.split()
                            new_txt_list.pop()
                            txt = ' '.join(new_txt_list)
                            txt = txt.strip()+'...'
                        if w2_test >= 250 or j >= maxLenght-1:
                            if '.' not in txt:
                                txt = txt+'.'
                            texts.append(txt.strip())
                            return texts
        return texts

    def saveImageTemp(self):

        if self.totalFrames == 1:
            self.newImFrames[0].save('interface//temp.png')
        else:
            # write GIF animation
            if int(self.dirJson["high_quality_preview"]) == 1:
                mimsave('interface//temp.gif',self.newImFrames,fps=1/(self.original_duration/1000))
            else:
                self.newImFrames[0].save('interface//temp.gif', save_all=True, optimize=False, 
                    append_images=self.newImFrames[1:], loop=0, duration=self.original_duration)

    def saveImage(self,dir):

        if len(self.newImFrames) == 1:
            self.newImFrames[0].save(dir)
        else:
            # write GIF animation
            if int(self.dirJson["high_quality_preview"]) == 1:
                mimsave(dir,self.newImFrames,fps=1/(self.original_duration/1000))
            else:
                self.newImFrames[0].save(dir, save_all=True, optimize=False, 
                    append_images=self.newImFrames[1:], loop=0, duration=self.original_duration)
