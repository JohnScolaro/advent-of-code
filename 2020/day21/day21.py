"""
Solutions for the Advent of Code - Day 21

An interesting question. I genuinly don't know how to solve part A without
accidentally solving part B first.
"""

def get_foods(file_name: str):
    """
    Gets a list of foods. Each element of the list is a dictionary with two
    keys. The value corresponding to the 'ingredients' key is a list of
    ingredient strings. The value corresponding to the 'allergens' key is a
    list of allergen strings.
    """
    l = []
    with open(file_name, 'r') as fb:
        for line in fb:
            line = line[:-1]
            ingredients = line.split('(')[0].split(' ')[:-1]
            may_contain = line.split('(')[1].replace('contains ', '').replace(')', '').split(', ')
            d = {'ingredients': ingredients , 'allergens': may_contain}
            l.append(d)
    return l

def get_all_allergens(foods: dict) -> set:
    """ Returns a set of all allergens """
    s = set()
    for food in foods:
        for allergen in food['allergens']:
            s.add(allergen)
    return s

def get_foods_with_allergen(foods: list, allergen: str) -> dict:
    """
    Returns a list of foods, but only foods that contains the specified allergen.
    """
    l = []
    for food in foods:
        if allergen in food['allergens']:
            l.append(food)
    return l

def get_common_ingredients(foods: list) -> set:
    """ Get the common ingredients between a list of foods. """
    s = set()
    for food in foods:
        if len(s) == 0:
            s = set(food['ingredients'])
        else:
            s = s.intersection(set(food['ingredients']))
    return s

def get_allergen_to_ingredient_map(foods: list) -> int:
    """
    Contains all logic to figure out what allergens are contained by which
    ingredients. Works in two stages. First stage simply gets a set of all the
    possible ingredients that could have the allergen by looking at what
    ingredients are specified in all of the foods that may contain that
    allergen.

    Send stage uses deduction (ie: Ingredient A contains allergen B, therefore
    Ingredient B can not contain allergen B) to reduce the list of possible
    ingredients to a single ingredient.
    """
    # Get allergens with all ingredients that could possibly be in them.
    allergens_with_common_ingredients = {}
    for allergen in get_all_allergens(foods):
        foods_with_allergen = get_foods_with_allergen(foods, allergen)
        common_ingredients = get_common_ingredients(foods_with_allergen)
        allergens_with_common_ingredients[allergen] = common_ingredients

    # Reduce possible options using deduction.
    done = False
    while not done:
        # Check if we are done
        done = True
        for _, ingredients in allergens_with_common_ingredients.items():
            if len(ingredients) != 1:
                done = False

        # Attempt to remove all single elements from other sets
        for allergen, ingredients in allergens_with_common_ingredients.items():
            if len(ingredients) == 1:
                for a, i in allergens_with_common_ingredients.items():
                    if a != allergen:
                        i.discard(next(iter(ingredients)))

    for a, i in allergens_with_common_ingredients.items():
        allergens_with_common_ingredients[a] = next(iter(i))
    
    return allergens_with_common_ingredients


def part_a(foods: list) -> int:
    """ Returns part A's answer """
    allergen_to_ingredient_mapping = get_allergen_to_ingredient_map(foods)
    allergenic_ingredinets = set([i for _, i in allergen_to_ingredient_mapping.items()])
    counter = 0
    for food in foods:
        for ingredient in food['ingredients']:
            if ingredient not in allergenic_ingredinets:
                counter += 1
    return counter

def part_b(foods: list) -> str:
    """ Returns part B's answer """
    allergen_to_ingredient_mapping = get_allergen_to_ingredient_map(foods)
    allergens = sorted(allergen_to_ingredient_mapping.keys())
    return ','.join([allergen_to_ingredient_mapping[a] for a in allergens])

if __name__ == "__main__":
    foods = get_foods('input.txt')
    print("Part A: " + str(part_a(foods)))
    print("Part B: " + str(part_b(foods)))