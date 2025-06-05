# Listing 5-1, 5-2, 5-3, 5-4, 5-5

# Note: Links are often referred to as nodes
#
# using lower_case instead of mixedCase for functions and variables

class Link:
    def __init__(self, data, next=None):
        self.__data = data
        self.__next = next

    def get_data(self):
        return self.__data
    
    def set_data(self, data):
        self.__data = data

    def get_next(self):
        return self.__next
    
    def set_next(self, link):
        self.__next = link

    def is_last(self):
        return self.__next is None
    
    def __str__(self):
        return str(self.get_data())

# TODO: create, connect and use links    
if __name__=='__main__':
    link1 = 'First'
    link2 = 'Second'
    link3 = 'Third'
    
    links = [Link(link1, None), Link(link2, None), Link(link3, None)]
    
    links[0].set_next(links[2])
    links[1].set_next(links[0])
    
    print(links[0].get_next().get_next().get_data())
    print(links[0].get_next().get_data())
    