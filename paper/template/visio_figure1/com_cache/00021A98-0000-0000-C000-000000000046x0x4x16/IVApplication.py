# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.11.5 | packaged by Anaconda, Inc. | (main, Sep 11 2023, 13:26:23) [MSC v.1916 64 bit (AMD64)]
# From type library '{00021A98-0000-0000-C000-000000000046}'
# On Sat Sep 12 14:27:45 2026
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
class IVApplication(DispatchBaseClass):
	CLSID = IID('{000D0700-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{00021A20-0000-0000-C000-000000000046}')

	def AddUndoUnit(self, pUndoUnit=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(70, LCID, 1, (24, 0), ((13, 1),),pUndoUnit
			)

	def BeginUndoScope(self, bstrUndoScopeName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(68, LCID, 1, (3, 0), ((8, 1),),bstrUndoScopeName
			)

	# Result is of type IVUIObject
	# The method BuiltInToolbars is actually a property, but must be used as a method to correctly pass the arguments
	def BuiltInToolbars(self, fIgnored=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(23, LCID, 2, (9, 0), ((2, 1),),fIgnored
			)
		if ret is not None:
			ret = Dispatch(ret, 'BuiltInToolbars', '{000D0202-0000-0000-C000-000000000046}')
		return ret

	def ClearCustomMenus(self):
		return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), (),)

	def ClearCustomToolbars(self):
		return self._oleobj_.InvokeTypes(31, LCID, 1, (24, 0), (),)

	def ConvertResult(self, StringOrNumber=defaultNamedNotOptArg, UnitsIn=defaultNamedNotOptArg, UnitsOut=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(58, LCID, 1, (5, 0), ((12, 1), (12, 1), (12, 1)),StringOrNumber
			, UnitsIn, UnitsOut)

	# Result is of type IVDataVisualizerSettings
	def CreateDataVisualizerSettings(self):
		ret = self._oleobj_.InvokeTypes(1610743967, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateDataVisualizerSettings', '{000D074A-0000-0000-C000-000000000046}')
		return ret

	def DoCmd(self, CommandID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(43, LCID, 1, (24, 0), ((2, 1),),CommandID
			)

	def EndUndoScope(self, nScopeID=defaultNamedNotOptArg, bCommit=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(69, LCID, 1, (24, 0), ((3, 1), (11, 1)),nScopeID
			, bCommit)

	def EnumDirectories(self, PathsString=defaultNamedNotOptArg, NameArray=pythoncom.Missing):
		return self._ApplyTypes_(60, 1, (24, 0), ((8, 1), (24584, 2)), 'EnumDirectories', None,PathsString
			, NameArray)

	# The method EventInfo is actually a property, but must be used as a method to correctly pass the arguments
	def EventInfo(self, eventSeqNum=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(45, LCID, 2, (8, 0), ((3, 1),),eventSeqNum
			)

	def FormatResult(self, StringOrNumber=defaultNamedNotOptArg, UnitsIn=defaultNamedNotOptArg, UnitsOut=defaultNamedNotOptArg, Format=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(57, LCID, 1, (8, 0), ((12, 1), (12, 1), (12, 1), (8, 1)),StringOrNumber
			, UnitsIn, UnitsOut, Format)

	def FormatResultEx(self, StringOrNumber=defaultNamedNotOptArg, UnitsIn=defaultNamedNotOptArg, UnitsOut=defaultNamedNotOptArg, Format=defaultNamedNotOptArg
			, LangID=0, CalendarID=-1):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1610743948, LCID, 1, (8, 0), ((12, 1), (12, 1), (12, 1), (8, 1), (3, 49), (3, 49)),StringOrNumber
			, UnitsIn, UnitsOut, Format, LangID, CalendarID
			)

	def GetBuiltInStencilFile(self, StencilType=defaultNamedNotOptArg, MeasurementSystem=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1610743961, LCID, 1, (8, 0), ((3, 1), (3, 1)),StencilType
			, MeasurementSystem)

	def GetCustomStencilFile(self, StencilType=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1610743962, LCID, 1, (8, 0), ((3, 1),),StencilType
			)

	def GetPreferredVisioTemplate(self, DataTemplateId=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1610743969, LCID, 1, (8, 0), ((8, 1),),DataTemplateId
			)

	def GetPreviewEnabled(self, GalleryName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743959, LCID, 1, (11, 0), ((8, 1),),GalleryName
			)

	def GetUsageStatistic(self, nWhichStatistic=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610743941, 1, (12, 0), ((3, 1),), 'GetUsageStatistic', None,nWhichStatistic
			)

	def InvokeHelp(self, bstrHelpFileName=defaultNamedNotOptArg, Command=defaultNamedNotOptArg, Data=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743924, LCID, 1, (24, 0), ((8, 1), (3, 1), (3, 1)),bstrHelpFileName
			, Command, Data)

	# The method IsInScope is actually a property, but must be used as a method to correctly pass the arguments
	def IsInScope(self, nCmdID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(74, LCID, 2, (11, 0), ((3, 1),),nCmdID
			)

	def IsNewThemeEnabled(self):
		return self._oleobj_.InvokeTypes(1610743970, LCID, 1, (11, 0), (),)

	def OnComponentEnterState(self, uStateID=defaultNamedNotOptArg, bEnter=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743937, LCID, 1, (24, 0), ((3, 1), (11, 1)),uStateID
			, bEnter)

	def PurgeUndo(self):
		return self._oleobj_.InvokeTypes(62, LCID, 1, (24, 0), (),)

	def QueueMarkerEvent(self, ContextString=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(63, LCID, 1, (3, 0), ((8, 1),),ContextString
			)

	def Quit(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), (),)

	def Redo(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def RegisterRibbonX(self, SourceAddOn=defaultNamedNotOptArg, TargetDocument=defaultNamedNotOptArg, TargetModes=defaultNamedNotOptArg, FriendlyName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743957, LCID, 1, (24, 0), ((13, 1), (9, 1), (3, 1), (8, 1)),SourceAddOn
			, TargetDocument, TargetModes, FriendlyName)

	def RenameCurrentScope(self, bstrScopeName=defaultNamedNotOptArg):
		'Renames the currently open top level undo scope such that bstrScopeName shows up in the do menu item. Raises an exception if not in an open scope.'
		return self._oleobj_.InvokeTypes(1610743923, LCID, 1, (24, 0), ((8, 1),),bstrScopeName
			)

	def SaveWorkspaceAs(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(42, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	def SetCustomMenus(self, MenusObject=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(25, LCID, 1, (24, 0), ((9, 1),),MenusObject
			)

	def SetCustomToolbars(self, ToolbarsObject=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(29, LCID, 1, (24, 0), ((9, 1),),ToolbarsObject
			)

	def SetPreviewEnabled(self, GalleryName=defaultNamedNotOptArg, OnOrOff=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743960, LCID, 1, (24, 0), ((8, 1), (11, 0)),GalleryName
			, OnOrOff)

	def Undo(self):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (24, 0), (),)

	def UnregisterRibbonX(self, SourceAddOn=defaultNamedNotOptArg, TargetDocument=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743958, LCID, 1, (24, 0), ((13, 1), (9, 1)),SourceAddOn
			, TargetDocument)

	_prop_map_get_ = {
		"Active": (48, 2, (2, 0), (), "Active", None),
		# Method 'ActiveDocument' returns object of type 'IVDocument'
		"ActiveDocument": (0, 2, (9, 0), (), "ActiveDocument", '{000D0705-0000-0000-C000-000000000046}'),
		# Method 'ActivePage' returns object of type 'IVPage'
		"ActivePage": (1, 2, (9, 0), (), "ActivePage", '{000D0709-0000-0000-C000-000000000046}'),
		"ActivePrinter": (1610743920, 2, (8, 0), (), "ActivePrinter", None),
		# Method 'ActiveWindow' returns object of type 'IVWindow'
		"ActiveWindow": (2, 2, (9, 0), (), "ActiveWindow", '{000D0710-0000-0000-C000-000000000046}'),
		"AddonPaths": (32, 2, (8, 0), (), "AddonPaths", None),
		# Method 'Addons' returns object of type 'IVAddons'
		"Addons": (41, 2, (9, 0), (), "Addons", '{000D0719-0000-0000-C000-000000000046}'),
		"AlertResponse": (50, 2, (2, 0), (), "AlertResponse", None),
		# Method 'Application' returns object of type 'IVApplication'
		"Application": (3, 2, (9, 0), (), "Application", '{000D0700-0000-0000-C000-000000000046}'),
		"Assistance": (1610743956, 2, (9, 0), (), "Assistance", None),
		"AutoLayout": (66, 2, (11, 0), (), "AutoLayout", None),
		"AutoRecoverInterval": (81, 2, (2, 0), (), "AutoRecoverInterval", None),
		"AvailablePrinters": (1610743922, 2, (8200, 0), (), "AvailablePrinters", None),
		"Build": (1610743926, 2, (3, 0), (), "Build", None),
		# Method 'BuiltInMenus' returns object of type 'IVUIObject'
		"BuiltInMenus": (22, 2, (9, 0), (), "BuiltInMenus", '{000D0202-0000-0000-C000-000000000046}'),
		"COMAddIns": (1610743927, 2, (9, 0), (), "COMAddIns", None),
		"CommandBars": (1610743925, 2, (9, 0), (), "CommandBars", None),
		"CommandLine": (71, 2, (8, 0), (), "CommandLine", None),
		"ConnectorToolDataObject": (1610743946, 2, (13, 0), (), "ConnectorToolDataObject", None),
		"CurrentEdition": (1610743965, 2, (3, 0), (), "CurrentEdition", None),
		"CurrentScope": (73, 2, (3, 0), (), "CurrentScope", None),
		# Method 'CustomMenus' returns object of type 'IVUIObject'
		"CustomMenus": (24, 2, (9, 0), (), "CustomMenus", '{000D0202-0000-0000-C000-000000000046}'),
		"CustomMenusFile": (26, 2, (8, 0), (), "CustomMenusFile", None),
		# Method 'CustomToolbars' returns object of type 'IVUIObject'
		"CustomToolbars": (28, 2, (9, 0), (), "CustomToolbars", '{000D0202-0000-0000-C000-000000000046}'),
		"CustomToolbarsFile": (30, 2, (8, 0), (), "CustomToolbarsFile", None),
		"DataFeaturesEnabled": (1610743954, 2, (11, 0), (), "DataFeaturesEnabled", None),
		"DataVisualizationEnabled": (1610743968, 2, (11, 0), (), "DataVisualizationEnabled", None),
		"DefaultAngleUnits": (1610743932, 2, (12, 0), (), "DefaultAngleUnits", None),
		"DefaultDurationUnits": (1610743934, 2, (12, 0), (), "DefaultDurationUnits", None),
		"DefaultPageUnits": (1610743928, 2, (12, 0), (), "DefaultPageUnits", None),
		"DefaultRectangleDataObject": (1610743953, 2, (13, 0), (), "DefaultRectangleDataObject", None),
		"DefaultTextUnits": (1610743930, 2, (12, 0), (), "DefaultTextUnits", None),
		"DefaultZoomBehavior": (1610743939, 2, (3, 0), (), "DefaultZoomBehavior", None),
		"DeferRecalc": (49, 2, (2, 0), (), "DeferRecalc", None),
		"DeferRelationshipRecalc": (1610743963, 2, (11, 0), (), "DeferRelationshipRecalc", None),
		# Method 'DialogFont' returns object of type 'Font'
		"DialogFont": (1610743942, 2, (9, 0), (), "DialogFont", '{BEF6E003-A874-101A-8BBA-00AA00300CAB}'),
		# Method 'Documents' returns object of type 'IVDocuments'
		"Documents": (4, 2, (9, 0), (), "Documents", '{000D0706-0000-0000-C000-000000000046}'),
		"DrawingPaths": (33, 2, (8, 0), (), "DrawingPaths", None),
		# Method 'EventList' returns object of type 'IVEventList'
		"EventList": (46, 2, (9, 0), (), "EventList", '{000D071B-0000-0000-C000-000000000046}'),
		"EventsEnabled": (56, 2, (2, 0), (), "EventsEnabled", None),
		"FilterPaths": (34, 2, (8, 0), (), "FilterPaths", None),
		"FullBuild": (1610743936, 2, (3, 0), (), "FullBuild", None),
		"HelpPaths": (35, 2, (8, 0), (), "HelpPaths", None),
		"InhibitSelectChange": (1610743918, 2, (11, 0), (), "InhibitSelectChange", None),
		"InstanceHandle": (20, 2, (2, 0), (), "InstanceHandle", None),
		"InstanceHandle32": (21, 2, (3, 0), (), "InstanceHandle32", None),
		"InstanceHandle64": (1610743966, 2, (20, 0), (), "InstanceHandle64", None),
		"IsUndoingOrRedoing": (72, 2, (11, 0), (), "IsUndoingOrRedoing", None),
		"IsVisio16": (17, 2, (2, 0), (), "IsVisio16", None),
		"IsVisio32": (18, 2, (2, 0), (), "IsVisio32", None),
		"Language": (8, 2, (3, 0), (), "Language", None),
		"LanguageHelp": (1610743943, 2, (3, 0), (), "LanguageHelp", None),
		"LanguageSettings": (1610743955, 2, (9, 0), (), "LanguageSettings", None),
		"LiveDynamics": (65, 2, (11, 0), (), "LiveDynamics", None),
		"MsoDebugOptions": (1610743950, 2, (9, 0), (), "MsoDebugOptions", None),
		"MyShapesPath": (1610743951, 2, (8, 0), (), "MyShapesPath", None),
		"Name": (1610743945, 2, (8, 0), (), "Name", None),
		"ObjectType": (5, 2, (2, 0), (), "ObjectType", None),
		"OnDataChangeDelay": (6, 2, (3, 0), (), "OnDataChangeDelay", None),
		"Path": (59, 2, (8, 0), (), "Path", None),
		"PersistsEvents": (47, 2, (2, 0), (), "PersistsEvents", None),
		"ProcessID": (7, 2, (3, 0), (), "ProcessID", None),
		"ProductName": (76, 2, (8, 0), (), "ProductName", None),
		"ProfileName": (44, 2, (8, 0), (), "ProfileName", None),
		"PromptForSummary": (40, 2, (2, 0), (), "PromptForSummary", None),
		"SaveAsWebObject": (1610743949, 2, (9, 0), (), "SaveAsWebObject", None),
		"ScreenUpdating": (11, 2, (2, 0), (), "ScreenUpdating", None),
		# Method 'Settings' returns object of type 'IVApplicationSettings'
		"Settings": (1610743947, 2, (9, 0), (), "Settings", '{000D072D-0000-0000-C000-000000000046}'),
		"ShowChanges": (78, 2, (11, 0), (), "ShowChanges", None),
		"ShowMenus": (53, 2, (2, 0), (), "ShowMenus", None),
		"ShowProgress": (51, 2, (2, 0), (), "ShowProgress", None),
		"ShowStatusBar": (55, 2, (2, 0), (), "ShowStatusBar", None),
		"ShowToolbar": (64, 2, (2, 0), (), "ShowToolbar", None),
		"StartupPaths": (36, 2, (8, 0), (), "StartupPaths", None),
		"Stat": (12, 2, (2, 0), (), "Stat", None),
		"StencilPaths": (37, 2, (8, 0), (), "StencilPaths", None),
		"TemplatePaths": (38, 2, (8, 0), (), "TemplatePaths", None),
		"ToolbarStyle": (54, 2, (2, 0), (), "ToolbarStyle", None),
		"TraceFlags": (61, 2, (3, 0), (), "TraceFlags", None),
		"TypelibMajorVersion": (79, 2, (2, 0), (), "TypelibMajorVersion", None),
		"TypelibMinorVersion": (80, 2, (2, 0), (), "TypelibMinorVersion", None),
		"UndoEnabled": (77, 2, (11, 0), (), "UndoEnabled", None),
		"UserName": (39, 2, (8, 0), (), "UserName", None),
		"VBAEnabled": (1610743938, 2, (11, 0), (), "VBAEnabled", None),
		"Vbe": (52, 2, (9, 0), (), "Vbe", None),
		"Version": (14, 2, (8, 0), (), "Version", None),
		"Visible": (67, 2, (11, 0), (), "Visible", None),
		# Method 'Window' returns object of type 'IVWindow'
		"Window": (1610743944, 2, (9, 0), (), "Window", '{000D0710-0000-0000-C000-000000000046}'),
		"WindowHandle": (15, 2, (2, 0), (), "WindowHandle", None),
		"WindowHandle32": (19, 2, (3, 0), (), "WindowHandle32", None),
		# Method 'Windows' returns object of type 'IVWindows'
		"Windows": (16, 2, (9, 0), (), "Windows", '{000D0711-0000-0000-C000-000000000046}'),
		"old_Addins": (75, 2, (9, 0), (), "old_Addins", None),
	}
	_prop_map_put_ = {
		"ActivePrinter": ((1610743920, LCID, 4, 0),()),
		"AddonPaths": ((32, LCID, 4, 0),()),
		"AlertResponse": ((50, LCID, 4, 0),()),
		"AutoLayout": ((66, LCID, 4, 0),()),
		"AutoRecoverInterval": ((81, LCID, 4, 0),()),
		"CustomMenusFile": ((26, LCID, 4, 0),()),
		"CustomToolbarsFile": ((30, LCID, 4, 0),()),
		"DefaultAngleUnits": ((1610743932, LCID, 4, 0),()),
		"DefaultDurationUnits": ((1610743934, LCID, 4, 0),()),
		"DefaultPageUnits": ((1610743928, LCID, 4, 0),()),
		"DefaultTextUnits": ((1610743930, LCID, 4, 0),()),
		"DefaultZoomBehavior": ((1610743939, LCID, 4, 0),()),
		"DeferRecalc": ((49, LCID, 4, 0),()),
		"DeferRelationshipRecalc": ((1610743963, LCID, 4, 0),()),
		"DrawingPaths": ((33, LCID, 4, 0),()),
		"EventsEnabled": ((56, LCID, 4, 0),()),
		"FilterPaths": ((34, LCID, 4, 0),()),
		"HelpPaths": ((35, LCID, 4, 0),()),
		"InhibitSelectChange": ((1610743918, LCID, 4, 0),()),
		"LiveDynamics": ((65, LCID, 4, 0),()),
		"MyShapesPath": ((1610743951, LCID, 4, 0),()),
		"OnDataChangeDelay": ((6, LCID, 4, 0),()),
		"PromptForSummary": ((40, LCID, 4, 0),()),
		"ScreenUpdating": ((11, LCID, 4, 0),()),
		"ShowChanges": ((78, LCID, 4, 0),()),
		"ShowMenus": ((53, LCID, 4, 0),()),
		"ShowProgress": ((51, LCID, 4, 0),()),
		"ShowStatusBar": ((55, LCID, 4, 0),()),
		"ShowToolbar": ((64, LCID, 4, 0),()),
		"StartupPaths": ((36, LCID, 4, 0),()),
		"StencilPaths": ((37, LCID, 4, 0),()),
		"TemplatePaths": ((38, LCID, 4, 0),()),
		"ToolbarStyle": ((54, LCID, 4, 0),()),
		"TraceFlags": ((61, LCID, 4, 0),()),
		"UndoEnabled": ((77, LCID, 4, 0),()),
		"UserName": ((39, LCID, 4, 0),()),
		"Visible": ((67, LCID, 4, 0),()),
	}
	# Default property for this class is 'ActiveDocument'
	def __call__(self):
		return self._ApplyTypes_(*(0, 2, (9, 0), (), "ActiveDocument", '{000D0705-0000-0000-C000-000000000046}'))
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

win32com.client.CLSIDToClass.RegisterCLSID( "{000D0700-0000-0000-C000-000000000046}", IVApplication )
# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.11.5 | packaged by Anaconda, Inc. | (main, Sep 11 2023, 13:26:23) [MSC v.1916 64 bit (AMD64)]
# From type library '{00021A98-0000-0000-C000-000000000046}'
# On Sat Sep 12 14:27:45 2026
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

IVApplication_vtables_dispatch_ = 1
IVApplication_vtables_ = [
	(( 'ActiveDocument' , 'lpdispRet' , ), 0, (0, (), [ (16393, 10, None, "IID('{000D0705-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'ActivePage' , 'lpdispRet' , ), 1, (1, (), [ (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'ActiveWindow' , 'lpdispRet' , ), 2, (2, (), [ (16393, 10, None, "IID('{000D0710-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Application' , 'lpdispRet' , ), 3, (3, (), [ (16393, 10, None, "IID('{000D0700-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Documents' , 'lpdispRet' , ), 4, (4, (), [ (16393, 10, None, "IID('{000D0706-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'ObjectType' , 'lpi2Ret' , ), 5, (5, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'OnDataChangeDelay' , 'lpi4Ret' , ), 6, (6, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'OnDataChangeDelay' , 'lpi4Ret' , ), 6, (6, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ProcessID' , 'lpi4Ret' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Quit' , ), 9, (9, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Redo' , ), 10, (10, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'ScreenUpdating' , 'lpi2Ret' , ), 11, (11, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'ScreenUpdating' , 'lpi2Ret' , ), 11, (11, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'Stat' , 'lpi2Ret' , ), 12, (12, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'Undo' , ), 13, (13, (), [ ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'Version' , 'lpbstrRet' , ), 14, (14, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'WindowHandle' , 'lpi2Ret' , ), 15, (15, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 64 , )),
	(( 'Windows' , 'lpdispRet' , ), 16, (16, (), [ (16393, 10, None, "IID('{000D0711-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'Language' , 'lpi4Ret' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'IsVisio16' , 'lpi2Ret' , ), 17, (17, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 64 , )),
	(( 'IsVisio32' , 'lpi2Ret' , ), 18, (18, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'WindowHandle32' , 'lpi4Ret' , ), 19, (19, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'InstanceHandle' , 'lpi2Ret' , ), 20, (20, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 64 , )),
	(( 'InstanceHandle32' , 'lpi4Ret' , ), 21, (21, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'BuiltInMenus' , 'lpdispRet' , ), 22, (22, (), [ (16393, 10, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'BuiltInToolbars' , 'fIgnored' , 'lpdispRet' , ), 23, (23, (), [ (2, 1, None, None) , 
			 (16393, 10, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'CustomMenus' , 'lpdispRet' , ), 24, (24, (), [ (16393, 10, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'SetCustomMenus' , 'MenusObject' , ), 25, (25, (), [ (9, 1, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'CustomMenusFile' , 'lpbstrRet' , ), 26, (26, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'CustomMenusFile' , 'lpbstrRet' , ), 26, (26, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'ClearCustomMenus' , ), 27, (27, (), [ ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'CustomToolbars' , 'lpdispRet' , ), 28, (28, (), [ (16393, 10, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'SetCustomToolbars' , 'ToolbarsObject' , ), 29, (29, (), [ (9, 1, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'CustomToolbarsFile' , 'lpbstrRet' , ), 30, (30, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'CustomToolbarsFile' , 'lpbstrRet' , ), 30, (30, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'ClearCustomToolbars' , ), 31, (31, (), [ ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'AddonPaths' , 'lpbstrRet' , ), 32, (32, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'AddonPaths' , 'lpbstrRet' , ), 32, (32, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'DrawingPaths' , 'lpbstrRet' , ), 33, (33, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'DrawingPaths' , 'lpbstrRet' , ), 33, (33, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'FilterPaths' , 'lpbstrRet' , ), 34, (34, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 376 , (3, 0, None, None) , 64 , )),
	(( 'FilterPaths' , 'lpbstrRet' , ), 34, (34, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 384 , (3, 0, None, None) , 64 , )),
	(( 'HelpPaths' , 'lpbstrRet' , ), 35, (35, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'HelpPaths' , 'lpbstrRet' , ), 35, (35, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'StartupPaths' , 'lpbstrRet' , ), 36, (36, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'StartupPaths' , 'lpbstrRet' , ), 36, (36, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'StencilPaths' , 'lpbstrRet' , ), 37, (37, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'StencilPaths' , 'lpbstrRet' , ), 37, (37, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'TemplatePaths' , 'lpbstrRet' , ), 38, (38, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'TemplatePaths' , 'lpbstrRet' , ), 38, (38, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'UserName' , 'lpbstrRet' , ), 39, (39, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'UserName' , 'lpbstrRet' , ), 39, (39, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'PromptForSummary' , 'lpi2Ret' , ), 40, (40, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 472 , (3, 0, None, None) , 0 , )),
	(( 'PromptForSummary' , 'lpi2Ret' , ), 40, (40, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'Addons' , 'lpdispRet' , ), 41, (41, (), [ (16393, 10, None, "IID('{000D0719-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 488 , (3, 0, None, None) , 0 , )),
	(( 'SaveWorkspaceAs' , 'FileName' , ), 42, (42, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 496 , (3, 0, None, None) , 64 , )),
	(( 'DoCmd' , 'CommandID' , ), 43, (43, (), [ (2, 1, None, None) , ], 1 , 1 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( 'ProfileName' , 'lpbstrRet' , ), 44, (44, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 512 , (3, 0, None, None) , 64 , )),
	(( 'EventInfo' , 'eventSeqNum' , 'lpbstrRet' , ), 45, (45, (), [ (3, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( 'EventList' , 'lpdispRet' , ), 46, (46, (), [ (16393, 10, None, "IID('{000D071B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 528 , (3, 0, None, None) , 0 , )),
	(( 'PersistsEvents' , 'lpi2Ret' , ), 47, (47, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 536 , (3, 0, None, None) , 0 , )),
	(( 'Active' , 'lpi2Ret' , ), 48, (48, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 544 , (3, 0, None, None) , 0 , )),
	(( 'DeferRecalc' , 'lpi2Ret' , ), 49, (49, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 552 , (3, 0, None, None) , 0 , )),
	(( 'DeferRecalc' , 'lpi2Ret' , ), 49, (49, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 560 , (3, 0, None, None) , 0 , )),
	(( 'AlertResponse' , 'lpi2Ret' , ), 50, (50, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 568 , (3, 0, None, None) , 0 , )),
	(( 'AlertResponse' , 'lpi2Ret' , ), 50, (50, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'ShowProgress' , 'lpi2Ret' , ), 51, (51, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 584 , (3, 0, None, None) , 0 , )),
	(( 'ShowProgress' , 'lpi2Ret' , ), 51, (51, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 592 , (3, 0, None, None) , 0 , )),
	(( 'Vbe' , 'lpdispRet' , ), 52, (52, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
	(( 'ShowMenus' , 'lpi2Ret' , ), 53, (53, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 608 , (3, 0, None, None) , 64 , )),
	(( 'ShowMenus' , 'lpi2Ret' , ), 53, (53, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 616 , (3, 0, None, None) , 64 , )),
	(( 'ToolbarStyle' , 'lpi2Ret' , ), 54, (54, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 624 , (3, 0, None, None) , 64 , )),
	(( 'ToolbarStyle' , 'lpi2Ret' , ), 54, (54, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 632 , (3, 0, None, None) , 64 , )),
	(( 'ShowStatusBar' , 'lpi2Ret' , ), 55, (55, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 640 , (3, 0, None, None) , 0 , )),
	(( 'ShowStatusBar' , 'lpi2Ret' , ), 55, (55, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 648 , (3, 0, None, None) , 0 , )),
	(( 'EventsEnabled' , 'lpi2Ret' , ), 56, (56, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 656 , (3, 0, None, None) , 0 , )),
	(( 'EventsEnabled' , 'lpi2Ret' , ), 56, (56, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 664 , (3, 0, None, None) , 0 , )),
	(( 'FormatResult' , 'StringOrNumber' , 'UnitsIn' , 'UnitsOut' , 'Format' , 
			 'lpbstrRet' , ), 57, (57, (), [ (12, 1, None, None) , (12, 1, None, None) , (12, 1, None, None) , 
			 (8, 1, None, None) , (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 672 , (3, 0, None, None) , 0 , )),
	(( 'ConvertResult' , 'StringOrNumber' , 'UnitsIn' , 'UnitsOut' , 'lpr8Ret' , 
			 ), 58, (58, (), [ (12, 1, None, None) , (12, 1, None, None) , (12, 1, None, None) , (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 680 , (3, 0, None, None) , 0 , )),
	(( 'Path' , 'lpbstrRet' , ), 59, (59, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 688 , (3, 0, None, None) , 0 , )),
	(( 'EnumDirectories' , 'PathsString' , 'NameArray' , ), 60, (60, (), [ (8, 1, None, None) , 
			 (24584, 2, None, None) , ], 1 , 1 , 4 , 0 , 696 , (3, 0, None, None) , 0 , )),
	(( 'TraceFlags' , 'lpi4Ret' , ), 61, (61, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 704 , (3, 0, None, None) , 0 , )),
	(( 'TraceFlags' , 'lpi4Ret' , ), 61, (61, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 712 , (3, 0, None, None) , 0 , )),
	(( 'PurgeUndo' , ), 62, (62, (), [ ], 1 , 1 , 4 , 0 , 720 , (3, 0, None, None) , 0 , )),
	(( 'QueueMarkerEvent' , 'ContextString' , 'lpi4Ret' , ), 63, (63, (), [ (8, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 728 , (3, 0, None, None) , 0 , )),
	(( 'ShowToolbar' , 'lpi2Ret' , ), 64, (64, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 736 , (3, 0, None, None) , 0 , )),
	(( 'ShowToolbar' , 'lpi2Ret' , ), 64, (64, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 744 , (3, 0, None, None) , 0 , )),
	(( 'LiveDynamics' , 'pbRet' , ), 65, (65, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 752 , (3, 0, None, None) , 0 , )),
	(( 'LiveDynamics' , 'pbRet' , ), 65, (65, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 760 , (3, 0, None, None) , 0 , )),
	(( 'AutoLayout' , 'pbRet' , ), 66, (66, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 768 , (3, 0, None, None) , 0 , )),
	(( 'AutoLayout' , 'pbRet' , ), 66, (66, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 776 , (3, 0, None, None) , 0 , )),
	(( 'Visible' , 'pbVisible' , ), 67, (67, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 784 , (3, 0, None, None) , 0 , )),
	(( 'Visible' , 'pbVisible' , ), 67, (67, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 792 , (3, 0, None, None) , 0 , )),
	(( 'BeginUndoScope' , 'bstrUndoScopeName' , 'pnScopeID' , ), 68, (68, (), [ (8, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 800 , (3, 0, None, None) , 0 , )),
	(( 'EndUndoScope' , 'nScopeID' , 'bCommit' , ), 69, (69, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 808 , (3, 0, None, None) , 0 , )),
	(( 'AddUndoUnit' , 'pUndoUnit' , ), 70, (70, (), [ (13, 1, None, None) , ], 1 , 1 , 4 , 0 , 816 , (3, 0, None, None) , 0 , )),
	(( 'CommandLine' , 'pbstrCmdLine' , ), 71, (71, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 824 , (3, 0, None, None) , 0 , )),
	(( 'IsUndoingOrRedoing' , 'pbInUndoOrRedo' , ), 72, (72, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 832 , (3, 0, None, None) , 0 , )),
	(( 'CurrentScope' , 'pnCmdID' , ), 73, (73, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 840 , (3, 0, None, None) , 0 , )),
	(( 'IsInScope' , 'nCmdID' , 'pbInScope' , ), 74, (74, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 848 , (3, 0, None, None) , 0 , )),
	(( 'old_Addins' , 'lpdispRet' , ), 75, (75, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 856 , (3, 0, None, None) , 64 , )),
	(( 'ProductName' , 'lpbstrRet' , ), 76, (76, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 864 , (3, 0, None, None) , 64 , )),
	(( 'UndoEnabled' , 'pbRet' , ), 77, (77, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 872 , (3, 0, None, None) , 0 , )),
	(( 'UndoEnabled' , 'pbRet' , ), 77, (77, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 880 , (3, 0, None, None) , 0 , )),
	(( 'ShowChanges' , 'pbRet' , ), 78, (78, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 888 , (3, 0, None, None) , 0 , )),
	(( 'ShowChanges' , 'pbRet' , ), 78, (78, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 896 , (3, 0, None, None) , 0 , )),
	(( 'TypelibMajorVersion' , 'lpi2Ret' , ), 79, (79, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 904 , (3, 0, None, None) , 0 , )),
	(( 'TypelibMinorVersion' , 'lpi2Ret' , ), 80, (80, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 912 , (3, 0, None, None) , 0 , )),
	(( 'AutoRecoverInterval' , 'lpi2Ret' , ), 81, (81, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 920 , (3, 0, None, None) , 0 , )),
	(( 'AutoRecoverInterval' , 'lpi2Ret' , ), 81, (81, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 928 , (3, 0, None, None) , 0 , )),
	(( 'InhibitSelectChange' , 'pbRet' , ), 1610743918, (1610743918, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 936 , (3, 0, None, None) , 0 , )),
	(( 'InhibitSelectChange' , 'pbRet' , ), 1610743918, (1610743918, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 944 , (3, 0, None, None) , 0 , )),
	(( 'ActivePrinter' , 'pbstrPrinterName' , ), 1610743920, (1610743920, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 952 , (3, 0, None, None) , 0 , )),
	(( 'ActivePrinter' , 'pbstrPrinterName' , ), 1610743920, (1610743920, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 960 , (3, 0, None, None) , 0 , )),
	(( 'AvailablePrinters' , 'NamesArray' , ), 1610743922, (1610743922, (), [ (24584, 10, None, None) , ], 1 , 2 , 4 , 0 , 968 , (3, 0, None, None) , 0 , )),
	(( 'RenameCurrentScope' , 'bstrScopeName' , ), 1610743923, (1610743923, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 976 , (3, 0, None, None) , 0 , )),
	(( 'InvokeHelp' , 'bstrHelpFileName' , 'Command' , 'Data' , ), 1610743924, (1610743924, (), [ 
			 (8, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 984 , (3, 0, None, None) , 0 , )),
	(( 'CommandBars' , 'lpdispRet' , ), 1610743925, (1610743925, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 992 , (3, 0, None, None) , 0 , )),
	(( 'Build' , 'pnBuild' , ), 1610743926, (1610743926, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1000 , (3, 0, None, None) , 0 , )),
	(( 'COMAddIns' , 'lpdispRet' , ), 1610743927, (1610743927, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 1008 , (3, 0, None, None) , 0 , )),
	(( 'DefaultPageUnits' , 'pUnitsNameOrCode' , ), 1610743928, (1610743928, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 1016 , (3, 0, None, None) , 64 , )),
	(( 'DefaultPageUnits' , 'pUnitsNameOrCode' , ), 1610743928, (1610743928, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 1024 , (3, 0, None, None) , 64 , )),
	(( 'DefaultTextUnits' , 'pUnitsNameOrCode' , ), 1610743930, (1610743930, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 1032 , (3, 0, None, None) , 0 , )),
	(( 'DefaultTextUnits' , 'pUnitsNameOrCode' , ), 1610743930, (1610743930, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 1040 , (3, 0, None, None) , 0 , )),
	(( 'DefaultAngleUnits' , 'pUnitsNameOrCode' , ), 1610743932, (1610743932, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 1048 , (3, 0, None, None) , 0 , )),
	(( 'DefaultAngleUnits' , 'pUnitsNameOrCode' , ), 1610743932, (1610743932, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 1056 , (3, 0, None, None) , 0 , )),
	(( 'DefaultDurationUnits' , 'pUnitsNameOrCode' , ), 1610743934, (1610743934, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 1064 , (3, 0, None, None) , 0 , )),
	(( 'DefaultDurationUnits' , 'pUnitsNameOrCode' , ), 1610743934, (1610743934, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 1072 , (3, 0, None, None) , 0 , )),
	(( 'FullBuild' , 'pnFullBuild' , ), 1610743936, (1610743936, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1080 , (3, 0, None, None) , 0 , )),
	(( 'OnComponentEnterState' , 'uStateID' , 'bEnter' , ), 1610743937, (1610743937, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 1088 , (3, 0, None, None) , 0 , )),
	(( 'VBAEnabled' , 'pbRet' , ), 1610743938, (1610743938, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1096 , (3, 0, None, None) , 0 , )),
	(( 'DefaultZoomBehavior' , 'pnZoomBehavior' , ), 1610743939, (1610743939, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1104 , (3, 0, None, None) , 0 , )),
	(( 'DefaultZoomBehavior' , 'pnZoomBehavior' , ), 1610743939, (1610743939, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1112 , (3, 0, None, None) , 0 , )),
	(( 'GetUsageStatistic' , 'nWhichStatistic' , 'pvStatistic' , ), 1610743941, (1610743941, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 1120 , (3, 0, None, None) , 64 , )),
	(( 'DialogFont' , 'ppFontDisp' , ), 1610743942, (1610743942, (), [ (16393, 10, None, "IID('{BEF6E003-A874-101A-8BBA-00AA00300CAB}')") , ], 1 , 2 , 4 , 0 , 1128 , (3, 0, None, None) , 0 , )),
	(( 'LanguageHelp' , 'lpi4Ret' , ), 1610743943, (1610743943, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1136 , (3, 0, None, None) , 0 , )),
	(( 'Window' , 'lpdispRet' , ), 1610743944, (1610743944, (), [ (16393, 10, None, "IID('{000D0710-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1144 , (3, 0, None, None) , 0 , )),
	(( 'Name' , 'pbstrName' , ), 1610743945, (1610743945, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1152 , (3, 0, None, None) , 0 , )),
	(( 'ConnectorToolDataObject' , 'lpdispRet' , ), 1610743946, (1610743946, (), [ (16397, 10, None, None) , ], 1 , 2 , 4 , 0 , 1160 , (3, 0, None, None) , 0 , )),
	(( 'Settings' , 'lpSettingRet' , ), 1610743947, (1610743947, (), [ (16393, 10, None, "IID('{000D072D-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1168 , (3, 0, None, None) , 0 , )),
	(( 'FormatResultEx' , 'StringOrNumber' , 'UnitsIn' , 'UnitsOut' , 'Format' , 
			 'LangID' , 'CalendarID' , 'lpbstrRet' , ), 1610743948, (1610743948, (), [ (12, 1, None, None) , 
			 (12, 1, None, None) , (12, 1, None, None) , (8, 1, None, None) , (3, 49, '0', None) , (3, 49, '-1', None) , 
			 (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 1176 , (3, 0, None, None) , 0 , )),
	(( 'SaveAsWebObject' , 'lpdispRet' , ), 1610743949, (1610743949, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 1184 , (3, 0, None, None) , 0 , )),
	(( 'MsoDebugOptions' , 'lpdispRet' , ), 1610743950, (1610743950, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 1192 , (3, 0, None, None) , 64 , )),
	(( 'MyShapesPath' , 'lpbstrRet' , ), 1610743951, (1610743951, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1200 , (3, 0, None, None) , 0 , )),
	(( 'MyShapesPath' , 'lpbstrRet' , ), 1610743951, (1610743951, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1208 , (3, 0, None, None) , 0 , )),
	(( 'DefaultRectangleDataObject' , 'lpunkRet' , ), 1610743953, (1610743953, (), [ (16397, 10, None, None) , ], 1 , 2 , 4 , 0 , 1216 , (3, 0, None, None) , 0 , )),
	(( 'DataFeaturesEnabled' , 'pbRet' , ), 1610743954, (1610743954, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1224 , (3, 0, None, None) , 0 , )),
	(( 'LanguageSettings' , 'lpdispRet' , ), 1610743955, (1610743955, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 1232 , (3, 0, None, None) , 0 , )),
	(( 'Assistance' , 'lpdispRet' , ), 1610743956, (1610743956, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 1240 , (3, 0, None, None) , 0 , )),
	(( 'RegisterRibbonX' , 'SourceAddOn' , 'TargetDocument' , 'TargetModes' , 'FriendlyName' , 
			 ), 1610743957, (1610743957, (), [ (13, 1, None, None) , (9, 1, None, "IID('{000D0705-0000-0000-C000-000000000046}')") , (3, 1, None, None) , (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 1248 , (3, 0, None, None) , 0 , )),
	(( 'UnregisterRibbonX' , 'SourceAddOn' , 'TargetDocument' , ), 1610743958, (1610743958, (), [ (13, 1, None, None) , 
			 (9, 1, None, "IID('{000D0705-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1256 , (3, 0, None, None) , 0 , )),
	(( 'GetPreviewEnabled' , 'GalleryName' , 'pbRet' , ), 1610743959, (1610743959, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 1264 , (3, 0, None, None) , 0 , )),
	(( 'SetPreviewEnabled' , 'GalleryName' , 'OnOrOff' , ), 1610743960, (1610743960, (), [ (8, 1, None, None) , 
			 (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 1272 , (3, 0, None, None) , 0 , )),
	(( 'GetBuiltInStencilFile' , 'StencilType' , 'MeasurementSystem' , 'lpbstrRet' , ), 1610743961, (1610743961, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 1280 , (3, 0, None, None) , 0 , )),
	(( 'GetCustomStencilFile' , 'StencilType' , 'lpbstrRet' , ), 1610743962, (1610743962, (), [ (3, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 1288 , (3, 0, None, None) , 0 , )),
	(( 'DeferRelationshipRecalc' , 'lpi2Ret' , ), 1610743963, (1610743963, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1296 , (3, 0, None, None) , 0 , )),
	(( 'DeferRelationshipRecalc' , 'lpi2Ret' , ), 1610743963, (1610743963, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1304 , (3, 0, None, None) , 0 , )),
	(( 'CurrentEdition' , 'pbRet' , ), 1610743965, (1610743965, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1312 , (3, 0, None, None) , 0 , )),
	(( 'InstanceHandle64' , 'lpi8Ret' , ), 1610743966, (1610743966, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 1320 , (3, 0, None, None) , 0 , )),
	(( 'CreateDataVisualizerSettings' , 'ppDVSettings' , ), 1610743967, (1610743967, (), [ (16393, 10, None, "IID('{000D074A-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1328 , (3, 0, None, None) , 0 , )),
	(( 'DataVisualizationEnabled' , 'pbEnabled' , ), 1610743968, (1610743968, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1336 , (3, 0, None, None) , 0 , )),
	(( 'GetPreferredVisioTemplate' , 'DataTemplateId' , 'pTemplatePath' , ), 1610743969, (1610743969, (), [ (8, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 1344 , (3, 0, None, None) , 0 , )),
	(( 'IsNewThemeEnabled' , 'pbRet' , ), 1610743970, (1610743970, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 1352 , (3, 0, None, None) , 0 , )),
]

win32com.client.CLSIDToClass.RegisterCLSID( "{000D0700-0000-0000-C000-000000000046}", IVApplication )
