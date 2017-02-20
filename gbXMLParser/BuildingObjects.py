'''
Created on Jul 25, 2016

@author: t_songr
'''

import xml.etree.cElementTree as ET

class ExteriorWall:
    '''
    Object of ExteriorWall in gbXML
    '''
    def __init__(self, ExteriorWallObject, unit):
        self.unit = unit
        
        self.Height = 0
        self.Width = 0
        self.angle = 0  # The direction of this surface in degree
        self.Area = 0 # Total Wall Area for this Surface
        self.level = 0
        self.AreaHeight = 0 # the area * level for this surface
        
        # Find all of the geometry for this wall
        self.this_RectangularGeometry_all = ExteriorWallObject.find('{http://www.gbxml.org/schema}RectangularGeometry')

        self.get_surface_geometery()
    
    def get_surface_geometery(self):
        # RectangularGeometry
        self.angle = float(self.this_RectangularGeometry_all.find('{http://www.gbxml.org/schema}Azimuth').text)
        self.Height = float(self.this_RectangularGeometry_all.find('{http://www.gbxml.org/schema}Height').text)
        self.Width = float(self.this_RectangularGeometry_all.find('{http://www.gbxml.org/schema}Width').text)
        self.level = float(self.this_RectangularGeometry_all.find('{http://www.gbxml.org/schema}CartesianPoint')[-1].text) # the level is always the last element in the list

        if self.unit == 'SI':

            # Convert meter to feet
            self.Height = self.Height * 3.28084
            self.Width = self.Width * 3.28084
            self.level = self.level * 3.28084 # why is this times 3.28084 as well?
            
        self.Area = self.Height *  self.Width
        self.AreaHeight = self.Area * self.level
  
class Window:
    '''
    Get the windows geometry from the exterior wall object
    '''
    def __init__(self, ExteriorWallObject, SurfaceLevel, WindowTypeDict,unit):
        self.unit = unit
        
        self.WindowArea = 0
        self.OtherArea = 0
        self.Height = 0
        self.Width = 0
        self.SurfaceLevel = SurfaceLevel # The level of the surface that the window is on
        self.level = 0 
        self.WindowAreaHeight = 0
        self.OtherAreaHeight = 0
        
        self.WindowTypeDict = WindowTypeDict
        self.WindowType = None
        self.WindowUV = 0
        self.WindowSHGC = 0
        self.WindowUVArea = 0
        self.WindowSHGCArea = 0
        
        self.this_window_all = ExteriorWallObject.findall('{http://www.gbxml.org/schema}Opening')

        self.get_window_geometry_and_type_value()

    def get_window_geometry_and_type_value(self):
        '''
        Get the geometry for each window
        Add AreaUV feature and the AreaSHGC feature
        '''
        
        for eachWindow in self.this_window_all:
            
            # find the geometry and window type
            this_geo = eachWindow.find('{http://www.gbxml.org/schema}RectangularGeometry')
            
            # deal with only windows
            if eachWindow.attrib['openingType'] == 'FixedWindow':
                # find the window type
                self.WindowType = eachWindow.attrib['windowTypeIdRef']
                self.WindowUV = self.WindowTypeDict[self.WindowType]['U-Value']
                self.WindowSHGC = self.WindowTypeDict[self.WindowType]['SHGC']
                
                # find the geometry
                self.Height = float(this_geo.find('{http://www.gbxml.org/schema}Height').text)
                self.Width = float(this_geo.find('{http://www.gbxml.org/schema}Width').text)
                # the level of the windows is built based on the level of the wall
                self.level = self.SurfaceLevel + float(this_geo.find('{http://www.gbxml.org/schema}CartesianPoint')[-1].text)
    
                if self.unit =='SI':
                    self.Height = self.Height * 3.28084
                    self.Width = self.Width * 3.28084
                    self.level  = self.level * 3.28084 # Double Accounting?????
                    
                self.WindowArea = self.Height * self.Width
                self.WindowAreaHeight = self.WindowArea * self.level
                self.WindowUVArea = self.WindowArea * self.WindowUV
                self.WindowSHGCArea = self.WindowArea * self.WindowSHGC
            
            else: 
                ''' Deal with Other openings (like slide doors) '''
                self.Height = float(this_geo.find('{http://www.gbxml.org/schema}Height').text)
                self.Width = float(this_geo.find('{http://www.gbxml.org/schema}Width').text)
                self.level = self.SurfaceLevel + float(this_geo.find('{http://www.gbxml.org/schema}CartesianPoint')[-1].text)
                
                if self.unit =='SI':
                    self.Height = self.Height * 3.28084
                    self.Width = self.Width * 3.28084
                    self.level  = self.level * 3.28084 # Double Accounting?????
                
                self.OtherArea = self.Height * self.Width
                self.OtherAreaHeight = self.OtherArea * self.level
                
                
                
                
  
class Roof:
    def __init__(self,RoofObject, unit):
        self.unit = unit
        
        self.Height = 0
        self.Width = 0
        self.angle = 0
        self.RoofArea = 0
        self.level = 0
        self.Tilt = 0
        self.heightArea = 0
        
        self.this_geo = RoofObject.find('{http://www.gbxml.org/schema}RectangularGeometry')
        self.get_roof_geometry()
    
    def get_roof_geometry(self):
        self.Height = float(self.this_geo.find('{http://www.gbxml.org/schema}Height').text)
        self.Width = float(self.this_geo.find('{http://www.gbxml.org/schema}Width').text)
        self.angle = float(self.this_geo.find('{http://www.gbxml.org/schema}Azimuth').text)
        self.Tilt = float(self.this_geo.find('{http://www.gbxml.org/schema}Tilt').text)
        self.level = float(self.this_geo.find('{http://www.gbxml.org/schema}CartesianPoint')[-1].text)
        
        if self.unit == 'SI':
            # Convert meter to feet
            self.Height = self.Height * 3.28084
            self.Width = self.Width * 3.28084
            self.level = self.level * 3.28084 # why is this times 3.28084 as well?
  
        self.RoofArea = self.Height * self.Width
        self.heightArea = self.RoofArea * self.level

class RaisedFloor:
    def __init__(self,RaisedFloorObject, unit):
        self.unit = unit
        self.Height = 0
        self.Width = 0
        self.level = 0
        self.tilt = 0
        self.Area = 0
        self.heightArea = 0
        
        self.this_geo = RaisedFloorObject.find('{http://www.gbxml.org/schema}RectangularGeometry')
        self.get_raised_floor_geometry()
    
    def get_raised_floor_geometry(self):
        
        self.Height = float(self.this_geo.find('{http://www.gbxml.org/schema}Height').text)
        self.Width = float(self.this_geo.find('{http://www.gbxml.org/schema}Width').text)
        self.Tilt = float(self.this_geo.find('{http://www.gbxml.org/schema}Tilt').text)
        
        self.level = float(self.this_geo.find('{http://www.gbxml.org/schema}CartesianPoint')[-1].text)
        
        if self.unit == 'SI':

            # Convert meter to feet
            self.Height = self.Height * 3.28084
            self.Width = self.Width * 3.28084
            self.level = self.level * 3.28084 # why is this times 3.28084 as well?
  
        self.Area = self.Height * self.Width
        self.heightArea = self.Area * self.level       

class InteriorFloor:
    def __init__(self,InteriorFloorObject, unit):
        self.unit = unit
        self.Height = 0
        self.Width = 0
        self.level = 0
        self.tilt = 0
        
        self.Area = 0
        self.heightArea = 0
        
        self.this_geo = InteriorFloorObject.find('{http://www.gbxml.org/schema}RectangularGeometry')
        self.get_interior_floor_geometry()
        
    def get_interior_floor_geometry(self):
        self.Height = float(self.this_geo.find('{http://www.gbxml.org/schema}Height').text)
        self.Width = float(self.this_geo.find('{http://www.gbxml.org/schema}Width').text)
        self.Tilt = float(self.this_geo.find('{http://www.gbxml.org/schema}Tilt').text)
        
        self.level = float(self.this_geo.find('{http://www.gbxml.org/schema}CartesianPoint')[-1].text)
        
        if self.unit == 'SI':
            # Convert meter to feet
            self.Height = self.Height * 3.28084
            self.Width = self.Width * 3.28084
            self.level = self.level * 3.28084 # why is this times 3.28084 as well?
  
        self.Area = self.Height * self.Width
        self.heightArea = self.Area * self.level   
  
class SlabOnGrade:
    def __init__(self, SlabOnGradeObject, unit ):
        self.unit = unit
        self.Height = 0
        self.Width = 0
        self.level = 0
        self.tilt = 0
        
        self.Area = 0
        self.heightArea = 0
        
        self.this_geo = SlabOnGradeObject.find('{http://www.gbxml.org/schema}RectangularGeometry')
        self.get_slab_on_grade_geometry()
    
    def get_slab_on_grade_geometry(self):
        self.Height = float(self.this_geo.find('{http://www.gbxml.org/schema}Height').text)
        self.Width = float(self.this_geo.find('{http://www.gbxml.org/schema}Width').text)
        self.Tilt = float(self.this_geo.find('{http://www.gbxml.org/schema}Tilt').text)
        self.level = float(self.this_geo.find('{http://www.gbxml.org/schema}CartesianPoint')[-1].text)
        
        if self.unit == 'SI':
            # Convert meter to feet
            self.Height = self.Height * 3.28084
            self.Width = self.Width * 3.28084
            self.level = self.level * 3.28084 # why is this times 3.28084 as well?
        
        self.Area = self.Height * self.Width
        self.heightArea = self.Area * self.level  

class UndergroundSlab:
    def __init__(self, UndergroundSlabObject ,unit):
        self.unit = unit
        self.Height = 0
        self.Width = 0
        self.Tilt = 0
        
        self.Area = 0
        
        self.this_geo = UndergroundSlabObject.find('{http://www.gbxml.org/schema}RectangularGeometry')
        self.get_underground_slab_geometry()
        
    def get_underground_slab_geometry(self):
        self.Height = float(self.this_geo.find('{http://www.gbxml.org/schema}Height').text)
        self.Width = float(self.this_geo.find('{http://www.gbxml.org/schema}Width').text)
        self.Tilt = float(self.this_geo.find('{http://www.gbxml.org/schema}Tilt').text)
                
        if self.unit == 'SI':
            # Convert meter to feet
            self.Height = self.Height * 3.28084
            self.Width = self.Width * 3.28084
        
        self.Area = self.Height * self.Width

class Shade:
    def __init__(self, ShadeObject, unit):
        self.unit = unit
        
        self.Height = 0
        self.Width = 0
        self.Tilt = 0
        self.angle = 0
        
        self.Area = 0
        
        self.this_geo = ShadeObject.find('{http://www.gbxml.org/schema}RectangularGeometry')
        self.get_shade_geometry()
        
    def get_shade_geometry(self):
        self.Height = float(self.this_geo.find('{http://www.gbxml.org/schema}Height').text)
        self.Width = float(self.this_geo.find('{http://www.gbxml.org/schema}Width').text)
        self.Tilt = float(self.this_geo.find('{http://www.gbxml.org/schema}Tilt').text)
        self.angle = float(self.this_geo.find('{http://www.gbxml.org/schema}Azimuth').text)
        
        if self.unit == 'SI':
            # Convert meter to feet
            self.Height = self.Height * 3.28084
            self.Width = self.Width * 3.28084
        self.Area = self.Height * self.Width

class LightingandPlugLoadEfficiency:
    '''
    Class of lighting efficiency for each space
    Key word: LightPowerPerArea
    '''
    def __init__(self, SpaceObject, unit):
        self.unit = unit
        self.SpaceObject = SpaceObject        
        self.SpaceArea = 0 
        
        self.LightingPower = 0
        self.LightingPowerbySpaceArea = 0
        
        self.PlugLoadPower = 0
        self.PlugLoadPowerbySpaceArea = 0

        self.lightingObject = self.SpaceObject.find('{http://www.gbxml.org/schema}LightPowerPerArea')
        self.plugloadObject = self.SpaceObject.find('{http://www.gbxml.org/schema}EquipPowerPerArea')
        
   
        if self.lightingObject is not None and self.plugloadObject is not None: # might overlook some data here, but doesn't affect much
            self.efficiency_unit = self.SpaceObject.find('{http://www.gbxml.org/schema}LightPowerPerArea').attrib['unit']
            self.get_lighting_plugload_efficiency()

    def get_lighting_plugload_efficiency(self):
        '''
        Get the lighting efficiency times the area of the space
        '''
        self.SpaceArea = float(self.SpaceObject.find('{http://www.gbxml.org/schema}Area').text)
        self.LightingPower = float(self.lightingObject.text)
        self.PlugLoadPower = float(self.plugloadObject.text)
        
        if self.unit == 'SI':
            # Convert meter to feet
            self.SpaceArea = self.SpaceArea * 3.28084 * 3.28084
        
        # convert the unit to WattPerSqureFeet here if the efficiency unit is WattPerSquareMeter
        if self.efficiency_unit == 'WattPerSquareMeter':
            self.LightingPower = self.LightingPower/(3.28084 * 3.28084) 
            self.PlugLoadPower = self.PlugLoadPower/(3.28084 * 3.28084) 
        
        self.LightingPowerbySpaceArea = self.SpaceArea * self.LightingPower
        self.PlugLoadPowerbySpaceArea = self.SpaceArea * self.PlugLoadPower

class ElectricityResults: 
    def __init__(self, ResultsObject, unit):
        '''
        Get the annual total electricity consumption and kbtu
        '''
        self.AnnualElectricity = 0
        self.unit = unit
        self.get_electricity(ResultsObject)

    def get_electricity(self, thisResultsObject):
        '''
        Get the training target
        Electricity and Fuel
        '''
        self.AnnualElectricity = float(thisResultsObject.find('{http://www.gbxml.org/schema}Value').text) * 3.41214 # kwh to kBtu

class FuelResults: 
    def __init__(self, ResultsObject, unit):
        '''
        Get the annual total electricity consumption and kbtu
        '''
        self.AnnualFuel = 0
        self.unit = unit
        self.get_fuel(ResultsObject)

    def get_fuel(self, thisResultsObject):
        '''
        Get the training target
        Electricity and Fuel
        '''
        self.AnnualFuel = float(thisResultsObject.find('{http://www.gbxml.org/schema}Value').text) # kwh to kBtu
        
        if self.unit == 'SI':
            self.AnnualFuel = self.AnnualFuel * (0.0009478171/1000) # joules to kbtu
        elif self.unit == 'IP':
            self.AnnualFuel = self.AnnualFuel / 1000 # btu to kbtu
            
class MonthlyHeating:
    def __init__(self, HeatingObject, unit):
        self.unit = unit
        self.HeatingLoadResults = []
        self.get_monthly_heating(HeatingObject)
    
    def get_monthly_heating(self, thisHeatingObject):
        
        values = thisHeatingObject.findall('{http://www.gbxml.org/schema}Value')
        for eachValue in values:
            thisHeating = float(eachValue.text)
            if self.unit == 'SI':
                # joule to BTU:
                thisHeating = thisHeating * 0.0009478171
            self.HeatingLoadResults.append(thisHeating/1000) # convert to kBTU
            
class MonthlyCooling:
    def __init__(self, CoolingObject, unit):
        self.unit = unit
        self.HeatingLoadResults = []
        self.get_monthly_heating(CoolingObject)
    
    def get_monthly_heating(self, thisCoolingObject):
        
        values = thisCoolingObject.findall('{http://www.gbxml.org/schema}Value')
        for eachValue in values:
            thisCooling = float(eachValue.text)
            if self.unit == 'SI':
                # joule to BTU:
                thisCooling = thisCooling * 0.0009478171
                
            self.HeatingLoadResults.append(thisCooling/1000) # convert to kBTU
        
        
        
        
    
    
    
    
    
    
    