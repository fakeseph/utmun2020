from typing import List, TextIO
import math
import pygame

pygame.init()

white = (255,255,255)
black = (0,0,0)

width = 900
height = 750

gameDisplay = pygame.display.set_mode((width, height))
gameDisplay.fill(white)

######################################################

# helper functions
def latlongtopixel(lat, long):
    
    x = (1150 * (180 + int(long)) / 360) % 1150 + (1150 / 2)

    latRad = int(lat) * math.pi / 180
    mercN = math.log(math.tan((math.pi / 4) + (latRad / 2)))
    y = (1150 / 2) - (1150 * mercN / (2 * math.pi))
    
    return [int(x - (1150 / 2)), int(y)]

    #x = (width * (180 + int(long)) / 360) % width + (width / 2)

    #latRad = int(lat) * math.pi / 180
    #mercN = math.log(math.tan((math.pi / 4) + (latRad / 2)))
    #y = (height / 2) - (width * mercN / (2 * math.pi))
    
    # return [int(x - (width / 2)), int(y)]
    
def findgdp(country):
    print('$' + str(countrytogdp[country]) + ' in 2011 US dollars')

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

countrytogdp = {}

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
    countrytogdp[name] = gdp

    if 0 < gdp <= 500:
        colour = (18, 82, 123)
    elif 500 < gdp <= 1000:
        colour = (25, 112, 167)
    elif 1000 < gdp <= 1500:
        colour = (44, 154, 224)
    elif 1500 < gdp <= 2000:
        colour = (89, 176, 230)
    elif 2000 < gdp <= 2500:
        colour = (111, 186, 234)
    elif 2500 < gdp <= 3000:
        colour = (133, 197, 237)
    elif 3000 < gdp <= 3500:
        colour = (155, 208, 241)
    elif 3500 < gdp <= 4000:
        colour = (178, 218, 244)
    elif 4000 < gdp <= 4500:
        colour = (200, 229, 247)
    elif 4500 < gdp <= 5000:
        colour = (222, 240, 250)
    elif 5000 < gdp:
        colour = (245, 250, 253)

    pygame.draw.polygon(gameDisplay, colour, tuple(listofcoords))
    pygame.draw.polygon(gameDisplay, black, tuple(listofcoords), 1)

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