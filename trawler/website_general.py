from bs4 import BeautifulSoup
from datetime import date
from trawler.book import Book
from resources.resources import site_nav
import requests
import urllib.request
import re
import json

class Website:
    def __init__(self, site_url, country):
        self.site_url = site_url
        self.response = self.get_source()
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.top_books_section = []
        self.top_links = []
        self.search_links = []

        self.book_collection = [None for i in range(len(self.top_links))]
        self.search_data = {
            "date_of_access": date.today(),
            "source": self.site_url,
            "country_of_list": country,
        }

    def get_source(self):
        return requests.get(self.site_url)


    def get_links(self):
        """Retrieves the links to the top books listed on the webpage - these
        links can be accessed in the list variable top_links"""
        str_soup = str(self.soup)
        all_links = []
        # get links with a tags
        a_links = self.soup.find_all('a')
        for link in a_links:
            if link not in all_links:
                all_links.append(str(link.get('href')))
        # get links without a tags
        http_links = re.findall(r'https://[A-Za-z0-9/.-]+"', str_soup)
        for link in http_links:
            if link not in all_links:
                all_links.append(link[:-1])
        # add links to top_links if they contain isbn
        for link in set(all_links):
            try:
                isbn_ref = re.search("[0-9]{13}?", link)
                if isbn_ref and link[:-1] not in self.top_links:
                    self.top_links.append(link)
            except TypeError:
                pass


    def get_base_url(self):
        """Extracts the sites base url from the url provided to the object
        in the form of [domain-name].[top-level-domain]"""
        base = re.findall(r"([A-Za-z0-9-]+\.(com|nl))", self.site_url)
        return base[0][0]

    def through_the_dict(self, soup, dict):
        working_soup = soup
        for key in dict.items():
            if type(dict[key]) == list:
                for item in dict[key]:
                    working_soup = working_soup.find_all(item['findall'], {item['filter'].keys()[0]: item['filter'].values()[0]})
                working_soup = working_soup.find_all()
            # for each item (author, title, isbn) in dict
            got = working_soup.find_all(dict[key]['findall'], {dict[key]['filter'].keys()[0]: dict[key]['filter'].values()[0]})
            if 'get' in dict[key]:
                got = got.get(dict[key]['get'])
            elif 'get_text' in dict[key]:
                got = got.get(dict[key]['get_text'])
        return got

    def get_link_details(self, link):
        """Follows a list of links to obtain details to form the search link"""
        new_link = link
        # in case the link is a partial address, assemble full address
        if not re.match(r'^https://', link):
            new_link = 'https://' + self.get_base_url() + '/' + link + '#'

        # get soup from full address
        link_response = requests.get(new_link)
        link_soup = BeautifulSoup(link_response.text, 'html.parser')

        # prepare variables for search link
        author_name = ""
        book_title = ""
        isbn = ""

        # from resources, get the search tree for the current website
        print('base url', self.get_base_url())
        search_tree = site_nav[self.get_base_url()]
        print(search_tree)

        # iterate through search tree and get the required information from the soup
        current_soup = None
        for key in search_tree.keys():
            print('key', key)
            for item in search_tree[key]:
                print('item', item)
                current_soup = link_soup.find_all(item['findall'], item['filter'])
                print(current_soup)
                try:
                    if 'json' in item:
                        print('json in item')
                        print(current_soup[0].contents[0])
                        print(type(current_soup[0].contents[0]))
                        data = current_soup[0].contents[0] #MAKE THE READING OF THE JSON WORK!!!
                        print(json.loads(data)[item['json']])
                        json_object = json.loads(data)[item['json']]
                        with open('red.txt', 'w') as file:
                            file.writelines(json.loads(data)) #GET JSON EXPORTED AND FORMATTED TO SEE NESTING TREE FOR AUTHOR NAME
                        print(json_object)
                except TypeError:
                    pass
                try:
                    if 'get_text' in item:
                        print('get_text in item')
                        print('item', item)
                        if key == 'author':
                            author_name = current_soup[0].get_text()
                            print(author_name)
                        elif key == 'isbn':
                            isbn = current_soup[0].get_text()
                            print(isbn)
                        elif key == 'title':
                            book_title = current_soup[0].get_text()
                            print(book_title)
                except TypeError:
                    pass
                try:
                    if 'get' in item:
                        print('get in item')
                        print('item', item)
                        if key == 'author':
                            author_name = current_soup[0].get(item['get'])
                            print(author_name)
                        elif key == 'isbn':
                            isbn = current_soup[0].get(item['get'])
                            print(isbn)
                        elif key == 'title':
                            book_title = current_soup[0].get(item['get'])
                            print(book_title)
                except TypeError:
                    pass

        return [author_name, book_title, isbn]

    def bruna_get_author(self, soup, type, json_key):
        data = soup.select(type)[1]
        json_object = json.loads(data.text)[json_key]
        print(json_object)
        return json_object


    def scheltema_search_link(self, author, title, isbn):
        #https://www.scheltema.nl/boek/?authortitle=matt-haig/middernachtbibliotheek--9789048860067
        return "https://www.scheltema.nl/boek/?authortitle=" + author + "/" + title + '--' + isbn + '#'


    def get_data(self):
        # access links
        link_dict = {}

        for link in self.top_links:
            link_details = self.get_link_details(link)
            schelt_link = self.scheltema_search_link(link_details[0], link_details[1], link_details[2])
            link_response = requests.get(schelt_link)
            link_soup = BeautifulSoup(link_response.text, 'html.parser')
            link_dict[link] = link_soup

        # collate information about the books
        counter = 1
        for link in self.top_links:
            self.book_collection.append(Book())

        for key in link_dict:
            #next_book = Book

            # rank
            self.book_collection[counter - 1].rank_in_list = counter

            # title
            for h1 in link_dict[key].find_all('h1'):
                book_title = h1.text[h1.text.find('>') + 1: h1.text.rfind('<')].strip().rstrip()
                self.book_collection[counter - 1].title = book_title

            # author
            for a in link_dict[key].find_all('a'):
                try:
                    if 'book-detail__content__author' in a.get('class'):
                        author_name = a.text[a.text.find('>') + 1:].strip().rstrip()
                        self.book_collection[counter - 1].authors_first_name = author_name.split(' ')[0]
                        self.book_collection[counter - 1].authors_last_name = author_name.split(' ')[1]
                except TypeError:
                    pass

            # price
            for span in link_dict[key].find_all('span'):
                try:
                    if 'main-price' in span.get('class'):
                        # make str out of bs4 object, extract price
                        price = span.text[span.text.find('>') + 1: span.text.rfind('<')]
                        # split currency and price
                        split_price = price.split(" ")
                        self.book_collection[counter - 1].currency = split_price[0]
                        self.book_collection[counter - 1].price = split_price[1]
                except TypeError:
                    pass

            for div in link_dict[key].find_all('div'):
                try:
                    if 'book-detail_specifications-grid_row' in div.get('class'):
                        # isbn
                        if 'ISBN' in div.text:
                            stripped_div = div.text.split('\n')
                            for item in stripped_div:
                                if item and re.search('\d{9}', item):
                                    self.book_collection[counter - 1].isbn = item
                        # imprint - DON'T FORGET TO SORT PUBLISHER
                        elif 'Uitgever' in div.text:
                            stripped_div = div.text.split('\n')
                            for item in stripped_div:
                                if item and item != 'Uitgever':
                                    self.book_collection[counter - 1].imprint = item
                        # publish date
                        elif 'Verschenen' in div.text:
                            stripped_div = div.text.split('\n')
                            for item in stripped_div:
                                if item and re.search('[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]', item):
                                    self.book_collection[counter - 1].publish_date = item
                        # language
                        elif 'Taal' in div.text:
                            stripped_div = div.text.split('\n')
                            for item in stripped_div:
                                if item and item != 'Taal':
                                    self.book_collection[counter - 1].language = item
                        # pages
                        elif 'Bladzijden' in div.text:
                            stripped_div = div.text.split('\n')
                            for item in stripped_div:
                                pages_match = re.findall('[0-9]+', item)
                                if item and pages_match:
                                    self.book_collection[counter - 1].pages = pages_match[0]
                        # genre
                        elif 'Rubriek' in div.text:
                            stripped_div = div.text.split('\n')
                            for item in stripped_div:
                                if item and item != 'Rubriek':
                                    self.book_collection[counter - 1].genre = item
                        # genre
                        elif 'Bindwijze' in div.text:
                            stripped_div = div.text.split('\n')
                            for item in stripped_div:
                                if item and item != 'Bindwijze':
                                    self.book_collection[counter - 1].binding = item
                except TypeError:
                    pass
            #self.book_collection.append(next_book)
            counter += 1


x = Website('https://www.bruna.nl/boeken-top-10/literatuur-roman-top-10', "Netherlands")
x.get_links()
print("Printing x.toplinks")
print(x.top_links)
x.get_link_details('https://www.bruna.nl/boeken/de-zeven-zussen-7-de-zevende-zus-9789401614283')
#x.get_data()
#print(x.book_collection)
#print(len(x.book_collection))
#for book in x.book_collection:
#    print(book)