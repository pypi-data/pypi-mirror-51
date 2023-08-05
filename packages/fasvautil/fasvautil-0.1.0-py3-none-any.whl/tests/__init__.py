# -*- coding: utf-8 -*-
# Copyright (c) 2019 by Lars Klitzke, Lars.Klitzke@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import ssl

import dagmar as dm
from dagmar.core import StreetFinder, MappedVehiclePose
from dagmar.location import OSM, GPSLocation

streetfinder = StreetFinder(
    OSM(**{'url': 'https://mux.hs-emden-leer.de/overpass/api/interpreter', "context": ssl._create_unverified_context()})
)

# get ways of crossroads Ubierstraße, Larrelter Straße, Schlesiersraße

UBIERSTRASSE_NORTH = streetfinder.way(646115131)
UBIERSTRASSE_SOUTH = streetfinder.way(15931699)

LARRELTERSTRASSE_EAST_MAIN = streetfinder.way(131757963)
LARRELTERSTRASSE_MAIN = streetfinder.way(646115130)

LARRELTERSTRASSE_MAIN_EAST = streetfinder.way(369036938)
LARRELTERSTRASSE_EAST = streetfinder.way(646115132)

SCHLESIERSTRASSE_NORTH_MAIN = streetfinder.way(103428069)
SCHLESIERSTRASSE_MAIN = streetfinder.way(646115133)

P1 = MappedVehiclePose(wayid=UBIERSTRASSE_NORTH.id, way=UBIERSTRASSE_NORTH,
                       location=GPSLocation(position=(0, 0), deviation=(0, 0)),  likelihood=0.99, velocity=1,
                       orientation=0.1, streetfinder=streetfinder)
P2 = MappedVehiclePose(wayid=LARRELTERSTRASSE_MAIN.id, way=LARRELTERSTRASSE_MAIN,
                       location=GPSLocation(position=(0, 0), deviation=(0, 0)),  likelihood=0.99, velocity=1,
                       orientation=0.1, streetfinder=streetfinder)
P3 = MappedVehiclePose(wayid=SCHLESIERSTRASSE_NORTH_MAIN.id, way=SCHLESIERSTRASSE_NORTH_MAIN,
                       location=GPSLocation(position=(0, 0), deviation=(0, 0)),  likelihood=0.99, velocity=1,
                       orientation=0.1, streetfinder=streetfinder)
P4 = MappedVehiclePose(wayid=SCHLESIERSTRASSE_MAIN.id, way=SCHLESIERSTRASSE_MAIN,
                       location=GPSLocation(position=(0, 0), deviation=(0, 0)),  likelihood=0.99, velocity=1,
                       orientation=0.1, streetfinder=streetfinder)
P5 = MappedVehiclePose(wayid=LARRELTERSTRASSE_EAST.id, way=LARRELTERSTRASSE_EAST,
                       location=GPSLocation(position=(0, 0), deviation=(0, 0)),  likelihood=0.99, velocity=1,
                       orientation=0.1, streetfinder=streetfinder)

P6 = MappedVehiclePose(wayid=UBIERSTRASSE_SOUTH.id, way=UBIERSTRASSE_SOUTH,
                       location=GPSLocation(position=(0, 0), deviation=(0, 0)),  likelihood=0.99, velocity=1,
                       orientation=0.1, streetfinder=streetfinder)