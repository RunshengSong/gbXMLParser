'''
Created on Jul 25, 2016

@author: t_songr
'''

import xml.etree.cElementTree as ET
from collections import OrderedDict
from BuildingObjects import *
import operator
import csv
import subprocess as sb
import os

class gbXMLparser():
    def __init__(self, file_path, convert_climate = False):
        self._root = ET.parse(file_path).getroot()
        
        self.convert_climate = convert_climate
        # all of the building features:
        # Basic building info:
        self.unit = None
        self.BuildingType = None
        self.Longitude = None
        self.Latitude = None
        self.CityAndCountry = None
        self.designHeatWeathIdRef = None
        self.designCoolWeathIdRef = None
        
        # wall and window features
        self.TotalWallArea = 0 # Total Wall Area for the entire building
        self.TotalWindowArea = 0 # Total Window Area for the entire building
        self.TotalWallAreaHeight = 0 # The total area times the level of the floor
        self.TotalWindowAreaHeight = 0 # The total area times the level of the floor
        
        self.WallAreaNorth = 0
        self.WallAreaNorthHeight = 0
        self.WindowAreaNorth = 0
        self.WindowAreaNorthHeight = 0
        self.WindowUVWeightedNorth = 0
        self.WindowSHGCWeightedNorth = 0
        self._UV_area_north = 0
        self._SHGC_area_north = 0
        
        self.WallAreaNorthEast = 0
        self.WallAreaNorthEastHeight = 0
        self.WindowAreaNorthEast = 0
        self.WindowAreaNorthEastHeight = 0
        self.WindowUVWeightedNorthEast = 0
        self.WindowSHGCWeightedNorthEast = 0
        self._UV_area_northeast = 0
        self._SHGC_area_northeast = 0
        
        self.WallAreaEast = 0
        self.WallAreaEastHeight = 0
        self.WindowAreaEast = 0
        self.WindowAreaEastHeight = 0
        self.WindowUVWeightedEast = 0
        self.WindowSHGCWeightedEast = 0
        self._UV_area_east = 0
        self._SHGC_area_east = 0
        
        self.WallAreaSouthEast = 0
        self.WallAreaSouthEastHeight = 0
        self.WindowAreaSouthEast = 0
        self.WindowAreaSouthEastHeight = 0
        self.WindowUVWeightedSouthEast = 0
        self.WindowSHGCWeightedSouthEast = 0
        self._UV_area_southeast = 0
        self._SHGC_area_southeast = 0
        
        self.WallAreaSouth = 0
        self.WallAreaSouthHeight = 0
        self.WindowAreaSouth = 0
        self.WindowAreaSouthHeight = 0
        self.WindowUVWeightedSouth = 0
        self.WindowSHGCWeightedSouth = 0
        self._UV_area_south = 0
        self._SHGC_area_south = 0
        
        self.WallAreaSouthWest = 0 
        self.WallAreaSouthWestHeight = 0
        self.WindowAreaSouthWest = 0
        self.WindowAreaSouthWestHeight = 0
        self.WindowUVWeightedSouthWest = 0
        self.WindowSHGCWeightedSouthWest = 0
        self._UV_area_southwest = 0
        self._SHGC_area_southwest = 0
                
        self.WallAreaWest = 0
        self.WallAreaWestHeight = 0
        self.WindowAreaWest = 0
        self.WindowAreaWestHeight = 0
        self.WindowUVWeightedWest = 0
        self.WindowSHGCWeightedWest = 0
        self._UV_area_west = 0
        self._SHGC_area_west = 0
        
        self.WallAreaNorthWest = 0
        self.WallAreaNorthWestHeight = 0
        self.WindowAreaNorthWest = 0
        self.WindowAreaNorthWestHeight = 0
        self.WindowUVWeightedNorthWest = 0
        self.WindowSHGCWeightedNorthWest = 0
        self._UV_area_northwest = 0
        self._SHGC_area_northwest = 0
        
        self.TotalOtherOpeningArea = 0
        self.TotalOtherOpeningAreaHeight = 0
        
        # Roof features
        self.TotalRoofArea = 0
        self.TotalRoofAreaHeight = 0 
        
        # Raised floor feature
        self.TotalRaiseFloorArea = 0
        self.TotalRaisedFloorAreaHeight = 0
        
        # interior floor feature
        self.TotalInteriorFloorArea = 0
        self.TotalInteriorFloorAreaHeight = 0
        
        # slab on grade feature
        self.TotalSlabOnGradeArea = 0
        
        # underground slab feature
        self.TotalUnderGroundSlabArea = 0
        
        # shade features
        self.TotalShadeArea = 0
        self.TotalSouthShadeArea = 0
        self.TotalNorthShadeArea = 0
        self.TotalWestShadeArea = 0
        self.TotalEastShadeArea = 0

        # Lighting and Plug Load Efficiency       
        self.WeightedLightingEfficiency = 0
        self.WeightedPlugLoadEfficiency = 0

        # Predicting Targets:
        self.annualElectricity = 0
        self.annualFuel = 0
        
        self.CoolingJan = 0
        self.CoolingFeb = 0
        self.CoolingMar = 0
        self.CoolingApr = 0
        self.CoolingMay = 0
        self.CoolingJun = 0
        self.CoolingJuly = 0
        self.CoolingAug = 0
        self.CoolingSep = 0
        self.CoolingOct = 0
        self.CoolingNov = 0
        self.CoolingDec = 0
        
        self.HeatingJan = 0
        self.HeatingFeb = 0
        self.HeatingMar = 0
        self.HeatingApr = 0
        self.HeatingMay = 0
        self.HeatingJun = 0
        self.HeatingJuly = 0
        self.HeatingAug = 0
        self.HeatingSep = 0
        self.HeatingOct = 0
        self.HeatingNov = 0
        self.HeatingDec = 0

        # the results dictionary
        self.results_dict = OrderedDict()
        
        # the unit of the project is here
        self.get_basic_info(self._root)
        
        # get the window type dictionary
        self.windowTypeDict = {}

        # call sub-functions to get desired building features
        self.get_supporting_info(self._root)  
        self.get_surface_info(self._root)
        self.get_lighting_and_plugload_info(self._root)
#         self.get_hvac_info(self._root)
        self.get_results_info(self._root)

    def get_supporting_info(self,_root):
        '''
        get the supporting information for this project
        e.g. the window type dictionary that contains the UV value and SHGC
        '''
        window_type_all = _root.findall('{http://www.gbxml.org/schema}WindowType')
        for each_window_type in window_type_all:
            thisID = each_window_type.attrib['id']
            thisUV = float(each_window_type.find('{http://www.gbxml.org/schema}U-value').text)
            thisSHGC = float(each_window_type.find('{http://www.gbxml.org/schema}SolarHeatGainCoeff').text)
            
            # converting square meter to square foot for UV-value
            thisUV = thisUV / (3.28084 * 3.28084)
            self.windowTypeDict[thisID] = {'U-Value':thisUV,'SHGC':thisSHGC}
            
    def get_basic_info(self, _root):
        '''
        Get the basic information of the building XML file:
        Unit, BuildingType, Latitude, Longitude, City and Country,
        designHeatWeathIdRef and designCoolWeathIdRef
        
        Input: Root, the root of the xml file
        Output: update the self.results_dict
        '''
        
        # getting sub-roots:
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _building = _campus.find('{http://www.gbxml.org/schema}Building')
        _location = _campus.find('{http://www.gbxml.org/schema}Location')
        
        # The unit that users used for the project
        Unit = _root.attrib['lengthUnit']
        if Unit == 'Feet':
            Unit = 'IP'
            self.unit = Unit
        elif Unit == 'Meters':
            Unit = 'SI'
            self.unit = Unit
        self.results_dict['Unit'] = Unit

        # Building Type:
        self.BuildingType = _building.attrib['buildingType']
        self.results_dict['BuildingType'] = self.BuildingType

        # Latitude and Longitude:
        self.Longitude = _location.find('{http://www.gbxml.org/schema}Longitude').text
        self.Latitude = _location.find('{http://www.gbxml.org/schema}Latitude').text
        self.results_dict['Latitude'] = self.Latitude
        self.results_dict['Longitude'] = self.Longitude

        # City and County:
        self.CityAndCountry = _location.find('{http://www.gbxml.org/schema}Name').text
        self.results_dict['CityAndCountry'] = self.CityAndCountry

        # Climate Zone:
        self.designHeatWeathIdRef = _campus.attrib['designHeatWeathIdRef']
        self.designCoolWeathIdRef = _campus.attrib['designCoolWeathIdRef']   
        self.results_dict['designHeatWeathIdRef'] = self.designHeatWeathIdRef
        self.results_dict['designCoolWeathIdRef'] = self.designCoolWeathIdRef
        
        if self.convert_climate:
            # call Thor application converting the climate zone code
            # will significantly slow down parsing
            # don't turn this on in the batch mode
            thisClimateZone = self._get_climate_zone(self.designHeatWeathIdRef)
            self.results_dict['ClimateZone'] = thisClimateZone

    def _get_climate_zone(self, weather_id):
        script_dir = os.path.dirname(__file__)
        rel_path = r'ThorV2ConsoleBin\bin\Release\ThorV2Console.exe'
        thor_path = os.path.join(script_dir, rel_path)
        eachId = weather_id.split('-')[1]
        this_output = sb.check_output([thor_path,'getclimatezone',eachId,'2015'])
        thisClimateZone = this_output.strip().split(' ')[-1]
        return thisClimateZone
    
    def get_surface_info(self, _root):
        '''
        loop over all of the surface objects and parse data according to the type of the object
        now supporting 
            exterior wall
            roof
            raised floor
            interior floor
            slab on grade
            underground slab
            shade
        '''
        def safe_division(n, d):
            '''
            handle the case when window area is zero
            '''
            return n / d if d else 0

        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _surface_all = _campus.findall('{http://www.gbxml.org/schema}Surface')
        
        # Get the sub-roots:
        for eachObject in _surface_all:
            if eachObject.attrib['surfaceType'] == 'ExteriorWall':
                self.get_exterior_wall_info(eachObject)
            elif eachObject.attrib['surfaceType'] == 'Roof':
                self.get_roof_info(eachObject)
            elif eachObject.attrib['surfaceType'] == 'RaisedFloor':
                self.get_raised_floor_info(eachObject)
            elif eachObject.attrib['surfaceType'] == 'InteriorFloor':
                self.get_interior_floor_info(eachObject)
            elif eachObject.attrib['surfaceType'] == 'SlabOnGrade':
                self.get_slab_on_grade_info(eachObject)
            elif eachObject.attrib['surfaceType'] == 'UndergroundSlab':
                self.get_underground_slab_info(eachObject)
            elif eachObject.attrib['surfaceType'] == 'Shade':
                self.get_shade_info(eachObject)

        # Now we finished looping over all object
        # Calculate the weighted UV and SHGC for each direction
        self.WindowUVWeightedNorth = safe_division(self._UV_area_north , self.WindowAreaNorth)
        self.WindowSHGCWeightedNorth = safe_division(self._SHGC_area_north , self.WindowAreaNorth)
        
        self.WindowUVWeightedNorthEast = safe_division(self._UV_area_northeast , self.WindowAreaNorthEast)
        self.WindowSHGCWeightedNorthEast = safe_division(self._SHGC_area_northeast , self.WindowAreaNorthEast)
        
        self.WindowUVWeightedEast = safe_division(self._UV_area_east , self.WindowAreaEast)
        self.WindowSHGCWeightedEast = safe_division(self._SHGC_area_east , self.WindowAreaEast)
        
        self.WindowUVWeightedSouthEast = safe_division(self._UV_area_southeast , self.WindowAreaSouthEast)
        self.WindowSHGCWeightedSouthEast = safe_division(self._SHGC_area_southeast ,self.WindowAreaSouthEast)
        
        self.WindowUVWeightedSouth = safe_division(self._UV_area_south , self.WindowAreaSouth)
        self.WindowSHGCWeightedSouth = safe_division(self._SHGC_area_south , self.WindowAreaSouth)
        
        self.WindowUVWeightedSouthWest = safe_division(self._UV_area_southwest , self.WindowAreaSouthWest)
        self.WindowSHGCWeightedSouthWest = safe_division(self._SHGC_area_southwest , self.WindowAreaSouthWest)
        
        self.WindowUVWeightedWest = safe_division(self._UV_area_west , self.WindowAreaWest)
        self.WindowSHGCWeightedWest = safe_division(self._SHGC_area_west , self.WindowAreaWest)
        
        self.WindowUVWeightedNorthWest = safe_division(self._UV_area_northwest , self.WindowAreaNorthWest)
        self.WindowSHGCWeightedNorthWest = safe_division(self._SHGC_area_northwest , self.WindowAreaNorthWest)

        # Dump Data    
        self.results_dict['TotalWallArea'] = self.TotalWallArea
        self.results_dict['TotalWallAreaHeight'] = self.TotalWallAreaHeight
        
        self.results_dict['WallAreaNorth'] = self.WallAreaNorth
        self.results_dict['WallAreaNorthHeight'] = self.WallAreaNorthHeight
        self.results_dict['WallAreaNorthEast'] = self.WallAreaNorthEast
        self.results_dict['WallAreaNorthEastHeight'] = self.WallAreaNorthEastHeight
        self.results_dict['WallAreaEast'] = self.WallAreaEast
        self.results_dict['WallAreaEastHeight'] = self.WallAreaEastHeight
        self.results_dict['WallAreaSouthEast'] = self.WallAreaSouthEast
        self.results_dict['WallAreaSouthEastHeight'] = self.WallAreaSouthEastHeight
        self.results_dict['WallAreaSouth'] = self.WallAreaSouth
        self.results_dict['WallAreaSouthHeight'] = self.WallAreaSouthHeight
        self.results_dict['WallAreaSouthWest'] = self.WallAreaSouthWest
        self.results_dict['WallAreaSouthWestHeight'] = self.WallAreaSouthWestHeight
        self.results_dict['WallAreaWest'] = self.WallAreaWest
        self.results_dict['WallAreaWestHeight'] = self.WallAreaWestHeight
        self.results_dict['WallAreaNorthWest'] = self.WallAreaNorthWest
        self.results_dict['WallAreaNorthWestHeight'] = self.WallAreaNorthWestHeight
        
        self.results_dict['TotalWindowArea'] = self.TotalWindowArea
        self.results_dict['TotalWindowAreaHeight'] = self.TotalWindowAreaHeight
        
        self.results_dict['WindowAreaNorth'] = self.WindowAreaNorth
        self.results_dict['WindowAreaNorthHeight'] = self.WindowAreaNorthHeight
        self.results_dict['WindowUVWeightedNorth'] = self.WindowUVWeightedNorth
        self.results_dict['WindowSHGCWeightedNorth'] = self.WindowSHGCWeightedNorth
        
        self.results_dict['WindowAreaNorthEast'] = self.WindowAreaNorthEast
        self.results_dict['WindowAreaNorthEastHeight'] = self.WindowAreaNorthEastHeight
        self.results_dict['WindowUVWeightedNorthEast'] = self.WindowUVWeightedNorthEast
        self.results_dict['WindowSHGCWeightedNorthEast'] = self.WindowSHGCWeightedNorthEast
        
        self.results_dict['WindowAreaEast'] = self.WindowAreaEast
        self.results_dict['WindowAreaEastHeight'] = self.WindowAreaEastHeight
        self.results_dict['WindowUVWeightedEast'] = self.WindowUVWeightedEast
        self.results_dict['WindowSHGCWeightedEast'] = self.WindowSHGCWeightedEast
        
        self.results_dict['WindowAreaSouthEast'] = self.WindowAreaSouthEast
        self.results_dict['WindowAreaSouthEastHeight'] = self.WindowAreaSouthEastHeight
        self.results_dict['WindowUVWeightedSouthEast'] = self.WindowUVWeightedSouthEast
        self.results_dict['WindowSHGCWeightedSouthEast'] = self.WindowSHGCWeightedSouthEast
        
        self.results_dict['WindowAreaSouth'] = self.WindowAreaSouth
        self.results_dict['WindowAreaSouthHeight'] = self.WindowAreaSouthHeight
        self.results_dict['WindowUVWeightedSouth'] = self.WindowUVWeightedSouth
        self.results_dict['WindowSHGCWeightedSouth'] = self.WindowSHGCWeightedSouth
        
        self.results_dict['WindowAreaSouthWest'] = self.WindowAreaSouthWest
        self.results_dict['WindowAreaSouthWestHeight'] = self.WindowAreaSouthWestHeight
        self.results_dict['WindowUVWeightedSouthWest'] = self.WindowUVWeightedSouthWest
        self.results_dict['WindowSHGCWeightedSouthWest'] = self.WindowSHGCWeightedSouthWest
        
        self.results_dict['WindowAreaWest'] = self.WindowAreaWest
        self.results_dict['WindowAreaWestHeight'] = self.WindowAreaWestHeight
        self.results_dict['WindowUVWeightedWest'] = self.WindowUVWeightedWest
        self.results_dict['WindowSHGCWeightedWest'] = self.WindowSHGCWeightedWest
        
        self.results_dict['WindowAreaNorthWest'] = self.WindowAreaNorthWest
        self.results_dict['WindowAreaNorthWestHeight'] = self.WindowAreaNorthWestHeight
        self.results_dict['WindowUVWeightedNorthWest'] = self.WindowUVWeightedNorthWest
        self.results_dict['WindowSHGCWeightedNorthWest'] = self.WindowSHGCWeightedNorthWest
        
        self.results_dict['TotalOtherOpeningArea'] = self.TotalOtherOpeningArea
        self.results_dict['TotalOtherOpeningAreaHeight'] = self.TotalOtherOpeningAreaHeight
        
        self.results_dict['TotalRoofArea'] = self.TotalRoofArea
        self.results_dict['TotalRoofAreaHeight'] = self.TotalRoofAreaHeight

        self.results_dict['TotalRaiseFloorArea'] = self.TotalRaiseFloorArea
        self.results_dict['TotalRaisedFloorAreaHeight'] = self.TotalRaisedFloorAreaHeight

        self.results_dict['TotalInteriorFloorArea'] = self.TotalInteriorFloorArea
        self.results_dict['TotalInteriorFloorAreaHeight'] = self.TotalInteriorFloorAreaHeight

        self.results_dict['TotalSlabOnGradeArea'] = self.TotalSlabOnGradeArea
        self.results_dict['TotalUnderGroundSlabArea'] = self.TotalUnderGroundSlabArea
        
        self.results_dict['TotalShadeArea'] = self.TotalShadeArea
        self.results_dict['TotalSouthShadeArea'] = self.TotalSouthShadeArea
        self.results_dict['TotalNorthShadeArea'] = self.TotalNorthShadeArea
        self.results_dict['TotalWestShadeArea'] = self.TotalWestShadeArea
        self.results_dict['TotalEastShadeArea'] = self.TotalEastShadeArea
        
    def get_exterior_wall_info(self, exteriorWallObject):
        '''
        Get the Information of Exterior Wall/Window
        '''
        this_wall_area = 0 # Total Wall Area for this Surface (surface area - window area)
        
        # For this surface            
        ThisSurface = ExteriorWall(exteriorWallObject, self.unit)
        
        this_surface_area = ThisSurface.Area # Total Surface Area for this Surface
        this_angle = ThisSurface.angle # The direction of this surface in degree
        this_area_height = ThisSurface.AreaHeight # the area * level for this surface
        this_surface_level = ThisSurface.level
        
        # For every window on this surface
        ThisWindow = Window(exteriorWallObject, this_surface_level, self.windowTypeDict, self.unit)
        this_window_area = ThisWindow.WindowArea # Total Window Area for this Surface
        this_window_area_height = ThisWindow.WindowAreaHeight # the area of the window * level for this surface
        
        # For every other opening area:
        this_other_area = ThisWindow.OtherArea
        this_other_area_height = ThisWindow.OtherAreaHeight
        
        # Calculate the area of the wall by minus the area of the windows and the area of other opening from the wall
        this_wall_area = this_surface_area - this_window_area - this_other_area
        this_wall_area_height = this_area_height - this_window_area_height - this_other_area_height
        
        # Update the overall building wall area and window area
        self.TotalWallArea += this_wall_area
        self.TotalWindowArea += this_window_area
        
        self.TotalWallAreaHeight += this_wall_area_height
        self.TotalWindowAreaHeight += this_window_area_height
        
        self.TotalOtherOpeningArea += ThisWindow.OtherArea
        self.TotalOtherOpeningAreaHeight += ThisWindow.OtherAreaHeight
        
        if (this_angle >= 0 and this_angle < 22.5) or (this_angle <= 360 and this_angle >= 337.5):
            self.WallAreaNorth += this_wall_area
            self.WallAreaNorthHeight += this_wall_area_height
            self.WindowAreaNorth += this_window_area
            self.WindowAreaNorthHeight += this_window_area_height
            self._UV_area_north += ThisWindow.WindowUVArea
            self._SHGC_area_north += ThisWindow.WindowSHGCArea 
        
        elif (this_angle >= 22.5 and this_angle < 67.5):
            self.WallAreaNorthEast += this_wall_area
            self.WallAreaNorthEastHeight += this_wall_area_height
            self.WindowAreaNorthEast += this_window_area
            self.WindowAreaNorthEastHeight += this_window_area_height
            self._UV_area_northeast += ThisWindow.WindowUVArea
            self._UV_area_northeast += ThisWindow.WindowSHGCArea
        
        elif (this_angle >= 67.5 and this_angle < 112.5):
            self.WallAreaEast += this_wall_area
            self.WallAreaEastHeight += this_wall_area_height
            self.WindowAreaEast += this_window_area
            self.WindowAreaEastHeight += this_window_area_height
            self._UV_area_east += ThisWindow.WindowUVArea
            self._SHGC_area_east += ThisWindow.WindowSHGCArea
           
        elif (this_angle >= 112.5 and this_angle < 157.5):
            self.WallAreaSouthEast += this_wall_area
            self.WallAreaSouthEastHeight += this_wall_area_height
            self.WindowAreaSouthEast += this_window_area
            self.WindowAreaSouthEastHeight += this_window_area_height
            self._UV_area_southeast += ThisWindow.WindowUVArea
            self._SHGC_area_southeast += ThisWindow.WindowSHGCArea
        
        elif (this_angle >= 157.5 and this_angle < 202.5):
            self.WallAreaSouth += this_wall_area
            self.WallAreaSouthHeight += this_wall_area_height
            self.WindowAreaSouth += this_window_area
            self.WindowAreaSouthHeight += this_window_area_height
            self._UV_area_south += ThisWindow.WindowUVArea
            self._SHGC_area_south += ThisWindow.WindowSHGCArea
        
        elif (this_angle >= 202.5 and this_angle < 247.5):
            self.WallAreaSouthWest += this_wall_area
            self.WallAreaSouthWestHeight += this_wall_area_height
            self.WindowAreaSouthWest += this_window_area
            self.WindowAreaSouthWestHeight += this_window_area_height
            self._UV_area_southwest += ThisWindow.WindowUVArea
            self._SHGC_area_southwest += ThisWindow.WindowSHGCArea
           
        elif (this_angle >= 247.5 and this_angle < 292.5):
            self.WallAreaWest += this_wall_area
            self.WallAreaWestHeight += this_wall_area_height
            self.WindowAreaWest += this_window_area
            self.WindowAreaWestHeight += this_window_area_height
            self._UV_area_west += ThisWindow.WindowUVArea
            self._SHGC_area_west += ThisWindow.WindowSHGCArea
           
        elif (this_angle >= 292.5 and this_angle < 337.5):
            self.WallAreaNorthWest += this_wall_area
            self.WallAreaNorthWestHeight += this_wall_area_height
            self.WindowAreaNorthWest += this_window_area
            self.WindowAreaNorthWestHeight += this_window_area_height   
            self._UV_area_northwest += ThisWindow.WindowUVArea
            self._SHGC_area_northwest += ThisWindow.WindowSHGCArea 
           
        else: raise ValueError("Azimuth's range is wrong")

    def get_roof_info(self, roofObject):
        '''
        Get the geometry information for roof
        '''        

        thisRoof = Roof(roofObject, self.unit)
        
        self.TotalRoofArea += thisRoof.RoofArea
        self.TotalRoofAreaHeight += thisRoof.heightArea   
 
    def get_raised_floor_info(self,raisedfloorObject):  
        ''' 
        get the raised floor area info
        '''  
        thisRaisedFloor = RaisedFloor(raisedfloorObject,self.unit)
        self.TotalRaiseFloorArea += thisRaisedFloor.Area
        self.TotalRaisedFloorAreaHeight += thisRaisedFloor.heightArea
  
    def get_interior_floor_info(self,interiorfloorObject):
        '''
        get the interior floor information
        '''

        thisInteriorFloor = InteriorFloor(interiorfloorObject,self.unit)
        self.TotalInteriorFloorArea += thisInteriorFloor.Area
        self.TotalInteriorFloorAreaHeight += thisInteriorFloor.heightArea
    
    def get_underground_slab_info(self,undergroundslabObject):
        '''
        get the underground slab info
        '''
        thisUnderGroundSlab = UndergroundSlab(undergroundslabObject, self.unit)
        self.TotalUnderGroundSlabArea += thisUnderGroundSlab.Area

    def get_slab_on_grade_info(self,slabongradeObject):   
        '''
        get the slab on grade information
        '''
        thisSlabOnGrade = SlabOnGrade(slabongradeObject, self.unit)
        self.TotalSlabOnGradeArea += thisSlabOnGrade.Area

    
    def get_shade_info(self,shadeObject):
        '''
        get the shading area info (for four different directions)
        '''
        thisShade = Shade(shadeObject,self.unit)
        # update the total shade area of the building
        self.TotalShadeArea += thisShade.Area
        
        # the angle of this shading:
        this_angle = thisShade.angle
        
        if (this_angle >= 0 and this_angle < 45 ) or (this_angle <= 360 and this_angle >= 315):
            self.TotalNorthShadeArea += thisShade.Area
        
        elif (this_angle >= 45 and this_angle < 135):
            self.TotalEastShadeArea += thisShade.Area
        
        elif (this_angle >= 135 and this_angle < 225):
            self.TotalSouthShadeArea += thisShade.Area
           
        elif (this_angle >= 225 and this_angle < 315):
            self.TotalWestShadeArea += thisShade.Area
  
    def get_lighting_and_plugload_info(self,_root):
        '''
        getting the lighting efficiency information for each space
        '''
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _building = _campus.find('{http://www.gbxml.org/schema}Building')
        _space_all = _building.findall('{http://www.gbxml.org/schema}Space')
        
        TotalSpaceArea = 0
        TotalLightingEfficiencybySpaceArea = 0
        TotalPlugLoadEfficiencybySpaceArea = 0

        for eachSpace in _space_all:
            thisSpaceEfficiency = LightingandPlugLoadEfficiency(eachSpace, self.unit)
            TotalSpaceArea += thisSpaceEfficiency.SpaceArea
            TotalLightingEfficiencybySpaceArea += thisSpaceEfficiency.LightingPowerbySpaceArea
            TotalPlugLoadEfficiencybySpaceArea += thisSpaceEfficiency.PlugLoadPowerbySpaceArea

        self.WeightedLightingEfficiency = TotalLightingEfficiencybySpaceArea / TotalSpaceArea
        
        self.WeightedPlugLoadEfficiency = TotalPlugLoadEfficiencybySpaceArea / TotalSpaceArea
           
        #Dump data
        self.results_dict['WeightedLightingEfficiency'] = self.WeightedLightingEfficiency
        self.results_dict['WeightedPlugLoadEfficiency'] = self.WeightedPlugLoadEfficiency
        
    def get_results_info(self, _root):
        _results = _root.findall('{http://www.gbxml.org/schema}Results')
        
        TotalMonthlyCoolingLoad = [0] * 12
        TotalMonthlyHeatiingLoad = [0] * 12
        
        for eachResults in _results:
            try:
                if eachResults.attrib['id'] == 'Campus-2305001-1':
                    # Electricity, kBtu
                    thisElectricity = ElectricityResults(eachResults, self.unit)
                    self.annualElectricity = thisElectricity.AnnualElectricity

                elif eachResults.attrib['id'] == 'Campus-2306001-1':
                    # Nature Gas, kBtu
                    thisFuel = FuelResults(eachResults, self.unit)
                    self.annualFuel = thisFuel.AnnualFuel
                
                elif eachResults.attrib['resultsType'] == 'CoolingLoad' and eachResults.attrib['timeUnit'] == 'Month':
                    # getting the cooling load, need to sum up by different types, return a list
                    thisHeating = MonthlyHeating(eachResults, self.unit)   
                    TotalMonthlyCoolingLoad = map(operator.add, TotalMonthlyCoolingLoad,thisHeating.HeatingLoadResults)
                
                elif eachResults.attrib['resultsType'] == 'HeatLoad' and eachResults.attrib['timeUnit'] == 'Month':
                    # getting the heating load, need to sum up by different types, return a list
                    thisHeating = MonthlyHeating(eachResults, self.unit)   
                    TotalMonthlyHeatiingLoad = map(operator.add, TotalMonthlyHeatiingLoad,thisHeating.HeatingLoadResults)

            except KeyError: 
                continue
            
            # Dump data
            self.results_dict['Fuel Energy Use (KBtu)'] = self.annualFuel
            self.results_dict['Electric Energy Use (KBtu)'] = self.annualElectricity    
            
            self.results_dict['HeatingJan'] = TotalMonthlyHeatiingLoad[0]
            self.results_dict['HeatingFeb'] = TotalMonthlyHeatiingLoad[1]
            self.results_dict['HeatingMar'] = TotalMonthlyHeatiingLoad[2]
            self.results_dict['HeatingApr'] = TotalMonthlyHeatiingLoad[3]
            self.results_dict['HeatingMay'] = TotalMonthlyHeatiingLoad[4]
            self.results_dict['HeatingJun'] = TotalMonthlyHeatiingLoad[5]
            self.results_dict['HeatingJuly'] = TotalMonthlyHeatiingLoad[6]
            self.results_dict['HeatingAug'] = TotalMonthlyHeatiingLoad[7]
            self.results_dict['HeatingSep'] = TotalMonthlyHeatiingLoad[8]
            self.results_dict['HeatingOct'] = TotalMonthlyHeatiingLoad[9]
            self.results_dict['HeatingNov'] = TotalMonthlyHeatiingLoad[10]
            self.results_dict['HeatingDec'] = TotalMonthlyHeatiingLoad[11]
            
            self.results_dict['CoolingJan'] = TotalMonthlyCoolingLoad[0]
            self.results_dict['CoolingFeb'] = TotalMonthlyCoolingLoad[1]
            self.results_dict['CoolingMar'] = TotalMonthlyCoolingLoad[2]
            self.results_dict['CoolingApr'] = TotalMonthlyCoolingLoad[3]
            self.results_dict['CoolingMay'] = TotalMonthlyCoolingLoad[4]
            self.results_dict['CoolingJun'] = TotalMonthlyCoolingLoad[5]
            self.results_dict['CoolingJuly'] = TotalMonthlyCoolingLoad[6]
            self.results_dict['CoolingAug'] = TotalMonthlyCoolingLoad[7]
            self.results_dict['CoolingSep'] = TotalMonthlyCoolingLoad[8]
            self.results_dict['CoolingOct'] = TotalMonthlyCoolingLoad[9]
            self.results_dict['CoolingNov'] = TotalMonthlyCoolingLoad[10]
            self.results_dict['CoolingDec'] = TotalMonthlyCoolingLoad[11]
            
                
    def dump_to_csv(self, file_name):
        '''
        Save to file
        '''
        with open(file_name, 'wb') as myfile:
            thisWriter = csv.writer(myfile)
            thisWriter.writerow(self.results_dict.keys())
            thisWriter.writerow(self.results_dict.values())
            
if __name__ == '__main__':
    
    # Example:
    file = 'gbXMLFullDefaults.xml'
    thisParser = gbXMLparser(file, convert_climate=True)

    thisParser.dump_to_csv('test2.csv')
    
    # Batch Example:
#     folder_path = './gbXML_all/'
    
    
    
    
    
    
    