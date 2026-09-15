# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.11.5 | packaged by Anaconda, Inc. | (main, Sep 11 2023, 13:26:23) [MSC v.1916 64 bit (AMD64)]
# From type library '{00021A98-0000-0000-C000-000000000046}'
# On Sat Sep 12 14:27:46 2026
'Microsoft Visio 16.0 Type Library'
makepy_version = '0.5.01'
python_version = 0x30b05f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{00021A98-0000-0000-C000-000000000046}')
MajorVersion = 4
MinorVersion = 16
LibraryFlags = 8
LCID = 0x0

from win32com.client import DispatchBaseClass
class IVCell(DispatchBaseClass):
	CLSID = IID('{000D0701-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{000D0A0D-0000-0000-C000-000000000046}')

	def GlueTo(self, CellObject=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (24, 0), ((9, 1),),CellObject
			)

	def GlueToPos(self, SheetObject=defaultNamedNotOptArg, xPercent=defaultNamedNotOptArg, yPercent=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), ((9, 1), (5, 1), (5, 1)),SheetObject
			, xPercent, yPercent)

	# The method Result is actually a property, but must be used as a method to correctly pass the arguments
	def Result(self, UnitsNameOrCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 2, (5, 0), ((12, 1),),UnitsNameOrCode
			)

	# The method ResultForce is actually a property, but must be used as a method to correctly pass the arguments
	def ResultForce(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(9, LCID, 4, (24, 0), ((12, 1), (5, 1)),UnitsNameOrCode
			, arg1)

	# The method ResultFromInt is actually a property, but must be used as a method to correctly pass the arguments
	def ResultFromInt(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(2499, LCID, 4, (24, 0), ((12, 1), (3, 1)),UnitsNameOrCode
			, arg1)

	# The method ResultFromIntForce is actually a property, but must be used as a method to correctly pass the arguments
	def ResultFromIntForce(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(25, LCID, 4, (24, 0), ((12, 1), (3, 1)),UnitsNameOrCode
			, arg1)

	# The method ResultInt is actually a property, but must be used as a method to correctly pass the arguments
	def ResultInt(self, UnitsNameOrCode=defaultNamedNotOptArg, fRound=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(24, LCID, 2, (3, 0), ((12, 1), (2, 1)),UnitsNameOrCode
			, fRound)

	# The method ResultStr is actually a property, but must be used as a method to correctly pass the arguments
	def ResultStr(self, UnitsNameOrCode=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(26, LCID, 2, (8, 0), ((12, 1),),UnitsNameOrCode
			)

	# The method ResultStrU is actually a property, but must be used as a method to correctly pass the arguments
	def ResultStrU(self, UnitsNameOrCode=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1610743855, LCID, 2, (8, 0), ((12, 1),),UnitsNameOrCode
			)

	# The method SetResult is actually a property, but must be used as a method to correctly pass the arguments
	def SetResult(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(8, LCID, 4, (24, 0), ((12, 1), (5, 1)),UnitsNameOrCode
			, arg1)

	def Trigger(self):
		return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		# Method 'Application' returns object of type 'IVApplication'
		"Application": (1, 2, (9, 0), (), "Application", '{000D0700-0000-0000-C000-000000000046}'),
		"Column": (21, 2, (2, 0), (), "Column", None),
		"ContainingMasterID": (1610743854, 2, (3, 0), (), "ContainingMasterID", None),
		"ContainingPageID": (1610743853, 2, (3, 0), (), "ContainingPageID", None),
		# Method 'ContainingRow' returns object of type 'IVRow'
		"ContainingRow": (30, 2, (9, 0), (), "ContainingRow", '{000D0725-0000-0000-C000-000000000046}'),
		# Method 'Dependents' returns object of type 'IVCell'
		"Dependents": (1610743851, 2, (8201, 0), (), "Dependents", '{000D0701-0000-0000-C000-000000000046}'),
		# Method 'Document' returns object of type 'IVDocument'
		"Document": (16, 2, (9, 0), (), "Document", '{000D0705-0000-0000-C000-000000000046}'),
		"Error": (3, 2, (2, 0), (), "Error", None),
		# Method 'EventList' returns object of type 'IVEventList'
		"EventList": (28, 2, (9, 0), (), "EventList", '{000D071B-0000-0000-C000-000000000046}'),
		"Formula": (4, 2, (8, 0), (), "Formula", None),
		"FormulaU": (31, 2, (8, 0), (), "FormulaU", None),
		# Method 'InheritedFormulaSource' returns object of type 'IVCell'
		"InheritedFormulaSource": (1610743850, 2, (9, 0), (), "InheritedFormulaSource", '{000D0701-0000-0000-C000-000000000046}'),
		# Method 'InheritedValueSource' returns object of type 'IVCell'
		"InheritedValueSource": (1610743849, 2, (9, 0), (), "InheritedValueSource", '{000D0701-0000-0000-C000-000000000046}'),
		"IsConstant": (22, 2, (2, 0), (), "IsConstant", None),
		"IsInherited": (23, 2, (2, 0), (), "IsInherited", None),
		"LocalName": (14, 2, (8, 0), (), "LocalName", None),
		"Name": (13, 2, (8, 0), (), "Name", None),
		"ObjectType": (2, 2, (2, 0), (), "ObjectType", None),
		"PersistsEvents": (29, 2, (2, 0), (), "PersistsEvents", None),
		# Method 'Precedents' returns object of type 'IVCell'
		"Precedents": (1610743852, 2, (8201, 0), (), "Precedents", '{000D0701-0000-0000-C000-000000000046}'),
		"ResultIU": (0, 2, (5, 0), (), "ResultIU", None),
		"Row": (20, 2, (2, 0), (), "Row", None),
		"RowName": (15, 2, (8, 0), (), "RowName", None),
		"RowNameU": (33, 2, (8, 0), (), "RowNameU", None),
		"Section": (19, 2, (2, 0), (), "Section", None),
		# Method 'Shape' returns object of type 'IVShape'
		"Shape": (17, 2, (9, 0), (), "Shape", '{000D070C-0000-0000-C000-000000000046}'),
		"Stat": (11, 2, (2, 0), (), "Stat", None),
		# Method 'Style' returns object of type 'IVStyle'
		"Style": (18, 2, (9, 0), (), "Style", '{000D070E-0000-0000-C000-000000000046}'),
		"Units": (12, 2, (2, 0), (), "Units", None),
	}
	_prop_map_put_ = {
		"Formula": ((4, LCID, 4, 0),()),
		"FormulaForce": ((5, LCID, 4, 0),()),
		"FormulaForceU": ((32, LCID, 4, 0),()),
		"FormulaU": ((31, LCID, 4, 0),()),
		"ResultIU": ((0, LCID, 4, 0),()),
		"ResultIUForce": ((10, LCID, 4, 0),()),
		"RowName": ((15, LCID, 4, 0),()),
		"RowNameU": ((33, LCID, 4, 0),()),
	}
	# Default property for this class is 'ResultIU'
	def __call__(self):
		return self._ApplyTypes_(*(0, 2, (5, 0), (), "ResultIU", None))
	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

win32com.client.CLSIDToClass.RegisterCLSID( "{000D0701-0000-0000-C000-000000000046}", IVCell )
# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.11.5 | packaged by Anaconda, Inc. | (main, Sep 11 2023, 13:26:23) [MSC v.1916 64 bit (AMD64)]
# From type library '{00021A98-0000-0000-C000-000000000046}'
# On Sat Sep 12 14:27:46 2026
'Microsoft Visio 16.0 Type Library'
makepy_version = '0.5.01'
python_version = 0x30b05f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{00021A98-0000-0000-C000-000000000046}')
MajorVersion = 4
MinorVersion = 16
LibraryFlags = 8
LCID = 0x0

IVCell_vtables_dispatch_ = 1
IVCell_vtables_ = [
	(( 'Application' , 'lpdispRet' , ), 1, (1, (), [ (16393, 10, None, "IID('{000D0700-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'ObjectType' , 'lpi2Ret' , ), 2, (2, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Error' , 'lpi2Ret' , ), 3, (3, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Formula' , 'lpbstrRet' , ), 4, (4, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Formula' , 'lpbstrRet' , ), 4, (4, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'FormulaForce' , ), 5, (5, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GlueTo' , 'CellObject' , ), 6, (6, (), [ (9, 1, None, "IID('{000D0701-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GlueToPos' , 'SheetObject' , 'xPercent' , 'yPercent' , ), 7, (7, (), [ 
			 (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (5, 1, None, None) , (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Result' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 8, (8, (), [ (12, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Result' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 8, (8, (), [ (12, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'ResultForce' , 'UnitsNameOrCode' , ), 9, (9, (), [ (12, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'ResultIU' , 'lpr8Ret' , ), 0, (0, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'ResultIU' , 'lpr8Ret' , ), 0, (0, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'ResultIUForce' , ), 10, (10, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'Stat' , 'lpi2Ret' , ), 11, (11, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'Units' , 'lpi2Ret' , ), 12, (12, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'Name' , 'lpLocaleIndependentName' , ), 13, (13, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'LocalName' , 'lpLocaleSpecificName' , ), 14, (14, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'RowName' , 'lpbstrRet' , ), 15, (15, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'Document' , 'lpdispRet' , ), 16, (16, (), [ (16393, 10, None, "IID('{000D0705-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'Shape' , 'lpdispRet' , ), 17, (17, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'Style' , 'lpdispRet' , ), 18, (18, (), [ (16393, 10, None, "IID('{000D070E-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'Section' , 'lpi2Ret' , ), 19, (19, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'Row' , 'lpi2Ret' , ), 20, (20, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'Column' , 'lpi2Ret' , ), 21, (21, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'IsConstant' , 'lpi2Ret' , ), 22, (22, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'IsInherited' , 'lpi2Ret' , ), 23, (23, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'ResultInt' , 'UnitsNameOrCode' , 'fRound' , 'lpi4Ret' , ), 24, (24, (), [ 
			 (12, 1, None, None) , (2, 1, None, None) , (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'ResultFromInt' , 'UnitsNameOrCode' , ), 2499, (2499, (), [ (12, 1, None, None) , (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'ResultFromIntForce' , 'UnitsNameOrCode' , ), 25, (25, (), [ (12, 1, None, None) , (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'ResultStr' , 'UnitsNameOrCode' , 'lpbstrRet' , ), 26, (26, (), [ (12, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'Trigger' , ), 27, (27, (), [ ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'RowName' , 'lpbstrRet' , ), 15, (15, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'EventList' , 'lpdispRet' , ), 28, (28, (), [ (16393, 10, None, "IID('{000D071B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'PersistsEvents' , 'lpboolRet' , ), 29, (29, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'ContainingRow' , 'lpdispRet' , ), 30, (30, (), [ (16393, 10, None, "IID('{000D0725-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'FormulaU' , 'lpbstrRet' , ), 31, (31, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'FormulaU' , 'lpbstrRet' , ), 31, (31, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'FormulaForceU' , ), 32, (32, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'RowNameU' , 'lpLocaleIndependentName' , ), 33, (33, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'RowNameU' , 'lpLocaleIndependentName' , ), 33, (33, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'InheritedValueSource' , 'ppCell' , ), 1610743849, (1610743849, (), [ (16393, 10, None, "IID('{000D0701-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'InheritedFormulaSource' , 'ppCell' , ), 1610743850, (1610743850, (), [ (16393, 10, None, "IID('{000D0701-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'Dependents' , 'dependentCellsArray' , ), 1610743851, (1610743851, (), [ (24585, 10, None, "IID('{000D0701-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'Precedents' , 'precedentCellsArray' , ), 1610743852, (1610743852, (), [ (24585, 10, None, "IID('{000D0701-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'ContainingPageID' , 'lpi4Ret' , ), 1610743853, (1610743853, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'ContainingMasterID' , 'lpi4Ret' , ), 1610743854, (1610743854, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'ResultStrU' , 'UnitsNameOrCode' , 'lpbstrRet' , ), 1610743855, (1610743855, (), [ (12, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
]

win32com.client.CLSIDToClass.RegisterCLSID( "{000D0701-0000-0000-C000-000000000046}", IVCell )
