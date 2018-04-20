######  Michelin Guide  ######

Introduction:
This python program aims to provide the users with a guide for Michelin Star Restaurants in the United States. The information that can be fetched from the program include the distribution of Michelin Restaurants in different cities, the list of restaurants, the price, the ratings etc.
The data will be stored and presented in database and plotly graphs.

Usage:
1. Set up virutal environment according to requirements.txt
2. Initialize a file named "secrets.py" and put in the line below:
                google_places_key = [your key]
3. Run the file "michelin_init.py" to intialize the database
4. Run the file "michelin_visual.py" to get the statistical graphs with plotly.

Main Structure:
1. [michelin_init.py] crawls michelin guide webpage(https://guide.michelin.com/us/chicago etc.), gets ratings from Google Places API, and initializes the database.
1) prepare_database():
    contains [scape_rest_info()] that crawls all the related Michelin Guide Websites and get the price, cuisine type etc.
    contains [google_place_for_rest()] that gets rating for each restaurant through Google Place API.
2) init_second_table(): initialize the city table from the information in the first database.

2. [michelin_visual.py] processes the data from the database, and plot with plotly.
3. [cache_data.json] stores cached data, and michelin.db stores restaurants info.


