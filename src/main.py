from utils.db_utils import *

ATTRIBUTES = ["name", "servings_in_days", "ingredients", "type_of_cuisine", "protein", "level_of_difficulty"]
# TODO: Create a class and have some vars as part of class?


def generate_dinner_plan(dinners_wanted_list, num_dinners, num_lunches):
    """

    :param dinners_wanted_list: list of dinners to include in generated plan
    :param num_dinners: total number of dinners required
    :param num_lunches: total number of lunches required
    :return: dinner_names, dinner_plan, lunch_plan, ingredients_list
    """
    dinner_plan = []
    dinner_names = []
    lunch_plan = []
    ingredients_list = {}
    remaining_dinners, remaining_lunches = float(num_dinners), float(num_lunches)

    # First, add any wanted dinners to plan
    for dinner_wanted in dinners_wanted_list:
        _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = dinner_wanted
        if meal_name not in dinner_names:
            dinner_names.append(meal_name)
            if ingredients:
                add_ingredients_to_list(ingredients_list, ingredients)

            leftovers = servings-1 if servings-1 > 0 else 0
            dinner_info = {
                "name": meal_name,
                "leftovers": leftovers,
                "ingredients": ingredients
            }

            remaining_dinners = remaining_dinners - 1
            remaining_lunches = remaining_lunches - leftovers
            while leftovers > 0:
                lunch_plan.append(meal_name)
                leftovers = max(0, leftovers - 1)

            dinner_plan.append(dinner_info)

    completed_plan = False
    if remaining_dinners == 0:
        completed_plan = True
    while not completed_plan:
        if remaining_dinners == 1:
            # Add 1 to remaining lunches because need servings for 1 dinner
            dinner = get_dinner_by_servings(remaining_lunches + 1)
            completed_plan, _ = add_dinner_to_plan(dinner, dinner_names, ingredients_list, dinner_plan, lunch_plan, remaining_lunches)
        else:
            # Add 1 to remaining lunches because need servings for 1 dinner
            dinner = get_dinner_by_max_servings(remaining_lunches + 1)
            added_meal, remaining_lunches = add_dinner_to_plan(dinner, dinner_names, ingredients_list, dinner_plan, lunch_plan, remaining_lunches)
            if added_meal:
                remaining_dinners = remaining_dinners - 1

    return dinner_names, dinner_plan, lunch_plan, ingredients_list


def add_dinner_to_plan(dinner, dinner_names, ingredients_list, dinner_plan, lunch_plan, remaining_lunches):
    _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = dinner
    if meal_name not in dinner_names:
        dinner_names.append(meal_name)
        if ingredients:
            add_ingredients_to_list(ingredients_list, ingredients)

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
    get_input = True
    while get_input:
        resp = input("Would you like to replace any meals in the generated dinner plan?\n"
                     "Enter Y for yes. ")
        if resp.upper() == "Y":
            print("Which dinner would you like to replace? Options are:")
            for i, dinner in enumerate(dinner_names):
                print(f"{i} - {dinner}")
            valid_input, to_replace = False, ""
            while not valid_input:
                to_replace = input("Please enter a valid integer option: ")
                try:
                    if 0 <= int(to_replace) < len(dinner_names):
                        valid_input = True
                except Exception as ex:
                    print(f"Input not valid: {ex}")

            dinner_to_replace = dinner_names[int(to_replace)]
            for dinner in dinner_plan:
                if dinner["name"] == dinner_to_replace:
                    servings = dinner["leftovers"] + 1
                    replaced = False
                    while not replaced:
                        _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = (
                            get_dinner_by_servings(servings))
                        if meal_name not in dinner_names:
                            dinner["name"] = meal_name
                            dinner["ingredients"] = ingredients
                            dinner_names.remove(dinner_to_replace)
                            dinner_names.append(meal_name)
                            lunch_plan = [meal_name if lunch == dinner_to_replace else lunch for lunch in lunch_plan]
                            replaced = True
            print(dinner_names)
            print(lunch_plan)

            # TODO: Update list of ingredients, may be easier to just create new list or need quantity
        else:
            get_input = False


def add_ingredients_to_list(ingredients_list, new_ingredients):
    ingredients = new_ingredients.split('; ')
    for ingredient in ingredients:
        # Ingredient format will be: name,quantity,store_category (ex. chicken,2,meat)
        ingredient_name, quantity, store_category = ingredient.split(',')
        if ingredient_name in ingredients_list:
            # Update quantity
            total_quantity = ingredients_list[ingredient_name][0] + float(quantity)
            ingredients_list[ingredient_name][0] = total_quantity
        else:
            # Add new ingredient and quantity
            ingredients_list[ingredient_name] = [float(quantity), store_category]


def print_ingredients_list(ingredients_list):
    sorted_ingredients = {"produce": [], "deli": [], "meat": [], "bakery": [], "dry goods": [], "frozen": [], "dairy": []}
    for ingredient in ingredients_list:
        store_loc = ingredients_list[ingredient][1]
        quantity = ingredients_list[ingredient][0]
        sorted_ingredients[store_loc].append(f"{ingredient}-{quantity}")
    print(sorted_ingredients)


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
    get_more_dinners = True
    while get_more_dinners:
        response = input("Are there any specific dinners you'd like included? Enter Y for yes. ")
        if response.upper() == "Y":
            dinner_name = input("What dinner would you like to include? ")
            # Check if dinner is in database
            dinners = get_dinners_by_attribute("name", dinner_name)
            if dinners:
                if len(dinners) > 1:
                    # Found multiple dinners with the same name, have the user select which one they want
                    for i, dinner in enumerate(dinners):
                        print(f"{i} - {dinner}")
                    tmp_input = ""
                    selected_specific_dinner = False
                    while not selected_specific_dinner:
                        try:
                            tmp_input = input("Multiple dinners found. Which one would you like?\nEnter an integer. ")
                            if validate_positive_number(tmp_input):
                                dinner_int = int(tmp_input)
                                dinners_to_include.append(dinners[dinner_int])
                                selected_specific_dinner = True
                            else:
                                raise Exception
                        except: # TODO: Add specific exception
                            print(f"{tmp_input} is not a valid input.")
                else:
                    dinners_to_include.append(dinners[0])
                print(f"{dinner_name} will be included in the plan.")
            else:
                print(f"{dinner_name} is not a valid dinner name.")
        else:
            get_more_dinners = False
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
    done = False
    while not done:
        response = input("Please enter an integer from the following options.\n"
                         "0 - Exit.\n"
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
            num_dinners, num_lunches = get_create_dinner_plan_user_input()
            dinners_to_include = get_dinners_to_include()
            dinner_names, dinner_plan, lunch_plan, ingredients_list = generate_dinner_plan(
                dinners_to_include, num_dinners, num_lunches)
            print(f"Generated dinner plan with {num_dinners} dinners and at least {num_lunches} lunches.")
            print(f"Dinners are {dinner_names}")
            print(lunch_plan)
            print_ingredients_list(ingredients_list)
            replace_dinner_in_plan(dinner_names, dinner_plan, lunch_plan)
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
            print("This is not functioning yet :)")
        elif response == "0":
            done = True
        else:
            print(f"{response} is not a valid input")


if __name__ == "__main__":
    main()
