from bs4 import BeautifulSoup
from datetime import date
from trawler.book import Book
import requests
import re

# fetch site
site_url = 'https://www.scheltema.nl/fictie'
response = requests.get(site_url)

# soupify site
soup = BeautifulSoup(response.text, 'html.parser')

# get links to top books
conts = []
for cont in soup.find_all('div'):
    try:
        if 'parool-top-10-fictie' in cont.get('class'):
            conts.append(cont)
    except TypeError:
        pass

top_10_links = []

for cont in conts:
    for link in cont.find_all('a'):
        link_ref = link.get('href')
        # if link has isbn, and isn't already in the list, add link to list
        isbn_ref = re.search("\d{9}", link_ref)
        if isbn_ref and link_ref not in top_10_links:
            top_10_links.append(link_ref)

# access links
link_dict = {}

for link in top_10_links:
    link_url = 'https://www.scheltema.nl//' + link + '#'
    link_response = requests.get(link_url)
    link_soup = BeautifulSoup(link_response.text, 'html.parser')
    link_dict[link] = link_soup

# collate information about the books
search_data = {
    "date_of_access": date.today(),
    "source": site_url,
    "country_of_list": "Netherlands",
}

counter = 1

for key in link_dict:
    next_book = Book

    # rank
    next_book.rank_in_list = counter
    counter += 1

    # title
    for h1 in link_dict[key].find_all('h1'):
        book_title = h1.text[h1.text.find('>') + 1: h1.text.rfind('<')].strip().rstrip()
        next_book.title = book_title

    # author
    for a in link_dict[key].find_all('a'):
        try:
            if 'book-detail__content__author' in a.get('class'):
                author_name = a.text[a.text.find('>') + 1:].strip().rstrip()
                next_book.authors_first_name = author_name.split(' ')[0]
                next_book.authors_last_name = author_name.split(' ')[1]
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
                next_book.currency = split_price[0]
                next_book.price = split_price[1]
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
                            next_book.isbn = item
                # imprint - DON'T FORGET TO SORT PUBLISHER
                elif 'Uitgever' in div.text:
                    stripped_div = div.text.split('\n')
                    for item in stripped_div:
                        if item and item != 'Uitgever':
                            next_book.imprint = item
                # publish date
                elif 'Verschenen' in div.text:
                    stripped_div = div.text.split('\n')
                    for item in stripped_div:
                        if item and re.search('[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]', item):
                            next_book.publish_date = item
                # language
                elif 'Taal' in div.text:
                    stripped_div = div.text.split('\n')
                    for item in stripped_div:
                        if item and item != 'Taal':
                            next_book.language = item
                # pages
                elif 'Bladzijden' in div.text:
                    stripped_div = div.text.split('\n')
                    for item in stripped_div:
                        pages_match = re.findall('[0-9]+', item)
                        if item and pages_match:
                            next_book.pages = pages_match[0]
                # genre
                elif 'Rubriek' in div.text:
                    stripped_div = div.text.split('\n')
                    for item in stripped_div:
                        if item and item != 'Rubriek':
                            next_book.genre = item
                # genre
                elif 'Bindwijze' in div.text:
                    stripped_div = div.text.split('\n')
                    for item in stripped_div:
                        if item and item != 'Bindwijze':
                            next_book.binding = item
        except TypeError:
            pass

"""
series_no = self.series_no
illustrators_first_name = self.illustrators_first_name
illustrators_last_name = self.illustrators_last_name
"""
