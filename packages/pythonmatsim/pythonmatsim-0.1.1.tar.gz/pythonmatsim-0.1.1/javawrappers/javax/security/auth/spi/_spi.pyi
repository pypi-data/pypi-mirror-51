################################################################################
#          This file was automatically generated. Please do not edit.          #
################################################################################

import javawrappers.java.util
import javawrappers.javax.security.auth.callback
import javawrappers.javax.security.auth

from jpype.types import *
from typing import Union

from typing import overload

class LoginModule:
	def logout(self, ) -> Union[int, JBoolean]: ...
	def abort(self, ) -> Union[int, JBoolean]: ...
	def commit(self, ) -> Union[int, JBoolean]: ...
	def initialize(self, arg0: javawrappers.javax.security.auth.Subject, arg1: javawrappers.javax.security.auth.callback.CallbackHandler, arg2: javawrappers.java.util.Map, arg3: javawrappers.java.util.Map, ) -> None: ...
	def login(self, ) -> Union[int, JBoolean]: ...


