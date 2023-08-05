################################################################################
#          This file was automatically generated. Please do not edit.          #
################################################################################

import javawrappers.org.matsim.api.core.v01.population
import javawrappers.org.matsim.core.replanning

from jpype.types import *
from typing import Union

from typing import overload

class PlanStrategyModule:
	@overload
	def handlePlan(self, arg0: javawrappers.org.matsim.api.core.v01.population.BasicPlan, ) -> None: ...
	@overload
	def handlePlan(self, arg0: javawrappers.org.matsim.api.core.v01.population.Plan, ) -> None: ...
	def prepareReplanning(self, arg0: javawrappers.org.matsim.core.replanning.ReplanningContext, ) -> None: ...
	def finishReplanning(self, ) -> None: ...


