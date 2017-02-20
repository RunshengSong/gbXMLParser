'''
Created on Jul 28, 2016

Parser in Batch Mode. And out put to csv file.
@author: t_songr
'''
import zipfile
import gbXMLParser
import os
import csv
import subprocess as sb

class BatchParser:
    def __init__(self, source_folder, csv_file_name, save_mod = 'wb'):
        '''
        Source folder: the source folder of the downloaded zip file
        csv_file_name: the file name you would like to save in csv
        save_mod: the mode that the csv will be saved. wb for a new csv file 
        and a for appending to existing files
        '''
        self.save_mod = save_mod
        self.csv_file_name = csv_file_name
        self.source_folder = source_folder
        self.unzipped_temp_folder = './~temp'
        self.climatezonedict = {}
        
        self.parse_all()
    
    def _unzip_to_temp(self, full_path_zipped):
        '''
        Unzip to a temp folder in the project folder
        full_path_zipped: full path name of the zipped file
         '''
        thisZip = zipfile.ZipFile(full_path_zipped,'r')
        thisZip.extractall(self.unzipped_temp_folder)
        thisZip.close()
        
    def parse_file_in_temp(self):
        '''
        parse the gbXML in the temp folder, return the dictionary
        '''
        full_path_temp_gbxml = self.unzipped_temp_folder +'/'+ 'gbXMLStandard.xml'
        thisParser = gbXMLParser.gbXMLparser(full_path_temp_gbxml, convert_climate = False)
        os.remove(full_path_temp_gbxml)
        return thisParser.results_dict
    
    def _get_climate_zone(self, weather_id):
        script_dir = os.path.dirname(__file__)
        rel_path = r'ThorV2ConsoleBin\bin\Release\ThorV2Console.exe'
        thor_path = os.path.join(script_dir, rel_path)
        eachId = weather_id.split('-')[1]
        this_output = sb.check_output([thor_path,'getclimatezone',eachId,'2015'])
        thisClimateZone = this_output.strip().split(' ')[-1]
        self.climatezonedict[weather_id] = thisClimateZone
        return thisClimateZone

    def parse_all(self):
        '''
        iter over the source folder that contain the zipped files
        unzip every file to temp folder
        parse it, save it to csv 
        then delete the temp folder
        '''
        with open(self.csv_file_name,self.save_mod) as myfile:
            thisWriter = csv.writer(myfile)
            count = 0
        
            for path, subdirs, files in os.walk(self.source_folder):
                for eachFiles in files:
                    count += 1
                    
                    full_path_zipped = path + '/' + eachFiles
                    project_id = eachFiles.split('-')[1].split('.')[0]
                    print count, 'Parsing', project_id
                    
                    self._unzip_to_temp(full_path_zipped)
                    this_results_dict = self.parse_file_in_temp()
                    
                    # try to get the climate id from the dictionary 
                    try:
                        thisClimateZone = self.climatezonedict[this_results_dict['designCoolWeathIdRef']]
                    except KeyError:
                        # if this weather station is not in the dictionary yet, run the Thor program and add that to the dictionary
                        thisClimateZone = self._get_climate_zone(this_results_dict['designCoolWeathIdRef'])
                    
                    # add the climate zone code
                    this_results_dict['ClimateZone'] = thisClimateZone

                    ''' if you are writing a new file and this is the first file '''
                    ''' write the header '''
                    if self.save_mod == 'wb' and count == 1:
                        thisWriter.writerow(['Project ID']+this_results_dict.keys())
                    
                    thisWriter.writerow([project_id]+this_results_dict.values())  
                    myfile.flush()
        
if __name__ == '__main__':
    ''' testing '''
    source_folder = 'C:/Users/t_songr/Box Sync/gbXMLData/new_data/zipped_files'
    thisBatch = BatchParser(source_folder,'test.csv','wb')
        
        
        
        
        
        
        
