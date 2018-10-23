import re
import os
import csv
import datetime, time
from datetime import datetime
import time

starting_dir = "/badc/glocaem/data"



def fixglocaem():
  
  for country in os.listdir(starting_dir):
    if country == 'aragats':    

      for resolution in os.listdir(os.path.join(starting_dir,country)):


          if resolution != '.ftp':

              if resolution != '00README_catalogue_and_licence.txt':

                  for year in os.listdir(os.path.join(starting_dir,country,resolution)):

                     if year != '00README_catalogue_and_licence.txt':


                         for month in os.listdir(os.path.join(starting_dir,country,resolution,year)):


                             for files in os.listdir(os.path.join(starting_dir,country,resolution,year,month)):


                                 glocaem_file = open(os.path.join(starting_dir,country,resolution,year,month,files))

                                                                
                                 filename, file_extension = os.path.splitext(files)
                                 newfilename = ''.join([filename, '_v2', file_extension])

                                                              


                                 newfile = open(newfilename,"w")

                                 lines = glocaem_file.readlines()


                                 newheader = ""

                                 for line1 in lines:
                                     #print "%%%%", line1
                                     pattern = re.search('(?P<years>[0-9.]*),(?P<months>[0-9.]*),(?P<day>[0-9.]*),(?P<hours>[0-9.]*),(?P<mins>[0-9.]*),(?P<sec>[0-9.]*),(?P<measurements>[0-9.,-]*)',line1) 

                                     if pattern:
                                         combined = addtime(line1,pattern)
                                         newheader = newheader +combined

                                         #print "newdata",newdata 


                                     #assuming everything else is a header
                                     else:

                                         match = re.search('Year,Mon,Day',line1)
                                         li = re.search('licence,G,',line1)
                                         ac = re.search('acknowledgement,G,',line1)

                                         if match:
                                            new = line1.replace("\n",',decimalhours\n')

                                            newheader = newheader + new


                                           # print "*match**", new

                                         elif line1 == "data,\n":
                                             newdataline = "long_name,decimalhours,time in decimal hours since begining of the year,\n"+ 'type,decimalhours,float\n'+ line1
                                             #print "%%data%%", newdataline
                                             newheader = newheader +newdataline



                                         elif li:

                                             newlicence = line1.replace("licence,G,Data are available in http://www.adei.crd.yerphi.am\n",'licence,G,Data are available under the Creative Commons Attribution licence (https://creativecommons.org/licenses/by-nc-sa/4.0/) - non commercial use only')
                                             #print "%%licence%%", newlicence
                                             newheader = newheader +newlicence



                                         elif ac:

                                             newack = line1.replace("acknowledgement,G,Acknowledgement of ASEC/YERPHI as the data provider is required whenever and wherever this data is used",'acknowledgement,G,GLOCAEM project partners (listed at https://glocaem.wordpress.com/introduction/project-partners-and-measurement-sites/) and Natural Environment Research Council (NERC) grant NE/N013689/1 for the provision of the GLOCAEM data')
                                             #print "%%acknoldge%%", newack
                                             newheader= newheader+newack

                                         else:


                                             newheader = newheader+line1 



                                 #print ' I am new the new file', newheader
                                 newfile.write(newheader)



   

                             
def addtime(line1, match):                                                           
   #pattern = re.compile('(?P<years>[0-9.]*),(?P<months>[0-9.]*),(?P<day>[0-9.]*),(?P<hours>[0-9.]*),(?P<mins>[0-9.]*),(?P<sec>[0-9.]*),(?P<measurements>[0-9.,-]*)',line1)

   #match = re.search(pattern,line1)
   if match:
       #print "^^^^^^", line1

       years = match.group('years')
       iyears = int(years)
       months = match.group('months')
       imonths = int(months)
       day = match.group('day')
       iday = int(day)
       hours = match.group('hours')
       ihours = int(hours)
       mins = match.group('mins') 
       imins = int(mins)
       sec = match.group('sec')
       isec = int(sec)
       measurements = match.group('measurements')


       timetrue = '{0}/{1}/{2} {3}:{4}:{5}'.format(iday,imonths,iyears,ihours,imins,isec)

       d = datetime.strptime(timetrue, "%d/%m/%Y %H:%M:%S")
       #print d


       convert = time.mktime(d.timetuple())

       timestart = "01/01/{} 00:00:00".format(years)

       startdt = datetime.strptime(timestart, "%d/%m/%Y %H:%M:%S")


       diff = d - startdt           

       totsecs = ((diff.days * (3600*24)) + diff.seconds)
       
       dechours = float(totsecs)/3600l


       combined =  str(iyears) + "," + str(imonths) + "," + str(iday) + "," + str(ihours) + "," + str(imins) + "," + str(isec) + "," + measurements + "," + str(dechours)+ '\n'

       #print combined

       return combined



if __name__=="__main__":
     fixglocaem()




