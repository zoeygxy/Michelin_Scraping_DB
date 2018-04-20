from michelin_init import *
import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3

DBNAME = 'michelin.db'

# Generate Graph 1
def generate_city_star_avg_rating(num):
    option = {1:"Chicago", 2:"New York City", 3:"San Francisco", 4:"Washington DC"}
    city_name = option[num]
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = """
        SELECT City, Distinction, AVG(Rating)
        FROM Restaurants
		GROUP BY City, Distinction
		ORDER BY CIty, Distinction
    """
    cur.execute(statement)
    avg_ratings = []
    for row in cur:
        if (row[0] == city_name):
            avg_ratings.append(round(row[2], 3))

    if len(avg_ratings) == 2:
        distinctions = ['1 Star', '2 Stars']
    else:
        distinctions = ['1 Star', '2 Stars', '3 Stars']

    trace1 = go.Bar(
        x = distinctions,
        y = avg_ratings,
        name = 'Average',
        marker = dict(
            color = 'red'
        ),
    )

    data = [trace1]
    layout = go.Layout(
        title = 'Average Ratings of Different Distinctions in {}'.format(city_name),
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='bar-direct-labels')

# Generate Graph2
def generate_cities_counts():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = """
        SELECT City, [1 Star Count], [2 Star Count], [3 Star Count]
        FROM Cities
    """
    cur.execute(statement)
    star1 = []
    star2 = []
    star3 = []
    for row in cur:
        star1.append(row[1])
        star2.append(row[2])
        star3.append(row[3])


    cities = ["Chicago", "New York City", "San Francisco", "Washington DC"]
    trace1 = go.Bar(
        x = cities,
        y = star1,
        name='1 Star Restaurants',
        marker=dict(
            color='blue',
        ),
    )
    trace2 = go.Bar(
        x = cities,
        y = star2,
        name='2 Star Restaurants',
        marker=dict(
            color='red',
        ),
    )

    trace3 = go.Bar(
        x = cities,
        y = star3,
        name='3 Star Restaurants',
        marker=dict(
            color='purple',
        ),
    )

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title = 'Restaurant Count by Distinction and Cities',
        barmode = 'group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='grouped-bar')

# Generate Graph 3
def generate_scatter_sheet():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = """
        SELECT [Cuisine Type], AVG(Rating)
        FROM Restaurants
        GROUP BY [Cuisine Type]
        ORDER BY [Cuisine Type]
    """
    cur.execute(statement)
    type_list = []
    for row in cur:
        type_list.append(row[0])

    x_chicago = []
    for i in type_list:
        statement = """
            SELECT AVG(Rating)
            FROM Restaurants
            WHERE City='Chicago'
            GROUP BY [Cuisine Type]
            HAVING [Cuisine Type] = ?
        """
        params = (i,)
        cur.execute(statement, params)
        count = 0
        for row in cur:
            avg_rating = round(row[0], 3)
            count += 1
        if count == 0 :
            x_chicago.append(0)
        else:
            x_chicago.append(avg_rating)

    x_nyc = []
    for i in type_list:
        statement = """
            SELECT AVG(Rating)
            FROM Restaurants
            WHERE City='New York City'
            GROUP BY [Cuisine Type]
            HAVING [Cuisine Type] = ?
        """
        params = (i,)
        cur.execute(statement, params)
        count = 0
        for row in cur:
            avg_rating = round(row[0], 3)
            count += 1
        if count == 0 :
            x_nyc.append(0)
        else:
            x_nyc.append(avg_rating)

    x_sf = []
    for i in type_list:
        statement = """
            SELECT AVG(Rating)
            FROM Restaurants
            WHERE City='San Francisco'
            GROUP BY [Cuisine Type]
            HAVING [Cuisine Type] = ?
        """
        params = (i,)
        cur.execute(statement, params)
        count = 0
        for row in cur:
            avg_rating = round(row[0], 3)
            count += 1
        if count == 0 :
            x_sf.append(0)
        else:
            x_sf.append(avg_rating)


    x_dc = []
    for i in type_list:
        statement = """
            SELECT AVG(Rating)
            FROM Restaurants
            WHERE City='Washington DC'
            GROUP BY [Cuisine Type]
            HAVING [Cuisine Type] = ?
        """
        params = (i,)
        cur.execute(statement, params)
        count = 0
        for row in cur:
            avg_rating = round(row[0], 3)
            count += 1
        if count == 0 :
            x_dc.append(0)
        else:
            x_dc.append(avg_rating)

    trace1 = {"x": x_chicago,
          "y": type_list,
          "marker": {"color": "pink", "size": 12},
          "mode": "markers",
          "name": "Chicago",
          "type": "scatter"}

    trace2 = {"x": x_nyc,
          "y": type_list,
          "marker": {"color": "blue", "size": 12},
          "mode": "markers",
          "name": "New York City",
          "type": "scatter"}

    trace3 = {"x": x_sf,
          "y": type_list,
          "marker": {"color": "red", "size": 12},
          "mode": "markers",
          "name": "San Francisco",
          "type": "scatter"}

    trace4 = {"x": x_dc,
          "y": type_list,
          "marker": {"color": "green", "size": 12},
          "mode": "markers",
          "name": "Washington DC",
          "type": "scatter"}


    data = go.Data([trace1, trace2, trace3, trace4])
    layout = {"title": "Cuisine in Different Cities",
          "xaxis": {"title": "Average Rating (out of 5)", },
          "yaxis": {"title": "Cuisine Types"}}
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filenmae='basic_dot-plot')

# Generate Graph 4
def generat_price_chart():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    distinction_list = ['1 Star MICHELIN', '2 Stars MICHELIN', '3 Stars MICHELIN']

    distinction_price = {}
    for i in distinction_list:
        statement = """
            SELECT [$Price >], COUNT(*)
            FROM Restaurants
            WHERE Distinction=?
            GROUP BY [$Price >]
            ORDER BY Distinction
        """
        params = (i,)
        cur.execute(statement, params)
        distinction_price[i] = {}
        for row in cur:
            distinction_price[i][row[0]] = row[1]
    #print(distinction_price)
    price1 = []
    price2 = []
    price3 = []

    for key in distinction_price:
        if 25.0 in distinction_price[key]:
            price1.append(distinction_price[key][25.0])
        else:
            price1.append(0)
        if 50.0 in distinction_price[key]:
            price2.append(distinction_price[key][50.0])
        else:
            price2.append(0)
        if 75.0 in distinction_price[key]:
            price3.append(distinction_price[key][75.0])
        else:
            price3.append(0)

    trace1 = go.Bar(
        x = distinction_list,
        y = price1,
        name=' > $25',
        marker=dict(
            color='purple',
        ),
    )

    trace2 = go.Bar(
        x = distinction_list,
        y = price2,
        name=' > $50',
        marker=dict(
            color='red',
        ),
    )

    trace3 = go.Bar(
        x = distinction_list,
        y = price3,
        name=' > $75',
        marker=dict(
            color='pink',
        ),
    )

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title = 'Price Counts for Different Stars',
        barmode = 'group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='price')


if __name__ == '__main__':
    intro_str = "Welcome to the North America Michelin Guide Graphing!\n"
    intro_str += "Graphing Options:\n"
    intro_str += "1. The average rating of different stars in a chosen city\n"
    intro_str += "2. The distribution of star resturants in the city\n"
    intro_str += "3. The average ratings of different cuisine types\n"
    intro_str += "4. Distribution of prices among different distinctions\n"

    valid = True
    while valid == True:
        print(intro_str)
        print("Please choose the No. of graph to present!\nType 'exit' to end the program")
        option = input()
        if option == '1':
            prompt_str = 'Choose a number! 1. Chicago   2. New York City  '
            prompt_str += '3. San Francisco    4. Washington DC\n'
            city = input(prompt_str)
            generate_city_star_avg_rating(int(city))
        elif option == '2':
            generate_cities_counts()
        elif option == '3':
            generate_scatter_sheet()
        elif option == '4':
            generat_price_chart()
        elif option == 'exit':
            print('Goodbye!')
            valid = False
        else:
            print('Input not recognized. Try Again.')
