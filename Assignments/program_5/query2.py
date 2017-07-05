import math
import os
import sys
import pygame
import pprint as pp
from ast import literal_eval
from pymongo import MongoClient
DIRPATH = os.path.dirname(os.path.realpath(__file__))

client = MongoClient()


    # def get_features_near_me(self,collection,point,radius,earth_radius=3963.2): #km = 6371
"""
        Finds "features" within some radius of a given point.
        Params:
            collection_name: e.g airports or meteors etc.
            point: e.g (-98.5034180, 33.9382331)
            radius: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
            mh = mongoHelper()
            loc = (-98.5034180, 33.9382331)
            miles = 200
            feature_list = mh.get_features_near_me('airports', loc, miles)
"""
# Returns points after processing all the given values
def get_features_near_me(feature,field,field_value,min_max,max_results,radius,point):
    x,y = literal_eval(point)
    #x,y = point
    i = 0
    j = 0
    earth_radius = 3963.2
    final_result = []
    if feature == 'volcanos':
        res = client['world_data'][feature].find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , float(radius)/earth_radius ] } }} )
        res_list = []
        k =0
        for r in res:
            if field == 'Altitude':
                if r['properties']['Altitude'] != '':
                    altitude = float(r['properties']['Altitude'])
                    k+=1

                        
            if altitude < int(field_value) and min_max == 'min' and i < int(max_results):
                final_result.append(r['geometry']['coordinates'])
                i+=1
            elif altitude > int(field_value) and min_max == 'max' and i < int(max_results):
                final_result.append(r['geometry']['coordinates'])
                i+=1
        print(k)
        print(len(final_result))

    elif feature == 'earthquakes':
        #print(feature)
        res = client['world_data'][feature].find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , float(radius)/earth_radius ] } }} )
        for r in res:
            if field == 'mag':
                magnitude = float(r['properties']['mag'])
                #print(magnitude)
                #print(type(altitude))
                if magnitude < float(field_value) and min_max == 'min' and i < int(max_results):
                    final_result.append(r['geometry']['coordinates'])
                    i+=1
                elif magnitude > float(field_value) and min_max == 'max' and i < int(max_results):
                    final_result.append(r['geometry']['coordinates'])
                    i+=1
        print(len(final_result))
    elif feature == 'meteorite':
        res = client['world_data'][feature].find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , float(radius)/earth_radius ] } }} )
        for r in res:
            if field == 'year':
                year = float(r['properties']['year'])
                #print(magnitude)
                #print(type(altitude))
                if year < int(field_value) and min_max == 'min' and i < int(max_results):
                    final_result.append(r['geometry']['coordinates'])
                    i+=1
                elif year > int(field_value) and min_max == 'max' and i < int(max_results):
                    final_result.append(r['geometry']['coordinates'])
                    i+=1
    
    return final_result
        #print(altitude)

# def get_all_data(radius, point):
    # x,y = literal_eval(point)
    # i = 0
    # earth_radius = 3963.2
    # #result = 
    # final_result = []
    # result = client['world_data'].volcanos.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , float(radius)/earth_radius ] } }} )
    # for i in result:
    #     final_result.append(i)
    # result = client['world_data'].earthquakes.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , float(radius)/earth_radius ] } }} )
    # for i in result:
    #     final_result.append(i)
    # result = client['world_data'].meteorite.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , float(radius)/earth_radius ] } }} )
    # for i in result:
    #     final_result.append(i)
    #print(final_result)
    # return final_result
   
    # def _haversine(self,lon1, lat1, lon2, lat2):
    #     """
    #     Calculate the great circle distance between two points 
    #     on the earth (specified in decimal degrees)
    #     """
    #     # convert decimal degrees to radians 
    #     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    #     # haversine formula 
    #     dlon = lon2 - lon1 
    #     dlat = lat2 - lat1 
    #     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    #     c = 2 * asin(sqrt(a)) 
    #     r = 3956 # Radius of earth in kilometers. Use 6371 for km
    #     return c * r
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
        adjy = int(yprime*height)
        adjusted.append((adjx,adjy))
    return adjusted

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

#To display the coordinates on the screen.
def run_tests():
    allx = []
    ally = []
    points = []
    result = 0
    screen_width = 1024
    screen_height = 512
    if len(sys.argv) > 3:
        result = get_features_near_me(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])#(138.252924, 36.204824)
        for coord in result:
            x = int((mercX(coord[0]) / 1024 * screen_width))        
            y = int((mercY(coord[1]) / 512 * screen_height) - 256)     
            points.append((x,y))
        background_colour = (255,255,255)
        black = (0,0,0)
        (width, height) = (1024, 512)

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Query_2')
        screen.fill(background_colour)
        pygame.init()
        bg = pygame.image.load(DIRPATH+'/'+'1024x512.png')
        pygame.display.flip()
        #Json File with all the adjusted coordinates
        running = True
        i = 1
        while running:
            screen.blit(bg, (0, 0))
            for p in points:
                if(sys.argv[1]=='volcanos'):
                    pygame.draw.circle(screen, (194,35,38), p, 2,0)
                elif(sys.argv[1]=='earthquakes'):
                    pygame.draw.circle(screen, (0,255,255), p, 2,0)
                elif(sys.argv[1]=='meteorite'):
                    pygame.draw.circle(screen, (0,255,0), p, 2,0)

                    #print(p)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clean_area(screen,(0,0),width,height,(255,255,255))
                if event.type == pygame.QUIT:
                    pygame.image.save(screen,DIRPATH+'/'+'Query2(1)_ScreenShot.png')
                    running = False

            pygame.display.flip()
            pygame.time.wait(150)


        #print(points)
    elif len(sys.argv) <= 3 :
        points = []
        i = 0
        eq = []
        vol = []
        met = []
        eq_adjusted = []
        vol_adjusted = []
        met_adjusted = []
        earth_radius = 3963.2
        radius = sys.argv[1]
        x,y = literal_eval(sys.argv[2])
        result = client['world_data'].volcanos.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , float(radius)/earth_radius ] } }} )
        for i in result:
            vol.append(i)
        result = client['world_data'].earthquakes.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , float(radius)/earth_radius ] } }} )
        for i in result:
            eq.append(i)
        result = client['world_data'].meteorite.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , float(radius)/earth_radius ] } }} )
        for i in result:
            met.append(i)
        #print(met)
        for coord in vol:
            lon = float(coord['geometry']['coordinates'][0])
            lat = float(coord['geometry']['coordinates'][1])
            x = int((mercX(lon) / 1024 * screen_width))        
            y = int((mercY(lat) / 512 * screen_height) - 256)     
            vol_adjusted.append((x,y))
        #print(len(vol_adjusted))
        for coord in eq:
            lon = float(coord['geometry']['coordinates'][0])
            lat = float(coord['geometry']['coordinates'][1])
            x = int((mercX(lon) / 1024 * screen_width))        
            y = int((mercY(lat) / 512 * screen_height) - 256)     
            eq_adjusted.append((x,y))
        #print(len(eq_adjusted))
        for coord in met:
            #print(coord['geometry']['coordinates'][0])
            lon = float(coord['geometry']['coordinates'][0])
            lat = float(coord['geometry']['coordinates'][1])
            x = int((mercX(lon) / 1024 * screen_width))        
            y = int((mercY(lat) / 512 * screen_height) - 256)     
            met_adjusted.append((x,y))
            #point = (len(vol_adjusted)+len(eq_adjusted)+len(met_adjusted))
       # print(point)
       # print(len(met_adjusted))
        background_colour = (255,255,255)
        black = (0,0,0)
        (width, height) = (1024, 512)

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Query_2')
        screen.fill(background_colour)
        pygame.init()
        bg = pygame.image.load(DIRPATH+'/'+'1024x512.png')
        pygame.display.flip()
        #Json File with all the adjusted coordinates
        running = True
        # c = 1
        while running:
            screen.blit(bg, (0, 0))
            for p in vol_adjusted:
                pygame.draw.circle(screen, (194,35,38), p, 1,0)
            for q in eq_adjusted:
                pygame.draw.circle(screen, (0,255,255), q, 1,0)
            for r in met_adjusted:    
                pygame.draw.circle(screen, (0,255,0), r, 1,0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.QUIT:
                    pygame.image.save(screen,DIRPATH+'/'+'Query2_ScreenShot.png')
                    running = False
            pygame.display.flip()
            pygame.time.wait(200)

if __name__=='__main__':
   
    run_tests()
