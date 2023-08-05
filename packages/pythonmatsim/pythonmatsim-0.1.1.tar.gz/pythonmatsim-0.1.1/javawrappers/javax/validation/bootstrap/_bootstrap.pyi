################################################################################
#          This file was automatically generated. Please do not edit.          #
################################################################################

import javawrappers.javax.validation.bootstrap
import javawrappers.javax.validation

from jpype.types import *
from typing import Union

from typing import overload

class GenericBootstrap:
	def providerResolver(self, arg0: javawrappers.javax.validation.ValidationProviderResolver, ) -> javawrappers.javax.validation.bootstrap.GenericBootstrap: ...
	def configure(self, ) -> javawrappers.javax.validation.Configuration: ...


class ProviderSpecificBootstrap:
	def providerResolver(self, arg0: javawrappers.javax.validation.ValidationProviderResolver, ) -> javawrappers.javax.validation.bootstrap.ProviderSpecificBootstrap: ...
	def configure(self, ) -> javawrappers.javax.validation.Configuration: ...


