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
class IVPages(DispatchBaseClass):
	CLSID = IID('{000D070A-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{000D0A05-0000-0000-C000-000000000046}')

	# Result is of type IVPage
	def Add(self):
		ret = self._oleobj_.InvokeTypes(4, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'Add', '{000D0709-0000-0000-C000-000000000046}')
		return ret

	def GetNames(self, localeSpecificNameArray=pythoncom.Missing):
		'Returns locale specific names of pages.'
		return self._ApplyTypes_(9, 1, (24, 0), ((24584, 2),), 'GetNames', None,localeSpecificNameArray
			)

	def GetNamesU(self, localeIndependentNameArray=pythoncom.Missing):
		'Returns locale independent names of pages.'
		return self._ApplyTypes_(11, 1, (24, 0), ((24584, 2),), 'GetNamesU', None,localeIndependentNameArray
			)

	# Result is of type IVPage
	# The method Item is actually a property, but must be used as a method to correctly pass the arguments
	def Item(self, NameOrIndex=defaultNamedNotOptArg):
		'The first item in a Pages collection is item 1. Name treated as locale specific.'
		ret = self._oleobj_.InvokeTypes(0, LCID, 2, (9, 0), ((12, 1),),NameOrIndex
			)
		if ret is not None:
			ret = Dispatch(ret, 'Item', '{000D0709-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVPage
	# The method ItemFromID is actually a property, but must be used as a method to correctly pass the arguments
	def ItemFromID(self, nID=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743821, LCID, 2, (9, 0), ((3, 1),),nID
			)
		if ret is not None:
			ret = Dispatch(ret, 'ItemFromID', '{000D0709-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVPage
	# The method ItemU is actually a property, but must be used as a method to correctly pass the arguments
	def ItemU(self, NameOrIndex=defaultNamedNotOptArg):
		'Like Item() but names treated locale independent.'
		ret = self._oleobj_.InvokeTypes(10, LCID, 2, (9, 0), ((12, 1),),NameOrIndex
			)
		if ret is not None:
			ret = Dispatch(ret, 'ItemU', '{000D0709-0000-0000-C000-000000000046}')
		return ret

	_prop_map_get_ = {
		# Method 'Application' returns object of type 'IVApplication'
		"Application": (3, 2, (9, 0), (), "Application", '{000D0700-0000-0000-C000-000000000046}'),
		"Count": (1, 2, (2, 0), (), "Count", None),
		# Method 'Document' returns object of type 'IVDocument'
		"Document": (5, 2, (9, 0), (), "Document", '{000D0705-0000-0000-C000-000000000046}'),
		# Method 'EventList' returns object of type 'IVEventList'
		"EventList": (7, 2, (9, 0), (), "EventList", '{000D071B-0000-0000-C000-000000000046}'),
		"ObjectType": (2, 2, (2, 0), (), "ObjectType", None),
		"PersistsEvents": (8, 2, (2, 0), (), "PersistsEvents", None),
		"Stat": (6, 2, (2, 0), (), "Stat", None),
	}
	_prop_map_put_ = {
	}
	# Default method for this class is 'Item'
	def __call__(self, NameOrIndex=defaultNamedNotOptArg):
		'The first item in a Pages collection is item 1. Name treated as locale specific.'
		ret = self._oleobj_.InvokeTypes(0, LCID, 2, (9, 0), ((12, 1),),NameOrIndex
			)
		if ret is not None:
			ret = Dispatch(ret, '__call__', '{000D0709-0000-0000-C000-000000000046}')
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
		return win32com.client.util.Iterator(ob, '{000D0709-0000-0000-C000-000000000046}')
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(1, 2, (2, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

win32com.client.CLSIDToClass.RegisterCLSID( "{000D070A-0000-0000-C000-000000000046}", IVPages )
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

IVPages_vtables_dispatch_ = 1
IVPages_vtables_ = [
	(( 'Application' , 'lpdispRet' , ), 3, (3, (), [ (16393, 10, None, "IID('{000D0700-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'ObjectType' , 'lpi2Ret' , ), 2, (2, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Item' , 'NameOrIndex' , 'lpdispRet' , ), 0, (0, (), [ (12, 1, None, None) , 
			 (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Count' , 'lpi2Ret' , ), 1, (1, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Add' , 'lpdispRet' , ), 4, (4, (), [ (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Document' , 'lpdispRet' , ), 5, (5, (), [ (16393, 10, None, "IID('{000D0705-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Stat' , 'lpi2Ret' , ), 6, (6, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'EventList' , 'lpdispRet' , ), 7, (7, (), [ (16393, 10, None, "IID('{000D071B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'PersistsEvents' , 'lpboolRet' , ), 8, (8, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetNames' , 'localeSpecificNameArray' , ), 9, (9, (), [ (24584, 2, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'ItemU' , 'NameOrIndex' , 'lpdispRet' , ), 10, (10, (), [ (12, 1, None, None) , 
			 (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetNamesU' , 'localeIndependentNameArray' , ), 11, (11, (), [ (24584, 2, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( '_NewEnum' , 'ppEnum' , ), -4, (-4, (), [ (16397, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 1 , )),
	(( 'ItemFromID' , 'nID' , 'ppPage' , ), 1610743821, (1610743821, (), [ (3, 1, None, None) , 
			 (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
]

win32com.client.CLSIDToClass.RegisterCLSID( "{000D070A-0000-0000-C000-000000000046}", IVPages )
