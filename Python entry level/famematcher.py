#Assignment 1 fame matcher
#List for each attribute
gender = ["male", "female"] #List
hair_color = ["brown", "blonde", "red"] #List
eye_color = ["green", "blue", "brown"] #List

#Apply varibles as the people, and give them seperate index in each list
daniel_radcliffe = [gender[0], hair_color[0], eye_color[2]]
rupert_grint = [gender[0], hair_color[2], eye_color[1]]
emma_watson = [gender[1], hair_color[0], eye_color[2]]
selena_gomez = [gender[1], hair_color[0], eye_color[2]]
ryan_reynolds = [gender[0], hair_color[0], eye_color[2]]
adam_hellgren = [gender[0], hair_color[0], eye_color[0]]
oscar_gullberg = [gender[0], hair_color[0], eye_color[1]]
kylie_jenner = [gender[1], hair_color[0], eye_color[2]]
trump = [gender[0], hair_color[1], eye_color[1]]

# Apply dictionary, so we can apply name for each varible
people = {
    "Daniel Radcliffe": daniel_radcliffe,
    "Rupert Grint": rupert_grint,
    "Emma Watson": emma_watson,
    "Selena Gomez": selena_gomez,
    "Ryan Reynolds": ryan_reynolds,
    "Adam 'Snygg' Hellgren": adam_hellgren,
    "Oscar Gullberg": oscar_gullberg, 
    "Kylie Jenner": kylie_jenner,
    "Donald Trump": trump
}

#Inputs to search the people
a = input("Choose a gender (male/female): ")
b = input("Choose a hair color (brown/blonde/red): ")
c = input("Choose a eye color (green/blue/brown): ")

#False to make the program run
match_found = False
#For-loop to controll if the selected attributes 
for name, attributes in people.items():
    #if-statement to check the input attributes match with the selected people
    if [a, b, c] == attributes:
        print(f"Matched person {name}")
        #match found true if a match has been made
        match_found = True
    #else we print no match found 
else:
    print("No match found!")