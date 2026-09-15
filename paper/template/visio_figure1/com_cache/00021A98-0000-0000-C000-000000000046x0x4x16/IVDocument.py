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
class IVDocument(DispatchBaseClass):
	CLSID = IID('{000D0705-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{00021A21-0000-0000-C000-000000000046}')

	def AddUndoUnit(self, pUndoUnit=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610744019, LCID, 1, (24, 0), ((13, 1),),pUndoUnit
			)

	def BeginUndoScope(self, bstrUndoScopeName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610744017, LCID, 1, (3, 0), ((8, 1),),bstrUndoScopeName
			)

	def CanCheckIn(self):
		return self._oleobj_.InvokeTypes(1610744009, LCID, 1, (11, 0), (),)

	def CanUndoCheckOut(self):
		return self._oleobj_.InvokeTypes(1610744030, LCID, 1, (11, 0), (),)

	def CheckIn(self, SaveChanges=True, Comments=defaultNamedNotOptArg, MakePublic=False):
		return self._oleobj_.InvokeTypes(1610744010, LCID, 1, (24, 0), ((11, 49), (16396, 17), (11, 49)),SaveChanges
			, Comments, MakePublic)

	def Clean(self, nTargets=defaultNamedOptArg, nActions=defaultNamedOptArg, nAlerts=defaultNamedOptArg, nFixes=defaultNamedOptArg
			, bStopOnError=defaultNamedOptArg, bLogFileName=defaultNamedOptArg, nReserved=defaultNamedOptArg):
		'Detects and repairs various indicated conditions in a document.'
		return self._oleobj_.InvokeTypes(1610743985, LCID, 1, (24, 0), ((12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17)),nTargets
			, nActions, nAlerts, nFixes, bStopOnError, bLogFileName
			, nReserved)

	def ClearCustomMenus(self):
		return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), (),)

	def ClearCustomToolbars(self):
		return self._oleobj_.InvokeTypes(31, LCID, 1, (24, 0), (),)

	def ClearGestureFormatSheet(self):
		return self._oleobj_.InvokeTypes(78, LCID, 1, (24, 0), (),)

	def Close(self):
		return self._oleobj_.InvokeTypes(23, LCID, 1, (24, 0), (),)

	def CopyPreviewPicture(self, pSourceDoc=defaultNamedNotOptArg):
		'Copies the preview picture from pSourceDoc into this one.'
		return self._oleobj_.InvokeTypes(1610743993, LCID, 1, (24, 0), ((9, 1),),pSourceDoc
			)

	def DeleteSolutionXMLElement(self, ElementName=defaultNamedNotOptArg):
		'Deletes the Solution XML element with the given name.'
		return self._oleobj_.InvokeTypes(1610744002, LCID, 1, (24, 0), ((8, 1),),ElementName
			)

	# Result is of type IVMaster
	def Drop(self, ObjectToDrop=defaultNamedNotOptArg, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(9, LCID, 1, (9, 0), ((13, 1), (2, 1), (2, 1)),ObjectToDrop
			, xPos, yPos)
		if ret is not None:
			ret = Dispatch(ret, 'Drop', '{000D0707-0000-0000-C000-000000000046}')
		return ret

	def EndUndoScope(self, nScopeID=defaultNamedNotOptArg, bCommit=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610744018, LCID, 1, (24, 0), ((3, 1), (11, 1)),nScopeID
			, bCommit)

	def ExecuteLine(self, Line=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(58, LCID, 1, (24, 0), ((8, 1),),Line
			)

	def ExportAsFixedFormat(self, FixedFormat=defaultNamedNotOptArg, OutputFileName=defaultNamedNotOptArg, Intent=defaultNamedNotOptArg, PrintRange=defaultNamedNotOptArg
			, FromPage=1, ToPage=-1, ColorAsBlack=False, IncludeBackground=True, IncludeDocumentProperties=True
			, IncludeStructureTags=True, UseISO19005_1=False, FixedFormatExtClass=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610744034, LCID, 1, (24, 0), ((3, 1), (8, 1), (3, 1), (3, 1), (3, 49), (3, 49), (11, 49), (11, 49), (11, 49), (11, 49), (11, 49), (12, 17)),FixedFormat
			, OutputFileName, Intent, PrintRange, FromPage, ToPage
			, ColorAsBlack, IncludeBackground, IncludeDocumentProperties, IncludeStructureTags, UseISO19005_1
			, FixedFormatExtClass)

	def FollowHyperlink(self, Address=defaultNamedNotOptArg, SubAddress=defaultNamedNotOptArg, ExtraInfo=defaultNamedOptArg, Frame=defaultNamedOptArg
			, NewWindow=defaultNamedOptArg, res1=defaultNamedOptArg, res2=defaultNamedOptArg, res3=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(66, LCID, 1, (24, 0), ((8, 1), (8, 1), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17), (12, 17)),Address
			, SubAddress, ExtraInfo, Frame, NewWindow, res1
			, res2, res3)

	def FollowHyperlink45(self, Target=defaultNamedNotOptArg, Location=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(63, LCID, 1, (24, 0), ((8, 1), (8, 1)),Target
			, Location)

	# The method GetBottomMargin is actually a property, but must be used as a method to correctly pass the arguments
	def GetBottomMargin(self, UnitsNameOrCode=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(43, LCID, 2, (5, 0), ((12, 17),),UnitsNameOrCode
			)

	# The method GetFooterMargin is actually a property, but must be used as a method to correctly pass the arguments
	def GetFooterMargin(self, UnitsNameOrCode=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743976, LCID, 2, (5, 0), ((12, 17),),UnitsNameOrCode
			)

	# The method GetHeaderMargin is actually a property, but must be used as a method to correctly pass the arguments
	def GetHeaderMargin(self, UnitsNameOrCode=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743968, LCID, 2, (5, 0), ((12, 17),),UnitsNameOrCode
			)

	def GetIcon(self, ID=defaultNamedNotOptArg, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(38, LCID, 1, (24, 0), ((2, 1), (8, 1)),ID
			, FileName)

	# The method GetLeftMargin is actually a property, but must be used as a method to correctly pass the arguments
	def GetLeftMargin(self, UnitsNameOrCode=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(40, LCID, 2, (5, 0), ((12, 17),),UnitsNameOrCode
			)

	# The method GetProtection is actually a property, but must be used as a method to correctly pass the arguments
	def GetProtection(self, bstrPassword=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743956, LCID, 2, (3, 0), ((12, 17),),bstrPassword
			)

	# The method GetRightMargin is actually a property, but must be used as a method to correctly pass the arguments
	def GetRightMargin(self, UnitsNameOrCode=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(41, LCID, 2, (5, 0), ((12, 17),),UnitsNameOrCode
			)

	def GetThemeNames(self, eType=defaultNamedNotOptArg, NameArray=pythoncom.Missing):
		return self._ApplyTypes_(1610744028, 1, (24, 0), ((3, 1), (24584, 2)), 'GetThemeNames', None,eType
			, NameArray)

	def GetThemeNamesU(self, eType=defaultNamedNotOptArg, NameArray=pythoncom.Missing):
		return self._ApplyTypes_(1610744029, 1, (24, 0), ((3, 1), (24584, 2)), 'GetThemeNamesU', None,eType
			, NameArray)

	# The method GetTopMargin is actually a property, but must be used as a method to correctly pass the arguments
	def GetTopMargin(self, UnitsNameOrCode=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(42, LCID, 2, (5, 0), ((12, 17),),UnitsNameOrCode
			)

	# Result is of type IVWindow
	def OpenStencilWindow(self):
		ret = self._oleobj_.InvokeTypes(56, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'OpenStencilWindow', '{000D0710-0000-0000-C000-000000000046}')
		return ret

	# The method PaperHeight is actually a property, but must be used as a method to correctly pass the arguments
	def PaperHeight(self, UnitsNameOrCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(61, LCID, 2, (5, 0), ((12, 1),),UnitsNameOrCode
			)

	# The method PaperWidth is actually a property, but must be used as a method to correctly pass the arguments
	def PaperWidth(self, UnitsNameOrCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(60, LCID, 2, (5, 0), ((12, 1),),UnitsNameOrCode
			)

	def ParseLine(self, Line=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(57, LCID, 1, (24, 0), ((8, 1),),Line
			)

	def Print(self):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (24, 0), (),)

	def PrintOut(self, PrintRange=defaultNamedNotOptArg, FromPage=1, ToPage=-1, ScaleCurrentViewToPaper=False
			, PrinterName='', PrintToFile=False, OutputFileName='', Copies=1, Collate=False
			, ColorAsBlack=False):
		return self._ApplyTypes_(1610744016, 1, (24, 32), ((3, 1), (3, 49), (3, 49), (11, 49), (8, 49), (11, 49), (8, 49), (3, 49), (11, 49), (11, 49)), 'PrintOut', None,PrintRange
			, FromPage, ToPage, ScaleCurrentViewToPaper, PrinterName, PrintToFile
			, OutputFileName, Copies, Collate, ColorAsBlack)

	def PurgeUndo(self):
		return self._oleobj_.InvokeTypes(1610744020, LCID, 1, (24, 0), (),)

	def RemoveHiddenInformation(self, RemoveHiddenInfoItems=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610744026, LCID, 1, (24, 0), ((3, 1),),RemoveHiddenInfoItems
			)

	def RenameCurrentScope(self, bstrScopeName=defaultNamedNotOptArg):
		'Renames the currently open top level undo scope such that bstrScopeName shows up in the Undo menu item. Raises an exception if not in an open scope.'
		return self._oleobj_.InvokeTypes(1610744023, LCID, 1, (24, 0), ((8, 1),),bstrScopeName
			)

	def Save(self):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (2, 0), (),)

	def SaveAs(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (2, 0), ((8, 1),),FileName
			)

	def SaveAsEx(self, FileName=defaultNamedNotOptArg, SaveFlags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(36, LCID, 1, (24, 0), ((8, 1), (2, 1)),FileName
			, SaveFlags)

	# The method SetBottomMargin is actually a property, but must be used as a method to correctly pass the arguments
	def SetBottomMargin(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(43, LCID, 4, (24, 0), ((12, 17), (5, 1)),UnitsNameOrCode
			, arg1)

	def SetCustomMenus(self, MenusObject=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(25, LCID, 1, (24, 0), ((9, 1),),MenusObject
			)

	def SetCustomToolbars(self, ToolbarsObject=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(29, LCID, 1, (24, 0), ((9, 1),),ToolbarsObject
			)

	# The method SetFooterMargin is actually a property, but must be used as a method to correctly pass the arguments
	def SetFooterMargin(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(1610743976, LCID, 4, (24, 0), ((12, 17), (5, 1)),UnitsNameOrCode
			, arg1)

	# The method SetHeaderMargin is actually a property, but must be used as a method to correctly pass the arguments
	def SetHeaderMargin(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(1610743968, LCID, 4, (24, 0), ((12, 17), (5, 1)),UnitsNameOrCode
			, arg1)

	def SetIcon(self, ID=defaultNamedNotOptArg, Index=defaultNamedNotOptArg, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(39, LCID, 1, (24, 0), ((2, 1), (2, 1), (8, 1)),ID
			, Index, FileName)

	# The method SetLeftMargin is actually a property, but must be used as a method to correctly pass the arguments
	def SetLeftMargin(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(40, LCID, 4, (24, 0), ((12, 17), (5, 1)),UnitsNameOrCode
			, arg1)

	# The method SetPassword is actually a property, but must be used as a method to correctly pass the arguments
	def SetPassword(self, bstrExistingPassword=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'Obsolete as of Visio 2003.'
		return self._oleobj_.InvokeTypes(1610743982, LCID, 4, (24, 0), ((12, 17), (8, 1)),bstrExistingPassword
			, arg1)

	# The method SetProtection is actually a property, but must be used as a method to correctly pass the arguments
	def SetProtection(self, bstrPassword=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(1610743956, LCID, 4, (24, 0), ((12, 17), (3, 1)),bstrPassword
			, arg1)

	# The method SetRightMargin is actually a property, but must be used as a method to correctly pass the arguments
	def SetRightMargin(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(41, LCID, 4, (24, 0), ((12, 17), (5, 1)),UnitsNameOrCode
			, arg1)

	# The method SetSolutionXMLElement is actually a property, but must be used as a method to correctly pass the arguments
	def SetSolutionXMLElement(self, ElementName=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'Data of the Solution XML element with the given name. Putting data to non-existent element creates element.'
		return self._oleobj_.InvokeTypes(1610744000, LCID, 4, (24, 0), ((8, 1), (8, 1)),ElementName
			, arg1)

	# The method SetTopMargin is actually a property, but must be used as a method to correctly pass the arguments
	def SetTopMargin(self, UnitsNameOrCode=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(42, LCID, 4, (24, 0), ((12, 17), (5, 1)),UnitsNameOrCode
			, arg1)

	# The method SolutionXMLElement is actually a property, but must be used as a method to correctly pass the arguments
	def SolutionXMLElement(self, ElementName=defaultNamedNotOptArg):
		'Data of the Solution XML element with the given name. Putting data to non-existent element creates element.'
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1610744000, LCID, 2, (8, 0), ((8, 1),),ElementName
			)

	# The method SolutionXMLElementExists is actually a property, but must be used as a method to correctly pass the arguments
	def SolutionXMLElementExists(self, ElementName=defaultNamedNotOptArg):
		'Returns true if there is a Solution XML element with the given name.'
		return self._oleobj_.InvokeTypes(1610743999, LCID, 2, (11, 0), ((8, 1),),ElementName
			)

	# The method SolutionXMLElementName is actually a property, but must be used as a method to correctly pass the arguments
	def SolutionXMLElementName(self, Index=defaultNamedNotOptArg):
		"Returns the name of the i'th (1-based) Solution XML element."
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1610743998, LCID, 2, (8, 0), ((3, 1),),Index
			)

	def UndoCheckOut(self):
		return self._oleobj_.InvokeTypes(1610744031, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"AlternateNames": (76, 2, (8, 0), (), "AlternateNames", None),
		# Method 'Application' returns object of type 'IVApplication'
		"Application": (1, 2, (9, 0), (), "Application", '{000D0700-0000-0000-C000-000000000046}'),
		"AutoRecover": (79, 2, (11, 0), (), "AutoRecover", None),
		"BottomMargin": (43, 2, (5, 0), ((12, 17),), "BottomMargin", None),
		"BuildNumberCreated": (1610743986, 2, (3, 0), (), "BuildNumberCreated", None),
		"BuildNumberEdited": (1610743987, 2, (3, 0), (), "BuildNumberEdited", None),
		"Category": (69, 2, (8, 0), (), "Category", None),
		"ClassID": (73, 2, (8, 0), (), "ClassID", None),
		"CodeName": (-2147418112, 2, (8, 0), (), "CodeName", None),
		# Method 'Colors' returns object of type 'IVColors'
		"Colors": (33, 2, (9, 0), (), "Colors", '{000D0717-0000-0000-C000-000000000046}'),
		# Method 'Comments' returns object of type 'IVComments'
		"Comments": (1610744046, 2, (9, 0), (), "Comments", '{000D0743-0000-0000-C000-000000000046}'),
		"Company": (68, 2, (8, 0), (), "Company", None),
		"CompatibilityMode": (1610744045, 2, (11, 0), (), "CompatibilityMode", None),
		"Container": (72, 2, (9, 0), (), "Container", None),
		"ContainsWorkspace": (1610743994, 2, (11, 0), (), "ContainsWorkspace", None),
		"ContainsWorkspaceEx": (1610744032, 2, (11, 0), (), "ContainsWorkspaceEx", None),
		"Creator": (17, 2, (8, 0), (), "Creator", None),
		# Method 'CustomMenus' returns object of type 'IVUIObject'
		"CustomMenus": (24, 2, (9, 0), (), "CustomMenus", '{000D0202-0000-0000-C000-000000000046}'),
		"CustomMenusFile": (26, 2, (8, 0), (), "CustomMenusFile", None),
		# Method 'CustomToolbars' returns object of type 'IVUIObject'
		"CustomToolbars": (28, 2, (9, 0), (), "CustomToolbars", '{000D0202-0000-0000-C000-000000000046}'),
		"CustomToolbarsFile": (30, 2, (8, 0), (), "CustomToolbarsFile", None),
		"CustomUI": (1610744037, 2, (8, 0), (), "CustomUI", None),
		# Method 'DataRecordsets' returns object of type 'IVDataRecordsets'
		"DataRecordsets": (1610744027, 2, (9, 0), (), "DataRecordsets", '{000D072E-0000-0000-C000-000000000046}'),
		"DefaultFillStyle": (53, 2, (8, 0), (), "DefaultFillStyle", None),
		"DefaultGuideStyle": (1610743954, 2, (8, 0), (), "DefaultGuideStyle", None),
		"DefaultLineStyle": (52, 2, (8, 0), (), "DefaultLineStyle", None),
		"DefaultSavePath": (1610744035, 2, (8, 0), (), "DefaultSavePath", None),
		"DefaultStyle": (51, 2, (8, 0), (), "DefaultStyle", None),
		"DefaultTextStyle": (54, 2, (8, 0), (), "DefaultTextStyle", None),
		"Description": (19, 2, (8, 0), (), "Description", None),
		"DiagramServicesEnabled": (1610744043, 2, (3, 0), (), "DiagramServicesEnabled", None),
		# Method 'DocumentSheet' returns object of type 'IVShape'
		"DocumentSheet": (71, 2, (9, 0), (), "DocumentSheet", '{000D070C-0000-0000-C000-000000000046}'),
		"DynamicGridEnabled": (1610743952, 2, (11, 0), (), "DynamicGridEnabled", None),
		"EditorCount": (1610744047, 2, (3, 0), (), "EditorCount", None),
		"EmailRoutingData": (1610743995, 2, (8204, 0), (), "EmailRoutingData", None),
		# Method 'EventList' returns object of type 'IVEventList'
		"EventList": (34, 2, (9, 0), (), "EventList", '{000D071B-0000-0000-C000-000000000046}'),
		# Method 'Fonts' returns object of type 'IVFonts'
		"Fonts": (32, 2, (9, 0), (), "Fonts", '{000D0715-0000-0000-C000-000000000046}'),
		"FooterCenter": (1610743972, 2, (8, 0), (), "FooterCenter", None),
		"FooterLeft": (1610743970, 2, (8, 0), (), "FooterLeft", None),
		"FooterMargin": (1610743976, 2, (5, 0), ((12, 17),), "FooterMargin", None),
		"FooterRight": (1610743974, 2, (8, 0), (), "FooterRight", None),
		"FullBuildNumberCreated": (1610744003, 2, (3, 0), (), "FullBuildNumberCreated", None),
		"FullBuildNumberEdited": (1610744004, 2, (3, 0), (), "FullBuildNumberEdited", None),
		"FullName": (21, 2, (8, 0), (), "FullName", None),
		# Method 'GestureFormatSheet' returns object of type 'IVShape'
		"GestureFormatSheet": (77, 2, (9, 0), (), "GestureFormatSheet", '{000D070C-0000-0000-C000-000000000046}'),
		"GlueEnabled": (1610743948, 2, (11, 0), (), "GlueEnabled", None),
		"GlueSettings": (1610743950, 2, (3, 0), (), "GlueSettings", None),
		"HeaderCenter": (1610743964, 2, (8, 0), (), "HeaderCenter", None),
		"HeaderFooterColor": (1610743980, 2, (19, 0), (), "HeaderFooterColor", None),
		# Method 'HeaderFooterFont' returns object of type 'Font'
		"HeaderFooterFont": (1610743978, 2, (9, 0), (), "HeaderFooterFont", '{BEF6E003-A874-101A-8BBA-00AA00300CAB}'),
		"HeaderLeft": (1610743962, 2, (8, 0), (), "HeaderLeft", None),
		"HeaderMargin": (1610743968, 2, (5, 0), ((12, 17),), "HeaderMargin", None),
		"HeaderRight": (1610743966, 2, (8, 0), (), "HeaderRight", None),
		"HyperlinkBase": (70, 2, (8, 0), (), "HyperlinkBase", None),
		"ID": (1610744005, 2, (3, 0), (), "ID", None),
		"InPlace": (5, 2, (2, 0), (), "InPlace", None),
		"Index": (4, 2, (2, 0), (), "Index", None),
		"Keywords": (18, 2, (8, 0), (), "Keywords", None),
		"Language": (1610744012, 2, (3, 0), (), "Language", None),
		"LeftMargin": (40, 2, (5, 0), ((12, 17),), "LeftMargin", None),
		"MacrosEnabled": (1610744006, 2, (11, 0), (), "MacrosEnabled", None),
		"Manager": (67, 2, (8, 0), (), "Manager", None),
		# Method 'MasterShortcuts' returns object of type 'IVMasterShortcuts'
		"MasterShortcuts": (75, 2, (9, 0), (), "MasterShortcuts", '{000D0726-0000-0000-C000-000000000046}'),
		# Method 'Masters' returns object of type 'IVMasters'
		"Masters": (6, 2, (9, 0), (), "Masters", '{000D0708-0000-0000-C000-000000000046}'),
		"Mode": (1610743938, 2, (3, 0), (), "Mode", None),
		"Name": (0, 2, (8, 0), (), "Name", None),
		# Method 'OLEObjects' returns object of type 'IVOLEObjects'
		"OLEObjects": (65, 2, (9, 0), (), "OLEObjects", '{000D071E-0000-0000-C000-000000000046}'),
		"ObjectType": (3, 2, (2, 0), (), "ObjectType", None),
		# Method 'Pages' returns object of type 'IVPages'
		"Pages": (7, 2, (9, 0), (), "Pages", '{000D070A-0000-0000-C000-000000000046}'),
		"PaperSize": (1610743936, 2, (3, 0), (), "PaperSize", None),
		"Path": (20, 2, (8, 0), (), "Path", None),
		"Permission": (1610744048, 2, (9, 0), (), "Permission", None),
		"PersistsEvents": (55, 2, (2, 0), (), "PersistsEvents", None),
		# Method 'PreviewPicture' returns object of type 'Picture'
		"PreviewPicture": (1610743983, 2, (9, 0), (), "PreviewPicture", '{7BF80981-BF32-101A-8BBB-00AA00300CAB}'),
		"PrintCenteredH": (1610743930, 2, (11, 0), (), "PrintCenteredH", None),
		"PrintCenteredV": (1610743932, 2, (11, 0), (), "PrintCenteredV", None),
		"PrintCopies": (1610743960, 2, (3, 0), (), "PrintCopies", None),
		"PrintFitOnPages": (1610743934, 2, (11, 0), (), "PrintFitOnPages", None),
		"PrintLandscape": (1610743928, 2, (11, 0), (), "PrintLandscape", None),
		"PrintPagesAcross": (49, 2, (2, 0), (), "PrintPagesAcross", None),
		"PrintPagesDown": (50, 2, (2, 0), (), "PrintPagesDown", None),
		"PrintScale": (47, 2, (5, 0), (), "PrintScale", None),
		"Printer": (1610743958, 2, (8, 0), (), "Printer", None),
		"ProgID": (74, 2, (8, 0), (), "ProgID", None),
		"Protection": (1610743956, 2, (3, 0), ((12, 17),), "Protection", None),
		"ReadOnly": (11, 2, (2, 0), (), "ReadOnly", None),
		"RemovePersonalInformation": (1610744014, 2, (11, 0), (), "RemovePersonalInformation", None),
		"RightMargin": (41, 2, (5, 0), ((12, 17),), "RightMargin", None),
		"SavePreviewMode": (1610743926, 2, (3, 0), (), "SavePreviewMode", None),
		"Saved": (1610743922, 2, (11, 0), (), "Saved", None),
		# Method 'ServerPublishOptions' returns object of type 'IVServerPublishOptions'
		"ServerPublishOptions": (1610744041, 2, (9, 0), (), "ServerPublishOptions", '{000D0739-0000-0000-C000-000000000046}'),
		"SharedWorkspace": (1610744024, 2, (9, 0), (), "SharedWorkspace", None),
		"SnapAngles": (1610743946, 2, (8197, 0), (), "SnapAngles", None),
		"SnapEnabled": (1610743940, 2, (11, 0), (), "SnapEnabled", None),
		"SnapExtensions": (1610743944, 2, (3, 0), (), "SnapExtensions", None),
		"SnapSettings": (1610743942, 2, (3, 0), (), "SnapSettings", None),
		"SolutionXMLElementCount": (1610743997, 2, (3, 0), (), "SolutionXMLElementCount", None),
		"Stat": (2, 2, (2, 0), (), "Stat", None),
		# Method 'Styles' returns object of type 'IVStyles'
		"Styles": (8, 2, (9, 0), (), "Styles", '{000D070F-0000-0000-C000-000000000046}'),
		"Subject": (16, 2, (8, 0), (), "Subject", None),
		"Sync": (1610744025, 2, (9, 0), (), "Sync", None),
		"Template": (35, 2, (8, 0), (), "Template", None),
		"Time": (1610743989, 2, (7, 0), (), "Time", None),
		"TimeCreated": (1610743988, 2, (7, 0), (), "TimeCreated", None),
		"TimeEdited": (1610743990, 2, (7, 0), (), "TimeEdited", None),
		"TimePrinted": (1610743991, 2, (7, 0), (), "TimePrinted", None),
		"TimeSaved": (1610743992, 2, (7, 0), (), "TimeSaved", None),
		"Title": (15, 2, (8, 0), (), "Title", None),
		"TopMargin": (42, 2, (5, 0), ((12, 17),), "TopMargin", None),
		"Type": (1610744011, 2, (3, 0), (), "Type", None),
		"UndoEnabled": (1610744021, 2, (11, 0), (), "UndoEnabled", None),
		"UserCustomUI": (1610744039, 2, (8, 0), (), "UserCustomUI", None),
		"VBProject": (59, 2, (9, 0), (), "VBProject", None),
		"VBProjectData": (1610743996, 2, (8209, 0), (), "VBProjectData", None),
		# Method 'Validation' returns object of type 'IVValidation'
		"Validation": (1610744042, 2, (9, 0), (), "Validation", '{000D073A-0000-0000-C000-000000000046}'),
		"Version": (1610743924, 2, (3, 0), (), "Version", None),
		"ZoomBehavior": (1610744007, 2, (3, 0), (), "ZoomBehavior", None),
		"old_Mode": (64, 2, (2, 0), (), "old_Mode", None),
		"old_PaperSize": (62, 2, (2, 0), (), "old_PaperSize", None),
		"old_PrintCenteredH": (45, 2, (2, 0), (), "old_PrintCenteredH", None),
		"old_PrintCenteredV": (46, 2, (2, 0), (), "old_PrintCenteredV", None),
		"old_PrintFitOnPages": (48, 2, (2, 0), (), "old_PrintFitOnPages", None),
		"old_PrintLandscape": (44, 2, (2, 0), (), "old_PrintLandscape", None),
		"old_SavePreviewMode": (37, 2, (2, 0), (), "old_SavePreviewMode", None),
		"old_Saved": (10, 2, (2, 0), (), "old_Saved", None),
		"old_Version": (14, 2, (3, 0), (), "old_Version", None),
	}
	_prop_map_put_ = {
		"AlternateNames": ((76, LCID, 4, 0),()),
		"AutoRecover": ((79, LCID, 4, 0),()),
		"BottomMargin": ((43, LCID, 4, 0),()),
		"Category": ((69, LCID, 4, 0),()),
		"Company": ((68, LCID, 4, 0),()),
		"ContainsWorkspaceEx": ((1610744032, LCID, 4, 0),()),
		"Creator": ((17, LCID, 4, 0),()),
		"CustomMenusFile": ((26, LCID, 4, 0),()),
		"CustomToolbarsFile": ((30, LCID, 4, 0),()),
		"CustomUI": ((1610744037, LCID, 4, 0),()),
		"DefaultFillStyle": ((53, LCID, 4, 0),()),
		"DefaultGuideStyle": ((1610743954, LCID, 4, 0),()),
		"DefaultLineStyle": ((52, LCID, 4, 0),()),
		"DefaultSavePath": ((1610744035, LCID, 4, 0),()),
		"DefaultStyle": ((51, LCID, 4, 0),()),
		"DefaultTextStyle": ((54, LCID, 4, 0),()),
		"Description": ((19, LCID, 4, 0),()),
		"DiagramServicesEnabled": ((1610744043, LCID, 4, 0),()),
		"DynamicGridEnabled": ((1610743952, LCID, 4, 0),()),
		"FooterCenter": ((1610743972, LCID, 4, 0),()),
		"FooterLeft": ((1610743970, LCID, 4, 0),()),
		"FooterMargin": ((1610743976, LCID, 4, 0),()),
		"FooterRight": ((1610743974, LCID, 4, 0),()),
		"GlueEnabled": ((1610743948, LCID, 4, 0),()),
		"GlueSettings": ((1610743950, LCID, 4, 0),()),
		"HeaderCenter": ((1610743964, LCID, 4, 0),()),
		"HeaderFooterColor": ((1610743980, LCID, 4, 0),()),
		"HeaderFooterFont": ((1610743978, LCID, 8, 0),()),
		"HeaderLeft": ((1610743962, LCID, 4, 0),()),
		"HeaderMargin": ((1610743968, LCID, 4, 0),()),
		"HeaderRight": ((1610743966, LCID, 4, 0),()),
		"HyperlinkBase": ((70, LCID, 4, 0),()),
		"Keywords": ((18, LCID, 4, 0),()),
		"Language": ((1610744012, LCID, 4, 0),()),
		"LeftMargin": ((40, LCID, 4, 0),()),
		"Manager": ((67, LCID, 4, 0),()),
		"Mode": ((1610743938, LCID, 4, 0),()),
		"PaperSize": ((1610743936, LCID, 4, 0),()),
		"Password": ((1610743982, LCID, 4, 0),()),
		"PreviewPicture": ((1610743983, LCID, 8, 0),()),
		"PrintCenteredH": ((1610743930, LCID, 4, 0),()),
		"PrintCenteredV": ((1610743932, LCID, 4, 0),()),
		"PrintCopies": ((1610743960, LCID, 4, 0),()),
		"PrintFitOnPages": ((1610743934, LCID, 4, 0),()),
		"PrintLandscape": ((1610743928, LCID, 4, 0),()),
		"PrintPagesAcross": ((49, LCID, 4, 0),()),
		"PrintPagesDown": ((50, LCID, 4, 0),()),
		"PrintScale": ((47, LCID, 4, 0),()),
		"Printer": ((1610743958, LCID, 4, 0),()),
		"Protection": ((1610743956, LCID, 4, 0),()),
		"RemovePersonalInformation": ((1610744014, LCID, 4, 0),()),
		"RightMargin": ((41, LCID, 4, 0),()),
		"SavePreviewMode": ((1610743926, LCID, 4, 0),()),
		"Saved": ((1610743922, LCID, 4, 0),()),
		"SnapAngles": ((1610743946, LCID, 4, 0),()),
		"SnapEnabled": ((1610743940, LCID, 4, 0),()),
		"SnapExtensions": ((1610743944, LCID, 4, 0),()),
		"SnapSettings": ((1610743942, LCID, 4, 0),()),
		"Subject": ((16, LCID, 4, 0),()),
		"Title": ((15, LCID, 4, 0),()),
		"TopMargin": ((42, LCID, 4, 0),()),
		"UndoEnabled": ((1610744021, LCID, 4, 0),()),
		"UserCustomUI": ((1610744039, LCID, 4, 0),()),
		"Version": ((1610743924, LCID, 4, 0),()),
		"ZoomBehavior": ((1610744007, LCID, 4, 0),()),
		"old_Mode": ((64, LCID, 4, 0),()),
		"old_PaperSize": ((62, LCID, 4, 0),()),
		"old_PrintCenteredH": ((45, LCID, 4, 0),()),
		"old_PrintCenteredV": ((46, LCID, 4, 0),()),
		"old_PrintFitOnPages": ((48, LCID, 4, 0),()),
		"old_PrintLandscape": ((44, LCID, 4, 0),()),
		"old_SavePreviewMode": ((37, LCID, 4, 0),()),
		"old_Saved": ((10, LCID, 4, 0),()),
		"old_Version": ((14, LCID, 4, 0),()),
	}
	# Default property for this class is 'Name'
	def __call__(self):
		return self._ApplyTypes_(*(0, 2, (8, 0), (), "Name", None))
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

win32com.client.CLSIDToClass.RegisterCLSID( "{000D0705-0000-0000-C000-000000000046}", IVDocument )
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

IVDocument_vtables_dispatch_ = 1
IVDocument_vtables_ = [
	(( 'Application' , 'lpdispRet' , ), 1, (1, (), [ (16393, 10, None, "IID('{000D0700-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Stat' , 'lpi2Ret' , ), 2, (2, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'ObjectType' , 'lpi2Ret' , ), 3, (3, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'InPlace' , 'lpi2Ret' , ), 5, (5, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Masters' , 'lpdispRet' , ), 6, (6, (), [ (16393, 10, None, "IID('{000D0708-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Pages' , 'lpdispRet' , ), 7, (7, (), [ (16393, 10, None, "IID('{000D070A-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Styles' , 'lpdispRet' , ), 8, (8, (), [ (16393, 10, None, "IID('{000D070F-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'Name' , 'lpbstrRet' , ), 0, (0, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Path' , 'lpbstrRet' , ), 20, (20, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'FullName' , 'lpbstrRet' , ), 21, (21, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Drop' , 'ObjectToDrop' , 'xPos' , 'yPos' , 'lpdispRet' , 
			 ), 9, (9, (), [ (13, 1, None, None) , (2, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D0707-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Index' , 'lpi2Ret' , ), 4, (4, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'old_Saved' , 'lpi2Ret' , ), 10, (10, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 64 , )),
	(( 'old_Saved' , 'lpi2Ret' , ), 10, (10, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 64 , )),
	(( 'ReadOnly' , 'lpi2Ret' , ), 11, (11, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'Save' , 'lpi2Ret' , ), 12, (12, (), [ (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'SaveAs' , 'FileName' , 'lpi2Ret' , ), 13, (13, (), [ (8, 1, None, None) , 
			 (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'old_Version' , 'lpi4Ret' , ), 14, (14, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 64 , )),
	(( 'old_Version' , 'lpi4Ret' , ), 14, (14, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 64 , )),
	(( 'Title' , 'lpbstrRet' , ), 15, (15, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'lpbstrRet' , ), 15, (15, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'Subject' , 'lpbstrRet' , ), 16, (16, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'Subject' , 'lpbstrRet' , ), 16, (16, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'Creator' , 'lpbstrRet' , ), 17, (17, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'Creator' , 'lpbstrRet' , ), 17, (17, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'Keywords' , 'lpbstrRet' , ), 18, (18, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'Keywords' , 'lpbstrRet' , ), 18, (18, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'Description' , 'lpbstrRet' , ), 19, (19, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'Description' , 'lpbstrRet' , ), 19, (19, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'Print' , ), 22, (22, (), [ ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'Close' , ), 23, (23, (), [ ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'CustomMenus' , 'lpdispRet' , ), 24, (24, (), [ (16393, 10, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'SetCustomMenus' , 'MenusObject' , ), 25, (25, (), [ (9, 1, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'CustomMenusFile' , 'lpbstrRet' , ), 26, (26, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'CustomMenusFile' , 'lpbstrRet' , ), 26, (26, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'ClearCustomMenus' , ), 27, (27, (), [ ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'CustomToolbars' , 'lpdispRet' , ), 28, (28, (), [ (16393, 10, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'SetCustomToolbars' , 'ToolbarsObject' , ), 29, (29, (), [ (9, 1, None, "IID('{000D0202-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'CustomToolbarsFile' , 'lpbstrRet' , ), 30, (30, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'CustomToolbarsFile' , 'lpbstrRet' , ), 30, (30, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'ClearCustomToolbars' , ), 31, (31, (), [ ], 1 , 1 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'Fonts' , 'lpdispRet' , ), 32, (32, (), [ (16393, 10, None, "IID('{000D0715-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'Colors' , 'lpdispRet' , ), 33, (33, (), [ (16393, 10, None, "IID('{000D0717-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'EventList' , 'lpdispRet' , ), 34, (34, (), [ (16393, 10, None, "IID('{000D071B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'Template' , 'lpbstrRet' , ), 35, (35, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'SaveAsEx' , 'FileName' , 'SaveFlags' , ), 36, (36, (), [ (8, 1, None, None) , 
			 (2, 1, None, None) , ], 1 , 1 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'old_SavePreviewMode' , 'lpi2Ret' , ), 37, (37, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 424 , (3, 0, None, None) , 64 , )),
	(( 'old_SavePreviewMode' , 'lpi2Ret' , ), 37, (37, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 432 , (3, 0, None, None) , 64 , )),
	(( 'GetIcon' , 'ID' , 'FileName' , ), 38, (38, (), [ (2, 1, None, None) , 
			 (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 440 , (3, 0, None, None) , 64 , )),
	(( 'SetIcon' , 'ID' , 'Index' , 'FileName' , ), 39, (39, (), [ 
			 (2, 1, None, None) , (2, 1, None, None) , (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 448 , (3, 0, None, None) , 64 , )),
	(( 'LeftMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 40, (40, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 456 , (3, 0, None, None) , 0 , )),
	(( 'LeftMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 40, (40, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 456 , (3, 0, None, None) , 0 , )),
	(( 'LeftMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 40, (40, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'LeftMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 40, (40, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'RightMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 41, (41, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 472 , (3, 0, None, None) , 0 , )),
	(( 'RightMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 41, (41, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 472 , (3, 0, None, None) , 0 , )),
	(( 'RightMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 41, (41, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'RightMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 41, (41, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'TopMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 42, (42, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 488 , (3, 0, None, None) , 0 , )),
	(( 'TopMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 42, (42, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 488 , (3, 0, None, None) , 0 , )),
	(( 'TopMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 42, (42, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'TopMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 42, (42, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'BottomMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 43, (43, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 504 , (3, 0, None, None) , 0 , )),
	(( 'BottomMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 43, (43, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 504 , (3, 0, None, None) , 0 , )),
	(( 'BottomMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 43, (43, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'BottomMargin' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 43, (43, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'old_PrintLandscape' , 'lpi2Ret' , ), 44, (44, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 520 , (3, 0, None, None) , 64 , )),
	(( 'old_PrintLandscape' , 'lpi2Ret' , ), 44, (44, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 528 , (3, 0, None, None) , 64 , )),
	(( 'old_PrintCenteredH' , 'lpi2Ret' , ), 45, (45, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 536 , (3, 0, None, None) , 64 , )),
	(( 'old_PrintCenteredH' , 'lpi2Ret' , ), 45, (45, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 544 , (3, 0, None, None) , 64 , )),
	(( 'old_PrintCenteredV' , 'lpi2Ret' , ), 46, (46, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 552 , (3, 0, None, None) , 64 , )),
	(( 'old_PrintCenteredV' , 'lpi2Ret' , ), 46, (46, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 560 , (3, 0, None, None) , 64 , )),
	(( 'PrintScale' , 'lpr8Ret' , ), 47, (47, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 568 , (3, 0, None, None) , 0 , )),
	(( 'PrintScale' , 'lpr8Ret' , ), 47, (47, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'old_PrintFitOnPages' , 'lpi2Ret' , ), 48, (48, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 584 , (3, 0, None, None) , 64 , )),
	(( 'old_PrintFitOnPages' , 'lpi2Ret' , ), 48, (48, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 592 , (3, 0, None, None) , 64 , )),
	(( 'PrintPagesAcross' , 'lpi2Ret' , ), 49, (49, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
	(( 'PrintPagesAcross' , 'lpi2Ret' , ), 49, (49, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 608 , (3, 0, None, None) , 0 , )),
	(( 'PrintPagesDown' , 'lpi2Ret' , ), 50, (50, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 616 , (3, 0, None, None) , 0 , )),
	(( 'PrintPagesDown' , 'lpi2Ret' , ), 50, (50, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 624 , (3, 0, None, None) , 0 , )),
	(( 'DefaultStyle' , 'lpLocaleSpecificName' , ), 51, (51, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 632 , (3, 0, None, None) , 0 , )),
	(( 'DefaultStyle' , 'lpLocaleSpecificName' , ), 51, (51, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 640 , (3, 0, None, None) , 0 , )),
	(( 'DefaultLineStyle' , 'lpLocaleSpecificName' , ), 52, (52, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 648 , (3, 0, None, None) , 0 , )),
	(( 'DefaultLineStyle' , 'lpLocaleSpecificName' , ), 52, (52, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 656 , (3, 0, None, None) , 0 , )),
	(( 'DefaultFillStyle' , 'lpLocaleSpecificName' , ), 53, (53, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 664 , (3, 0, None, None) , 0 , )),
	(( 'DefaultFillStyle' , 'lpLocaleSpecificName' , ), 53, (53, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 672 , (3, 0, None, None) , 0 , )),
	(( 'DefaultTextStyle' , 'lpLocaleSpecificName' , ), 54, (54, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 680 , (3, 0, None, None) , 0 , )),
	(( 'DefaultTextStyle' , 'lpLocaleSpecificName' , ), 54, (54, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 688 , (3, 0, None, None) , 0 , )),
	(( 'PersistsEvents' , 'lpboolRet' , ), 55, (55, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 696 , (3, 0, None, None) , 0 , )),
	(( 'OpenStencilWindow' , 'lpdispRet' , ), 56, (56, (), [ (16393, 10, None, "IID('{000D0710-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 704 , (3, 0, None, None) , 0 , )),
	(( 'ParseLine' , 'Line' , ), 57, (57, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 712 , (3, 0, None, None) , 0 , )),
	(( 'ExecuteLine' , 'Line' , ), 58, (58, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 720 , (3, 0, None, None) , 0 , )),
	(( 'VBProject' , 'lpdispRet' , ), 59, (59, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 728 , (3, 0, None, None) , 0 , )),
	(( 'PaperWidth' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 60, (60, (), [ (12, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 736 , (3, 0, None, None) , 0 , )),
	(( 'PaperHeight' , 'UnitsNameOrCode' , 'lpr8Ret' , ), 61, (61, (), [ (12, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 744 , (3, 0, None, None) , 0 , )),
	(( 'old_PaperSize' , 'lpi2Ret' , ), 62, (62, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 752 , (3, 0, None, None) , 64 , )),
	(( 'old_PaperSize' , 'lpi2Ret' , ), 62, (62, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 760 , (3, 0, None, None) , 64 , )),
	(( 'FollowHyperlink45' , 'Target' , 'Location' , ), 63, (63, (), [ (8, 1, None, None) , 
			 (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 768 , (3, 0, None, None) , 64 , )),
	(( 'CodeName' , 'lpbstrRet' , ), -2147418112, (-2147418112, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 776 , (3, 0, None, None) , 64 , )),
	(( 'old_Mode' , 'lpi2Ret' , ), 64, (64, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 784 , (3, 0, None, None) , 64 , )),
	(( 'old_Mode' , 'lpi2Ret' , ), 64, (64, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 792 , (3, 0, None, None) , 64 , )),
	(( 'OLEObjects' , 'lpdispRet' , ), 65, (65, (), [ (16393, 10, None, "IID('{000D071E-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 800 , (3, 0, None, None) , 0 , )),
	(( 'FollowHyperlink' , 'Address' , 'SubAddress' , 'ExtraInfo' , 'Frame' , 
			 'NewWindow' , 'res1' , 'res2' , 'res3' , ), 66, (66, (), [ 
			 (8, 1, None, None) , (8, 1, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , 
			 (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , ], 1 , 1 , 4 , 6 , 808 , (3, 0, None, None) , 0 , )),
	(( 'Manager' , 'lpbstrRet' , ), 67, (67, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 816 , (3, 0, None, None) , 0 , )),
	(( 'Manager' , 'lpbstrRet' , ), 67, (67, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 824 , (3, 0, None, None) , 0 , )),
	(( 'Company' , 'lpbstrRet' , ), 68, (68, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 832 , (3, 0, None, None) , 0 , )),
	(( 'Company' , 'lpbstrRet' , ), 68, (68, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 840 , (3, 0, None, None) , 0 , )),
	(( 'Category' , 'lpbstrRet' , ), 69, (69, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 848 , (3, 0, None, None) , 0 , )),
	(( 'Category' , 'lpbstrRet' , ), 69, (69, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 856 , (3, 0, None, None) , 0 , )),
	(( 'HyperlinkBase' , 'lpbstrRet' , ), 70, (70, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 864 , (3, 0, None, None) , 0 , )),
	(( 'HyperlinkBase' , 'lpbstrRet' , ), 70, (70, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 872 , (3, 0, None, None) , 0 , )),
	(( 'DocumentSheet' , 'lpdispRet' , ), 71, (71, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 880 , (3, 0, None, None) , 0 , )),
	(( 'Container' , 'lpdispRet' , ), 72, (72, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 888 , (3, 0, None, None) , 0 , )),
	(( 'ClassID' , 'lpbstrRet' , ), 73, (73, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 896 , (3, 0, None, None) , 0 , )),
	(( 'ProgID' , 'lpbstrRet' , ), 74, (74, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 904 , (3, 0, None, None) , 0 , )),
	(( 'MasterShortcuts' , 'lpdispRet' , ), 75, (75, (), [ (16393, 10, None, "IID('{000D0726-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 912 , (3, 0, None, None) , 0 , )),
	(( 'AlternateNames' , 'lpbstrRet' , ), 76, (76, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 920 , (3, 0, None, None) , 0 , )),
	(( 'AlternateNames' , 'lpbstrRet' , ), 76, (76, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 928 , (3, 0, None, None) , 0 , )),
	(( 'GestureFormatSheet' , 'lpdispRet' , ), 77, (77, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 936 , (3, 0, None, None) , 0 , )),
	(( 'ClearGestureFormatSheet' , ), 78, (78, (), [ ], 1 , 1 , 4 , 0 , 944 , (3, 0, None, None) , 0 , )),
	(( 'AutoRecover' , 'pbRet' , ), 79, (79, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 952 , (3, 0, None, None) , 0 , )),
	(( 'AutoRecover' , 'pbRet' , ), 79, (79, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 960 , (3, 0, None, None) , 0 , )),
	(( 'Saved' , 'pbRet' , ), 1610743922, (1610743922, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 968 , (3, 0, None, None) , 0 , )),
	(( 'Saved' , 'pbRet' , ), 1610743922, (1610743922, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 976 , (3, 0, None, None) , 0 , )),
	(( 'Version' , 'lpi4Ret' , ), 1610743924, (1610743924, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 984 , (3, 0, None, None) , 0 , )),
	(( 'Version' , 'lpi4Ret' , ), 1610743924, (1610743924, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 992 , (3, 0, None, None) , 0 , )),
	(( 'SavePreviewMode' , 'lpi4Ret' , ), 1610743926, (1610743926, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1000 , (3, 0, None, None) , 0 , )),
	(( 'SavePreviewMode' , 'lpi4Ret' , ), 1610743926, (1610743926, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1008 , (3, 0, None, None) , 0 , )),
	(( 'PrintLandscape' , 'pbRet' , ), 1610743928, (1610743928, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1016 , (3, 0, None, None) , 0 , )),
	(( 'PrintLandscape' , 'pbRet' , ), 1610743928, (1610743928, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1024 , (3, 0, None, None) , 0 , )),
	(( 'PrintCenteredH' , 'pbRet' , ), 1610743930, (1610743930, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1032 , (3, 0, None, None) , 0 , )),
	(( 'PrintCenteredH' , 'pbRet' , ), 1610743930, (1610743930, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1040 , (3, 0, None, None) , 0 , )),
	(( 'PrintCenteredV' , 'pbRet' , ), 1610743932, (1610743932, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1048 , (3, 0, None, None) , 0 , )),
	(( 'PrintCenteredV' , 'pbRet' , ), 1610743932, (1610743932, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1056 , (3, 0, None, None) , 0 , )),
	(( 'PrintFitOnPages' , 'pbRet' , ), 1610743934, (1610743934, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1064 , (3, 0, None, None) , 0 , )),
	(( 'PrintFitOnPages' , 'pbRet' , ), 1610743934, (1610743934, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1072 , (3, 0, None, None) , 0 , )),
	(( 'PaperSize' , 'lpi4Ret' , ), 1610743936, (1610743936, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1080 , (3, 0, None, None) , 0 , )),
	(( 'PaperSize' , 'lpi4Ret' , ), 1610743936, (1610743936, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1088 , (3, 0, None, None) , 0 , )),
	(( 'Mode' , 'lpi4Ret' , ), 1610743938, (1610743938, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1096 , (3, 0, None, None) , 0 , )),
	(( 'Mode' , 'lpi4Ret' , ), 1610743938, (1610743938, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1104 , (3, 0, None, None) , 0 , )),
	(( 'SnapEnabled' , 'pbRet' , ), 1610743940, (1610743940, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1112 , (3, 0, None, None) , 0 , )),
	(( 'SnapEnabled' , 'pbRet' , ), 1610743940, (1610743940, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1120 , (3, 0, None, None) , 0 , )),
	(( 'SnapSettings' , 'pnRet' , ), 1610743942, (1610743942, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1128 , (3, 0, None, None) , 0 , )),
	(( 'SnapSettings' , 'pnRet' , ), 1610743942, (1610743942, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1136 , (3, 0, None, None) , 0 , )),
	(( 'SnapExtensions' , 'pnRet' , ), 1610743944, (1610743944, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1144 , (3, 0, None, None) , 0 , )),
	(( 'SnapExtensions' , 'pnRet' , ), 1610743944, (1610743944, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1152 , (3, 0, None, None) , 0 , )),
	(( 'SnapAngles' , 'dAngles' , ), 1610743946, (1610743946, (), [ (24581, 10, None, None) , ], 1 , 2 , 4 , 0 , 1160 , (3, 0, None, None) , 0 , )),
	(( 'SnapAngles' , 'dAngles' , ), 1610743946, (1610743946, (), [ (24581, 1, None, None) , ], 1 , 4 , 4 , 0 , 1168 , (3, 0, None, None) , 0 , )),
	(( 'GlueEnabled' , 'pbRet' , ), 1610743948, (1610743948, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1176 , (3, 0, None, None) , 0 , )),
	(( 'GlueEnabled' , 'pbRet' , ), 1610743948, (1610743948, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1184 , (3, 0, None, None) , 0 , )),
	(( 'GlueSettings' , 'pnRet' , ), 1610743950, (1610743950, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1192 , (3, 0, None, None) , 0 , )),
	(( 'GlueSettings' , 'pnRet' , ), 1610743950, (1610743950, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1200 , (3, 0, None, None) , 0 , )),
	(( 'DynamicGridEnabled' , 'pbRet' , ), 1610743952, (1610743952, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1208 , (3, 0, None, None) , 0 , )),
	(( 'DynamicGridEnabled' , 'pbRet' , ), 1610743952, (1610743952, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1216 , (3, 0, None, None) , 0 , )),
	(( 'DefaultGuideStyle' , 'lpLocaleSpecificName' , ), 1610743954, (1610743954, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1224 , (3, 0, None, None) , 0 , )),
	(( 'DefaultGuideStyle' , 'lpLocaleSpecificName' , ), 1610743954, (1610743954, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1232 , (3, 0, None, None) , 0 , )),
	(( 'Protection' , 'bstrPassword' , 'pnRet' , ), 1610743956, (1610743956, (), [ (12, 17, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 1 , 1240 , (3, 0, None, None) , 0 , )),
	(( 'Protection' , 'bstrPassword' , 'pnRet' , ), 1610743956, (1610743956, (), [ (12, 17, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 1 , 1240 , (3, 0, None, None) , 0 , )),
	(( 'Protection' , 'bstrPassword' , 'pnRet' , ), 1610743956, (1610743956, (), [ (12, 17, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1248 , (3, 0, None, None) , 0 , )),
	(( 'Protection' , 'bstrPassword' , 'pnRet' , ), 1610743956, (1610743956, (), [ (12, 17, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1248 , (3, 0, None, None) , 0 , )),
	(( 'Printer' , 'pbstrRet' , ), 1610743958, (1610743958, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1256 , (3, 0, None, None) , 0 , )),
	(( 'Printer' , 'pbstrRet' , ), 1610743958, (1610743958, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1264 , (3, 0, None, None) , 0 , )),
	(( 'PrintCopies' , 'pnRet' , ), 1610743960, (1610743960, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1272 , (3, 0, None, None) , 64 , )),
	(( 'PrintCopies' , 'pnRet' , ), 1610743960, (1610743960, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1280 , (3, 0, None, None) , 64 , )),
	(( 'HeaderLeft' , 'pbstrRet' , ), 1610743962, (1610743962, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1288 , (3, 0, None, None) , 0 , )),
	(( 'HeaderLeft' , 'pbstrRet' , ), 1610743962, (1610743962, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1296 , (3, 0, None, None) , 0 , )),
	(( 'HeaderCenter' , 'pbstrRet' , ), 1610743964, (1610743964, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1304 , (3, 0, None, None) , 0 , )),
	(( 'HeaderCenter' , 'pbstrRet' , ), 1610743964, (1610743964, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1312 , (3, 0, None, None) , 0 , )),
	(( 'HeaderRight' , 'pbstrRet' , ), 1610743966, (1610743966, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1320 , (3, 0, None, None) , 0 , )),
	(( 'HeaderRight' , 'pbstrRet' , ), 1610743966, (1610743966, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1328 , (3, 0, None, None) , 0 , )),
	(( 'HeaderMargin' , 'UnitsNameOrCode' , 'pdRet' , ), 1610743968, (1610743968, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 1336 , (3, 0, None, None) , 0 , )),
	(( 'HeaderMargin' , 'UnitsNameOrCode' , 'pdRet' , ), 1610743968, (1610743968, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 1336 , (3, 0, None, None) , 0 , )),
	(( 'HeaderMargin' , 'UnitsNameOrCode' , 'pdRet' , ), 1610743968, (1610743968, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 1344 , (3, 0, None, None) , 0 , )),
	(( 'HeaderMargin' , 'UnitsNameOrCode' , 'pdRet' , ), 1610743968, (1610743968, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 1344 , (3, 0, None, None) , 0 , )),
	(( 'FooterLeft' , 'pbstrRet' , ), 1610743970, (1610743970, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1352 , (3, 0, None, None) , 0 , )),
	(( 'FooterLeft' , 'pbstrRet' , ), 1610743970, (1610743970, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1360 , (3, 0, None, None) , 0 , )),
	(( 'FooterCenter' , 'pbstrRet' , ), 1610743972, (1610743972, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1368 , (3, 0, None, None) , 0 , )),
	(( 'FooterCenter' , 'pbstrRet' , ), 1610743972, (1610743972, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1376 , (3, 0, None, None) , 0 , )),
	(( 'FooterRight' , 'pbstrRet' , ), 1610743974, (1610743974, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1384 , (3, 0, None, None) , 0 , )),
	(( 'FooterRight' , 'pbstrRet' , ), 1610743974, (1610743974, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1392 , (3, 0, None, None) , 0 , )),
	(( 'FooterMargin' , 'UnitsNameOrCode' , 'pdRet' , ), 1610743976, (1610743976, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 1400 , (3, 0, None, None) , 0 , )),
	(( 'FooterMargin' , 'UnitsNameOrCode' , 'pdRet' , ), 1610743976, (1610743976, (), [ (12, 17, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 1 , 1400 , (3, 0, None, None) , 0 , )),
	(( 'FooterMargin' , 'UnitsNameOrCode' , 'pdRet' , ), 1610743976, (1610743976, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 1408 , (3, 0, None, None) , 0 , )),
	(( 'FooterMargin' , 'UnitsNameOrCode' , 'pdRet' , ), 1610743976, (1610743976, (), [ (12, 17, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 1408 , (3, 0, None, None) , 0 , )),
	(( 'HeaderFooterFont' , 'ppFontDisp' , ), 1610743978, (1610743978, (), [ (16393, 10, None, "IID('{BEF6E003-A874-101A-8BBA-00AA00300CAB}')") , ], 1 , 2 , 4 , 0 , 1416 , (3, 0, None, None) , 0 , )),
	(( 'HeaderFooterFont' , 'ppFontDisp' , ), 1610743978, (1610743978, (), [ (9, 1, None, "IID('{BEF6E003-A874-101A-8BBA-00AA00300CAB}')") , ], 1 , 8 , 4 , 0 , 1424 , (3, 0, None, None) , 0 , )),
	(( 'HeaderFooterColor' , 'pColor' , ), 1610743980, (1610743980, (), [ (16403, 10, None, None) , ], 1 , 2 , 4 , 0 , 1432 , (3, 0, None, None) , 0 , )),
	(( 'HeaderFooterColor' , 'pColor' , ), 1610743980, (1610743980, (), [ (19, 1, None, None) , ], 1 , 4 , 4 , 0 , 1440 , (3, 0, None, None) , 0 , )),
	(( 'Password' , 'bstrExistingPassword' , ), 1610743982, (1610743982, (), [ (12, 17, None, None) , (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1448 , (3, 0, None, None) , 64 , )),
	(( 'Password' , 'bstrExistingPassword' , ), 1610743982, (1610743982, (), [ (12, 17, None, None) , (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1448 , (3, 0, None, None) , 64 , )),
	(( 'PreviewPicture' , 'ppPictureDisp' , ), 1610743983, (1610743983, (), [ (16393, 10, None, "IID('{7BF80981-BF32-101A-8BBB-00AA00300CAB}')") , ], 1 , 2 , 4 , 0 , 1456 , (3, 0, None, None) , 0 , )),
	(( 'PreviewPicture' , 'ppPictureDisp' , ), 1610743983, (1610743983, (), [ (9, 1, None, "IID('{7BF80981-BF32-101A-8BBB-00AA00300CAB}')") , ], 1 , 8 , 4 , 0 , 1464 , (3, 0, None, None) , 0 , )),
	(( 'Clean' , 'nTargets' , 'nActions' , 'nAlerts' , 'nFixes' , 
			 'bStopOnError' , 'bLogFileName' , 'nReserved' , ), 1610743985, (1610743985, (), [ (12, 17, None, None) , 
			 (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , (12, 17, None, None) , 
			 (12, 17, None, None) , ], 1 , 1 , 4 , 7 , 1472 , (3, 0, None, None) , 0 , )),
	(( 'BuildNumberCreated' , 'pnBuildNumCreated' , ), 1610743986, (1610743986, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1480 , (3, 0, None, None) , 0 , )),
	(( 'BuildNumberEdited' , 'pnBuildNumEdited' , ), 1610743987, (1610743987, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1488 , (3, 0, None, None) , 0 , )),
	(( 'TimeCreated' , 'pdTimeCreated' , ), 1610743988, (1610743988, (), [ (16391, 10, None, None) , ], 1 , 2 , 4 , 0 , 1496 , (3, 0, None, None) , 0 , )),
	(( 'Time' , 'pdTimeCurrent' , ), 1610743989, (1610743989, (), [ (16391, 10, None, None) , ], 1 , 2 , 4 , 0 , 1504 , (3, 0, None, None) , 0 , )),
	(( 'TimeEdited' , 'pdTimeEdited' , ), 1610743990, (1610743990, (), [ (16391, 10, None, None) , ], 1 , 2 , 4 , 0 , 1512 , (3, 0, None, None) , 0 , )),
	(( 'TimePrinted' , 'pdTimePrinted' , ), 1610743991, (1610743991, (), [ (16391, 10, None, None) , ], 1 , 2 , 4 , 0 , 1520 , (3, 0, None, None) , 0 , )),
	(( 'TimeSaved' , 'pdTimeSaved' , ), 1610743992, (1610743992, (), [ (16391, 10, None, None) , ], 1 , 2 , 4 , 0 , 1528 , (3, 0, None, None) , 0 , )),
	(( 'CopyPreviewPicture' , 'pSourceDoc' , ), 1610743993, (1610743993, (), [ (9, 1, None, "IID('{000D0705-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1536 , (3, 0, None, None) , 0 , )),
	(( 'ContainsWorkspace' , 'pbRet' , ), 1610743994, (1610743994, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1544 , (3, 0, None, None) , 64 , )),
	(( 'EmailRoutingData' , 'pData' , ), 1610743995, (1610743995, (), [ (24588, 10, None, None) , ], 1 , 2 , 4 , 0 , 1552 , (3, 0, None, None) , 0 , )),
	(( 'VBProjectData' , 'pData' , ), 1610743996, (1610743996, (), [ (24593, 10, None, None) , ], 1 , 2 , 4 , 0 , 1560 , (3, 0, None, None) , 0 , )),
	(( 'SolutionXMLElementCount' , 'pElementCount' , ), 1610743997, (1610743997, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1568 , (3, 0, None, None) , 0 , )),
	(( 'SolutionXMLElementName' , 'Index' , 'pElementName' , ), 1610743998, (1610743998, (), [ (3, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1576 , (3, 0, None, None) , 0 , )),
	(( 'SolutionXMLElementExists' , 'ElementName' , 'pbRet' , ), 1610743999, (1610743999, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1584 , (3, 0, None, None) , 0 , )),
	(( 'SolutionXMLElement' , 'ElementName' , 'pWellFormedXML' , ), 1610744000, (1610744000, (), [ (8, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1592 , (3, 0, None, None) , 0 , )),
	(( 'SolutionXMLElement' , 'ElementName' , 'pWellFormedXML' , ), 1610744000, (1610744000, (), [ (8, 1, None, None) , 
			 (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1600 , (3, 0, None, None) , 0 , )),
	(( 'DeleteSolutionXMLElement' , 'ElementName' , ), 1610744002, (1610744002, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 1608 , (3, 0, None, None) , 0 , )),
	(( 'FullBuildNumberCreated' , 'pnFullBuildNumCreated' , ), 1610744003, (1610744003, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1616 , (3, 0, None, None) , 0 , )),
	(( 'FullBuildNumberEdited' , 'pnFullBuildNumEdited' , ), 1610744004, (1610744004, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1624 , (3, 0, None, None) , 0 , )),
	(( 'ID' , 'lpi4Ret' , ), 1610744005, (1610744005, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1632 , (3, 0, None, None) , 0 , )),
	(( 'MacrosEnabled' , 'pbRet' , ), 1610744006, (1610744006, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1640 , (3, 0, None, None) , 0 , )),
	(( 'ZoomBehavior' , 'pnZoomBehavior' , ), 1610744007, (1610744007, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1648 , (3, 0, None, None) , 0 , )),
	(( 'ZoomBehavior' , 'pnZoomBehavior' , ), 1610744007, (1610744007, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1656 , (3, 0, None, None) , 0 , )),
	(( 'CanCheckIn' , 'pbRet' , ), 1610744009, (1610744009, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 1664 , (3, 0, None, None) , 0 , )),
	(( 'CheckIn' , 'SaveChanges' , 'Comments' , 'MakePublic' , ), 1610744010, (1610744010, (), [ 
			 (11, 49, 'True', None) , (16396, 17, None, None) , (11, 49, 'False', None) , ], 1 , 1 , 4 , 0 , 1672 , (3, 0, None, None) , 0 , )),
	(( 'Type' , 'pnDocType' , ), 1610744011, (1610744011, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1680 , (3, 0, None, None) , 0 , )),
	(( 'Language' , 'lpLangID' , ), 1610744012, (1610744012, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1688 , (3, 0, None, None) , 0 , )),
	(( 'Language' , 'lpLangID' , ), 1610744012, (1610744012, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1696 , (3, 0, None, None) , 64 , )),
	(( 'RemovePersonalInformation' , 'pbRet' , ), 1610744014, (1610744014, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1704 , (3, 0, None, None) , 0 , )),
	(( 'RemovePersonalInformation' , 'pbRet' , ), 1610744014, (1610744014, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1712 , (3, 0, None, None) , 0 , )),
	(( 'PrintOut' , 'PrintRange' , 'FromPage' , 'ToPage' , 'ScaleCurrentViewToPaper' , 
			 'PrinterName' , 'PrintToFile' , 'OutputFileName' , 'Copies' , 'Collate' , 
			 'ColorAsBlack' , ), 1610744016, (1610744016, (), [ (3, 1, None, None) , (3, 49, '1', None) , (3, 49, '-1', None) , 
			 (11, 49, 'False', None) , (8, 49, "''", None) , (11, 49, 'False', None) , (8, 49, "''", None) , (3, 49, '1', None) , 
			 (11, 49, 'False', None) , (11, 49, 'False', None) , ], 1 , 1 , 4 , 0 , 1720 , (3, 32, None, None) , 0 , )),
	(( 'BeginUndoScope' , 'bstrUndoScopeName' , 'pnScopeID' , ), 1610744017, (1610744017, (), [ (8, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 1728 , (3, 0, None, None) , 0 , )),
	(( 'EndUndoScope' , 'nScopeID' , 'bCommit' , ), 1610744018, (1610744018, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 1736 , (3, 0, None, None) , 0 , )),
	(( 'AddUndoUnit' , 'pUndoUnit' , ), 1610744019, (1610744019, (), [ (13, 1, None, None) , ], 1 , 1 , 4 , 0 , 1744 , (3, 0, None, None) , 0 , )),
	(( 'PurgeUndo' , ), 1610744020, (1610744020, (), [ ], 1 , 1 , 4 , 0 , 1752 , (3, 0, None, None) , 0 , )),
	(( 'UndoEnabled' , 'pbRet' , ), 1610744021, (1610744021, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1760 , (3, 0, None, None) , 0 , )),
	(( 'UndoEnabled' , 'pbRet' , ), 1610744021, (1610744021, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1768 , (3, 0, None, None) , 0 , )),
	(( 'RenameCurrentScope' , 'bstrScopeName' , ), 1610744023, (1610744023, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 1776 , (3, 0, None, None) , 0 , )),
	(( 'SharedWorkspace' , 'lpdispRet' , ), 1610744024, (1610744024, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 1784 , (3, 0, None, None) , 0 , )),
	(( 'Sync' , 'lpdispRet' , ), 1610744025, (1610744025, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 1792 , (3, 0, None, None) , 0 , )),
	(( 'RemoveHiddenInformation' , 'RemoveHiddenInfoItems' , ), 1610744026, (1610744026, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 1800 , (3, 0, None, None) , 0 , )),
	(( 'DataRecordsets' , 'DataRecordsets' , ), 1610744027, (1610744027, (), [ (16393, 10, None, "IID('{000D072E-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1808 , (3, 0, None, None) , 0 , )),
	(( 'GetThemeNames' , 'eType' , 'NameArray' , ), 1610744028, (1610744028, (), [ (3, 1, None, None) , 
			 (24584, 2, None, None) , ], 1 , 1 , 4 , 0 , 1816 , (3, 0, None, None) , 0 , )),
	(( 'GetThemeNamesU' , 'eType' , 'NameArray' , ), 1610744029, (1610744029, (), [ (3, 1, None, None) , 
			 (24584, 2, None, None) , ], 1 , 1 , 4 , 0 , 1824 , (3, 0, None, None) , 0 , )),
	(( 'CanUndoCheckOut' , 'pbRet' , ), 1610744030, (1610744030, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 1832 , (3, 0, None, None) , 0 , )),
	(( 'UndoCheckOut' , ), 1610744031, (1610744031, (), [ ], 1 , 1 , 4 , 0 , 1840 , (3, 0, None, None) , 0 , )),
	(( 'ContainsWorkspaceEx' , 'TrueOrFalse' , ), 1610744032, (1610744032, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1848 , (3, 0, None, None) , 0 , )),
	(( 'ContainsWorkspaceEx' , 'TrueOrFalse' , ), 1610744032, (1610744032, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1856 , (3, 0, None, None) , 0 , )),
	(( 'ExportAsFixedFormat' , 'FixedFormat' , 'OutputFileName' , 'Intent' , 'PrintRange' , 
			 'FromPage' , 'ToPage' , 'ColorAsBlack' , 'IncludeBackground' , 'IncludeDocumentProperties' , 
			 'IncludeStructureTags' , 'UseISO19005_1' , 'FixedFormatExtClass' , ), 1610744034, (1610744034, (), [ (3, 1, None, None) , 
			 (8, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 49, '1', None) , (3, 49, '-1', None) , 
			 (11, 49, 'False', None) , (11, 49, 'True', None) , (11, 49, 'True', None) , (11, 49, 'True', None) , (11, 49, 'False', None) , 
			 (12, 17, None, None) , ], 1 , 1 , 4 , 1 , 1864 , (3, 0, None, None) , 0 , )),
	(( 'DefaultSavePath' , 'SaveLocation' , ), 1610744035, (1610744035, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1872 , (3, 0, None, None) , 0 , )),
	(( 'DefaultSavePath' , 'SaveLocation' , ), 1610744035, (1610744035, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1880 , (3, 0, None, None) , 0 , )),
	(( 'CustomUI' , 'lpbstrRet' , ), 1610744037, (1610744037, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1888 , (3, 0, None, None) , 0 , )),
	(( 'CustomUI' , 'lpbstrRet' , ), 1610744037, (1610744037, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1896 , (3, 0, None, None) , 0 , )),
	(( 'UserCustomUI' , 'lpbstrRet' , ), 1610744039, (1610744039, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1904 , (3, 0, None, None) , 0 , )),
	(( 'UserCustomUI' , 'lpbstrRet' , ), 1610744039, (1610744039, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1912 , (3, 0, None, None) , 0 , )),
	(( 'ServerPublishOptions' , 'ServerPublishOptions' , ), 1610744041, (1610744041, (), [ (16393, 10, None, "IID('{000D0739-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1920 , (3, 0, None, None) , 0 , )),
	(( 'Validation' , 'pValidation' , ), 1610744042, (1610744042, (), [ (16393, 10, None, "IID('{000D073A-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1928 , (3, 0, None, None) , 0 , )),
	(( 'DiagramServicesEnabled' , 'pDiagramServices' , ), 1610744043, (1610744043, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1936 , (3, 0, None, None) , 0 , )),
	(( 'DiagramServicesEnabled' , 'pDiagramServices' , ), 1610744043, (1610744043, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1944 , (3, 0, None, None) , 0 , )),
	(( 'CompatibilityMode' , 'pbRet' , ), 1610744045, (1610744045, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1952 , (3, 0, None, None) , 0 , )),
	(( 'Comments' , 'ppComments' , ), 1610744046, (1610744046, (), [ (16393, 10, None, "IID('{000D0743-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1960 , (3, 0, None, None) , 0 , )),
	(( 'EditorCount' , 'pEditors' , ), 1610744047, (1610744047, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1968 , (3, 0, None, None) , 0 , )),
	(( 'Permission' , 'lpdispRet' , ), 1610744048, (1610744048, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 1976 , (3, 0, None, None) , 0 , )),
]

win32com.client.CLSIDToClass.RegisterCLSID( "{000D0705-0000-0000-C000-000000000046}", IVDocument )
