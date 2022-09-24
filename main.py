# Chad Self 000430387
# WGUPS Routing Application
# import csv for loading data from csv files
import csv


# package class created to host package data
class Package:
    def __init__(self, id, address, city, state, zipcode, deadline, kilo, notes="", status="At the Hub",
                 deliverylocationid=0):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.kilo = kilo
        self.notes = notes
        self.status = status
        self.deliverylocationid = deliverylocationid
        self.starttime = 800
        self.whodelivered = None
        self.routetime = 0
        self.delivertime = 0
        self.deliverynumber = 1
        self.deliveryticket = 0
        self.allmiles = 0
        self.beforeIDonroute = 0
        self.beforeLConroute = 0
        self.afteronIDroute = 0
        self.afteronLCroute = 0
        self.milesroad = 0
        self.totalmilesroad = 0
        self.lastwayhomemiles = 0
        self.hasbeenrouted = False
        if self.deadline != 'EOD':
            self.deadnum = deadline
        else:
            self.deadnum = 1700

    def setstarttime(self, newstart):
        self.starttime = newstart

    def printstatus(self):
        print(f'{self.starttime:04d}', self.id, self.address, self.city, self.state, self.zipcode, self.deadline,
              self.kilo, self.notes, '--->', 'routed at ', f'{self.routetime:04d}', self.status)

    def setdeliverylocationid(self, deliverylocationid):
        self.deliverylocationid = deliverylocationid

    def distancefrom(self, locationid):
        return distancedict[f'{self.deliverylocationid:02d}' + f'{locationid:02d}']

    def setstatus(self, newstatus):
        self.status = newstatus

    def setzipcode(self, newzip):
        self.zipcode = newzip

    def setnewaddress(self, newaddress):
        self.address = newaddress

    def sethasbeenrouted(self):
        self.hasbeenrouted = True


# truck class created to host truck data
class Truck:
    def __init__(self, truck_id):
        self.id = truck_id
        self.lastlocation = 1
        self.nextlocation = None
        self.cargo = []
        self.driver = None
        self.milesdriven = 0

    def addtocargo(self, packageid):
        self.cargo.append(packageid)

    def setdriver(self, driverid):
        self.driver = driverid


# driver class created to host driver data
class Driver:
    def __init__(self, id, name, truckid):
        self.id = id
        self.name = name
        self.truckid = truckid


# Location class creatd to host location data
class Location:
    def __init__(self, id, name, address, longname):
        self.id = id
        self.name = name
        self.address = address
        self.longname = longname

    def setlongaddress(self, longaddress):
        self.longaddress = longaddress


# hashmap created to host hashtable
class hashmap:
    def __init__(self):
        self.table = []
        self.modulus = 40
        for x in range(self.modulus):
            self.table.append(None)

    def insert(self, key, item):
        self.table[key % 40] = item

    def searchby(self, id):
        if self.table[id % self.modulus] != 0:
            return self.table[id % 40]

    def package(self, id):
        if self.table[id % self.modulus] != 0:
            return self.table[id % self.modulus]

    def total(self):
        return len(self.table)


# class deliverycenter created to host delivery center data
class deliverycenter:
    def __init__(self, opentime=800):
        self.opentime = opentime
        self.deliverynumber = 0
        self.Nowtime = opentime
        self.totalpackages = None
        self.undeliveredpackages = None
        self.delayedpackages = None
        self.deliveryticket = 0
        self.hashtable = hashmap()
        self.lastenteredtime = None
        self.locationlist = [Location(0, 'Name', 'Address', 'LongName')]
        self.deliverydata = []


# delayed function to set packages as delayed and assign possible start time
def delayed(packageid, until):
    wgups.hashtable.package(packageid).setstarttime(until)
    wgups.hashtable.package(packageid).setstatus('Delayed')


# assignPackage function to assign packages to truck cargo for delivery
def assignPackage(truckid, packageId):
    if (len(trucks[truckid].cargo) < 16) and (packageId != 0):
        if wgups.hashtable.package(packageId).hasbeenrouted == False:
            trucks[truckid].addtocargo(packageId)
            wgups.hashtable.package(packageId).setstatus('en route')
            wgups.hashtable.package(packageId).sethasbeenrouted()
            wgups.hashtable.package(packageId).routetime = wgups.Nowtime
            return True
        return False


# addtime function adds number of minutes to our military time, and returns military time
def addtime(start, total):
    hrs = int(f'{start:04d}'[:2])
    mins = int(str(start)[1:]) + total
    while mins > 59:
        hrs = hrs + 1
        mins = round(mins - 59)
    return int(f'{hrs:02d}' + f'{round(mins):02d}')


# function truckdeliver to deliver the pacakges after they are assigned
def truckdeliver(truckid, starttime):
    wgups.deliveryticket = wgups.deliveryticket + 1
    total_time = 0
    dfrom = '01'
    packageid = 0
    toid = '01'
    ttime = 0
    distance = 0
    total_dist = 0
    total_time = 0
    frompackageID = '01'
    for x in range(0, len(trucks[truckid].cargo)):
        svid = packageid
        wgups.deliverydata.append(('------------------------- Truck', truckid, ' Cargo #', x))
        # wgups.deliverydata.append (("Deliver the Package ",x,"Route time : ",addtime(starttime,0)))
        if (x == 0):
            toid = f'{wgups.hashtable.package(trucks[truckid].cargo[x]).deliverylocationid:02d}'
            fromid = '01'
        else:
            fromid = toid
            toid = f'{wgups.hashtable.package(trucks[truckid].cargo[0]).deliverylocationid:02d}'
        wgups.deliverynumber = wgups.deliverynumber + 1
        packageid = wgups.hashtable.package(trucks[truckid].cargo[0]).id
        distance = float(distancedict[fromid + toid])
        total_dist = total_dist + distance
        total_time = total_time + (distance / .3)
        deliveredtime = addtime(starttime, total_time)
        wgups.hashtable.package(packageid).setstatus(
            'delivered at ' + f'{deliveredtime:04d}' + ' by Truck' + f'{truckid:02}')
        trueremove = len(trucks[truckid].cargo)
        trucks[truckid].cargo.remove(trucks[truckid].cargo[0])
        if trueremove > len(trucks[truckid].cargo):
            wgups.undeliveredpackages = wgups.undeliveredpackages - 1
        trucks[truckid].milesdriven = trucks[truckid].milesdriven + distance
        wgups.deliverydata.append(('Route Time      :', addtime(starttime, 0)))
        wgups.hashtable.package(packageid).routetime = addtime(starttime, 0)
        wgups.deliverydata.append(('From Package ID : ', frompackageID))
        frompackageID = packageid
        wgups.deliverydata.append(('To Package   ID : ', packageid))
        wgups.deliverydata.append(('From Location ID: ', fromid))
        wgups.deliverydata.append(('To Location   ID: ', toid))
        wgups.deliverydata.append(('Trip Miles      : ', distance))
        wgups.deliverydata.append(('Truck  Miles    :', round(trucks[truckid].milesdriven)))
        wgups.deliverydata.append(('All Truck  Miles:', round(trucks[1].milesdriven + trucks[2].milesdriven)))
        wgups.deliverydata.append(('Total Miles     : ', round(total_dist, 2)))
        wgups.deliverydata.append(('Trip time       : ', round(distance / .3, 2)))
        wgups.deliverydata.append(('Total Time      :', round(total_time, 2)))
        wgups.deliverydata.append(('Delivery Time   : ', addtime(starttime, total_time)))
        wgups.hashtable.package(packageid).delivertime = addtime(starttime, total_time)
        wgups.hashtable.package(packageid).whodelivered = truckid
        wgups.hashtable.package(packageid).deliveryticket = wgups.deliveryticket
        wgups.hashtable.package(packageid).delivertime = deliveredtime
        wgups.hashtable.package(packageid).beforeonLCroute = fromid
        wgups.hashtable.package(packageid).beforeonIDroute = svid
        wgups.hashtable.package(packageid).milesrode = distance
        wgups.hashtable.package(packageid).totalmilesroad = round(total_dist, 2)
        wgups.hashtable.package(packageid).alltruckmilesatdelivery = round(
            trucks[1].milesdriven + trucks[2].milesdriven, 2)
        wgups.hashtable.package(packageid).deliverynumber = wgups.deliverynumber
        if len(trucks[truckid].cargo) > 1:
            wgups.hashtable.package(
                packageid).afteronLCroute = f'{wgups.hashtable.package(trucks[truckid].cargo[1]).deliverylocationid:02d}'
            wgups.hashtable.package(
                packageid).afteronIDroute = f'{wgups.hashtable.package(trucks[truckid].cargo[0]).id:02d}'
        else:
            if len(trucks[truckid].cargo) == 1:
                wgups.hashtable.package(
                    packageid).afteronLCroute = f'{wgups.hashtable.package(trucks[truckid].cargo[0]).deliverylocationid:02d}'
                wgups.hashtable.package(
                    packageid).afteronIDroute = f'{wgups.hashtable.package(trucks[truckid].cargo[0]).id:02d}'
            else:
                wgups.hashtable.package(packageid).afteronLCroute = '01'
                wgups.hashtable.package(packageid).afteronIDroute = '00'
    # wgups.deliverydata.append(('Return to WGUPS Delivery Center '))
    x = len(trucks[1].cargo) - 1
    fromid = toid
    toid = '01'
    distance = float(distancedict[fromid + toid])
    wgups.hashtable.package(packageid).lastwayhomemiles = distance
    total_dist = total_dist + distance
    total_time = total_time + (distance / .3)
    trucks[truckid].milesdriven = trucks[truckid].milesdriven + distance
    wgups.deliverydata.append(('------------------------- Truck', truckid, ' Return'))
    wgups.deliverydata.append(('Route Time      : ', addtime(starttime, 0)))
    wgups.deliverydata.append(('From Package ID : ', frompackageID))
    wgups.deliverydata.append(('To Package   ID : ', 'Hub'))
    wgups.deliverydata.append(('From Location ID: ', fromid))
    wgups.deliverydata.append(('To Location   ID: ', '01'))
    wgups.deliverydata.append(('Trip Miles      : ', round(distance)))
    wgups.deliverydata.append(('Total Miles     : ', round(total_dist, 2)))
    wgups.deliverydata.append(('Truck Miles     :', round(trucks[truckid].milesdriven)))
    wgups.deliverydata.append(('All Truck  Miles:', round(trucks[1].milesdriven + trucks[2].milesdriven)))
    wgups.allmiles = trucks[1].milesdriven + trucks[2].milesdriven
    wgups.deliverydata.append(('Trip time       : ', round(distance / .3, 2)))
    wgups.deliverydata.append(('Total Time      : ', round(total_time, 2)))
    wgups.deliverydata.append(('Return Time     : ', addtime(starttime, total_time)))
    # wgups.deliverydata.append(())
    for x in trucks[truckid].cargo:
        trucks[truckid].cargo.remove(x)
    return addtime(starttime, total_time)


# allpackagesrouted function checks if all packages have been routed, returns boolean
def allpackagesrouted():
    hbr = True
    for x in range(0, 40):
        if wgups.hashtable.package(x).hasbeenrouted == False:
            if x.id != 0:
                hbr = False
    return hbr


# closesttohub function returns the id of the package in a list which is closest to location #1
def closesttohub(cargo):
    closest = 99
    for x in cargo:
        distancefromhub = float(distancedict[f'{wgups.hashtable.package(x).deliverylocationid:02}' + '01'])
        if distancefromhub < closest:
            closest = distancefromhub
            closeid = x
    # print (distancefromhub)
    return closeid


# closesttopackage function returns the id of the package in a list which is closest to the provided package
# and has not already been assigned to a truck
def closesttopackage(packageid, varlist):
    findkey = wgups.hashtable.package(packageid).deliverylocationid
    smallestfound = 100
    for x in range(0, len(varlist)):
        distancekey = f'{findkey:02d}' + f'{wgups.hashtable.package(varlist[x]).deliverylocationid:02d}'
        distance = float(distancedict[distancekey])
        # print(distance, varlist[x])
        if (distance < smallestfound) and (distance != 0) and (
                wgups.hashtable.package(varlist[x]).hasbeenrouted != True):
            smallestfound = distance
            closeid = varlist[x]
    return closeid


# findmatchinglocations function finds any package which is not delayed which has the same
# delivery location as the provided id
def findmatchinglocations(checkid):
    check = checkid
    found = []
    for x in range(wgups.hashtable.total()):
        if (wgups.hashtable.package(x).id != wgups.hashtable.package(check).id) and (
                wgups.Nowtime >= wgups.hashtable.package(x).starttime) and (
                wgups.hashtable.package(x).deliverylocationid == wgups.hashtable.package(check).deliverylocationid):
            found.append(wgups.hashtable.package(x).id)
    # for x in (wgups.packagelist):
    # if (x.id!=wgups.packagelist[check].id) and (wgups.Nowtime >= x.starttime ) and (x.deliverylocationid==wgups.packagelist[check].deliverylocationid):
    # found.append(x.id)
    return found


# assignslot function assigns the package closest to prev_slot and matching locations
def assignslot(truckid, cargo, prev_slot):
    slot = closesttopackage(prev_slot, cargo)
    # print ('slot   :',slot)
    assignPackage(truckid, slot)
    for x in findmatchinglocations(slot):
        assignPackage(truckid, x)
        # print (x)
    return slot


# smallresults function displays a summery of delivery data up to the time given
def smallresults(entertime):
    tt, c1, c2, c3 = 0, 0, 0, 0
    c17, c18, c19, c20 = True, True, True, True
    if entertime > 1020:
        wgups.hashtable.package(9).setnewaddress("410 S State St")
    for y in sorted(bigresults, key=lambda x: float(x[1])):
        if int(y[4]) <= entertime:
            if int(y[6]) <= entertime:
                c1 = c1 + 1
                tt = tt + float(y[11]) + float(y[16])
            else:
                for w in range(0, len(y)):
                    if w == 6:
                        c3 = c3 + 1
        if int(y[4]) > entertime:
            if int(y[6]) > entertime:
                for w in range(0, len(y)):
                    if w == 4:
                        c2 = c2 + 1
        c17 = y[17] and c17
        c18 = y[18] and c18
        c19 = y[19] and c19
        c20 = y[20] and c20
    sm = 'AM'
    processedtime = entertime
    if entertime >= 1200:
        sm = 'PM'
    if entertime >= 1300:
        processedtime = entertime - 1200
    if int(f'{entertime:04}'[2:]) > 59:
        processedtime = int(f'{entertime:04}'[:2] + '00')
    if f'{processedtime:04d}'[:2] == '00':
        processedtime = int('12' + f'{processedtime:04d}'[2:])
    print('--------------------------------------------------------------------------------------------')
    print("Entered Time             :", f'{processedtime:04d}'[:2] + ':' + f'{processedtime:04d}'[2:] + sm)
    print('Packages At Hub           :', c2)
    print('Packages En Rou           :', c3)
    print('Packages Delivered        :', c1)
    print('Total Miles Driven        :', round(tt, 1))
    print('Total Time Taken          :', round((tt / .3) / 60, 1), 'Hours')
    print('All Delivered On time     :', c18)
    print('All Routed to requirement :', c17)
    print('Must be routed together   :', c19)
    print('Must be routed on truck 2 :', c20)


# menuresults function displays detailed information about packages, routing, delivery, and
# information about whether delivery requirements were met
def menuresults(entertime):
    print(
        '(0)Pacakge ID, (1)Location ID, (2)StartTime, (3)Deadline Time, (4)Route Time, (5)Truck ID, (6)Time Delivered Time,')
    print(
        '(7)Delivery Ticket, (8)Delivery Number, (9)Before TicketID,(10)Before LocationID, (11)Trip Miles, (12)Total Miles,')
    print('(13)Truckstotal Miles, (14)Next PacakgeID, (15)Next LocationID, (16)ReturnToHub,');
    try:
        sortby = int(input("Enter a value to sort the results: "))
    except:
        print('Invalid response, default listing: Delivery Number')
        sortby = 8
    print('(17)Routed Ontime,(18)Delivered Ontime,(19)Requirement1Met, (20)Requirement2Met,(21)Destination')

    print(' 0  1    2    3    4  5    6  7  8  9 10   11   12    13 14 15   16   17   18   19   20               21')
    print('Id Ld StTm DnTm RoTm Td TmDV DT DN Bd BL TrMl ToMl TksMl Nd NL  RTH RADT ONTD R1GT R2GA Destination Name')
    # The wrong delivery address for package #9, Third District Juvenile Court, will be corrected at 10:20 a.m.
    if entertime > 1020:
        wgups.hashtable.package(9).setnewaddress("410 S State St")
    tt, c1, c2, c3 = 0, 0, 0, 0
    c17, c18, c19 = True, True, True
    if entertime > 1020:
        wgups.hashtable.package(9).setnewaddress("410 S State St")
    for y in sorted(bigresults, key=lambda x: float(x[sortby])):
        if int(y[4]) <= entertime:
            if int(y[6]) <= entertime:
                for w in range(0, len(y)):
                    print(y[w], end=' ')
                c1 = c1 + 1
                tt = tt + float(y[11]) + float(y[16])

                print(wgups.locationlist[int(y[1])].name)
            else:

                for w in range(0, len(y)):
                    if w == 6:
                        print('EnRo', end=' ')
                        c3 = c3 + 1
                    else:
                        print(y[w], end=' ')

                print(wgups.locationlist[int(y[1])].name)
        if int(y[4]) > entertime:
            if int(y[6]) > entertime:
                for w in range(0, len(y)):
                    if w == 4:
                        print('AtHu', end=' ')
                        c2 = c2 + 1
                    if w == 6:
                        print('AtHu', end=' ')
                    if (w != 6) and (w != 4):
                        print(y[w], end=' ')
                print(wgups.locationlist[int(y[1])].name)
        c17 = y[17] and c17
        c18 = y[18] and c18
        c19 = y[19] and c19
    sm = 'AM'
    processedtime = entertime
    if entertime >= 1200:
        sm = 'PM'
    if entertime >= 1300:
        processedtime = entertime - 1200
    if int(f'{entertime:04}'[2:]) > 59:
        processedtime = int(f'{entertime:04}'[:2] + '00')
    if f'{processedtime:04d}'[:2] == '00':
        processedtime = int('12' + f'{processedtime:04d}'[2:])
    smallresults(entertime)


# menupackages function displays package data and delivery status up to the time given
def menupackages(entertime):
    status = None

    # The wrong delivery address for package #9, Third District Juvenile Court, will be corrected at 10:20 a.m.
    if entertime > 1020:
        wgups.hashtable.package(9).setnewaddress("410 S State St")
    tt, c1, c2, c3 = 0, 0, 0, 0
    c17, c18, c19 = True, True, True
    if entertime > 1020:
        wgups.hashtable.package(9).setnewaddress("410 S State St")
    for y in sorted(bigresults, key=lambda x: float(x[0])):
        if int(y[4]) <= entertime:
            if int(y[6]) <= entertime:
                c1 = c1 + 1
                # tt=tt+float(y[11])+float(y[16])
                status = 'Delivered'

                print(status, wgups.hashtable.package(int(y[0])).id, wgups.hashtable.package(int(y[0])).address,
                      wgups.hashtable.package(int(y[0])).city, wgups.hashtable.package(int(y[0])).zipcode,
                      wgups.hashtable.package(int(y[0])).deadline, wgups.hashtable.package(int(y[0])).kilo,
                      wgups.hashtable.package(int(y[0])).notes)
            else:
                for w in range(0, len(y)):
                    if w == 6:
                        status = 'EnRoute  '
                        c3 = c3 + 1
                print(status, wgups.hashtable.package(int(y[0])).id, wgups.hashtable.package(int(y[0])).address,
                      wgups.hashtable.package(int(y[0])).city, wgups.hashtable.package(int(y[0])).zipcode,
                      wgups.hashtable.package(int(y[0])).deadline, wgups.hashtable.package(int(y[0])).kilo,
                      wgups.hashtable.package(int(y[0])).notes)
        if int(y[4]) > entertime:
            if int(y[6]) > entertime:
                for w in range(0, len(y)):
                    if w == 4:
                        status = 'AtTheHub '
                        c2 = c2 + 1
                    if w == 6:
                        status = 'AtTheHub '
                print(status, wgups.hashtable.package(int(y[0])).id, wgups.hashtable.package(int(y[0])).address,
                      wgups.hashtable.package(int(y[0])).city, wgups.hashtable.package(int(y[0])).zipcode,
                      wgups.hashtable.package(int(y[0])).deadline, wgups.hashtable.package(int(y[0])).kilo,
                      wgups.hashtable.package(int(y[0])).notes)

    smallresults(entertime)


# menulocations function displays delivery location data
def menulocations():
    for x in wgups.locationlist:
        print(x.id, x.name, x.address)
    smallresults(entertime)


# menudistances function displays delivery location and their distances
def menudistances():
    for x in range(1, 28):
        print(wgups.locationlist[x].id, wgups.locationlist[x].name)
        for y in range(1, 27):
            d = float(distancedict[f'{x:02d}' + f'{y:02d}'])
            print(f'{d:04.1f}', end=" ")
            if y == 13:
                print()
        print('\n')
    smallresults(entertime)


# menuviewdeliverydata displays delivery data up to the time given
def menuviewdeliverydata(entertime):
    ct = 0
    for x in range(len(wgups.deliverydata)):
        if ct == 0:
            if wgups.deliverydata[x][0] != 'Delivery Time   : ':
                print(wgups.deliverydata[x])
            if wgups.deliverydata[x][0] == 'Delivery Time   : ':
                if (wgups.deliverydata[x][1] > entertime):
                    print(wgups.deliverydata[x][0], 'EnRoute')

                    ct = 1
                else:
                    print(wgups.deliverydata[x])

                    ct = 0
        else:
            if wgups.deliverydata[x][0] == 'Delivery Time   : ':
                if (wgups.deliverydata[x][1] < entertime):
                    ct = 0
    smallresults(entertime)


# function dothework assigns packages to trucks based on list provided and nearest neighbor algorithm
def dothework():
    # some packages must be routed together, also added a few more packages to the list
    requirement1 = [14, 15, 16, 34, 24, 26, 22, 21, 20, 19, 12, 13]
    # Nearest Neighbor Algorithm:
    # find the closest package to the hub and assign it to truck 1
    slot1 = closesttohub(requirement1)
    # find the closest package to the previous package which has not already been routed
    # and assign it to truck 1
    slot2 = assignslot(1, requirement1, slot1)
    # find the closest package to the previous package which has not already been routed
    # and assign it to truck 1, after the previous package
    slot3 = assignslot(1, requirement1, slot2)
    # find the closest package to the previous package which has not already been routed
    # and assign it to truck 1
    slot4 = assignslot(1, requirement1, slot3)
    # find the closest package to the previous package which has not already been routed
    # and assign it to truck 1
    slot5 = assignslot(1, requirement1, slot4)
    # find the closest package to the previous package which has not already been routed
    # and assign it to truck 1
    slot6 = assignslot(1, requirement1, slot5)
    # find the closest package to the previous package which has not already been routed
    # and assign it to truck 1
    slot7 = assignslot(1, requirement1, slot6)
    # find the closest package to the previous package which has not already been routed
    # and assign it to truck 1
    slot8 = assignslot(1, requirement1, slot7)
    # find the closest package to the previous package which has not already been routed
    # and assign it to truck 1
    slot9 = assignslot(1, requirement1, slot8)
    # find the closest package to the previous package which has not already been routed
    # and assign it to truck 1
    slot10 = assignslot(1, requirement1, slot9)
    # set the start time for truck 1 to be 0800
    wgups.Nowtime = 800
    # deliver the packages and store the return time in returntime1
    returntime1 = truckdeliver(1, wgups.Nowtime)
    # set the start time for truck 1 second route to returntime1
    wgups.Nowtime = returntime1
    # assign pacakge 25 to truck 1
    assignPackage(1, 25)
    # deliver the package and store the return time in returntime1
    returntime1 = truckdeliver(1, returntime1)

    # using the same pattern as above route and deliver the newcargo pacakges for truck 2
    wgups.Nowtime = 800
    newcargo = [36, 17, 4, 40, 1, 2, 33, 7, 29, 37, 38, 3, 8, 30]
    slot1 = closesttohub(newcargo)
    slot2 = assignslot(2, newcargo, slot1)
    slot3 = assignslot(2, newcargo, slot2)
    slot4 = assignslot(2, newcargo, slot3)
    slot5 = assignslot(2, newcargo, slot4)
    slot6 = assignslot(2, newcargo, slot5)
    slot7 = assignslot(2, newcargo, slot6)
    slot8 = assignslot(2, newcargo, slot7)
    slot9 = assignslot(2, newcargo, slot8)
    returntime2 = truckdeliver(2, wgups.Nowtime)
    wgups.Nowtime = returntime2
    # using the same pattern as above route and deliver the nextcargo pacakges for truck 2
    nextcargo = [28, 6, 32, 31, 10, 27, 35, 13, 39, 23, 11, 18]
    slot1 = closesttohub(nextcargo)
    slot2 = assignslot(2, nextcargo, slot1)
    slot3 = assignslot(2, nextcargo, slot2)
    slot4 = assignslot(2, nextcargo, slot3)
    slot5 = assignslot(2, nextcargo, slot4)
    slot6 = assignslot(2, nextcargo, slot5)
    slot7 = assignslot(2, nextcargo, slot6)
    slot8 = assignslot(2, nextcargo, slot7)
    slot9 = assignslot(2, nextcargo, slot8)
    returntime2 = truckdeliver(2, returntime2)
    # package #9 is delayed, if the time is still premature to route, have truck 1 wait until the start time
    if returntime1 < wgups.hashtable.package(9).starttime:
        returntime1 = wgups.hashtable.package(9).starttime
    wgups.Nowtime = returntime1
    # route all remaining packages, this allows the function to be self adjusting
    # any error in assignment will not hault the remaining steps and all packages
    # will always be delivered
    for x in range(wgups.hashtable.total()):
        if wgups.hashtable.package(x).hasbeenrouted == False:
            assignPackage(1, wgups.hashtable.package(x).id)
    returntime1 = truckdeliver(1, returntime1)


# declare some variables
rows, drows, bigresults = [], [], []
tt, c1, c2, c3 = 0, 0, 0, 0
x, addresstart, idn = -1, 0, 0
isint = True
wgups = deliverycenter();
distancedict = {'0000': 0}
trucks = [Truck(0), Truck(1), Truck(2)]
driver1 = Driver(1, 'New Driver', 1)
driver2 = Driver(2, 'Old Driver', 2)
wgups.Nowtime = 800
wgups.undeliveredpackages = wgups.hashtable.total()
# import data from WGUPSPackageFile.csv and WGUPSDistanceTable.csv files
print('Importing Packages...')
with open("WGUPSPackageFile.csv") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)
for eachrow in rows:
    if (len(eachrow)) > 7:
        wgups.hashtable.insert(int(eachrow[0]),
                               Package(int(eachrow[0]), eachrow[1], eachrow[2], eachrow[3], eachrow[4], eachrow[5],
                                       int(eachrow[6]), eachrow[7]))
    else:
        wgups.hashtable.insert(int(eachrow[0]),
                               Package(int(eachrow[0]), eachrow[1], eachrow[2], eachrow[3], eachrow[4], eachrow[5],
                                       int(eachrow[6])))
with open("WGUPSDistanceTable.csv") as dfile:
    csvreader = csv.reader(dfile)
    for row in csvreader:
        drows.append(row)
print('Importing Locations...')
for item in drows[0]:
    sp = False
    inx = 0
    idn = idn + 1
    for ch in item:
        if str(ch) in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            if (sp == False):
                sp = True
                inx = item.index(str(ch))
    wgups.locationlist.append(Location(idn, item[:inx], item[inx:], item))
print('Binding Package IDs with Location IDs...')
for x in wgups.locationlist:
    for y in range(40):
        if wgups.hashtable.package(y).address == x.address:
            wgups.hashtable.package(y).setdeliverylocationid(x.id)
print('Importing distances...')
for x in range(1, 28):
    for y in range(2, len(drows[x])):
        distancedict[f'{wgups.locationlist[x].id:02d}' + f'{wgups.locationlist[y - 1].id:02d}'] = drows[x][y]
        distancedict[f'{wgups.locationlist[y - 1].id:02d}' + f'{wgups.locationlist[x].id:02d}'] = drows[x][y]
# set package #6, #25, #28, #32 as delayed with a 0905 possible start time
# set pacakge #9 as delayed with a 1020 possible start time
print('Processing delayed packages...')
delayed(6, 905)
delayed(25, 905)
delayed(28, 905)
delayed(32, 905)
delayed(9, 1020)
# assign packages to trucks using nearest neighbor and process the delivery data
print('Prossessing deliveries...')
dothework()
# store data results in bigresults
for x in range(0, wgups.hashtable.total()):
    deadln = wgups.hashtable.package(x).deadline[:2] + wgups.hashtable.package(x).deadline[3:5]
    if deadln == 'EO':
        deadln = 1700
    if str(deadln)[0] == '9':
        deadln = 900
    mustbeon1 = 'True'
    mustbeon2 = 'True'
    if x in [13, 14, 15, 16, 19, 20]:
        if (wgups.hashtable.package(20).deliveryticket == wgups.hashtable.package(
                19).deliveryticket == wgups.hashtable.package(16).deliveryticket == wgups.hashtable.package(
                13).deliveryticket == wgups.hashtable.package(14).deliveryticket == wgups.hashtable.package(
                15).deliveryticket):
            mustbeon1 = True
        else:
            mustbeon1 = False
    if x in [3, 18, 36, 38]:
        if int(wgups.hashtable.package(x).whodelivered) == 2:
            mustbeon2 = True
        else:
            mustbeon2 = False
    bigresults.append([f'{wgups.hashtable.package(x).id:02d}', f'{wgups.hashtable.package(x).deliverylocationid:02d}',
                       f'{wgups.hashtable.package(x).starttime:04d}', f'{int(deadln):04d}',
                       f'{wgups.hashtable.package(x).routetime:04d}', f'{wgups.hashtable.package(x).whodelivered:02d}',
                       f'{wgups.hashtable.package(x).delivertime:04d}',
                       f'{wgups.hashtable.package(x).deliveryticket:02d}',
                       f'{wgups.hashtable.package(x).deliverynumber:02d}',
                       f'{int(wgups.hashtable.package(x).beforeonIDroute):02d}',
                       f'{int(wgups.hashtable.package(x).beforeLConroute):02d}',
                       f'{wgups.hashtable.package(x).milesrode:04.1f}',
                       f'{wgups.hashtable.package(x).totalmilesroad:04.1f}',
                       f'{wgups.hashtable.package(x).alltruckmilesatdelivery:05.1f}',
                       f'{wgups.hashtable.package(x).afteronIDroute}', f'{wgups.hashtable.package(x).afteronLCroute}',
                       f'{wgups.hashtable.package(x).lastwayhomemiles:04.1f}',
                       wgups.hashtable.package(x).starttime <= wgups.hashtable.package(x).routetime,
                       wgups.hashtable.package(x).delivertime <= int(deadln), mustbeon1, mustbeon2])

# display menu and request time from user
while isint == True:
    try:
        print('--------------------------------------------------------------------------------------------')
        print(
            'Menu Keys: (Q)uit, display(R)esults, display(P)ackages,display(L)ocations,display(D)istances,(V)iew delivery data')
        menu = input("Enter any Military Time (0001-2359) or any menu key (q, r, p, d, or v): ")
        print('--------------------------------------------------------------------------------------------')
        entertime = int(menu)
        # if the user enters a time then check if the time is between  0001-2359
        # if the time enter is invalid but numeric then change the invalid part to 00 ex:1299 becomes 1200
        while (entertime < 1) or (entertime > 2359):
            entertime = int(input("Should be any Time 0001-2359 or any nonnumeric key to quit: "))
        # smallresults shows a summary of delivery data
        smallresults(entertime)
        wgups.lastenteredtime = entertime
    # if the user enters a nonnumeric character then run a menu command
    except ValueError:
        if menu[0] == "q" or menu == "Q":
            print(menu, "Quitting....")
            isint = False
        if menu[0] == "r" or menu[0] == "R":
            if (wgups.lastenteredtime == None):
                print("Enter a Time before requesting results")
            else:
                menuresults(wgups.lastenteredtime)
        if menu[0] == "p" or menu[0] == "P":
            if (wgups.lastenteredtime == None):
                print("Enter a Time before requesting results")
            else:
                menupackages(wgups.lastenteredtime)

        if menu[0] == "l" or menu[0] == "L":
            if (wgups.lastenteredtime == None):
                print("Enter a Time before requesting locations")
            else:
                menulocations()
        if menu[0] == "d" or menu[0] == "D":
            if (wgups.lastenteredtime == None):
                print("Enter a Time before requesting distances")
            else:
                menudistances()
        if menu[0] == "v" or menu[0] == "V":
            if (wgups.lastenteredtime == None):
                print("Enter a Time before requesting delivery data")
            else:
                menuviewdeliverydata(wgups.lastenteredtime)