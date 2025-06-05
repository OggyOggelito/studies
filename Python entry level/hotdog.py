#Prices for each package and drink
hotdog_cost_per_package = 20.95
vegan_cost_per_package = 34.95
drink_cost = 13.95
#Amount of regular hotdogs and vegan hotdogs per package
hotdogs_per_package = 8
vegan_hotdogs_per_package = 4

#Inputs for each amount that students want to order
two_hotdogs = int(input("Enter the number of students who want 2 hotdogs: "))
three_hotdogs = int(input("Enter the number of students who want 3 hotdogs: "))
two_vegan_hotdogs = int(input("Enter the number of students who want 2 vegan hotdogs: "))
three_vegan_hotdogs = int(input("Enter the number of students who want 3 vegan hotdogs: "))
total_students = two_hotdogs + three_hotdogs + two_vegan_hotdogs + three_vegan_hotdogs

# Calculate the total amount regular hotdogs and vegan hotdogs
total_hotdogs = (two_hotdogs * 2) + (three_hotdogs * 3)
total_vegan_hotdogs = (two_vegan_hotdogs * 2) + (three_vegan_hotdogs * 3)

# Round up how many packages are needed
hotdog_packages = -(-total_hotdogs // hotdogs_per_package) 
vegan_hotdog_packages = -(-total_vegan_hotdogs // vegan_hotdogs_per_package)

# The total amount of students
total_drinks = total_students

# Calculate the cost for each package based on how many students have orderd + drinks 
total_hotdogs_cost = hotdog_packages * hotdog_cost_per_package
total_vegan_hotdogs_cost = vegan_hotdog_packages * vegan_cost_per_package
total_drink_cost = total_drinks * drink_cost
total_cost = total_hotdogs_cost + total_vegan_hotdogs_cost + total_drink_cost

# Display the results in a formatted table (:.2f for round up to two decimals)
print("\n| Product         | Quantity | Cost   |")
print("|-----------------|----------|---------|")
print(f"| Hotdog Packages | {hotdog_packages}        | {total_hotdogs_cost:.2f}:-|")
print(f"| Vegan Packages  | {vegan_hotdog_packages}        | {total_vegan_hotdogs_cost:.2f}:-|")
print(f"| Drinks          | {total_drinks}        | {total_drink_cost:.2f}:-|")
print("|-----------------|----------|---------|")
print(f"| Total Cost      |          | {total_cost:.2f}:-|")