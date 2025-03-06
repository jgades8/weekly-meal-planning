import random
import sqlite3


MEAL_INFO_DB = 'meal_info.db'

# List of meals to insert in db
# Format is name, servings, ingredients, cuisine, protein, level of difficulty
meals = [
    ("Chicken and Rice", 1, "chicken, rice", None, "chicken", 1),
    ("Biscuits and Gravy", 1.5, "breakfast sausage, biscuits, country gravy, eggs", "breakfast", "breakfast sausage", 1),
    ("Chilli", 4, None, None, None, None),
    ("Buffalo Chicken", 2, None, None, None, None),
    ("Brown Butter Gnocchi", 1, None, None, None, None),
    ("Pretzels", 1, None, None, None, None),
    ("Chicken Parm", 4, None, None, None, None),
    ("Nachos", 3, None, None, None, None),
    ("Enchiladas", 4, None, None, None, None),
    ("Pesto Pasta", 3, None, None, None, None),
    ("Fish Tacos", 1, None, None, None, None),
    ("Subs", 2, None, None, None, None),
    ("Gordon Ramsey Lamb", 1, None, None, None, None),
    ("Burgers", 1, None, None, None, None),
    ("Veggie Pasta", 3, None, None, None, None),
    ("Shrimp Tacos", 1, None, None, None, None),
    ("Steaks", 1, None, None, None, None),
    ("Grilled Chicken Salad", 2, None, None, None, None),
    ("Stuffed Peppers", 2, None, None, None, None),
    ("Twice Baked Potatoes", 2, None, None, None, None),
    ("Swedish Meatballs", 4, None, None, None, None),
    ("Crepes", 2, None, None, None, None),
    ("Beef Burritos", 1.5, None, None, None, None),
    ("Chicken Fajitas", 1.5, None, None, None, None),
    ("Sesame Noodles", 3, None, None, None, None),
    ("Quesadilla", 3, None, None, None, None),
    ("Pigs in a Blanket", 1, None, None, None, None),
    ("Chicken Sandwich", 1, None, None, None, None),
    ("Pasta Milano", 3.5, None, None, None, None),
    ("Fettucine Alfredo", 3, None, None, None, None),
    ("Sausages", 1, None, None, None, None),
    ("Pasta Carbonara", 2, None, None, None, None),
    ("SOS", 1.5, None, None, None, None),
    ("Chicken Fried Steak", 2, None, None, None, None),
    ("Pizza", 2.5, None, None, None, None),
    ("Mac and Cheese", 3, None, None, None, None),
    ("Lasagna", 4, None, None, None, None),
    ("BLT", 1, None, None, None, None),
    ("Pork Chops", 1, None, None, None, None),
    ("Pork Sliders", 1, None, None, None, None),
    ("Trtip Tacos", 3, None, None, None, None),
    ("Spaghetti and Meatballs", 4, None, None, None, None),
    ("Meatball Subs", 3, None, None, None, None),
    ("Caprese", 1, None, None, None, None),
    ("Ziti", 4, None, None, None, None),
    ("Philly Cheesesteak", 2, None, None, None, None)
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


def generate_random_offset(cursor):
    # cursor.execute("SELECT COUNT(*) FROM dinners")
    # total_rows = cursor.fetchone()[0]
    # random_offset = random.randint(0, total_rows-1)
    cursor.execute("SELECT MAX(ROWID) FROM dinners WHERE ")
    max_rowid = cursor.fetchone()
    if max_rowid is None:
        #throw error or something
        print("error")
    random_offset = random.randint(0, max_rowid)
    return random_offset


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


# Returns 1 dinner with servings <= input max servings
def get_dinner_by_servings(num_servings):
    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ROWID) FROM dinners WHERE servings_in_days >= ? AND servings_in_days <= ?",
                   (num_servings, num_servings+1,))
    max_rowid = cursor.fetchone()[0]
    if max_rowid is None:
        print("error")
    random_rowid = random.randint(0, max_rowid)
    dinner = None
    while not dinner:
        cursor.execute("SELECT * FROM dinners WHERE servings_in_days >= ? AND servings_in_days <= ? LIMIT 1 OFFSET ?",
                       (num_servings, num_servings+1, random_rowid,))
        dinner = cursor.fetchone()
        random_rowid = (random_rowid % max_rowid) + 1
    print(f"found dinner {dinner}")
    conn.close()
    return dinner


def get_dinner_by_max_servings(max_servings):
    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ROWID) FROM dinners WHERE servings_in_days <= ?", (max_servings,))
    max_rowid = cursor.fetchone()[0]
    if max_rowid is None:
        print("error")
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
    cursor.execute("SELECT * FROM dinners WHERE LOWER(?) = LOWER(?)", (attribute, value,))
    dinners = cursor.fetchall()
    conn.close()
    return dinners


# Get all dinners excluding listed parameter
# For ex. If input protein, chicken, returns all dinners that do not use chicken as the protein
def get_dinners_by_not_parameter(attribute, value):
    conn = sqlite3.connect(MEAL_INFO_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dinners WHERE ? != ?", (attribute, value,))
    dinners = cursor.fetchall()
    conn.close()
    return dinners


def general_query():
    # TODO: Add logic to query based on unspecified number of input attributes and values
    tmp = 1


def insert_new_meal():
    # TODO: Take input from user and input into db
    tmp = 1
