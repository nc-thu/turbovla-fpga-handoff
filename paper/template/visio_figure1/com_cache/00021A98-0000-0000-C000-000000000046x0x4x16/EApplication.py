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

class EApplication:
	'Visio Application Event Interface'
	CLSID = CLSID_Sink = IID('{000D0B00-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{00021A20-0000-0000-C000-000000000046}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		     4097 : "OnAppActivated",
		     4098 : "OnAppDeactivated",
		     4100 : "OnAppObjActivated",
		     4104 : "OnAppObjDeactivated",
		     4112 : "OnBeforeQuit",
		     4128 : "OnBeforeModal",
		     4160 : "OnAfterModal",
		    32769 : "OnWindowOpened",
		      701 : "OnSelectionChanged",
		    16385 : "OnBeforeWindowClosed",
		     4224 : "OnWindowActivated",
		      702 : "OnBeforeWindowSelDelete",
		      703 : "OnBeforeWindowPageTurn",
		      704 : "OnWindowTurnedToPage",
		        2 : "OnDocumentOpened",
		        1 : "OnDocumentCreated",
		        3 : "OnDocumentSaved",
		        4 : "OnDocumentSavedAs",
		     8194 : "OnDocumentChanged",
		    16386 : "OnBeforeDocumentClose",
		    32772 : "OnStyleAdded",
		     8196 : "OnStyleChanged",
		    16388 : "OnBeforeStyleDelete",
		    32776 : "OnMasterAdded",
		     8200 : "OnMasterChanged",
		    16392 : "OnBeforeMasterDelete",
		    32784 : "OnPageAdded",
		     8208 : "OnPageChanged",
		    16400 : "OnBeforePageDelete",
		    32832 : "OnShapeAdded",
		      901 : "OnBeforeSelectionDelete",
		     8256 : "OnShapeChanged",
		      902 : "OnSelectionAdded",
		    16448 : "OnBeforeShapeDelete",
		     8320 : "OnTextChanged",
		    10240 : "OnCellChanged",
		     4352 : "OnMarkerEvent",
		     4608 : "OnNoEventsPending",
		     5120 : "OnVisioIsIdle",
		      200 : "OnMustFlushScopeBeginning",
		      201 : "OnMustFlushScopeEnded",
		        5 : "OnRunModeEntered",
		        6 : "OnDesignModeEntered",
		        7 : "OnBeforeDocumentSave",
		        8 : "OnBeforeDocumentSaveAs",
		    12288 : "OnFormulaChanged",
		    33024 : "OnConnectionsAdded",
		    16640 : "OnConnectionsDeleted",
		      202 : "OnEnterScope",
		      203 : "OnExitScope",
		      204 : "OnQueryCancelQuit",
		      205 : "OnQuitCanceled",
		     8193 : "OnWindowChanged",
		      705 : "OnViewChanged",
		      706 : "OnQueryCancelWindowClose",
		      707 : "OnWindowCloseCanceled",
		        9 : "OnQueryCancelDocumentClose",
		       10 : "OnDocumentCloseCanceled",
		      300 : "OnQueryCancelStyleDelete",
		      301 : "OnStyleDeleteCanceled",
		      400 : "OnQueryCancelMasterDelete",
		      401 : "OnMasterDeleteCanceled",
		      500 : "OnQueryCancelPageDelete",
		      501 : "OnPageDeleteCanceled",
		      802 : "OnShapeParentChanged",
		      803 : "OnBeforeShapeTextEdit",
		      804 : "OnShapeExitedTextEdit",
		      903 : "OnQueryCancelSelectionDelete",
		      904 : "OnSelectionDeleteCanceled",
		      905 : "OnQueryCancelUngroup",
		      906 : "OnUngroupCanceled",
		      907 : "OnQueryCancelConvertToGroup",
		      908 : "OnConvertToGroupCanceled",
		      206 : "OnQueryCancelSuspend",
		      207 : "OnSuspendCanceled",
		      208 : "OnBeforeSuspend",
		      209 : "OnAfterResume",
		      708 : "OnKeystrokeMessageForAddon",
		      709 : "OnMouseDown",
		      710 : "OnMouseMove",
		      711 : "OnMouseUp",
		      712 : "OnKeyDown",
		      713 : "OnKeyPress",
		      714 : "OnKeyUp",
		      210 : "OnQueryCancelSuspendEvents",
		      211 : "OnSuspendEventsCanceled",
		      212 : "OnBeforeSuspendEvents",
		      213 : "OnAfterResumeEvents",
		      909 : "OnQueryCancelGroup",
		      910 : "OnGroupCanceled",
		      807 : "OnShapeDataGraphicChanged",
		    16416 : "OnBeforeDataRecordsetDelete",
		     8224 : "OnDataRecordsetChanged",
		    32800 : "OnDataRecordsetAdded",
		      805 : "OnShapeLinkAdded",
		      806 : "OnShapeLinkDeleted",
		       11 : "OnAfterRemoveHiddenInformation",
		      502 : "OnContainerRelationshipAdded",
		      503 : "OnContainerRelationshipDeleted",
		      504 : "OnCalloutRelationshipAdded",
		      505 : "OnCalloutRelationshipDeleted",
		       13 : "OnRuleSetValidated",
		      911 : "OnQueryCancelReplaceShapes",
		      912 : "OnReplaceShapesCanceled",
		      913 : "OnBeforeReplaceShapes",
		      914 : "OnAfterReplaceShapes",
		}

	def __init__(self, oobj = None):
		if oobj is None:
			self._olecp = None
		else:
			import win32com.server.util
			from win32com.server.policy import EventHandlerPolicy
			cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
			cp=cpc.FindConnectionPoint(self.CLSID_Sink)
			cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
			self._olecp,self._olecp_cookie = cp,cookie
	def __del__(self):
		try:
			self.close()
		except pythoncom.com_error:
			pass
	def close(self):
		if self._olecp is not None:
			cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
			cp.Unadvise(cookie)
	def _query_interface_(self, iid):
		import win32com.server.util
		if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

	# Event Handlers
	# If you create handlers, they should have the following prototypes:
#	def OnAppActivated(self, app=defaultNamedNotOptArg):
#	def OnAppDeactivated(self, app=defaultNamedNotOptArg):
#	def OnAppObjActivated(self, app=defaultNamedNotOptArg):
#	def OnAppObjDeactivated(self, app=defaultNamedNotOptArg):
#	def OnBeforeQuit(self, app=defaultNamedNotOptArg):
#	def OnBeforeModal(self, app=defaultNamedNotOptArg):
#	def OnAfterModal(self, app=defaultNamedNotOptArg):
#	def OnWindowOpened(self, Window=defaultNamedNotOptArg):
#	def OnSelectionChanged(self, Window=defaultNamedNotOptArg):
#	def OnBeforeWindowClosed(self, Window=defaultNamedNotOptArg):
#	def OnWindowActivated(self, Window=defaultNamedNotOptArg):
#	def OnBeforeWindowSelDelete(self, Window=defaultNamedNotOptArg):
#	def OnBeforeWindowPageTurn(self, Window=defaultNamedNotOptArg):
#	def OnWindowTurnedToPage(self, Window=defaultNamedNotOptArg):
#	def OnDocumentOpened(self, doc=defaultNamedNotOptArg):
#	def OnDocumentCreated(self, doc=defaultNamedNotOptArg):
#	def OnDocumentSaved(self, doc=defaultNamedNotOptArg):
#	def OnDocumentSavedAs(self, doc=defaultNamedNotOptArg):
#	def OnDocumentChanged(self, doc=defaultNamedNotOptArg):
#	def OnBeforeDocumentClose(self, doc=defaultNamedNotOptArg):
#	def OnStyleAdded(self, Style=defaultNamedNotOptArg):
#	def OnStyleChanged(self, Style=defaultNamedNotOptArg):
#	def OnBeforeStyleDelete(self, Style=defaultNamedNotOptArg):
#	def OnMasterAdded(self, Master=defaultNamedNotOptArg):
#	def OnMasterChanged(self, Master=defaultNamedNotOptArg):
#	def OnBeforeMasterDelete(self, Master=defaultNamedNotOptArg):
#	def OnPageAdded(self, Page=defaultNamedNotOptArg):
#	def OnPageChanged(self, Page=defaultNamedNotOptArg):
#	def OnBeforePageDelete(self, Page=defaultNamedNotOptArg):
#	def OnShapeAdded(self, Shape=defaultNamedNotOptArg):
#	def OnBeforeSelectionDelete(self, Selection=defaultNamedNotOptArg):
#	def OnShapeChanged(self, Shape=defaultNamedNotOptArg):
#	def OnSelectionAdded(self, Selection=defaultNamedNotOptArg):
#	def OnBeforeShapeDelete(self, Shape=defaultNamedNotOptArg):
#	def OnTextChanged(self, Shape=defaultNamedNotOptArg):
#	def OnCellChanged(self, Cell=defaultNamedNotOptArg):
#		"Fires after a cell's value changes."
#	def OnMarkerEvent(self, app=defaultNamedNotOptArg, SequenceNum=defaultNamedNotOptArg, ContextString=defaultNamedNotOptArg):
#	def OnNoEventsPending(self, app=defaultNamedNotOptArg):
#	def OnVisioIsIdle(self, app=defaultNamedNotOptArg):
#	def OnMustFlushScopeBeginning(self, app=defaultNamedNotOptArg):
#	def OnMustFlushScopeEnded(self, app=defaultNamedNotOptArg):
#	def OnRunModeEntered(self, doc=defaultNamedNotOptArg):
#	def OnDesignModeEntered(self, doc=defaultNamedNotOptArg):
#	def OnBeforeDocumentSave(self, doc=defaultNamedNotOptArg):
#	def OnBeforeDocumentSaveAs(self, doc=defaultNamedNotOptArg):
#	def OnFormulaChanged(self, Cell=defaultNamedNotOptArg):
#		"Fires after a cell's formula changes."
#	def OnConnectionsAdded(self, Connects=defaultNamedNotOptArg):
#	def OnConnectionsDeleted(self, Connects=defaultNamedNotOptArg):
#	def OnEnterScope(self, app=defaultNamedNotOptArg, nScopeID=defaultNamedNotOptArg, bstrDescription=defaultNamedNotOptArg):
#	def OnExitScope(self, app=defaultNamedNotOptArg, nScopeID=defaultNamedNotOptArg, bstrDescription=defaultNamedNotOptArg, bErrOrCancelled=defaultNamedNotOptArg):
#	def OnQueryCancelQuit(self, app=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel terminate of application? T:Yes F:No'
#	def OnQuitCanceled(self, app=defaultNamedNotOptArg):
#		'Terminate application operation was canceled.'
#	def OnWindowChanged(self, Window=defaultNamedNotOptArg):
#		"Fires after a window's size or position changes"
#	def OnViewChanged(self, Window=defaultNamedNotOptArg):
#		'Fires after scroll or zoom in a drawing window'
#	def OnQueryCancelWindowClose(self, Window=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel close of window? T:Yes F:No'
#	def OnWindowCloseCanceled(self, Window=defaultNamedNotOptArg):
#		'Window close operation was canceled.'
#	def OnQueryCancelDocumentClose(self, doc=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel close of document? T:Yes F:No'
#	def OnDocumentCloseCanceled(self, doc=defaultNamedNotOptArg):
#		'Document close operation was canceled.'
#	def OnQueryCancelStyleDelete(self, Style=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel delete of style? T:Yes F:No'
#	def OnStyleDeleteCanceled(self, Style=defaultNamedNotOptArg):
#		'Delete style operation was canceled.'
#	def OnQueryCancelMasterDelete(self, Master=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel delete of master? T:Yes F:No'
#	def OnMasterDeleteCanceled(self, Master=defaultNamedNotOptArg):
#		'Delete master operation was canceled.'
#	def OnQueryCancelPageDelete(self, Page=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel delete of page? T:Yes F:No'
#	def OnPageDeleteCanceled(self, Page=defaultNamedNotOptArg):
#		'Delete page operation was canceled.'
#	def OnShapeParentChanged(self, Shape=defaultNamedNotOptArg):
#	def OnBeforeShapeTextEdit(self, Shape=defaultNamedNotOptArg):
#	def OnShapeExitedTextEdit(self, Shape=defaultNamedNotOptArg):
#	def OnQueryCancelSelectionDelete(self, Selection=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel delete of shapes? T:Yes F:No'
#	def OnSelectionDeleteCanceled(self, Selection=defaultNamedNotOptArg):
#		'Delete shapes operation was canceled.'
#	def OnQueryCancelUngroup(self, Selection=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel ungroup operation? T:Yes F:No'
#	def OnUngroupCanceled(self, Selection=defaultNamedNotOptArg):
#		'Ungroup operation was canceled.'
#	def OnQueryCancelConvertToGroup(self, Selection=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel convert to group operation? T:Yes F:No'
#	def OnConvertToGroupCanceled(self, Selection=defaultNamedNotOptArg):
#		'Convert to group operation was canceled.'
#	def OnQueryCancelSuspend(self, app=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel suspension of application? T:Yes F:No'
#	def OnSuspendCanceled(self, app=defaultNamedNotOptArg):
#		'Suspend application operation was canceled.'
#	def OnBeforeSuspend(self, app=defaultNamedNotOptArg):
#	def OnAfterResume(self, app=defaultNamedNotOptArg):
#	def OnKeystrokeMessageForAddon(self, MSG=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Called when keystroke message received for Addon window. True return indicates message was handled.'
#	def OnMouseDown(self, Button=defaultNamedNotOptArg, KeyButtonState=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg
#			, CancelDefault=defaultNamedNotOptArg):
#		'Called when mousedown message received for window. If you set CancelDefault to True then Visio will not process this message.'
#	def OnMouseMove(self, Button=defaultNamedNotOptArg, KeyButtonState=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg
#			, CancelDefault=defaultNamedNotOptArg):
#		'Called when mousemove message received for window. If you set CancelDefault to True then Visio will not process this message.'
#	def OnMouseUp(self, Button=defaultNamedNotOptArg, KeyButtonState=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg
#			, CancelDefault=defaultNamedNotOptArg):
#		'Called when mouseup message received for window. If you set CancelDefault to True then Visio will not process this message.'
#	def OnKeyDown(self, KeyCode=defaultNamedNotOptArg, KeyButtonState=defaultNamedNotOptArg, CancelDefault=defaultNamedNotOptArg):
#		'Called when keydown message received for window. If you set CancelDefault to True then Visio will not process this message.'
#	def OnKeyPress(self, KeyAscii=defaultNamedNotOptArg, CancelDefault=defaultNamedNotOptArg):
#		'Called when keypress message received for window. If you set CancelDefault to True then Visio will not process this message.'
#	def OnKeyUp(self, KeyCode=defaultNamedNotOptArg, KeyButtonState=defaultNamedNotOptArg, CancelDefault=defaultNamedNotOptArg):
#		'Called when keyup message received for window. If you set CancelDefault to True then Visio will not process this message.'
#	def OnQueryCancelSuspendEvents(self, app=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel suspension of application events? T:Yes F:No'
#	def OnSuspendEventsCanceled(self, app=defaultNamedNotOptArg):
#		'Suspend application events operation was canceled.'
#	def OnBeforeSuspendEvents(self, app=defaultNamedNotOptArg):
#	def OnAfterResumeEvents(self, app=defaultNamedNotOptArg):
#	def OnQueryCancelGroup(self, Selection=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel group operation? T:Yes F:No'
#	def OnGroupCanceled(self, Selection=defaultNamedNotOptArg):
#		'Group operation was canceled.'
#	def OnShapeDataGraphicChanged(self, Shape=defaultNamedNotOptArg):
#	def OnBeforeDataRecordsetDelete(self, DataRecordset=defaultNamedNotOptArg):
#	def OnDataRecordsetChanged(self, DataRecordsetChanged=defaultNamedNotOptArg):
#	def OnDataRecordsetAdded(self, DataRecordset=defaultNamedNotOptArg):
#	def OnShapeLinkAdded(self, Shape=defaultNamedNotOptArg, DataRecordsetID=defaultNamedNotOptArg, DataRowID=defaultNamedNotOptArg):
#	def OnShapeLinkDeleted(self, Shape=defaultNamedNotOptArg, DataRecordsetID=defaultNamedNotOptArg, DataRowID=defaultNamedNotOptArg):
#	def OnAfterRemoveHiddenInformation(self, doc=defaultNamedNotOptArg):
#	def OnContainerRelationshipAdded(self, ShapePair=defaultNamedNotOptArg):
#	def OnContainerRelationshipDeleted(self, ShapePair=defaultNamedNotOptArg):
#	def OnCalloutRelationshipAdded(self, ShapePair=defaultNamedNotOptArg):
#	def OnCalloutRelationshipDeleted(self, ShapePair=defaultNamedNotOptArg):
#	def OnRuleSetValidated(self, RuleSet=defaultNamedNotOptArg):
#	def OnQueryCancelReplaceShapes(self, replaceShapes=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#	def OnReplaceShapesCanceled(self, replaceShapes=defaultNamedNotOptArg):
#	def OnBeforeReplaceShapes(self, replaceShapes=defaultNamedNotOptArg):
#	def OnAfterReplaceShapes(self, sel=defaultNamedNotOptArg):


win32com.client.CLSIDToClass.RegisterCLSID( "{000D0B00-0000-0000-C000-000000000046}", EApplication )
