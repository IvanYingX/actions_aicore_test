from typing import List, Union
from bs4 import BeautifulSoup
import requests
import re

class AnimalReporter:
    def __init__(self, animal: str):
        self.animal = animal
    
    def _get_request(self) -> Union[bytes, str]:
        ROOT = 'https://en.wikipedia.org/wiki/'
        r = requests.get(ROOT + self.animal)
        return r.text

    def _get_soup(self, html: Union[bytes, str]) -> BeautifulSoup:
        soup = BeautifulSoup(html, 'html.parser')
        return soup
        
    def get_class(self) -> str:
        html = self._get_request()
        soup = self._get_soup(html)
        class_row = soup.find('td', text = re.compile('Class:'))
        animal_class = class_row.find_next_sibling().text.strip()
        return animal_class
    
    def get_taxonomy(self) -> List:
        html = self._get_request()
        soup = self._get_soup(html)
        syn_text = soup.find('a', text = re.compile('Synonyms'))
        if syn_text:
            syn_header = syn_text.find_parent('tr')
            syn_table = syn_header.find_next_sibling()
            contents = syn_table.find_all('i')
            if contents:
                contents = [x.text for x in contents]
                return contents
        else:
            return []

ani = input('Enter an animal: ')
ar = AnimalReporter(ani)
print(ar.get_class())