################################################################################
#          This file was automatically generated. Please do not edit.          #
################################################################################

import javawrappers.java.lang
import javawrappers.java.util

from jpype.types import *
from typing import Union

from typing import overload

class Reportable:
	def getMessageParameters(self, ) -> JArray(javawrappers.java.lang.Object, 1): ...
	@overload
	def getMessage(self, ) -> javawrappers.java.lang.String: ...
	@overload
	def getMessage(self, arg0: javawrappers.java.util.ResourceBundle, ) -> javawrappers.java.lang.String: ...
	def getMessageCode(self, ) -> javawrappers.java.lang.String: ...


