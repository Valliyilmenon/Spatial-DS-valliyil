import os
import sys
import pygame
import math
import pprint as pp
from ast import literal_eval
from pymongo import MongoClient
from math import radians, cos, sin, asin, sqrt
import string
DIRPATH = os.path.dirname(os.path.realpath(__file__))
client = MongoClient()

def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r

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

# It keeps finding nearest airports with radius of 500. If airports are not available at a radius of 500 then the value of the radius increments by 500.
def get_nearest_neighbor():
    a = input_data()
    lon, lat = a
    radius = int(sys.argv[3])
    points = []
    rad_count = 0
    points.append(a)
    recount = 0
    origin = sys.argv[1]
    destination =sys.argv[2]
    duplicate = []
    duplicate.append(origin)
    traverse = True
    closest_ap = None
    results = client['world_data'].airports.find()
    for r in results:
        if r['properties']['ap_iata'] == destination:
            dest_coords = r['geometry']['coordinates']
            dest_lon = r['geometry']['coordinates'][0]
            dest_lat = r['geometry']['coordinates'][1]
    for k in range(300):
        print(lon,lat)
        min = 999999
        print("Radius count is",rad_count)
        print("Radius is",radius)
        air_res = client['world_data'].airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , float(radius)/3963.2 ] } }} )
        res_count = 0
        for ap in air_res:
            origin = ap['properties']['ap_iata']
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1]
            alt = ap['properties']['ap_name']
            dest_dist = haversine(lon2,lat2,dest_lon,dest_lat)

            if origin not in duplicate: 
                if dest_dist < min:
                    radius = 500
                    rad_count = 0                    
                    res_count +=1
                    min = dest_dist
                    print(dest_dist)
                    print(ap['properties']['ap_name'])
                    closest_ap = ap
            elif res_count == 0:
                print('radius changed')
                radius += 500
                print('Updated radius is',radius)
                res_count = 0
                rad_count +=1
                break
        visited = closest_ap['properties']['ap_iata']     
        if visited not in duplicate:
            duplicate.append(closest_ap['properties']['ap_iata'])
            print("duplicate is",duplicate)
            point_lon = closest_ap['geometry']['coordinates'][0]
            point_lat = closest_ap['geometry']['coordinates'][1]
            points.append((point_lon,point_lat))
            print(points)
        print(closest_ap)
        print(closest_ap['geometry']['coordinates'][0])
        print(closest_ap['geometry']['coordinates'][1])
        print(closest_ap['properties']['ap_iata'])
        print(destination)
        lon = closest_ap['geometry']['coordinates'][0]
        lat = closest_ap['geometry']['coordinates'][1]
        print(origin)
        if closest_ap['properties']['ap_iata'] == destination:
            break
        
    return points
# Returns coordinates of the Source.
def input_data():
    value = sys.argv[1]
    result = client['world_data'].airports.find()
    for i in result:
        if i['properties']['ap_iata'] == value:
            lon = i['geometry']['coordinates'][0]
            lat = i['geometry']['coordinates'][1]
            x = lon,lat
            break
        else:
            continue
    return x

# To retrieve all the features nearby the radius of 500
def get_neighbor_eq(points):
    vol_adjusted = []
    screen_width = 1024
    screen_height = 512
    radius = sys.argv[3]
    #To retrieve EarthQuake Data
    for p in points:
        air_res = client['world_data'].earthquakes.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [p[0], p[1] ] , float(radius)/3963.2 ] } }} )
        for coord in air_res:
            lon = float(coord['geometry']['coordinates'][0])
            lat = float(coord['geometry']['coordinates'][1])
            x = int((mercX(lon) / 1024 * screen_width))        
            y = int((mercY(lat) / 512 * screen_height) - 256)     
            vol_adjusted.append((x,y))
    return vol_adjusted

#To retrieve volcano data
def get_neighbor_vol(points):
    vol_adjusted = []
    screen_width = 1024
    screen_height = 512
    radius = sys.argv[3]
    for p in points:
        air_res = client['world_data'].volcanos.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [p[0], p[1] ] , float(radius)/3963.2 ] } }} )
        for coord in air_res:
            lon = float(coord['geometry']['coordinates'][0])
            lat = float(coord['geometry']['coordinates'][1])
            x = int((mercX(lon) / 1024 * screen_width))        
            y = int((mercY(lat) / 512 * screen_height) - 256)     
            vol_adjusted.append((x,y))
    return vol_adjusted
# To retrieve meteorite data
def get_neighbor_met(points):
    vol_adjusted = []
    screen_width = 1024
    screen_height = 512
    radius = sys.argv[3]
    for p in points:
        air_res = client['world_data'].meteorite.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [p[0], p[1] ] , float(radius)/3963.2 ] } }} )
        for coord in air_res:
            lon = float(coord['geometry']['coordinates'][0])
            lat = float(coord['geometry']['coordinates'][1])
            x = int((mercX(lon) / 1024 * screen_width))        
            y = int((mercY(lat) / 512 * screen_height) - 256)     
            vol_adjusted.append((x,y))
    return vol_adjusted

#To plot the acquired points onto the map
def run_tests():
    screen_width = 1024
    screen_height = 512
    con_points = []
    result = get_nearest_neighbor()
    pp.pprint(result)
    print(len(result))
    np = get_neighbor_eq(result)
    vol = get_neighbor_vol(result)
    met = get_neighbor_met(result)
    for con in result:
        x = int((mercX(con[0]) / 1024 * screen_width))        
        y = int((mercY(con[1]) / 512 * screen_height) - 256)
        con_points.append((x,y))
    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024, 512)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Query_1')
    screen.fill(background_colour)
    pygame.init()
    bg = pygame.image.load(DIRPATH+'/'+'1024x512.png')
    pygame.display.flip()
    left = []
    right = []
        #Json File with all the adjusted coordinates
    running = True
        # c = 1
    while running:
        screen.blit(bg, (0, 0))
        for p in con_points:
            pygame.draw.circle(screen, (0,0,255), p, 1,0)
        for q in np:
           pygame.draw.circle(screen, (0,255,255), q, 1)
        for r in vol:
            pygame.draw.circle(screen, (194,35,38), r, 1)
        for s in met:
            pygame.draw.circle(screen, (0,255,0), s, 1)
            pygame.draw.lines(screen,(0,0,255),False,con_points,3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clean_area(screen,(0,0),width,height,(255,255,255))
            if event.type == pygame.QUIT:
                pygame.image.save(screen,DIRPATH+'/'+'Query1_ScreenShot.png')
                running = False
        pygame.display.flip()
        pygame.time.wait(200)


if __name__=='__main__':
   
    run_tests()
