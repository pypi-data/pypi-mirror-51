################################################################################
#          This file was automatically generated. Please do not edit.          #
################################################################################

import javawrappers.org.matsim.core.controler.events

from jpype.types import *
from typing import Union

from typing import overload

class ScoringListener:
	def notifyScoring(self, arg0: javawrappers.org.matsim.core.controler.events.ScoringEvent, ) -> None: ...


class ReplanningListener:
	def notifyReplanning(self, arg0: javawrappers.org.matsim.core.controler.events.ReplanningEvent, ) -> None: ...


class AfterMobsimListener:
	def notifyAfterMobsim(self, arg0: javawrappers.org.matsim.core.controler.events.AfterMobsimEvent, ) -> None: ...


class StartupListener:
	def notifyStartup(self, arg0: javawrappers.org.matsim.core.controler.events.StartupEvent, ) -> None: ...


class IterationEndsListener:
	def notifyIterationEnds(self, arg0: javawrappers.org.matsim.core.controler.events.IterationEndsEvent, ) -> None: ...


class ShutdownListener:
	def notifyShutdown(self, arg0: javawrappers.org.matsim.core.controler.events.ShutdownEvent, ) -> None: ...


class IterationStartsListener:
	def notifyIterationStarts(self, arg0: javawrappers.org.matsim.core.controler.events.IterationStartsEvent, ) -> None: ...


class ControlerListener:


class BeforeMobsimListener:
	def notifyBeforeMobsim(self, arg0: javawrappers.org.matsim.core.controler.events.BeforeMobsimEvent, ) -> None: ...


