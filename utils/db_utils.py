import random
import sqlite3
import sys

MEAL_INFO_DB = 'meal_info.db'

# List of meals to insert in db
# Format is name, servings, ingredients, cuisine, protein, level of difficulty (on a scale of 1-5)
# ingredient store location options are: produce, deli, meat, bakery, dry goods, frozen, dairy
# TODO: Fill out meal details
# TODO: Maybe make a sides db for ingredients??
# meal ideas: chicken noodle soup, broccoli cheddar panera soup, fried rice
meals = [
    ("chicken and rice", 1, "chicken,1,meat; rice,1,dry goods", "american", "chicken", 1),
    ("biscuits and gravy", 1.5, "breakfast sausage,1,meat; biscuits,1,dairy; country gravy,1,dry goods; eggs,3,dairy", 
        "breakfast", "breakfast sausage", 1),
    ("chilli", 4, "beef,2,meat; chilli seasoning,2,dry goods; kidney beans,2,dry goods; diced tomatoes,2,dry goods; "
                  "white onion,1,produce", "american", "beef", 2), #TODO: Should I add cornbread ingredients? option to select maybe
    ("buffalo chicken", 2, "chicken,3,meat; hot sauce,1,dry goods; blue cheese crumbles,1,deli; cream cheese,1,dairy;"
                           " ranch seasoning,1,dry goods", "american", "chicken", 2),
    ("brown butter gnocchi", 1, "gnocchi,1,dry goods; thyme,1,produce; garlic,1,produce", "pasta", "none", 1),
    ("pretzels", 1, "yeast,1,dry goods; brown sugar,1,dry goods; flour,4,dry goods; baking soda,0.5,dry goods",
        "american", "none", 5),
    ("chicken parm", 4, "chicken,3,meat; spaghetti,1,dry goods; red sauce,1,dry goods; eggs,3,dairy; bread crumbs,2,dry goods;"
                        " mozzarella cheese,0.5,dairy; dinner bread,1,bakery", "pasta", "chicken", 3),
    ("nachos", 3, "chips,2,dry goods; cheddar cheese,1,dairy; olives,1,dry goods; beef,1,meat; salsa,1,dry goods; "
                  "jalapeno,1,produce; refried beans,1,dry goods", "american", "beef", 3),
    ("buffalo chicken nachos", 3, "chips,2,dry goods; chicken,1,meat; hot sauce,1,dry goods; mozzarella cheese,1,dairy",
        "american", "chicken", 3),
    ("enchiladas", 4, None, "texmex", "chicken", 3),
    ("pesto pasta", 3, None, "pasta", "none", 4),
    ("fish tacos", 1, "soft tacos,6,dry goods; white fish,1,meat; shredded cabbage,0.5,produce; chipotle aioli,0.5,"
                      "dry goods", "texmex", "fish", 2),
    ("subs", 2, "sub rolls,4,bakery; lunch meat,2,deli; roma tomatoes,2,produce; mayo,0.25,dry goods; shredded lettuce,"
                "0.5,produce; deli dressing,1,deli; pepper jack cheese slices,6,dairy", "sandwich", "lunch meat", 1),
    ("gordon ramsey lamb", 1, None, "fancy", "lamb", 3),
    ("burgers", 1, "beef,1,meat; burger rolls,2,dry goods; white onion,0.5,produce; tomato,1,produce", "american",
        "beef", 1),
    ("veggie pasta", 3, None, "pasta", "chicken", 3),
    ("shrimp tacos", 1, None, "texmex", "shrimp", 1),
    ("steaks", 1, None, "american", "beef", 1),
    ("grilled chicken salad", 2, "lettuce,1,produce; pepper,1,produce; cherry tomatoes,1,produce; tortilla strips,1,dry goods;"
                                 " chipotle ranch,0.25,dry goods", "salad", "chicken", 1),
    ("stuffed peppers", 2, None, "texmex", "beef", 3),
    ("twice baked potatoes", 2, None, "american", "bacon", 3),
    ("swedish meatballs", 4, None, "pasta", "beef", 3),
    ("crepes", 2, None, "french", "chicken", 4),
    ("beef burritos", 1.5, None, "texmex", "beef", 1),
    ("chicken fajitas", 1.5, None, "texmex", "chicken", 1),
    ("sesame noodles", 3, None, "asian", "pork", 3),
    ("quesadilla", 2.5, None, "texmex", "chicken", 4),
    ("quesadilla", 2.5, None, "texmex", "steak", 4),
    ("pigs in a blanket", 1, None, "american", "hot dog", 2),
    ("chicken sandwich", 1, None, "sandwich", "chicken", 1),
    ("pasta milano", 3.5, None, "pasta", "chicken", 4),
    ("fettuccine alfredo", 3, None, "pasta", "chicken", 3),
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
    ("philly cheesesteak", 2, None, "sandwich", "beef", 2),
    ("gnocchi with asparagus and miso butter", 1, "gnocchi,1,dry goods; asparagus,0.5,produce; shallot,1,produce; "
                                                  "garlic,3,produce; light miso,1,dry goods; parmigiano-reggiano,0.25,deli",
        "pasta", "none", 2),
    ("orange chicken", 2, "chicken thighs,4,meat; cornstarch,0.3,dry goods; vegetable oil,0.3,dry goods; orange,5,produce; "
                          "white vinegar,0.2.dry goods; brown sugar,0.3,dry goods; soy sauce,0.2,dry goods; garlic,2,produce; "
                          "ginger powder,0.25,dry goods",
        "asian", "chicken", 3),
    ("cavatelli with sausage, peppers, and oregano", 3, "noodles,1,dry goods; italian sausage,1,meat; yellow onion,"
                                                        "1,produce; bay leaf,1,dry goods; garlic,4,produce; tomato paste,"
                                                        "3,dry goods; chicken stock,0.5,dry goods; pepper,3,produce; "
                                                        "sherry vinegar,0.3,dry goods; heavy cream,0.5,dairy; "
                                                        "parmigiano-reggiano,0.25,deli",
        "pasta", "sausage", 3),
    ("grilled cheese", 1, "dinner bread,0.5,bakery; sharp cheddar cheese,0.5,dairy; tomato soup,2,dry goods", "sandwich",
        "none", 1),
    ("garganelli with vodka sauce", 2.5, "noodles,1,dry goods; shallot,1,produce; garlic,2,produce; red thai chile,1,produce; "
                                         "tomato paste,3,dry goods; vodka,0.25,liquor; heavy cream,0.75,dairy; "
                                         "parmigiano-reggiano,0.75,deli; basil,0.3,produce",
        "pasta", "none", 2),
    ("ravioli with vodka sauce", 1, "dinner bread,0.5,bakery; ravioli,2,dairy; vodka sauce,1,dry goods", "pasta", "none", 1),
    ("rice bowl", 1, "chicken,1,meat; rice,1,dry goods; black beans,1,dry goods, corn,1,dry goods; avocado,1,produce; "
                     "chips,0.5,dry goods; salsa,0.5,dry goods", "texmex", "chicken", 2),
    ("chicken with mediterranean salad", 2, "chicken,2,meat; roma tomatoes,4,produce; cucumber,1,produce; red onion,0.5"
                                            ",produce; feta,1,deli; red wine vinegar,0.2,dry goods; kalamata olives,1,"
                                            "dry goods", "greek", "chicken", 1)
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
        random_rowid = (random_rowid % max_rowid) + 1 # TODO: Is it more efficient to instead get all results and randomly select one
    print(f"found dinner {dinner}") # TODO: remove
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
