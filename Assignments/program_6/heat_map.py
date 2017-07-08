"""
Program:
--------
    Program 6 
Description:
------------
     Generates heat map for the terrorist attacks taken place in cities around the world
    
Name: SaiKiran Valliyil, Revathi Chikoti
Date:07 july 2017
"""

import pprint as pp
import os,sys
import json
import math
import pygame
EPSILON = sys.float_info.epsilon 


#Absolute path for Data
DIRPATH = os.path.dirname(os.path.realpath(__file__))

def convert_to_rgb(minval, maxval, val, colors):
    fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i = int(fi)
    f = fi - i
    if f < EPSILON:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

#To open and read a json file
def mercX(lon):
    """
    Mercator projection from longitude to X coord
    """
    zoom = 1.0
    lon = math.radians(lon)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = lon + math.pi
    return int(a * b)


def mercY(lat):
    """
    Mercator projection from latitude to Y coord
    """
    zoom = 1.0
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return int(a * c)


if __name__=='__main__':
    f = open(DIRPATH+'/'+"attacks.json","r")
    data = f.read()
    data = json.loads(data)
    coords = []
    count = []
    converted = []
    final_color = []
    screen_width,screen_height = 1024, 512
    
    for key,value in data.items():
        for i,j in value.items():
            coords.append(j['geometry']['coordinates'])
            count.append(int(j['count']))
    for con in coords:
        x = int((mercX(con[0]) / 1024 * screen_width))        
        y = int((mercY(con[1]) / 512 * screen_height) - 256)
        converted.append((x,y))
    minval = min(count)
    maxval = max(count)
    color = []
    color_values = []
    radius_range = []
    radius= []
    radius_width = []
    rd = []
    steps = 30
    delta = float(maxval-minval) / steps
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # [BLUE, GREEN, RED]
    

    for i in range(steps+1):
        val = minval + i*delta
        r, g, b = convert_to_rgb(minval, maxval, val, colors)
        color_values.append(val)
        color.append((r,g,b))
    color_values.append(maxval+1)
    print(len(color_values))

   # Initializing radius and its width with minimal values
    for v in range (len(color_values)):
        radius_range.append(v+1)
        rd.append(v+1)
    
    # Appends colors,radius and its width for each terrorist attack count
    for j in range(len(count)):
        for k in range(len(color_values)-1):
            if count[j] >= color_values[k] and count[j] < color_values[k+1]:
                final_color.append(color[k])
                radius.append(int(radius_range[k]*5/2))
                radius_width.append(rd[k]*2/4)
    print(max(radius))
    print("max of rad is",max(radius_width))
    #print(radius_width)
    
    background_colour = (255,255,255)   
    black = (0,0,0)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Terrorist Attacks')
    screen.fill(background_colour)
    pygame.init()
    
    bg = pygame.image.load(DIRPATH+'/'+'1024x512.png')
    pygame.display.flip()


    running = True
    while running:
        screen.blit(bg, (0, 0))
        for p in range(len(converted)):
            pygame.draw.circle(screen, final_color[p], (converted[p]), radius[p],int(radius_width[p]))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.QUIT:
                pygame.image.save(screen,DIRPATH+'/'+'Heat_map.png')
                running = False
        pygame.display.flip()
        pygame.time.wait(200)
