from utils.db_utils import *

ATTRIBUTES = ["name", "servings_in_days", "ingredients", "type_of_cuisine", "protein", "level_of_difficulty"]
# TODO: Create a class and have some vars as part of class


def generate_dinner_plan(dinners_wanted_list, num_dinners, num_lunches):
    dinner_plan = []
    dinner_names = []
    lunch_plan = []
    ingredients_list = set()

    # First, add any input dinners to plan
    for dinner_wanted in dinners_wanted_list:
        _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = dinner_wanted[0]
        if meal_name not in dinner_names:
            dinner_names.append(meal_name)
            if ingredients:
                ingredients = ingredients.split(', ')
                ingredients_list.update(ingredient for ingredient in ingredients)

            leftovers = servings-1 if servings-1 > 0 else 0
            dinner_info = {
                "meal": meal_name,
                "leftovers": leftovers,
                "ingredients": ingredients
            }

            while leftovers > 0:
                lunch_plan.append(meal_name)
                leftovers = leftovers - 1

            dinner_plan.append(dinner_info)

    remaining_dinners = float(num_dinners) - len(dinner_plan)
    remaining_lunches = float(num_lunches) - len(lunch_plan)
    completed_plan = False
    if remaining_dinners == 0:
        completed_plan = True
    while not completed_plan:
        if remaining_dinners == 1:
            # Add 1 to remaining lunches because need servings for 1 dinner
            dinner = get_dinner_by_servings(remaining_lunches + 1)
            completed_plan = add_dinner_to_plan(dinner, dinner_names, ingredients_list, dinner_plan, lunch_plan, remaining_lunches)
        else:
            # Add 1 to remaining lunches because need servings for 1 dinner
            dinner = get_dinner_by_max_servings(remaining_lunches + 1)
            added_meal, remaining_lunches = add_dinner_to_plan(dinner, dinner_names, ingredients_list, dinner_plan, lunch_plan, remaining_lunches)
            if added_meal:
                remaining_dinners = remaining_dinners - 1

    print(dinner_names)
    return dinner_names, dinner_plan, lunch_plan, ingredients_list


def add_dinner_to_plan(dinner, dinner_names, ingredients_list, dinner_plan, lunch_plan, remaining_lunches):
    _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = dinner
    if meal_name not in dinner_names:
        dinner_names.append(meal_name)
        # TODO: Add quantity of ingredients, maybe type of ingredient
        if ingredients:
            ingredients = ingredients.split(', ')
            ingredients_list.update(ingredient for ingredient in ingredients)

        leftovers = servings-1 if servings-1 > 0 else 0
        dinner_info = {
            "name": meal_name,
            "leftovers": leftovers,
            "ingredients": ingredients
        }

        remaining_lunches = max(remaining_lunches - leftovers, 0)

        while leftovers > 0:
            lunch_plan.append(meal_name)
            leftovers = leftovers - 1

        dinner_plan.append(dinner_info)
        return True, remaining_lunches
    return False, remaining_lunches


def replace_dinner_in_plan(dinner_names, dinner_plan, lunch_plan):
    while True:
        resp = input("Would you like to replace any meals in the generated dinner plan?\n"
                     "Enter Y for yes. ")
        if resp.upper() == "Y":
            print("Which dinner would you like to replace? Options are:")
            for i, dinner in enumerate(dinner_names):
                print(f"{i} - {dinner}")
            to_replace = input("Please enter an integer: ") # TODO: validate input
            dinner_to_replace = dinner_names[int(to_replace)]
            for dinner in dinner_plan:
                if dinner["name"] == dinner_to_replace:
                    servings = dinner["leftovers"] + 1
                    while True:
                        _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = (
                            get_dinner_by_servings(servings))
                        if meal_name not in dinner_names:
                            dinner["name"] = meal_name
                            dinner["ingredients"] = ingredients
                            dinner_names.remove(dinner_to_replace)
                            dinner_names.append(meal_name)
                            lunch_plan = [meal_name if lunch == dinner_to_replace else lunch for lunch in lunch_plan]
                            break
            print(dinner_names)
            print(lunch_plan)

            # TODO: Update list of ingredients, may be easier to just create new list or need quantity
        else:
            break


def get_create_dinner_plan_user_input():
    num_dinners, num_lunches = 0, 0

    is_valid = False
    while not is_valid:
        num_dinners = input("How many dinners are needed? ")
        is_valid = validate_positive_number(num_dinners)

    is_valid = False
    while not is_valid:
        num_lunches = input("How many lunches are needed? ")
        is_valid = validate_positive_number(num_lunches)

    return num_dinners, num_lunches


def get_query_database_user_input():
    attribute, value = "", ""

    is_valid = False
    while not is_valid:
        attribute = input("What attribute would you like to filter by?\n"
                          f"Valid attributes are {ATTRIBUTES} ")
        is_valid = validate_attribute(attribute)

    value = input(f"What value would you like to filter by with attribute {attribute}? ")

    return attribute, value


def get_dinners_to_include():
    dinners_to_include = []
    while True:
        response = input("Are there any specific dinners you'd like included? Enter Y for yes. ")
        if response.upper() == "Y":
            dinner_name = input("What dinner would you like to include? ")
            # Check if dinner is in database
            dinner = get_dinners_by_attribute("name", dinner_name)
            if dinner:
                dinners_to_include.append(dinner)
                print(f"{dinner_name} will be included in the plan.")
            else:
                print(f"{dinner_name} is not a valid dinner name.")
        else:
            break
    return dinners_to_include


def validate_positive_number(input):
    try:
        val = float(input)
        if val < 0:
            print("Input is not positive.")
            return False
    except:
        print("Input is not a number.")
        return False
    return True


def validate_attribute(input):
    if input in ATTRIBUTES:
        return True
    return False


def main():
    while True:
        response = input("Please enter an integer from the following options. To exit, enter 0.\n"
                         "1 - Create database.\n"
                         "2 - Generate dinner plan.\n"
                         f"3 - List all meals with specific attribute. Ex. List all meals with protein of chicken.\n"
                         f"4 - List all meals that are not attribute. Ex. List all meals without protein of chicken.\n"
                         "5 - Add meal to database.\n")
        if response == "1":
            create_dinner_db()
            insert_meal_data()
            print("Created meal database.")
        elif response == "2":
            # Take in any dinners definitely want, todo turn into list
            # dinner_wanted = input("...")
            # dinner_wanted_tuple = get_dinners_by_attribute("name", dinner_wanted)
            num_dinners, num_lunches = get_create_dinner_plan_user_input()
            dinners_to_include = get_dinners_to_include()
            dinner_names, dinner_plan, lunch_plan, ingredients_list = generate_dinner_plan(
                dinners_to_include, num_dinners, num_lunches)
            print(f"Generated dinner plan with {num_dinners} dinners and at least {num_lunches} lunches.")
            # print(dinner_plan)
            print(lunch_plan)
            print(ingredients_list)
            dinner_plan = replace_dinner_in_plan(dinner_names, dinner_plan, lunch_plan)
        elif response == "3":
            attribute, value = get_query_database_user_input()
            filtered_dinners = get_dinners_by_attribute(attribute, value)
            if filtered_dinners:
                for dinner in filtered_dinners:
                    _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = dinner
                    print(f"{meal_name}: servings:{servings}, ingredients:{ingredients}, type:{type_of_cuisine},"
                          f" protein:{protein}, level of difficulty:{level_of_difficulty}")
            else:
                print(f"There are no dinners with {attribute} equal to {value}")
        elif response == "4":
            attribute, value = get_query_database_user_input()
            filtered_dinners = get_dinners_by_not_parameter(attribute, value)
            if filtered_dinners:
                for dinner in filtered_dinners:
                    _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = dinner
                    print(f"{meal_name}: servings:{servings}, ingredients:{ingredients}, type:{type_of_cuisine},"
                          f" protein:{protein}, level of difficulty:{level_of_difficulty}")
            else:
                print(f"There are no dinners with {attribute} that is not {value}")
        elif response == "5":
            # TODO: Create get input and add meal to db
            break
        elif response == "0":
            break
        else:
            print(f"{response} is not a valid input")


if __name__ == "__main__":
    main()
