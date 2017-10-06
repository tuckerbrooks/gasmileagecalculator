import csv
import re
import sys

def main():
	pass

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

vehicleInfo = csv.DictReader(open('vehicles.csv'))
for row in vehicleInfo:
	vehicles.append(Vehicle(row["citympg"], row["combmpg"], row["highwaympg"], row["year"], row["make"], row["model"], row["cylinders"], row["displacement"], row["transmission"], row["drive"]))

for vehicle in vehicles:
	print(vehicle.citympg, vehicle.model)

main()