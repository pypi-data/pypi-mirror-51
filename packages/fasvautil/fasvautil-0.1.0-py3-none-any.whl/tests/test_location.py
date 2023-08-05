import ssl
import unittest

import numpy

import fasvautil as fu

from fasvautil.location import Location, GPSLocation, UTMLocation, gps_utm_location, OSM, StreetFinder


class LocationTest(unittest.TestCase):

    def test_create_location_with_dev(self):
        l = Location(position=(53.368367, 7.184645), deviation=(0.5, 0.5))

    def test_create_location_without_dev(self):
        l = Location(position=(53.368367, 7.184645))

        self.assertEqual(l.deviation[0], 0)
        self.assertEqual(l.deviation[1], 0)

    def test_print_location(self):
        l = Location(position=(53.368367, 7.184645), deviation=(0.5, 0.5))

        print("{}".format(l))

    def test_check_invalid(self):

        l = Location(position=(None, None))

        self.assertFalse(l.valid())

class GPSLocationTest(unittest.TestCase):

    def test_create_gpslocation(self):
        l = GPSLocation(position=(53.368367, 7.184645))

        self.assertEqual(l.latitude, 53.368367)

    def test_convert_to_utm(self):
        l = GPSLocation(position=(53.368367, 7.184645))

        u = l.as_utm()

        # https://www.koordinaten-umrechner.de/Dezimal/53.368367,7.184645?karte=OpenStreetMap&zoom=17
        self.assertTrue(numpy.isclose(u.easting, 379216.092))
        self.assertTrue(numpy.isclose(u.northing, 5914785.340))
        self.assertEqual((32, 'U'), u.zone)
        self.assertEqual((u.zone_number, u.zone_letter), u.zone)

    def test_create_mean_gps(self):

        r = GPSLocation.from_list(numpy.asarray([
            (53.368367, 7.184645),
            (53.368367, 7.184645),
            (53.368367, 7.184645),
            (53.368367, 7.184645)

        ]), [0.25, 0.25, 0.25, 0.25])

        self.assertEqual(53.368367, r.latitude)
        self.assertTrue(7.184645, r.longitude)

        r = GPSLocation.from_list(numpy.asarray([
            (53.368367, 7.184645),
            (53.368367, 7.184645),

        ]).T, [0.5, 0.5])

        self.assertEqual(53.368367, r.latitude)
        self.assertTrue(7.184645, r.longitude)


class UTMLocationTest(unittest.TestCase):

    def test_create_utmlocation(self):
        l =  UTMLocation(position=(379216.092, 5914785.340), zone=(32, 'U'))

        self.assertEqual(l.easting, 379216.092)

    def test_create_utm_without_zone_error(self):

        with self.assertRaises(fu.location.InvalidUTMLocation):
            l = UTMLocation(position=(379216.092, 5914785.340), zone=[32, ])

    def test_create_utm_without_zone_params_error(self):

        with self.assertRaises(fu.location.InvalidUTMLocation):
            l = UTMLocation(position=(379216.092, 5914785.340))


    def test_convert_to_gps(self):
        l =  UTMLocation(position=(379216.092, 5914785.340), zone=(32, 'U'))

        u = l.as_gps()

        # https://www.koordinaten-umrechner.de/Dezimal/53.368367,7.184645?karte=OpenStreetMap&zoom=17
        self.assertTrue(numpy.isclose(u.latitude, 53.368367))
        self.assertTrue(numpy.isclose(u.longitude, 7.184645))

    def test_from_list_of_gpslocation_obj(self):

        utms = gps_utm_location([GPSLocation(position=(53.368367, 7.184645)),
                                 GPSLocation(position=(53.368367, 7.184645)),
                                 GPSLocation(position=(53.368367, 7.184645))])

        self.assertEqual(3, len(utms))

    def test_from_list_of_gps_coordinates(self):
        utms = gps_utm_location([(53.368367, 7.184645),
                                 (53.368367, 7.184645),
                                 (53.368367, 7.184645)])

        self.assertEqual(3, len(utms))


class TestStreetFinder(unittest.TestCase):

    def test_create_streetfinder(self):
        streetfinder = StreetFinder(
            OSM(**{'url': 'https://mux.hs-emden-leer.de/overpass/api/interpreter',
                   "context": ssl._create_unverified_context()})
        )

        way = streetfinder.way(646115131)

        self.assertIsNotNone(way)
        self.assertEqual(646115131, way.id)

