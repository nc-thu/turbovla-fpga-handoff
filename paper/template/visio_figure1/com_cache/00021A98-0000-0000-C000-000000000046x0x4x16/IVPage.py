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
class IVPage(DispatchBaseClass):
	CLSID = IID('{000D0709-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{000D0A06-0000-0000-C000-000000000046}')

	# Result is of type IVShape
	def AddDataVisualization(self, DataRecordsetID=defaultNamedNotOptArg, ObjectToDrop=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743916, LCID, 1, (9, 0), ((3, 1), (13, 17)),DataRecordsetID
			, ObjectToDrop)
		if ret is not None:
			ret = Dispatch(ret, 'AddDataVisualization', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def AddGuide(self, Type=defaultNamedNotOptArg, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((2, 1), (5, 1), (5, 1)),Type
			, xPos, yPos)
		if ret is not None:
			ret = Dispatch(ret, 'AddGuide', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def AutoConnectMany(self, FromShapeIDs=defaultNamedNotOptArg, ToShapeIDs=defaultNamedNotOptArg, PlacementDirs=defaultNamedNotOptArg, Connector=None):
		return self._oleobj_.InvokeTypes(1610743887, LCID, 1, (3, 0), ((24579, 1), (24579, 1), (24579, 1), (13, 49)),FromShapeIDs
			, ToShapeIDs, PlacementDirs, Connector)

	def AutoSizeDrawing(self):
		return self._oleobj_.InvokeTypes(1610743903, LCID, 1, (24, 0), (),)

	def AvoidPageBreaks(self):
		return self._oleobj_.InvokeTypes(1610743891, LCID, 1, (24, 0), (),)

	def BoundingBox(self, Flags=defaultNamedNotOptArg, lpr8Left=pythoncom.Missing, lpr8Bottom=pythoncom.Missing, lpr8Right=pythoncom.Missing
			, lpr8Top=pythoncom.Missing):
		return self._ApplyTypes_(39, 1, (24, 0), ((2, 1), (16389, 2), (16389, 2), (16389, 2), (16389, 2)), 'BoundingBox', None,Flags
			, lpr8Left, lpr8Bottom, lpr8Right, lpr8Top)

	def CenterDrawing(self):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (24, 0), (),)

	# Result is of type IVShape
	def CreateDataVisualizerDiagram(self, szConnectionString='', szQueryString='', ObjectToDrop=defaultNamedNotOptArg, pDataVisualizerSettings=defaultNamedNotOptArg
			, bConfirmSettings=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610743917, 1, (9, 32), ((8, 49), (8, 49), (13, 17), (9, 17), (11, 17)), 'CreateDataVisualizerDiagram', '{000D070C-0000-0000-C000-000000000046}',szConnectionString
			, szQueryString, ObjectToDrop, pDataVisualizerSettings, bConfirmSettings)

	# Result is of type IVSelection
	def CreateSelection(self, SelType=defaultNamedNotOptArg, IterationMode=256, Data=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(1610743868, LCID, 1, (9, 0), ((3, 1), (3, 49), (12, 17)),SelType
			, IterationMode, Data)
		if ret is not None:
			ret = Dispatch(ret, 'CreateSelection', '{000D070B-0000-0000-C000-000000000046}')
		return ret

	def Delete(self, fRenumberPages=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((2, 1),),fRenumberPages
			)

	# Result is of type IVShape
	def DrawArcByThreePoints(self, xBegin=defaultNamedNotOptArg, yBegin=defaultNamedNotOptArg, xEnd=defaultNamedNotOptArg, yEnd=defaultNamedNotOptArg
			, xControl=defaultNamedNotOptArg, yControl=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743870, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1)),xBegin
			, yBegin, xEnd, yEnd, xControl, yControl
			)
		if ret is not None:
			ret = Dispatch(ret, 'DrawArcByThreePoints', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawBezier(self, xyArray=defaultNamedNotOptArg, degree=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(26, LCID, 1, (9, 0), ((24581, 1), (2, 1), (2, 1)),xyArray
			, degree, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'DrawBezier', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawCircularArc(self, xCenter=defaultNamedNotOptArg, yCenter=defaultNamedNotOptArg, Radius=defaultNamedNotOptArg, StartAngle=0.0
			, EndAngle=3.1415927410125732):
		ret = self._oleobj_.InvokeTypes(1610743872, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 49), (5, 49)),xCenter
			, yCenter, Radius, StartAngle, EndAngle)
		if ret is not None:
			ret = Dispatch(ret, 'DrawCircularArc', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawLine(self, xBegin=defaultNamedNotOptArg, yBegin=defaultNamedNotOptArg, xEnd=defaultNamedNotOptArg, yEnd=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(6, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1)),xBegin
			, yBegin, xEnd, yEnd)
		if ret is not None:
			ret = Dispatch(ret, 'DrawLine', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawNURBS(self, degree=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg, xyArray=defaultNamedNotOptArg, knots=defaultNamedNotOptArg
			, weights=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(47, LCID, 1, (9, 0), ((2, 1), (2, 1), (24581, 1), (24581, 1), (12, 17)),degree
			, Flags, xyArray, knots, weights)
		if ret is not None:
			ret = Dispatch(ret, 'DrawNURBS', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawOval(self, x1=defaultNamedNotOptArg, y1=defaultNamedNotOptArg, x2=defaultNamedNotOptArg, y2=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(8, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1)),x1
			, y1, x2, y2)
		if ret is not None:
			ret = Dispatch(ret, 'DrawOval', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawPolyline(self, xyArray=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(27, LCID, 1, (9, 0), ((24581, 1), (2, 1)),xyArray
			, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'DrawPolyline', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawQuarterArc(self, xBegin=defaultNamedNotOptArg, yBegin=defaultNamedNotOptArg, xEnd=defaultNamedNotOptArg, yEnd=defaultNamedNotOptArg
			, SweepFlag=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743871, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1), (3, 1)),xBegin
			, yBegin, xEnd, yEnd, SweepFlag)
		if ret is not None:
			ret = Dispatch(ret, 'DrawQuarterArc', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawRectangle(self, x1=defaultNamedNotOptArg, y1=defaultNamedNotOptArg, x2=defaultNamedNotOptArg, y2=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(7, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1)),x1
			, y1, x2, y2)
		if ret is not None:
			ret = Dispatch(ret, 'DrawRectangle', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawSpline(self, xyArray=defaultNamedNotOptArg, Tolerance=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(25, LCID, 1, (9, 0), ((24581, 1), (5, 1), (2, 1)),xyArray
			, Tolerance, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'DrawSpline', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def Drop(self, ObjectToDrop=defaultNamedNotOptArg, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(9, LCID, 1, (9, 0), ((13, 1), (5, 1), (5, 1)),ObjectToDrop
			, xPos, yPos)
		if ret is not None:
			ret = Dispatch(ret, 'Drop', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DropCallout(self, ObjectToDrop=defaultNamedNotOptArg, TargetShape=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743893, LCID, 1, (9, 0), ((13, 1), (9, 1)),ObjectToDrop
			, TargetShape)
		if ret is not None:
			ret = Dispatch(ret, 'DropCallout', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DropConnected(self, ObjectToDrop=defaultNamedNotOptArg, TargetShape=defaultNamedNotOptArg, PlacementDir=defaultNamedNotOptArg, Connector=None):
		ret = self._oleobj_.InvokeTypes(1610743886, LCID, 1, (9, 0), ((13, 1), (9, 1), (3, 1), (13, 49)),ObjectToDrop
			, TargetShape, PlacementDir, Connector)
		if ret is not None:
			ret = Dispatch(ret, 'DropConnected', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DropContainer(self, ObjectToDrop=defaultNamedNotOptArg, TargetShapes=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743888, LCID, 1, (9, 0), ((13, 1), (13, 1)),ObjectToDrop
			, TargetShapes)
		if ret is not None:
			ret = Dispatch(ret, 'DropContainer', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DropIntoList(self, ObjectToDrop=defaultNamedNotOptArg, TargetList=defaultNamedNotOptArg, lPosition=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743900, LCID, 1, (9, 0), ((13, 1), (9, 1), (3, 1)),ObjectToDrop
			, TargetList, lPosition)
		if ret is not None:
			ret = Dispatch(ret, 'DropIntoList', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DropLegend(self, OuterList=defaultNamedNotOptArg, InnerContainer=defaultNamedNotOptArg, populateFlags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743899, LCID, 1, (9, 0), ((13, 1), (13, 1), (3, 1)),OuterList
			, InnerContainer, populateFlags)
		if ret is not None:
			ret = Dispatch(ret, 'DropLegend', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DropLinked(self, ObjectToDrop=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, DataRecordsetID=defaultNamedNotOptArg
			, DataRowID=defaultNamedNotOptArg, ApplyDataGraphicAfterLink=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743880, LCID, 1, (9, 0), ((13, 1), (5, 1), (5, 1), (3, 1), (3, 1), (11, 1)),ObjectToDrop
			, x, y, DataRecordsetID, DataRowID, ApplyDataGraphicAfterLink
			)
		if ret is not None:
			ret = Dispatch(ret, 'DropLinked', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def DropMany(self, ObjectsToInstance=defaultNamedNotOptArg, xyArray=defaultNamedNotOptArg, IDArray=pythoncom.Missing):
		'Creates many shapes on this page. Names, if supplied, are considered locale specific.'
		return self._ApplyTypes_(31, 1, (2, 0), ((24588, 1), (24581, 1), (24578, 2)), 'DropMany', None,ObjectsToInstance
			, xyArray, IDArray)

	def DropManyLinkedU(self, ObjectsToInstance=defaultNamedNotOptArg, XYs=defaultNamedNotOptArg, DataRecordsetID=defaultNamedNotOptArg, DataRowIDs=defaultNamedNotOptArg
			, ApplyDataGraphicAfterLink=defaultNamedNotOptArg, ShapeIDs=pythoncom.Missing):
		'Creates many linked shapes on this page. Names, if supplied, are considered locale independent.'
		return self._ApplyTypes_(1610743881, 1, (3, 0), ((24588, 1), (24581, 1), (3, 1), (24579, 1), (11, 1), (24579, 2)), 'DropManyLinkedU', None,ObjectsToInstance
			, XYs, DataRecordsetID, DataRowIDs, ApplyDataGraphicAfterLink, ShapeIDs
			)

	def DropManyU(self, ObjectsToInstance=defaultNamedNotOptArg, xyArray=defaultNamedNotOptArg, IDArray=pythoncom.Missing):
		'Creates many shapes on this page. Names, if supplied, are considered locale independent.'
		return self._ApplyTypes_(45, 1, (2, 0), ((24588, 1), (24581, 1), (24578, 2)), 'DropManyU', None,ObjectsToInstance
			, xyArray, IDArray)

	# Result is of type IVPage
	def Duplicate(self):
		'Returns a new page duplicated from this page.'
		ret = self._oleobj_.InvokeTypes(1610743904, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'Duplicate', '{000D0709-0000-0000-C000-000000000046}')
		return ret

	def Export(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	def GetCallouts(self, NestedOptions=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610743896, 1, (8195, 0), ((3, 1),), 'GetCallouts', None,NestedOptions
			)

	def GetContainers(self, NestedOptions=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610743895, 1, (8195, 0), ((3, 1),), 'GetContainers', None,NestedOptions
			)

	def GetFormulas(self, SID_SRCStream=defaultNamedNotOptArg, formulaArray=pythoncom.Missing):
		'Returns cell formulas in locale specific syntax.'
		return self._ApplyTypes_(32, 1, (24, 0), ((24578, 1), (24588, 2)), 'GetFormulas', None,SID_SRCStream
			, formulaArray)

	def GetFormulasU(self, SID_SRCStream=defaultNamedNotOptArg, formulaArray=pythoncom.Missing):
		'Returns cell formulas in locale independent syntax.'
		return self._ApplyTypes_(46, 1, (24, 0), ((24578, 1), (24588, 2)), 'GetFormulasU', None,SID_SRCStream
			, formulaArray)

	def GetResults(self, SID_SRCStream=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg, UnitsNamesOrCodes=defaultNamedNotOptArg, resultArray=pythoncom.Missing):
		return self._ApplyTypes_(33, 1, (24, 0), ((24578, 1), (2, 1), (24588, 1), (24588, 2)), 'GetResults', None,SID_SRCStream
			, Flags, UnitsNamesOrCodes, resultArray)

	def GetShapesLinkedToData(self, DataRecordsetID=defaultNamedNotOptArg, ShapeIDs=pythoncom.Missing):
		return self._ApplyTypes_(1610743875, 1, (24, 0), ((3, 1), (24579, 2)), 'GetShapesLinkedToData', None,DataRecordsetID
			, ShapeIDs)

	def GetShapesLinkedToDataRow(self, DataRecordsetID=defaultNamedNotOptArg, DataRowID=defaultNamedNotOptArg, ShapeIDs=pythoncom.Missing):
		return self._ApplyTypes_(1610743876, 1, (24, 0), ((3, 1), (3, 1), (24579, 2)), 'GetShapesLinkedToDataRow', None,DataRecordsetID
			, DataRowID, ShapeIDs)

	def GetTheme(self, eThemeType=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610743905, 1, (12, 0), ((3, 1),), 'GetTheme', None,eThemeType
			)

	def GetThemeVariant(self, pVariantColor=pythoncom.Missing, pVariantStyle=pythoncom.Missing, pEmbellishment=0):
		return self._ApplyTypes_(1610743909, 1, (24, 0), ((16386, 2), (16386, 2), (16386, 50)), 'GetThemeVariant', None,pVariantColor
			, pVariantStyle, pEmbellishment)

	# Result is of type IVShape
	def Import(self, FileName=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(17, LCID, 1, (9, 0), ((8, 1),),FileName
			)
		if ret is not None:
			ret = Dispatch(ret, 'Import', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def InsertFromFile(self, FileName=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(28, LCID, 1, (9, 0), ((8, 1), (2, 1)),FileName
			, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'InsertFromFile', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def InsertObject(self, ClassOrProgID=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(29, LCID, 1, (9, 0), ((8, 1), (2, 1)),ClassOrProgID
			, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'InsertObject', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def Layout(self):
		return self._oleobj_.InvokeTypes(38, LCID, 1, (24, 0), (),)

	def LayoutChangeDirection(self, Direction=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743890, LCID, 1, (24, 0), ((3, 1),),Direction
			)

	def LayoutIncremental(self, AlignOrSpace=defaultNamedNotOptArg, AlignHorizontal=defaultNamedNotOptArg, AlignVertical=defaultNamedNotOptArg, SpaceHorizontal=defaultNamedNotOptArg
			, SpaceVertical=defaultNamedNotOptArg, UnitsNameOrCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743889, LCID, 1, (24, 0), ((3, 1), (3, 1), (3, 1), (5, 1), (5, 1), (3, 1)),AlignOrSpace
			, AlignHorizontal, AlignVertical, SpaceHorizontal, SpaceVertical, UnitsNameOrCode
			)

	def LinkShapesToDataRows(self, DataRecordsetID=defaultNamedNotOptArg, DataRowIDs=defaultNamedNotOptArg, ShapeIDs=defaultNamedNotOptArg, ApplyDataGraphicAfterLink=True):
		return self._oleobj_.InvokeTypes(1610743877, LCID, 1, (24, 0), ((3, 1), (24579, 1), (24579, 1), (11, 49)),DataRecordsetID
			, DataRowIDs, ShapeIDs, ApplyDataGraphicAfterLink)

	# Result is of type IVWindow
	def OpenDrawWindow(self):
		ret = self._oleobj_.InvokeTypes(30, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'OpenDrawWindow', '{000D0710-0000-0000-C000-000000000046}')
		return ret

	def Paste(self, Flags=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743866, LCID, 1, (24, 0), ((12, 17),),Flags
			)

	def PasteSpecial(self, Format=defaultNamedNotOptArg, Link=defaultNamedOptArg, DisplayAsIcon=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743867, LCID, 1, (24, 0), ((3, 1), (12, 17), (12, 17)),Format
			, Link, DisplayAsIcon)

	def PasteToLocation(self, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743894, LCID, 1, (24, 0), ((5, 1), (5, 1), (3, 1)),xPos
			, yPos, Flags)

	def Print(self):
		return self._oleobj_.InvokeTypes(15, LCID, 1, (24, 0), (),)

	def PrintTile(self, nTile=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743864, LCID, 1, (24, 0), ((3, 1),),nTile
			)

	def ResizeToFitContents(self):
		return self._oleobj_.InvokeTypes(1610743865, LCID, 1, (24, 0), (),)

	def SetFormulas(self, SID_SRCStream=defaultNamedNotOptArg, formulaArray=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(34, LCID, 1, (2, 0), ((24578, 1), (24588, 1), (2, 1)),SID_SRCStream
			, formulaArray, Flags)

	def SetResults(self, SID_SRCStream=defaultNamedNotOptArg, UnitsNamesOrCodes=defaultNamedNotOptArg, resultArray=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(35, LCID, 1, (2, 0), ((24578, 1), (24588, 1), (24588, 1), (2, 1)),SID_SRCStream
			, UnitsNamesOrCodes, resultArray, Flags)

	def SetTheme(self, varThemeIndex=defaultNamedNotOptArg, varColorScheme=defaultNamedOptArg, varEffectScheme=defaultNamedOptArg, varConnectorScheme=defaultNamedOptArg
			, varFontScheme=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743906, LCID, 1, (24, 0), ((12, 1), (12, 17), (12, 17), (12, 17), (12, 17)),varThemeIndex
			, varColorScheme, varEffectScheme, varConnectorScheme, varFontScheme)

	def SetThemeVariant(self, variantColor=defaultNamedNotOptArg, variantStyle=defaultNamedNotOptArg, embellishment=-1):
		return self._oleobj_.InvokeTypes(1610743910, LCID, 1, (24, 0), ((2, 1), (2, 1), (2, 49)),variantColor
			, variantStyle, embellishment)

	def ShapeIDsToUniqueIDs(self, ShapeIDs=defaultNamedNotOptArg, UniqueIDArgs=defaultNamedNotOptArg, GUIDs=pythoncom.Missing):
		return self._ApplyTypes_(1610743878, 1, (24, 0), ((24579, 1), (3, 1), (24584, 2)), 'ShapeIDsToUniqueIDs', None,ShapeIDs
			, UniqueIDArgs, GUIDs)

	# Result is of type IVSelection
	# The method SpatialSearch is actually a property, but must be used as a method to correctly pass the arguments
	def SpatialSearch(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, Relation=defaultNamedNotOptArg, Tolerance=defaultNamedNotOptArg
			, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(43, LCID, 2, (9, 0), ((5, 1), (5, 1), (2, 1), (5, 1), (2, 1)),x
			, y, Relation, Tolerance, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'SpatialSearch', '{000D070B-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def SplitConnector(self, ConnectorToSplit=defaultNamedNotOptArg, Shape=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743892, LCID, 1, (9, 0), ((9, 1), (9, 1)),ConnectorToSplit
			, Shape)
		if ret is not None:
			ret = Dispatch(ret, 'SplitConnector', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def UniqueIDsToShapeIDs(self, GUIDs=defaultNamedNotOptArg, ShapeIDs=pythoncom.Missing):
		return self._ApplyTypes_(1610743879, 1, (24, 0), ((24584, 1), (24579, 2)), 'UniqueIDsToShapeIDs', None,GUIDs
			, ShapeIDs)

	def VisualBoundingBox(self, Flags=defaultNamedNotOptArg, lpr8Left=pythoncom.Missing, lpr8Bottom=pythoncom.Missing, lpr8Right=pythoncom.Missing
			, lpr8Top=pythoncom.Missing):
		return self._ApplyTypes_(1610743911, 1, (24, 0), ((2, 1), (16389, 2), (16389, 2), (16389, 2), (16389, 2)), 'VisualBoundingBox', None,Flags
			, lpr8Left, lpr8Bottom, lpr8Right, lpr8Top)

	def old_Paste(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def old_PasteSpecial(self, Format=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (24, 0), ((2, 1),),Format
			)

	_prop_map_get_ = {
		"AlternativeText": (1610743914, 2, (8, 0), (), "AlternativeText", None),
		# Method 'Application' returns object of type 'IVApplication'
		"Application": (1, 2, (9, 0), (), "Application", '{000D0700-0000-0000-C000-000000000046}'),
		"AutoSize": (1610743901, 2, (11, 0), (), "AutoSize", None),
		"BackPage": (37, 2, (12, 0), (), "BackPage", None),
		# Method 'BackPageAsObj' returns object of type 'IVPage'
		"BackPageAsObj": (14, 2, (9, 0), (), "BackPageAsObj", '{000D0709-0000-0000-C000-000000000046}'),
		"Background": (11, 2, (2, 0), (), "Background", None),
		# Method 'Comments' returns object of type 'IVComments'
		"Comments": (1610743907, 2, (9, 0), (), "Comments", '{000D0743-0000-0000-C000-000000000046}'),
		# Method 'Connects' returns object of type 'IVConnects'
		"Connects": (36, 2, (9, 0), (), "Connects", '{000D0704-0000-0000-C000-000000000046}'),
		# Method 'Document' returns object of type 'IVDocument'
		"Document": (13, 2, (9, 0), (), "Document", '{000D0705-0000-0000-C000-000000000046}'),
		# Method 'EventList' returns object of type 'IVEventList'
		"EventList": (23, 2, (9, 0), (), "EventList", '{000D071B-0000-0000-C000-000000000046}'),
		"ID": (42, 2, (3, 0), (), "ID", None),
		"ID16": (40, 2, (2, 0), (), "ID16", None),
		"Index": (4, 2, (2, 0), (), "Index", None),
		# Method 'Layers' returns object of type 'IVLayers'
		"Layers": (19, 2, (9, 0), (), "Layers", '{000D0713-0000-0000-C000-000000000046}'),
		"LayoutRoutePassive": (1610743897, 2, (11, 0), (), "LayoutRoutePassive", None),
		"Name": (0, 2, (8, 0), (), "Name", None),
		"NameU": (44, 2, (8, 0), (), "NameU", None),
		# Method 'OLEObjects' returns object of type 'IVOLEObjects'
		"OLEObjects": (41, 2, (9, 0), (), "OLEObjects", '{000D071E-0000-0000-C000-000000000046}'),
		"ObjectType": (3, 2, (2, 0), (), "ObjectType", None),
		# Method 'OriginalPage' returns object of type 'IVPage'
		"OriginalPage": (1610743874, 2, (9, 0), (), "OriginalPage", '{000D0709-0000-0000-C000-000000000046}'),
		# Method 'PageSheet' returns object of type 'IVShape'
		"PageSheet": (20, 2, (9, 0), (), "PageSheet", '{000D070C-0000-0000-C000-000000000046}'),
		"PersistsEvents": (24, 2, (2, 0), (), "PersistsEvents", None),
		# Method 'Picture' returns object of type 'Picture'
		"Picture": (1610743861, 2, (9, 0), (), "Picture", '{7BF80981-BF32-101A-8BBB-00AA00300CAB}'),
		"PrintTileCount": (1610743863, 2, (3, 0), (), "PrintTileCount", None),
		"ReviewerID": (1610743873, 2, (3, 0), (), "ReviewerID", None),
		# Method 'ShapeComments' returns object of type 'IVComments'
		"ShapeComments": (1610743908, 2, (9, 0), (), "ShapeComments", '{000D0743-0000-0000-C000-000000000046}'),
		# Method 'Shapes' returns object of type 'IVShapes'
		"Shapes": (5, 2, (9, 0), (), "Shapes", '{000D070D-0000-0000-C000-000000000046}'),
		"Stat": (2, 2, (2, 0), (), "Stat", None),
		"ThemeColors": (1610743882, 2, (12, 0), (), "ThemeColors", None),
		"ThemeEffects": (1610743884, 2, (12, 0), (), "ThemeEffects", None),
		"Title": (1610743912, 2, (8, 0), (), "Title", None),
		"Type": (1610743869, 2, (3, 0), (), "Type", None),
	}
	_prop_map_put_ = {
		"AlternativeText": ((1610743914, LCID, 4, 0),()),
		"AutoSize": ((1610743901, LCID, 4, 0),()),
		"BackPage": ((37, LCID, 4, 0),()),
		"BackPageFromName": ((1499, LCID, 4, 0),()),
		"Background": ((11, LCID, 4, 0),()),
		"Index": ((4, LCID, 4, 0),()),
		"LayoutRoutePassive": ((1610743897, LCID, 4, 0),()),
		"Name": ((0, LCID, 4, 0),()),
		"NameU": ((44, LCID, 4, 0),()),
		"ThemeColors": ((1610743882, LCID, 4, 0),()),
		"ThemeEffects": ((1610743884, LCID, 4, 0),()),
		"Title": ((1610743912, LCID, 4, 0),()),
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

win32com.client.CLSIDToClass.RegisterCLSID( "{000D0709-0000-0000-C000-000000000046}", IVPage )
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

IVPage_vtables_dispatch_ = 1
IVPage_vtables_ = [
	(( 'Document' , 'lpdispRet' , ), 13, (13, (), [ (16393, 10, None, "IID('{000D0705-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Application' , 'lpdispRet' , ), 1, (1, (), [ (16393, 10, None, "IID('{000D0700-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Stat' , 'lpi2Ret' , ), 2, (2, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Background' , 'lpi2Ret' , ), 11, (11, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Background' , 'lpi2Ret' , ), 11, (11, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'old_Paste' , ), 10, (10, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 64 , )),
	(( 'old_PasteSpecial' , 'Format' , ), 16, (16, (), [ (2, 1, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 64 , )),
	(( 'ObjectType' , 'lpi2Ret' , ), 3, (3, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DrawLine' , 'xBegin' , 'yBegin' , 'xEnd' , 'yEnd' , 
			 'lpdispRet' , ), 6, (6, (), [ (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'DrawRectangle' , 'x1' , 'y1' , 'x2' , 'y2' , 
			 'lpdispRet' , ), 7, (7, (), [ (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'DrawOval' , 'x1' , 'y1' , 'x2' , 'y2' , 
			 'lpdispRet' , ), 8, (8, (), [ (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Index' , 'lpi2Ret' , ), 4, (4, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Name' , 'lpLocaleSpecificName' , ), 0, (0, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'Name' , 'lpLocaleSpecificName' , ), 0, (0, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'Shapes' , 'lpdispRet' , ), 5, (5, (), [ (16393, 10, None, "IID('{000D070D-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'Drop' , 'ObjectToDrop' , 'xPos' , 'yPos' , 'lpdispRet' , 
			 ), 9, (9, (), [ (13, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'AddGuide' , 'Type' , 'xPos' , 'yPos' , 'lpdispRet' , 
			 ), 12, (12, (), [ (2, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'BackPageAsObj' , 'lpdispRet' , ), 14, (14, (), [ (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 64 , )),
	(( 'BackPageFromName' , ), 1499, (1499, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 64 , )),
	(( 'Print' , ), 15, (15, (), [ ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'Import' , 'FileName' , 'lpdispRet' , ), 17, (17, (), [ (8, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'Export' , 'FileName' , ), 18, (18, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'Layers' , 'lpdispRet' , ), 19, (19, (), [ (16393, 10, None, "IID('{000D0713-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'PageSheet' , 'lpdispRet' , ), 20, (20, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'Delete' , 'fRenumberPages' , ), 21, (21, (), [ (2, 1, None, None) , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'CenterDrawing' , ), 22, (22, (), [ ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'EventList' , 'lpdispRet' , ), 23, (23, (), [ (16393, 10, None, "IID('{000D071B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'PersistsEvents' , 'lpboolRet' , ), 24, (24, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'DrawSpline' , 'xyArray' , 'Tolerance' , 'Flags' , 'lpdispRet' , 
			 ), 25, (25, (), [ (24581, 1, None, None) , (5, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'DrawBezier' , 'xyArray' , 'degree' , 'Flags' , 'lpdispRet' , 
			 ), 26, (26, (), [ (24581, 1, None, None) , (2, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'DrawPolyline' , 'xyArray' , 'Flags' , 'lpdispRet' , ), 27, (27, (), [ 
			 (24581, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'InsertFromFile' , 'FileName' , 'Flags' , 'lpdispRet' , ), 28, (28, (), [ 
			 (8, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'InsertObject' , 'ClassOrProgID' , 'Flags' , 'lpdispRet' , ), 29, (29, (), [ 
			 (8, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'OpenDrawWindow' , 'lpdispRet' , ), 30, (30, (), [ (16393, 10, None, "IID('{000D0710-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'DropMany' , 'ObjectsToInstance' , 'xyArray' , 'IDArray' , 'lpi2Ret' , 
			 ), 31, (31, (), [ (24588, 1, None, None) , (24581, 1, None, None) , (24578, 2, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'GetFormulas' , 'SID_SRCStream' , 'formulaArray' , ), 32, (32, (), [ (24578, 1, None, None) , 
			 (24588, 2, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'GetResults' , 'SID_SRCStream' , 'Flags' , 'UnitsNamesOrCodes' , 'resultArray' , 
			 ), 33, (33, (), [ (24578, 1, None, None) , (2, 1, None, None) , (24588, 1, None, None) , (24588, 2, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'SetFormulas' , 'SID_SRCStream' , 'formulaArray' , 'Flags' , 'lpi2Ret' , 
			 ), 34, (34, (), [ (24578, 1, None, None) , (24588, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'SetResults' , 'SID_SRCStream' , 'UnitsNamesOrCodes' , 'resultArray' , 'Flags' , 
			 'lpi2Ret' , ), 35, (35, (), [ (24578, 1, None, None) , (24588, 1, None, None) , (24588, 1, None, None) , 
			 (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'Connects' , 'lpdispRet' , ), 36, (36, (), [ (16393, 10, None, "IID('{000D0704-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'BackPage' , 'lpobjRet' , ), 37, (37, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'BackPage' , 'lpobjRet' , ), 37, (37, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'Layout' , ), 38, (38, (), [ ], 1 , 1 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'BoundingBox' , 'Flags' , 'lpr8Left' , 'lpr8Bottom' , 'lpr8Right' , 
			 'lpr8Top' , ), 39, (39, (), [ (2, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'ID16' , 'lpi2Ret' , ), 40, (40, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 64 , )),
	(( 'OLEObjects' , 'lpdispRet' , ), 41, (41, (), [ (16393, 10, None, "IID('{000D071E-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'ID' , 'lpi4Ret' , ), 42, (42, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'SpatialSearch' , 'x' , 'y' , 'Relation' , 'Tolerance' , 
			 'Flags' , 'lpdispRet' , ), 43, (43, (), [ (5, 1, None, None) , (5, 1, None, None) , 
			 (2, 1, None, None) , (5, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'NameU' , 'lpLocaleIndependentName' , ), 44, (44, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'NameU' , 'lpLocaleIndependentName' , ), 44, (44, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'DropManyU' , 'ObjectsToInstance' , 'xyArray' , 'IDArray' , 'lpi2Ret' , 
			 ), 45, (45, (), [ (24588, 1, None, None) , (24581, 1, None, None) , (24578, 2, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'GetFormulasU' , 'SID_SRCStream' , 'formulaArray' , ), 46, (46, (), [ (24578, 1, None, None) , 
			 (24588, 2, None, None) , ], 1 , 1 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'DrawNURBS' , 'degree' , 'Flags' , 'xyArray' , 'knots' , 
			 'weights' , 'lpdispRet' , ), 47, (47, (), [ (2, 1, None, None) , (2, 1, None, None) , 
			 (24581, 1, None, None) , (24581, 1, None, None) , (12, 17, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 1 , 472 , (3, 0, None, None) , 0 , )),
	(( 'Picture' , 'ppPictureDisp' , ), 1610743861, (1610743861, (), [ (16393, 10, None, "IID('{7BF80981-BF32-101A-8BBB-00AA00300CAB}')") , ], 1 , 2 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'Index' , 'lpi2Ret' , ), 4, (4, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 488 , (3, 0, None, None) , 0 , )),
	(( 'PrintTileCount' , 'pnCount' , ), 1610743863, (1610743863, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'PrintTile' , 'nTile' , ), 1610743864, (1610743864, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( 'ResizeToFitContents' , ), 1610743865, (1610743865, (), [ ], 1 , 1 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'Paste' , 'Flags' , ), 1610743866, (1610743866, (), [ (12, 17, None, None) , ], 1 , 1 , 4 , 1 , 520 , (3, 0, None, None) , 0 , )),
	(( 'PasteSpecial' , 'Format' , 'Link' , 'DisplayAsIcon' , ), 1610743867, (1610743867, (), [ 
			 (3, 1, None, None) , (12, 17, None, None) , (12, 17, None, None) , ], 1 , 1 , 4 , 2 , 528 , (3, 0, None, None) , 0 , )),
	(( 'CreateSelection' , 'SelType' , 'IterationMode' , 'Data' , 'ppSelection' , 
			 ), 1610743868, (1610743868, (), [ (3, 1, None, None) , (3, 49, '256', None) , (12, 17, None, None) , (16393, 10, None, "IID('{000D070B-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 1 , 536 , (3, 0, None, None) , 0 , )),
	(( 'Type' , 'pnPageType' , ), 1610743869, (1610743869, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 544 , (3, 0, None, None) , 0 , )),
	(( 'DrawArcByThreePoints' , 'xBegin' , 'yBegin' , 'xEnd' , 'yEnd' , 
			 'xControl' , 'yControl' , 'lpdispRet' , ), 1610743870, (1610743870, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 552 , (3, 0, None, None) , 0 , )),
	(( 'DrawQuarterArc' , 'xBegin' , 'yBegin' , 'xEnd' , 'yEnd' , 
			 'SweepFlag' , 'lpdispRet' , ), 1610743871, (1610743871, (), [ (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 560 , (3, 0, None, None) , 0 , )),
	(( 'DrawCircularArc' , 'xCenter' , 'yCenter' , 'Radius' , 'StartAngle' , 
			 'EndAngle' , 'lpdispRet' , ), 1610743872, (1610743872, (), [ (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (5, 49, '0.0', None) , (5, 49, '3.1415927410125732', None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 568 , (3, 0, None, None) , 0 , )),
	(( 'ReviewerID' , 'ReviewerID' , ), 1610743873, (1610743873, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'OriginalPage' , 'ppPage' , ), 1610743874, (1610743874, (), [ (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 584 , (3, 0, None, None) , 0 , )),
	(( 'GetShapesLinkedToData' , 'DataRecordsetID' , 'ShapeIDs' , ), 1610743875, (1610743875, (), [ (3, 1, None, None) , 
			 (24579, 2, None, None) , ], 1 , 1 , 4 , 0 , 592 , (3, 0, None, None) , 0 , )),
	(( 'GetShapesLinkedToDataRow' , 'DataRecordsetID' , 'DataRowID' , 'ShapeIDs' , ), 1610743876, (1610743876, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (24579, 2, None, None) , ], 1 , 1 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
	(( 'LinkShapesToDataRows' , 'DataRecordsetID' , 'DataRowIDs' , 'ShapeIDs' , 'ApplyDataGraphicAfterLink' , 
			 ), 1610743877, (1610743877, (), [ (3, 1, None, None) , (24579, 1, None, None) , (24579, 1, None, None) , (11, 49, 'True', None) , ], 1 , 1 , 4 , 0 , 608 , (3, 0, None, None) , 0 , )),
	(( 'ShapeIDsToUniqueIDs' , 'ShapeIDs' , 'UniqueIDArgs' , 'GUIDs' , ), 1610743878, (1610743878, (), [ 
			 (24579, 1, None, None) , (3, 1, None, None) , (24584, 2, None, None) , ], 1 , 1 , 4 , 0 , 616 , (3, 0, None, None) , 0 , )),
	(( 'UniqueIDsToShapeIDs' , 'GUIDs' , 'ShapeIDs' , ), 1610743879, (1610743879, (), [ (24584, 1, None, None) , 
			 (24579, 2, None, None) , ], 1 , 1 , 4 , 0 , 624 , (3, 0, None, None) , 0 , )),
	(( 'DropLinked' , 'ObjectToDrop' , 'x' , 'y' , 'DataRecordsetID' , 
			 'DataRowID' , 'ApplyDataGraphicAfterLink' , 'Shape' , ), 1610743880, (1610743880, (), [ (13, 1, None, None) , 
			 (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (11, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 632 , (3, 0, None, None) , 0 , )),
	(( 'DropManyLinkedU' , 'ObjectsToInstance' , 'XYs' , 'DataRecordsetID' , 'DataRowIDs' , 
			 'ApplyDataGraphicAfterLink' , 'ShapeIDs' , 'Ret' , ), 1610743881, (1610743881, (), [ (24588, 1, None, None) , 
			 (24581, 1, None, None) , (3, 1, None, None) , (24579, 1, None, None) , (11, 1, None, None) , (24579, 2, None, None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 640 , (3, 0, None, None) , 0 , )),
	(( 'ThemeColors' , 'pVar' , ), 1610743882, (1610743882, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 648 , (3, 0, None, None) , 0 , )),
	(( 'ThemeColors' , 'pVar' , ), 1610743882, (1610743882, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 656 , (3, 0, None, None) , 0 , )),
	(( 'ThemeEffects' , 'pVar' , ), 1610743884, (1610743884, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 664 , (3, 0, None, None) , 0 , )),
	(( 'ThemeEffects' , 'pVar' , ), 1610743884, (1610743884, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 672 , (3, 0, None, None) , 0 , )),
	(( 'DropConnected' , 'ObjectToDrop' , 'TargetShape' , 'PlacementDir' , 'Connector' , 
			 'DroppedShape' , ), 1610743886, (1610743886, (), [ (13, 1, None, None) , (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (3, 1, None, None) , 
			 (13, 49, 'None', None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 680 , (3, 0, None, None) , 0 , )),
	(( 'AutoConnectMany' , 'FromShapeIDs' , 'ToShapeIDs' , 'PlacementDirs' , 'Connector' , 
			 'ConnectCount' , ), 1610743887, (1610743887, (), [ (24579, 1, None, None) , (24579, 1, None, None) , (24579, 1, None, None) , 
			 (13, 49, 'None', None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 688 , (3, 0, None, None) , 0 , )),
	(( 'DropContainer' , 'ObjectToDrop' , 'TargetShapes' , 'DroppedShape' , ), 1610743888, (1610743888, (), [ 
			 (13, 1, None, None) , (13, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 696 , (3, 0, None, None) , 0 , )),
	(( 'LayoutIncremental' , 'AlignOrSpace' , 'AlignHorizontal' , 'AlignVertical' , 'SpaceHorizontal' , 
			 'SpaceVertical' , 'UnitsNameOrCode' , ), 1610743889, (1610743889, (), [ (3, 1, None, None) , (3, 1, None, None) , 
			 (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 704 , (3, 0, None, None) , 0 , )),
	(( 'LayoutChangeDirection' , 'Direction' , ), 1610743890, (1610743890, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 712 , (3, 0, None, None) , 0 , )),
	(( 'AvoidPageBreaks' , ), 1610743891, (1610743891, (), [ ], 1 , 1 , 4 , 0 , 720 , (3, 0, None, None) , 0 , )),
	(( 'SplitConnector' , 'ConnectorToSplit' , 'Shape' , 'NewConnector' , ), 1610743892, (1610743892, (), [ 
			 (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 728 , (3, 0, None, None) , 0 , )),
	(( 'DropCallout' , 'ObjectToDrop' , 'TargetShape' , 'DroppedShape' , ), 1610743893, (1610743893, (), [ 
			 (13, 1, None, None) , (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 736 , (3, 0, None, None) , 0 , )),
	(( 'PasteToLocation' , 'xPos' , 'yPos' , 'Flags' , ), 1610743894, (1610743894, (), [ 
			 (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 744 , (3, 0, None, None) , 0 , )),
	(( 'GetContainers' , 'NestedOptions' , 'pContainersList' , ), 1610743895, (1610743895, (), [ (3, 1, None, None) , 
			 (24579, 10, None, None) , ], 1 , 1 , 4 , 0 , 752 , (3, 0, None, None) , 0 , )),
	(( 'GetCallouts' , 'NestedOptions' , 'pCalloutsList' , ), 1610743896, (1610743896, (), [ (3, 1, None, None) , 
			 (24579, 10, None, None) , ], 1 , 1 , 4 , 0 , 760 , (3, 0, None, None) , 0 , )),
	(( 'LayoutRoutePassive' , 'pbRet' , ), 1610743897, (1610743897, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 768 , (3, 0, None, None) , 0 , )),
	(( 'LayoutRoutePassive' , 'pbRet' , ), 1610743897, (1610743897, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 776 , (3, 0, None, None) , 0 , )),
	(( 'DropLegend' , 'OuterList' , 'InnerContainer' , 'populateFlags' , 'ppRet' , 
			 ), 1610743899, (1610743899, (), [ (13, 1, None, None) , (13, 1, None, None) , (3, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 784 , (3, 0, None, None) , 0 , )),
	(( 'DropIntoList' , 'ObjectToDrop' , 'TargetList' , 'lPosition' , 'ppRet' , 
			 ), 1610743900, (1610743900, (), [ (13, 1, None, None) , (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (3, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 792 , (3, 0, None, None) , 0 , )),
	(( 'AutoSize' , 'pbRet' , ), 1610743901, (1610743901, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 800 , (3, 0, None, None) , 0 , )),
	(( 'AutoSize' , 'pbRet' , ), 1610743901, (1610743901, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 808 , (3, 0, None, None) , 0 , )),
	(( 'AutoSizeDrawing' , ), 1610743903, (1610743903, (), [ ], 1 , 1 , 4 , 0 , 816 , (3, 0, None, None) , 0 , )),
	(( 'Duplicate' , 'ppPage' , ), 1610743904, (1610743904, (), [ (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 824 , (3, 0, None, None) , 0 , )),
	(( 'GetTheme' , 'eThemeType' , 'pVar' , ), 1610743905, (1610743905, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 832 , (3, 0, None, None) , 0 , )),
	(( 'SetTheme' , 'varThemeIndex' , 'varColorScheme' , 'varEffectScheme' , 'varConnectorScheme' , 
			 'varFontScheme' , ), 1610743906, (1610743906, (), [ (12, 1, None, None) , (12, 17, None, None) , (12, 17, None, None) , 
			 (12, 17, None, None) , (12, 17, None, None) , ], 1 , 1 , 4 , 4 , 840 , (3, 0, None, None) , 0 , )),
	(( 'Comments' , 'ppComments' , ), 1610743907, (1610743907, (), [ (16393, 10, None, "IID('{000D0743-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 848 , (3, 0, None, None) , 0 , )),
	(( 'ShapeComments' , 'ppComments' , ), 1610743908, (1610743908, (), [ (16393, 10, None, "IID('{000D0743-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 856 , (3, 0, None, None) , 0 , )),
	(( 'GetThemeVariant' , 'pVariantColor' , 'pVariantStyle' , 'pEmbellishment' , ), 1610743909, (1610743909, (), [ 
			 (16386, 2, None, None) , (16386, 2, None, None) , (16386, 50, '0', None) , ], 1 , 1 , 4 , 0 , 864 , (3, 0, None, None) , 0 , )),
	(( 'SetThemeVariant' , 'variantColor' , 'variantStyle' , 'embellishment' , ), 1610743910, (1610743910, (), [ 
			 (2, 1, None, None) , (2, 1, None, None) , (2, 49, '-1', None) , ], 1 , 1 , 4 , 0 , 872 , (3, 0, None, None) , 0 , )),
	(( 'VisualBoundingBox' , 'Flags' , 'lpr8Left' , 'lpr8Bottom' , 'lpr8Right' , 
			 'lpr8Top' , ), 1610743911, (1610743911, (), [ (2, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 880 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'pTitle' , ), 1610743912, (1610743912, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 888 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'pTitle' , ), 1610743912, (1610743912, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 896 , (3, 0, None, None) , 0 , )),
	(( 'AlternativeText' , 'pAlternativeText' , ), 1610743914, (1610743914, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 904 , (3, 0, None, None) , 0 , )),
	(( 'AlternativeText' , 'pAlternativeText' , ), 1610743914, (1610743914, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 912 , (3, 0, None, None) , 0 , )),
	(( 'AddDataVisualization' , 'DataRecordsetID' , 'ObjectToDrop' , 'Shape' , ), 1610743916, (1610743916, (), [ 
			 (3, 1, None, None) , (13, 17, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 920 , (3, 0, None, None) , 0 , )),
	(( 'CreateDataVisualizerDiagram' , 'szConnectionString' , 'szQueryString' , 'ObjectToDrop' , 'pDataVisualizerSettings' , 
			 'bConfirmSettings' , 'Shape' , ), 1610743917, (1610743917, (), [ (8, 49, "''", None) , (8, 49, "''", None) , 
			 (13, 17, None, None) , (9, 17, None, "IID('{000D074A-0000-0000-C000-000000000046}')") , (11, 17, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 928 , (3, 32, None, None) , 0 , )),
]

win32com.client.CLSIDToClass.RegisterCLSID( "{000D0709-0000-0000-C000-000000000046}", IVPage )
