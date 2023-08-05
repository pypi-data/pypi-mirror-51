################################################################################
#          This file was automatically generated. Please do not edit.          #
################################################################################

import javawrappers.java.lang
import javawrappers.java.net
import javawrappers.org.matsim.core.api.internal
import javawrappers.org.matsim.api.core.v01.network
import javawrappers.org.matsim.api.core.v01

from jpype.types import *
from typing import Union

from typing import overload

class MatsimComparator:


class MatsimWriter:
	def write(self, arg0: javawrappers.java.lang.String, ) -> None: ...


class MatsimExtensionPoint:


class HasPersonId:
	def getPersonId(self, ) -> javawrappers.org.matsim.api.core.v01.Id: ...


class MatsimManager:


class MatsimReader:
	def readFile(self, arg0: javawrappers.java.lang.String, ) -> None: ...
	def readURL(self, arg0: javawrappers.java.net.URL, ) -> None: ...


class MatsimPopulationObject:


class MatsimNetworkObject:


class NetworkRunnable:
	def run(self, arg0: javawrappers.org.matsim.api.core.v01.network.Network, ) -> None: ...


class MatsimFacilitiesObject:


class MatsimFactory:


class MatsimDataClassImplMarkerInterface:


class MatsimParameters:


class MatsimToplevelContainer:
	def getFactory(self, ) -> javawrappers.org.matsim.core.api.internal.MatsimFactory: ...


class MatsimSomeWriter:


class MatsimSomeReader:


