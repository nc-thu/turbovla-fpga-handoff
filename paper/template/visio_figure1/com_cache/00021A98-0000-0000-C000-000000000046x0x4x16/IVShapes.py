# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.11.5 | packaged by Anaconda, Inc. | (main, Sep 11 2023, 13:26:23) [MSC v.1916 64 bit (AMD64)]
# From type library '{00021A98-0000-0000-C000-000000000046}'
# On Sat Sep 12 14:28:16 2026
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
class IVShapes(DispatchBaseClass):
	CLSID = IID('{000D070D-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{000D0A09-0000-0000-C000-000000000046}')

	def CenterDrawing(self):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), (),)

	# Result is of type IVShape
	# The method Item is actually a property, but must be used as a method to correctly pass the arguments
	def Item(self, NameUIDOrIndex=defaultNamedNotOptArg):
		'The first item in a Shapes collection is item 1. Name treated as locale specific.'
		ret = self._oleobj_.InvokeTypes(0, LCID, 2, (9, 0), ((12, 1),),NameUIDOrIndex
			)
		if ret is not None:
			ret = Dispatch(ret, 'Item', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	# The method ItemFromID is actually a property, but must be used as a method to correctly pass the arguments
	def ItemFromID(self, ObjectID=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 2, (9, 0), ((3, 1),),ObjectID
			)
		if ret is not None:
			ret = Dispatch(ret, 'ItemFromID', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	# The method ItemFromID16 is actually a property, but must be used as a method to correctly pass the arguments
	def ItemFromID16(self, ObjectID=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 2, (9, 0), ((2, 1),),ObjectID
			)
		if ret is not None:
			ret = Dispatch(ret, 'ItemFromID16', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	# The method ItemFromUniqueID is actually a property, but must be used as a method to correctly pass the arguments
	def ItemFromUniqueID(self, UniqueID=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743825, LCID, 2, (9, 0), ((8, 1),),UniqueID
			)
		if ret is not None:
			ret = Dispatch(ret, 'ItemFromUniqueID', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	# The method ItemU is actually a property, but must be used as a method to correctly pass the arguments
	def ItemU(self, NameUIDOrIndex=defaultNamedNotOptArg):
		'Like Item() but names treated locale independent.'
		ret = self._oleobj_.InvokeTypes(15, LCID, 2, (9, 0), ((12, 1),),NameUIDOrIndex
			)
		if ret is not None:
			ret = Dispatch(ret, 'ItemU', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	_prop_map_get_ = {
		# Method 'Application' returns object of type 'IVApplication'
		"Application": (3, 2, (9, 0), (), "Application", '{000D0700-0000-0000-C000-000000000046}'),
		# Method 'ContainingMaster' returns object of type 'IVMaster'
		"ContainingMaster": (6, 2, (9, 0), (), "ContainingMaster", '{000D0707-0000-0000-C000-000000000046}'),
		# Method 'ContainingPage' returns object of type 'IVPage'
		"ContainingPage": (5, 2, (9, 0), (), "ContainingPage", '{000D0709-0000-0000-C000-000000000046}'),
		# Method 'ContainingShape' returns object of type 'IVShape'
		"ContainingShape": (7, 2, (9, 0), (), "ContainingShape", '{000D070C-0000-0000-C000-000000000046}'),
		"Count": (13, 2, (3, 0), (), "Count", None),
		"Count16": (1, 2, (2, 0), (), "Count16", None),
		# Method 'Document' returns object of type 'IVDocument'
		"Document": (4, 2, (9, 0), (), "Document", '{000D0705-0000-0000-C000-000000000046}'),
		# Method 'EventList' returns object of type 'IVEventList'
		"EventList": (10, 2, (9, 0), (), "EventList", '{000D071B-0000-0000-C000-000000000046}'),
		"ObjectType": (2, 2, (2, 0), (), "ObjectType", None),
		"PersistsEvents": (11, 2, (2, 0), (), "PersistsEvents", None),
		"Stat": (9, 2, (2, 0), (), "Stat", None),
	}
	_prop_map_put_ = {
	}
	# Default method for this class is 'Item'
	def __call__(self, NameUIDOrIndex=defaultNamedNotOptArg):
		'The first item in a Shapes collection is item 1. Name treated as locale specific.'
		ret = self._oleobj_.InvokeTypes(0, LCID, 2, (9, 0), ((12, 1),),NameUIDOrIndex
			)
		if ret is not None:
			ret = Dispatch(ret, '__call__', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,2,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, '{000D070C-0000-0000-C000-000000000046}')
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(13, 2, (3, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

win32com.client.CLSIDToClass.RegisterCLSID( "{000D070D-0000-0000-C000-000000000046}", IVShapes )
# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.11.5 | packaged by Anaconda, Inc. | (main, Sep 11 2023, 13:26:23) [MSC v.1916 64 bit (AMD64)]
# From type library '{00021A98-0000-0000-C000-000000000046}'
# On Sat Sep 12 14:28:16 2026
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

IVShapes_vtables_dispatch_ = 1
IVShapes_vtables_ = [
	(( 'Application' , 'lpdispRet' , ), 3, (3, (), [ (16393, 10, None, "IID('{000D0700-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'ObjectType' , 'lpi2Ret' , ), 2, (2, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Item' , 'NameUIDOrIndex' , 'lpdispRet' , ), 0, (0, (), [ (12, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Count16' , 'lpi2Ret' , ), 1, (1, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 64 , )),
	(( 'Document' , 'lpdispRet' , ), 4, (4, (), [ (16393, 10, None, "IID('{000D0705-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'ContainingPage' , 'lpdispRet' , ), 5, (5, (), [ (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'ContainingMaster' , 'lpdispRet' , ), 6, (6, (), [ (16393, 10, None, "IID('{000D0707-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'ContainingShape' , 'lpdispRet' , ), 7, (7, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'CenterDrawing' , ), 8, (8, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Stat' , 'lpi2Ret' , ), 9, (9, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'EventList' , 'lpdispRet' , ), 10, (10, (), [ (16393, 10, None, "IID('{000D071B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'PersistsEvents' , 'lpboolRet' , ), 11, (11, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'ItemFromID16' , 'ObjectID' , 'lpdispRet' , ), 12, (12, (), [ (2, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 64 , )),
	(( 'Count' , 'lpi4Ret' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'ItemFromID' , 'ObjectID' , 'lpdispRet' , ), 14, (14, (), [ (3, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'ItemU' , 'NameUIDOrIndex' , 'lpdispRet' , ), 15, (15, (), [ (12, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( '_NewEnum' , 'ppEnum' , ), -4, (-4, (), [ (16397, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 1 , )),
	(( 'ItemFromUniqueID' , 'UniqueID' , 'Shape' , ), 1610743825, (1610743825, (), [ (8, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
]

win32com.client.CLSIDToClass.RegisterCLSID( "{000D070D-0000-0000-C000-000000000046}", IVShapes )
