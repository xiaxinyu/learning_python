from pip._vendor.pyparsing import basestring
from Cake import displayMovies
movies = ["m1","m2"]
print(movies)
movies.append("m3")
print(movies)

#while loop
count = 0;
while count < len(movies):
    print(movies[count])
    count = count + 1
#isinstance
flag = isinstance(movies, list)   
print(flag)
flag = isinstance(len(movies), int)
print(flag)
flag = isinstance(movies[0], basestring)
print(flag)
"""first def"""
displayMovies(movies, "summer")