A: ALGORITHM IDENTIFICATION
Nearest neighbor algorithm 
Find the package closest to the hub.  Find the package closest to the first package.  Find the package closest to the second package. Find the package closest to the previous package until all packages have been routed and/or delivered.

B1: LOGIC COMMENTS
Import packages, distances, locations
Bind package ids with location ids
Create hashtable to store all package class data
Set delayed(packages 6,9,25,28,32)
requirement1= Packages 15, 14, 16, 20, 19,13 #must go out for delivery on the same truck
requirement1.append(34,24,26,22,21,12) #manualy added for best output
def function closesttohub(list):
	return closest package to hub from list which is unassigned
def function assignpackageclosestto(trucked,list,prevpackage)
	assign closest package to package from list which is unassigned to trucked
	return id of closest package to package from list which was unassigned
#Nearest neighbor 
    slot1=closesttohub(requirement1)
    slot2=assignpackageclosestto(1,requirement1,slot1)
    slot3= assignpackageclosestto (1,requirement1,slot2)
    slot4= assignpackageclosestto (1,requirement1,slot3)
    … #continue pattern until all ids have been assigned slot9 or slot10
    newcargo=[36,17,4,40,1,2,33,7,29,37,38,3,8,30]
    slot1=closesttohub(newcargo)
    slot2=assignpackageclosestto(2, newcargo,slot1)
    slot3= assignpackageclosestto (2, newcargo,slot2)
    slot4= assignpackageclosestto (2, newcargo,slot3)
     … #continue pattern until all ids have been assigned
Deliverpacakges();
    nextcargo=[28,6,32,31,10,27,35,13,39,23,11,18]
    slot1=closesttohub(newcargo)
    slot2=assignpackageclosestto(2, nextcargo, slot1)
    slot3= assignpackageclosestto (2, nextcargo, slot2)
    slot4= assignpackageclosestto (2, nextcargo, slot3)
     … #continue pattern until all ids have been assigned
#route remaining packages to truck 1
For x in packages:
	assign(1,x)
displayresults()

B2: DEVELOPMENT ENVIRONMENT
	In order to develop this project, I used Microsoft Visual Studio with Python 3.10 (64-bit) under Microsoft Windows 10 Operating System.  The PC I used was custom built with an 8 core AMD FX 8320 CPU, 8 GB of RAM, 256 GB solid state hard drive, AMD RX570 8GB GPU, with 3 monitors all using resolution of 1080P.   
I also tested the application using PyCharm to ensure compatibility across different integrated development environment.

B3: SPACE-TIME AND BIG-O
	The project currently runs in O(N^2) time complexity.   During the operation of the program there are many loops, however most loops only represent O(n) time complexity, because they are not nested loops.  
During operation the built in Python sorted function was used, which it self has O(n log n) time complexity.  During this operation all of n will be sorted using the sorted command.  
When the data is initially loaded there is a nested loop which binds the locations and the packages, this would perform as O(n log n) as well since there is log n locations for every n package.  In the worst-case scenario this binding would perform as O(n^2) but on average we could expect an ‘n’ to ‘log n’ ratio of packages and locations.  The best-case would-be O(n) if all packages went to the same location.
During the Nearest Neighbor algorithm our project has O(n^2) because for every package we route, we iterate through our entire list to find any package with a matching delivery location.  We do this for every package we assign through our nearest neighbor.  We also look through our entire list at the locations and choose the closest location.  
O(n^2) is the final time complexity of the project.

B4: SCALABILITY AND ADAPTABILITY
	The nearest neighbor algorithm will scale according to input values.  As the input values increases the time to process the data would also increase, however it will always remain at quadratic time.  This means when the data is doubled, the time taken to process will be fourfold.  This means this application would be efficient if the data remained relatively small.    This project takes approximately 0.0148868 seconds to process 40 packages going to 27 different locations.  This would indicate that about 5,000 addresses could be processed in less than 10 mins, however 10,000 would take almost 40 mins, using the same hardware as presented in this project.   

B5: SOFTWARE EFFICIENCY AND MAINTAINABILITY
The software is efficient and easy to maintain.  The program is separated into classes and functions.  Each part is grouped according to the logic of loading, processing, and displaying the data.  Any part of the application could be updated, modified, or changed in any way.  Integrating new features would be as simple as adding the new function or class and referencing it either in the loading functions at the begging, the processing parts in the center, or the displaying at the end.  There are six classes and 

B6: SELF-ADJUSTING DATA STRUCTURES
	    The class hashmap contains the hashtable function, insert method, search method, and total. Upon initialization, class hashmap allocates 40 packages set to the value of None.  Data will then be read from the cvs file and inserted into the hashtable.  The hashtable insert function will insert the package data into a list, which is stored in the class hashmap and index corresponds to the value of the id mod 40.  The program will accept any valid input and will change output accordingly.  The allocation will allow 40 packages to be routed and delivered.  If the input was over the 40 packages, the packages over 40 would override the existing packages in the hash table that corresponds to the id mod 40. For example, package #41 would override package #1.  The hash table modulo expression can easily be modified to allow any number of packages to be stored in the hash table with respect to local machine limits.  The strengths for this hashmap are that it is easy to implement, easy to modify to allow more packages, stores the packages in a modulus 1:1 mapping for the package id, and easy to access data.   O(1) time complexity.   The weakness is the lack of automation if you were to try to add more packages.  
	The location data uses a list as the data structure.  When importing the location data, the program creates a list of locations and creates a unique location id.  Then the location id is added to the package id under the variable ‘deliverylocationid’ when the address matches.  This is a self-adjusting data structure and will allow any number of locations to be added and will automatically bind all locations to packages.  
	The distance table is a python dictionary.  The key is created by taking the two-digit location id of the source location and joining it with the two digit location id of the destination location.  The distance table will output miles between the two locations.  The advantages of this are the amount of data which can be inserted and called on is only limited by machine hardware, in other words virtually unlimited. The disadvantage of the distance table is sometimes Ids can be one digit therefore always must be string formatted to return a two-digit value.  
	
C: ORIGINAL CODE
Code is original and provided in the main.py file.  WGUPSPackageFile.csv and WGUPSDistanceTable.csv are required to be in the same folder as main.py during execution of the python script.  The code does not have any warnings or errors.
C1: IDENTIFICATION INFORMATION

# WGUPS Routing Application
These identifying comments exist as the first line of the file named “main.py”. This includes the candidate’s correct first name, last name, and student ID.
C2: PROCESS AND FLOW COMMENTS
Comments are provided within the code that adequately and accurately explain the process and the flow of the program.

D:DATA STRUCTURE
	A class is created with the title ‘deliverycenter’.  Inside of ‘deliverycenter’ is an object name ‘hashtable’.  ‘hashtable’ is an instance of class ‘hashmap’, which contains hash functions to insert, search by id, and return the total number of allocated packages.  An object named wgups is created as an instance of ‘deliverycenter’.  The search by id is called ‘hashmap.package()’ This allow referencing packages in the ‘hashtable’ as ‘wgups.hashtable.package(id)’.  The insert function can be invoked by executing ‘wgups.hashtable.insert(id, package type)’.  The ‘wgups.hashtable.total’ will return the number of packages in the hash table.  Package type is an object of a class package.  The class package stores package id, address, zip code, city, kilo, notes, delayed data, deadline, status, and other delivery information. This hash table uses a list as the underlying data structure for the hash table.  The hash function will map out a 1:1 hash map without chaining using modulus 40. 
This can store all the package information all hash functions perform at constant time complexity (big O notation of O (1)).

D1: EXPLANATION OF DATA STRUCTURE
The ‘wgups.hashtable.pacakge(id)’ function will return the package which is stored in the hash table.  All of attributes of the package can be accessible through the hash function.  As the package is going through the function ‘dothework’ all data points are stored in the package.  Once all packages have been routed, the application will iterate through all packages and store all statistics in a table called bigresults.  This table will be used to display sortable data to the user interface in loglinear complexity (big O notation of O (n log n)). 

E: HASH TABLE
wgups.hashtable has an insertion function, without using any additional libraries or classes, that is free from errors and includes, as input, all of the given components. The function can be invoked using ‘wgups.hashtable.insert(id, package type)’

F: LOOK-UP FUNCTION
wgups.hashtable has a look-up function, without using any additional libraries or classes, that is free from errors and includes, as input, the package id. The function can be invoked using ‘wgups.hashtable.package(id)’ or ‘wgups.hashtable.searchby(id)’ .

G: INTERFACE
All menu keys are shown to the user.  The interface request either a time or a menu key.  If the user enters a menu key without a time, the interface will request for a time first.  Once a time is entered the user can view delivery results, which include all data points and allows the user to sort the results according to the data points.  The interface also allows the user to view each package and its delivery status.  The user can also view all distance data.  The user can view each delivery up to the time they entered.  If the user enters a value which is numeric but can not be a time, the computer changes the time to be valid.  If the user enters a letter which is not a menu key, then the options will appear again and the user will need to follow the onscreen options to continue.  
