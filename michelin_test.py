from michelin_init import *
import unittest
import sqlite3

DBNAME = 'michelin.db'
class Michelin(unittest.TestCase):
    def test_url(self):
        url_list = crawling_to_stars_page('chicago', 1)
        url_correct = "https://guide.michelin.com/us/chicago/1-star-michelin/restaurants?max=30&sort=relevance&order=desc"
        self.assertEqual(url_list[0], url_correct)

        url2_list = crawling_to_stars_page('san-francisco', 3)
        url2_correct = "https://guide.michelin.com/us/san-francisco/3-stars-michelin/restaurants?max=30&sort=relevance&order=desc"
        self.assertEqual(url2_list[0], url2_correct)

        url3_list = crawling_to_stars_page('washington-dc', 3)
        url3_correct = []
        self.assertEqual(url3_list, url3_correct)

    def test_rest_list(self):
        rest_list1 = scrape_rest_info('san-francisco', 2)
        self.assertEqual(len(rest_list1), 7)
        rest_list2 = scrape_rest_info('washington-dc', 1)
        self.assertEqual(len(rest_list2), 11)

    def test_rest_object(self):
        rest_list = scrape_rest_info('chicago', 1)
        obj = rest_list[0]
        self.assertEqual(obj.name, 'Band of Bohemia')
        self.assertEqual(obj.city, 'chicago')
        self.assertEqual(obj.distinction, 1)
        self.assertEqual(obj.cuisine, 'Gastropub')
        self.assertEqual(obj.price, 25.0)

    def test_google_rating(self):
        rest_list = scrape_rest_info('chicago', 1)
        obj1 = rest_list[0]
        obj2 = rest_list[10]
        google_place_for_rest(obj1)
        google_place_for_rest(obj2)
        self.assertEqual(obj1.rating, 4.6)
        self.assertEqual(obj2.rating, 4.4)

    def test_database(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        statement = """
            SELECT Name, [$Price >], Rating
            FROM Restaurants
            WHERE City='Washington DC'
        """
        cur.execute(statement)
        name_list = []
        price_list = []
        rating_list = []
        for row in cur:
            name_list.append(row[0])
            price_list.append(row[1])
            rating_list.append(row[2])

        self.assertEqual(name_list[0], 'Blue Duck Tavern')
        self.assertEqual(price_list[3], 75.0)
        self.assertEqual(rating_list[2], 4.7)







if __name__ == '__main__':
    unittest.main()
