# this file defines a bunch of cases

# not possible to get a monopoly,
# i.e. it's a color group of size three
# and two different people each own one
no_monopoly = 0

# similar to above
one_from_monopoly = 1

# the property is two from a monopoly, 
# i.e. it belongs to a color group of size three
# and someone owns one of the properties already,
# or it belongs to a color grou pof size two
# and no one owns any of them yet
two_from_monopoly = 2

# the property is three from a monopoly, 
# i.e. it belongs to a color group of size three
# and no one owns any of them yet
three_from_monopoly = 3

# property belongs to a color_group of three
# and I already own one of the other colors
# plus no one owns the third one
two_from_monopoly_me = 4

# property belongs to a color_group of three
# and I already own the other two squares
# OR
# property belongs to a color_group of two
# and I already own the other square
one_from_monopoly_me = 5

# developing the nth building
one_building = 6
two_building = 7
three_building = 8
four_building = 9
five_building = 10
