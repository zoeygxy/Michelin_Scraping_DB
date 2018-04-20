import requests
import json
import sqlite3
from bs4 import BeautifulSoup
from secrets import *


GOOGLE_API_KEY = google_places_key
DBNAME = 'michelin.db'
# class definition
class Restaurant:
    def __init__(self, name=''):
        self.name = name
        self.city = ''
        self.distinction = 0
        self.cuisine = ''
        self.price = 0
        self.rating = 0
        self.address = ""

    def set_info(self, city, distinction, cuisine, price, rating=None):
        self.name = name
        self.city = city
        self.distinction = distinction
        self.cuisine = cuisine
        self.price = price
        if yelp is not None:
            self.yelp = yelp

    def __str__(self):
        string = "name= " + self.name + ", city= " + self.city + ", distinction= " +\
                 str(self.distinction) + ", cuisine= " + self.cuisine + ", price= " + str(self.price)
        return string

# Helper Functions
def make_unique_ident(url, params):
    if params == None:
        return url
    else:
        alphabetized_keys = sorted(params.keys())
        res = []
        for k in alphabetized_keys:
            res.append("{}={}".format(k, params[k]))
        return url + "&".join(res)

def make_request_using_cache(url, CACHE_DICT, params=None):
    unique_ident = make_unique_ident(url, params)
    if unique_ident in CACHE_DICT:
        print('Getting Cached Data...')
        pass

    else:
        print('Making a request for new data...')
        resp = requests.get(url, params=params)
        CACHE_DICT[unique_ident] = resp.text
        fw = open('cache_data.json', 'w')
        fw.write(json.dumps(CACHE_DICT))
        fw.close()

#####################################
###### Crawling Michelin Guide ######
#####################################

# param: string of city name: 'chicago', 'washington-dc',
# 'new-york' or 'san-francisco'
# return: nothing
def get_page_for_city(city):
    base_url = "https://guide.michelin.com/"
    city_url = "https://guide.michelin.com/us/{}/restaurants".format(city)

    # Try open cache File
    try:
        fr = open('cache_data.json', 'r')
        data = fr.read()
        CACHE_DICT = json.loads(data)
        fr.close()
    except:
        CACHE_DICT = {}

    # Check Cache; if info not in it, update cache
    make_request_using_cache(city_url, CACHE_DICT, params=None)

    return CACHE_DICT

#############################
def crawling_to_stars_page(city, stars):
    CACHE_DICT = get_page_for_city(city)
    base_url = "https://guide.michelin.com"
    city_url = "https://guide.michelin.com/us/{}/restaurants".format(city)

    url_list = []
    # Look for the city page we want
    city_ident = make_unique_ident(city_url, None)
    city_html = CACHE_DICT[city_ident]
    city_soup = BeautifulSoup(city_html, "html.parser")
    distinction = city_soup.find_all(class_='restaurants-awards-list')
    check_box = distinction[0].find_all(class_='checkbox grid-restaurants-filter__checkbox')
    label = check_box[0].find('label')

    for i in check_box:
        label = i.find('label')
        try:
            web_star = int(label.text.split()[0])
            if web_star == stars:
                star_exten = i.find('input')['data-url']
                star_url = base_url + star_exten
                url_list.append(star_url)
                break
        except:
            pass

    # If there are more than one pages
    if (len(url_list) > 0):
        has_next_page = True
        while has_next_page and star_url:
            city_star_ident = make_unique_ident(star_url, None)
            make_request_using_cache(star_url, CACHE_DICT)
            city_star_html = CACHE_DICT[city_star_ident]
            city_star_soup = BeautifulSoup(city_star_html, "html.parser")
            pages_section = city_star_soup.find_all(class_='page-arrow')
            if len(pages_section) == 2:
                try:
                    star_url = base_url + pages_section[1]['href']
                    url_list.append(star_url)
                except:
                    has_next_page = False
            else:
                has_next_page = False

    return url_list


#############################################
def scrape_rest_info(city, stars):
    scrape_url_list = crawling_to_stars_page(city, stars);
    restaurant_list = []
    for scrape_url in scrape_url_list:
        print('scraping: ' + city + ' ' + str(stars) + '\n' + scrape_url + '\n')
        if scrape_url == 'None':
            break
        else:
            # Try open cache File
            try:
                fr = open('cache_data.json', 'r')
                data = fr.read()
                CACHE_DICT = json.loads(data)
                fr.close()
            except:
                CACHE_DICT = {}

            # Check Cache; if info not in it, update cache
            make_request_using_cache(scrape_url, CACHE_DICT, params=None)

            # Look for the scrape page we want
            scrape_ident = make_unique_ident(scrape_url, None)
            scrape_html = CACHE_DICT[scrape_ident]
            scrape_soup = BeautifulSoup(scrape_html, "html.parser")
            rests = scrape_soup.find_all(class_="grid-restaurants-new_right_item nested-link")
            for r in rests:
                # get name
                name_content = r.find(class_='resto-inner-title').text
                name_list = name_content.split()
                name = name_list[0]
                for w in name_list[1:]:
                    if len(w) > 1 or w == "A":
                        name += ' ' + w
                restaurant = Restaurant(name)
                # get city
                restaurant.city = city
                # get cuisine
                detail_content = r.find(class_='resto-inner-category').text
                detail_list = detail_content.split()
                restaurant.cuisine = detail_list[0]
                # get distinction
                restaurant.distinction = stars
                # get price
                restaurant.price = float(detail_list[-1].strip('$'))
                restaurant_list.append(restaurant)
    return restaurant_list


####### GOOGLE PLACES API ########
def google_place_for_rest(rest_object):
    CACHE_DICT = {}
    # Try open cache File
    try:
        fr = open('cache_data.json', 'r')
        data = fr.read()
        CACHE_DICT = json.loads(data)
        fr.close()
    except:
        CACHE_DICT = {}

    # Google text search
    # Check Cache; if info not in it, update cache
    text_search_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    params1 = {'query':rest_object.name+' '+rest_object.city + ' ' + 'restaurant',
               'key': GOOGLE_API_KEY}

    make_request_using_cache(text_search_url, CACHE_DICT, params1)
    unique_ident = make_unique_ident(text_search_url, params1)
    place_content = json.loads(CACHE_DICT[unique_ident])
    try:
        rest_object.rating = place_content['results'][0]['rating']
    except:
        print(place_content)

    rest_object.address = place_content['results'][0]['formatted_address']


####### DATA BASE ###########
def create_database():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # DROP Table
    statement = """
        DROP TABLE IF EXISTS 'Restaurants'
    """
    cur.execute(statement)
    conn.commit()

    # Create the table 'Restaurants'
    statement = """
        CREATE TABLE 'Restaurants' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'Distinction' TEXT NOT NULL,
            'City' TEXT NOT NULL,
            'Cuisine Type' TEXT NOT NULL,
            '$Price >' FLOAT NOT NULL,
            'Rating' FLOAT,
            'Address' TEXT);
    """
    cur.execute(statement)
    conn.commit()

def init_db(rest_obj_list):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    city_dict = {'chicago' : 'Chicago', 'new-york' : 'New York City',
                      'washington-dc' : 'Washington DC',
                      'san-francisco' : 'San Francisco'}
    distinction_dict = {1 : '1 Star MICHELIN', 2 : '2 Stars MICHELIN',
                        3 : '3 Stars MICHELIN'}

    for r in rest_obj_list:
        insertion = (None, r.name, distinction_dict[r.distinction], city_dict[r.city], r.cuisine,
                    r.price, r.rating, r.address)
        statement = 'INSERT INTO "Restaurants"'
        statement += 'VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

def init_second_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # Drop and initilize table
    statement = """
        DROP TABLE IF EXISTS 'Cities'
    """
    cur.execute(statement)
    conn.commit()

    statement = """
        DROP TABLE IF EXISTS 'Cuisine_Types'
    """
    cur.execute(statement)
    conn.commit()

    statement = """
        CREATE TABLE 'Cities' (
            'City' TEXT NOT NULL,
            'Total' INTEGER NOT NULL,
            'Avg Rating' FLOAT NOT NULL,
            '1 Star Count' INTEGER NOT NULL,
            '2 Star Count' INTEGER NOT NULL,
            '3 Star Count' INTEGER NOT NULL);
    """
    cur.execute(statement)
    conn.commit()
    # fill in the table
    city_detail = {}
    statement = """
        SELECT City, COUNT(*), AVG(Rating)
        FROM Restaurants
        GROUP BY City
    """
    cur.execute(statement)
    for row in cur:
        city_detail[row[0]] = [row[1], round(row[2], 3)]

    statement = """
        SELECT City, Distinction, COUNT(*)
        FROM Restaurants
        GROUP BY City, Distinction
        ORDER BY Distinction
    """
    cur.execute(statement)
    temp_dict = {}
    #print(city_detail)
    for row in cur:
        city_detail[row[0]].append(row[2])


    # insert into the table
    for city in city_detail:
        try:
            insertion = (city, city_detail[city][0], city_detail[city][1],
                     city_detail[city][2], city_detail[city][3],
                     city_detail[city][4])
            statement = 'INSERT INTO "Cities"'
            statement += 'VALUES(?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
        except:
            insertion = (city, city_detail[city][0], city_detail[city][1],
                     city_detail[city][2], city_detail[city][3],
                     0)
            statement = 'INSERT INTO "Cities"'
            statement += 'VALUES(?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
    conn.commit()
    print('Tables initialized successfully.')

def prepare_database():
    city_list = ['chicago', 'washington-dc', 'san-francisco', 'new-york']
    stars_list = [1, 2, 3]
    rest_obj_list = []
    for c in city_list:
        for s in stars_list:
            city_star_list = scrape_rest_info(c, s)
            if len(city_star_list) != 0:
                for i in city_star_list:
                    google_place_for_rest(i)
                    print('Place name: '+ i.name + '\n')
                rest_obj_list.extend(city_star_list)
    create_database()
    init_db(rest_obj_list)
    print('Data imported successfully.')

if __name__ == '__main__':
    prepare_database()
    init_second_table()
