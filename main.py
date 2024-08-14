#
# Project 01: Analyzing CTA2 L data in Python
# Author: Ricardo Gonzalez
# Date: 09/16/2022
# CS 341 Fall 2022: Patrick Troy
#
# This program inputs commands from user and outputs data from 
# the CTA2 L daily ridership database.
#

# Command description:
# 1: Displays stations that are 'like' the user's input.
# 2: Displays the ridership at each station, in ascending order by station name.
# 3: Displays the top-10 busiest stations in terms of ridership, in descending order by ridership.
# 4: Displays the least-10 busiest stations in terms of ridership, in ascending order by ridership.
# 5: Displays all stop names that are part of a line color input rom the user, in ascending order. 
#    If the line does not exist, it says so.
# 6: Displays total ridership by month, in ascending order, by month. After the output, 
#    the user is given the option to plot the data.
# 7: Displays total ridership by year, in ascending order by year. After the output, 
#    the user is given the option to plot the data.
# 8: Inputs a year and the names of two stations (full or partial names), and then outputs 
#    the daily ridership at #each station for that year.
# 9: Input a line color from the user and output all unique station names that are part of 
#    that line, in ascending order.
# x: Exit the program
#




import sqlite3
import matplotlib.pyplot as plt

################################################################## #
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    print("General stats:")
    
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")
    
    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")
    
    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")
    
    dbCursor.execute("Select DISTINCT date(Ride_Date) From Ridership;")
    rows = dbCursor.fetchall(); # We need to determine the first and last date in the database, so we fetch ALL the data
    print("  date range: " + rows[0][0] + " - " + rows[len(rows) - 1][0]) # We treat rows as a table here
    
    dbCursor.execute("Select SUM(Num_Riders) From Ridership;")
    row = dbCursor.fetchone();
    total = row[0]
    print("  Total ridership:", f"{row[0]:,}")
    
    dbCursor.execute("Select SUM(Num_Riders) From Ridership WHERE Type_of_Day = 'W';")
    row = dbCursor.fetchone();
    print("  Weekday ridership:", f"{row[0]:,}", f"({row[0]/total * 100:.2f}%)")
    
    dbCursor.execute("Select SUM(Num_Riders) From Ridership WHERE Type_of_Day = 'A';")
    row = dbCursor.fetchone();
    print("  Saturday ridership:", f"{row[0]:,}", f"({row[0]/total * 100:.2f}%)")
    
    dbCursor.execute("Select SUM(Num_Riders) From Ridership WHERE Type_of_Day = 'U';")
    row = dbCursor.fetchone();
    print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({row[0]/total * 100:.2f}%)")
    
#
# This function displays the stations that are 'like' the user's input
#
def command1(dbConn):
    dbCursor = dbConn.cursor()
    userInput = input("\nEnter partial station name (wildcards _ and %): ")
    sql = ("Select * "
           + "FROM Stations "
           + "WHERE Station_Name LIKE " + "'" + userInput + "' "
           + "ORDER BY Station_Name")
    
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    
    if len(rows) == 0: # No data was retrieved
        print("**No stations found...")
        print()
        return
    
    for row in rows:
        print(row[0], ":", row[1]) # Display Station_ID : Station_Name
    print()

#
# This function displays the ridership at each station, in ascending order by station name
#
def command2(dbConn):
    dbCursor = dbConn.cursor()
    print("** ridership all stations **")
    sql = ("Select Station_Name, SUM(Num_Riders) "
            "FROM Stations JOIN Ridership ON(Stations.Station_ID = Ridership.Station_ID) "
            "GROUP BY Ridership.Station_ID "
            "ORDER BY Station_Name ASC")
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    
    total = 0
    for row in rows:
        total = total + row[1] # For computing percentage
    
    
    # Displaying in the format Station_Name, Ridership Sum for that Station, Percentage
    for row in rows:
        print(row[0], ":", f"{row[1]:,}", f"({row[1]/total * 100:.2f}%)")
    print()
  
    
#
# This function displays the top-10 busiest stations in terms of ridership, in descending order by ridership
#
def command3(dbConn):
    dbCursor = dbConn.cursor()
    print("** top-10 stations **")
    sql = ("Select Station_Name, SUM(Num_Riders) as total "
            "FROM Stations JOIN Ridership ON(Stations.Station_ID = Ridership.Station_ID) "
            "GROUP BY Ridership.Station_ID "
            "ORDER BY total DESC ")
    
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()

    total = 0
    for row in rows:
        total = total + row[1]  # For computing percentage, row[1] has the sum
  
    i = 0 # To have a way to make 10 iterations while taking advantage of the for each loop
    # Displaying in the format Station_Name, Ridership Sum for that station, Percentage
    for row in rows:
        print(row[0], ":", f"{row[1]:,}", f"({row[1]/total * 100:.2f}%)")
        i = i + 1
        if i == 10:
            break
    print()
    

#
# This function displays the least-10 busiest stations in terms of ridership, in ascending order by ridership.
#
def command4(dbConn):
    dbCursor = dbConn.cursor()
    print("** least-10 stations **")
    sql = ("Select Station_Name, SUM(Num_Riders) as total "
            "FROM Stations JOIN Ridership ON(Stations.Station_ID = Ridership.Station_ID) "
            "GROUP BY Ridership.Station_ID "
            "ORDER BY total ASC ")
    
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    
    total = 0
    
    for row in rows:
        total = total + row[1]   # For computing percentage, row[1] has the sum
   
    i=0  # To have a way to make 10 iterations while taking advantage of the for each loop
    # Displaying in the format Station_Name, Ridership Sum for that station, Percentage
    for row in rows:
        print(row[0], ":", f"{row[1]:,}", f"({row[1]/total * 100:.2f}%)")
        i = i + 1
        if i == 10:
            break
        
    print()
  
    
#
# Displays all stop names that are part of a line color input rom the user, in ascending order. 
# If the line does not exist, it says so.
#  
def command5(dbConn):
    dbCursor = dbConn.cursor()
    userInput = input("\nEnter a line color (e.g. Red or Yellow): ")
    userInput = (userInput.lower()).capitalize()
    
    if userInput == 'Purple-express':  # Solution to not finding a way to capitalize 'express'
        userInput = 'Purple-Express'

    sql = ("Select Stop_Name, Direction, ADA, Color "
            "FROM Stops "
            "JOIN StopDetails ON(Stops.Stop_ID = StopDetails.Stop_ID) "
            "JOIN Lines ON(StopDetails.Line_ID = Lines.Line_ID) "
            "WHERE Color = " + "'" + userInput + "' "
            + "ORDER BY Stop_Name ASC ")
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    
    #Check if empty first
    if len(rows) == 0:
        print("**No such line...")
        print()
        return
    
    # Displaying in the format Stop_Name, Direction (N or S), Accesibility
    for row in rows: 
        print(row[0], ":", "direction =", row[1], end=" ")
        print("(accessible?", end=" ")
        if row[2] == 1 :    # '1' means it is accessible, '0' means it is not
          print("yes)")
        else:
          print("no)")
    
    print()
                 

#
# Displays total ridership by month, in ascending order, by month. After the output, 
# the user is given the option to plot the data.
#
def command6(dbConn):
    dbCursor = dbConn.cursor()
    print("** ridership by month **")
    sql = ("Select strftime('%m', Ride_Date) as month, SUM(Num_Riders)"
            "FROM Ridership "
            "GROUP BY month "
            "ORDER BY month ASC")
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    
    # display in the format Month number(01-12), ridership sum
    for row in rows:
        print(row[0], ":", f"{row[1]:,}")
        
    print()
    userInput = (input("Plot? (y/n)\n")).lower()
    
    if userInput != "y":   # If input is anything other than 'y' or 'Y', we return. Plot otherwise
        return
    
    # Populate x and y lists with month number and the corresponding ridership sum
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])
          
    # Determine label names and plot
    plt.xlabel("month")
    plt.ylabel("number of riders(x * 10^8)")
    plt.title("monthly ridership")
    plt.plot(x, y)
    plt.show()
    print()


#
# Displays total ridership by year, in ascending order by year. After the output, 
# the user is given the option to plot the data.
#
def command7(dbConn):
    dbCursor = dbConn.cursor()
    print("** ridership by year **")
    sql = ("Select strftime('%Y', Ride_Date) as Year, SUM(Num_Riders)"
            "FROM Ridership "
            "GROUP BY Year "
            "ORDER BY Year ASC")
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()

    # display in the format Year (2001-2021), ridership sum
    for row in rows:
        print(row[0], ":", f"{row[1]:,}")
    
    print()
    userInput = (input("Plot? (y/n)\n")).lower()
    
    if userInput != "y":  # If input is anything other than 'y' or 'Y', we return. Plot otherwise
        return
    
    # Populate x and y lists with year number and the corresponding ridership sum
    x = []
    y = []
    for row in rows:
        temp = int(row[0]) % 100  # Temp extracts last two digits, with '% 100'
        x.append(str(temp).zfill(2))  # zfill fills string with zeros to the left
        y.append(row[1])
        
    plt.xlabel("year")
    plt.ylabel("number of riders(x * 10^8)")
    plt.title("yearly ridership")
    plt.plot(x, y)
    plt.show()
  
#
# Helper function for command 8. Determines if a query has exactly zero, or multiple
# entries and displays the corresponding message
#
def validateStation(validationList):
    if len(validationList) == 0:  # The list is empty, thus no data was retrieved
        print("**No station found...\n")
        return False
    if len(validationList) > 1:  # The list is larger than one, and we cannot have multiple stations
        print("**Multiple stations found...\n")
        return False
    return True

#
# Helper function for command 8. Displays the data.
#
def displayCmnd8(string, rows):
    # Display "Station 1 or 2, Station_ID, Station_Name
    print(string, rows[0][0],rows[0][1]) # Here we treat rows as a table
    i = 0   # To control what row indices we want to display
    length = len(rows)
    for row in rows:
        if i < 5 or i >= (length - 5):  # Displays first and last 5 elements. 
            print(row[2], row[3])   # Displays in the format Date, ridership
        i = i + 1

#
# Helper function for command 8. Plots the data.
#
def plotCmmnd8(rows1,rows2):
    x1 = [] # Lists for station 1
    y1 = []
    
    x2 = [] # Lists for station 2
    y2 = []
    
    i = 1
    length = len(rows1)  # note that both rows1 and rows2 should have the same length, as we are retrieving data from the same year
    while i < length + 1:  # Populate x axes from both stations (1 - 365, or 1 - 366)
        x1.append(i)
        x2.append(i)
        i = i + 1
    
    for row in rows1:   # populate y axis for Station 1
        y1.append(row[3])   # row at index 3 has Number of Riders
            
    for row in rows2:   # populate y axis for Station 2
        y2.append(row[3])   # row at 3 has Number of Riders
        
    plt.xlabel("day")
    plt.ylabel("number of riders")
    plt.title("riders each day of 2020")
    plt.plot(x1, y1)
    plt.plot(x2, y2)
    plt.legend([rows1[0][1],rows2[0][1]]) #  rows1/2 at entry [0][1] has  Station Name
    plt.show()

#
# Inputs a year and the names of two stations (full or partial names), and then outputs 
# the daily ridership at each station for that year.
#
def command8(dbConn):
    dbCursor = dbConn.cursor()
    yearInput = int(input("\nYear to compare against? "))

    # STATION 1 QUERY
    station1 = input("\nEnter station 1 (wildcards _ and %): ")
    validationQuery = ("SELECT Station_Name "
                       "FROM Stations "
                       "WHERE Station_Name LIKE '" + station1 +"'")
    dbCursor.execute(validationQuery)
    validationList = dbCursor.fetchall()
    
    if not(validateStation(validationList)):  # Make sure there is exactly one station in the list
        return
    
    # STATION 2 QUERY
    print()
    station2 = input("Enter station 2 (wildcards _ and %): ") 
    validationQuery = ("SELECT Station_Name "
                       "FROM Stations "
                       "WHERE Station_Name LIKE '" + station2 +"'")
    dbCursor.execute(validationQuery)
    validationList = dbCursor.fetchall()
    
    if not(validateStation(validationList)):   # Make sure there is exactly one station in the list
        return
    
    # At this point we know both Station Queries were valid. Proceed with queries for each station
    sql1 = ("SELECT Stations.Station_ID, Station_Name, date(Ride_Date) as theDate, Num_Riders "
            "FROM Stations "
            "JOIN Ridership ON(Stations.Station_ID = Ridership.Station_ID) "
            "WHERE strftime('%Y', Ride_Date) = '" + str(yearInput) +"' AND Station_Name LIKE '" + station1 + "' "
            "ORDER BY theDate")
    
    dbCursor.execute(sql1)
    rows1 = dbCursor.fetchall()
    
    sql2 = ("SELECT Stations.Station_ID, Station_Name, date(Ride_Date) as theDate, Num_Riders "
            "FROM Stations "
            "JOIN Ridership ON(Stations.Station_ID = Ridership.Station_ID) "
            "WHERE strftime('%Y', Ride_Date) = '" + str(yearInput) +"' AND Station_Name LIKE '" + station2 + "' "
            "ORDER BY theDate")

    dbCursor.execute(sql2)
    rows2 = dbCursor.fetchall()
    
    #if len(rows1) != 0 and len(rows1) != 0:
    displayCmnd8("Station 1:", rows1)
    displayCmnd8("Station 2:", rows2)
        
    print()
    userInput = (input("Plot? (y/n)\n")).lower()
    
    if userInput != "y":
        return
    
    plotCmmnd8(rows1, rows2)    # Plot in a helper function
    
 #
 # Helper function for command 9. Plots the data.
 #
def plotCmmnd9(rows, userInput, color):
    x = [] # List for the axis
    y = []

    for row in rows:
        x.append(row[2])    # append longitudes
        y.append(row[1])    # append latitudes
    
    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    plt.imshow(image, extent=xydims)
    plt.title(color.lower() + " line")
    
    if(userInput.lower() == "purple-express"): # To deal with 'purple-express and purple as one single line'
        color = "Purple"
    
    plt.plot(x, y, "o", c = color)
    
    for row in rows:
        plt.annotate(row[0], (row[2], row[1])) # To match each station name with its coordinate
        
    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])
    plt.show()
    print()
    
    
#   
# Input a line color from the user and output all unique station names that are part of 
# that line, in ascending order.
#
def command9(dbConn):
    dbCursor = dbConn.cursor()
    color = input("\nEnter a line color (e.g. Red or Yellow): ")
    color = (color.lower()).capitalize()
    
    if color == 'Purple-express':    # Solution to not finding a way to capitalize 'express'
        color = 'Purple-Express'
        
    sql = ("Select DISTINCT Station_Name, Latitude, Longitude "
            "FROM Stations "
            "JOIN Stops ON(Stations.Station_ID = Stops.Station_ID) "
            "JOIN StopDetails ON(Stops.Stop_ID = StopDetails.Stop_ID) "
            "JOIN Lines ON(StopDetails.Line_ID = Lines.Line_ID) "
            "WHERE Color = " + "'" + color + "' "
            + "ORDER BY Station_Name ASC ")
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    
    #Check if empty first
    if len(rows) == 0:  
        print("**No such line...")
        print()
        return
    
    for row in rows:
        print(row[0], ":", f"({row[1]},", f"{row[2]})")
    
    print()
    userInput = (input("Plot? (y/n)\n")).lower()
    
    if userInput != "y":
        return
    
    plotCmmnd9(rows, userInput, color) #plot the data
    
    
############################################################################## 
# main
#
print('** Welcome to CTA L analysis app **')
print()
dbConn = sqlite3.connect('CTA2_L_daily_ridership.db') 
print_stats(dbConn)

print()
while True:
    userInput = input("Please enter a command (1-9, x to exit): ")
    if userInput == '1':
       command1(dbConn)
    elif userInput == '2':
        command2(dbConn)
    elif userInput == '3':
        command3(dbConn)
    elif userInput == '4':
        command4(dbConn)   
    elif userInput == '5':
        command5(dbConn)   
    elif userInput == '6':
        command6(dbConn)   
    elif userInput == '7':
        command7(dbConn)   
    elif userInput == '8':
       command8(dbConn)
    elif userInput == '9':
       command9(dbConn)
    elif userInput == 'x':
        break
    else: 
        print("**Error, unknown command, try again...\n")
        continue
#
# done
#