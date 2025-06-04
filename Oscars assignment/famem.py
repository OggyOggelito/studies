#Empty list
matches = []

#Input for each category
a = input('Choose a gender (male/female) ')
b = input('Choose a hair color (brown/blonde/red) ')
c = input('Choose a eye color (green/blue/brown) ')
# If and elif-statements to search between the people
if a == 'male':
    if b == 'brown':
        if c == 'brown':
            matches.append('Daniel Radcliffe')
            matches.append('Ryan Reynolds')
        elif c == 'green':
            matches.append('Adam "Handsome" Hellgren')
        elif c == 'blue':
            matches.append('Oscar Gullberg')
    elif b == 'red' and c == 'blue':
        matches.append('Rupert Grint')
    elif b == 'blonde' and c == 'blue':
        matches.append('Donald Trump')
elif a == 'female':
    if b == 'brown':
        if c == 'brown':
            matches.append('Emma Watson')
            matches.append('Kylie Jenner')
            matches.append('Selena Gomez')
# if-statement for matches
if matches:
    print('Matched persons: ')
    #for-loop for match in matches to print the list in String format rather than list format
    for match in matches:
        print(match)
# else no match found
else:
    print('No match found!')