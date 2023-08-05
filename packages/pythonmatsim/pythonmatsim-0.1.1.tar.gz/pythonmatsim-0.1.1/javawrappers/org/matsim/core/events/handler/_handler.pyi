################################################################################
#          This file was automatically generated. Please do not edit.          #
################################################################################

import javawrappers.org.matsim.api.core.v01.events

from jpype.types import *
from typing import Union

from typing import overload

class BasicEventHandler:
	def handleEvent(self, arg0: javawrappers.org.matsim.api.core.v01.events.Event, ) -> None: ...
	def reset(self, arg0: Union[int, JInt], ) -> None: ...


class EventHandler:
	def reset(self, arg0: Union[int, JInt], ) -> None: ...


