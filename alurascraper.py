from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import mechanize
import os
import re

liga = 'https://cursos.alura.com.br'


# lists properties
def _listing(opcoes):
    while True:
        escolha = ''
        os.system('cls')
        print(' | '.join(str(i) for i in opcoes))
        print('Selecione uma das opções:')
        opcao = input()
        for i in opcoes:
            if opcao in i and opcoes:
                escolha = i
                break
        if escolha:
            break
    return escolha


# Scraps Alura Formations!
class AluraScraper:

    def __init__(self, session=None):
        # If called by AluraLogin, uses session from AluraLogin
        if session:
            self._session = session
            self._principal = self._session.open(liga + '/formacoes').read()
        # else if called without AluraLogin, create its own session
        else:
            session = mechanize.Browser()
            self._principal = session.open(liga + '/formacoes').read()
        # properties to save time next time it uses again
        self._categories = None
        self._category = None
        self._formations = None

    def title_scrapper(self, links):
        titles = []
        modules = []
        i = 0
        for link in links:
            req = self._session.open(link)
            soup = BeautifulSoup(req, 'html.parser')
            title = soup.find_all('span', class_='task-body-header-title-text')[0].string.strip()
            module = soup.find_all('option', selected=True)[0].string
            module = re.sub('^\d+. ', '', module)
            titles.append(title)
            if f'{i} - {module}' not in modules:
                i+= 1
            modules.append(f'{i} - {module}')

        with open('output-titles.txt', 'w', encoding='utf-8') as f:
            i = 1
            for item in titles:
                f.write(f'{modules[i-1]}**{i} - {item}\n')
                print(f'{modules[i-1]} {i} - {item}\n')
                i += 1

    # Scrap formations videos from json requests and save to data.txt
    def formation_scraper(self, links):
        result = []
        for link in links:
            #print(link + '/video')
            req = self._session.open(link + '/video').read()
            result.append(req)
        try:
            os.remove('data.txt')
        except OSError:
            pass
        with open('data.txt', 'w') as f:
            for item in result:
                f.write(f'{item}\n')
        print('Done! Saved in data.txt')

    # Scrap categories and formations from the site
    def _text_scraper(self, tag='li', category=None):
        classes = ['formacoes__item', 'formacao__link']
        links = []
        soup = BeautifulSoup(self._principal, 'html.parser')
        if category is None:
            for a in soup.find_all(tag, class_=classes[0]):
                links.append(a['id'])
        else:
            li = soup.find('li', id=category, recursive=True)
            for i in li.findChildren('a', class_=classes[1]):
                links.append(i['href'])
        return links

    # saves categories and formations to the properties
    def formation_categories(self):
        if not self.categories:
            self.categories = self._text_scraper()
        if not self.category:
            self.category = _listing(self.categories)
        if not self.formations:
            self.formations = self._text_scraper(category=self.category)

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def formations(self):
        return self._formations

    @formations.setter
    def formations(self, value):
        self._formations = value


# Crawls all video links from a formation
class AluraCrawler(AluraScraper):
    def __init__(self, session=None):
        self._session = session
        super().__init__(self._session)
        self._link = None
        self._links = None

    # Choose formation using href tag list from alura page
    def choose_formation(self, formacoes):
        formacao = _listing(formacoes)
        print(formacao + '  escolhida...')
        self.link = ['https://cursos.alura.com.br' + formacao]

    # Crawls every link that has video from a formation
    def formation_crawler(self, lst=None, aux=0):
        if not lst:
            lst = self.link
        classes = ['learning-content__link', 'courseSectionList-section', 'task-menu-nav-item-link-VIDEO']
        links = []
        for link in lst:
            req = self._session.open(link).read()
            links.extend(self.__link_crawler(classes, req, aux))
            print(links)
        if aux < 2:
            return self.formation_crawler(lst=links, aux=aux + 1)
        self.links = links

    # submethod for formation_crawler
    @staticmethod
    def __link_crawler(classes, req, aux=0):
        links = []
        soup = BeautifulSoup(req, 'html.parser')
        for a in soup.find_all('a', class_=classes[aux]):
            if a['href'].startswith('/'):
                print(a['href'])
                links.append(liga + a['href'])
        return links

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, value):
        self._links = value


# Login to Alura
class AluraLogin(AluraCrawler):
    def __init__(self, user, password):
        cj = CookieJar()
        self._session = mechanize.Browser()
        self._session.set_handle_robots(False)
        self._session.set_cookiejar(cj)
        self._session.open("https://cursos.alura.com.br/loginForm")
        self._session.select_form(nr=1)
        self._session.form['username'] = user
        self._session.form['password'] = password
        self._session.submit()
        super().__init__(self._session)
