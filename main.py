import csv

def main():
	getVehicleInfo()
	deleteVehicles(getMake())
	for vehicle in vehicles:
		pass
		#print (vehicle.make, vehicle.model)

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

vehicles = []

def getVehicleInfo():
	vehicleInfo = csv.DictReader(open('vehicles.csv'))
	for row in vehicleInfo:
		vehicles.append(Vehicle(row["citympg"], row["combmpg"], row["highwaympg"], row["year"], row["make"], row["model"], row["cylinders"], row["displacement"], row["transmission"], row["drive"]))

def getMake():
	seen = set()
	unique = []
	sortedVehicles = sorted(vehicles, key=lambda vehicle: vehicle.make)
	for vehicle in sortedVehicles:
		if vehicle.make not in seen:
			unique.append(vehicle.make)
			seen.add(vehicle.make)
	for make in unique:
		print(make)
	return input("Which make is your vehicle? (Make sure capitalization and spelling is correct on all questions)")

def deleteVehicles(attribute):
	out = []
	for vehicle in vehicles:
		if vehicle.make == attribute:
			out.append(vehicle)
			print(vehicle.make, vehicle.model)

main()