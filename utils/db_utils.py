import random
import sqlite3
import sys

MEAL_INFO_DB = 'meal_info.db'

# List of meals to insert in db
# Format is name, servings, ingredients, cuisine, protein, level of difficulty
# TODO: Fill out meal details
meals = [
    ("chicken and rice", 1, "chicken, rice", None, "chicken", 1),
    ("biscuits and gravy", 1.5, "breakfast sausage, biscuits, country gravy, eggs", "breakfast", "breakfast sausage", 1),
    ("chilli", 4, None, None, None, None),
    ("buffalo chicken", 2, None, None, None, None),
    ("brown butter gnocchi", 1, None, None, None, None),
    ("pretzels", 1, None, None, None, None),
    ("chicken parm", 4, None, None, None, None),
    ("nachos", 3, None, None, None, None),
    ("enchiladas", 4, None, None, None, None),
    ("pesto pasta", 3, None, None, None, None),
    ("fish tacos", 1, None, None, None, None),
    ("subs", 2, None, None, None, None),
    ("gordon ramsey lamb", 1, None, None, None, None),
    ("burgers", 1, None, None, None, None),
    ("veggie pasta", 3, None, None, None, None),
    ("shrimp tacos", 1, None, None, None, None),
    ("steaks", 1, None, None, None, None),
    ("grilled chicken salad", 2, None, None, None, None),
    ("stuffed peppers", 2, None, None, None, None),
    ("twice baked potatoes", 2, None, None, None, None),
    ("swedish meatballs", 4, None, None, None, None),
    ("crepes", 2, None, None, None, None),
    ("beef burritos", 1.5, None, None, None, None),
    ("chicken fajitas", 1.5, None, None, None, None),
    ("sesame noodles", 3, None, None, None, None),
    ("quesadilla", 3, None, None, None, None),
    ("pigs in a blanket", 1, None, None, None, None),
    ("chicken sandwich", 1, None, None, None, None),
    ("pasta milano", 3.5, None, None, None, None),
    ("fettucine alfredo", 3, None, None, None, None),
    ("sausages", 1, None, None, None, None),
    ("pasta carbonara", 2, None, None, None, None),
    ("sos", 1.5, None, None, None, None),
    ("chicken fried steak", 2, None, None, None, None),
    ("pizza", 2.5, None, None, None, None),
    ("mac and cheese", 3, None, None, None, None),
    ("lasagna", 4, None, None, None, None),
    ("blt", 1, None, None, None, None),
    ("pork chops", 1, None, None, None, None),
    ("pork sliders", 1, None, None, None, None),
    ("prtip tacos", 3, None, None, None, None),
    ("spaghetti and meatballs", 4, None, None, None, None),
    ("meatball subs", 3, None, None, None, None),
    ("caprese", 1, None, None, None, None),
    ("ziti", 4, None, None, None, None),
    ("philly cheesesteak", 2, None, None, None, None)
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
