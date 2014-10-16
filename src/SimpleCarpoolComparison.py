"""

 Copyright 2014 Jason Randolph Eads

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

"""
# SimpleCarpoolComparion.py
# Description: This compares two routes to see which one saves time.

__author__ = 'Jason R. Eads <jeads442@gmail.com'

import math
import logging

class SimpleCarpoolComparison:
	"""Problem:

	"Calculate the detour distance between two different rides. Given four
	latitude / longitude pairs, where driver one is traveling from point A to
	point B and driver two is traveling from point C to point D, write a
	function (in your language of choice) to calculate the shorter of the
	detour distances the drivers would need to take to pick-up and drop-off the
	other driver." -- Lyft



	Interpretation:

	How long to travel from a start point to the other driver's start, to the
	other driver's finish, and finally to your own end point? Which starting
	point's path is longer?

	apath = a -> c -> d -> b
	bpath = c -> a -> b -> d

	apath >|< bpath



	Solution:
	Uses the 'haversine' formula to determine the great-circle distance between
	two points over the earth's surface on a direct path.



	References:

	// Provided planet radius numbers
	http://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
	 via: http://www.universetoday.com/15055/diameter-of-earth/
	  via: google.com

	// Provided algorithm
	http://www.movable-type.co.uk/scripts/latlong.html
	 via: google.com

	// Provided example coordinates & testing values
	http://www.chemical-ecology.net/java/lat-long.htm
	 via: google.com



	Notes & Limitations:

	This algorithm does not account for minor details such as oceans,
	mountains, traffic, unsafe neighborhoods, weather, road conditions, fuel
	level, lack of roads or other surface obstructions.

	This algorithm does not account for local earth's surface variations due to
	the moon or other celestial bodies, beyond what is already accounted for in
	the global averages included in the calculations provided by the sources.

	If they are the same distance the selected route is arbitrary but
	consistent.

	There may be room for optimization in the squaring procedures.

	This relies on an average, though a more sophisticated method with greater
	accuracy should be possible.

	Test coverage through, but less the 100%

	TODO: Write library to wrap generic type checking... further research req.

	"""

	equatorial_radius_kilometers = 6378.1
	polar_radius_kilometers = 6356.8
	volumetric_mean_radius_kilometers = 6371.0

	def __init__(self):
		self._log = logging.getLogger(__name__)

	@staticmethod
	def is_longer_trip( x, y ):
		"""Compares two routes to see which one can detour to complete the
		other more efficiently.

		Argument components should be floating point values.

		:param x: The first route.
			(source(latitude, longitude),destination(latitude, longitude))
		:param y: The second route.
			(source(latitude, longitude),destination(latitude, longitude))
		:return: True if the first route is longer, otherwise False
		"""

		# Check input
		invalid = "Invalid input to is_longer_trip! %s"
		if type(x) is not tuple:
			raise TypeError( invalid % "Expected tuple in arg[0]")
		elif len(x) is not 2:
			raise TypeError(invalid % "Incorrect tuple size in arg[0]")
		elif type(x[0]) is not tuple:
			raise TypeError(invalid % "Expected tuple in arg[0][0]")
		elif len(x[0]) is not 2:
			raise TypeError(invalid % "Incorrect tuple size in arg[0][0]")
		elif type(x[0][0]) is not float:
			raise TypeError(invalid % "Expected float in arg[0][0][0]")
		elif type(x[0][1]) is not float:
			raise TypeError(invalid % "Expected float in arg[0][0][0]")
		elif type(x[1]) is not tuple:
			raise TypeError(invalid % "Expected tuple in arg[0][1]")
		elif len(x[1]) is not 2:
			raise TypeError(invalid % "Incorrect tuple size in arg[0][1]")
		elif type(x[1][0]) is not float:
			raise TypeError(invalid % "Expected float in arg[0][1][0]")
		elif type(x[1][1]) is not float:
			raise TypeError(invalid % "Expected float in arg[0][1][1]")
		elif type(y) is not tuple:
			raise TypeError(invalid % "Expected tuple in arg[1]")
		elif len(y) is not 2:
			raise TypeError(invalid % "Incorrect tuple size in arg[1]")
		elif type(y[0]) is not tuple:
			raise TypeError(invalid % "Expected tuple in arg[1][0]")
		elif len(y[0]) is not 2:
			raise TypeError(invalid % "Incorrect tuple size in arg[1][0]")
		elif type(y[0][0]) is not float:
			raise TypeError(invalid % "Expected float in arg[1][0][0]")
		elif type(y[0][1]) is not float:
			raise TypeError(invalid % "Expected float in arg[1][0][1]")
		elif type(y[1]) is not tuple:
			raise TypeError(invalid % "Expected float in arg[1][1]")
		elif len(y) is not 2:
			raise TypeError(invalid % "Incorrect tuple size in arg[1][1]")
		elif type(y[1][0]) is not float:
			raise TypeError(invalid % "Expected float in arg[1][1][0]")
		elif type(y[1][1]) is not float:
			raise TypeError(invalid % "Expected float in arg[1][1][1]")


		a = x[0]
		b = x[1]
		c = y[0]
		d = y[1]

		xtrip = 0.0
		xtrip += SimpleCarpoolComparison.dist(a, c)
		xtrip += SimpleCarpoolComparison.dist(c, d)
		xtrip += SimpleCarpoolComparison.dist(d, b)
		logging.debug("xtrip is %f", xtrip)

		ytrip = 0.0
		ytrip += SimpleCarpoolComparison.dist(c, a)
		ytrip += SimpleCarpoolComparison.dist(a, b)
		ytrip += SimpleCarpoolComparison.dist(b, d)
		logging.debug("ytrip is %f", ytrip)

		if xtrip > ytrip:
			logging.debug("True, xtrip is longer")
			return True
		else:
			logging.debug("False, ytrip is longer")
			return False


	@staticmethod
	def dist(v1, v2):
		"""Determine the distance between two coordinate pairs on Earth.

		Argument elemental components should be floating point values.

		:param v1: (latitude, longitude)
		:param v2: (latitude, longitude)
		:return: distance_kilometers
		"""

		# Check input
		invalid = "Invalid input to dist! %s"
		if type(v1) is not tuple:
			raise TypeError( invalid % "Expected tuple in arg[0]")
		elif len(v1) is not 2:
			raise TypeError(invalid % "Incorrect tuple size in arg[0]")
		elif type(v1[0]) is not float:
			raise TypeError(invalid % "Expected float in arg[0][0]")
		elif type(v1[1]) is not float:
			raise TypeError(invalid % "Expected float in arg[0][1]")
		elif type(v2) is not tuple:
			raise TypeError( invalid % "Expected tuple in arg[1]")
		elif len(v2) is not 2:
			raise TypeError(invalid % "Incorrect tuple size in arg[1]")
		elif type(v2[0]) is not float:
			raise TypeError(invalid % "Expected float in arg[1][0]")
		elif type(v2[1]) is not float:
			raise TypeError(invalid % "Expected float in arg[1][1]")


		# radius of the earth

		# volumetric_mean_radius
		R = SimpleCarpoolComparison.volumetric_mean_radius_kilometers


		# determine the angle from the equator in radians

		# v1_lat_radians
		v1a = math.radians(v1[0])

		# v2_lat_radians
		v2a = math.radians(v2[0])


		# Determine the change in each direction

		# lat_delta
		lad = math.radians(v2[0] - v1[0])
		logging.debug('difference in latitude is %f', lad)

		# long_delta
		lod = math.radians(v2[1] - v1[1])
		logging.debug('difference in longitude is %f', lod)


		# half_chord_length_squared
		a = math.sin(lad / 2.0) * math.sin(lad / 2.0) + \
		    math.cos(v1a) * math.cos(v2a) * \
		    math.sin(lod / 2.0) * math.sin(lod / 2.0)
		logging.debug('half the chord length squared is %f', a)

		# angular_distance_radians
		c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
		logging.debug('angular distance is %f', c)

		# distance_kilometers
		d = R * c

		logging.debug('resulting distance between %s & %s is %f', v1, v2, d)
		return d


	@staticmethod
	def coordinate_to_float(degrees, minutes, seconds, sign):
		"""This takes the components of a coordinate and converts them to the
		number of degrees as floating point value.

		:param degrees: number of degrees as integer
		:param minutes: number of minutes as integer
		:param seconds: number of seconds as integer
		:param sign: True for North & West, False for South & East
		:return: the floating point representation of the coordinate component
		"""

		# Check input
		invalid = "Invalid input to coordinate_to_float! %s"
		if type(degrees) is not int:
			raise TypeError( invalid % "Expected int in arg[0]")
		elif type(minutes) is not int:
			raise TypeError( invalid % "Expected int in arg[1]")
		elif type(seconds) is not int:
			raise TypeError( invalid % "Expected int in arg[2]")
		elif type(sign) is not bool:
			raise TypeError( invalid % "Expected bool in arg[3]")

		ret = degrees + 0.0
		ret += minutes / 60.0
		ret += seconds / 3600.0
		if sign:
			return ret
		else:
			return -ret

# execute tests if the file was run directly
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)

	def within_tolerance(value, target):
		"""Determines if the value is within testing tolerance range."""
		tolerance = 0.001 # a tenth of a percent
		bottom_bound = target - target * tolerance
		top_bound = target + target * tolerance
		if value > bottom_bound:
			if value < top_bound:
				return True
		return False

	logging.warning("Running tests...")
	comp = SimpleCarpoolComparison()

	new_york_lat = comp.coordinate_to_float(40, 45, 6, True)
	new_york_long = comp.coordinate_to_float(73, 59, 39, True)
	new_york_coor = (new_york_lat, new_york_long)
	logging.info("New York Coordinates: %s", new_york_coor)

	san_francisco_lat = comp.coordinate_to_float(37, 46, 39, True)
	san_francisco_long = comp.coordinate_to_float(122, 24, 40, True)
	san_francisco_coor = (san_francisco_lat, san_francisco_long)
	logging.info("San Francisco Coordinates: %s", san_francisco_coor)

	sf_to_ny = comp.dist(san_francisco_coor, new_york_coor)
	logging.info("From San Francisco to New York (km): %f", sf_to_ny)
	sf_to_ny_comparison = 4125.62483398
	assert within_tolerance(sf_to_ny, sf_to_ny_comparison)

	washington_dc_lat = comp.coordinate_to_float(38, 49, 0, True)
	washington_dc_long = comp.coordinate_to_float(76, 59, 0, True)
	washington_dc_coor = (washington_dc_lat, washington_dc_long)
	logging.info("Washington DC Coordinates: %s", washington_dc_coor)

	dc_to_ny = comp.dist(washington_dc_coor, new_york_coor)
	logging.info("From Washington DC to New York (km): %s", dc_to_ny)
	dc_to_ny_comparison = 333.70534907
	assert within_tolerance(dc_to_ny,dc_to_ny_comparison)

	rio_de_janeiro_lat = comp.coordinate_to_float(22, 53, 43, False)
	rio_de_janeiro_long = comp.coordinate_to_float(43, 13, 22, True)
	rio_de_janeiro_coor = (rio_de_janeiro_lat, rio_de_janeiro_long)
	logging.info("Rio De Janeiro Coordinates: %s", rio_de_janeiro_coor)

	sf_to_rio = comp.dist(san_francisco_coor, rio_de_janeiro_coor)
	logging.info(
		"From San Francisco To Rio De Janeiro (km): %s", sf_to_rio)
	sf_to_rio_comparison = 10649.71401662
	assert within_tolerance(sf_to_rio,sf_to_rio_comparison)

	dc_to_rio = comp.dist(washington_dc_coor, rio_de_janeiro_coor)
	logging.info(
		"From Washington DC To Rio De Janeiro (km): %s", dc_to_rio)
	dc_to_rio_comparison = 7704.76741197
	assert within_tolerance(dc_to_rio,dc_to_rio_comparison)

	rio_to_ny = comp.dist(rio_de_janeiro_coor, new_york_coor)
	logging.info("From Rio De Janeiro To New York (km): %s", rio_to_ny)
	rio_to_ny_comparison = 7753.77149753
	assert within_tolerance(rio_to_ny,rio_to_ny_comparison)

	paris_lat = comp.coordinate_to_float(48, 52, 0, True)
	paris_long = comp.coordinate_to_float(2, 20, 0, False)
	paris_coor = (paris_lat, paris_long)
	logging.info("Paris Coordinates: %s", paris_coor)

	ny_to_paris = comp.dist(new_york_coor, paris_coor)
	logging.info("From New York to Paris (km): %s", ny_to_paris)
	ny_to_paris_comparison = 5828.25247481
	assert within_tolerance(ny_to_paris,ny_to_paris_comparison)

	paris_to_ny = comp.dist(paris_coor, new_york_coor)
	logging.info("From Paris to New York (km): %s", paris_to_ny)
	paris_to_ny_comparison = 5828.25247481
	assert within_tolerance(paris_to_ny,paris_to_ny_comparison)

	santiago_lat = comp.coordinate_to_float(33, 27, 0, False)
	santiago_long = comp.coordinate_to_float(70, 42, 0, True)
	santiago_coor = (santiago_lat, santiago_long)
	logging.info("Santiago Coordinates: %s", santiago_coor)

	st_to_ny = comp.dist(santiago_coor, new_york_coor)
	logging.info("From Santiago to New York (km): %s", st_to_ny)
	st_to_ny_comparison = 8252.19846886
	assert within_tolerance(st_to_ny, st_to_ny_comparison)

	st_to_paris = comp.dist(santiago_coor, paris_coor)
	logging.info("From Santiago to Paris (km): %s", st_to_paris)
	st_to_paris_comparison = 11642.40739436
	assert within_tolerance(st_to_paris, st_to_paris)

	gulf_of_guinea_lat  = 0.0
	gulf_of_guinea_long = 0.0
	gulf_of_guinea_coor = (gulf_of_guinea_lat,gulf_of_guinea_long)
	logging.info("Gulf of Guinea Coordinates: %s", gulf_of_guinea_coor)

	gog_to_ny = comp.dist(gulf_of_guinea_coor,new_york_coor)
	logging.info("From the Gulf of Guinea to New York (km): %s", gog_to_ny)
	gog_to_ny_comparison = 8661.04288456
	assert within_tolerance(gog_to_ny,gog_to_ny_comparison)

	paris_to_gog = comp.dist(paris_coor,gulf_of_guinea_coor)
	logging.info("From Paris to the Gulf of Guinea (km): %s", paris_to_gog)
	paris_to_gog_comparison = 5434.67290662
	assert within_tolerance(paris_to_gog, paris_to_gog_comparison)

	comp1 = comp.is_longer_trip((paris_coor,new_york_coor),
	                            (washington_dc_coor,san_francisco_coor))
	# faster to go to PARIS and come back then to backtrack across the US after
	assert comp1 == False

	comp2 = comp.is_longer_trip((san_francisco_coor,rio_de_janeiro_coor),
								(new_york_coor,san_francisco_coor))
	# in this case SF has to go to NY and back then travel to RIO
	# NY has to go to SF, then RIO, then back from RIO
	# RIO is very far, so doubling it's distance takes a lot of time
	assert comp2 == False

	comp3 = comp.is_longer_trip((gulf_of_guinea_coor,paris_coor),
								(rio_de_janeiro_coor,paris_coor))
	# in this case, RIO can go to GOG then PARIS
	# GOG must go to RIO, then backtrack to PARIS
	# RIO's is longer
	assert comp3 == True

	comp4 = comp.is_longer_trip((new_york_coor,san_francisco_coor),
								(new_york_coor,washington_dc_coor))
	# in this case NY2DC has to backtrack across the USA after dropping off
	assert comp4 == False

	# is_longer_trip

	# empty tuple
	raised = False
	try:
		comp.is_longer_trip((), new_york_coor)
	except TypeError:
		logging.info(
			"is_longer_trip: type checking on empty tuple arg[0] succeeds")
		raised = True
	if not raised:
		raise AssertionError(
			"is_longer_trip: type checking on empty tuple arg[0] failed!")

	raised = False
	try:
		comp.is_longer_trip(paris_coor, ())
	except TypeError:
		logging.info(
			"is_longer_trip: type checking on empty tuple arg[1] succeeds")
		raised = True
	if not raised:
		raise AssertionError(
			"is_longer_trip: type checking on empty tuple arg[1] failed!")

	# bad subtype
	raised = False
	try:
		comp.is_longer_trip(santiago_coor, (7,(4.4,5.5)))
	except TypeError:
		logging.info(
			"is_longer_trip: type checking on bad subtype arg[1][0] succeeds!"
			" (int)")
		raised = True
	if not raised:
		raise AssertionError(
			"is_longer_trip: type checking on empty tuple failed! (int)")

	raised = False
	try:
		comp.is_longer_trip(santiago_coor, ('(1.1, 1.2)',(4.4,5.5)))
	except TypeError:
		logging.info(
			"is_longer_trip: type checking on bad subtype arg[1][0] succeeds!"
			" (str)")
		raised = True
	if not raised:
		raise AssertionError(
			"is_longer_trip: type checking on bad subtype arg[1][0] failed! "
			"(str)")

	# bad elemental data type
	raised = False
	try:
		comp.is_longer_trip(san_francisco_coor, ((1.1, 1.2),(4.4,7)))
	except TypeError:
		logging.info(
			"is_longer_trip: type checking on bad subtype arg[0][0][1]"
			" succeeds! (int)")
		raised = True
	if not raised:
		raise AssertionError(
			"is_longer_trip: type checking on bad subtype arg[0][0][1]"
			" failed! (int)")

	raised = False
	try:
		comp.is_longer_trip(((('x'), 9.435),(4.,7.)),washington_dc_coor )
	except TypeError:
		logging.info(
			"is_longer_trip: type checking on bad subtype arg[0][0][0]"
			" succeeds! (tuple(str))")
		raised = True
	if not raised:
		raise AssertionError(
			"is_longer_trip: type checking on bad subtype arg[0][0][0]"
			" failed! (tuple(str))")

	# wrong tuple size
	raised = False
	try:
		comp.is_longer_trip(((6.6, 9.435, 4.5),(4.,7.)),washington_dc_coor )
	except TypeError:
		logging.info(
			"is_longer_trip: type checking on oversized tuple size succeeds!")
		raised = True
	if not raised:
		raise AssertionError(
			"is_longer_trip: type checking on oversized tuple size failed!")

	raised = False
	try:
		comp.is_longer_trip(((6.6, 9.435),(4.,)),washington_dc_coor )
	except TypeError:
		logging.info(
			"is_longer_trip: type checking on undersized tuple size succeeds!")
		raised = True
	if not raised:
		raise AssertionError(
			"is_longer_trip: type checking on undersized tuple size failed!")

	raised = False
	try:
		comp.is_longer_trip(
			((6.6, 9.435),(4.,5.5),(6.6,3.)),
			washington_dc_coor )
	except TypeError:
		logging.info(
			"is_longer_trip: type checking on extra tuple succeeds!")
		raised = True
	if not raised:
		raise AssertionError(
			"is_longer_trip: type checking on extra tuple size failed!")

	# dist

	raised = False
	try:
		comp.dist(washington_dc_coor,((1,2),(3,4)))
	except TypeError:
		logging.info(
			"dist: type checking on wrong elemental type succeeds! (int)")
		raised = True
	if not raised:
		raise AssertionError(
			"dist: type checking on wrong elemental type failed! (int)")


	raised = False
	try:
		comp.dist(washington_dc_coor,((),(3.,4.)))
	except TypeError:
		logging.info(
			"dist: type checking on empty sub-tuple succeeds!")
		raised = True
	if not raised:
		raise AssertionError(
			"dist: type checking on empty sub-tuple failed!")


	raised = False
	try:
		comp.dist(washington_dc_coor,((2.,4.,1.7),(3.,4.)))
	except TypeError:
		logging.info(
			"dist: type checking on wrong tuple size succeeds!")
		raised = True
	if not raised:
		raise AssertionError(
			"dist: type checking on wrong tuple size failed!")

	# coordinate_to_float
	raised = False
	try:
		comp.coordinate_to_float(6.6,5,4,True)
	except TypeError:
		logging.info(
			"coordinate_to_float: type checking on wrong argument type "
			"succeeds! (float)")
		raised = True
	if not raised:
		raise AssertionError(
			"coordinate_to_float: type checking on wrong argument type"
			" failed! (float)")

	raised = False
	try:
		comp.coordinate_to_float(6,5,4,1)
	except TypeError:
		logging.info(
			"coordinate_to_float: type checking on wrong argument type "
			"succeeds! arg[3] (int instead of bool)")
		raised = True
	if not raised:
		raise AssertionError(
			"coordinate_to_float: type checking on wrong argument type"
			" failed! arg[3](int instead of bool)")

	logging.warning("All tests passed!")
