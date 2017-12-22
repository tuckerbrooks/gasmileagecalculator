import csv
import googlemaps
from lxml import html
import requests
from datetime import datetime

def main():
	gasPrice()
	getVehicleInfo()
	specifiedVehicle = vehicleLookup()
	theVehicle = specifyVehicle(specifiedVehicle)
	printIt = printInfo(theVehicle)
	calculateTrip(printIt, theVehicle)

gmaps = googlemaps.Client(key='AIzaSyCatPE9kkddRTSF6bNvmq0MOgdF4XFeycQ')
vehicles = []

def createTables(metadata, conn):
	users = Table('users', metadata, Column('id', Integer, primary_key=True), Column('city', Integer), Column('comb', Integer), Column('highway', Integer), Column('year', Integer), Column('make', String), Column('model', String), Column('cylinders', Integer), Column('displacement', Float), Column('transmission', String), Column('drive', String))
	metadata.create_all(engine)

class Vehicle():
	def __init__(self, citympg, combmpg, highwaympg, year, make, model, cylinders, displacement, transmission, drive):
		self.citympg = citympg
		self.combmpg = combmpg
		self.highwaympg = highwaympg
		self.year = year
		self.make = make
		self.model = model
		self.cylinders = cylinders
		self.displacement = displacement
		self.transmission = transmission
		self.drive = drive

questions = [
	"What year is your vehicle? ",
	"What make is your vehicle? (Make sure capitalization and spelling is correct on all questions) ",
	"What model is your vehicle? ",
	"How many cylinders does your vehicle have? ",
	"What is your engine displacement? ",
	"What kind of transmission does your vehicle have? ",
	"What is the drivetrain of your vehicle? "
]

def gasPrice():
	page = requests.get('http://gasprices.aaa.com')
	tree = html.fromstring(page.content)
	gasPrices = tree.xpath('/html/body/main/div[3]/table/tbody/tr[1]/td[2]')
	print (str(gasPrices))

def getDistance():
	origin = str(input("What is the starting point? (Please write out full address) "))
	destination = str(input("What is the destination? (Please write out full address) "))
	now = datetime.now()
	directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=now)
	distance = str(directions_result[0]['legs'][0]['distance']['text'])
	return float(distance.rstrip(" mi"))

def specifyVehicle(specifiedVehicle):
	output = []
	for vehicle in vehicles:
		if specifiedVehicle[0] == vehicle.year and specifiedVehicle[1] == vehicle.make and specifiedVehicle[2] == vehicle.model and specifiedVehicle[3] == vehicle.cylinders and specifiedVehicle[4] == vehicle.displacement and specifiedVehicle[5] == vehicle.transmission and specifiedVehicle[6] == vehicle.drive:
			output.append(vehicle)
	return output[0]

def calculateTrip(tf, vehicle):
	if tf == 0:
		answer = extraQuestions()
		gasPrice = answer[0]
		distance = answer[1]
		percentage = answer[2] / 50
		mpg = 0
		if 0 <= percentage <= 1:
			diff = abs(float(vehicle.citympg) - float(vehicle.combmpg))
			if vehicle.citympg <= vehicle.combmpg:
				mpg = (percentage * diff) + float(vehicle.citympg)
			else:
				mpg = float(vehicle.citympg) - (percentage * diff)
		elif 1 < percentage <= 2:
			diff = abs(float(vehicle.combmpg) - float(vehicle.highwaympg))
			if vehicle.combmpg <= vehicle.highwaympg:
				mpg = ((percentage - 1) * diff) + float(vehicle.combmpg)
			else:
				mpg = float(vehicle.combmpg) - ((percentage - 1) * diff)
		else:
			percentage = input("Error, please type a percentage between 0 - 100.")
			exit()
		finalPrice = (distance/mpg) * gasPrice
		print ("Traveling", str(distance), "miles, $" + str(gasPrice), "per gallon, with", str(mpg), "mpg.")
		print ("Total: $" + str(round(finalPrice, 2)))

def getVehicleInfo():
	vehicleInfo = csv.DictReader(open('vehicles.csv'))
	for row in vehicleInfo:
		vehicles.append(Vehicle(row["citympg"], row["combmpg"], row["highwaympg"], row["year"], row["make"], row["model"], row["cylinders"], row["displacement"], row["transmission"], row["drive"]))

def vehicleLookup():
	year = getYear(questions[0])
	make = getMake(year, questions[1])
	model = getModel(make, year, questions[2])
	cylinders = getCylinders(model, year, questions[3])
	displacement = getDisplacement(cylinders, model, year, questions[4])
	transmission = getTransmission(displacement, model, year, questions[5])
	drive = getDrive(transmission, model, year, questions[6])
	return [year, make, model, cylinders, displacement, transmission, drive]

def getYear(question):
	seen = set()
	unique = []
	sortedVehicles = sorted(vehicles, key=lambda vehicle: vehicle.year)
	for vehicle in sortedVehicles:
		if vehicle.year not in seen:
			unique.append(vehicle.year)
			seen.add(vehicle.year)
	if len(unique) == 1:
		return unique[0]
	else:
		for vehicle in unique:
			print(vehicle)
		return input(question)

def getMake(attribute, question):
	seen = set()
	unique = []
	out = []
	for vehicle in vehicles:
		if vehicle.year == attribute:				
			out.append(vehicle)
	sortedVehicles = sorted(out, key=lambda vehicle: vehicle.make)
	for vehicle in sortedVehicles:
		if vehicle.make not in seen:
			unique.append(vehicle.make)
			seen.add(vehicle.make)
	if len(unique) == 1:
		return unique[0]
	else:
		for vehicle in unique:
			print(vehicle)
		return input(question)

def getModel(attribute1, attribute2, question):
	seen = set()
	unique = []
	out = []				
	for vehicle in vehicles:
		if vehicle.make == attribute1 and vehicle.year == attribute2:
			out.append(vehicle)
	sortedVehicles = sorted(out, key=lambda vehicle: vehicle.model)
	for vehicle in sortedVehicles:
		if vehicle.model not in seen:
			unique.append(vehicle.model)
			seen.add(vehicle.model)
	if len(unique) == 1:
		return unique[0]
	else:
		for vehicle in unique:
			print(vehicle)
		return input(question)

def getCylinders(attribute1, attribute2, question):
	seen = set()
	unique = []
	out = []
	for vehicle in vehicles:
		if vehicle.model == attribute1 and vehicle.year == attribute2:
			out.append(vehicle)
	sortedVehicles = sorted(out, key=lambda vehicle: vehicle.cylinders)
	for vehicle in sortedVehicles:
		if vehicle.cylinders not in seen:
			unique.append(vehicle.cylinders)
			seen.add(vehicle.cylinders)
	if len(unique) == 1:
		return unique[0]
	else:
		for vehicle in unique:
			print(vehicle)
		return input(question)

def getDisplacement(attribute1, attribute2, attribute3, question):	
	seen = set()
	unique = []
	out = []
	for vehicle in vehicles:
		if vehicle.cylinders == attribute1 and vehicle.model == attribute2 and vehicle.year == attribute3:
			out.append(vehicle)
	sortedVehicles = sorted(out, key=lambda vehicle: vehicle.displacement)
	for vehicle in sortedVehicles:
		if vehicle.displacement not in seen:
			unique.append(vehicle.displacement)
			seen.add(vehicle.displacement)
	if len(unique) == 1:
		return unique[0]
	else:
		for vehicle in unique:
			print(vehicle)
		return input(question)

def getTransmission(attribute1, attribute2, attribute3, question):	
	seen = set()
	unique = []
	out = []
	for vehicle in vehicles:
		if vehicle.displacement == attribute1 and vehicle.model == attribute2 and vehicle.year == attribute3:
			out.append(vehicle)
	sortedVehicles = sorted(out, key=lambda vehicle: vehicle.transmission)
	for vehicle in sortedVehicles:
		if vehicle.transmission not in seen:
			unique.append(vehicle.transmission)
			seen.add(vehicle.transmission)
	if len(unique) == 1:
		return unique[0]
	else:
		for vehicle in unique:
			print(vehicle)
		return input(question)

def getDrive(attribute1, attribute2, attribute3, question):	
	seen = set()
	unique = []
	out = []
	for vehicle in vehicles:
		if vehicle.transmission == attribute1 and vehicle.model == attribute2 and vehicle.year == attribute3:
			out.append(vehicle)
	sortedVehicles = sorted(out, key=lambda vehicle: vehicle.drive)
	for vehicle in sortedVehicles:
		if vehicle.drive not in seen:
			unique.append(vehicle.drive)
			seen.add(vehicle.drive)
	if len(unique) == 1:
		return unique[0]
	else:
		for vehicle in unique:
			print(vehicle)
		return input(question)

def printInfo(specifiedVehicle):
	print (specifiedVehicle.year, specifiedVehicle.make, specifiedVehicle.model)
	print (specifiedVehicle.cylinders + "cyl", specifiedVehicle.displacement + "L")
	print (specifiedVehicle.transmission)
	print (specifiedVehicle.drive)
	print ("City:", specifiedVehicle.citympg)
	print ("Highway:", specifiedVehicle.highwaympg)
	print ("Combined:", specifiedVehicle.combmpg)
	tripYN = input("Would you like to calculate the price of a trip? ")
	if tripYN == "yes" or tripYN == "Yes" or tripYN == "y":
		return 0
	elif tripYN == "no" or tripYN == "No" or tripYN == "n":
		return 1
	else:
		tripYN = input("Error. Please type yes or no.")
		exit()

def extraQuestions():
	gasPrice = float(input("What is the current gas price? (do not include $ symbol) "))
	distance = getDistance()
	percentage = float(input("What percentage of driving will be on the highway? (do not include percent symbol) "))
	return [gasPrice, distance, percentage]


main()