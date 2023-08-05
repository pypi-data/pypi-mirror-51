################################################################################
#          This file was automatically generated. Please do not edit.          #
################################################################################

import javawrappers.javax.measure
import javawrappers.java.lang

from jpype.types import *
from typing import Union

from typing import overload

class FactorSupplier:
	def getFactor(self, ) -> javawrappers.java.lang.Object: ...


class DoubleFactorSupplier:
	def getFactor(self, ) -> Union[float, JDouble]: ...


class ValueSupplier:
	def getValue(self, ) -> javawrappers.java.lang.Object: ...


class IntPrioritySupplier:
	def getPriority(self, ) -> Union[int, JInt]: ...


class Versioned:
	def getVersion(self, ) -> javawrappers.java.lang.Object: ...


class Nameable:
	def getName(self, ) -> javawrappers.java.lang.String: ...


class IntIdentifiable:
	def getId(self, ) -> Union[int, JInt]: ...


class UnitConverterSupplier:
	def getConverter(self, ) -> javawrappers.javax.measure.UnitConverter: ...


class DescriptionSupplier:
	def getDescription(self, ) -> javawrappers.java.lang.String: ...


class SymbolSupplier:
	def getSymbol(self, ) -> javawrappers.java.lang.String: ...


class MaximumSupplier:
	def getMaximum(self, ) -> javawrappers.java.lang.Object: ...


class QuantitySupplier:
	def getQuantity(self, ) -> javawrappers.javax.measure.Quantity: ...


class LongIdentifiable:
	def getId(self, ) -> Union[long, JLong]: ...


class MinimumSupplier:
	def getMinimum(self, ) -> javawrappers.java.lang.Object: ...


class Parser:
	def parse(self, arg0: javawrappers.java.lang.Object, ) -> javawrappers.java.lang.Object: ...


class UnitSupplier:
	def getUnit(self, ) -> javawrappers.javax.measure.Unit: ...


class Coded:
	def getCode(self, ) -> javawrappers.java.lang.Object: ...


class QuantityOperator:
	def apply(self, arg0: javawrappers.javax.measure.Quantity, ) -> javawrappers.javax.measure.Quantity: ...


class IntMaximumSupplier:
	def getMaximum(self, ) -> Union[int, JInt]: ...


class LabelSupplier:
	def getLabel(self, ) -> javawrappers.java.lang.String: ...


class Identifiable:
	def getId(self, ) -> javawrappers.java.lang.Object: ...


class IntMinimumSupplier:
	def getMinimum(self, ) -> javawrappers.java.lang.Object: ...


