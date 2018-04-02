import time
import random
from parsers.parser import Parser
from scrappers import scrapper
from storages import file_storage as fs
import re


from bs4 import BeautifulSoup  # You can use any other library


class HtmlParser(Parser):

    def parse(self, data):
        """
        Parses html text and extracts field values
        :param data: html text (page)
        :return: a dictionary where key is one
        of defined fields and value is this field's value
        """
        soup = BeautifulSoup(data)

        # Your code here: find an appropriate html element
        objects_list = soup.find('div', {'class': 'itemsList'})

        # Your code here
        return [dict()]

    def get_parsed_data(self, data, domen):
        fs_object = fs.FileStorage('data1.csv')
        soup = BeautifulSoup(data)
        RegExp = re.compile(r'[\d]+')
        objects_list = soup.find_all("div", {"class": "item item_list js-catalog-item-enum item_car clearfix c-b-0"})
        for el_of_list in objects_list :
            price = re.sub('[\s+]', '', el_of_list.find( "div", {"class" :"price"}).p.next)
            price = RegExp.search(price).group()
            photo_len = el_of_list.find("i", {"class": "i i-photo"})
            if photo_len != None :
                photo_len = re.sub('[\s+]', '', photo_len.next)
            else:
                photo_len = '0'
            photo_len = RegExp.search(photo_len).group()
            link = domen + el_of_list.find("h3", {"class": "h3 fader description-title-h3"}).find("a", {"class": "description-title-link"}).attrs["href"]
            time.sleep(int(random.uniform(10, 20)))
            scr_add = scrapper.Scrapper()
            soup_add = BeautifulSoup(scr_add.scrap_process(link).text)
            params_add = soup_add.find("ul", {"class" : "item-params-list"}).find_all("li", {"class" : "item-params-list-item"})
            marka = ''
            model = ''
            year = ''
            probeg = ''
            owners = ''
            for param in params_add:
                if param.span.next.strip(' \t\n\r') == "Марка:":
                    marka = param.span.next_sibling.strip(' \t\n\r')
                if param.span.next.strip(' \t\n\r') == "Модель:":
                    model = param.span.next_sibling.strip(' \t\n\r')
                if param.span.next.strip(' \t\n\r') == "Год выпуска:":
                    year = RegExp.search(param.span.next_sibling).group()
                if param.span.next.strip(' \t\n\r') == "Пробег:":
                    probeg = RegExp.search(param.span.next_sibling).group()
                if param.span.next.strip(' \t\n\r') == "Владельцев по ПТС:":
                    owners = RegExp.search(param.span.next_sibling).group()
            discription = "" + soup_add.find("div", {"class": "item-description-text"}).p.text.strip(' \t\n\r')
            len_discription = str(len(discription))
            soup_add.clear(True)
            del(soup_add)
            print(link+"\n")
            print(marka, model, price, year, photo_len, probeg, owners)
            id = RegExp.search(el_of_list.attrs['id']).group().strip(' \t\n\r')
            line = ["" + id + "," + marka + "," + model + "," + price + "," + year + "," + photo_len + "," + probeg + "," + owners + "," + len_discription]
            print(line)
            fs_object.append_data(line)
            print('\n')
            #код для pandas frame
            """data_liast['marka'].append(marka)
            data_liast['model'].append(model)
            data_liast['price'].append(price)
            data_liast['year'].append(year)
            data_liast['year'].append(photo_len)
            data_liast['probeg'].append(probeg)
            data_liast['owners'].append(owners)"""

        del (fs_object)
