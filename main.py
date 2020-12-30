# Pip Imports
from copy import deepcopy
from itertools import combinations
from progressbar import ProgressBar, Counter, Timer

# Script Imports
from methods import can_carry, can_craft, gather_n_recipes, gather_materials

# Asset Imports
from recipes import RECIPES

# Number of Items to Craft
TO_CRAFT = [0, 3, 8, 14, 24, 34, 45, 55, 70, 90, 110]
while True:
    TASK_TIER = int(input("What tier of the task are you on (1-10):\n"))
    if not (1 <= TASK_TIER <= 10):
        print("Please enter a valid tier")
    else:
        break

# Gather Carry Capacities
try:
    from inventory import INVENTORY
except ImportError:
    INVENTORY = {"weapon": 1, "armor": 1, "tool": 1, "bag": 1}
    while True:
        try:
            caps = input("Capacities (Slots, Materials, Mining, Fishing, Foods, Chopping, Bugs:\n")
            (INVENTORY["slots"], INVENTORY["material"], INVENTORY["mining"], INVENTORY["fish"], INVENTORY["food"],
             INVENTORY["choppin"], INVENTORY["bug"]) = [int(i) for i in caps.split(" ")]
            break
        except ValueError:
            print("Please enter a valid capacity input")
# Loop Through Combinations
FOUND = False
CRAFTABLE = [k for k, v in RECIPES.items() if v[1]]
widgets = ["Combinations tested: ", Counter(), " ", Timer()]
pbar = ProgressBar(widgets=widgets)
for combo in pbar(combinations(iterable=CRAFTABLE, r=TO_CRAFT[TASK_TIER])):
    # Gather recipe list, material list, and simulate carrying
    all_recipes = gather_n_recipes(to_craft=combo, recipes=RECIPES)
    materials = gather_materials(to_craft=combo, recipes=RECIPES)
    carry = can_carry(materials=materials, inventory=INVENTORY)
    # Make copy of materials
    materials_copy = deepcopy(materials)
    if carry:
        # Simulate crafting
        craft = can_craft(to_craft=combo, materials=materials, recipes=RECIPES, inv=INVENTORY)
        if craft:
            FOUND = True
            # Print Recipes to Craft
            nl = "\n"
            p_to_craft = {}
            for r in all_recipes:
                if r not in p_to_craft:
                    p_to_craft[r] = 0
                p_to_craft[r] += 1
            max_width = len(str(max(p_to_craft.values())))
            printRecipes = [f"{v:{max_width}} {m}" for m, v in p_to_craft.items()]
            print(f"\nRecipes:\n  {f'{nl}  '.join(printRecipes)}")
            # Print Materials Needed
            max_val = max(materials_copy.values(), key=lambda x: x["quantity"])
            max_width = len(str(max_val["quantity"]))
            pMaterials = [f"{v['quantity']:{max_width}} {m}" for m, v in materials_copy.items()]
            print(f"\nMaterials:\n  {f'{nl}  '.join(pMaterials)}")
            print(f"Can carry: {carry}")
            print(f"Can Craft: {craft}")
            if FOUND:
                # Ask for another combo
                if input(f"Find another recipe (y/n):\n") in ["", "y"]:
                    continue
                else:
                    break
            else:
                continue
if not FOUND:
    print(f"No recipe combinations found. Raise your carry capacity/slots and try again.")
