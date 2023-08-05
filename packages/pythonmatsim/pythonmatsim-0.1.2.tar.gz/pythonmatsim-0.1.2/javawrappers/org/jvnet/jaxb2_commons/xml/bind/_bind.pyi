################################################################################
#          This file was automatically generated. Please do not edit.          #
################################################################################

import javawrappers.java.lang
import javawrappers.javax.xml.bind

from jpype.types import *
from typing import Union

from typing import overload

class AfterUnmarshallCallback:
	def afterUnmarshal(self, arg0: javawrappers.javax.xml.bind.Unmarshaller, arg1: javawrappers.java.lang.Object, ) -> None: ...


class BeforeMarshallCallback:
	def beforeMarshal(self, arg0: javawrappers.javax.xml.bind.Marshaller, ) -> None: ...


class BeforeUnmarshallCallback:
	def beforeUnmarshal(self, arg0: javawrappers.javax.xml.bind.Unmarshaller, arg1: javawrappers.java.lang.Object, ) -> None: ...


class AfterMarshallCallback:
	def afterMarshal(self, arg0: javawrappers.javax.xml.bind.Marshaller, ) -> None: ...


class ContextPathAware:
	def getContextPath(self, ) -> javawrappers.java.lang.String: ...


