import pymysql

db = pymysql.connect(host="localhost",
                     user="root",
                     password="",
                     database="movies",
                     charset="utf8mb4",
                     cursorclass=pymysql.cursors.Cursor)

cursor = db.cursor()

print('Hi, welcome in the Movie Collection App!\n')

menu_text = """Select what you want to do:
l - See the full list of movies in the list
a - Add a new movie to the list
f - Find a movie in the list
q - Quit\n"""

menu_input = input(menu_text).lower()  # Asks user what to do


def add_movie():    # add movie function
    movie_title = input('Enter the title of the movie:\n').title()  # title variable
    movie_director = input(f'Enter the director of {movie_title}:\n').title()   # director variable
    movie_year = input(f'Enter the year of {movie_title}:\n')   # year variable

    print(f"""Movie '{movie_title}' directed by {movie_director} in {movie_year} was added to the collection successfully.\n""")    # Success message
    sql_create_query = """CREATE TABLE IF NOT EXISTS
    movie_list (id int PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR (256) NOT NULL,
            director VARCHAR (256) NOT NULL,
            year INT NOT NULL);"""
    sql_insert_query = f"""INSERT INTO movie_list (name, director, year)
               VALUES ('{movie_title}','{movie_director}','{movie_year}');"""
    try:
        cursor.execute(sql_create_query)

        cursor.execute(sql_insert_query)

        db.commit()
    except:
        db.rollback()


def show_movie_list():
    sql_select_query = """SELECT name, director, year FROM movie_list"""
    cursor.execute(sql_select_query)
    movie_list_sql = cursor.fetchall()
    i = 1
    print("Movie Collection: ")
    for movie in movie_list_sql:
        print(f"{i}. {movie[0]} -- {movie[1]} -- {movie[2]}")
        i += 1
    print('\n')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def find_movie():
    sql_select_query = """SELECT name, director, year FROM movie_list"""
    cursor.execute(sql_select_query)
    movie_list_sql = cursor.fetchall()
    input_find_text = """\nDo you want to find a movie using:
Name (n)
Director (d)
Year (y)
Go Back (b)\n"""
    user_find_input = input(input_find_text).lower()
    name_index = 0
    director_index = 0
    year_index = 0
    while user_find_input != 'b':
        if user_find_input == 'n':
            name_input = input("Search for: \n").title()
            for movie in movie_list_sql:
                if name_input not in movie[0]:
                    pass
                else:
                    print(f"{name_index+1}. {movie[0]} -- {movie[1]} -- {movie[2]}")
                    name_index += 1
            if name_index == 0:
                print("No item found")
            user_find_input = input(input_find_text).lower()
            name_index = 0

        elif user_find_input == 'd':
            director_input = input("Search for: \n").title()
            for movie in movie_list_sql:
                if director_input not in movie[1]:
                    pass
                else:
                    print(f"{director_index+1}. {movie[0]} -- {movie[1]} -- {movie[2]}")
                    director_index += 1
            if director_index == 0:
                print("No item found")
            user_find_input = input(input_find_text)
            director_index = 0

        elif user_find_input == 'y':
            year_input = str(input("Search for: \n"))
            for movie in movie_list_sql:
                if year_input not in str(movie[2]):
                    pass
                else:
                    print(f"{year_index+1}. {movie[0]} -- {movie[1]} -- {movie[2]}")
                    year_index += 1
            if year_index == 0:
                print("No item found")
            user_find_input = input(input_find_text)
            year_index = 0

        else:
            print('Unknown command. Please try again')
            user_find_input = input(input_find_text)


# main menu loop
while menu_input != 'q':     # quit option
    if menu_input == 'l':    # list option
        cursor.execute("""SELECT * FROM movie_list""")
        rows_number = len(cursor.fetchall())
        if rows_number == 0:  # check if collection is empty
            print('The collection of movies is currently empty.\n')
        else:
            show_movie_list()

        menu_input = input(menu_text).lower()
    elif menu_input == 'a':  # add option
        add_movie()
        menu_input = input(menu_text).lower()
    elif menu_input == 'f':  # find option
        find_movie()
        menu_input = input(menu_text).lower()
    else:
        print('Unknown command. Please try again')  # wrong command option
        menu_input = input(menu_text).lower()       # ask again

print('Thanks for using the Movie Collection App!')  # app end
