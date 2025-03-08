import random
import sqlite3
import sys

MEAL_INFO_DB = 'meal_info.db'

# List of meals to insert in db
# Format is name, servings, ingredients, cuisine, protein, level of difficulty (on a scale of 1-5)
# TODO: Fill out meal details
meals = [
    ("chicken and rice", 1, "chicken, rice", "american", "chicken", 1),
    ("biscuits and gravy", 1.5, "breakfast sausage, biscuits, country gravy, eggs", "breakfast", "breakfast sausage", 1),
    ("chilli", 4, None, "american", "beef", 2),
    ("buffalo chicken", 2, None, "american", "chicken", 2),
    ("brown butter gnocchi", 1, None, "pasta", "none", 1),
    ("pretzels", 1, None, None, "none", 5),
    ("chicken parm", 4, None, "pasta", "chicken", 3),
    ("nachos", 3, None, "american", "beef", 3),
    ("buffalo chicken nachos", 3, None, "american", "chicken", 3),
    ("enchiladas", 4, None, "texmex", "chicken", 3),
    ("pesto pasta", 3, None, "pasta", "none", 4),
    ("fish tacos", 1, None, "texmex", "fish", 2),
    ("subs", 2, None, "sandwich", "lunch meat", 1),
    ("gordon ramsey lamb", 1, None, "fancy", "lamb", 3),
    ("burgers", 1, None, "american", "beef", 1),
    ("veggie pasta", 3, None, "pasta", "chicken", 3),
    ("shrimp tacos", 1, None, "texmex", "shrimp", 1),
    ("steaks", 1, None, "american", "beef", 1),
    ("grilled chicken salad", 2, None, "salad", "chicken", 1),
    ("stuffed peppers", 2, None, "texmex", "beef", 3),
    ("twice baked potatoes", 2, None, "american", "bacon", 3),
    ("swedish meatballs", 4, None, "pasta", "beef", 3),
    ("crepes", 2, None, "french", "chicken", 4),
    ("beef burritos", 1.5, None, "texmex", "beef", 1),
    ("chicken fajitas", 1.5, None, "texmex", "chicken", 1),
    ("sesame noodles", 3, None, "asian", "pork", 3),
    ("quesadilla", 3, None, "texmex", "chicken", 4),
    ("quesadilla", 3, None, "texmex", "steak", 4),
    ("pigs in a blanket", 1, None, "american", "hot dog", 2),
    ("chicken sandwich", 1, None, "sandwich", "chicken", 1),
    ("pasta milano", 3.5, None, "pasta", "chicken", 4),
    ("fettucine alfredo", 3, None, "pasta", "chicken", 3),
    ("sausages", 1, None, "american", "sausage", 1),
    ("pasta carbonara", 2, None, "pasta", "bacon", 3),
    ("sos", 1.5, None, "breakfast", "beef", 1),
    ("chicken fried steak", 2, None, "breakfast", "beef", 3),
    ("pizza", 2.5, None, "pizza", "sausage", 5),
    ("pizza", 2.5, None, "pizza", "pepperoni", 5),
    ("pizza", 2.5, None, "pizza", "none", 5),
    ("pizza", 2.5, None, "pizza", "chicken", 5),
    ("mac and cheese", 3, None, "pasta", "none", 3),
    ("lasagna", 4, None, "pasta", "beef", 4),
    ("blt", 1, None, "sandwich", "bacon", 1),
    ("pork chops", 1, None, "american", "pork", 2),
    ("pork sliders", 1, None, "american", "pork", 3),
    ("tritip tacos", 3, None, "texmex", "beef", 4),
    ("spaghetti and meatballs", 4, None, "pasta", "beef", 3),
    ("meatball subs", 3, None, "sandwich", "beef", 3),
    ("caprese", 1, None, "italian", "none", 1),
    ("ziti", 4, None, "pasta", "none", 2),
    ("philly cheesesteak", 2, None, "sandwich", "beef", 2)
]


def create_dinner_db():
    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()

    # Create a table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dinners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        servings_in_days FLOAT NOT NULL,
        ingredients TEXT,
        type_of_cuisine TEXT,
        protein TEXT,
        level_of_difficulty INTEGER)
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


def insert_meal_data():

    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()

    # Insert meals
    cursor.executemany('''
    INSERT INTO dinners (name, servings_in_days, ingredients, type_of_cuisine, protein, level_of_difficulty) VALUES (?, ?, ?, ?, ?, ?)
    ''', meals)

    conn.commit()
    conn.close()


# Retrieve all or specified number of random meals from the db
def get_dinners(num=None):
    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()

    if num:
        cursor.execute(f"SELECT * FROM dinners ORDER BY RANDOM() LIMIT {num}")
    else:
        cursor.execute("SELECT * FROM dinners")
    dinners = cursor.fetchall()

    conn.close()
    return dinners


# Returns 1 dinner with servings between input and input+0.5, inclusive
# For example, if 1.5 was passed in, the dinner returned would have 1.5 <= servings <=2
def get_dinner_by_servings(num_servings):
    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ROWID) FROM dinners WHERE servings_in_days >= ? AND servings_in_days <= ?",
                   (num_servings, num_servings+0.5,))
    max_rowid = cursor.fetchone()[0]
    if max_rowid is None:
        print("error")
        sys.exit(1)
    random_rowid = random.randint(0, max_rowid)
    dinner = None
    while not dinner:
        cursor.execute("SELECT * FROM dinners WHERE servings_in_days >= ? AND servings_in_days <= ? LIMIT 1 OFFSET ?",
                       (num_servings, num_servings+0.5, random_rowid,))
        dinner = cursor.fetchone()
        random_rowid = (random_rowid % max_rowid) + 1
    print(f"found dinner {dinner}")
    conn.close()
    return dinner


# Returns 1 dinner with servings <= input max servings
def get_dinner_by_max_servings(max_servings):
    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ROWID) FROM dinners WHERE servings_in_days <= ?", (max_servings,))
    max_rowid = cursor.fetchone()
    if max_rowid is None:
        print("error")
    else:
        max_rowid = max_rowid[0]
    random_rowid = random.randint(0, max_rowid)
    dinner = None
    while not dinner:
        cursor.execute("SELECT * FROM dinners WHERE servings_in_days <= ? LIMIT 1 OFFSET ?",
                   (max_servings, random_rowid,))
        random_rowid = (random_rowid % max_rowid) + 1
        dinner = cursor.fetchone()
    print(f"found dinner {dinner}")
    conn.close()
    return dinner


# Get all dinners with listed parameter
# For ex. If input protein, chicken, returns all dinners that use chicken as the protein
def get_dinners_by_attribute(attribute, value):
    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()
    query = f"SELECT * FROM dinners WHERE {attribute.lower()} = '{value.lower()}'"
    cursor.execute(query)
    dinners = cursor.fetchall()
    conn.close()
    return dinners


# Get all dinners excluding listed parameter
# For ex. If input protein, chicken, returns all dinners that do not use chicken as the protein
def get_dinners_by_not_parameter(attribute, value):
    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()
    query = f"SELECT * FROM dinners WHERE {attribute.lower()} != '{value.lower()}'"
    cursor.execute(query)
    dinners = cursor.fetchall()
    conn.close()
    return dinners


def general_query():
    # TODO: Add logic to query based on unspecified number of input attributes and values
    tmp = 1


def insert_new_meal():
    # TODO: Take input from user and input into db
    tmp = 1
