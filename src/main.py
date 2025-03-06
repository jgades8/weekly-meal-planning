from utils.db_utils import *


def generate_dinner_plan(dinners_wanted_list, num_dinners, num_lunches):
    dinner_plan = []
    dinner_names = []
    lunch_plan = []
    ingredients_list = set()

    # First, add any input dinners to plan
    for i, dinner_wanted in dinners_wanted_list:
        _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = dinner_wanted
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

    return dinner_plan, lunch_plan, ingredients_list


def add_dinner_to_plan(dinner, dinner_names, ingredients_list, dinner_plan, lunch_plan, remaining_lunches):
    _, meal_name, servings, ingredients, type_of_cuisine, protein, level_of_difficulty = dinner
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

        remaining_lunches = max(remaining_lunches - leftovers, 0)

        while leftovers > 0:
            lunch_plan.append(meal_name)
            leftovers = leftovers - 1

        dinner_plan.append(dinner_info)
        return True, remaining_lunches
    return False, remaining_lunches


def get_user_input():
    create_db = input("Does the dinner database need to be created? Reply Y for yes ")
    num_dinners, num_lunches = 0, 0

    is_valid = False
    while not is_valid:
        num_dinners = input("How many dinners are needed? ")
        is_valid = validate_positive_number(num_dinners)

    is_valid = False
    while not is_valid:
        num_lunches = input("How many lunches are needed? ")
        is_valid = validate_positive_number(num_lunches)

    return create_db, num_dinners, num_lunches


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


def main():
    create_db, num_dinners, num_lunches = get_user_input()
    if create_db.upper() == 'Y':
        create_dinner_db()
        insert_meal_data()

    # Take in any dinners definitely want, todo turn into list
    # dinner_wanted = input("...")
    # dinner_wanted_tuple = get_dinners_by_attribute("name", dinner_wanted)
    dinner_plan, lunch_plan, ingredients_list = generate_dinner_plan([], num_dinners, num_lunches)
    print(dinner_plan)
    print(lunch_plan)
    print(ingredients_list)


if __name__ == "__main__":
    main()
