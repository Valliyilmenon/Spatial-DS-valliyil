```py
"""
Program:
--------
    Program 2 - To create a 2D scatterplot of locations of crimes.

Description:
------------
    This program takes lats/longs from the given files to match the actual crime committed. 
    It scales the coordinates in order to plot the points from all five buroughs on the same screen.
    
Name: Valliyil Saikiran
Date: 19 June 2017
"""

import pygame
import sys,os
import pprint as pp

DIRPATH = os.path.dirname(os.path.realpath(__file__))

def all_points(file_path):
    """
    Retrieves coordinates from the given files and returns scaled coordinates to plot the points to match the actual crime committed.
     
    Args:
        path: Path of each given file

    Returns:
        A list of tupple consisting of x,y coordinates to plot the points:

    """
    points = []
    cord = []
    keys = []
    crimes = []
    got_keys = False
    x_min = 913357
    x_max = 1067226
    y_min = 121250
    y_max = 271820
    
#with open(DIRPATH+'/../NYPD_CrimeData/Nypd_Crime_01') as f:
    with open(file_path) as f:
        for line in f:
            line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
            line = line.strip().split(',')
            if not got_keys:
                keys = line
                got_keys = True
                continue
            crimes.append(line)
        for crime in crimes:
            try:
                x = int(crime[19])
                yold =int(crime[20])
                points.append((x,yold))
            except ValueError:
                pass

        for j in points:
            x = (((j[0]-x_min)/(x_max-x_min)))
            yold = (((j[1]-y_min)/(y_max-y_min)))
            cord.append((int(x*1000),int((1-yold)*1000)))
        return cord
        
if __name__ == '__main__':

    # if there are no command line args
    if len(sys.argv) == 1:
        width = 1000    # define width and height of screen
        height = 1000
    else:
        # use size passed in by user
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    
    # create an instance of pygame
    # "screen" is what will be used as a reference so we can
    # pass it to functions and draw to it.
    screen = pygame.display.set_mode((width, height)) 

    # Set title of window
    pygame.display.set_caption('Points')

    # Set background to white
    screen.fill((255,255,255))
    # Refresh screen
    pygame.display.flip()

    # Lists to store scaled coordinates
    final_list_Bronx  = []
    final_list_Manhatten = []
    final_list_Queens = []
    final_list_Staten_Island = []
    final_list_Brooklyn = []
    final_list_Bronx  = all_points(DIRPATH+'/'+'filtered_crimes_bronx.csv')
    final_list_Manhatten = all_points(DIRPATH+'/'+'filtered_crimes_manhattan.csv')
    final_list_Queens = all_points(DIRPATH+'/'+'filtered_crimes_queens.csv')
    final_list_Staten_Island = all_points(DIRPATH+'/'+'filtered_crimes_staten_island.csv')
    final_list_Brooklyn = all_points(DIRPATH+'/'+'filtered_crimes_brooklyn.csv')
    

running = True
while running:
    for p in final_list_Bronx:
        pygame.draw.circle(screen,(2,120,120),p,1,0)
    for p in final_list_Manhatten:
        pygame.draw.circle(screen,(194,35,38),p,1,0)
    for p in final_list_Queens:
        pygame.draw.circle(screen,(243,115,56),p,1,0)
    for p in final_list_Brooklyn:
        pygame.draw.circle(screen,(128,22,56),p,1,0)
    for p in final_list_Staten_Island:
        pygame.draw.circle(screen,(253,182,50),p,1,0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen,DIRPATH+'/'+'all_buroughs_screen_shot.png')
            running = False
            
        pygame.display.flip()
    
    
```
