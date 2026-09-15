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

from win32com.client import CoClassBaseClass
import sys
__import__('win32com.gen_py.00021A98-0000-0000-C000-000000000046x0x4x16.EShape')
EShape = sys.modules['win32com.gen_py.00021A98-0000-0000-C000-000000000046x0x4x16.EShape'].EShape
__import__('win32com.gen_py.00021A98-0000-0000-C000-000000000046x0x4x16.IVShape')
IVShape = sys.modules['win32com.gen_py.00021A98-0000-0000-C000-000000000046x0x4x16.IVShape'].IVShape
class Shape(CoClassBaseClass): # A CoClass
	# An object of a Visio Page or Master, a sub-shape of another Shape, the PageSheet of a Page or Master, or the DocumentSheet of a Document.
	CLSID = IID('{000D0A0A-0000-0000-C000-000000000046}')
	coclass_sources = [
		EShape,
	]
	default_source = EShape
	coclass_interfaces = [
		IVShape,
	]
	default_interface = IVShape

win32com.client.CLSIDToClass.RegisterCLSID( "{000D0A0A-0000-0000-C000-000000000046}", Shape )
