from typing import List, TextIO
import math
import pygame

pygame.init()

white = (255,255,255)
black = (0,0,0)

width = 900
height = 750

gameDisplay = pygame.display.set_mode((width, height))
gameDisplay.fill(black)

######################################################

# helper functions

def latlongtopixel(lat, long):
    
    x = (1000 * (180 + int(long)) / 360) % 1000 + (1000 / 2)

    latRad = int(lat) * math.pi / 180
    mercN = math.log(math.tan((math.pi / 4) + (latRad / 2)))
    y = (1000 / 2) - (1000 * mercN / (2 * math.pi))
    
    return [int(x - (1000 / 2)), int(y)]

    #x = (width * (180 + int(long)) / 360) % width + (width / 2)

    #latRad = int(lat) * math.pi / 180
    #mercN = math.log(math.tan((math.pi / 4) + (latRad / 2)))
    #y = (height / 2) - (width * mercN / (2 * math.pi))
    
    #return [int(x - (width / 2)), int(y)]

# draw the african continent in grey

contpoints = []

contdata = open('continent.csv')
contdata.readline()
contline = contdata.readline()

while contline != '':
    startoflat1 = contline.find(',')
    endoflat1 = contline.find(',', startoflat1 + 1)
    startoflong1 = endoflat1 + 1
    
    latitude1 = float(contline[(startoflat1 + 1):endoflat1])
    longitude1 = float(contline[startoflong1:(len(contline) - 1)])

    c1 = latlongtopixel(latitude1, longitude1)

    contpoints.append(c1)

    contline = contdata.readline()
    
pygame.draw.polygon(gameDisplay, (112, 112, 112), tuple(contpoints))


######################################################

# function that takes all border coordinates in one file and adds to a coords_dict
coords_dict = {}

borderdata = open('africaborders.csv')
borderdata.readline()
dataline = borderdata.readline()

while dataline != '':
    startoflat = dataline.find(',')
    endoflat = dataline.find(',', startoflat + 1)
    startoflong = endoflat + 1
    
    latitude = dataline[(startoflat + 1):endoflat]
    longitude = dataline[startoflong:(len(dataline) - 1)]

    country_name = dataline[:startoflat]
    
    if country_name not in coords_dict:
        coords_dict[country_name] = [[latitude, longitude]]
    coords_dict[country_name].append([latitude, longitude])

    dataline = borderdata.readline()

# gathering gdp data
gdpdata = open('gdpdata.csv')
gdpdata.readline()
gdpstr = gdpdata.readline()

# drawing
list_of_countries = list(coords_dict.keys())
listofcoords = []

for name in list_of_countries:
    country_coordinates = coords_dict[name]
    
    for item in country_coordinates:
        latpoint = float(item[0])
        longpoint = float(item[1])
        c = latlongtopixel(latpoint, longpoint)
        listofcoords.append(c)
        
    # function that reads gdp data and determines colour

    gdp = float(gdpstr[9:(len(gdpstr) - 2)])

    if 0 < gdp <= 500:
        colour = (69, 129, 137)
    elif 500 < gdp <= 1000:
        colour = (79, 148, 157)
    elif 1000 < gdp <= 1500:
        colour = (89, 166, 177)
    elif 1500 < gdp <= 2000:
        colour = (99, 185, 197)
    elif 2000 < gdp <= 2500:
        colour = (114, 192, 202)
    elif 2500 < gdp <= 3000:
        colour = (130, 199, 208)
    elif 3000 < gdp <= 3500:
        colour = (145, 206, 214)
    elif 3500 < gdp <= 4000:
        colour = (161, 213, 220)
    elif 4000 < gdp <= 4500:
        colour = (177, 220, 226)
    elif 4500 < gdp <= 5000:
        colour = (192, 227, 231)
    elif 5000 < gdp:
        colour = (208, 234, 237)

    pygame.draw.polygon(gameDisplay, colour, tuple(listofcoords))

    # resetting  variables
    listofcoords = []
    if gdpstr != '':
        gdpstr = gdpdata.readline()

######################################################

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()