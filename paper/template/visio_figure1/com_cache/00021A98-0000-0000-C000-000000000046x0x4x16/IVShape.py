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
class IVShape(DispatchBaseClass):
	CLSID = IID('{000D070C-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{000D0A0A-0000-0000-C000-000000000046}')

	# Result is of type IVShape
	def AddGuide(self, Type=defaultNamedNotOptArg, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743967, LCID, 1, (9, 0), ((2, 1), (5, 1), (5, 1)),Type
			, xPos, yPos)
		if ret is not None:
			ret = Dispatch(ret, 'AddGuide', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVHyperlink
	def AddHyperlink(self):
		ret = self._oleobj_.InvokeTypes(106, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'AddHyperlink', '{000D071D-0000-0000-C000-000000000046}')
		return ret

	def AddNamedRow(self, Section=defaultNamedNotOptArg, RowName=defaultNamedNotOptArg, RowTag=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(71, LCID, 1, (2, 0), ((2, 1), (8, 1), (2, 1)),Section
			, RowName, RowTag)

	def AddRow(self, Section=defaultNamedNotOptArg, Row=defaultNamedNotOptArg, RowTag=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(27, LCID, 1, (2, 0), ((2, 1), (2, 1), (2, 1)),Section
			, Row, RowTag)

	def AddRows(self, Section=defaultNamedNotOptArg, Row=defaultNamedNotOptArg, RowTag=defaultNamedNotOptArg, RowCount=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(72, LCID, 1, (2, 0), ((2, 1), (2, 1), (2, 1), (2, 1)),Section
			, Row, RowTag, RowCount)

	def AddSection(self, Section=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(25, LCID, 1, (2, 0), ((2, 1),),Section
			)

	def AddToContainers(self):
		return self._oleobj_.InvokeTypes(1610743997, LCID, 1, (24, 0), (),)

	def AutoConnect(self, ToShape=defaultNamedNotOptArg, PlacementDir=defaultNamedNotOptArg, Connector=None):
		return self._oleobj_.InvokeTypes(1610743982, LCID, 1, (24, 0), ((9, 1), (3, 1), (13, 49)),ToShape
			, PlacementDir, Connector)

	def BoundingBox(self, Flags=defaultNamedNotOptArg, lpr8Left=pythoncom.Missing, lpr8Bottom=pythoncom.Missing, lpr8Right=pythoncom.Missing
			, lpr8Top=pythoncom.Missing):
		return self._ApplyTypes_(99, 1, (24, 0), ((2, 1), (16389, 2), (16389, 2), (16389, 2), (16389, 2)), 'BoundingBox', None,Flags
			, lpr8Left, lpr8Bottom, lpr8Right, lpr8Top)

	def BreakLinkToData(self, DataRecordsetID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743976, LCID, 1, (24, 0), ((3, 1),),DataRecordsetID
			)

	def BringForward(self):
		return self._oleobj_.InvokeTypes(46, LCID, 1, (24, 0), (),)

	def BringToFront(self):
		return self._oleobj_.InvokeTypes(47, LCID, 1, (24, 0), (),)

	# The method CellExists is actually a property, but must be used as a method to correctly pass the arguments
	def CellExists(self, localeSpecificCellName=defaultNamedNotOptArg, fExistsLocally=defaultNamedNotOptArg):
		'Returns whether this shape has cell with given locale specific name.'
		return self._oleobj_.InvokeTypes(67, LCID, 2, (2, 0), ((8, 1), (2, 1)),localeSpecificCellName
			, fExistsLocally)

	# The method CellExistsU is actually a property, but must be used as a method to correctly pass the arguments
	def CellExistsU(self, localeIndependentCellName=defaultNamedNotOptArg, fExistsLocally=defaultNamedNotOptArg):
		'Returns whether this shape has cell with given locale independent name.'
		return self._oleobj_.InvokeTypes(123, LCID, 2, (2, 0), ((8, 1), (2, 1)),localeIndependentCellName
			, fExistsLocally)

	# Result is of type IVCell
	# The method Cells is actually a property, but must be used as a method to correctly pass the arguments
	def Cells(self, localeSpecificCellName=defaultNamedNotOptArg):
		'Returns cell of this shape with given locale specific name.'
		ret = self._oleobj_.InvokeTypes(13, LCID, 2, (9, 0), ((8, 1),),localeSpecificCellName
			)
		if ret is not None:
			ret = Dispatch(ret, 'Cells', '{000D0701-0000-0000-C000-000000000046}')
		return ret

	# The method CellsRowIndex is actually a property, but must be used as a method to correctly pass the arguments
	def CellsRowIndex(self, localeSpecificCellName=defaultNamedNotOptArg):
		'Returns index of row of cell with given locale specific name.'
		return self._oleobj_.InvokeTypes(127, LCID, 2, (2, 0), ((8, 1),),localeSpecificCellName
			)

	# The method CellsRowIndexU is actually a property, but must be used as a method to correctly pass the arguments
	def CellsRowIndexU(self, localeIndependentCellName=defaultNamedNotOptArg):
		'Returns index of row of cell with given locale independent name.'
		return self._oleobj_.InvokeTypes(128, LCID, 2, (2, 0), ((8, 1),),localeIndependentCellName
			)

	# Result is of type IVCell
	# The method CellsSRC is actually a property, but must be used as a method to correctly pass the arguments
	def CellsSRC(self, Section=defaultNamedNotOptArg, Row=defaultNamedNotOptArg, Column=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 2, (9, 0), ((2, 1), (2, 1), (2, 1)),Section
			, Row, Column)
		if ret is not None:
			ret = Dispatch(ret, 'CellsSRC', '{000D0701-0000-0000-C000-000000000046}')
		return ret

	# The method CellsSRCExists is actually a property, but must be used as a method to correctly pass the arguments
	def CellsSRCExists(self, Section=defaultNamedNotOptArg, Row=defaultNamedNotOptArg, Column=defaultNamedNotOptArg, fExistsLocally=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(68, LCID, 2, (2, 0), ((2, 1), (2, 1), (2, 1), (2, 1)),Section
			, Row, Column, fExistsLocally)

	# Result is of type IVCell
	# The method CellsU is actually a property, but must be used as a method to correctly pass the arguments
	def CellsU(self, localeIndependentCellName=defaultNamedNotOptArg):
		'Returns cell of this shape with given locale independent name.'
		ret = self._oleobj_.InvokeTypes(121, LCID, 2, (9, 0), ((8, 1),),localeIndependentCellName
			)
		if ret is not None:
			ret = Dispatch(ret, 'CellsU', '{000D0701-0000-0000-C000-000000000046}')
		return ret

	def CenterDrawing(self):
		return self._oleobj_.InvokeTypes(83, LCID, 1, (24, 0), (),)

	def ChangePicture(self, FileName=defaultNamedNotOptArg, ChangePictureFlags=0):
		return self._oleobj_.InvokeTypes(1610744004, LCID, 1, (5, 0), ((8, 1), (3, 49)),FileName
			, ChangePictureFlags)

	def ConnectedShapes(self, Flags=defaultNamedNotOptArg, CategoryFilter=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610743989, 1, (8195, 0), ((3, 1), (8, 1)), 'ConnectedShapes', None,Flags
			, CategoryFilter)

	def ConvertToGroup(self):
		return self._oleobj_.InvokeTypes(48, LCID, 1, (24, 0), (),)

	def Copy(self, Flags=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743959, LCID, 1, (24, 0), ((12, 17),),Flags
			)

	# Result is of type IVSelection
	def CreateSelection(self, SelType=defaultNamedNotOptArg, IterationMode=256, Data=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(1610743963, LCID, 1, (9, 0), ((3, 1), (3, 49), (12, 17)),SelType
			, IterationMode, Data)
		if ret is not None:
			ret = Dispatch(ret, 'CreateSelection', '{000D070B-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVPage
	def CreateSubProcess(self):
		ret = self._oleobj_.InvokeTypes(1610743999, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateSubProcess', '{000D0709-0000-0000-C000-000000000046}')
		return ret

	def Cut(self, Flags=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743960, LCID, 1, (24, 0), ((12, 17),),Flags
			)

	def Delete(self):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (24, 0), (),)

	def DeleteEx(self, DelFlags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610744001, LCID, 1, (24, 0), ((3, 1),),DelFlags
			)

	def DeleteRow(self, Section=defaultNamedNotOptArg, Row=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(28, LCID, 1, (24, 0), ((2, 1), (2, 1)),Section
			, Row)

	def DeleteSection(self, Section=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(26, LCID, 1, (24, 0), ((2, 1),),Section
			)

	def Disconnect(self, ConnectorEnd=defaultNamedNotOptArg, OffsetX=defaultNamedNotOptArg, OffsetY=defaultNamedNotOptArg, Units=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743991, LCID, 1, (24, 0), ((3, 1), (5, 1), (5, 1), (3, 1)),ConnectorEnd
			, OffsetX, OffsetY, Units)

	# The method DistanceFrom is actually a property, but must be used as a method to correctly pass the arguments
	def DistanceFrom(self, OtherShape=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(112, LCID, 2, (5, 0), ((9, 1), (2, 1)),OtherShape
			, Flags)

	# Result is of type IVShape
	def DrawArcByThreePoints(self, xBegin=defaultNamedNotOptArg, yBegin=defaultNamedNotOptArg, xEnd=defaultNamedNotOptArg, yEnd=defaultNamedNotOptArg
			, xControl=defaultNamedNotOptArg, yControl=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743970, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1)),xBegin
			, yBegin, xEnd, yEnd, xControl, yControl
			)
		if ret is not None:
			ret = Dispatch(ret, 'DrawArcByThreePoints', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawBezier(self, xyArray=defaultNamedNotOptArg, degree=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(79, LCID, 1, (9, 0), ((24581, 1), (2, 1), (2, 1)),xyArray
			, degree, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'DrawBezier', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawCircularArc(self, xCenter=defaultNamedNotOptArg, yCenter=defaultNamedNotOptArg, Radius=defaultNamedNotOptArg, StartAngle=0.0
			, EndAngle=3.1415927410125732):
		ret = self._oleobj_.InvokeTypes(1610743972, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 49), (5, 49)),xCenter
			, yCenter, Radius, StartAngle, EndAngle)
		if ret is not None:
			ret = Dispatch(ret, 'DrawCircularArc', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawLine(self, xBegin=defaultNamedNotOptArg, yBegin=defaultNamedNotOptArg, xEnd=defaultNamedNotOptArg, yEnd=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(75, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1)),xBegin
			, yBegin, xEnd, yEnd)
		if ret is not None:
			ret = Dispatch(ret, 'DrawLine', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawNURBS(self, degree=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg, xyArray=defaultNamedNotOptArg, knots=defaultNamedNotOptArg
			, weights=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(126, LCID, 1, (9, 0), ((2, 1), (2, 1), (24581, 1), (24581, 1), (12, 17)),degree
			, Flags, xyArray, knots, weights)
		if ret is not None:
			ret = Dispatch(ret, 'DrawNURBS', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawOval(self, x1=defaultNamedNotOptArg, y1=defaultNamedNotOptArg, x2=defaultNamedNotOptArg, y2=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(77, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1)),x1
			, y1, x2, y2)
		if ret is not None:
			ret = Dispatch(ret, 'DrawOval', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawPolyline(self, xyArray=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(80, LCID, 1, (9, 0), ((24581, 1), (2, 1)),xyArray
			, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'DrawPolyline', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawQuarterArc(self, xBegin=defaultNamedNotOptArg, yBegin=defaultNamedNotOptArg, xEnd=defaultNamedNotOptArg, yEnd=defaultNamedNotOptArg
			, SweepFlag=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1610743971, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1), (3, 1)),xBegin
			, yBegin, xEnd, yEnd, SweepFlag)
		if ret is not None:
			ret = Dispatch(ret, 'DrawQuarterArc', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawRectangle(self, x1=defaultNamedNotOptArg, y1=defaultNamedNotOptArg, x2=defaultNamedNotOptArg, y2=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(76, LCID, 1, (9, 0), ((5, 1), (5, 1), (5, 1), (5, 1)),x1
			, y1, x2, y2)
		if ret is not None:
			ret = Dispatch(ret, 'DrawRectangle', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def DrawSpline(self, xyArray=defaultNamedNotOptArg, Tolerance=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(78, LCID, 1, (9, 0), ((24581, 1), (5, 1), (2, 1)),xyArray
			, Tolerance, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'DrawSpline', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def Drop(self, ObjectToDrop=defaultNamedNotOptArg, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(19, LCID, 1, (9, 0), ((13, 1), (5, 1), (5, 1)),ObjectToDrop
			, xPos, yPos)
		if ret is not None:
			ret = Dispatch(ret, 'Drop', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def DropMany(self, ObjectsToInstance=defaultNamedNotOptArg, xyArray=defaultNamedNotOptArg, IDArray=pythoncom.Missing):
		'Creates many shapes in this shape (if it is group). Names, if supplied, are considered locale specific.'
		return self._ApplyTypes_(92, 1, (2, 0), ((24588, 1), (24581, 1), (24578, 2)), 'DropMany', None,ObjectsToInstance
			, xyArray, IDArray)

	def DropManyU(self, ObjectsToInstance=defaultNamedNotOptArg, xyArray=defaultNamedNotOptArg, IDArray=pythoncom.Missing):
		'Creates many shapes in this shape (if it is group). Names, if supplied, are considered locale independent.'
		return self._ApplyTypes_(124, 1, (2, 0), ((24588, 1), (24581, 1), (24578, 2)), 'DropManyU', None,ObjectsToInstance
			, xyArray, IDArray)

	# Result is of type IVShape
	def Duplicate(self):
		'Returns the duplicated shape'
		ret = self._oleobj_.InvokeTypes(1610743955, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'Duplicate', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def Export(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(57, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	def FitCurve(self, Tolerance=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(81, LCID, 1, (24, 0), ((5, 1), (2, 1)),Tolerance
			, Flags)

	def FlipHorizontal(self):
		return self._oleobj_.InvokeTypes(49, LCID, 1, (24, 0), (),)

	def FlipVertical(self):
		return self._oleobj_.InvokeTypes(50, LCID, 1, (24, 0), (),)

	# The method GeomExIf is actually a property, but must be used as a method to correctly pass the arguments
	def GeomExIf(self, fFill=defaultNamedNotOptArg, LineRes=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(60, LCID, 2, (13, 0), ((2, 1), (5, 1)),fFill
			, LineRes)
		if ret is not None:
			# See if this IUnknown is really an IDispatch
			try:
				ret = ret.QueryInterface(pythoncom.IID_IDispatch)
			except pythoncom.error:
				return ret
			ret = Dispatch(ret, 'GeomExIf', None)
		return ret

	# The method GetAreaIU is actually a property, but must be used as a method to correctly pass the arguments
	def GetAreaIU(self, fIncludeSubShapes=False):
		return self._oleobj_.InvokeTypes(1610743968, LCID, 2, (5, 0), ((11, 49),),fIncludeSubShapes
			)

	def GetCustomPropertiesLinkedToData(self, DataRecordsetID=defaultNamedNotOptArg, CustomPropertyIndices=pythoncom.Missing):
		return self._ApplyTypes_(1610743979, 1, (24, 0), ((3, 1), (24579, 2)), 'GetCustomPropertiesLinkedToData', None,DataRecordsetID
			, CustomPropertyIndices)

	def GetCustomPropertyLinkedColumn(self, DataRecordsetID=defaultNamedNotOptArg, CustomPropertyIndex=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1610743981, LCID, 1, (8, 0), ((3, 1), (3, 1)),DataRecordsetID
			, CustomPropertyIndex)

	# The method GetDistanceFromPoint is actually a property, but must be used as a method to correctly pass the arguments
	def GetDistanceFromPoint(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg, pvPathIndex=pythoncom.Missing
			, pvCurveIndex=pythoncom.Missing, pvt=pythoncom.Missing):
		return self._ApplyTypes_(113, 2, (5, 0), ((5, 1), (5, 1), (2, 1), (16396, 18), (16396, 18), (16396, 18)), 'GetDistanceFromPoint', None,x
			, y, Flags, pvPathIndex, pvCurveIndex, pvt
			)

	def GetFormulas(self, SRCStream=defaultNamedNotOptArg, formulaArray=pythoncom.Missing):
		'Returns cell formulas in locale specific syntax.'
		return self._ApplyTypes_(93, 1, (24, 0), ((24578, 1), (24588, 2)), 'GetFormulas', None,SRCStream
			, formulaArray)

	def GetFormulasU(self, SRCStream=defaultNamedNotOptArg, formulaArray=pythoncom.Missing):
		'Returns cell formulas in locale independent syntax.'
		return self._ApplyTypes_(125, 1, (24, 0), ((24578, 1), (24588, 2)), 'GetFormulasU', None,SRCStream
			, formulaArray)

	# The method GetLengthIU is actually a property, but must be used as a method to correctly pass the arguments
	def GetLengthIU(self, fIncludeSubShapes=False):
		return self._oleobj_.InvokeTypes(1610743969, LCID, 2, (5, 0), ((11, 49),),fIncludeSubShapes
			)

	def GetLinkedDataRecordsetIDs(self, DataRecordsetIDs=pythoncom.Missing):
		return self._ApplyTypes_(1610743978, 1, (24, 0), ((24579, 2),), 'GetLinkedDataRecordsetIDs', None,DataRecordsetIDs
			)

	def GetLinkedDataRow(self, DataRecordsetID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743977, LCID, 1, (3, 0), ((3, 1),),DataRecordsetID
			)

	def GetResults(self, SRCStream=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg, UnitsNamesOrCodes=defaultNamedNotOptArg, resultArray=pythoncom.Missing):
		return self._ApplyTypes_(94, 1, (24, 0), ((24578, 1), (2, 1), (24588, 1), (24588, 2)), 'GetResults', None,SRCStream
			, Flags, UnitsNamesOrCodes, resultArray)

	def GluedShapes(self, Flags=defaultNamedNotOptArg, CategoryFilter=defaultNamedNotOptArg, pOtherConnectedShape=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610743990, 1, (8195, 0), ((3, 1), (8, 1), (9, 17)), 'GluedShapes', None,Flags
			, CategoryFilter, pOtherConnectedShape)

	# Result is of type IVShape
	def Group(self):
		'Returns the created group shape'
		ret = self._oleobj_.InvokeTypes(1610743954, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'Group', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def HasCategory(self, Category=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743987, LCID, 1, (11, 0), ((8, 1),),Category
			)

	def HitTest(self, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg, Tolerance=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(100, LCID, 1, (2, 0), ((5, 1), (5, 1), (5, 1)),xPos
			, yPos, Tolerance)

	# Result is of type IVShape
	def Import(self, FileName=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(82, LCID, 1, (9, 0), ((8, 1),),FileName
			)
		if ret is not None:
			ret = Dispatch(ret, 'Import', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def InsertFromFile(self, FileName=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(84, LCID, 1, (9, 0), ((8, 1), (2, 1)),FileName
			, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'InsertFromFile', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVShape
	def InsertObject(self, ClassOrProgID=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(85, LCID, 1, (9, 0), ((8, 1), (2, 1)),ClassOrProgID
			, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'InsertObject', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def IsCustomPropertyLinked(self, DataRecordsetID=defaultNamedNotOptArg, CustomPropertyIndex=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743980, LCID, 1, (11, 0), ((3, 1), (3, 1)),DataRecordsetID
			, CustomPropertyIndex)

	# Result is of type IVLayer
	# The method Layer is actually a property, but must be used as a method to correctly pass the arguments
	def Layer(self, Index=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(70, LCID, 2, (9, 0), ((2, 1),),Index
			)
		if ret is not None:
			ret = Dispatch(ret, 'Layer', '{000D0712-0000-0000-C000-000000000046}')
		return ret

	def Layout(self):
		return self._oleobj_.InvokeTypes(98, LCID, 1, (24, 0), (),)

	def LinkToData(self, DataRecordsetID=defaultNamedNotOptArg, RowID=defaultNamedNotOptArg, ApplyDataGraphicAfterLink=True):
		return self._oleobj_.InvokeTypes(1610743975, LCID, 1, (24, 0), ((3, 1), (3, 1), (11, 49)),DataRecordsetID
			, RowID, ApplyDataGraphicAfterLink)

	# Result is of type IVSelection
	def MoveToSubprocess(self, Page=defaultNamedNotOptArg, ObjectToDrop=defaultNamedNotOptArg, NewShape=0):
		return self._ApplyTypes_(1610744000, 1, (9, 0), ((9, 1), (13, 1), (16393, 50)), 'MoveToSubprocess', '{000D070B-0000-0000-C000-000000000046}',Page
			, ObjectToDrop, NewShape)

	def Offset(self, Distance=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743966, LCID, 1, (24, 0), ((5, 1),),Distance
			)

	# Result is of type IVWindow
	def OpenDrawWindow(self):
		ret = self._oleobj_.InvokeTypes(89, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'OpenDrawWindow', '{000D0710-0000-0000-C000-000000000046}')
		return ret

	# Result is of type IVWindow
	def OpenSheetWindow(self):
		ret = self._oleobj_.InvokeTypes(90, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'OpenSheetWindow', '{000D0710-0000-0000-C000-000000000046}')
		return ret

	def Paste(self, Flags=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743961, LCID, 1, (24, 0), ((12, 17),),Flags
			)

	def PasteSpecial(self, Format=defaultNamedNotOptArg, Link=defaultNamedOptArg, DisplayAsIcon=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1610743962, LCID, 1, (24, 0), ((3, 1), (12, 17), (12, 17)),Format
			, Link, DisplayAsIcon)

	def RemoveFromContainers(self):
		return self._oleobj_.InvokeTypes(1610743998, LCID, 1, (24, 0), (),)

	# Result is of type IVShape
	def ReplaceShape(self, MasterOrMasterShortcutToDrop=defaultNamedNotOptArg, ReplaceFlags=0):
		ret = self._oleobj_.InvokeTypes(1610744002, LCID, 1, (9, 0), ((13, 1), (3, 49)),MasterOrMasterShortcutToDrop
			, ReplaceFlags)
		if ret is not None:
			ret = Dispatch(ret, 'ReplaceShape', '{000D070C-0000-0000-C000-000000000046}')
		return ret

	def Resize(self, Direction=defaultNamedNotOptArg, Distance=defaultNamedNotOptArg, UnitCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610743996, LCID, 1, (24, 0), ((3, 1), (5, 1), (3, 1)),Direction
			, Distance, UnitCode)

	def ReverseEnds(self):
		return self._oleobj_.InvokeTypes(51, LCID, 1, (24, 0), (),)

	def Rotate90(self):
		return self._oleobj_.InvokeTypes(54, LCID, 1, (24, 0), (),)

	# The method RowCount is actually a property, but must be used as a method to correctly pass the arguments
	def RowCount(self, Section=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(24, LCID, 2, (2, 0), ((2, 1),),Section
			)

	# The method RowExists is actually a property, but must be used as a method to correctly pass the arguments
	def RowExists(self, Section=defaultNamedNotOptArg, Row=defaultNamedNotOptArg, fExistsLocally=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(66, LCID, 2, (2, 0), ((2, 1), (2, 1), (2, 1)),Section
			, Row, fExistsLocally)

	# The method RowType is actually a property, but must be used as a method to correctly pass the arguments
	def RowType(self, Section=defaultNamedNotOptArg, Row=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(30, LCID, 2, (2, 0), ((2, 1), (2, 1)),Section
			, Row)

	# The method RowsCellCount is actually a property, but must be used as a method to correctly pass the arguments
	def RowsCellCount(self, Section=defaultNamedNotOptArg, Row=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(29, LCID, 2, (2, 0), ((2, 1), (2, 1)),Section
			, Row)

	# Result is of type IVSection
	# The method Section is actually a property, but must be used as a method to correctly pass the arguments
	def Section(self, Index=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(109, LCID, 2, (9, 0), ((2, 1),),Index
			)
		if ret is not None:
			ret = Dispatch(ret, 'Section', '{000D0724-0000-0000-C000-000000000046}')
		return ret

	# The method SectionExists is actually a property, but must be used as a method to correctly pass the arguments
	def SectionExists(self, Section=defaultNamedNotOptArg, fExistsLocally=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(65, LCID, 2, (2, 0), ((2, 1), (2, 1)),Section
			, fExistsLocally)

	def SendBackward(self):
		return self._oleobj_.InvokeTypes(52, LCID, 1, (24, 0), (),)

	def SendToBack(self):
		return self._oleobj_.InvokeTypes(53, LCID, 1, (24, 0), (),)

	def SetBegin(self, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(32, LCID, 1, (24, 0), ((5, 1), (5, 1)),xPos
			, yPos)

	def SetCenter(self, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(31, LCID, 1, (24, 0), ((5, 1), (5, 1)),xPos
			, yPos)

	def SetEnd(self, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(33, LCID, 1, (24, 0), ((5, 1), (5, 1)),xPos
			, yPos)

	def SetFormulas(self, SRCStream=defaultNamedNotOptArg, formulaArray=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(95, LCID, 1, (2, 0), ((24578, 1), (24588, 1), (2, 1)),SRCStream
			, formulaArray, Flags)

	def SetQuickStyle(self, lineMatrix=defaultNamedNotOptArg, fillMatrix=defaultNamedNotOptArg, effectsMatrix=defaultNamedNotOptArg, fontMatrix=defaultNamedNotOptArg
			, lineColor=defaultNamedNotOptArg, fillColor=defaultNamedNotOptArg, shadowColor=defaultNamedNotOptArg, fontColor=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610744003, LCID, 1, (24, 0), ((3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1)),lineMatrix
			, fillMatrix, effectsMatrix, fontMatrix, lineColor, fillColor
			, shadowColor, fontColor)

	def SetResults(self, SRCStream=defaultNamedNotOptArg, UnitsNamesOrCodes=defaultNamedNotOptArg, resultArray=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(96, LCID, 1, (2, 0), ((24578, 1), (24588, 1), (24588, 1), (2, 1)),SRCStream
			, UnitsNamesOrCodes, resultArray, Flags)

	# The method SetRowType is actually a property, but must be used as a method to correctly pass the arguments
	def SetRowType(self, Section=defaultNamedNotOptArg, Row=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(30, LCID, 4, (24, 0), ((2, 1), (2, 1), (2, 1)),Section
			, Row, arg2)

	# Result is of type IVSelection
	# The method SpatialNeighbors is actually a property, but must be used as a method to correctly pass the arguments
	def SpatialNeighbors(self, Relation=defaultNamedNotOptArg, Tolerance=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg, ResultRoot=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(114, LCID, 2, (9, 0), ((2, 1), (5, 1), (2, 1), (12, 17)),Relation
			, Tolerance, Flags, ResultRoot)
		if ret is not None:
			ret = Dispatch(ret, 'SpatialNeighbors', '{000D070B-0000-0000-C000-000000000046}')
		return ret

	# The method SpatialRelation is actually a property, but must be used as a method to correctly pass the arguments
	def SpatialRelation(self, OtherShape=defaultNamedNotOptArg, Tolerance=defaultNamedNotOptArg, Flags=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(111, LCID, 2, (2, 0), ((9, 1), (5, 1), (2, 1)),OtherShape
			, Tolerance, Flags)

	# Result is of type IVSelection
	# The method SpatialSearch is actually a property, but must be used as a method to correctly pass the arguments
	def SpatialSearch(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, Relation=defaultNamedNotOptArg, Tolerance=defaultNamedNotOptArg
			, Flags=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(115, LCID, 2, (9, 0), ((5, 1), (5, 1), (2, 1), (5, 1), (2, 1)),x
			, y, Relation, Tolerance, Flags)
		if ret is not None:
			ret = Dispatch(ret, 'SpatialSearch', '{000D070B-0000-0000-C000-000000000046}')
		return ret

	def SwapEnds(self):
		'Performs end point and glue swapping on 1D shapes'
		return self._oleobj_.InvokeTypes(1610743956, LCID, 1, (24, 0), (),)

	def TransformXYFrom(self, OtherShape=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, xprime=pythoncom.Missing
			, yprime=pythoncom.Missing):
		return self._ApplyTypes_(117, 1, (24, 0), ((9, 1), (5, 1), (5, 1), (16389, 2), (16389, 2)), 'TransformXYFrom', None,OtherShape
			, x, y, xprime, yprime)

	def TransformXYTo(self, OtherShape=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, xprime=pythoncom.Missing
			, yprime=pythoncom.Missing):
		return self._ApplyTypes_(116, 1, (24, 0), ((9, 1), (5, 1), (5, 1), (16389, 2), (16389, 2)), 'TransformXYTo', None,OtherShape
			, x, y, xprime, yprime)

	def Ungroup(self):
		return self._oleobj_.InvokeTypes(55, LCID, 1, (24, 0), (),)

	# The method UniqueID is actually a property, but must be used as a method to correctly pass the arguments
	def UniqueID(self, fUniqueID=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(61, LCID, 2, (8, 0), ((2, 1),),fUniqueID
			)

	def UpdateAlignmentBox(self):
		return self._oleobj_.InvokeTypes(120, LCID, 1, (24, 0), (),)

	def VisualBoundingBox(self, Flags=defaultNamedNotOptArg, lpr8Left=pythoncom.Missing, lpr8Bottom=pythoncom.Missing, lpr8Right=pythoncom.Missing
			, lpr8Top=pythoncom.Missing):
		return self._ApplyTypes_(1610744006, 1, (24, 0), ((2, 1), (16389, 2), (16389, 2), (16389, 2), (16389, 2)), 'VisualBoundingBox', None,Flags
			, lpr8Left, lpr8Bottom, lpr8Right, lpr8Top)

	def VisualizeData(self, DataRecordsetID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610744013, LCID, 1, (24, 0), ((3, 1),),DataRecordsetID
			)

	def VoidDuplicate(self):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (24, 0), (),)

	def VoidGroup(self):
		return self._oleobj_.InvokeTypes(45, LCID, 1, (24, 0), (),)

	def XYFromPage(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, xprime=pythoncom.Missing, yprime=pythoncom.Missing):
		return self._ApplyTypes_(119, 1, (24, 0), ((5, 1), (5, 1), (16389, 2), (16389, 2)), 'XYFromPage', None,x
			, y, xprime, yprime)

	def XYToPage(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, xprime=pythoncom.Missing, yprime=pythoncom.Missing):
		return self._ApplyTypes_(118, 1, (24, 0), ((5, 1), (5, 1), (16389, 2), (16389, 2)), 'XYToPage', None,x
			, y, xprime, yprime)

	def old_Copy(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), (),)

	def old_Cut(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"AlternativeText": (1610744009, 2, (8, 0), (), "AlternativeText", None),
		# Method 'Application' returns object of type 'IVApplication'
		"Application": (1, 2, (9, 0), (), "Application", '{000D0700-0000-0000-C000-000000000046}'),
		"AreaIU": (1610743968, 2, (5, 0), ((11, 49),), "AreaIU", None),
		# Method 'CalloutTarget' returns object of type 'IVShape'
		"CalloutTarget": (1610743993, 2, (9, 0), (), "CalloutTarget", '{000D070C-0000-0000-C000-000000000046}'),
		"CalloutsAssociated": (1610743995, 2, (8195, 0), (), "CalloutsAssociated", None),
		"CharCount": (7, 2, (3, 0), (), "CharCount", None),
		# Method 'Characters' returns object of type 'IVCharacters'
		"Characters": (8, 2, (9, 0), (), "Characters", '{000D0702-0000-0000-C000-000000000046}'),
		"ClassID": (86, 2, (8, 0), (), "ClassID", None),
		# Method 'Comments' returns object of type 'IVComments'
		"Comments": (1610744005, 2, (9, 0), (), "Comments", '{000D0743-0000-0000-C000-000000000046}'),
		# Method 'Connects' returns object of type 'IVConnects'
		"Connects": (34, 2, (9, 0), (), "Connects", '{000D0704-0000-0000-C000-000000000046}'),
		# Method 'ContainerProperties' returns object of type 'IVContainerProperties'
		"ContainerProperties": (1610743986, 2, (9, 0), (), "ContainerProperties", '{000D0736-0000-0000-C000-000000000046}'),
		# Method 'ContainingMaster' returns object of type 'IVMaster'
		"ContainingMaster": (63, 2, (9, 0), (), "ContainingMaster", '{000D0707-0000-0000-C000-000000000046}'),
		"ContainingMasterID": (1610743974, 2, (3, 0), (), "ContainingMasterID", None),
		# Method 'ContainingPage' returns object of type 'IVPage'
		"ContainingPage": (62, 2, (9, 0), (), "ContainingPage", '{000D0709-0000-0000-C000-000000000046}'),
		"ContainingPageID": (1610743973, 2, (3, 0), (), "ContainingPageID", None),
		# Method 'ContainingShape' returns object of type 'IVShape'
		"ContainingShape": (64, 2, (9, 0), (), "ContainingShape", '{000D070C-0000-0000-C000-000000000046}'),
		"Data1": (15, 2, (8, 0), (), "Data1", None),
		"Data2": (16, 2, (8, 0), (), "Data2", None),
		"Data3": (17, 2, (8, 0), (), "Data3", None),
		# Method 'DataGraphic' returns object of type 'IVMaster'
		"DataGraphic": (1610743983, 2, (9, 0), (), "DataGraphic", '{000D0707-0000-0000-C000-000000000046}'),
		"DistanceFromPoint": (113, 2, (5, 0), ((5, 1), (5, 1), (2, 1), (16396, 18), (16396, 18), (16396, 18)), "DistanceFromPoint", None),
		# Method 'Document' returns object of type 'IVDocument'
		"Document": (44, 2, (9, 0), (), "Document", '{000D0705-0000-0000-C000-000000000046}'),
		# Method 'EventList' returns object of type 'IVEventList'
		"EventList": (73, 2, (9, 0), (), "EventList", '{000D071B-0000-0000-C000-000000000046}'),
		"FillStyle": (38, 2, (8, 0), (), "FillStyle", None),
		"ForeignData": (1610743958, 2, (8209, 0), (), "ForeignData", None),
		"ForeignType": (87, 2, (2, 0), (), "ForeignType", None),
		# Method 'FromConnects' returns object of type 'IVConnects'
		"FromConnects": (97, 2, (9, 0), (), "FromConnects", '{000D0704-0000-0000-C000-000000000046}'),
		"GeometryCount": (23, 2, (2, 0), (), "GeometryCount", None),
		"Help": (18, 2, (8, 0), (), "Help", None),
		# Method 'Hyperlink' returns object of type 'IVHyperlink'
		"Hyperlink": (101, 2, (9, 0), (), "Hyperlink", '{000D071D-0000-0000-C000-000000000046}'),
		# Method 'Hyperlinks' returns object of type 'IVHyperlinks'
		"Hyperlinks": (110, 2, (9, 0), (), "Hyperlinks", '{000D0723-0000-0000-C000-000000000046}'),
		"ID": (107, 2, (3, 0), (), "ID", None),
		"ID16": (91, 2, (2, 0), (), "ID16", None),
		"Index": (108, 2, (3, 0), (), "Index", None),
		"Index16": (35, 2, (2, 0), (), "Index16", None),
		"IsCallout": (1610743992, 2, (11, 0), (), "IsCallout", None),
		"IsDataGraphicCallout": (1610743985, 2, (11, 0), (), "IsDataGraphicCallout", None),
		"IsOpenForTextEdit": (129, 2, (11, 0), (), "IsOpenForTextEdit", None),
		"Language": (1610743964, 2, (3, 0), (), "Language", None),
		"LayerCount": (69, 2, (2, 0), (), "LayerCount", None),
		"LengthIU": (1610743969, 2, (5, 0), ((11, 49),), "LengthIU", None),
		"LineStyle": (37, 2, (8, 0), (), "LineStyle", None),
		# Method 'Master' returns object of type 'IVMaster'
		"Master": (21, 2, (9, 0), (), "Master", '{000D0707-0000-0000-C000-000000000046}'),
		# Method 'MasterShape' returns object of type 'IVShape'
		"MasterShape": (1610743952, 2, (9, 0), (), "MasterShape", '{000D070C-0000-0000-C000-000000000046}'),
		"MemberOfContainers": (1610743988, 2, (8195, 0), (), "MemberOfContainers", None),
		"Name": (0, 2, (8, 0), (), "Name", None),
		"NameID": (4, 2, (8, 0), (), "NameID", None),
		"NameU": (122, 2, (8, 0), (), "NameU", None),
		"NavigationIndex": (1610744011, 2, (3, 0), (), "NavigationIndex", None),
		"Object": (88, 2, (9, 0), (), "Object", None),
		"ObjectIsInherited": (103, 2, (2, 0), (), "ObjectIsInherited", None),
		"ObjectType": (3, 2, (2, 0), (), "ObjectType", None),
		"OneD": (22, 2, (2, 0), (), "OneD", None),
		"Parent": (56, 2, (9, 0), (), "Parent", None),
		# Method 'Paths' returns object of type 'IVPaths'
		"Paths": (104, 2, (9, 0), (), "Paths", '{000D0720-0000-0000-C000-000000000046}'),
		# Method 'PathsLocal' returns object of type 'IVPaths'
		"PathsLocal": (105, 2, (9, 0), (), "PathsLocal", '{000D0720-0000-0000-C000-000000000046}'),
		"PersistsEvents": (74, 2, (2, 0), (), "PersistsEvents", None),
		# Method 'Picture' returns object of type 'Picture'
		"Picture": (1610743953, 2, (9, 0), (), "Picture", '{7BF80981-BF32-101A-8BBB-00AA00300CAB}'),
		"ProgID": (102, 2, (8, 0), (), "ProgID", None),
		# Method 'RootShape' returns object of type 'IVShape'
		"RootShape": (1610743951, 2, (9, 0), (), "RootShape", '{000D070C-0000-0000-C000-000000000046}'),
		# Method 'Shapes' returns object of type 'IVShapes'
		"Shapes": (5, 2, (9, 0), (), "Shapes", '{000D070D-0000-0000-C000-000000000046}'),
		"Stat": (2, 2, (2, 0), (), "Stat", None),
		"Style": (36, 2, (8, 0), (), "Style", None),
		"Text": (6, 2, (8, 0), (), "Text", None),
		"TextStyle": (39, 2, (8, 0), (), "TextStyle", None),
		"Title": (1610744007, 2, (8, 0), (), "Title", None),
		"Type": (20, 2, (2, 0), (), "Type", None),
		"old_AreaIU": (58, 2, (5, 0), (), "old_AreaIU", None),
		"old_LengthIU": (59, 2, (5, 0), (), "old_LengthIU", None),
	}
	_prop_map_put_ = {
		"AlternativeText": ((1610744009, LCID, 4, 0),()),
		"CalloutTarget": ((1610743993, LCID, 4, 0),()),
		"Data1": ((15, LCID, 4, 0),()),
		"Data2": ((16, LCID, 4, 0),()),
		"Data3": ((17, LCID, 4, 0),()),
		"DataGraphic": ((1610743983, LCID, 4, 0),()),
		"FillStyle": ((38, LCID, 4, 0),()),
		"FillStyleKeepFmt": ((42, LCID, 4, 0),()),
		"Help": ((18, LCID, 4, 0),()),
		"Language": ((1610743964, LCID, 4, 0),()),
		"LineStyle": ((37, LCID, 4, 0),()),
		"LineStyleKeepFmt": ((41, LCID, 4, 0),()),
		"Name": ((0, LCID, 4, 0),()),
		"NameU": ((122, LCID, 4, 0),()),
		"NavigationIndex": ((1610744011, LCID, 4, 0),()),
		"OneD": ((22, LCID, 4, 0),()),
		"Parent": ((56, LCID, 4, 0),()),
		"Style": ((36, LCID, 4, 0),()),
		"StyleKeepFmt": ((40, LCID, 4, 0),()),
		"Text": ((6, LCID, 4, 0),()),
		"TextStyle": ((39, LCID, 4, 0),()),
		"TextStyleKeepFmt": ((43, LCID, 4, 0),()),
		"Title": ((1610744007, LCID, 4, 0),()),
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

win32com.client.CLSIDToClass.RegisterCLSID( "{000D070C-0000-0000-C000-000000000046}", IVShape )
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

IVShape_vtables_dispatch_ = 1
IVShape_vtables_ = [
	(( 'VoidGroup' , ), 45, (45, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 64 , )),
	(( 'BringForward' , ), 46, (46, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'BringToFront' , ), 47, (47, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'ConvertToGroup' , ), 48, (48, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'FlipHorizontal' , ), 49, (49, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'FlipVertical' , ), 50, (50, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'ReverseEnds' , ), 51, (51, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SendBackward' , ), 52, (52, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SendToBack' , ), 53, (53, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Rotate90' , ), 54, (54, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Ungroup' , ), 55, (55, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Document' , 'lpdispRet' , ), 44, (44, (), [ (16393, 10, None, "IID('{000D0705-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Parent' , 'lpdispRet' , ), 56, (56, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'Application' , 'lpdispRet' , ), 1, (1, (), [ (16393, 10, None, "IID('{000D0700-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'Stat' , 'lpi2Ret' , ), 2, (2, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'Master' , 'lpdispRet' , ), 21, (21, (), [ (16393, 10, None, "IID('{000D0707-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'Type' , 'lpi2Ret' , ), 20, (20, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'ObjectType' , 'lpi2Ret' , ), 3, (3, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'Cells' , 'localeSpecificCellName' , 'lpdispRet' , ), 13, (13, (), [ (8, 1, None, None) , 
			 (16393, 10, None, "IID('{000D0701-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'CellsSRC' , 'Section' , 'Row' , 'Column' , 'lpdispRet' , 
			 ), 14, (14, (), [ (2, 1, None, None) , (2, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D0701-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'Shapes' , 'lpdispRet' , ), 5, (5, (), [ (16393, 10, None, "IID('{000D070D-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'Data1' , 'lpbstrRet' , ), 15, (15, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'Data1' , 'lpbstrRet' , ), 15, (15, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'Data2' , 'lpbstrRet' , ), 16, (16, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'Data2' , 'lpbstrRet' , ), 16, (16, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'Data3' , 'lpbstrRet' , ), 17, (17, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'Data3' , 'lpbstrRet' , ), 17, (17, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'Help' , 'lpbstrRet' , ), 18, (18, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'Help' , 'lpbstrRet' , ), 18, (18, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'NameID' , 'lpLocaleIndependentName' , ), 4, (4, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'Name' , 'lpLocaleSpecificName' , ), 0, (0, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'Name' , 'lpLocaleSpecificName' , ), 0, (0, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'Text' , 'lpbstrRet' , ), 6, (6, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'Text' , 'lpbstrRet' , ), 6, (6, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'CharCount' , 'lpi4Ret' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'Characters' , 'lpdispRet' , ), 8, (8, (), [ (16393, 10, None, "IID('{000D0702-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'old_Copy' , ), 9, (9, (), [ ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 64 , )),
	(( 'old_Cut' , ), 10, (10, (), [ ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 64 , )),
	(( 'Delete' , ), 11, (11, (), [ ], 1 , 1 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'VoidDuplicate' , ), 12, (12, (), [ ], 1 , 1 , 4 , 0 , 368 , (3, 0, None, None) , 64 , )),
	(( 'Drop' , 'ObjectToDrop' , 'xPos' , 'yPos' , 'lpdispRet' , 
			 ), 19, (19, (), [ (13, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'OneD' , 'lpi2Ret' , ), 22, (22, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'OneD' , 'lpi2Ret' , ), 22, (22, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'GeometryCount' , 'lpi2Ret' , ), 23, (23, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'RowCount' , 'Section' , 'lpi2Ret' , ), 24, (24, (), [ (2, 1, None, None) , 
			 (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'AddSection' , 'Section' , 'lpi2Ret' , ), 25, (25, (), [ (2, 1, None, None) , 
			 (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'DeleteSection' , 'Section' , ), 26, (26, (), [ (2, 1, None, None) , ], 1 , 1 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'AddRow' , 'Section' , 'Row' , 'RowTag' , 'lpi2Ret' , 
			 ), 27, (27, (), [ (2, 1, None, None) , (2, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'DeleteRow' , 'Section' , 'Row' , ), 28, (28, (), [ (2, 1, None, None) , 
			 (2, 1, None, None) , ], 1 , 1 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'RowsCellCount' , 'Section' , 'Row' , 'lpi2Ret' , ), 29, (29, (), [ 
			 (2, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'RowType' , 'Section' , 'Row' , 'lpi2Ret' , ), 30, (30, (), [ 
			 (2, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'RowType' , 'Section' , 'Row' , 'lpi2Ret' , ), 30, (30, (), [ 
			 (2, 1, None, None) , (2, 1, None, None) , (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'SetCenter' , 'xPos' , 'yPos' , ), 31, (31, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 472 , (3, 0, None, None) , 0 , )),
	(( 'SetBegin' , 'xPos' , 'yPos' , ), 32, (32, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'SetEnd' , 'xPos' , 'yPos' , ), 33, (33, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 488 , (3, 0, None, None) , 0 , )),
	(( 'Connects' , 'lpdispRet' , ), 34, (34, (), [ (16393, 10, None, "IID('{000D0704-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'Index16' , 'lpi2Ret' , ), 35, (35, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 504 , (3, 0, None, None) , 64 , )),
	(( 'Style' , 'lpLocaleSpecificStyleName' , ), 36, (36, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'Style' , 'lpLocaleSpecificStyleName' , ), 36, (36, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( 'StyleKeepFmt' , ), 40, (40, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 528 , (3, 0, None, None) , 0 , )),
	(( 'LineStyle' , 'lpLocaleSpecificStyleName' , ), 37, (37, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 536 , (3, 0, None, None) , 0 , )),
	(( 'LineStyle' , 'lpLocaleSpecificStyleName' , ), 37, (37, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 544 , (3, 0, None, None) , 0 , )),
	(( 'LineStyleKeepFmt' , ), 41, (41, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 552 , (3, 0, None, None) , 0 , )),
	(( 'FillStyle' , 'lpLocaleSpecificStyleName' , ), 38, (38, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 560 , (3, 0, None, None) , 0 , )),
	(( 'FillStyle' , 'lpLocaleSpecificStyleName' , ), 38, (38, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 568 , (3, 0, None, None) , 0 , )),
	(( 'FillStyleKeepFmt' , ), 42, (42, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'TextStyle' , 'lpLocaleSpecificStyleName' , ), 39, (39, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 584 , (3, 0, None, None) , 0 , )),
	(( 'TextStyle' , 'lpLocaleSpecificStyleName' , ), 39, (39, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 592 , (3, 0, None, None) , 0 , )),
	(( 'TextStyleKeepFmt' , ), 43, (43, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
	(( 'Export' , 'FileName' , ), 57, (57, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 608 , (3, 0, None, None) , 0 , )),
	(( 'old_AreaIU' , 'lpr8Ret' , ), 58, (58, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 616 , (3, 0, None, None) , 64 , )),
	(( 'old_LengthIU' , 'lpr8Ret' , ), 59, (59, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 624 , (3, 0, None, None) , 64 , )),
	(( 'GeomExIf' , 'fFill' , 'LineRes' , 'lpunkRet' , ), 60, (60, (), [ 
			 (2, 1, None, None) , (5, 1, None, None) , (16397, 10, None, None) , ], 1 , 2 , 4 , 0 , 632 , (3, 0, None, None) , 64 , )),
	(( 'UniqueID' , 'fUniqueID' , 'lpbstrRet' , ), 61, (61, (), [ (2, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 640 , (3, 0, None, None) , 0 , )),
	(( 'ContainingPage' , 'lpdispRet' , ), 62, (62, (), [ (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 648 , (3, 0, None, None) , 0 , )),
	(( 'ContainingMaster' , 'lpdispRet' , ), 63, (63, (), [ (16393, 10, None, "IID('{000D0707-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 656 , (3, 0, None, None) , 0 , )),
	(( 'ContainingShape' , 'lpdispRet' , ), 64, (64, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 664 , (3, 0, None, None) , 0 , )),
	(( 'SectionExists' , 'Section' , 'fExistsLocally' , 'lpi2Ret' , ), 65, (65, (), [ 
			 (2, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 672 , (3, 0, None, None) , 0 , )),
	(( 'RowExists' , 'Section' , 'Row' , 'fExistsLocally' , 'lpi2Ret' , 
			 ), 66, (66, (), [ (2, 1, None, None) , (2, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 680 , (3, 0, None, None) , 0 , )),
	(( 'CellExists' , 'localeSpecificCellName' , 'fExistsLocally' , 'lpi2Ret' , ), 67, (67, (), [ 
			 (8, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 688 , (3, 0, None, None) , 0 , )),
	(( 'CellsSRCExists' , 'Section' , 'Row' , 'Column' , 'fExistsLocally' , 
			 'lpi2Ret' , ), 68, (68, (), [ (2, 1, None, None) , (2, 1, None, None) , (2, 1, None, None) , 
			 (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 696 , (3, 0, None, None) , 0 , )),
	(( 'LayerCount' , 'lpi2Ret' , ), 69, (69, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 704 , (3, 0, None, None) , 0 , )),
	(( 'Layer' , 'Index' , 'lpdispRet' , ), 70, (70, (), [ (2, 1, None, None) , 
			 (16393, 10, None, "IID('{000D0712-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 712 , (3, 0, None, None) , 0 , )),
	(( 'AddNamedRow' , 'Section' , 'RowName' , 'RowTag' , 'lpi2Ret' , 
			 ), 71, (71, (), [ (2, 1, None, None) , (8, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 720 , (3, 0, None, None) , 0 , )),
	(( 'AddRows' , 'Section' , 'Row' , 'RowTag' , 'RowCount' , 
			 'lpi2Ret' , ), 72, (72, (), [ (2, 1, None, None) , (2, 1, None, None) , (2, 1, None, None) , 
			 (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 728 , (3, 0, None, None) , 0 , )),
	(( 'EventList' , 'lpdispRet' , ), 73, (73, (), [ (16393, 10, None, "IID('{000D071B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 736 , (3, 0, None, None) , 0 , )),
	(( 'PersistsEvents' , 'lpboolRet' , ), 74, (74, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 744 , (3, 0, None, None) , 0 , )),
	(( 'DrawLine' , 'xBegin' , 'yBegin' , 'xEnd' , 'yEnd' , 
			 'lpdispRet' , ), 75, (75, (), [ (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 752 , (3, 0, None, None) , 0 , )),
	(( 'DrawRectangle' , 'x1' , 'y1' , 'x2' , 'y2' , 
			 'lpdispRet' , ), 76, (76, (), [ (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 760 , (3, 0, None, None) , 0 , )),
	(( 'DrawOval' , 'x1' , 'y1' , 'x2' , 'y2' , 
			 'lpdispRet' , ), 77, (77, (), [ (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 768 , (3, 0, None, None) , 0 , )),
	(( 'DrawSpline' , 'xyArray' , 'Tolerance' , 'Flags' , 'lpdispRet' , 
			 ), 78, (78, (), [ (24581, 1, None, None) , (5, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 776 , (3, 0, None, None) , 0 , )),
	(( 'DrawBezier' , 'xyArray' , 'degree' , 'Flags' , 'lpdispRet' , 
			 ), 79, (79, (), [ (24581, 1, None, None) , (2, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 784 , (3, 0, None, None) , 0 , )),
	(( 'DrawPolyline' , 'xyArray' , 'Flags' , 'lpdispRet' , ), 80, (80, (), [ 
			 (24581, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 792 , (3, 0, None, None) , 0 , )),
	(( 'FitCurve' , 'Tolerance' , 'Flags' , ), 81, (81, (), [ (5, 1, None, None) , 
			 (2, 1, None, None) , ], 1 , 1 , 4 , 0 , 800 , (3, 0, None, None) , 0 , )),
	(( 'Import' , 'FileName' , 'lpdispRet' , ), 82, (82, (), [ (8, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 808 , (3, 0, None, None) , 0 , )),
	(( 'CenterDrawing' , ), 83, (83, (), [ ], 1 , 1 , 4 , 0 , 816 , (3, 0, None, None) , 0 , )),
	(( 'InsertFromFile' , 'FileName' , 'Flags' , 'lpdispRet' , ), 84, (84, (), [ 
			 (8, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 824 , (3, 0, None, None) , 0 , )),
	(( 'InsertObject' , 'ClassOrProgID' , 'Flags' , 'lpdispRet' , ), 85, (85, (), [ 
			 (8, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 832 , (3, 0, None, None) , 0 , )),
	(( 'ClassID' , 'lpbstrRet' , ), 86, (86, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 840 , (3, 0, None, None) , 0 , )),
	(( 'ForeignType' , 'lpi2Ret' , ), 87, (87, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 848 , (3, 0, None, None) , 0 , )),
	(( 'Object' , 'lpdispRet' , ), 88, (88, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 856 , (3, 0, None, None) , 0 , )),
	(( 'OpenDrawWindow' , 'lpdispRet' , ), 89, (89, (), [ (16393, 10, None, "IID('{000D0710-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 864 , (3, 0, None, None) , 0 , )),
	(( 'OpenSheetWindow' , 'lpdispRet' , ), 90, (90, (), [ (16393, 10, None, "IID('{000D0710-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 872 , (3, 0, None, None) , 0 , )),
	(( 'ID16' , 'lpi2Ret' , ), 91, (91, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 880 , (3, 0, None, None) , 64 , )),
	(( 'DropMany' , 'ObjectsToInstance' , 'xyArray' , 'IDArray' , 'lpi2Ret' , 
			 ), 92, (92, (), [ (24588, 1, None, None) , (24581, 1, None, None) , (24578, 2, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 888 , (3, 0, None, None) , 0 , )),
	(( 'GetFormulas' , 'SRCStream' , 'formulaArray' , ), 93, (93, (), [ (24578, 1, None, None) , 
			 (24588, 2, None, None) , ], 1 , 1 , 4 , 0 , 896 , (3, 0, None, None) , 0 , )),
	(( 'GetResults' , 'SRCStream' , 'Flags' , 'UnitsNamesOrCodes' , 'resultArray' , 
			 ), 94, (94, (), [ (24578, 1, None, None) , (2, 1, None, None) , (24588, 1, None, None) , (24588, 2, None, None) , ], 1 , 1 , 4 , 0 , 904 , (3, 0, None, None) , 0 , )),
	(( 'SetFormulas' , 'SRCStream' , 'formulaArray' , 'Flags' , 'lpi2Ret' , 
			 ), 95, (95, (), [ (24578, 1, None, None) , (24588, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 912 , (3, 0, None, None) , 0 , )),
	(( 'SetResults' , 'SRCStream' , 'UnitsNamesOrCodes' , 'resultArray' , 'Flags' , 
			 'lpi2Ret' , ), 96, (96, (), [ (24578, 1, None, None) , (24588, 1, None, None) , (24588, 1, None, None) , 
			 (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 920 , (3, 0, None, None) , 0 , )),
	(( 'FromConnects' , 'lpdispRet' , ), 97, (97, (), [ (16393, 10, None, "IID('{000D0704-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 928 , (3, 0, None, None) , 0 , )),
	(( 'Layout' , ), 98, (98, (), [ ], 1 , 1 , 4 , 0 , 936 , (3, 0, None, None) , 0 , )),
	(( 'BoundingBox' , 'Flags' , 'lpr8Left' , 'lpr8Bottom' , 'lpr8Right' , 
			 'lpr8Top' , ), 99, (99, (), [ (2, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 944 , (3, 0, None, None) , 0 , )),
	(( 'HitTest' , 'xPos' , 'yPos' , 'Tolerance' , 'lpi2Ret' , 
			 ), 100, (100, (), [ (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 952 , (3, 0, None, None) , 0 , )),
	(( 'Hyperlink' , 'lpdispRet' , ), 101, (101, (), [ (16393, 10, None, "IID('{000D071D-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 960 , (3, 0, None, None) , 64 , )),
	(( 'ProgID' , 'lpbstrRet' , ), 102, (102, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 968 , (3, 0, None, None) , 0 , )),
	(( 'ObjectIsInherited' , 'lpboolRet' , ), 103, (103, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 976 , (3, 0, None, None) , 0 , )),
	(( 'Paths' , 'lpdispRet' , ), 104, (104, (), [ (16393, 10, None, "IID('{000D0720-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 984 , (3, 0, None, None) , 0 , )),
	(( 'PathsLocal' , 'lpdispRet' , ), 105, (105, (), [ (16393, 10, None, "IID('{000D0720-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 992 , (3, 0, None, None) , 0 , )),
	(( 'AddHyperlink' , 'lpdispRet' , ), 106, (106, (), [ (16393, 10, None, "IID('{000D071D-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1000 , (3, 0, None, None) , 0 , )),
	(( 'ID' , 'lpi4Ret' , ), 107, (107, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1008 , (3, 0, None, None) , 0 , )),
	(( 'Index' , 'lpi4Ret' , ), 108, (108, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1016 , (3, 0, None, None) , 0 , )),
	(( 'Section' , 'Index' , 'lpdispRet' , ), 109, (109, (), [ (2, 1, None, None) , 
			 (16393, 10, None, "IID('{000D0724-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1024 , (3, 0, None, None) , 0 , )),
	(( 'Hyperlinks' , 'lpdispRet' , ), 110, (110, (), [ (16393, 10, None, "IID('{000D0723-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1032 , (3, 0, None, None) , 0 , )),
	(( 'SpatialRelation' , 'OtherShape' , 'Tolerance' , 'Flags' , 'lpi2Ret' , 
			 ), 111, (111, (), [ (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (5, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 1040 , (3, 0, None, None) , 0 , )),
	(( 'DistanceFrom' , 'OtherShape' , 'Flags' , 'lpr8Ret' , ), 112, (112, (), [ 
			 (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (2, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 1048 , (3, 0, None, None) , 0 , )),
	(( 'DistanceFromPoint' , 'x' , 'y' , 'Flags' , 'pvPathIndex' , 
			 'pvCurveIndex' , 'pvt' , 'lpr8Ret' , ), 113, (113, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , (2, 1, None, None) , (16396, 18, None, None) , (16396, 18, None, None) , (16396, 18, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 3 , 1056 , (3, 0, None, None) , 0 , )),
	(( 'DistanceFromPoint' , 'x' , 'y' , 'Flags' , 'pvPathIndex' , 
			 'pvCurveIndex' , 'pvt' , 'lpr8Ret' , ), 113, (113, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , (2, 1, None, None) , (16396, 18, None, None) , (16396, 18, None, None) , (16396, 18, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 3 , 1056 , (3, 0, None, None) , 0 , )),
	(( 'SpatialNeighbors' , 'Relation' , 'Tolerance' , 'Flags' , 'ResultRoot' , 
			 'lpdispRet' , ), 114, (114, (), [ (2, 1, None, None) , (5, 1, None, None) , (2, 1, None, None) , 
			 (12, 17, None, None) , (16393, 10, None, "IID('{000D070B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 1 , 1064 , (3, 0, None, None) , 0 , )),
	(( 'SpatialSearch' , 'x' , 'y' , 'Relation' , 'Tolerance' , 
			 'Flags' , 'lpdispRet' , ), 115, (115, (), [ (5, 1, None, None) , (5, 1, None, None) , 
			 (2, 1, None, None) , (5, 1, None, None) , (2, 1, None, None) , (16393, 10, None, "IID('{000D070B-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1072 , (3, 0, None, None) , 0 , )),
	(( 'TransformXYTo' , 'OtherShape' , 'x' , 'y' , 'xprime' , 
			 'yprime' , ), 116, (116, (), [ (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (5, 1, None, None) , (5, 1, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 1080 , (3, 0, None, None) , 0 , )),
	(( 'TransformXYFrom' , 'OtherShape' , 'x' , 'y' , 'xprime' , 
			 'yprime' , ), 117, (117, (), [ (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (5, 1, None, None) , (5, 1, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 1088 , (3, 0, None, None) , 0 , )),
	(( 'XYToPage' , 'x' , 'y' , 'xprime' , 'yprime' , 
			 ), 118, (118, (), [ (5, 1, None, None) , (5, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 1096 , (3, 0, None, None) , 0 , )),
	(( 'XYFromPage' , 'x' , 'y' , 'xprime' , 'yprime' , 
			 ), 119, (119, (), [ (5, 1, None, None) , (5, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 1104 , (3, 0, None, None) , 0 , )),
	(( 'UpdateAlignmentBox' , ), 120, (120, (), [ ], 1 , 1 , 4 , 0 , 1112 , (3, 0, None, None) , 0 , )),
	(( 'CellsU' , 'localeIndependentCellName' , 'lpdispRet' , ), 121, (121, (), [ (8, 1, None, None) , 
			 (16393, 10, None, "IID('{000D0701-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1120 , (3, 0, None, None) , 0 , )),
	(( 'NameU' , 'lpLocaleIndependentName' , ), 122, (122, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1128 , (3, 0, None, None) , 0 , )),
	(( 'NameU' , 'lpLocaleIndependentName' , ), 122, (122, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1136 , (3, 0, None, None) , 0 , )),
	(( 'CellExistsU' , 'localeIndependentCellName' , 'fExistsLocally' , 'lpi2Ret' , ), 123, (123, (), [ 
			 (8, 1, None, None) , (2, 1, None, None) , (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 1144 , (3, 0, None, None) , 0 , )),
	(( 'DropManyU' , 'ObjectsToInstance' , 'xyArray' , 'IDArray' , 'lpi2Ret' , 
			 ), 124, (124, (), [ (24588, 1, None, None) , (24581, 1, None, None) , (24578, 2, None, None) , (16386, 10, None, None) , ], 1 , 1 , 4 , 0 , 1152 , (3, 0, None, None) , 0 , )),
	(( 'GetFormulasU' , 'SRCStream' , 'formulaArray' , ), 125, (125, (), [ (24578, 1, None, None) , 
			 (24588, 2, None, None) , ], 1 , 1 , 4 , 0 , 1160 , (3, 0, None, None) , 0 , )),
	(( 'DrawNURBS' , 'degree' , 'Flags' , 'xyArray' , 'knots' , 
			 'weights' , 'lpdispRet' , ), 126, (126, (), [ (2, 1, None, None) , (2, 1, None, None) , 
			 (24581, 1, None, None) , (24581, 1, None, None) , (12, 17, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 1 , 1168 , (3, 0, None, None) , 0 , )),
	(( 'CellsRowIndex' , 'localeSpecificCellName' , 'lpi2Ret' , ), 127, (127, (), [ (8, 1, None, None) , 
			 (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 1176 , (3, 0, None, None) , 0 , )),
	(( 'CellsRowIndexU' , 'localeIndependentCellName' , 'lpi2Ret' , ), 128, (128, (), [ (8, 1, None, None) , 
			 (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 1184 , (3, 0, None, None) , 0 , )),
	(( 'IsOpenForTextEdit' , 'pbOpenForTextEdit' , ), 129, (129, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1192 , (3, 0, None, None) , 0 , )),
	(( 'RootShape' , 'ppRootShape' , ), 1610743951, (1610743951, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1200 , (3, 0, None, None) , 0 , )),
	(( 'MasterShape' , 'ppMasterShape' , ), 1610743952, (1610743952, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1208 , (3, 0, None, None) , 0 , )),
	(( 'Picture' , 'ppPictureDisp' , ), 1610743953, (1610743953, (), [ (16393, 10, None, "IID('{7BF80981-BF32-101A-8BBB-00AA00300CAB}')") , ], 1 , 2 , 4 , 0 , 1216 , (3, 0, None, None) , 0 , )),
	(( 'Group' , 'ppShape' , ), 1610743954, (1610743954, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1224 , (3, 0, None, None) , 0 , )),
	(( 'Duplicate' , 'ppShape' , ), 1610743955, (1610743955, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1232 , (3, 0, None, None) , 0 , )),
	(( 'SwapEnds' , ), 1610743956, (1610743956, (), [ ], 1 , 1 , 4 , 0 , 1240 , (3, 0, None, None) , 0 , )),
	(( 'Parent' , 'lpdispRet' , ), 56, (56, (), [ (9, 1, None, None) , ], 1 , 4 , 4 , 0 , 1248 , (3, 0, None, None) , 0 , )),
	(( 'ForeignData' , 'pData' , ), 1610743958, (1610743958, (), [ (24593, 10, None, None) , ], 1 , 2 , 4 , 0 , 1256 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'Flags' , ), 1610743959, (1610743959, (), [ (12, 17, None, None) , ], 1 , 1 , 4 , 1 , 1264 , (3, 0, None, None) , 0 , )),
	(( 'Cut' , 'Flags' , ), 1610743960, (1610743960, (), [ (12, 17, None, None) , ], 1 , 1 , 4 , 1 , 1272 , (3, 0, None, None) , 0 , )),
	(( 'Paste' , 'Flags' , ), 1610743961, (1610743961, (), [ (12, 17, None, None) , ], 1 , 1 , 4 , 1 , 1280 , (3, 0, None, None) , 0 , )),
	(( 'PasteSpecial' , 'Format' , 'Link' , 'DisplayAsIcon' , ), 1610743962, (1610743962, (), [ 
			 (3, 1, None, None) , (12, 17, None, None) , (12, 17, None, None) , ], 1 , 1 , 4 , 2 , 1288 , (3, 0, None, None) , 0 , )),
	(( 'CreateSelection' , 'SelType' , 'IterationMode' , 'Data' , 'ppSelection' , 
			 ), 1610743963, (1610743963, (), [ (3, 1, None, None) , (3, 49, '256', None) , (12, 17, None, None) , (16393, 10, None, "IID('{000D070B-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 1 , 1296 , (3, 0, None, None) , 0 , )),
	(( 'Language' , 'lpLangID' , ), 1610743964, (1610743964, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1304 , (3, 0, None, None) , 0 , )),
	(( 'Language' , 'lpLangID' , ), 1610743964, (1610743964, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1312 , (3, 0, None, None) , 0 , )),
	(( 'Offset' , 'Distance' , ), 1610743966, (1610743966, (), [ (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 1320 , (3, 0, None, None) , 0 , )),
	(( 'AddGuide' , 'Type' , 'xPos' , 'yPos' , 'lpdispRet' , 
			 ), 1610743967, (1610743967, (), [ (2, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1328 , (3, 0, None, None) , 0 , )),
	(( 'AreaIU' , 'fIncludeSubShapes' , 'lpr8Ret' , ), 1610743968, (1610743968, (), [ (11, 49, 'False', None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 1336 , (3, 0, None, None) , 0 , )),
	(( 'AreaIU' , 'fIncludeSubShapes' , 'lpr8Ret' , ), 1610743968, (1610743968, (), [ (11, 49, 'False', None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 1336 , (3, 0, None, None) , 0 , )),
	(( 'LengthIU' , 'fIncludeSubShapes' , 'lpr8Ret' , ), 1610743969, (1610743969, (), [ (11, 49, 'False', None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 1344 , (3, 0, None, None) , 0 , )),
	(( 'LengthIU' , 'fIncludeSubShapes' , 'lpr8Ret' , ), 1610743969, (1610743969, (), [ (11, 49, 'False', None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 1344 , (3, 0, None, None) , 0 , )),
	(( 'DrawArcByThreePoints' , 'xBegin' , 'yBegin' , 'xEnd' , 'yEnd' , 
			 'xControl' , 'yControl' , 'lpdispRet' , ), 1610743970, (1610743970, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1352 , (3, 0, None, None) , 0 , )),
	(( 'DrawQuarterArc' , 'xBegin' , 'yBegin' , 'xEnd' , 'yEnd' , 
			 'SweepFlag' , 'lpdispRet' , ), 1610743971, (1610743971, (), [ (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1360 , (3, 0, None, None) , 0 , )),
	(( 'DrawCircularArc' , 'xCenter' , 'yCenter' , 'Radius' , 'StartAngle' , 
			 'EndAngle' , 'lpdispRet' , ), 1610743972, (1610743972, (), [ (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (5, 49, '0.0', None) , (5, 49, '3.1415927410125732', None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1368 , (3, 0, None, None) , 0 , )),
	(( 'ContainingPageID' , 'lpi4Ret' , ), 1610743973, (1610743973, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1376 , (3, 0, None, None) , 0 , )),
	(( 'ContainingMasterID' , 'lpi4Ret' , ), 1610743974, (1610743974, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1384 , (3, 0, None, None) , 0 , )),
	(( 'LinkToData' , 'DataRecordsetID' , 'RowID' , 'ApplyDataGraphicAfterLink' , ), 1610743975, (1610743975, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (11, 49, 'True', None) , ], 1 , 1 , 4 , 0 , 1392 , (3, 0, None, None) , 0 , )),
	(( 'BreakLinkToData' , 'DataRecordsetID' , ), 1610743976, (1610743976, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 1400 , (3, 0, None, None) , 0 , )),
	(( 'GetLinkedDataRow' , 'DataRecordsetID' , 'DataRowID' , ), 1610743977, (1610743977, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 1408 , (3, 0, None, None) , 0 , )),
	(( 'GetLinkedDataRecordsetIDs' , 'DataRecordsetIDs' , ), 1610743978, (1610743978, (), [ (24579, 2, None, None) , ], 1 , 1 , 4 , 0 , 1416 , (3, 0, None, None) , 0 , )),
	(( 'GetCustomPropertiesLinkedToData' , 'DataRecordsetID' , 'CustomPropertyIndices' , ), 1610743979, (1610743979, (), [ (3, 1, None, None) , 
			 (24579, 2, None, None) , ], 1 , 1 , 4 , 0 , 1424 , (3, 0, None, None) , 0 , )),
	(( 'IsCustomPropertyLinked' , 'DataRecordsetID' , 'CustomPropertyIndex' , 'Status' , ), 1610743980, (1610743980, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 1432 , (3, 0, None, None) , 0 , )),
	(( 'GetCustomPropertyLinkedColumn' , 'DataRecordsetID' , 'CustomPropertyIndex' , 'ColumnName' , ), 1610743981, (1610743981, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 1440 , (3, 0, None, None) , 0 , )),
	(( 'AutoConnect' , 'ToShape' , 'PlacementDir' , 'Connector' , ), 1610743982, (1610743982, (), [ 
			 (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (3, 1, None, None) , (13, 49, 'None', None) , ], 1 , 1 , 4 , 0 , 1448 , (3, 0, None, None) , 0 , )),
	(( 'DataGraphic' , 'DataGraphic' , ), 1610743983, (1610743983, (), [ (16393, 10, None, "IID('{000D0707-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1456 , (3, 0, None, None) , 0 , )),
	(( 'DataGraphic' , 'DataGraphic' , ), 1610743983, (1610743983, (), [ (9, 1, None, "IID('{000D0707-0000-0000-C000-000000000046}')") , ], 1 , 4 , 4 , 0 , 1464 , (3, 0, None, None) , 0 , )),
	(( 'IsDataGraphicCallout' , 'pbDataGraphicCallout' , ), 1610743985, (1610743985, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1472 , (3, 0, None, None) , 0 , )),
	(( 'ContainerProperties' , 'pContainerProps' , ), 1610743986, (1610743986, (), [ (16393, 10, None, "IID('{000D0736-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1480 , (3, 0, None, None) , 0 , )),
	(( 'HasCategory' , 'Category' , 'pbHasCategory' , ), 1610743987, (1610743987, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 1488 , (3, 0, None, None) , 0 , )),
	(( 'MemberOfContainers' , 'pContainedByList' , ), 1610743988, (1610743988, (), [ (24579, 10, None, None) , ], 1 , 2 , 4 , 0 , 1496 , (3, 0, None, None) , 0 , )),
	(( 'ConnectedShapes' , 'Flags' , 'CategoryFilter' , 'pConnectedList' , ), 1610743989, (1610743989, (), [ 
			 (3, 1, None, None) , (8, 1, None, None) , (24579, 10, None, None) , ], 1 , 1 , 4 , 0 , 1504 , (3, 0, None, None) , 0 , )),
	(( 'GluedShapes' , 'Flags' , 'CategoryFilter' , 'pOtherConnectedShape' , 'pConnectorList' , 
			 ), 1610743990, (1610743990, (), [ (3, 1, None, None) , (8, 1, None, None) , (9, 17, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , (24579, 10, None, None) , ], 1 , 1 , 4 , 0 , 1512 , (3, 0, None, None) , 0 , )),
	(( 'Disconnect' , 'ConnectorEnd' , 'OffsetX' , 'OffsetY' , 'Units' , 
			 ), 1610743991, (1610743991, (), [ (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 1520 , (3, 0, None, None) , 0 , )),
	(( 'IsCallout' , 'pbRet' , ), 1610743992, (1610743992, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1528 , (3, 0, None, None) , 0 , )),
	(( 'CalloutTarget' , 'pCalloutShape' , ), 1610743993, (1610743993, (), [ (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1536 , (3, 0, None, None) , 0 , )),
	(( 'CalloutTarget' , 'pCalloutShape' , ), 1610743993, (1610743993, (), [ (9, 1, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 4 , 4 , 0 , 1544 , (3, 0, None, None) , 0 , )),
	(( 'CalloutsAssociated' , 'pAssociatedCallouts' , ), 1610743995, (1610743995, (), [ (24579, 10, None, None) , ], 1 , 2 , 4 , 0 , 1552 , (3, 0, None, None) , 0 , )),
	(( 'Resize' , 'Direction' , 'Distance' , 'UnitCode' , ), 1610743996, (1610743996, (), [ 
			 (3, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 1560 , (3, 0, None, None) , 0 , )),
	(( 'AddToContainers' , ), 1610743997, (1610743997, (), [ ], 1 , 1 , 4 , 0 , 1568 , (3, 0, None, None) , 0 , )),
	(( 'RemoveFromContainers' , ), 1610743998, (1610743998, (), [ ], 1 , 1 , 4 , 0 , 1576 , (3, 0, None, None) , 0 , )),
	(( 'CreateSubProcess' , 'Page' , ), 1610743999, (1610743999, (), [ (16393, 10, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1584 , (3, 0, None, None) , 0 , )),
	(( 'MoveToSubprocess' , 'Page' , 'ObjectToDrop' , 'NewShape' , 'NewSelection' , 
			 ), 1610744000, (1610744000, (), [ (9, 1, None, "IID('{000D0709-0000-0000-C000-000000000046}')") , (13, 1, None, None) , (16393, 50, '0', "IID('{000D070C-0000-0000-C000-000000000046}')") , (16393, 10, None, "IID('{000D070B-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1592 , (3, 0, None, None) , 0 , )),
	(( 'DeleteEx' , 'DelFlags' , ), 1610744001, (1610744001, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 1600 , (3, 0, None, None) , 0 , )),
	(( 'ReplaceShape' , 'MasterOrMasterShortcutToDrop' , 'ReplaceFlags' , 'NewShape' , ), 1610744002, (1610744002, (), [ 
			 (13, 1, None, None) , (3, 49, '0', None) , (16393, 10, None, "IID('{000D070C-0000-0000-C000-000000000046}')") , ], 1 , 1 , 4 , 0 , 1608 , (3, 0, None, None) , 0 , )),
	(( 'SetQuickStyle' , 'lineMatrix' , 'fillMatrix' , 'effectsMatrix' , 'fontMatrix' , 
			 'lineColor' , 'fillColor' , 'shadowColor' , 'fontColor' , ), 1610744003, (1610744003, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			 (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 1616 , (3, 0, None, None) , 0 , )),
	(( 'ChangePicture' , 'FileName' , 'ChangePictureFlags' , 'lprAspectRatio' , ), 1610744004, (1610744004, (), [ 
			 (8, 1, None, None) , (3, 49, '0', None) , (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 1624 , (3, 0, None, None) , 0 , )),
	(( 'Comments' , 'ppComments' , ), 1610744005, (1610744005, (), [ (16393, 10, None, "IID('{000D0743-0000-0000-C000-000000000046}')") , ], 1 , 2 , 4 , 0 , 1632 , (3, 0, None, None) , 0 , )),
	(( 'VisualBoundingBox' , 'Flags' , 'lpr8Left' , 'lpr8Bottom' , 'lpr8Right' , 
			 'lpr8Top' , ), 1610744006, (1610744006, (), [ (2, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 1640 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'pTitle' , ), 1610744007, (1610744007, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1648 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'pTitle' , ), 1610744007, (1610744007, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1656 , (3, 0, None, None) , 0 , )),
	(( 'AlternativeText' , 'pAlternativeText' , ), 1610744009, (1610744009, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1664 , (3, 0, None, None) , 0 , )),
	(( 'AlternativeText' , 'pAlternativeText' , ), 1610744009, (1610744009, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1672 , (3, 0, None, None) , 0 , )),
	(( 'NavigationIndex' , 'lpIndex' , ), 1610744011, (1610744011, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 1680 , (3, 0, None, None) , 0 , )),
	(( 'NavigationIndex' , 'lpIndex' , ), 1610744011, (1610744011, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 1688 , (3, 0, None, None) , 0 , )),
	(( 'VisualizeData' , 'DataRecordsetID' , ), 1610744013, (1610744013, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 1696 , (3, 0, None, None) , 0 , )),
]

win32com.client.CLSIDToClass.RegisterCLSID( "{000D070C-0000-0000-C000-000000000046}", IVShape )
