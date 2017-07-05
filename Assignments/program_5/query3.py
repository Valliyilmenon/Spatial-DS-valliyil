import math
import os
import sys
import pygame
import pprint as pp
from ast import literal_eval
from pymongo import MongoClient
from dbscan import *

DIRPATH = os.path.dirname(os.path.realpath(__file__))

client = MongoClient()


def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)
    print(clusters)
    for id in range(len(clusters)-1):
        xs = []
        ys = []
        for p in clusters[id]:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    return mbrs
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

def find_extremes(result_list,width,height):
    extremes={}
    allx = []
    ally = []
    points = []
    for r in result_list:
        lon = r['geometry']['coordinates'][0]
        lat = r['geometry']['coordinates'][1]
        x,y = (mercX(lon),mercY(lat))
        allx.append(x)
        ally.append(y)
        points.append((x,y))
    extremes['max_x'] = width
    extremes['min_x'] = 0
    extremes['max_y'] = height
    extremes['min_y'] = 0
    extremes['max_x'] = width
    extremes['min_x'] = 0
    extremes['max_y'] = height
    extremes['min_y'] = 0
    return extremes,points
   
def adjust_location_coords(extremes,points,width,height):
    """
    Adjust your point data to fit in the screen. 
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """
    maxx = float(extremes['max_x']) # The max coords from bounding rectangles
    minx = float(extremes['min_x'])
    maxy = float(extremes['max_y'])
    miny = float(extremes['min_y'])
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    adjusted = []

    for p in points:
        x,y = p
        x = float(x)
        y = float(y)
        xprime = (x - minx) / deltax         # val (0,1)
        yprime = ((y - miny) / deltay) # val (0,1)
        adjx = int(xprime*width)
        adjy = int(yprime*height)-256
        adjusted.append((adjx,adjy))
    return adjusted


def run_tests():
    ext = {}
    pts = []
    top_rect = []
    (width,height) = (1024,512)
    feature = sys.argv[1]
    min_pts = int(sys.argv[2])
    eps = sys.argv[3]
    final = []
   
    result = client['world_data'][feature].find()
    pp.pprint(result)
    ext,pts = find_extremes(result,width,height)
    pts = adjust_location_coords(ext,pts,width,height)
    mbrs = calculate_mbrs(pts,eps,min_pts)
    colors = {'volcanos':(255,0,0),'earthquakes':(0,0,255),'meteorite':(0,255,0)}

    sorted(mbrs, key=len)
    for x in range(0,5):
        final.append(mbrs[x])

    background_colour = (255,255,255)
    black = (0,0,0)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Query_3')
    screen.fill(background_colour)
    pygame.init()
    bg = pygame.image.load(DIRPATH+'/'+'1024x512.png')
    pygame.display.flip()
    running = True
    while running:
        screen.blit(bg, (0, 0))
        for rec in final:
            pygame.draw.polygon(screen,(0,255,0),rec,2)
        for p in pts:
            pygame.draw.circle(screen,colors[feature], p, 2,1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.QUIT:
                pygame.image.save(screen,DIRPATH+'/'+'Query3_ScreenShot.png')
                running = False
        pygame.display.flip()


if __name__=='__main__':
    run_tests()