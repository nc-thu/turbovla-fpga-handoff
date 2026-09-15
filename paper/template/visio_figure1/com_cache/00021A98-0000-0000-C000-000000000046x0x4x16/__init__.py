# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.11.5 | packaged by Anaconda, Inc. | (main, Sep 11 2023, 13:26:23) [MSC v.1916 64 bit (AMD64)]
# From type library '{00021A98-0000-0000-C000-000000000046}'
# On Sat Sep 12 14:27:35 2026
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

class constants:
	visArcSweepFlagConcave        =0          # from enum VisArcSweepFlags
	visArcSweepFlagConvex         =1          # from enum VisArcSweepFlags
	visAutoConnectDirDown         =2          # from enum VisAutoConnectDir
	visAutoConnectDirLeft         =3          # from enum VisAutoConnectDir
	visAutoConnectDirNone         =0          # from enum VisAutoConnectDir
	visAutoConnectDirRight        =4          # from enum VisAutoConnectDir
	visAutoConnectDirUp           =1          # from enum VisAutoConnectDir
	visAutoLinkDontReplaceExistingLinks=16         # from enum VisAutoLinkBehaviors
	visAutoLinkGenericProgressBar =2          # from enum VisAutoLinkBehaviors
	visAutoLinkIncludeHiddenProps =64         # from enum VisAutoLinkBehaviors
	visAutoLinkNoApplyDataGraphic =4          # from enum VisAutoLinkBehaviors
	visAutoLinkNullMatchesNoFormula=32         # from enum VisAutoLinkBehaviors
	visAutoLinkReplaceExistingLinks=8          # from enum VisAutoLinkBehaviors
	visAutoLinkSelectedShapesOnly =1          # from enum VisAutoLinkBehaviors
	visAutoLinkCustPropsLabel     =2          # from enum VisAutoLinkFieldTypes
	visAutoLinkGeometryAngle      =4          # from enum VisAutoLinkFieldTypes
	visAutoLinkGeometryHeight     =6          # from enum VisAutoLinkFieldTypes
	visAutoLinkGeometryWidth      =5          # from enum VisAutoLinkFieldTypes
	visAutoLinkMasterName         =8          # from enum VisAutoLinkFieldTypes
	visAutoLinkMasterNameU        =16         # from enum VisAutoLinkFieldTypes
	visAutoLinkObjectData1        =11         # from enum VisAutoLinkFieldTypes
	visAutoLinkObjectData2        =12         # from enum VisAutoLinkFieldTypes
	visAutoLinkObjectData3        =13         # from enum VisAutoLinkFieldTypes
	visAutoLinkObjectID           =7          # from enum VisAutoLinkFieldTypes
	visAutoLinkObjectName         =9          # from enum VisAutoLinkFieldTypes
	visAutoLinkObjectNameU        =17         # from enum VisAutoLinkFieldTypes
	visAutoLinkObjectType         =10         # from enum VisAutoLinkFieldTypes
	visAutoLinkPropRowNameU       =14         # from enum VisAutoLinkFieldTypes
	visAutoLinkShapeText          =1          # from enum VisAutoLinkFieldTypes
	visAutoLinkUserRowName        =3          # from enum VisAutoLinkFieldTypes
	visAutoLinkUserRowNameU       =15         # from enum VisAutoLinkFieldTypes
	visBBoxDrawingCoords          =8192       # from enum VisBoundingBoxArgs
	visBBoxExtents                =4          # from enum VisBoundingBoxArgs
	visBBoxIgnoreVisible          =32         # from enum VisBoundingBoxArgs
	visBBoxIncludeDataGraphics    =64         # from enum VisBoundingBoxArgs
	visBBoxIncludeGuides          =4096       # from enum VisBoundingBoxArgs
	visBBoxIncludeHidden          =16         # from enum VisBoundingBoxArgs
	visBBoxNoNonPrint             =16384      # from enum VisBoundingBoxArgs
	visBBoxUprightText            =2          # from enum VisBoundingBoxArgs
	visBBoxUprightWH              =1          # from enum VisBoundingBoxArgs
	visBuiltInStencilBackgrounds  =0          # from enum VisBuiltInStencilTypes
	visBuiltInStencilBorders      =1          # from enum VisBuiltInStencilTypes
	visBuiltInStencilCallouts     =3          # from enum VisBuiltInStencilTypes
	visBuiltInStencilContainers   =2          # from enum VisBuiltInStencilTypes
	visBuiltInStencilLegends      =4          # from enum VisBuiltInStencilTypes
	visErrorDivideByZero          =39         # from enum VisCellError
	visErrorName                  =61         # from enum VisCellError
	visErrorNotAvailable          =74         # from enum VisCellError
	visErrorNumber                =68         # from enum VisCellError
	visErrorReference             =55         # from enum VisCellError
	visErrorSuccess               =0          # from enum VisCellError
	visErrorValue                 =47         # from enum VisCellError
	vis1DBeginX                   =0          # from enum VisCellIndices
	vis1DBeginY                   =1          # from enum VisCellIndices
	vis1DEndX                     =2          # from enum VisCellIndices
	vis1DEndY                     =3          # from enum VisCellIndices
	visActionAction               =3          # from enum VisCellIndices
	visActionBeginGroup           =8          # from enum VisCellIndices
	visActionButtonFace           =15         # from enum VisCellIndices
	visActionChecked              =4          # from enum VisCellIndices
	visActionDisabled             =5          # from enum VisCellIndices
	visActionFlyoutChild          =9          # from enum VisCellIndices
	visActionHelp                 =2          # from enum VisCellIndices
	visActionInvisible            =7          # from enum VisCellIndices
	visActionMenu                 =0          # from enum VisCellIndices
	visActionPrompt               =1          # from enum VisCellIndices
	visActionReadOnly             =6          # from enum VisCellIndices
	visActionSortKey              =16         # from enum VisCellIndices
	visActionTagName              =14         # from enum VisCellIndices
	visActiveRecord               =4          # from enum VisCellIndices
	visAlignBottom                =5          # from enum VisCellIndices
	visAlignCenter                =1          # from enum VisCellIndices
	visAlignLeft                  =0          # from enum VisCellIndices
	visAlignMiddle                =4          # from enum VisCellIndices
	visAlignRight                 =2          # from enum VisCellIndices
	visAlignTop                   =3          # from enum VisCellIndices
	visAnnotationComment          =5          # from enum VisCellIndices
	visAnnotationDate             =4          # from enum VisCellIndices
	visAnnotationLangID           =6          # from enum VisCellIndices
	visAnnotationMarkerIndex      =3          # from enum VisCellIndices
	visAnnotationReviewerID       =2          # from enum VisCellIndices
	visAnnotationX                =0          # from enum VisCellIndices
	visAnnotationY                =1          # from enum VisCellIndices
	visAspectRatio                =5          # from enum VisCellIndices
	visBegTrigger                 =11         # from enum VisCellIndices
	visBevelBottomHeight          =5          # from enum VisCellIndices
	visBevelBottomType            =3          # from enum VisCellIndices
	visBevelBottomWidth           =4          # from enum VisCellIndices
	visBevelContourColor          =8          # from enum VisCellIndices
	visBevelContourSize           =9          # from enum VisCellIndices
	visBevelDepthColor            =6          # from enum VisCellIndices
	visBevelDepthSize             =7          # from enum VisCellIndices
	visBevelLightingAngle         =12         # from enum VisCellIndices
	visBevelLightingType          =11         # from enum VisCellIndices
	visBevelMaterialType          =10         # from enum VisCellIndices
	visBevelTopHeight             =2          # from enum VisCellIndices
	visBevelTopType               =0          # from enum VisCellIndices
	visBevelTopWidth              =1          # from enum VisCellIndices
	visBow                        =2          # from enum VisCellIndices
	visBulletFont                 =9          # from enum VisCellIndices
	visBulletFontSize             =11         # from enum VisCellIndices
	visBulletIndex                =7          # from enum VisCellIndices
	visBulletString               =8          # from enum VisCellIndices
	visCellFirst                  =0          # from enum VisCellIndices
	visCellInval                  =255        # from enum VisCellIndices
	visCellNone                   =255        # from enum VisCellIndices
	visCharacterAsianFont         =51         # from enum VisCellIndices
	visCharacterCase              =3          # from enum VisCellIndices
	visCharacterColor             =1          # from enum VisCellIndices
	visCharacterColorTrans        =17         # from enum VisCellIndices
	visCharacterComplexScriptFont =52         # from enum VisCellIndices
	visCharacterComplexScriptSize =54         # from enum VisCellIndices
	visCharacterDblUnderline      =8          # from enum VisCellIndices
	visCharacterDoubleStrikethrough=13         # from enum VisCellIndices
	visCharacterFont              =0          # from enum VisCellIndices
	visCharacterFontScale         =5          # from enum VisCellIndices
	visCharacterLangID            =57         # from enum VisCellIndices
	visCharacterLetterspace       =16         # from enum VisCellIndices
	visCharacterLocale            =6          # from enum VisCellIndices
	visCharacterLocalizeFont      =53         # from enum VisCellIndices
	visCharacterOverline          =9          # from enum VisCellIndices
	visCharacterPerpendicular     =12         # from enum VisCellIndices
	visCharacterPos               =4          # from enum VisCellIndices
	visCharacterRTLText           =14         # from enum VisCellIndices
	visCharacterSize              =7          # from enum VisCellIndices
	visCharacterStrikethru        =10         # from enum VisCellIndices
	visCharacterStyle             =2          # from enum VisCellIndices
	visCharacterUseVertical       =15         # from enum VisCellIndices
	visCnnctA                     =2          # from enum VisCellIndices
	visCnnctAutoGen               =5          # from enum VisCellIndices
	visCnnctB                     =3          # from enum VisCellIndices
	visCnnctC                     =4          # from enum VisCellIndices
	visCnnctD                     =5          # from enum VisCellIndices
	visCnnctDirX                  =2          # from enum VisCellIndices
	visCnnctDirY                  =3          # from enum VisCellIndices
	visCnnctType                  =4          # from enum VisCellIndices
	visCnnctX                     =0          # from enum VisCellIndices
	visCnnctY                     =1          # from enum VisCellIndices
	visColorSchemeIndex           =0          # from enum VisCellIndices
	visComment                    =16         # from enum VisCellIndices
	visCompNoFill                 =0          # from enum VisCellIndices
	visCompNoLine                 =1          # from enum VisCellIndices
	visCompNoQuickDrag            =5          # from enum VisCellIndices
	visCompNoShow                 =2          # from enum VisCellIndices
	visCompNoSnap                 =3          # from enum VisCellIndices
	visCompPath                   =4          # from enum VisCellIndices
	visCompoundType               =10         # from enum VisCellIndices
	visConnectorSchemeIndex       =2          # from enum VisCellIndices
	visContainerLayout            =5          # from enum VisCellIndices
	visControl1X                  =2          # from enum VisCellIndices
	visControl1Y                  =3          # from enum VisCellIndices
	visControl2X                  =4          # from enum VisCellIndices
	visControl2Y                  =5          # from enum VisCellIndices
	visControlX                   =2          # from enum VisCellIndices
	visControlY                   =3          # from enum VisCellIndices
	visCopyright                  =1          # from enum VisCellIndices
	visCtlGlue                    =6          # from enum VisCellIndices
	visCtlTip                     =8          # from enum VisCellIndices
	visCtlType                    =7          # from enum VisCellIndices
	visCtlX                       =0          # from enum VisCellIndices
	visCtlXCon                    =4          # from enum VisCellIndices
	visCtlXDyn                    =2          # from enum VisCellIndices
	visCtlY                       =1          # from enum VisCellIndices
	visCtlYCon                    =5          # from enum VisCellIndices
	visCtlYDyn                    =3          # from enum VisCellIndices
	visCustPropsAsk               =7          # from enum VisCellIndices
	visCustPropsCalendar          =15         # from enum VisCellIndices
	visCustPropsDataLinked        =8          # from enum VisCellIndices
	visCustPropsFormat            =3          # from enum VisCellIndices
	visCustPropsInvis             =6          # from enum VisCellIndices
	visCustPropsLabel             =2          # from enum VisCellIndices
	visCustPropsLangID            =14         # from enum VisCellIndices
	visCustPropsPrompt            =1          # from enum VisCellIndices
	visCustPropsSortKey           =4          # from enum VisCellIndices
	visCustPropsType              =5          # from enum VisCellIndices
	visCustPropsValue             =0          # from enum VisCellIndices
	visDataItem                   =1          # from enum VisCellIndices
	visDataSource                 =0          # from enum VisCellIndices
	visDistanceFromGround         =5          # from enum VisCellIndices
	visDocAddMarkup               =3          # from enum VisCellIndices
	visDocLangID                  =19         # from enum VisCellIndices
	visDocLockDuplicatePage       =7          # from enum VisCellIndices
	visDocLockPreview             =1          # from enum VisCellIndices
	visDocLockReplace             =5          # from enum VisCellIndices
	visDocMetric                  =2          # from enum VisCellIndices
	visDocNoCoauth                =6          # from enum VisCellIndices
	visDocOutputFormat            =0          # from enum VisCellIndices
	visDocPreviewQuality          =9          # from enum VisCellIndices
	visDocPreviewScope            =10         # from enum VisCellIndices
	visDocViewMarkup              =4          # from enum VisCellIndices
	visDropSource                 =17         # from enum VisCellIndices
	visDynFeedback                =8          # from enum VisCellIndices
	visEccentricityAngle          =4          # from enum VisCellIndices
	visEffectSchemeIndex          =1          # from enum VisCellIndices
	visEllipseCenterX             =0          # from enum VisCellIndices
	visEllipseCenterY             =1          # from enum VisCellIndices
	visEllipseMajorX              =2          # from enum VisCellIndices
	visEllipseMajorY              =3          # from enum VisCellIndices
	visEllipseMinorX              =4          # from enum VisCellIndices
	visEllipseMinorY              =5          # from enum VisCellIndices
	visEmbellishmentIndex         =7          # from enum VisCellIndices
	visEndTrigger                 =12         # from enum VisCellIndices
	visEvtCellDblClick            =2          # from enum VisCellIndices
	visEvtCellDrop                =4          # from enum VisCellIndices
	visEvtCellMultiDrop           =22         # from enum VisCellIndices
	visEvtCellTheData             =0          # from enum VisCellIndices
	visEvtCellTheText             =1          # from enum VisCellIndices
	visEvtCellXFMod               =3          # from enum VisCellIndices
	visFieldCalendar              =7          # from enum VisCellIndices
	visFieldCell                  =0          # from enum VisCellIndices
	visFieldEditMode              =1          # from enum VisCellIndices
	visFieldFormat                =2          # from enum VisCellIndices
	visFieldObjectKind            =10         # from enum VisCellIndices
	visFieldType                  =3          # from enum VisCellIndices
	visFieldUICategory            =4          # from enum VisCellIndices
	visFieldUICode                =5          # from enum VisCellIndices
	visFieldUIFormat              =6          # from enum VisCellIndices
	visFillBkgnd                  =1          # from enum VisCellIndices
	visFillBkgndTrans             =7          # from enum VisCellIndices
	visFillForegnd                =0          # from enum VisCellIndices
	visFillForegndTrans           =6          # from enum VisCellIndices
	visFillGradientAngle          =3          # from enum VisCellIndices
	visFillGradientDir            =2          # from enum VisCellIndices
	visFillGradientEnabled        =5          # from enum VisCellIndices
	visFillPattern                =2          # from enum VisCellIndices
	visFillShdwBkgnd              =4          # from enum VisCellIndices
	visFillShdwBkgndTrans         =9          # from enum VisCellIndices
	visFillShdwBlur               =15         # from enum VisCellIndices
	visFillShdwForegnd            =3          # from enum VisCellIndices
	visFillShdwForegndTrans       =8          # from enum VisCellIndices
	visFillShdwObliqueAngle       =13         # from enum VisCellIndices
	visFillShdwOffsetX            =11         # from enum VisCellIndices
	visFillShdwOffsetY            =12         # from enum VisCellIndices
	visFillShdwPattern            =5          # from enum VisCellIndices
	visFillShdwScaleFactor        =14         # from enum VisCellIndices
	visFillShdwShow               =16         # from enum VisCellIndices
	visFillShdwType               =10         # from enum VisCellIndices
	visFlags                      =13         # from enum VisCellIndices
	visFontSchemeIndex            =3          # from enum VisCellIndices
	visFrgnImgClippingPath        =4          # from enum VisCellIndices
	visFrgnImgHeight              =3          # from enum VisCellIndices
	visFrgnImgOffsetX             =0          # from enum VisCellIndices
	visFrgnImgOffsetY             =1          # from enum VisCellIndices
	visFrgnImgWidth               =2          # from enum VisCellIndices
	visGlowColor                  =4          # from enum VisCellIndices
	visGlowColorTrans             =5          # from enum VisCellIndices
	visGlowSize                   =6          # from enum VisCellIndices
	visGlueType                   =9          # from enum VisCellIndices
	visGradientStopColor          =0          # from enum VisCellIndices
	visGradientStopColorTrans     =1          # from enum VisCellIndices
	visGradientStopPosition       =2          # from enum VisCellIndices
	visGroupDisplayMode           =1          # from enum VisCellIndices
	visGroupDontMoveChildren      =5          # from enum VisCellIndices
	visGroupIsDropTarget          =2          # from enum VisCellIndices
	visGroupIsSnapTarget          =3          # from enum VisCellIndices
	visGroupIsTextEditTarget      =4          # from enum VisCellIndices
	visGroupSelectMode            =0          # from enum VisCellIndices
	visGuideFlags                 =2          # from enum VisCellIndices
	visHLinkAddress               =1          # from enum VisCellIndices
	visHLinkDefault               =7          # from enum VisCellIndices
	visHLinkDescription           =0          # from enum VisCellIndices
	visHLinkExtraInfo             =3          # from enum VisCellIndices
	visHLinkFrame                 =4          # from enum VisCellIndices
	visHLinkInvisible             =8          # from enum VisCellIndices
	visHLinkNewWin                =5          # from enum VisCellIndices
	visHLinkSortKey               =15         # from enum VisCellIndices
	visHLinkSubAddress            =2          # from enum VisCellIndices
	visHideText                   =5          # from enum VisCellIndices
	visHorzAlign                  =6          # from enum VisCellIndices
	visImageBlur                  =4          # from enum VisCellIndices
	visImageBrightness            =2          # from enum VisCellIndices
	visImageContrast              =1          # from enum VisCellIndices
	visImageDenoise               =5          # from enum VisCellIndices
	visImageGamma                 =0          # from enum VisCellIndices
	visImageSharpen               =3          # from enum VisCellIndices
	visImageTransparency          =6          # from enum VisCellIndices
	visIndentFirst                =0          # from enum VisCellIndices
	visIndentLeft                 =1          # from enum VisCellIndices
	visIndentRight                =2          # from enum VisCellIndices
	visInfiniteLineX1             =0          # from enum VisCellIndices
	visInfiniteLineX2             =2          # from enum VisCellIndices
	visInfiniteLineY1             =1          # from enum VisCellIndices
	visInfiniteLineY2             =3          # from enum VisCellIndices
	visKeepTextFlat               =6          # from enum VisCellIndices
	visLOBehavior                 =15         # from enum VisCellIndices
	visLOFlags                    =13         # from enum VisCellIndices
	visLOInteraction              =14         # from enum VisCellIndices
	visLabelField                 =3          # from enum VisCellIndices
	visLayerActive                =6          # from enum VisCellIndices
	visLayerColor                 =2          # from enum VisCellIndices
	visLayerColorTrans            =11         # from enum VisCellIndices
	visLayerGlue                  =9          # from enum VisCellIndices
	visLayerLock                  =7          # from enum VisCellIndices
	visLayerMember                =0          # from enum VisCellIndices
	visLayerName                  =0          # from enum VisCellIndices
	visLayerNameUniv              =10         # from enum VisCellIndices
	visLayerPrint                 =5          # from enum VisCellIndices
	visLayerSnap                  =8          # from enum VisCellIndices
	visLayerStatus                =3          # from enum VisCellIndices
	visLayerVisible               =4          # from enum VisCellIndices
	visLineArrowSize              =4          # from enum VisCellIndices
	visLineBeginArrow             =5          # from enum VisCellIndices
	visLineBeginArrowSize         =8          # from enum VisCellIndices
	visLineColor                  =1          # from enum VisCellIndices
	visLineColorTrans             =9          # from enum VisCellIndices
	visLineEndArrow               =6          # from enum VisCellIndices
	visLineEndArrowSize           =4          # from enum VisCellIndices
	visLineEndCap                 =7          # from enum VisCellIndices
	visLineGradientAngle          =1          # from enum VisCellIndices
	visLineGradientDir            =0          # from enum VisCellIndices
	visLineGradientEnabled        =4          # from enum VisCellIndices
	visLinePattern                =2          # from enum VisCellIndices
	visLineRounding               =3          # from enum VisCellIndices
	visLineWeight                 =0          # from enum VisCellIndices
	visLocalizeBulletFont         =10         # from enum VisCellIndices
	visLockAspect                 =4          # from enum VisCellIndices
	visLockBegin                  =6          # from enum VisCellIndices
	visLockCalcWH                 =14         # from enum VisCellIndices
	visLockCrop                   =9          # from enum VisCellIndices
	visLockCustProp               =16         # from enum VisCellIndices
	visLockDelete                 =5          # from enum VisCellIndices
	visLockEnd                    =7          # from enum VisCellIndices
	visLockFormat                 =12         # from enum VisCellIndices
	visLockFromGroupFormat        =17         # from enum VisCellIndices
	visLockGroup                  =13         # from enum VisCellIndices
	visLockHeight                 =1          # from enum VisCellIndices
	visLockMoveX                  =2          # from enum VisCellIndices
	visLockMoveY                  =3          # from enum VisCellIndices
	visLockReplace                =23         # from enum VisCellIndices
	visLockRotate                 =8          # from enum VisCellIndices
	visLockSelect                 =15         # from enum VisCellIndices
	visLockTextEdit               =11         # from enum VisCellIndices
	visLockThemeColors            =18         # from enum VisCellIndices
	visLockThemeConnectors        =20         # from enum VisCellIndices
	visLockThemeEffects           =19         # from enum VisCellIndices
	visLockThemeFonts             =21         # from enum VisCellIndices
	visLockThemeIndex             =22         # from enum VisCellIndices
	visLockVariation              =24         # from enum VisCellIndices
	visLockVtxEdit                =10         # from enum VisCellIndices
	visLockWidth                  =0          # from enum VisCellIndices
	visNURBSData                  =6          # from enum VisCellIndices
	visNURBSKnot                  =2          # from enum VisCellIndices
	visNURBSKnotPrev              =4          # from enum VisCellIndices
	visNURBSWeight                =3          # from enum VisCellIndices
	visNURBSWeightPrev            =5          # from enum VisCellIndices
	visNoAlignBox                 =3          # from enum VisCellIndices
	visNoCtlHandles               =2          # from enum VisCellIndices
	visNoLiveDynamics             =18         # from enum VisCellIndices
	visNoObjHandles               =0          # from enum VisCellIndices
	visNonPrinting                =1          # from enum VisCellIndices
	visObjCalendar                =25         # from enum VisCellIndices
	visObjDropOnPageScale         =28         # from enum VisCellIndices
	visObjHelp                    =0          # from enum VisCellIndices
	visObjKeywords                =27         # from enum VisCellIndices
	visObjLangID                  =26         # from enum VisCellIndices
	visObjLocalizeMerge           =19         # from enum VisCellIndices
	visObjNoProofing              =20         # from enum VisCellIndices
	visObjTheme                   =29         # from enum VisCellIndices
	visObjThemeModern             =30         # from enum VisCellIndices
	visPLOAvenueSizeX             =20         # from enum VisCellIndices
	visPLOAvenueSizeY             =21         # from enum VisCellIndices
	visPLOAvoidPageBreaks         =4          # from enum VisCellIndices
	visPLOBlockSizeX              =18         # from enum VisCellIndices
	visPLOBlockSizeY              =19         # from enum VisCellIndices
	visPLOCtrlAsInput             =3          # from enum VisCellIndices
	visPLODynamicsOff             =2          # from enum VisCellIndices
	visPLOEnableGrid              =1          # from enum VisCellIndices
	visPLOJumpCode                =12         # from enum VisCellIndices
	visPLOJumpDirX                =14         # from enum VisCellIndices
	visPLOJumpDirY                =15         # from enum VisCellIndices
	visPLOJumpFactorX             =24         # from enum VisCellIndices
	visPLOJumpFactorY             =25         # from enum VisCellIndices
	visPLOJumpStyle               =13         # from enum VisCellIndices
	visPLOLineAdjustFrom          =26         # from enum VisCellIndices
	visPLOLineAdjustTo            =27         # from enum VisCellIndices
	visPLOLineRouteExt            =29         # from enum VisCellIndices
	visPLOLineToLineX             =22         # from enum VisCellIndices
	visPLOLineToLineY             =23         # from enum VisCellIndices
	visPLOLineToNodeX             =16         # from enum VisCellIndices
	visPLOLineToNodeY             =17         # from enum VisCellIndices
	visPLOPlaceDepth              =10         # from enum VisCellIndices
	visPLOPlaceFlip               =28         # from enum VisCellIndices
	visPLOPlaceStyle              =8          # from enum VisCellIndices
	visPLOPlowCode                =11         # from enum VisCellIndices
	visPLOResizePage              =0          # from enum VisCellIndices
	visPLORouteStyle              =9          # from enum VisCellIndices
	visPLOSplit                   =30         # from enum VisCellIndices
	visPageDrawResizeType         =38         # from enum VisCellIndices
	visPageDrawScaleType          =7          # from enum VisCellIndices
	visPageDrawSizeType           =6          # from enum VisCellIndices
	visPageDrawingScale           =5          # from enum VisCellIndices
	visPageHeight                 =1          # from enum VisCellIndices
	visPageInhibitSnap            =26         # from enum VisCellIndices
	visPageLockDuplicate          =28         # from enum VisCellIndices
	visPageLockReplace            =27         # from enum VisCellIndices
	visPageScale                  =4          # from enum VisCellIndices
	visPageShdwObliqueAngle       =36         # from enum VisCellIndices
	visPageShdwOffsetX            =2          # from enum VisCellIndices
	visPageShdwOffsetY            =3          # from enum VisCellIndices
	visPageShdwScaleFactor        =37         # from enum VisCellIndices
	visPageShdwType               =35         # from enum VisCellIndices
	visPageUIVisibility           =34         # from enum VisCellIndices
	visPageWidth                  =0          # from enum VisCellIndices
	visPageZOrderChanged          =39         # from enum VisCellIndices
	visPerspective                =4          # from enum VisCellIndices
	visPolylineData               =2          # from enum VisCellIndices
	visPrintPropertiesBottomMargin=3          # from enum VisCellIndices
	visPrintPropertiesCenterX     =8          # from enum VisCellIndices
	visPrintPropertiesCenterY     =9          # from enum VisCellIndices
	visPrintPropertiesLeftMargin  =0          # from enum VisCellIndices
	visPrintPropertiesOnPage      =10         # from enum VisCellIndices
	visPrintPropertiesPageOrientation=16         # from enum VisCellIndices
	visPrintPropertiesPagesX      =6          # from enum VisCellIndices
	visPrintPropertiesPagesY      =7          # from enum VisCellIndices
	visPrintPropertiesPaperKind   =17         # from enum VisCellIndices
	visPrintPropertiesPaperSource =18         # from enum VisCellIndices
	visPrintPropertiesPrintGrid   =11         # from enum VisCellIndices
	visPrintPropertiesRightMargin =1          # from enum VisCellIndices
	visPrintPropertiesScaleX      =4          # from enum VisCellIndices
	visPrintPropertiesScaleY      =5          # from enum VisCellIndices
	visPrintPropertiesTopMargin   =2          # from enum VisCellIndices
	visQuickStyleEffectsMatrix    =6          # from enum VisCellIndices
	visQuickStyleFillColor        =1          # from enum VisCellIndices
	visQuickStyleFillMatrix       =5          # from enum VisCellIndices
	visQuickStyleFontColor        =3          # from enum VisCellIndices
	visQuickStyleFontMatrix       =7          # from enum VisCellIndices
	visQuickStyleLineColor        =0          # from enum VisCellIndices
	visQuickStyleLineMatrix       =4          # from enum VisCellIndices
	visQuickStyleShadowColor      =2          # from enum VisCellIndices
	visQuickStyleType             =8          # from enum VisCellIndices
	visQuickStyleVariation        =9          # from enum VisCellIndices
	visReflectionBlur             =3          # from enum VisCellIndices
	visReflectionDist             =2          # from enum VisCellIndices
	visReflectionSize             =1          # from enum VisCellIndices
	visReflectionTrans            =0          # from enum VisCellIndices
	visReplaceCopyCells           =3          # from enum VisCellIndices
	visReplaceLockFormat          =2          # from enum VisCellIndices
	visReplaceLockShapeData       =0          # from enum VisCellIndices
	visReplaceLockText            =1          # from enum VisCellIndices
	visReviewerColor              =2          # from enum VisCellIndices
	visReviewerCurrentIndex       =4          # from enum VisCellIndices
	visReviewerInitials           =1          # from enum VisCellIndices
	visReviewerName               =0          # from enum VisCellIndices
	visReviewerReviewerID         =3          # from enum VisCellIndices
	visRotateGradientWithShape    =6          # from enum VisCellIndices
	visRotationType               =3          # from enum VisCellIndices
	visRotationXAngle             =0          # from enum VisCellIndices
	visRotationYAngle             =1          # from enum VisCellIndices
	visRotationZAngle             =2          # from enum VisCellIndices
	visSLOCategoryChanged         =24         # from enum VisCellIndices
	visSLOConFixedCode            =12         # from enum VisCellIndices
	visSLODisplayLevel            =22         # from enum VisCellIndices
	visSLOFixedCode               =8          # from enum VisCellIndices
	visSLOJumpCode                =13         # from enum VisCellIndices
	visSLOJumpDirX                =16         # from enum VisCellIndices
	visSLOJumpDirY                =17         # from enum VisCellIndices
	visSLOJumpStyle               =14         # from enum VisCellIndices
	visSLOLineRouteExt            =19         # from enum VisCellIndices
	visSLOPermX                   =0          # from enum VisCellIndices
	visSLOPermY                   =1          # from enum VisCellIndices
	visSLOPermeablePlace          =2          # from enum VisCellIndices
	visSLOPlaceFlip               =18         # from enum VisCellIndices
	visSLOPlaceStyle              =11         # from enum VisCellIndices
	visSLOPlowCode                =9          # from enum VisCellIndices
	visSLORelChanged              =23         # from enum VisCellIndices
	visSLORelationships           =3          # from enum VisCellIndices
	visSLORouteStyle              =10         # from enum VisCellIndices
	visSLOSplit                   =20         # from enum VisCellIndices
	visSLOSplittable              =21         # from enum VisCellIndices
	visScratchA                   =2          # from enum VisCellIndices
	visScratchB                   =3          # from enum VisCellIndices
	visScratchC                   =4          # from enum VisCellIndices
	visScratchD                   =5          # from enum VisCellIndices
	visScratchX                   =0          # from enum VisCellIndices
	visScratchY                   =1          # from enum VisCellIndices
	visShapeMasterSelector        =2          # from enum VisCellIndices
	visSketchAmount               =10         # from enum VisCellIndices
	visSketchEnabled              =9          # from enum VisCellIndices
	visSketchFillChange           =13         # from enum VisCellIndices
	visSketchLineChange           =12         # from enum VisCellIndices
	visSketchLineWeight           =11         # from enum VisCellIndices
	visSketchSeed                 =8          # from enum VisCellIndices
	visSmartTagButtonFace         =6          # from enum VisCellIndices
	visSmartTagDescription        =15         # from enum VisCellIndices
	visSmartTagDisabled           =7          # from enum VisCellIndices
	visSmartTagDisplayMode        =5          # from enum VisCellIndices
	visSmartTagName               =2          # from enum VisCellIndices
	visSmartTagX                  =0          # from enum VisCellIndices
	visSmartTagXJustify           =3          # from enum VisCellIndices
	visSmartTagY                  =1          # from enum VisCellIndices
	visSmartTagYJustify           =4          # from enum VisCellIndices
	visSoftEdgesSize              =7          # from enum VisCellIndices
	visSpaceAfter                 =5          # from enum VisCellIndices
	visSpaceBefore                =4          # from enum VisCellIndices
	visSpaceLine                  =3          # from enum VisCellIndices
	visSplineDegree               =5          # from enum VisCellIndices
	visSplineKnot                 =2          # from enum VisCellIndices
	visSplineKnot2                =3          # from enum VisCellIndices
	visSplineKnot3                =4          # from enum VisCellIndices
	visStyleHidden                =3          # from enum VisCellIndices
	visStyleIncludesFill          =1          # from enum VisCellIndices
	visStyleIncludesLine          =0          # from enum VisCellIndices
	visStyleIncludesText          =2          # from enum VisCellIndices
	visTabAlign                   =2          # from enum VisCellIndices
	visTabPos                     =1          # from enum VisCellIndices
	visTabStopCount               =0          # from enum VisCellIndices
	visTextPosAfterBullet         =12         # from enum VisCellIndices
	visThemeIndex                 =4          # from enum VisCellIndices
	visTxtBlkBkgnd                =5          # from enum VisCellIndices
	visTxtBlkBkgndTrans           =11         # from enum VisCellIndices
	visTxtBlkBottomMargin         =3          # from enum VisCellIndices
	visTxtBlkDefaultTabStop       =6          # from enum VisCellIndices
	visTxtBlkDirection            =10         # from enum VisCellIndices
	visTxtBlkLeftMargin           =0          # from enum VisCellIndices
	visTxtBlkRightMargin          =1          # from enum VisCellIndices
	visTxtBlkTopMargin            =2          # from enum VisCellIndices
	visTxtBlkVerticalAlign        =4          # from enum VisCellIndices
	visUpdateAlignBox             =4          # from enum VisCellIndices
	visUseGroupGradient           =7          # from enum VisCellIndices
	visUserPrompt                 =1          # from enum VisCellIndices
	visUserValue                  =0          # from enum VisCellIndices
	visVariationColorIndex        =5          # from enum VisCellIndices
	visVariationStyleIndex        =6          # from enum VisCellIndices
	visVerticalText               =6          # from enum VisCellIndices
	visWalkPref                   =10         # from enum VisCellIndices
	visX                          =0          # from enum VisCellIndices
	visXFormAngle                 =6          # from enum VisCellIndices
	visXFormFlipX                 =7          # from enum VisCellIndices
	visXFormFlipY                 =8          # from enum VisCellIndices
	visXFormHeight                =3          # from enum VisCellIndices
	visXFormLocPinX               =4          # from enum VisCellIndices
	visXFormLocPinY               =5          # from enum VisCellIndices
	visXFormPinX                  =0          # from enum VisCellIndices
	visXFormPinY                  =1          # from enum VisCellIndices
	visXFormResizeMode            =9          # from enum VisCellIndices
	visXFormWidth                 =2          # from enum VisCellIndices
	visXGridDensity               =6          # from enum VisCellIndices
	visXGridOrigin                =10         # from enum VisCellIndices
	visXGridSpacing               =8          # from enum VisCellIndices
	visXRulerDensity              =0          # from enum VisCellIndices
	visXRulerOrigin               =4          # from enum VisCellIndices
	visY                          =1          # from enum VisCellIndices
	visYGridDensity               =7          # from enum VisCellIndices
	visYGridOrigin                =11         # from enum VisCellIndices
	visYGridSpacing               =9          # from enum VisCellIndices
	visYRulerDensity              =1          # from enum VisCellIndices
	visYRulerOrigin               =5          # from enum VisCellIndices
	visArchitectural              =1          # from enum VisCellVals
	visArrowSizeColossal          =6          # from enum VisCellVals
	visArrowSizeJumbo             =5          # from enum VisCellVals
	visArrowSizeLarge             =3          # from enum VisCellVals
	visArrowSizeMedium            =2          # from enum VisCellVals
	visArrowSizeSmall             =1          # from enum VisCellVals
	visArrowSizeVeryLarge         =4          # from enum VisCellVals
	visArrowSizeVerySmall         =0          # from enum VisCellVals
	visBackDotsMini               =8          # from enum VisCellVals
	visBackDotsWide               =18         # from enum VisCellVals
	visBold                       =1          # from enum VisCellVals
	visCalArabicHijri             =1          # from enum VisCellVals
	visCalChineseTaiwan           =3          # from enum VisCellVals
	visCalHebrewLunar             =2          # from enum VisCellVals
	visCalJapaneseEmperor         =4          # from enum VisCellVals
	visCalKoreanDanki             =6          # from enum VisCellVals
	visCalSakaEra                 =7          # from enum VisCellVals
	visCalThaiBuddhism            =5          # from enum VisCellVals
	visCalThaiBuddhist            =5          # from enum VisCellVals
	visCalTranslitEnglish         =8          # from enum VisCellVals
	visCalTranslitFrench          =9          # from enum VisCellVals
	visCalWestern                 =0          # from enum VisCellVals
	visCaseAllCaps                =1          # from enum VisCellVals
	visCaseInitialCaps            =2          # from enum VisCellVals
	visCaseNormal                 =0          # from enum VisCellVals
	visCnnctTypeInward            =0          # from enum VisCellVals
	visCnnctTypeInwardOutward     =2          # from enum VisCellVals
	visCnnctTypeOutward           =1          # from enum VisCellVals
	visComplexBold                =16         # from enum VisCellVals
	visComplexItalic              =32         # from enum VisCellVals
	visCtlLocked                  =1          # from enum VisCellVals
	visCtlLockedHidden            =6          # from enum VisCellVals
	visCtlOffsetMax               =4          # from enum VisCellVals
	visCtlOffsetMaxHidden         =9          # from enum VisCellVals
	visCtlOffsetMid               =3          # from enum VisCellVals
	visCtlOffsetMidHidden         =8          # from enum VisCellVals
	visCtlOffsetMin               =2          # from enum VisCellVals
	visCtlOffsetMinHidden         =7          # from enum VisCellVals
	visCtlProportional            =0          # from enum VisCellVals
	visCtlProportionalHidden      =5          # from enum VisCellVals
	visCustom                     =3          # from enum VisCellVals
	visDSArch                     =7          # from enum VisCellVals
	visDSEngr                     =6          # from enum VisCellVals
	visDSMetric                   =5          # from enum VisCellVals
	visDocPreviewQualityDetailed  =1          # from enum VisCellVals
	visDocPreviewQualityDraft     =0          # from enum VisCellVals
	visDocPreviewScope1stPage     =0          # from enum VisCellVals
	visDocPreviewScopeAllPages    =2          # from enum VisCellVals
	visDocPreviewScopeNone        =1          # from enum VisCellVals
	visDynFBDefault               =0          # from enum VisCellVals
	visDynFBUCon3Leg              =1          # from enum VisCellVals
	visDynFBUCon5Leg              =2          # from enum VisCellVals
	visEngineering                =2          # from enum VisCellVals
	visFSTOblique                 =2          # from enum VisCellVals
	visFSTPageDefault             =0          # from enum VisCellVals
	visFSTSimple                  =1          # from enum VisCellVals
	visForeDotsMini               =10         # from enum VisCellVals
	visForeDotsNarrow             =11         # from enum VisCellVals
	visForeDotsWide               =12         # from enum VisCellVals
	visGlueTypeDefault            =0          # from enum VisCellVals
	visGlueTypeNoWalking          =4          # from enum VisCellVals
	visGlueTypeNoWalkingTo        =8          # from enum VisCellVals
	visGlueTypeTrigger            =1          # from enum VisCellVals
	visGlueTypeWalking            =2          # from enum VisCellVals
	visGridCoarse                 =2          # from enum VisCellVals
	visGridFine                   =8          # from enum VisCellVals
	visGridFixed                  =0          # from enum VisCellVals
	visGridNormal                 =4          # from enum VisCellVals
	visGrpDispModeBack            =1          # from enum VisCellVals
	visGrpDispModeFront           =2          # from enum VisCellVals
	visGrpDispModeNone            =0          # from enum VisCellVals
	visGrpSelModeGroup1st         =1          # from enum VisCellVals
	visGrpSelModeGroupOnly        =0          # from enum VisCellVals
	visGrpSelModeMembers1st       =2          # from enum VisCellVals
	visGuideXActive               =1024       # from enum VisCellVals
	visGuideYActive               =2048       # from enum VisCellVals
	visHalfAndHalf                =9          # from enum VisCellVals
	visHorzCenter                 =1          # from enum VisCellVals
	visHorzDistribute             =4          # from enum VisCellVals
	visHorzForce                  =4          # from enum VisCellVals
	visHorzJustify                =3          # from enum VisCellVals
	visHorzJustifyHigh            =7          # from enum VisCellVals
	visHorzJustifyLow             =5          # from enum VisCellVals
	visHorzJustifyMedium          =6          # from enum VisCellVals
	visHorzLeft                   =0          # from enum VisCellVals
	visHorzRight                  =2          # from enum VisCellVals
	visItalic                     =2          # from enum VisCellVals
	visLOBPlaceNormal             =0          # from enum VisCellVals
	visLOBRouteFlowNS             =5          # from enum VisCellVals
	visLOBRouteFlowWE             =6          # from enum VisCellVals
	visLOBRouteManual             =1024       # from enum VisCellVals
	visLOBRouteNormal             =0          # from enum VisCellVals
	visLOBRouteRightAng           =1          # from enum VisCellVals
	visLOBRouteStraight           =2          # from enum VisCellVals
	visLOBRouteTreeNS             =7          # from enum VisCellVals
	visLOBRouteTreeWE             =8          # from enum VisCellVals
	visLOFlagsDont                =4          # from enum VisCellVals
	visLOFlagsPNRGroup            =8          # from enum VisCellVals
	visLOFlagsPlacable            =1          # from enum VisCellVals
	visLOFlagsRoutable            =2          # from enum VisCellVals
	visLOFlagsVisDecides          =0          # from enum VisCellVals
	visLOFlipDefault              =0          # from enum VisCellVals
	visLOFlipNone                 =8          # from enum VisCellVals
	visLOFlipRotate               =4          # from enum VisCellVals
	visLOFlipX                    =1          # from enum VisCellVals
	visLOFlipY                    =2          # from enum VisCellVals
	visLOIPlaceNormal             =0          # from enum VisCellVals
	visLOIPlaceXPermeable         =2          # from enum VisCellVals
	visLOIPlaceYPermeable         =4          # from enum VisCellVals
	visLOIRouteNormal             =0          # from enum VisCellVals
	visLOJumpDirXDefault          =0          # from enum VisCellVals
	visLOJumpDirXDown             =2          # from enum VisCellVals
	visLOJumpDirXUp               =1          # from enum VisCellVals
	visLOJumpDirYDefault          =0          # from enum VisCellVals
	visLOJumpDirYLeft             =1          # from enum VisCellVals
	visLOJumpDirYRight            =2          # from enum VisCellVals
	visLOJumpStyle2Point          =5          # from enum VisCellVals
	visLOJumpStyle3Point          =6          # from enum VisCellVals
	visLOJumpStyle4Point          =7          # from enum VisCellVals
	visLOJumpStyle5Point          =8          # from enum VisCellVals
	visLOJumpStyle6Point          =9          # from enum VisCellVals
	visLOJumpStyleArc             =1          # from enum VisCellVals
	visLOJumpStyleDefault         =0          # from enum VisCellVals
	visLOJumpStyleGap             =2          # from enum VisCellVals
	visLOJumpStyleSquare          =3          # from enum VisCellVals
	visLOJumpStyleTriangle        =4          # from enum VisCellVals
	visLOPlaceBottomToTop         =4          # from enum VisCellVals
	visLOPlaceCircular            =6          # from enum VisCellVals
	visLOPlaceCompactDownLeft     =14         # from enum VisCellVals
	visLOPlaceCompactDownRight    =7          # from enum VisCellVals
	visLOPlaceCompactLeftDown     =13         # from enum VisCellVals
	visLOPlaceCompactLeftUp       =12         # from enum VisCellVals
	visLOPlaceCompactRightDown    =8          # from enum VisCellVals
	visLOPlaceCompactRightUp      =9          # from enum VisCellVals
	visLOPlaceCompactUpLeft       =11         # from enum VisCellVals
	visLOPlaceCompactUpRight      =10         # from enum VisCellVals
	visLOPlaceDefault             =0          # from enum VisCellVals
	visLOPlaceHierarchyBottomToTopCenter=20         # from enum VisCellVals
	visLOPlaceHierarchyBottomToTopLeft=19         # from enum VisCellVals
	visLOPlaceHierarchyBottomToTopRight=21         # from enum VisCellVals
	visLOPlaceHierarchyLeftToRightBottom=24         # from enum VisCellVals
	visLOPlaceHierarchyLeftToRightMiddle=23         # from enum VisCellVals
	visLOPlaceHierarchyLeftToRightTop=22         # from enum VisCellVals
	visLOPlaceHierarchyRightToLeftBottom=27         # from enum VisCellVals
	visLOPlaceHierarchyRightToLeftMiddle=26         # from enum VisCellVals
	visLOPlaceHierarchyRightToLeftTop=25         # from enum VisCellVals
	visLOPlaceHierarchyTopToBottomCenter=17         # from enum VisCellVals
	visLOPlaceHierarchyTopToBottomLeft=16         # from enum VisCellVals
	visLOPlaceHierarchyTopToBottomRight=18         # from enum VisCellVals
	visLOPlaceLeftToRight         =2          # from enum VisCellVals
	visLOPlaceParentDefault       =15         # from enum VisCellVals
	visLOPlaceRadial              =3          # from enum VisCellVals
	visLOPlaceRightToLeft         =5          # from enum VisCellVals
	visLOPlaceTopToBottom         =1          # from enum VisCellVals
	visLORouteCenterToCenter      =16         # from enum VisCellVals
	visLORouteDefault             =0          # from enum VisCellVals
	visLORouteExtDefault          =0          # from enum VisCellVals
	visLORouteExtNURBS            =2          # from enum VisCellVals
	visLORouteExtStraight         =1          # from enum VisCellVals
	visLORouteFlowchartEW         =13         # from enum VisCellVals
	visLORouteFlowchartNS         =5          # from enum VisCellVals
	visLORouteFlowchartSN         =12         # from enum VisCellVals
	visLORouteFlowchartWE         =6          # from enum VisCellVals
	visLORouteNetwork             =9          # from enum VisCellVals
	visLORouteOrgChartEW          =11         # from enum VisCellVals
	visLORouteOrgChartNS          =3          # from enum VisCellVals
	visLORouteOrgChartSN          =10         # from enum VisCellVals
	visLORouteOrgChartWE          =4          # from enum VisCellVals
	visLORouteRightAngle          =1          # from enum VisCellVals
	visLORouteSimpleEW            =20         # from enum VisCellVals
	visLORouteSimpleHV            =21         # from enum VisCellVals
	visLORouteSimpleNS            =17         # from enum VisCellVals
	visLORouteSimpleSN            =19         # from enum VisCellVals
	visLORouteSimpleVH            =22         # from enum VisCellVals
	visLORouteSimpleWE            =18         # from enum VisCellVals
	visLORouteStraight            =2          # from enum VisCellVals
	visLORouteTreeEW              =15         # from enum VisCellVals
	visLORouteTreeNS              =7          # from enum VisCellVals
	visLORouteTreeSN              =14         # from enum VisCellVals
	visLORouteTreeWE              =8          # from enum VisCellVals
	visLayerAvailable             =2          # from enum VisCellVals
	visLayerDeleted               =1          # from enum VisCellVals
	visLayerValid                 =0          # from enum VisCellVals
	visLocFontAlways              =1          # from enum VisCellVals
	visLocFontIfArialOrSym        =0          # from enum VisCellVals
	visLocFontNever               =2          # from enum VisCellVals
	visLogical                    =4          # from enum VisCellVals
	visNoFill                     =0          # from enum VisCellVals
	visNoLayerColor               =255        # from enum VisCellVals
	visNoScale                    =0          # from enum VisCellVals
	visPLOJumpDisplayOrder        =4          # from enum VisCellVals
	visPLOJumpHorizontal          =1          # from enum VisCellVals
	visPLOJumpLastRouted          =3          # from enum VisCellVals
	visPLOJumpNone                =0          # from enum VisCellVals
	visPLOJumpProhibitAll         =6          # from enum VisCellVals
	visPLOJumpReverseDisplayOrder =5          # from enum VisCellVals
	visPLOJumpVertical            =2          # from enum VisCellVals
	visPLOLineAdjustFromAll       =1          # from enum VisCellVals
	visPLOLineAdjustFromNone      =2          # from enum VisCellVals
	visPLOLineAdjustFromNotRelated=0          # from enum VisCellVals
	visPLOLineAdjustFromRoutingDefault=3          # from enum VisCellVals
	visPLOLineAdjustToAll         =1          # from enum VisCellVals
	visPLOLineAdjustToDefault     =0          # from enum VisCellVals
	visPLOLineAdjustToNone        =2          # from enum VisCellVals
	visPLOLineAdjustToRelated     =3          # from enum VisCellVals
	visPLOPlaceBottomToTop        =4          # from enum VisCellVals
	visPLOPlaceCircular           =6          # from enum VisCellVals
	visPLOPlaceCompactDownLeft    =14         # from enum VisCellVals
	visPLOPlaceCompactDownRight   =7          # from enum VisCellVals
	visPLOPlaceCompactLeftDown    =13         # from enum VisCellVals
	visPLOPlaceCompactLeftUp      =12         # from enum VisCellVals
	visPLOPlaceCompactRightDown   =8          # from enum VisCellVals
	visPLOPlaceCompactRightUp     =9          # from enum VisCellVals
	visPLOPlaceCompactUpLeft      =11         # from enum VisCellVals
	visPLOPlaceCompactUpRight     =10         # from enum VisCellVals
	visPLOPlaceDefault            =0          # from enum VisCellVals
	visPLOPlaceDepthDeep          =2          # from enum VisCellVals
	visPLOPlaceDepthDefault       =0          # from enum VisCellVals
	visPLOPlaceDepthMedium        =1          # from enum VisCellVals
	visPLOPlaceDepthShallow       =3          # from enum VisCellVals
	visPLOPlaceHierarchyBottomToTopCenter=20         # from enum VisCellVals
	visPLOPlaceHierarchyBottomToTopLeft=19         # from enum VisCellVals
	visPLOPlaceHierarchyBottomToTopRight=21         # from enum VisCellVals
	visPLOPlaceHierarchyLeftToRightBottom=24         # from enum VisCellVals
	visPLOPlaceHierarchyLeftToRightMiddle=23         # from enum VisCellVals
	visPLOPlaceHierarchyLeftToRightTop=22         # from enum VisCellVals
	visPLOPlaceHierarchyRightToLeftBottom=27         # from enum VisCellVals
	visPLOPlaceHierarchyRightToLeftMiddle=26         # from enum VisCellVals
	visPLOPlaceHierarchyRightToLeftTop=25         # from enum VisCellVals
	visPLOPlaceHierarchyTopToBottomCenter=17         # from enum VisCellVals
	visPLOPlaceHierarchyTopToBottomLeft=16         # from enum VisCellVals
	visPLOPlaceHierarchyTopToBottomRight=18         # from enum VisCellVals
	visPLOPlaceLeftToRight        =2          # from enum VisCellVals
	visPLOPlaceParentDefault      =15         # from enum VisCellVals
	visPLOPlaceRadial             =3          # from enum VisCellVals
	visPLOPlaceRightToLeft        =5          # from enum VisCellVals
	visPLOPlaceTopToBottom        =1          # from enum VisCellVals
	visPLOPlowAll                 =1          # from enum VisCellVals
	visPLOPlowNone                =0          # from enum VisCellVals
	visPLOSplitAllow              =1          # from enum VisCellVals
	visPLOSplitNone               =0          # from enum VisCellVals
	visPPFlagsRTLText             =1          # from enum VisCellVals
	visPPOLandscape               =2          # from enum VisCellVals
	visPPOPortrait                =1          # from enum VisCellVals
	visPPOSameAsPrinter           =0          # from enum VisCellVals
	visPosNormal                  =0          # from enum VisCellVals
	visPosSub                     =2          # from enum VisCellVals
	visPosSuper                   =1          # from enum VisCellVals
	visPrintSetup                 =0          # from enum VisCellVals
	visPropTypeBool               =3          # from enum VisCellVals
	visPropTypeCurrency           =7          # from enum VisCellVals
	visPropTypeDate               =5          # from enum VisCellVals
	visPropTypeDuration           =6          # from enum VisCellVals
	visPropTypeListFix            =1          # from enum VisCellVals
	visPropTypeListVar            =4          # from enum VisCellVals
	visPropTypeNumber             =2          # from enum VisCellVals
	visPropTypeString             =0          # from enum VisCellVals
	visRulerCoarse                =8          # from enum VisCellVals
	visRulerFine                  =32         # from enum VisCellVals
	visRulerFixed                 =0          # from enum VisCellVals
	visRulerNormal                =16         # from enum VisCellVals
	visSLOConFixedByAlgFrom       =4          # from enum VisCellVals
	visSLOConFixedByAlgFromTo     =6          # from enum VisCellVals
	visSLOConFixedByAlgTo         =5          # from enum VisCellVals
	visSLOConFixedRerouteAsNeeded =1          # from enum VisCellVals
	visSLOConFixedRerouteFreely   =0          # from enum VisCellVals
	visSLOConFixedRerouteNever    =2          # from enum VisCellVals
	visSLOConFixedRerouteOnCrossover=3          # from enum VisCellVals
	visSLOFixedConnPtsIgnore      =32         # from enum VisCellVals
	visSLOFixedConnPtsOnly        =64         # from enum VisCellVals
	visSLOFixedNoFoldToShape      =128        # from enum VisCellVals
	visSLOFixedPermeablePlow      =4          # from enum VisCellVals
	visSLOFixedPlacement          =1          # from enum VisCellVals
	visSLOFixedPlow               =2          # from enum VisCellVals
	visSLOJumpAlways              =2          # from enum VisCellVals
	visSLOJumpDefault             =0          # from enum VisCellVals
	visSLOJumpNeither             =4          # from enum VisCellVals
	visSLOJumpNever               =1          # from enum VisCellVals
	visSLOJumpOther               =3          # from enum VisCellVals
	visSLOPlowAlways              =2          # from enum VisCellVals
	visSLOPlowDefault             =0          # from enum VisCellVals
	visSLOPlowNever               =1          # from enum VisCellVals
	visSLOSplitAllow              =1          # from enum VisCellVals
	visSLOSplitNone               =0          # from enum VisCellVals
	visSLOSplittableAllow         =1          # from enum VisCellVals
	visSLOSplittableNone          =0          # from enum VisCellVals
	visScaleCustom                =3          # from enum VisCellVals
	visScaleMechanical            =5          # from enum VisCellVals
	visScaleMetric                =4          # from enum VisCellVals
	visSmallCaps                  =8          # from enum VisCellVals
	visSmartTagDispModeAlways     =2          # from enum VisCellVals
	visSmartTagDispModeMouseOver  =0          # from enum VisCellVals
	visSmartTagDispModeShapeSelected=1          # from enum VisCellVals
	visSmartTagXJustifyCenter     =1          # from enum VisCellVals
	visSmartTagXJustifyLeft       =0          # from enum VisCellVals
	visSmartTagXJustifyRight      =2          # from enum VisCellVals
	visSmartTagYJustifyBottom     =2          # from enum VisCellVals
	visSmartTagYJustifyMiddle     =1          # from enum VisCellVals
	visSmartTagYJustifyTop        =0          # from enum VisCellVals
	visSolid                      =1          # from enum VisCellVals
	visStandard                   =2          # from enum VisCellVals
	visTFOKHorizontalInVertical   =1          # from enum VisCellVals
	visTFOKStandard               =0          # from enum VisCellVals
	visTabStopCenter              =1          # from enum VisCellVals
	visTabStopComma               =4          # from enum VisCellVals
	visTabStopDecimal             =3          # from enum VisCellVals
	visTabStopLeft                =0          # from enum VisCellVals
	visTabStopRight               =2          # from enum VisCellVals
	visThickDiagonalCross         =17         # from enum VisCellVals
	visThickDownDiagonal          =15         # from enum VisCellVals
	visThickHorz                  =13         # from enum VisCellVals
	visThickUpDiagonal            =16         # from enum VisCellVals
	visThickVertical              =14         # from enum VisCellVals
	visThinCross                  =23         # from enum VisCellVals
	visThinDiagonalCross          =24         # from enum VisCellVals
	visThinDownDiagonal           =21         # from enum VisCellVals
	visThinHorz                   =19         # from enum VisCellVals
	visThinUpDiagonal             =22         # from enum VisCellVals
	visThinVert                   =20         # from enum VisCellVals
	visTight                      =1          # from enum VisCellVals
	visTxtBlkLeftToRight          =0          # from enum VisCellVals
	visTxtBlkOpaque               =255        # from enum VisCellVals
	visTxtBlkTopToBottom          =1          # from enum VisCellVals
	visUIVHidden                  =1          # from enum VisCellVals
	visUIVNormal                  =0          # from enum VisCellVals
	visUnderLine                  =4          # from enum VisCellVals
	visVertBottom                 =2          # from enum VisCellVals
	visVertMiddle                 =1          # from enum VisCellVals
	visVertTop                    =0          # from enum VisCellVals
	visWalkPrefBegNS              =1          # from enum VisCellVals
	visWalkPrefEndNS              =2          # from enum VisCellVals
	visWideCross                  =3          # from enum VisCellVals
	visWideDiagonalCross          =4          # from enum VisCellVals
	visWideDownDiagonal           =5          # from enum VisCellVals
	visWideHorz                   =6          # from enum VisCellVals
	visWideUpDiagonal             =2          # from enum VisCellVals
	visWideVert                   =7          # from enum VisCellVals
	visXFormResizeDontCare        =0          # from enum VisCellVals
	visXFormResizeScale           =2          # from enum VisCellVals
	visXFormResizeSpread          =1          # from enum VisCellVals
	visCenterViewDefault          =0          # from enum VisCenterViewFlags
	visCenterViewIfOffScreen      =1          # from enum VisCenterViewFlags
	visCenterViewSelectShape      =2          # from enum VisCenterViewFlags
	visBiasLeft                   =1          # from enum VisCharsBias
	visBiasLetVisioChoose         =0          # from enum VisCharsBias
	visBiasRight                  =2          # from enum VisCharsBias
	visColorDiscrete              =0          # from enum VisColoringMethod
	visColorInvalid               =2          # from enum VisColoringMethod
	visColorRange                 =1          # from enum VisColoringMethod
	visConnectedShapesAllNodes    =0          # from enum VisConnectedShapesFlags
	visConnectedShapesIncomingNodes=1          # from enum VisConnectedShapesFlags
	visConnectedShapesOutgoingNodes=2          # from enum VisConnectedShapesFlags
	visIn                         =0          # from enum VisConnectorDirection
	visOut                        =1          # from enum VisConnectorDirection
	visConnectorBeginpoint        =0          # from enum VisConnectorEnds
	visConnectorBothEnds          =2          # from enum VisConnectorEnds
	visConnectorEndPoint          =1          # from enum VisConnectorEnds
	visContainerAutoResizeExpand  =1          # from enum VisContainerAutoResize
	visContainerAutoResizeExpandContract=2          # from enum VisContainerAutoResize
	visContainerAutoResizeNone    =0          # from enum VisContainerAutoResize
	visContainerFlagsDefault      =0          # from enum VisContainerFlags
	visContainerFlagsExcludeCallouts=4          # from enum VisContainerFlags
	visContainerFlagsExcludeConnectors=2          # from enum VisContainerFlags
	visContainerFlagsExcludeContainers=1          # from enum VisContainerFlags
	visContainerFlagsExcludeElements=8          # from enum VisContainerFlags
	visContainerFlagsExcludeListMembers=32         # from enum VisContainerFlags
	visContainerFlagsExcludeNested=16         # from enum VisContainerFlags
	visContainerFormatContainerAutoResize=1          # from enum VisContainerFormatType
	visContainerFormatFitToContents=2          # from enum VisContainerFormatType
	visContainerFormatLockMembership=0          # from enum VisContainerFormatType
	visContainerMemberInList      =4          # from enum VisContainerMemberState
	visContainerMemberInterior    =1          # from enum VisContainerMemberState
	visContainerMemberNotAMember  =0          # from enum VisContainerMemberState
	visContainerMemberOnBoundary  =2          # from enum VisContainerMemberState
	visContainerMemberOutside     =3          # from enum VisContainerMemberState
	visContainerExcludeNested     =1          # from enum VisContainerNested
	visContainerIncludeNested     =0          # from enum VisContainerNested
	visContainerTypeList          =1          # from enum VisContainerTypes
	visContainerTypeNormal        =0          # from enum VisContainerTypes
	visHorizontal                 =0          # from enum VisCrossFunctionalFlowchartOrientation
	visVertical                   =1          # from enum VisCrossFunctionalFlowchartOrientation
	visCopyPasteCenter            =2          # from enum VisCutCopyPasteCodes
	visCopyPasteDontAddToContainers=32         # from enum VisCutCopyPasteCodes
	visCopyPasteNoAssociatedCallouts=16         # from enum VisCutCopyPasteCodes
	visCopyPasteNoCascade         =64         # from enum VisCutCopyPasteCodes
	visCopyPasteNoContainerMembers=8          # from enum VisCutCopyPasteCodes
	visCopyPasteNoHealConnectors  =4          # from enum VisCutCopyPasteCodes
	visCopyPasteNoTranslate       =1          # from enum VisCutCopyPasteCodes
	visCopyPasteNormal            =0          # from enum VisCutCopyPasteCodes
	visDataColumnPropertyCalendar =3          # from enum VisDataColumnProperties
	visDataColumnPropertyCurrency =5          # from enum VisDataColumnProperties
	visDataColumnPropertyDisplayName=6          # from enum VisDataColumnProperties
	visDataColumnPropertyHyperlink=8          # from enum VisDataColumnProperties
	visDataColumnPropertyLangID   =2          # from enum VisDataColumnProperties
	visDataColumnPropertyType     =1          # from enum VisDataColumnProperties
	visDataColumnPropertyUnits    =4          # from enum VisDataColumnProperties
	visDataColumnPropertyVisible  =7          # from enum VisDataColumnProperties
	visDataRecordsetBase          =64         # from enum VisDataRecordsetAddOptions
	visDataRecordsetDelayQuery    =8          # from enum VisDataRecordsetAddOptions
	visDataRecordsetDontCopyLinks =16         # from enum VisDataRecordsetAddOptions
	visDataRecordsetForDataVisualizer=32         # from enum VisDataRecordsetAddOptions
	visDataRecordsetNoAdvConfig   =4          # from enum VisDataRecordsetAddOptions
	visDataRecordsetNoExternalDataUI=1          # from enum VisDataRecordsetAddOptions
	visDataRecordsetNoRefreshUI   =2          # from enum VisDataRecordsetAddOptions
	visBlack                      =0          # from enum VisDefaultColors
	visBlue                       =4          # from enum VisDefaultColors
	visCyan                       =7          # from enum VisDefaultColors
	visDarkBlue                   =10         # from enum VisDefaultColors
	visDarkCyan                   =13         # from enum VisDefaultColors
	visDarkGray                   =19         # from enum VisDefaultColors
	visDarkGreen                  =9          # from enum VisDefaultColors
	visDarkRed                    =8          # from enum VisDefaultColors
	visDarkYellow                 =11         # from enum VisDefaultColors
	visGray                       =14         # from enum VisDefaultColors
	visGray10                     =15         # from enum VisDefaultColors
	visGray20                     =16         # from enum VisDefaultColors
	visGray30                     =17         # from enum VisDefaultColors
	visGray40                     =18         # from enum VisDefaultColors
	visGray50                     =19         # from enum VisDefaultColors
	visGray60                     =20         # from enum VisDefaultColors
	visGray70                     =21         # from enum VisDefaultColors
	visGray80                     =22         # from enum VisDefaultColors
	visGray90                     =23         # from enum VisDefaultColors
	visGreen                      =3          # from enum VisDefaultColors
	visMagenta                    =6          # from enum VisDefaultColors
	visPurple                     =12         # from enum VisDefaultColors
	visRed                        =2          # from enum VisDefaultColors
	visTransparent                =0          # from enum VisDefaultColors
	visWhite                      =1          # from enum VisDefaultColors
	visYellow                     =5          # from enum VisDefaultColors
	visDefaultSaveCurrent         =0          # from enum VisDefaultSaveFormats
	visDefaultSaveCurrentBinary   =0          # from enum VisDefaultSaveFormats
	visDefaultSaveCurrentMacroEnabled=3          # from enum VisDefaultSaveFormats
	visDefaultSaveCurrentXML      =2          # from enum VisDefaultSaveFormats
	visDefaultSavePreviousBinary  =1          # from enum VisDefaultSaveFormats
	visDeleteHealConnectors       =1          # from enum VisDeleteFlags
	visDeleteNoAssociatedCallouts =8          # from enum VisDeleteFlags
	visDeleteNoContainerMembers   =4          # from enum VisDeleteFlags
	visDeleteNoHealConnectors     =2          # from enum VisDeleteFlags
	visDeleteNormal               =0          # from enum VisDeleteFlags
	visServiceAll                 =-1         # from enum VisDiagramServices
	visServiceAnimations          =8          # from enum VisDiagramServices
	visServiceAutoSizePage        =1          # from enum VisDiagramServices
	visServiceNone                =0          # from enum VisDiagramServices
	visServiceStructureBasic      =2          # from enum VisDiagramServices
	visServiceStructureFull       =4          # from enum VisDiagramServices
	visServiceVersion140          =7          # from enum VisDiagramServices
	visServiceVersion150          =8          # from enum VisDiagramServices
	visDistHorzCenter             =2          # from enum VisDistributeTypes
	visDistHorzLeft               =1          # from enum VisDistributeTypes
	visDistHorzRight              =3          # from enum VisDistributeTypes
	visDistHorzSpace              =0          # from enum VisDistributeTypes
	visDistVertBottom             =7          # from enum VisDistributeTypes
	visDistVertMiddle             =6          # from enum VisDistributeTypes
	visDistVertSpace              =4          # from enum VisDistributeTypes
	visDistVertTop                =5          # from enum VisDistributeTypes
	visDocCleanActAll             =16383      # from enum VisDocCleanActions
	visDocCleanActBadDisplayLists =256        # from enum VisDocCleanActions
	visDocCleanActBadFieldCounts  =512        # from enum VisDocCleanActions
	visDocCleanActBadFieldFormulas=2048       # from enum VisDocCleanActions
	visDocCleanActBadFieldMarks   =4096       # from enum VisDocCleanActions
	visDocCleanActBadReferences   =8192       # from enum VisDocCleanActions
	visDocCleanActConstantFormulas=32         # from enum VisDocCleanActions
	visDocCleanActDefault         =8152       # from enum VisDocCleanActions
	visDocCleanActDeletedFields   =1024       # from enum VisDocCleanActions
	visDocCleanActDuplicateSubs   =128        # from enum VisDocCleanActions
	visDocCleanActEmptyRowsAndSects=2          # from enum VisDocCleanActions
	visDocCleanActLocalFormulas   =1          # from enum VisDocCleanActions
	visDocCleanActMissingSubs     =16         # from enum VisDocCleanActions
	visDocCleanActNearZero        =64         # from enum VisDocCleanActions
	visDocCleanActNonDefaultFonts =4          # from enum VisDocCleanActions
	visDocCleanActStaleResults    =8          # from enum VisDocCleanActions
	visDocCleanAlertDefault       =0          # from enum VisDocCleanActions
	visDocCleanFixDefault         =984        # from enum VisDocCleanActions
	visDocCleanPageSheet          =256        # from enum VisDocCleanTargets
	visDocCleanTargAll            =255        # from enum VisDocCleanTargets
	visDocCleanTargBPages         =2          # from enum VisDocCleanTargets
	visDocCleanTargDoc            =16         # from enum VisDocCleanTargets
	visDocCleanTargFPages         =1          # from enum VisDocCleanTargets
	visDocCleanTargMasters        =4          # from enum VisDocCleanTargets
	visDocCleanTargRPages         =32         # from enum VisDocCleanTargets
	visDocCleanTargStyles         =8          # from enum VisDocCleanTargets
	visDocExIntentPrint           =1          # from enum VisDocExIntent
	visDocExIntentScreen          =0          # from enum VisDocExIntent
	visDocModeDesign              =1          # from enum VisDocModeArgs
	visDocModeRun                 =0          # from enum VisDocModeArgs
	visInvalDocID                 =-1         # from enum VisDocModeArgs
	visVersion10                  =65571      # from enum VisDocVersions
	visVersion100                 =393216     # from enum VisDocVersions
	visVersion110                 =720896     # from enum VisDocVersions
	visVersion120                 =720896     # from enum VisDocVersions
	visVersion140                 =720896     # from enum VisDocVersions
	visVersion150                 =983040     # from enum VisDocVersions
	visVersion20                  =131072     # from enum VisDocVersions
	visVersion30                  =196611     # from enum VisDocVersions
	visVersion40                  =262144     # from enum VisDocVersions
	visVersion50                  =327680     # from enum VisDocVersions
	visVersion60                  =393216     # from enum VisDocVersions
	visVersionUnsaved             =0          # from enum VisDocVersions
	visDocTypeInval               =0          # from enum VisDocumentTypes
	visTypeDrawing                =1          # from enum VisDocumentTypes
	visTypeStencil                =2          # from enum VisDocumentTypes
	visTypeTemplate               =3          # from enum VisDocumentTypes
	visDrawRegionDeleteInput      =4          # from enum VisDrawRegionFlags
	visDrawRegionIgnoreVisible    =32         # from enum VisDrawRegionFlags
	visDrawRegionIncludeDataGraphics=64         # from enum VisDrawRegionFlags
	visDrawRegionIncludeHidden    =16         # from enum VisDrawRegionFlags
	visPolyarcs                   =256        # from enum VisDrawSplineFlags
	visPolyline1D                 =8          # from enum VisDrawSplineFlags
	visSpline1D                   =8          # from enum VisDrawSplineFlags
	visSplineAbrupt               =4          # from enum VisDrawSplineFlags
	visSplineDoCircles            =2          # from enum VisDrawSplineFlags
	visSplinePeriodic             =1          # from enum VisDrawSplineFlags
	visEditionPremium             =2          # from enum VisEdition
	visEditionProfessional        =1          # from enum VisEdition
	visEditionStandard            =0          # from enum VisEdition
	visActCodeAdvise              =2          # from enum VisEventCodes
	visActCodeRunAddon            =1          # from enum VisEventCodes
	visEvtAdd                     =32768      # from enum VisEventCodes
	visEvtAfterModal              =64         # from enum VisEventCodes
	visEvtApp                     =4096       # from enum VisEventCodes
	visEvtAppActivate             =1          # from enum VisEventCodes
	visEvtAppDeactivate           =2          # from enum VisEventCodes
	visEvtBeforeModal             =32         # from enum VisEventCodes
	visEvtBeforeQuit              =16         # from enum VisEventCodes
	visEvtCell                    =2048       # from enum VisEventCodes
	visEvtCode1stUser             =28672      # from enum VisEventCodes
	visEvtCodeAfterCoauthMerge    =14         # from enum VisEventCodes
	visEvtCodeAfterForcedFlush    =201        # from enum VisEventCodes
	visEvtCodeAfterResume         =209        # from enum VisEventCodes
	visEvtCodeAfterResumeEvents   =213        # from enum VisEventCodes
	visEvtCodeBefDocSave          =7          # from enum VisEventCodes
	visEvtCodeBefDocSaveAs        =8          # from enum VisEventCodes
	visEvtCodeBefForcedFlush      =200        # from enum VisEventCodes
	visEvtCodeBefSelDel           =901        # from enum VisEventCodes
	visEvtCodeBefWinPageTurn      =703        # from enum VisEventCodes
	visEvtCodeBefWinSelDel        =702        # from enum VisEventCodes
	visEvtCodeBeforeReplaceShapes =913        # from enum VisEventCodes
	visEvtCodeBeforeSuspend       =208        # from enum VisEventCodes
	visEvtCodeBeforeSuspendEvents =212        # from enum VisEventCodes
	visEvtCodeCalloutRelationshipAdded=504        # from enum VisEventCodes
	visEvtCodeCalloutRelationshipDeleted=505        # from enum VisEventCodes
	visEvtCodeCancelConvertToGroup=908        # from enum VisEventCodes
	visEvtCodeCancelDocClose      =10         # from enum VisEventCodes
	visEvtCodeCancelMasterDel     =401        # from enum VisEventCodes
	visEvtCodeCancelPageDel       =501        # from enum VisEventCodes
	visEvtCodeCancelQuit          =205        # from enum VisEventCodes
	visEvtCodeCancelReplaceShapes =912        # from enum VisEventCodes
	visEvtCodeCancelSelDel        =904        # from enum VisEventCodes
	visEvtCodeCancelSelGroup      =910        # from enum VisEventCodes
	visEvtCodeCancelStyleDel      =301        # from enum VisEventCodes
	visEvtCodeCancelSuspend       =207        # from enum VisEventCodes
	visEvtCodeCancelSuspendEvents =211        # from enum VisEventCodes
	visEvtCodeCancelUngroup       =906        # from enum VisEventCodes
	visEvtCodeCancelWinClose      =707        # from enum VisEventCodes
	visEvtCodeContainerRelationshipAdded=502        # from enum VisEventCodes
	visEvtCodeContainerRelationshipDeleted=503        # from enum VisEventCodes
	visEvtCodeCreate              =1          # from enum VisEventCodes
	visEvtCodeDocCreate           =1          # from enum VisEventCodes
	visEvtCodeDocDesign           =6          # from enum VisEventCodes
	visEvtCodeDocOpen             =2          # from enum VisEventCodes
	visEvtCodeDocRunning          =5          # from enum VisEventCodes
	visEvtCodeDocSave             =3          # from enum VisEventCodes
	visEvtCodeDocSaveAs           =4          # from enum VisEventCodes
	visEvtCodeEnterScope          =202        # from enum VisEventCodes
	visEvtCodeExitScope           =203        # from enum VisEventCodes
	visEvtCodeInval               =0          # from enum VisEventCodes
	visEvtCodeKeyDown             =712        # from enum VisEventCodes
	visEvtCodeKeyPress            =713        # from enum VisEventCodes
	visEvtCodeKeyUp               =714        # from enum VisEventCodes
	visEvtCodeLastUser            =32767      # from enum VisEventCodes
	visEvtCodeMouseDown           =709        # from enum VisEventCodes
	visEvtCodeMouseMove           =710        # from enum VisEventCodes
	visEvtCodeMouseUp             =711        # from enum VisEventCodes
	visEvtCodeOpen                =2          # from enum VisEventCodes
	visEvtCodeQueryCancelConvertToGroup=907        # from enum VisEventCodes
	visEvtCodeQueryCancelDocClose =9          # from enum VisEventCodes
	visEvtCodeQueryCancelMasterDel=400        # from enum VisEventCodes
	visEvtCodeQueryCancelPageDel  =500        # from enum VisEventCodes
	visEvtCodeQueryCancelQuit     =204        # from enum VisEventCodes
	visEvtCodeQueryCancelReplaceShapes=911        # from enum VisEventCodes
	visEvtCodeQueryCancelSelDel   =903        # from enum VisEventCodes
	visEvtCodeQueryCancelSelGroup =909        # from enum VisEventCodes
	visEvtCodeQueryCancelStyleDel =300        # from enum VisEventCodes
	visEvtCodeQueryCancelSuspend  =206        # from enum VisEventCodes
	visEvtCodeQueryCancelSuspendEvents=210        # from enum VisEventCodes
	visEvtCodeQueryCancelUngroup  =905        # from enum VisEventCodes
	visEvtCodeQueryCancelWinClose =706        # from enum VisEventCodes
	visEvtCodeRuleSetValidated    =13         # from enum VisEventCodes
	visEvtCodeSelAdded            =902        # from enum VisEventCodes
	visEvtCodeSelectionMovedToSubprocess=12         # from enum VisEventCodes
	visEvtCodeShapeBeforeTextEdit =803        # from enum VisEventCodes
	visEvtCodeShapeDelete         =801        # from enum VisEventCodes
	visEvtCodeShapeExitTextEdit   =804        # from enum VisEventCodes
	visEvtCodeShapeParentChange   =802        # from enum VisEventCodes
	visEvtCodeShapesReplaced      =914        # from enum VisEventCodes
	visEvtCodeViewChanged         =705        # from enum VisEventCodes
	visEvtCodeWinOnAddonKeyMSG    =708        # from enum VisEventCodes
	visEvtCodeWinPageTurn         =704        # from enum VisEventCodes
	visEvtCodeWinSelChange        =701        # from enum VisEventCodes
	visEvtConnect                 =256        # from enum VisEventCodes
	visEvtDataRecordset           =32         # from enum VisEventCodes
	visEvtDel                     =16384      # from enum VisEventCodes
	visEvtDoc                     =2          # from enum VisEventCodes
	visEvtFormula                 =4096       # from enum VisEventCodes
	visEvtIDInval                 =-1         # from enum VisEventCodes
	visEvtIdMostRecent            =0          # from enum VisEventCodes
	visEvtIdle                    =1024       # from enum VisEventCodes
	visEvtLayer                   =32         # from enum VisEventCodes
	visEvtMarker                  =256        # from enum VisEventCodes
	visEvtMaster                  =8          # from enum VisEventCodes
	visEvtMod                     =8192       # from enum VisEventCodes
	visEvtNonePending             =512        # from enum VisEventCodes
	visEvtObjActivate             =4          # from enum VisEventCodes
	visEvtObjDeactivate           =8          # from enum VisEventCodes
	visEvtPage                    =16         # from enum VisEventCodes
	visEvtRemoveHiddenInformation =11         # from enum VisEventCodes
	visEvtRow                     =1024       # from enum VisEventCodes
	visEvtSection                 =512        # from enum VisEventCodes
	visEvtShape                   =64         # from enum VisEventCodes
	visEvtShapeDataGraphicChanged =807        # from enum VisEventCodes
	visEvtShapeLinkAdded          =805        # from enum VisEventCodes
	visEvtShapeLinkDeleted        =806        # from enum VisEventCodes
	visEvtStyle                   =4          # from enum VisEventCodes
	visEvtText                    =128        # from enum VisEventCodes
	visEvtWinActivate             =128        # from enum VisEventCodes
	visEvtWindow                  =1          # from enum VisEventCodes
	visScopeIDInval               =-1         # from enum VisEventCodes
	visExistsAnywhere             =0          # from enum VisExistsFlags
	visExistsLocally              =1          # from enum VisExistsFlags
	visFCatCustom                 =0          # from enum VisFieldCategories
	visFCatDateTime               =1          # from enum VisFieldCategories
	visFCatDocument               =2          # from enum VisFieldCategories
	visFCatGeometry               =3          # from enum VisFieldCategories
	visFCatNotes                  =6          # from enum VisFieldCategories
	visFCatObject                 =4          # from enum VisFieldCategories
	visFCatPage                   =5          # from enum VisFieldCategories
	visFCodeAngle                 =2          # from enum VisFieldCodes
	visFCodeBackgroundName        =0          # from enum VisFieldCodes
	visFCodeCategory              =9          # from enum VisFieldCodes
	visFCodeCompany               =8          # from enum VisFieldCodes
	visFCodeCreateDate            =0          # from enum VisFieldCodes
	visFCodeCreateTime            =1          # from enum VisFieldCodes
	visFCodeCreator               =0          # from enum VisFieldCodes
	visFCodeCurrentDate           =2          # from enum VisFieldCodes
	visFCodeCurrentTime           =3          # from enum VisFieldCodes
	visFCodeData1                 =0          # from enum VisFieldCodes
	visFCodeData2                 =1          # from enum VisFieldCodes
	visFCodeData3                 =2          # from enum VisFieldCodes
	visFCodeDescription           =1          # from enum VisFieldCodes
	visFCodeDirectory             =2          # from enum VisFieldCodes
	visFCodeEditDate              =4          # from enum VisFieldCodes
	visFCodeEditTime              =5          # from enum VisFieldCodes
	visFCodeFileName              =3          # from enum VisFieldCodes
	visFCodeHeight                =1          # from enum VisFieldCodes
	visFCodeHyperlinkBase         =10         # from enum VisFieldCodes
	visFCodeKeyWords              =4          # from enum VisFieldCodes
	visFCodeManager               =7          # from enum VisFieldCodes
	visFCodeMasterName            =4          # from enum VisFieldCodes
	visFCodeNumberOfPages         =2          # from enum VisFieldCodes
	visFCodeObjectID              =3          # from enum VisFieldCodes
	visFCodeObjectName            =5          # from enum VisFieldCodes
	visFCodeObjectType            =6          # from enum VisFieldCodes
	visFCodePageName              =1          # from enum VisFieldCodes
	visFCodePageNumber            =3          # from enum VisFieldCodes
	visFCodePrintDate             =6          # from enum VisFieldCodes
	visFCodePrintTime             =7          # from enum VisFieldCodes
	visFCodeSubject               =5          # from enum VisFieldCodes
	visFCodeTitle                 =6          # from enum VisFieldCodes
	visFCodeWidth                 =0          # from enum VisFieldCodes
	visFmt0PlDefUnits             =3          # from enum VisFieldFormats
	visFmt0PlNoUnits              =2          # from enum VisFieldFormats
	visFmt1PlDefUnits             =5          # from enum VisFieldFormats
	visFmt1PlNoUnits              =4          # from enum VisFieldFormats
	visFmt2PlDefUnits             =7          # from enum VisFieldFormats
	visFmt2PlNoUnits              =6          # from enum VisFieldFormats
	visFmt3PlDefUnits             =9          # from enum VisFieldFormats
	visFmt3PlNoUnits              =8          # from enum VisFieldFormats
	visFmtCDateieXmmmmXdddd       =53         # from enum VisFieldFormats
	visFmtCDateieXmmmmXddddXww    =52         # from enum VisFieldFormats
	visFmtCDateiieXmmmmXdddd      =51         # from enum VisFieldFormats
	visFmtCDateiiieXmmmmXdddd     =50         # from enum VisFieldFormats
	visFmtDateDDMMYY              =27         # from enum VisFieldFormats
	visFmtDateDMMMMYYYY           =29         # from enum VisFieldFormats
	visFmtDateDMMMYYYY            =28         # from enum VisFieldFormats
	visFmtDateDMYY                =26         # from enum VisFieldFormats
	visFmtDateLong                =21         # from enum VisFieldFormats
	visFmtDateMDYY                =22         # from enum VisFieldFormats
	visFmtDateMMDDYY              =23         # from enum VisFieldFormats
	visFmtDateMmmDYYYY            =24         # from enum VisFieldFormats
	visFmtDateMmmmDYYYY           =25         # from enum VisFieldFormats
	visFmtDateShort               =20         # from enum VisFieldFormats
	visFmtDateTWNfYYYYMMDDD_C     =50         # from enum VisFieldFormats
	visFmtDateTWNfyyyymmdd_C      =53         # from enum VisFieldFormats
	visFmtDateTWNfyyyymmddww_C    =52         # from enum VisFieldFormats
	visFmtDateTWNsYYYYMMDDD_C     =51         # from enum VisFieldFormats
	visFmtDateYYYYMMMDDDWWW_C     =58         # from enum VisFieldFormats
	visFmtDateYYYYMMMDDD_C        =59         # from enum VisFieldFormats
	visFmtDategeMMMMddd_K         =62         # from enum VisFieldFormats
	visFmtDategeMMMMddddww_K      =60         # from enum VisFieldFormats
	visFmtDategggemd_J            =56         # from enum VisFieldFormats
	visFmtDategggemdww_J          =54         # from enum VisFieldFormats
	visFmtDatewwyyyymd_S          =79         # from enum VisFieldFormats
	visFmtDatewwyyyymmdd_S        =78         # from enum VisFieldFormats
	visFmtDateyy_mm_dd            =65         # from enum VisFieldFormats
	visFmtDateyymmdd              =45         # from enum VisFieldFormats
	visFmtDateyyyy_m_d            =64         # from enum VisFieldFormats
	visFmtDateyyyymd              =44         # from enum VisFieldFormats
	visFmtDateyyyymd_J            =57         # from enum VisFieldFormats
	visFmtDateyyyymd_K            =63         # from enum VisFieldFormats
	visFmtDateyyyymd_S            =76         # from enum VisFieldFormats
	visFmtDateyyyymdww_J          =55         # from enum VisFieldFormats
	visFmtDateyyyymdww_K          =61         # from enum VisFieldFormats
	visFmtDateyyyymmdd_S          =77         # from enum VisFieldFormats
	visFmtDegrees                 =12         # from enum VisFieldFormats
	visFmtFeetAndInches           =10         # from enum VisFieldFormats
	visFmtFeetAndInches1Pl        =13         # from enum VisFieldFormats
	visFmtFeetAndInches2Pl        =14         # from enum VisFieldFormats
	visFmtFraction1PlDefUnits     =16         # from enum VisFieldFormats
	visFmtFraction1PlNoUnits      =15         # from enum VisFieldFormats
	visFmtFraction2PlDefUnits     =18         # from enum VisFieldFormats
	visFmtFraction2PlNoUnits      =17         # from enum VisFieldFormats
	visFmtJDateaxpxhXmmX          =48         # from enum VisFieldFormats
	visFmtJDateaxpxhmm            =47         # from enum VisFieldFormats
	visFmtJDategggeXmXdX          =42         # from enum VisFieldFormats
	visFmtJDategggeXmXdXww        =40         # from enum VisFieldFormats
	visFmtJDatehXmmX              =49         # from enum VisFieldFormats
	visFmtJDatehmmaxpx            =46         # from enum VisFieldFormats
	visFmtJDateyymmdd             =45         # from enum VisFieldFormats
	visFmtJDateyyyyXmXdX          =43         # from enum VisFieldFormats
	visFmtJDateyyyyXmXdXww        =41         # from enum VisFieldFormats
	visFmtJDateyyyymd             =44         # from enum VisFieldFormats
	visFmtMsoDateEnglish          =208        # from enum VisFieldFormats
	visFmtMsoDateISO              =204        # from enum VisFieldFormats
	visFmtMsoDateLong             =202        # from enum VisFieldFormats
	visFmtMsoDateLongDay          =201        # from enum VisFieldFormats
	visFmtMsoDateMon_Yr           =210        # from enum VisFieldFormats
	visFmtMsoDateMonthYr          =209        # from enum VisFieldFormats
	visFmtMsoDateShort            =200        # from enum VisFieldFormats
	visFmtMsoDateShortAbb         =207        # from enum VisFieldFormats
	visFmtMsoDateShortAlt         =203        # from enum VisFieldFormats
	visFmtMsoDateShortMon         =205        # from enum VisFieldFormats
	visFmtMsoDateShortSlash       =206        # from enum VisFieldFormats
	visFmtMsoFEExtra1             =217        # from enum VisFieldFormats
	visFmtMsoFEExtra2             =218        # from enum VisFieldFormats
	visFmtMsoFEExtra3             =219        # from enum VisFieldFormats
	visFmtMsoFEExtra4             =220        # from enum VisFieldFormats
	visFmtMsoFEExtra5             =221        # from enum VisFieldFormats
	visFmtMsoTime24               =215        # from enum VisFieldFormats
	visFmtMsoTimeDatePM           =211        # from enum VisFieldFormats
	visFmtMsoTimeDateSecPM        =212        # from enum VisFieldFormats
	visFmtMsoTimePM               =213        # from enum VisFieldFormats
	visFmtMsoTimeSec24            =216        # from enum VisFieldFormats
	visFmtMsoTimeSecPM            =214        # from enum VisFieldFormats
	visFmtNumGenDefUnits          =1          # from enum VisFieldFormats
	visFmtNumGenNoUnits           =0          # from enum VisFieldFormats
	visFmtRadians                 =11         # from enum VisFieldFormats
	visFmtStrLower                =38         # from enum VisFieldFormats
	visFmtStrNormal               =37         # from enum VisFieldFormats
	visFmtStrUpper                =39         # from enum VisFieldFormats
	visFmtTimeAMPM_hmm_C          =70         # from enum VisFieldFormats
	visFmtTimeAMPM_hmm_J          =68         # from enum VisFieldFormats
	visFmtTimeAMPM_hmm_K          =72         # from enum VisFieldFormats
	visFmtTimeAMPMhhmm_S          =81         # from enum VisFieldFormats
	visFmtTimeAMPMhmm_C           =66         # from enum VisFieldFormats
	visFmtTimeAMPMhmm_J           =46         # from enum VisFieldFormats
	visFmtTimeAMPMhmm_K           =67         # from enum VisFieldFormats
	visFmtTimeAMPMhmm_S           =80         # from enum VisFieldFormats
	visFmtTimeGen                 =30         # from enum VisFieldFormats
	visFmtTimeHHMM                =32         # from enum VisFieldFormats
	visFmtTimeHHMM24              =34         # from enum VisFieldFormats
	visFmtTimeHHMMAMPM            =36         # from enum VisFieldFormats
	visFmtTimeHHMMAMPM_E          =75         # from enum VisFieldFormats
	visFmtTimeHMM                 =31         # from enum VisFieldFormats
	visFmtTimeHMM24               =33         # from enum VisFieldFormats
	visFmtTimeHMMAMPM             =35         # from enum VisFieldFormats
	visFmtTimeHMMAMPM_E           =74         # from enum VisFieldFormats
	visFmtTimehmm_C               =71         # from enum VisFieldFormats
	visFmtTimehmm_J               =69         # from enum VisFieldFormats
	visFmtTimehmm_K               =73         # from enum VisFieldFormats
	visFilterMouseMoveDragBegin   =1          # from enum VisFilterActions
	visFilterMouseMoveDragDrop    =5          # from enum VisFilterActions
	visFilterMouseMoveDragEnter   =2          # from enum VisFilterActions
	visFilterMouseMoveDragLeave   =4          # from enum VisFilterActions
	visFilterMouseMoveDragOver    =3          # from enum VisFilterActions
	visFilterMouseMoveNoDrag      =0          # from enum VisFilterActions
	visFixedFormatPDF             =1          # from enum VisFixedFormatTypes
	visFixedFormatXPS             =2          # from enum VisFixedFormatTypes
	visFlipHorizontal             =1          # from enum VisFlipDirection
	visFlipVertical               =2          # from enum VisFlipDirection
	visFlipSelection              =0          # from enum VisFlipTypes
	visFlipSelectionWithPin       =1          # from enum VisFlipTypes
	visFlipShapes                 =2          # from enum VisFlipTypes
	visFont0Alias                 =128        # from enum VisFontAttributes
	visFontDevice                 =32         # from enum VisFontAttributes
	visFontRaster                 =16         # from enum VisFontAttributes
	visFontScalable               =64         # from enum VisFontAttributes
	visBegin                      =9          # from enum VisFromParts
	visBeginX                     =7          # from enum VisFromParts
	visBeginY                     =8          # from enum VisFromParts
	visBottomEdge                 =4          # from enum VisFromParts
	visCenterEdge                 =2          # from enum VisFromParts
	visConnectFromError           =-1         # from enum VisFromParts
	visControlPoint               =100        # from enum VisFromParts
	visEnd                        =12         # from enum VisFromParts
	visEndX                       =10         # from enum VisFromParts
	visEndY                       =11         # from enum VisFromParts
	visFromAngle                  =13         # from enum VisFromParts
	visFromNone                   =0          # from enum VisFromParts
	visFromPin                    =14         # from enum VisFromParts
	visLeftEdge                   =1          # from enum VisFromParts
	visMiddleEdge                 =5          # from enum VisFromParts
	visRightEdge                  =3          # from enum VisFromParts
	visTopEdge                    =6          # from enum VisFromParts
	visGeomExcludeLastPoint       =1          # from enum VisGeomFlags
	visGeomWHPct                  =16         # from enum VisGeomFlags
	visGeomXYLocal                =32         # from enum VisGeomFlags
	visGetFloats                  =0          # from enum VisGetSetArgs
	visGetFormulas                =4          # from enum VisGetSetArgs
	visGetFormulasU               =5          # from enum VisGetSetArgs
	visGetRoundedInts             =2          # from enum VisGetSetArgs
	visGetStrings                 =3          # from enum VisGetSetArgs
	visGetTruncatedInts           =1          # from enum VisGetSetArgs
	visSetBlastGuards             =2          # from enum VisGetSetArgs
	visSetFormulas                =1          # from enum VisGetSetArgs
	visSetTestCircular            =4          # from enum VisGetSetArgs
	visSetUniversalSyntax         =8          # from enum VisGetSetArgs
	visGlueToConnectionPoints     =8          # from enum VisGlueSettings
	visGlueToDisabled             =32768      # from enum VisGlueSettings
	visGlueToGeometry             =32         # from enum VisGlueSettings
	visGlueToGuides               =1          # from enum VisGlueSettings
	visGlueToHandles              =2          # from enum VisGlueSettings
	visGlueToNone                 =0          # from enum VisGlueSettings
	visGlueToVertices             =4          # from enum VisGlueSettings
	visGluedShapesAll1D           =0          # from enum VisGluedShapesFlags
	visGluedShapesAll2D           =3          # from enum VisGluedShapesFlags
	visGluedShapesIncoming1D      =1          # from enum VisGluedShapesFlags
	visGluedShapesIncoming2D      =4          # from enum VisGluedShapesFlags
	visGluedShapesOutgoing1D      =2          # from enum VisGluedShapesFlags
	visGluedShapesOutgoing2D      =5          # from enum VisGluedShapesFlags
	visGraphicExpression          =2          # from enum VisGraphicField
	visGraphicPropertyLabel       =1          # from enum VisGraphicField
	visTypeColorByValue           =5          # from enum VisGraphicItemTypes
	visTypeDataBar                =4          # from enum VisGraphicItemTypes
	visTypeHeading                =6          # from enum VisGraphicItemTypes
	visTypeIconSet                =2          # from enum VisGraphicItemTypes
	visTypeTextCallout            =3          # from enum VisGraphicItemTypes
	visGraphicCenter              =3          # from enum VisGraphicPositionHorizontal
	visGraphicFarLeft             =0          # from enum VisGraphicPositionHorizontal
	visGraphicFarRight            =6          # from enum VisGraphicPositionHorizontal
	visGraphicLeft                =2          # from enum VisGraphicPositionHorizontal
	visGraphicLeftEdge            =1          # from enum VisGraphicPositionHorizontal
	visGraphicRight               =4          # from enum VisGraphicPositionHorizontal
	visGraphicRightEdge           =5          # from enum VisGraphicPositionHorizontal
	visGraphicAbove               =6          # from enum VisGraphicPositionVertical
	visGraphicBelow               =0          # from enum VisGraphicPositionVertical
	visGraphicBottom              =2          # from enum VisGraphicPositionVertical
	visGraphicBottomEdge          =1          # from enum VisGraphicPositionVertical
	visGraphicMiddle              =3          # from enum VisGraphicPositionVertical
	visGraphicTop                 =4          # from enum VisGraphicPositionVertical
	visGraphicTopEdge             =5          # from enum VisGraphicPositionVertical
	visHorz                       =2          # from enum VisGuideTypes
	visPoint                      =1          # from enum VisGuideTypes
	visVert                       =3          # from enum VisGuideTypes
	visHitInside                  =2          # from enum VisHitTestResults
	visHitOnBoundary              =1          # from enum VisHitTestResults
	visHitOutside                 =0          # from enum VisHitTestResults
	visHorzAlignCenter            =2          # from enum VisHorizontalAlignTypes
	visHorzAlignLeft              =1          # from enum VisHorizontalAlignTypes
	visHorzAlignNone              =0          # from enum VisHorizontalAlignTypes
	visHorzAlignRight             =3          # from enum VisHorizontalAlignTypes
	visInsertAsControl            =8192       # from enum VisInsertObjArgs
	visInsertAsEmbed              =16384      # from enum VisInsertObjArgs
	visInsertDontShow             =4096       # from enum VisInsertObjArgs
	visInsertIcon                 =16         # from enum VisInsertObjArgs
	visInsertLink                 =8          # from enum VisInsertObjArgs
	visInsertNoDesignModeTransition=256        # from enum VisInsertObjArgs
	visKeyControl                 =8          # from enum VisKeyButtonFlags
	visKeyShift                   =4          # from enum VisKeyButtonFlags
	visMouseLeft                  =1          # from enum VisKeyButtonFlags
	visMouseMiddle                =16         # from enum VisKeyButtonFlags
	visMouseRight                 =2          # from enum VisKeyButtonFlags
	visLangLocal                  =0          # from enum VisLangFlags
	visLangUniversal              =1          # from enum VisLangFlags
	visCircular                   =7          # from enum VisLayoutAlgorithm
	visFlowchartBottomToTop       =5          # from enum VisLayoutAlgorithm
	visFlowchartLeftToRight       =3          # from enum VisLayoutAlgorithm
	visFlowchartRightToLeft       =6          # from enum VisLayoutAlgorithm
	visFlowchartTopToBottom       =2          # from enum VisLayoutAlgorithm
	visHierarchyBottomToTopCenter =21         # from enum VisLayoutAlgorithm
	visHierarchyBottomToTopLeft   =20         # from enum VisLayoutAlgorithm
	visHierarchyBottomToTopRight  =22         # from enum VisLayoutAlgorithm
	visHierarchyLeftToRightBottom =25         # from enum VisLayoutAlgorithm
	visHierarchyLeftToRightMiddle =24         # from enum VisLayoutAlgorithm
	visHierarchyLeftToRightTop    =23         # from enum VisLayoutAlgorithm
	visHierarchyRightToLeftBottom =28         # from enum VisLayoutAlgorithm
	visHierarchyRightToLeftMiddle =27         # from enum VisLayoutAlgorithm
	visHierarchyRightToLeftTop    =26         # from enum VisLayoutAlgorithm
	visHierarchyTopToBottomCenter =18         # from enum VisLayoutAlgorithm
	visHierarchyTopToBottomLeft   =17         # from enum VisLayoutAlgorithm
	visHierarchyTopToBottomRight  =19         # from enum VisLayoutAlgorithm
	visPageDefault                =1          # from enum VisLayoutAlgorithm
	visParentDefault              =16         # from enum VisLayoutAlgorithm
	visRadial                     =4          # from enum VisLayoutAlgorithm
	visWideTreeDownLeft           =15         # from enum VisLayoutAlgorithm
	visWideTreeDownRight          =8          # from enum VisLayoutAlgorithm
	visWideTreeLeftDown           =14         # from enum VisLayoutAlgorithm
	visWideTreeLeftUp             =13         # from enum VisLayoutAlgorithm
	visWideTreeRightDown          =9          # from enum VisLayoutAlgorithm
	visWideTreeRightUp            =10         # from enum VisLayoutAlgorithm
	visWideTreeUpLeft             =12         # from enum VisLayoutAlgorithm
	visWideTreeUpRight            =11         # from enum VisLayoutAlgorithm
	visLayoutDirFlipHorz          =3          # from enum VisLayoutDirection
	visLayoutDirFlipVert          =2          # from enum VisLayoutDirection
	visLayoutDirRotateLeft        =1          # from enum VisLayoutDirection
	visLayoutDirRotateRight       =0          # from enum VisLayoutDirection
	visLayoutHorzAlignCenter      =3          # from enum VisLayoutHorzAlignType
	visLayoutHorzAlignDefault     =1          # from enum VisLayoutHorzAlignType
	visLayoutHorzAlignLeft        =2          # from enum VisLayoutHorzAlignType
	visLayoutHorzAlignNone        =0          # from enum VisLayoutHorzAlignType
	visLayoutHorzAlignRight       =4          # from enum VisLayoutHorzAlignType
	visLayoutIncrAlign            =1          # from enum VisLayoutIncrementalType
	visLayoutIncrSpace            =2          # from enum VisLayoutIncrementalType
	visLayoutVertAlignBottom      =4          # from enum VisLayoutVertAlignType
	visLayoutVertAlignDefault     =1          # from enum VisLayoutVertAlignType
	visLayoutVertAlignMiddle      =3          # from enum VisLayoutVertAlignType
	visLayoutVertAlignNone        =0          # from enum VisLayoutVertAlignType
	visLayoutVertAlignTop         =2          # from enum VisLayoutVertAlignType
	visLegendNoContents           =1          # from enum VisLegendFlags
	visLegendPopulate             =0          # from enum VisLegendFlags
	visLinkReplaceAlways          =1          # from enum VisLinkReplaceBehavior
	visLinkReplaceNever           =0          # from enum VisLinkReplaceBehavior
	visLinkReplacePrompt          =2          # from enum VisLinkReplaceBehavior
	visListAlignCenterOrMiddle    =1          # from enum VisListAlignment
	visListAlignLeftOrTop         =0          # from enum VisListAlignment
	visListAlignRightOrBottom     =2          # from enum VisListAlignment
	visListDirBottomToTop         =3          # from enum VisListDirection
	visListDirLeftToRight         =0          # from enum VisListDirection
	visListDirRightToLeft         =1          # from enum VisListDirection
	visListDirTopToBottom         =2          # from enum VisListDirection
	visAutomatic                  =1          # from enum VisMasterProperties
	visCenter                     =2          # from enum VisMasterProperties
	visDouble                     =4          # from enum VisMasterProperties
	visIconFormatBMP              =2          # from enum VisMasterProperties
	visIconFormatVisio            =0          # from enum VisMasterProperties
	visLeft                       =1          # from enum VisMasterProperties
	visManual                     =0          # from enum VisMasterProperties
	visMasFPCenter                =4096       # from enum VisMasterProperties
	visMasFPScale                 =16384      # from enum VisMasterProperties
	visMasFPStretch               =8192       # from enum VisMasterProperties
	visMasFPTile                  =0          # from enum VisMasterProperties
	visMasIsFillPat               =4          # from enum VisMasterProperties
	visMasIsLineEnd               =2          # from enum VisMasterProperties
	visMasIsLinePat               =1          # from enum VisMasterProperties
	visMasLEDefault               =0          # from enum VisMasterProperties
	visMasLEScale                 =1024       # from enum VisMasterProperties
	visMasLEUpright               =256        # from enum VisMasterProperties
	visMasLPAnnotate              =48         # from enum VisMasterProperties
	visMasLPScale                 =64         # from enum VisMasterProperties
	visMasLPStretch               =32         # from enum VisMasterProperties
	visMasLPTile                  =16         # from enum VisMasterProperties
	visMasLPTileDeform            =0          # from enum VisMasterProperties
	visNormal                     =1          # from enum VisMasterProperties
	visRight                      =3          # from enum VisMasterProperties
	visTall                       =2          # from enum VisMasterProperties
	visWide                       =3          # from enum VisMasterProperties
	visTypeDataGraphic            =5          # from enum VisMasterTypes
	visTypeFillPattern            =2          # from enum VisMasterTypes
	visTypeLineEnd                =4          # from enum VisMasterTypes
	visTypeLinePattern            =3          # from enum VisMasterTypes
	visTypeMaster                 =1          # from enum VisMasterTypes
	visTypeThemeColors            =6          # from enum VisMasterTypes
	visTypeThemeEffects           =7          # from enum VisMasterTypes
	visMSDefault                  =0          # from enum VisMeasurementSystem
	visMSMetric                   =1          # from enum VisMeasurementSystem
	visMSUS                       =2          # from enum VisMeasurementSystem
	visMemberAddDoNotExpand       =2          # from enum VisMemberAddOptions
	visMemberAddExpandContainer   =1          # from enum VisMemberAddOptions
	visMemberAddUseResizeSetting  =0          # from enum VisMemberAddOptions
	visMouseMoveDragStatesBegin   =1          # from enum VisMouseMoveDragStates
	visMouseMoveDragStatesDrop    =5          # from enum VisMouseMoveDragStates
	visMouseMoveDragStatesEnter   =2          # from enum VisMouseMoveDragStates
	visMouseMoveDragStatesLeave   =4          # from enum VisMouseMoveDragStates
	visMouseMoveDragStatesNone    =0          # from enum VisMouseMoveDragStates
	visMouseMoveDragStatesOver    =3          # from enum VisMouseMoveDragStates
	visObjTypeAddon               =31         # from enum VisObjectTypes
	visObjTypeAddons              =32         # from enum VisObjectTypes
	visObjTypeApp                 =3          # from enum VisObjectTypes
	visObjTypeApplicationSettings =51         # from enum VisObjectTypes
	visObjTypeCell                =4          # from enum VisObjectTypes
	visObjTypeChars               =5          # from enum VisObjectTypes
	visObjTypeColor               =29         # from enum VisObjectTypes
	visObjTypeColors              =30         # from enum VisObjectTypes
	visObjTypeComment             =74         # from enum VisObjectTypes
	visObjTypeComments            =73         # from enum VisObjectTypes
	visObjTypeConnect             =8          # from enum VisObjectTypes
	visObjTypeConnects            =9          # from enum VisObjectTypes
	visObjTypeContainerProperties =60         # from enum VisObjectTypes
	visObjTypeCurve               =42         # from enum VisObjectTypes
	visObjTypeDataColumn          =56         # from enum VisObjectTypes
	visObjTypeDataColumns         =55         # from enum VisObjectTypes
	visObjTypeDataConnection      =54         # from enum VisObjectTypes
	visObjTypeDataRecordset       =53         # from enum VisObjectTypes
	visObjTypeDataRecordsetChangedEvent=57         # from enum VisObjectTypes
	visObjTypeDataRecordsets      =52         # from enum VisObjectTypes
	visObjTypeDoc                 =10         # from enum VisObjectTypes
	visObjTypeDocs                =11         # from enum VisObjectTypes
	visObjTypeEvent               =33         # from enum VisObjectTypes
	visObjTypeEventList           =34         # from enum VisObjectTypes
	visObjTypeFont                =27         # from enum VisObjectTypes
	visObjTypeFonts               =28         # from enum VisObjectTypes
	visObjTypeGlobal              =36         # from enum VisObjectTypes
	visObjTypeGraphicItem         =59         # from enum VisObjectTypes
	visObjTypeGraphicItems        =58         # from enum VisObjectTypes
	visObjTypeHyperlink           =37         # from enum VisObjectTypes
	visObjTypeHyperlinks          =43         # from enum VisObjectTypes
	visObjTypeKeyboardEvent       =50         # from enum VisObjectTypes
	visObjTypeLayer               =25         # from enum VisObjectTypes
	visObjTypeLayers              =26         # from enum VisObjectTypes
	visObjTypeMSGWrap             =48         # from enum VisObjectTypes
	visObjTypeMaster              =12         # from enum VisObjectTypes
	visObjTypeMasterShortcut      =47         # from enum VisObjectTypes
	visObjTypeMasterShortcuts     =46         # from enum VisObjectTypes
	visObjTypeMasters             =13         # from enum VisObjectTypes
	visObjTypeMouseEvent          =49         # from enum VisObjectTypes
	visObjTypeMovedSelectionEvent =62         # from enum VisObjectTypes
	visObjTypeOLEObject           =39         # from enum VisObjectTypes
	visObjTypeOLEObjects          =38         # from enum VisObjectTypes
	visObjTypePage                =14         # from enum VisObjectTypes
	visObjTypePages               =15         # from enum VisObjectTypes
	visObjTypePath                =41         # from enum VisObjectTypes
	visObjTypePaths               =40         # from enum VisObjectTypes
	visObjTypeRelatedShapePairEvent=61         # from enum VisObjectTypes
	visObjTypeReplaceShapesEvent  =71         # from enum VisObjectTypes
	visObjTypeRow                 =45         # from enum VisObjectTypes
	visObjTypeSection             =44         # from enum VisObjectTypes
	visObjTypeSelection           =16         # from enum VisObjectTypes
	visObjTypeServerPublishOptions=63         # from enum VisObjectTypes
	visObjTypeShape               =17         # from enum VisObjectTypes
	visObjTypeShapes              =18         # from enum VisObjectTypes
	visObjTypeStyle               =19         # from enum VisObjectTypes
	visObjTypeStyles              =20         # from enum VisObjectTypes
	visObjTypeUnknown             =1          # from enum VisObjectTypes
	visObjTypeValidation          =64         # from enum VisObjectTypes
	visObjTypeValidationIssue     =70         # from enum VisObjectTypes
	visObjTypeValidationIssues    =69         # from enum VisObjectTypes
	visObjTypeValidationRule      =68         # from enum VisObjectTypes
	visObjTypeValidationRuleSet   =66         # from enum VisObjectTypes
	visObjTypeValidationRuleSets  =65         # from enum VisObjectTypes
	visObjTypeValidationRules     =67         # from enum VisObjectTypes
	visObjTypeWindow              =21         # from enum VisObjectTypes
	visObjTypeWindows             =22         # from enum VisObjectTypes
	visComponentStateModal        =1          # from enum VisOnComponentEnterCodes
	visModalDeferEvents           =65536      # from enum VisOnComponentEnterCodes
	visModalDisableVisiosFrame    =524288     # from enum VisOnComponentEnterCodes
	visModalDontBlockMessages     =262144     # from enum VisOnComponentEnterCodes
	visModalNoBeforeAfter         =131072     # from enum VisOnComponentEnterCodes
	visAddDeclineAutoRefresh      =1024       # from enum VisOpenSaveArgs
	visAddDocked                  =4          # from enum VisOpenSaveArgs
	visAddHidden                  =64         # from enum VisOpenSaveArgs
	visAddMacrosDisabled          =128        # from enum VisOpenSaveArgs
	visAddMinimized               =16         # from enum VisOpenSaveArgs
	visAddNoWorkspace             =256        # from enum VisOpenSaveArgs
	visAddStencil                 =512        # from enum VisOpenSaveArgs
	visOpenCopy                   =1          # from enum VisOpenSaveArgs
	visOpenCopyOfNaming           =2048       # from enum VisOpenSaveArgs
	visOpenDeclineAutoRefresh     =1024       # from enum VisOpenSaveArgs
	visOpenDocked                 =4          # from enum VisOpenSaveArgs
	visOpenDontList               =8          # from enum VisOpenSaveArgs
	visOpenHidden                 =64         # from enum VisOpenSaveArgs
	visOpenMacrosDisabled         =128        # from enum VisOpenSaveArgs
	visOpenMinimized              =16         # from enum VisOpenSaveArgs
	visOpenNoWorkspace            =256        # from enum VisOpenSaveArgs
	visOpenRO                     =2          # from enum VisOpenSaveArgs
	visOpenRW                     =32         # from enum VisOpenSaveArgs
	visSaveAsCheckCompatibility   =8          # from enum VisOpenSaveArgs
	visSaveAsListInMRU            =4          # from enum VisOpenSaveArgs
	visSaveAsRO                   =1          # from enum VisOpenSaveArgs
	visSaveAsWS                   =2          # from enum VisOpenSaveArgs
	visSavePrevDetailed1st        =2          # from enum VisOpenSaveArgs
	visSavePrevDetailedAll        =8          # from enum VisOpenSaveArgs
	visSavePrevDraft1st           =1          # from enum VisOpenSaveArgs
	visSavePrevDraftAll           =4          # from enum VisOpenSaveArgs
	visSavePrevNone               =0          # from enum VisOpenSaveArgs
	visInvalMasterID              =-1         # from enum VisPageAndMasterIDs
	visInvalPageID                =-1         # from enum VisPageAndMasterIDs
	visNeverResizePages           =0          # from enum VisPageSizingBehaviors
	visResizePages                =1          # from enum VisPageSizingBehaviors
	visPageTypeInval              =0          # from enum VisPageTypes
	visTypeBackground             =2          # from enum VisPageTypes
	visTypeForeground             =1          # from enum VisPageTypes
	visTypeMarkup                 =3          # from enum VisPageTypes
	visPaperSizeA3                =8          # from enum VisPaperSizes
	visPaperSizeA4                =9          # from enum VisPaperSizes
	visPaperSizeA5                =11         # from enum VisPaperSizes
	visPaperSizeB4                =12         # from enum VisPaperSizes
	visPaperSizeB5                =13         # from enum VisPaperSizes
	visPaperSizeC                 =24         # from enum VisPaperSizes
	visPaperSizeD                 =25         # from enum VisPaperSizes
	visPaperSizeE                 =26         # from enum VisPaperSizes
	visPaperSizeFolio             =14         # from enum VisPaperSizes
	visPaperSizeLegal             =5          # from enum VisPaperSizes
	visPaperSizeLetter            =1          # from enum VisPaperSizes
	visPaperSizeNote              =18         # from enum VisPaperSizes
	visPaperSizeUnknown           =0          # from enum VisPaperSizes
	visPasteBitmap                =2          # from enum VisPasteSpecialCodes
	visPasteDIB                   =8          # from enum VisPasteSpecialCodes
	visPasteEMF                   =14         # from enum VisPasteSpecialCodes
	visPasteHyperlink             =65538      # from enum VisPasteSpecialCodes
	visPasteInk                   =65544      # from enum VisPasteSpecialCodes
	visPasteMetafile              =3          # from enum VisPasteSpecialCodes
	visPasteOEMText               =7          # from enum VisPasteSpecialCodes
	visPasteOLEObject             =65536      # from enum VisPasteSpecialCodes
	visPasteRichText              =65537      # from enum VisPasteSpecialCodes
	visPasteText                  =1          # from enum VisPasteSpecialCodes
	visPasteURL                   =65539      # from enum VisPasteSpecialCodes
	visPasteVisioIcon             =65543      # from enum VisPasteSpecialCodes
	visPasteVisioMasters          =65541      # from enum VisPasteSpecialCodes
	visPasteVisioMastersXML       =65546      # from enum VisPasteSpecialCodes
	visPasteVisioShapes           =65540      # from enum VisPasteSpecialCodes
	visPasteVisioShapesWithoutDataLinks=65548      # from enum VisPasteSpecialCodes
	visPasteVisioShapesXML        =65545      # from enum VisPasteSpecialCodes
	visPasteVisioText             =65542      # from enum VisPasteSpecialCodes
	visKeyComposite               =3          # from enum VisPrimaryKeySettings
	visKeyRowOrder                =1          # from enum VisPrimaryKeySettings
	visKeySingle                  =2          # from enum VisPrimaryKeySettings
	visPrintAll                   =0          # from enum VisPrintOutRange
	visPrintCurrentPage           =2          # from enum VisPrintOutRange
	visPrintCurrentView           =4          # from enum VisPrintOutRange
	visPrintFromTo                =1          # from enum VisPrintOutRange
	visPrintSelection             =3          # from enum VisPrintOutRange
	visProtectBackgrounds         =8          # from enum VisProtection
	visProtectMasters             =4          # from enum VisProtection
	visProtectNone                =0          # from enum VisProtection
	visProtectPreviews            =16         # from enum VisProtection
	visProtectShapes              =2          # from enum VisProtection
	visProtectStyles              =1          # from enum VisProtection
	visPublishDataRecordsetAll    =0          # from enum VisPublishDataRecordsets
	visPublishDataRecordsetNone   =1          # from enum VisPublishDataRecordsets
	visPublishDataRecordsetSelect =2          # from enum VisPublishDataRecordsets
	visPublishPageAll             =0          # from enum VisPublishPages
	visPublishPageSelect          =1          # from enum VisPublishPages
	visQuickStyleColorAccent1     =2          # from enum VisQuickStyleColors
	visQuickStyleColorAccent2     =3          # from enum VisQuickStyleColors
	visQuickStyleColorAccent3     =4          # from enum VisQuickStyleColors
	visQuickStyleColorAccent4     =5          # from enum VisQuickStyleColors
	visQuickStyleColorAccent5     =6          # from enum VisQuickStyleColors
	visQuickStyleColorAccent6     =7          # from enum VisQuickStyleColors
	visQuickStyleColorBackground  =8          # from enum VisQuickStyleColors
	visQuickStyleColorDark        =0          # from enum VisQuickStyleColors
	visQuickStyleColorLight       =1          # from enum VisQuickStyleColors
	visQuickStyleColorVariant1    =100        # from enum VisQuickStyleColors
	visQuickStyleColorVariant2    =101        # from enum VisQuickStyleColors
	visQuickStyleColorVariant3    =102        # from enum VisQuickStyleColors
	visQuickStyleColorVariant4    =103        # from enum VisQuickStyleColors
	visQuickStyleColorVariant5    =104        # from enum VisQuickStyleColors
	visQuickStyleColorVariant6    =105        # from enum VisQuickStyleColors
	visQuickStyleColorVariant7    =106        # from enum VisQuickStyleColors
	visQuickStyleMatrixNone       =0          # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixTheme1     =1          # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixTheme2     =2          # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixTheme3     =3          # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixTheme4     =4          # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixTheme5     =5          # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixTheme6     =6          # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixVariant1   =100        # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixVariant2   =101        # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixVariant3   =102        # from enum VisQuickStyleMatrixIndices
	visQuickStyleMatrixVariant4   =103        # from enum VisQuickStyleMatrixIndices
	visRaster16Bit                =10         # from enum VisRasterExportColorFormat
	visRaster16Color              =1          # from enum VisRasterExportColorFormat
	visRaster16ColorGrayScale     =8          # from enum VisRasterExportColorFormat
	visRaster24Bit                =3          # from enum VisRasterExportColorFormat
	visRaster256Color             =2          # from enum VisRasterExportColorFormat
	visRaster256ColorGrayScale    =9          # from enum VisRasterExportColorFormat
	visRasterBiLevel              =0          # from enum VisRasterExportColorFormat
	visRasterCMYK                 =7          # from enum VisRasterExportColorFormat
	visRasterGrayScale            =6          # from enum VisRasterExportColorFormat
	visRasterRGB                  =4          # from enum VisRasterExportColorFormat
	visRasterYCC                  =5          # from enum VisRasterExportColorFormat
	visRasterAdaptive             =0          # from enum VisRasterExportColorReduction
	visRasterDiffusion            =1          # from enum VisRasterExportColorReduction
	visRasterHalftone             =2          # from enum VisRasterExportColorReduction
	visRasterGroup3               =2          # from enum VisRasterExportDataCompression
	visRasterGroup4               =4          # from enum VisRasterExportDataCompression
	visRasterLZW                  =5          # from enum VisRasterExportDataCompression
	visRasterModifiedHuffman      =6          # from enum VisRasterExportDataCompression
	visRasterNone                 =0          # from enum VisRasterExportDataCompression
	visRasterPackbits             =3          # from enum VisRasterExportDataCompression
	visRasterRLE                  =1          # from enum VisRasterExportDataCompression
	visRasterInterlace            =0          # from enum VisRasterExportDataFormat
	visRasterNonInterlace         =1          # from enum VisRasterExportDataFormat
	visRasterFlipHorizontal       =1          # from enum VisRasterExportFlip
	visRasterFlipVertical         =2          # from enum VisRasterExportFlip
	visRasterNoFlip               =0          # from enum VisRasterExportFlip
	visRasterBaseline             =0          # from enum VisRasterExportOperation
	visRasterProgressive          =1          # from enum VisRasterExportOperation
	visRasterUseCustomResolution  =3          # from enum VisRasterExportResolution
	visRasterUsePrinterResolution =1          # from enum VisRasterExportResolution
	visRasterUseScreenResolution  =0          # from enum VisRasterExportResolution
	visRasterUseSourceResolution  =2          # from enum VisRasterExportResolution
	visRasterPixelsPerCm          =1          # from enum VisRasterExportResolutionUnits
	visRasterPixelsPerInch        =0          # from enum VisRasterExportResolutionUnits
	visRasterNoRotation           =0          # from enum VisRasterExportRotation
	visRasterRotateLeft           =1          # from enum VisRasterExportRotation
	visRasterRotateRight          =2          # from enum VisRasterExportRotation
	visRasterFitToCustomSize      =3          # from enum VisRasterExportSize
	visRasterFitToPrinterSize     =1          # from enum VisRasterExportSize
	visRasterFitToScreenSize      =0          # from enum VisRasterExportSize
	visRasterFitToSourceSize      =2          # from enum VisRasterExportSize
	visRasterCm                   =1          # from enum VisRasterExportSizeUnits
	visRasterInch                 =2          # from enum VisRasterExportSizeUnits
	visRasterPixel                =0          # from enum VisRasterExportSizeUnits
	visFieldMappedAllCallouts     =3          # from enum VisRecordsetFieldStatus
	visFieldMappedNoCallouts      =1          # from enum VisRecordsetFieldStatus
	visFieldMappedSomeCallouts    =2          # from enum VisRecordsetFieldStatus
	visFieldNotMapped             =0          # from enum VisRecordsetFieldStatus
	visRefreshNoReconcilationUI   =2          # from enum VisRefreshSettings
	visRefreshOverwriteAll        =1          # from enum VisRefreshSettings
	VisRegionalUIOptionsHide      =0          # from enum VisRegionalUIOptions
	VisRegionalUIOptionsShow      =1          # from enum VisRegionalUIOptions
	VisRegionalUIOptionsUseSystemSettings=65535      # from enum VisRegionalUIOptions
	visRHIDataRecordsets          =16         # from enum VisRemoveHiddenInfoItems
	visRHIMasters                 =4          # from enum VisRemoveHiddenInfoItems
	visRHINone                    =0          # from enum VisRemoveHiddenInfoItems
	visRHIPersonalInfo            =1          # from enum VisRemoveHiddenInfoItems
	visRHIPreview                 =2          # from enum VisRemoveHiddenInfoItems
	visRHIStyles                  =8          # from enum VisRemoveHiddenInfoItems
	visRHIValidationRules         =32         # from enum VisRemoveHiddenInfoItems
	visReplaceShapeDefault        =0          # from enum VisReplaceFlags
	visReplaceShapeKeepBasic      =1          # from enum VisReplaceFlags
	visReplaceShapeLockFormat     =8          # from enum VisReplaceFlags
	visReplaceShapeLockShapeData  =4          # from enum VisReplaceFlags
	visReplaceShapeLockText       =2          # from enum VisReplaceFlags
	visResizeDirE                 =0          # from enum VisResizeDirection
	visResizeDirN                 =2          # from enum VisResizeDirection
	visResizeDirNE                =1          # from enum VisResizeDirection
	visResizeDirNW                =3          # from enum VisResizeDirection
	visResizeDirS                 =6          # from enum VisResizeDirection
	visResizeDirSE                =7          # from enum VisResizeDirection
	visResizeDirSW                =5          # from enum VisResizeDirection
	visResizeDirW                 =4          # from enum VisResizeDirection
	visRXModeDrawing              =1          # from enum VisRibbonXModes
	visRXModeNone                 =0          # from enum VisRibbonXModes
	visRXModePrintPreview         =4          # from enum VisRibbonXModes
	visRXModeStencil              =2          # from enum VisRibbonXModes
	visRoleSelCallout             =4          # from enum VisRoleSelectionTypes
	visRoleSelConnector           =1          # from enum VisRoleSelectionTypes
	visRoleSelContainer           =2          # from enum VisRoleSelectionTypes
	visRotateSelection            =0          # from enum VisRotationTypes
	visRotateSelectionWithPin     =1          # from enum VisRotationTypes
	visRotateShapes               =2          # from enum VisRotationTypes
	visRound                      =1          # from enum VisRoundFlags
	visTruncate                   =0          # from enum VisRoundFlags
	visRow1stHyperlink            =0          # from enum VisRowIndices
	visRow3DRotationProperties    =30         # from enum VisRowIndices
	visRowAction                  =0          # from enum VisRowIndices
	visRowAlign                   =14         # from enum VisRowIndices
	visRowAnnotation              =0          # from enum VisRowIndices
	visRowBevelProperties         =29         # from enum VisRowIndices
	visRowCharacter               =0          # from enum VisRowIndices
	visRowComponent               =0          # from enum VisRowIndices
	visRowConnectionPts           =0          # from enum VisRowIndices
	visRowControl                 =0          # from enum VisRowIndices
	visRowData123                 =16         # from enum VisRowIndices
	visRowDgmSemanticsLayoutProperties=33         # from enum VisRowIndices
	visRowDoc                     =20         # from enum VisRowIndices
	visRowEvent                   =5          # from enum VisRowIndices
	visRowExport                  =0          # from enum VisRowIndices
	visRowField                   =0          # from enum VisRowIndices
	visRowFill                    =3          # from enum VisRowIndices
	visRowFirst                   =0          # from enum VisRowIndices
	visRowForeign                 =9          # from enum VisRowIndices
	visRowFormat                  =0          # from enum VisRowIndices
	visRowGradientProperties      =26         # from enum VisRowIndices
	visRowGradientStop            =0          # from enum VisRowIndices
	visRowGroup                   =22         # from enum VisRowIndices
	visRowGuide                   =7          # from enum VisRowIndices
	visRowHelpCopyright           =16         # from enum VisRowIndices
	visRowHyperlink               =19         # from enum VisRowIndices
	visRowImage                   =21         # from enum VisRowIndices
	visRowInval                   =-1         # from enum VisRowIndices
	visRowLast                    =-2         # from enum VisRowIndices
	visRowLayer                   =0          # from enum VisRowIndices
	visRowLayerMem                =6          # from enum VisRowIndices
	visRowLine                    =2          # from enum VisRowIndices
	visRowLock                    =15         # from enum VisRowIndices
	visRowMember                  =0          # from enum VisRowIndices
	visRowMisc                    =17         # from enum VisRowIndices
	visRowNone                    =-1         # from enum VisRowIndices
	visRowOtherEffectProperties   =28         # from enum VisRowIndices
	visRowPage                    =10         # from enum VisRowIndices
	visRowPageLayout              =24         # from enum VisRowIndices
	visRowParagraph               =0          # from enum VisRowIndices
	visRowPrintProperties         =25         # from enum VisRowIndices
	visRowProp                    =0          # from enum VisRowIndices
	visRowQuickStyleProperties    =27         # from enum VisRowIndices
	visRowReplaceBehaviors        =32         # from enum VisRowIndices
	visRowReviewer                =0          # from enum VisRowIndices
	visRowRulerGrid               =18         # from enum VisRowIndices
	visRowScratch                 =0          # from enum VisRowIndices
	visRowShapeLayout             =23         # from enum VisRowIndices
	visRowSmartTag                =0          # from enum VisRowIndices
	visRowStyle                   =8          # from enum VisRowIndices
	visRowTab                     =0          # from enum VisRowIndices
	visRowText                    =11         # from enum VisRowIndices
	visRowTextXForm               =12         # from enum VisRowIndices
	visRowThemeProperties         =31         # from enum VisRowIndices
	visRowUser                    =0          # from enum VisRowIndices
	visRowVertex                  =1          # from enum VisRowIndices
	visRowXForm1D                 =4          # from enum VisRowIndices
	visRowXFormIn                 =1          # from enum VisRowIndices
	visRowXFormOut                =1          # from enum VisRowIndices
	visTagArcTo                   =140        # from enum VisRowTags
	visTagBase                    =130        # from enum VisRowTags
	visTagCnnctNamed              =185        # from enum VisRowTags
	visTagCnnctNamedABCD          =187        # from enum VisRowTags
	visTagCnnctPt                 =153        # from enum VisRowTags
	visTagCnnctPtABCD             =186        # from enum VisRowTags
	visTagComponent               =137        # from enum VisRowTags
	visTagCtlPt                   =162        # from enum VisRowTags
	visTagCtlPtTip                =170        # from enum VisRowTags
	visTagDefault                 =0          # from enum VisRowTags
	visTagEllipse                 =143        # from enum VisRowTags
	visTagEllipticalArcTo         =144        # from enum VisRowTags
	visTagInfiniteLine            =141        # from enum VisRowTags
	visTagInvalid                 =-1         # from enum VisRowTags
	visTagLineTo                  =139        # from enum VisRowTags
	visTagMoveTo                  =138        # from enum VisRowTags
	visTagNURBSTo                 =195        # from enum VisRowTags
	visTagPolylineTo              =193        # from enum VisRowTags
	visTagRelCubBezTo             =236        # from enum VisRowTags
	visTagRelEllipticalArcTo      =240        # from enum VisRowTags
	visTagRelLineTo               =239        # from enum VisRowTags
	visTagRelMoveTo               =238        # from enum VisRowTags
	visTagRelQuadBezTo            =237        # from enum VisRowTags
	visTagRowVoid                 =180        # from enum VisRowTags
	visTagSplineBeg               =165        # from enum VisRowTags
	visTagSplineSpan              =166        # from enum VisRowTags
	visTagTab0                    =136        # from enum VisRowTags
	visTagTab10                   =151        # from enum VisRowTags
	visTagTab2                    =150        # from enum VisRowTags
	visTagTab60                   =181        # from enum VisRowTags
	visRuleSetDefault             =0          # from enum VisRuleSetFlags
	visRuleSetHidden              =1          # from enum VisRuleSetFlags
	visRuleTargetDocument         =2          # from enum VisRuleTargets
	visRuleTargetPage             =1          # from enum VisRuleTargets
	visRuleTargetShape            =0          # from enum VisRuleTargets
	visCharPropRow                =1          # from enum VisRunTypes
	visFieldRun                   =20         # from enum VisRunTypes
	visParaPropRow                =2          # from enum VisRunTypes
	visParaRun                    =11         # from enum VisRunTypes
	visTabPropRow                 =3          # from enum VisRunTypes
	visWordRun                    =10         # from enum VisRunTypes
	visSVGExcludeVisioElements    =1          # from enum VisSVGExportFormat
	visSVGIncludeVisioElements    =0          # from enum VisSVGExportFormat
	visSavePreviewDetailed1st     =2          # from enum VisSavePreviewMode
	visSavePreviewDetailedAll     =8          # from enum VisSavePreviewMode
	visSavePreviewDraft1st        =1          # from enum VisSavePreviewMode
	visSavePreviewDraftAll        =4          # from enum VisSavePreviewMode
	visSavePreviewNone            =0          # from enum VisSavePreviewMode
	visScrollBarBoth              =5          # from enum VisScrollbarStates
	visScrollBarHoriz             =1          # from enum VisScrollbarStates
	visScrollBarNeither           =0          # from enum VisScrollbarStates
	visScrollBarVert              =4          # from enum VisScrollbarStates
	visSectionAction              =240        # from enum VisSectionIndices
	visSectionAnnotation          =246        # from enum VisSectionIndices
	visSectionCharacter           =3          # from enum VisSectionIndices
	visSectionConnectionPts       =7          # from enum VisSectionIndices
	visSectionControls            =9          # from enum VisSectionIndices
	visSectionDgmSemantics        =250        # from enum VisSectionIndices
	visSectionExport              =7          # from enum VisSectionIndices
	visSectionFillGradientStops   =249        # from enum VisSectionIndices
	visSectionFirst               =0          # from enum VisSectionIndices
	visSectionFirstComponent      =10         # from enum VisSectionIndices
	visSectionHyperlink           =244        # from enum VisSectionIndices
	visSectionInval               =255        # from enum VisSectionIndices
	visSectionLast                =252        # from enum VisSectionIndices
	visSectionLastComponent       =239        # from enum VisSectionIndices
	visSectionLastReal            =247        # from enum VisSectionIndices
	visSectionLayer               =241        # from enum VisSectionIndices
	visSectionLineGradientStops   =248        # from enum VisSectionIndices
	visSectionMember              =2          # from enum VisSectionIndices
	visSectionNone                =255        # from enum VisSectionIndices
	visSectionObject              =1          # from enum VisSectionIndices
	visSectionParagraph           =4          # from enum VisSectionIndices
	visSectionProp                =243        # from enum VisSectionIndices
	visSectionReviewer            =245        # from enum VisSectionIndices
	visSectionScratch             =6          # from enum VisSectionIndices
	visSectionSmartTag            =247        # from enum VisSectionIndices
	visSectionTab                 =5          # from enum VisSectionIndices
	visSectionTextField           =8          # from enum VisSectionIndices
	visSectionUser                =242        # from enum VisSectionIndices
	visDeselect                   =1          # from enum VisSelectArgs
	visDeselectAll                =256        # from enum VisSelectArgs
	visSelect                     =2          # from enum VisSelectArgs
	visSelectAll                  =4          # from enum VisSelectArgs
	visSubSelect                  =3          # from enum VisSelectArgs
	visSelIsPrimaryItem           =1          # from enum VisSelectItemStatus
	visSelIsSubItem               =2          # from enum VisSelectItemStatus
	visSelIsSuperItem             =4          # from enum VisSelectItemStatus
	visSelModeOnlySub             =2048       # from enum VisSelectMode
	visSelModeOnlySuper           =512        # from enum VisSelectMode
	visSelModeSkipSub             =1024       # from enum VisSelectMode
	visSelModeSkipSuper           =256        # from enum VisSelectMode
	visSelTypeAll                 =1          # from enum VisSelectionTypes
	visSelTypeByDataGraphic       =6          # from enum VisSelectionTypes
	visSelTypeByLayer             =3          # from enum VisSelectionTypes
	visSelTypeByMaster            =5          # from enum VisSelectionTypes
	visSelTypeByRole              =7          # from enum VisSelectionTypes
	visSelTypeByType              =4          # from enum VisSelectionTypes
	visSelTypeEmpty               =0          # from enum VisSelectionTypes
	visSelTypeSingle              =2          # from enum VisSelectionTypes
	visInvalShapeID               =-1         # from enum VisShapeIDs
	visPageSheetID                =0          # from enum VisShapeIDs
	visTypeBitmap                 =32         # from enum VisShapeTypes
	visTypeDoc                    =6          # from enum VisShapeTypes
	visTypeForeignObject          =4          # from enum VisShapeTypes
	visTypeGroup                  =2          # from enum VisShapeTypes
	visTypeGuide                  =5          # from enum VisShapeTypes
	visTypeInk                    =64         # from enum VisShapeTypes
	visTypeInval                  =0          # from enum VisShapeTypes
	visTypeIsControl              =1024       # from enum VisShapeTypes
	visTypeIsEmbedded             =512        # from enum VisShapeTypes
	visTypeIsLinked               =256        # from enum VisShapeTypes
	visTypeIsOLE2                 =32768      # from enum VisShapeTypes
	visTypeMetafile               =16         # from enum VisShapeTypes
	visTypePage                   =1          # from enum VisShapeTypes
	visTypeShape                  =3          # from enum VisShapeTypes
	visSnapExtAlignmentBoxExtension=1          # from enum VisSnapExtensions
	visSnapExtCenterAxes          =2          # from enum VisSnapExtensions
	visSnapExtCurveExtension      =64         # from enum VisSnapExtensions
	visSnapExtCurveTangent        =4          # from enum VisSnapExtensions
	visSnapExtEllipseCenter       =2048       # from enum VisSnapExtensions
	visSnapExtEndpoint            =8          # from enum VisSnapExtensions
	visSnapExtEndpointHorizontal  =512        # from enum VisSnapExtensions
	visSnapExtEndpointPerpendicular=128        # from enum VisSnapExtensions
	visSnapExtEndpointVertical    =1024       # from enum VisSnapExtensions
	visSnapExtIsometricAngles     =4096       # from enum VisSnapExtensions
	visSnapExtLinearExtension     =32         # from enum VisSnapExtensions
	visSnapExtMidpoint            =16         # from enum VisSnapExtensions
	visSnapExtMidpointPerpendicular=256        # from enum VisSnapExtensions
	visSnapExtNone                =0          # from enum VisSnapExtensions
	visSnapToAlignmentBox         =512        # from enum VisSnapSettings
	visSnapToConnectionPoints     =32         # from enum VisSnapSettings
	visSnapToDisabled             =32768      # from enum VisSnapSettings
	visSnapToExtensions           =1024       # from enum VisSnapSettings
	visSnapToGeometry             =256        # from enum VisSnapSettings
	visSnapToGrid                 =2          # from enum VisSnapSettings
	visSnapToGuides               =4          # from enum VisSnapSettings
	visSnapToHandles              =8          # from enum VisSnapSettings
	visSnapToIntersections        =65536      # from enum VisSnapSettings
	visSnapToNone                 =0          # from enum VisSnapSettings
	visSnapToRulerSubdivisions    =1          # from enum VisSnapSettings
	visSnapToVertices             =16         # from enum VisSnapSettings
	visSpatialContain             =2          # from enum VisSpatialRelationCodes
	visSpatialContainedIn         =4          # from enum VisSpatialRelationCodes
	visSpatialOverlap             =1          # from enum VisSpatialRelationCodes
	visSpatialTouching            =8          # from enum VisSpatialRelationCodes
	visSpatialBackToFront         =8          # from enum VisSpatialRelationFlags
	visSpatialFrontToBack         =4          # from enum VisSpatialRelationFlags
	visSpatialIgnoreVisible       =32         # from enum VisSpatialRelationFlags
	visSpatialIncludeContainerShapes=128        # from enum VisSpatialRelationFlags
	visSpatialIncludeDataGraphics =64         # from enum VisSpatialRelationFlags
	visSpatialIncludeGuides       =2          # from enum VisSpatialRelationFlags
	visSpatialIncludeHidden       =16         # from enum VisSpatialRelationFlags
	visStatAppHasShutdown         =1          # from enum VisStatCodes
	visStatClosed                 =8          # from enum VisStatCodes
	visStatDeleted                =2          # from enum VisStatCodes
	visStatNormal                 =0          # from enum VisStatCodes
	visStatSuspended              =16         # from enum VisStatCodes
	visStatTouched                =4          # from enum VisStatCodes
	visTextDisplayClear           =2          # from enum VisTextDisplayQualityTypes
	visTextDisplayFaster          =0          # from enum VisTextDisplayQualityTypes
	visTextDisplayHigherQuality   =1          # from enum VisTextDisplayQualityTypes
	visThemeColorsAdjacency       =37         # from enum VisThemeColors
	visThemeColorsAngles          =38         # from enum VisThemeColors
	visThemeColorsApex            =9          # from enum VisThemeColors
	visThemeColorsApothecary      =39         # from enum VisThemeColors
	visThemeColorsAspect          =13         # from enum VisThemeColors
	visThemeColorsAustin          =40         # from enum VisThemeColors
	visThemeColorsBasic           =36         # from enum VisThemeColors
	visThemeColorsBlackTie        =42         # from enum VisThemeColors
	visThemeColorsCivic           =15         # from enum VisThemeColors
	visThemeColorsClarity         =44         # from enum VisThemeColors
	visThemeColorsComposite       =43         # from enum VisThemeColors
	visThemeColorsConcourse       =4          # from enum VisThemeColors
	visThemeColorsConcourseDark   =27         # from enum VisThemeColors
	visThemeColorsConcourseLight  =26         # from enum VisThemeColors
	visThemeColorsCouture         =51         # from enum VisThemeColors
	visThemeColorsElemental       =45         # from enum VisThemeColors
	visThemeColorsEquity          =14         # from enum VisThemeColors
	visThemeColorsEquityDark      =33         # from enum VisThemeColors
	visThemeColorsEquityLight     =32         # from enum VisThemeColors
	visThemeColorsEssential       =41         # from enum VisThemeColors
	visThemeColorsExecutive       =46         # from enum VisThemeColors
	visThemeColorsFlow            =20         # from enum VisThemeColors
	visThemeColorsFoundry         =8          # from enum VisThemeColors
	visThemeColorsFoundryDark     =31         # from enum VisThemeColors
	visThemeColorsFoundryLight    =30         # from enum VisThemeColors
	visThemeColorsGrid            =47         # from enum VisThemeColors
	visThemeColorsHardcover       =48         # from enum VisThemeColors
	visThemeColorsHorizon         =49         # from enum VisThemeColors
	visThemeColorsMedian          =3          # from enum VisThemeColors
	visThemeColorsMedianDark      =25         # from enum VisThemeColors
	visThemeColorsMedianLight     =24         # from enum VisThemeColors
	visThemeColorsMetro           =21         # from enum VisThemeColors
	visThemeColorsModule          =11         # from enum VisThemeColors
	visThemeColorsMonochrome      =1          # from enum VisThemeColors
	visThemeColorsNewsprint       =50         # from enum VisThemeColors
	visThemeColorsNone            =0          # from enum VisThemeColors
	visThemeColorsOffice          =2          # from enum VisThemeColors
	visThemeColorsOfficeDark      =23         # from enum VisThemeColors
	visThemeColorsOfficeLight     =22         # from enum VisThemeColors
	visThemeColorsOpulent         =16         # from enum VisThemeColors
	visThemeColorsOriel           =12         # from enum VisThemeColors
	visThemeColorsOrigin          =18         # from enum VisThemeColors
	visThemeColorsPaper           =7          # from enum VisThemeColors
	visThemeColorsPaperDark       =29         # from enum VisThemeColors
	visThemeColorsPaperLight      =28         # from enum VisThemeColors
	visThemeColorsPerspective     =52         # from enum VisThemeColors
	visThemeColorsPushpin         =53         # from enum VisThemeColors
	visThemeColorsSlipstream      =54         # from enum VisThemeColors
	visThemeColorsSolstice        =5          # from enum VisThemeColors
	visThemeColorsTechnic         =6          # from enum VisThemeColors
	visThemeColorsThatch          =55         # from enum VisThemeColors
	visThemeColorsTrek            =10         # from enum VisThemeColors
	visThemeColorsUrban           =19         # from enum VisThemeColors
	visThemeColorsVerve           =17         # from enum VisThemeColors
	visThemeColorsVerveDark       =35         # from enum VisThemeColors
	visThemeColorsVerveLight      =34         # from enum VisThemeColors
	visThemeColorsWaveform        =56         # from enum VisThemeColors
	visThemeEffectsBasicShadow    =16         # from enum VisThemeEffects
	visThemeEffectsBevelHighlight =7          # from enum VisThemeEffects
	visThemeEffectsBevelIllusion  =6          # from enum VisThemeEffects
	visThemeEffectsButton         =3          # from enum VisThemeEffects
	visThemeEffectsDecal          =9          # from enum VisThemeEffects
	visThemeEffectsMesh           =11         # from enum VisThemeEffects
	visThemeEffectsNone           =0          # from enum VisThemeEffects
	visThemeEffectsOblique        =14         # from enum VisThemeEffects
	visThemeEffectsOutline        =8          # from enum VisThemeEffects
	visThemeEffectsPillow         =5          # from enum VisThemeEffects
	visThemeEffectsPinstripe      =12         # from enum VisThemeEffects
	visThemeEffectsRaisedSurface  =10         # from enum VisThemeEffects
	visThemeEffectsSimpleShadow   =2          # from enum VisThemeEffects
	visThemeEffectsSquare         =4          # from enum VisThemeEffects
	visThemeEffectsStripes        =13         # from enum VisThemeEffects
	visThemeEffectsSubdued        =1          # from enum VisThemeEffects
	visThemeEffectsToy            =15         # from enum VisThemeEffects
	visThemeTypeColor             =1          # from enum VisThemeTypes
	visThemeTypeConnector         =3          # from enum VisThemeTypes
	visThemeTypeEffect            =2          # from enum VisThemeTypes
	visThemeTypeFont              =4          # from enum VisThemeTypes
	visThemeTypeIndex             =0          # from enum VisThemeTypes
	visConnectError               =-1         # from enum VisToParts
	visConnectToError             =-1         # from enum VisToParts
	visConnectionPoint            =100        # from enum VisToParts
	visGuideIntersect             =4          # from enum VisToParts
	visGuideX                     =1          # from enum VisToParts
	visGuideY                     =2          # from enum VisToParts
	visNone                       =0          # from enum VisToParts
	visToAngle                    =7          # from enum VisToParts
	visToNone                     =0          # from enum VisToParts
	visWholeShape                 =3          # from enum VisToParts
	visToolBarLotusSS             =0          # from enum VisToolbarFlavors
	visToolBarMSOffice            =0          # from enum VisToolbarFlavors
	visToolBarNone                =-1         # from enum VisToolbarFlavors
	visToolBarOn                  =0          # from enum VisToolbarFlavors
	visTraceAddonInvokes          =4          # from enum VisTraceFlags
	visTraceAdvises               =2          # from enum VisTraceFlags
	visTraceCallsToVBA            =8          # from enum VisTraceFlags
	visTraceEvents                =1          # from enum VisTraceFlags
	visTypeSelBitmap              =16         # from enum VisTypeSelectionTypes
	visTypeSelGroup               =1          # from enum VisTypeSelectionTypes
	visTypeSelGuide               =4          # from enum VisTypeSelectionTypes
	visTypeSelInk                 =32         # from enum VisTypeSelectionTypes
	visTypeSelMetafile            =8          # from enum VisTypeSelectionTypes
	visTypeSelOLE                 =64         # from enum VisTypeSelectionTypes
	visTypeSelShape               =2          # from enum VisTypeSelectionTypes
	visBarBottom                  =3          # from enum VisUIBarPosition
	visBarFloating                =4          # from enum VisUIBarPosition
	visBarLeft                    =0          # from enum VisUIBarPosition
	visBarMenu                    =6          # from enum VisUIBarPosition
	visBarPopup                   =5          # from enum VisUIBarPosition
	visBarRight                   =2          # from enum VisUIBarPosition
	visBarTop                     =1          # from enum VisUIBarPosition
	visBarNoChangeDock            =16         # from enum VisUIBarProtection
	visBarNoCustomize             =1          # from enum VisUIBarProtection
	visBarNoHorizontalDock        =64         # from enum VisUIBarProtection
	visBarNoMove                  =4          # from enum VisUIBarProtection
	visBarNoProtection            =0          # from enum VisUIBarProtection
	visBarNoResize                =2          # from enum VisUIBarProtection
	visBarNoVerticalDock          =32         # from enum VisUIBarProtection
	visBarRowFirst                =0          # from enum VisUIBarRow
	visBarRowLast                 =-1         # from enum VisUIBarRow
	visButtonDown                 =-1         # from enum VisUIButtonState
	visButtonMixed                =2          # from enum VisUIButtonState
	visButtonUp                   =0          # from enum VisUIButtonState
	visButtonAutomatic            =0          # from enum VisUIButtonStyle
	visButtonCaption              =2          # from enum VisUIButtonStyle
	visButtonIcon                 =1          # from enum VisUIButtonStyle
	visButtonIconandCaption       =3          # from enum VisUIButtonStyle
	visCmdABarAutoHeight          =1684       # from enum VisUICmds
	visCmdABarAutohide            =1652       # from enum VisUICmds
	visCmdABarHide                =1650       # from enum VisUICmds
	visCmdABarToggleFloat         =1651       # from enum VisUICmds
	visCmdAcquireImages           =1868       # from enum VisUICmds
	visCmdActivateQuickShapesWnd  =2290       # from enum VisUICmds
	visCmdAddConnectPt            =1263       # from enum VisUICmds
	visCmdAddControlPt            =1266       # from enum VisUICmds
	visCmdAddDataRecordset        =1998       # from enum VisUICmds
	visCmdAddMemberToContainer    =2173       # from enum VisUICmds
	visCmdAddTextShape            =1181       # from enum VisUICmds
	visCmdAddToAllContainers      =2251       # from enum VisUICmds
	visCmdAddToNewContainer       =2268       # from enum VisUICmds
	visCmdAlignBox                =1768       # from enum VisUICmds
	visCmdAlignObjectBottom       =1201       # from enum VisUICmds
	visCmdAlignObjectCenter       =1197       # from enum VisUICmds
	visCmdAlignObjectLeft         =1196       # from enum VisUICmds
	visCmdAlignObjectMiddle       =1200       # from enum VisUICmds
	visCmdAlignObjectRight        =1198       # from enum VisUICmds
	visCmdAlignObjectTop          =1199       # from enum VisUICmds
	visCmdAllowThemes             =2056       # from enum VisUICmds
	visCmdAppMaximize             =1864       # from enum VisUICmds
	visCmdAppMinimize             =1865       # from enum VisUICmds
	visCmdAppRestore              =1904       # from enum VisUICmds
	visCmdApplyCalloutForRSField  =2455       # from enum VisUICmds
	visCmdApplyDataGraphic        =2017       # from enum VisUICmds
	visCmdApplyDataGraphicAfterLink=2092       # from enum VisUICmds
	visCmdApplyMainTheme          =2285       # from enum VisUICmds
	visCmdApplyMainThemeToDocument=2296       # from enum VisUICmds
	visCmdApplyMainThemeToPage    =2289       # from enum VisUICmds
	visCmdApplyThemeColors        =2188       # from enum VisUICmds
	visCmdApplyThemeEffects       =2189       # from enum VisUICmds
	visCmdApplyThemeToDoc         =2048       # from enum VisUICmds
	visCmdApplyThemeToNewShapesToggle=2297       # from enum VisUICmds
	visCmdApplyThemeToPage        =2047       # from enum VisUICmds
	visCmdAssociateCallout        =2287       # from enum VisUICmds
	visCmdAutoAlign               =2223       # from enum VisUICmds
	visCmdAutoAlignAndSpace       =2222       # from enum VisUICmds
	visCmdAutoConnectToggle       =2091       # from enum VisUICmds
	visCmdAutoGenerateDataGraphics=2105       # from enum VisUICmds
	visCmdAutoSizeDrawing         =2267       # from enum VisUICmds
	visCmdAutoSpace               =2224       # from enum VisUICmds
	visCmdBreakOLELink            =1900       # from enum VisUICmds
	visCmdBrowseSampleDrawings    =1645       # from enum VisUICmds
	visCmdBullets                 =1633       # from enum VisUICmds
	visCmdCOMAddinsDlg            =2238       # from enum VisUICmds
	visCmdCancelInPlaceEditing    =1602       # from enum VisUICmds
	visCmdCenterDrawing           =1202       # from enum VisUICmds
	visCmdCheckCompatibility      =2182       # from enum VisUICmds
	visCmdCheckForUpdates         =1962       # from enum VisUICmds
	visCmdCloseInkToolsRibbonTab  =2213       # from enum VisUICmds
	visCmdCloseWindow             =1361       # from enum VisUICmds
	visCmdCoauthMerging           =2385       # from enum VisUICmds
	visCmdCollapseShapesWindow    =2269       # from enum VisUICmds
	visCmdConnPoints              =1774       # from enum VisUICmds
	visCmdConnectorEffectCurved   =1945       # from enum VisUICmds
	visCmdConnectorEffectRightAngle=1943       # from enum VisUICmds
	visCmdConnectorEffectStraight =1944       # from enum VisUICmds
	visCmdContactUs               =1964       # from enum VisUICmds
	visCmdContainerAutoResizeExpandContract=2349       # from enum VisUICmds
	visCmdContainerAutoResizeExpandOnly=2348       # from enum VisUICmds
	visCmdContainerAutoResizeOff  =2347       # from enum VisUICmds
	visCmdCreateEditMaster        =1899       # from enum VisUICmds
	visCmdCreateNewDrawing        =1812       # from enum VisUICmds
	visCmdCreateShortcut          =1791       # from enum VisUICmds
	visCmdCreateSubProcessFromSel =2249       # from enum VisUICmds
	visCmdCropObject              =1192       # from enum VisUICmds
	visCmdCropTool                =1449       # from enum VisUICmds
	visCmdCustProp                =1658       # from enum VisUICmds
	visCmdCustPropDefine          =1695       # from enum VisUICmds
	visCmdCustomPropertySets      =1675       # from enum VisUICmds
	visCmdDRConnectionTool        =1226       # from enum VisUICmds
	visCmdDRConnectorTool         =1225       # from enum VisUICmds
	visCmdDRLineTool              =1221       # from enum VisUICmds
	visCmdDROvalTool              =1224       # from enum VisUICmds
	visCmdDRPencilTool            =1220       # from enum VisUICmds
	visCmdDRPointerTool           =1219       # from enum VisUICmds
	visCmdDRQtrArcTool            =1222       # from enum VisUICmds
	visCmdDRRectTool              =1223       # from enum VisUICmds
	visCmdDRRotateTool            =1228       # from enum VisUICmds
	visCmdDRSplineTool            =1311       # from enum VisUICmds
	visCmdDRTextTool              =1227       # from enum VisUICmds
	visCmdDataAutoConnect         =2098       # from enum VisUICmds
	visCmdDataAutoLink            =2046       # from enum VisUICmds
	visCmdDataAutoLinkWiz         =2045       # from enum VisUICmds
	visCmdDataColumnSettingsDlg   =2043       # from enum VisUICmds
	visCmdDataExplorerWindow      =2044       # from enum VisUICmds
	visCmdDataRecordsetProperties =2072       # from enum VisUICmds
	visCmdDataRecordsetSetCommand =2037       # from enum VisUICmds
	visCmdDataRecordsetSetPrimaryKey=2038       # from enum VisUICmds
	visCmdDataRefresh             =2021       # from enum VisUICmds
	visCmdDataRefreshAddConflict  =2094       # from enum VisUICmds
	visCmdDataRefreshConfigDlg    =2022       # from enum VisUICmds
	visCmdDataRefreshDeleteConflict=2095       # from enum VisUICmds
	visCmdDataRefreshDlg          =2019       # from enum VisUICmds
	visCmdDataRefreshResolveConflict=2103       # from enum VisUICmds
	visCmdDataSelectorDlg         =2011       # from enum VisUICmds
	visCmdDataUnlinkRow           =2058       # from enum VisUICmds
	visCmdDataUnlinkShape         =2057       # from enum VisUICmds
	visCmdDecreaseIndent          =1093       # from enum VisUICmds
	visCmdDecreaseParaSpacing     =1095       # from enum VisUICmds
	visCmdDelConnectPt            =1265       # from enum VisUICmds
	visCmdDelControlPt            =1268       # from enum VisUICmds
	visCmdDeleteBackWord          =1905       # from enum VisUICmds
	visCmdDeleteComment           =1920       # from enum VisUICmds
	visCmdDeleteConnectors        =2199       # from enum VisUICmds
	visCmdDeleteDataGraphic       =2067       # from enum VisUICmds
	visCmdDeleteDataRecordset     =1999       # from enum VisUICmds
	visCmdDeleteForwardWord       =2114       # from enum VisUICmds
	visCmdDeleteTheme             =2052       # from enum VisUICmds
	visCmdDeselectAll             =1213       # from enum VisUICmds
	visCmdDesignMode              =1388       # from enum VisUICmds
	visCmdDetectAndRepair         =1890       # from enum VisUICmds
	visCmdDiagramFlipHorizontal   =2229       # from enum VisUICmds
	visCmdDiagramFlipVertical     =2228       # from enum VisUICmds
	visCmdDiagramGallery          =1982       # from enum VisUICmds
	visCmdDiagramRotateLeft       =2227       # from enum VisUICmds
	visCmdDiagramRotateRight      =2226       # from enum VisUICmds
	visCmdDisbandContainer        =2204       # from enum VisUICmds
	visCmdDistributeBottom        =1238       # from enum VisUICmds
	visCmdDistributeCenter        =1233       # from enum VisUICmds
	visCmdDistributeHSpace        =1231       # from enum VisUICmds
	visCmdDistributeLeft          =1232       # from enum VisUICmds
	visCmdDistributeMiddle        =1237       # from enum VisUICmds
	visCmdDistributeRight         =1234       # from enum VisUICmds
	visCmdDistributeTop           =1236       # from enum VisUICmds
	visCmdDistributeVSpace        =1235       # from enum VisUICmds
	visCmdDlgCustomFit            =1536       # from enum VisUICmds
	visCmdDragDuplicate           =1184       # from enum VisUICmds
	visCmdDrawAddGuide            =1180       # from enum VisUICmds
	visCmdDrawFillStyle           =1123       # from enum VisUICmds
	visCmdDrawGlue                =1125       # from enum VisUICmds
	visCmdDrawLineStyle           =1122       # from enum VisUICmds
	visCmdDrawOval                =1183       # from enum VisUICmds
	visCmdDrawRect                =1182       # from enum VisUICmds
	visCmdDrawRegion              =1742       # from enum VisUICmds
	visCmdDrawSnap                =1124       # from enum VisUICmds
	visCmdDrawTextStyle           =1121       # from enum VisUICmds
	visCmdDrawZoom                =1126       # from enum VisUICmds
	visCmdDrawingExplorer         =1721       # from enum VisUICmds
	visCmdDrawingTools            =1946       # from enum VisUICmds
	visCmdDropAndContain          =2172       # from enum VisUICmds
	visCmdDropAndInsertIntoList   =2196       # from enum VisUICmds
	visCmdDropCallout             =2286       # from enum VisUICmds
	visCmdDropManyLinked          =2108       # from enum VisUICmds
	visCmdDropManyOnPage          =1869       # from enum VisUICmds
	visCmdDropOnPage              =1246       # from enum VisUICmds
	visCmdDropOnStencil           =1244       # from enum VisUICmds
	visCmdDropOnText              =1243       # from enum VisUICmds
	visCmdDuplicateDataGraphic    =2106       # from enum VisUICmds
	visCmdDuplicatePage           =2383       # from enum VisUICmds
	visCmdDuplicateTheme          =2050       # from enum VisUICmds
	visCmdDynConnReroute          =1829       # from enum VisUICmds
	visCmdDynamicGrid             =1765       # from enum VisUICmds
	visCmdEditConvertObject       =1439       # from enum VisUICmds
	visCmdEditFind                =1043       # from enum VisUICmds
	visCmdEditInsertField         =1032       # from enum VisUICmds
	visCmdEditInsertObject        =1031       # from enum VisUICmds
	visCmdEditLinks               =1030       # from enum VisUICmds
	visCmdEditOpenObject          =1029       # from enum VisUICmds
	visCmdEditPasteLink           =1028       # from enum VisUICmds
	visCmdEditPasteSpecial        =1027       # from enum VisUICmds
	visCmdEditRedo                =1018       # from enum VisUICmds
	visCmdEditRedoMultiple        =1683       # from enum VisUICmds
	visCmdEditRedoOrRepeat        =2295       # from enum VisUICmds
	visCmdEditRepeat              =1019       # from enum VisUICmds
	visCmdEditReplace             =1179       # from enum VisUICmds
	visCmdEditSelectSpecial       =1026       # from enum VisUICmds
	visCmdEditTheme               =2049       # from enum VisUICmds
	visCmdEditThemeColors         =2190       # from enum VisUICmds
	visCmdEditThemeEffects        =2191       # from enum VisUICmds
	visCmdEditUndo                =1017       # from enum VisUICmds
	visCmdEditUndoMultiple        =1682       # from enum VisUICmds
	visCmdEmailRouting            =1588       # from enum VisUICmds
	visCmdExportDatabaseAddOn     =1891       # from enum VisUICmds
	visCmdFileCheckIn             =1787       # from enum VisUICmds
	visCmdFileCheckOut            =1788       # from enum VisUICmds
	visCmdFileChooseTemplates     =1583       # from enum VisUICmds
	visCmdFileClose               =1003       # from enum VisUICmds
	visCmdFileExit                =1016       # from enum VisUICmds
	visCmdFileImport              =1007       # from enum VisUICmds
	visCmdFileLastFile1           =1012       # from enum VisUICmds
	visCmdFileLastFile10          =2127       # from enum VisUICmds
	visCmdFileLastFile11          =2128       # from enum VisUICmds
	visCmdFileLastFile12          =2129       # from enum VisUICmds
	visCmdFileLastFile13          =2130       # from enum VisUICmds
	visCmdFileLastFile14          =2131       # from enum VisUICmds
	visCmdFileLastFile15          =2132       # from enum VisUICmds
	visCmdFileLastFile16          =2133       # from enum VisUICmds
	visCmdFileLastFile17          =2134       # from enum VisUICmds
	visCmdFileLastFile18          =2135       # from enum VisUICmds
	visCmdFileLastFile19          =2136       # from enum VisUICmds
	visCmdFileLastFile2           =1013       # from enum VisUICmds
	visCmdFileLastFile20          =2137       # from enum VisUICmds
	visCmdFileLastFile3           =1014       # from enum VisUICmds
	visCmdFileLastFile4           =1015       # from enum VisUICmds
	visCmdFileLastFile5           =1561       # from enum VisUICmds
	visCmdFileLastFile6           =1569       # from enum VisUICmds
	visCmdFileLastFile7           =1570       # from enum VisUICmds
	visCmdFileLastFile8           =1571       # from enum VisUICmds
	visCmdFileLastFile9           =1572       # from enum VisUICmds
	visCmdFileNew                 =1001       # from enum VisUICmds
	visCmdFileNewBlankDrawing     =1579       # from enum VisUICmds
	visCmdFileNewBlankDrawingMetric=1671       # from enum VisUICmds
	visCmdFileNewBlankDrawingUS   =1672       # from enum VisUICmds
	visCmdFileNewBlankStencil     =1582       # from enum VisUICmds
	visCmdFileNewBlankStencilMetric=1673       # from enum VisUICmds
	visCmdFileNewBlankStencilUS   =1674       # from enum VisUICmds
	visCmdFileNewStencilDlg       =1580       # from enum VisUICmds
	visCmdFileOpen                =1002       # from enum VisUICmds
	visCmdFileOpenStencil         =1442       # from enum VisUICmds
	visCmdFilePrint               =1010       # from enum VisUICmds
	visCmdFileSave                =1004       # from enum VisUICmds
	visCmdFileSaveAs              =1005       # from enum VisUICmds
	visCmdFileSaveAsDWG           =2305       # from enum VisUICmds
	visCmdFileSaveAsDrawing       =2306       # from enum VisUICmds
	visCmdFileSaveAsDrawingPreviousFileFormat=2298       # from enum VisUICmds
	visCmdFileSaveAsEMF           =2302       # from enum VisUICmds
	visCmdFileSaveAsJPG           =2301       # from enum VisUICmds
	visCmdFileSaveAsMacroDrawing  =2311       # from enum VisUICmds
	visCmdFileSaveAsPNG           =2300       # from enum VisUICmds
	visCmdFileSaveAsSVG           =2303       # from enum VisUICmds
	visCmdFileSaveAsTemplate      =2299       # from enum VisUICmds
	visCmdFileSaveAsVDX           =2304       # from enum VisUICmds
	visCmdFileSaveAsWebPage       =1785       # from enum VisUICmds
	visCmdFileSaveWorkspace       =1006       # from enum VisUICmds
	visCmdFileSummaryInfoDlg      =1009       # from enum VisUICmds
	visCmdFileUndoCheckout        =2109       # from enum VisUICmds
	visCmdFirst                   =0          # from enum VisUICmds
	visCmdFirstTile               =1515       # from enum VisUICmds
	visCmdFitContainerToContents  =2195       # from enum VisUICmds
	visCmdFitCurve                =1538       # from enum VisUICmds
	visCmdFormatAllTextProps      =1642       # from enum VisUICmds
	visCmdFormatBehavior          =1071       # from enum VisUICmds
	visCmdFormatBlock             =1070       # from enum VisUICmds
	visCmdFormatCorners           =1334       # from enum VisUICmds
	visCmdFormatCustPropDef       =1687       # from enum VisUICmds
	visCmdFormatCustPropEdit      =1312       # from enum VisUICmds
	visCmdFormatDefineStyles      =1064       # from enum VisUICmds
	visCmdFormatDoubleClick       =1118       # from enum VisUICmds
	visCmdFormatFill              =1066       # from enum VisUICmds
	visCmdFormatInkDlg            =1955       # from enum VisUICmds
	visCmdFormatLine              =1065       # from enum VisUICmds
	visCmdFormatPainter           =1271       # from enum VisUICmds
	visCmdFormatParagraph         =1068       # from enum VisUICmds
	visCmdFormatPictureAutobalance=2205       # from enum VisUICmds
	visCmdFormatPictureCompressionDlg=2212       # from enum VisUICmds
	visCmdFormatProtection        =1072       # from enum VisUICmds
	visCmdFormatShadow            =1333       # from enum VisUICmds
	visCmdFormatSpecial           =1073       # from enum VisUICmds
	visCmdFormatStyle             =1063       # from enum VisUICmds
	visCmdFormatTabs              =1069       # from enum VisUICmds
	visCmdFormatText              =1067       # from enum VisUICmds
	visCmdFullScreenMode          =1492       # from enum VisUICmds
	visCmdGoToPageToolbar         =1635       # from enum VisUICmds
	visCmdGrid                    =1767       # from enum VisUICmds
	visCmdGuides                  =1771       # from enum VisUICmds
	visCmdHeaderFooter            =1720       # from enum VisUICmds
	visCmdHelpAboutVisio          =1100       # from enum VisUICmds
	visCmdHelpContents            =1092       # from enum VisUICmds
	visCmdHelpMode                =1386       # from enum VisUICmds
	visCmdHelpQuickTour           =1099       # from enum VisUICmds
	visCmdHelpSearch              =1809       # from enum VisUICmds
	visCmdHelpShapeBasics         =1822       # from enum VisUICmds
	visCmdHelpStencil             =1097       # from enum VisUICmds
	visCmdHelpTemplates           =1586       # from enum VisUICmds
	visCmdHideAllToolbars         =1726       # from enum VisUICmds
	visCmdHideDocumentStencil     =1689       # from enum VisUICmds
	visCmdHideMoreShapes          =2291       # from enum VisUICmds
	visCmdHierarchical            =0          # from enum VisUICmds
	visCmdHyperlinkHier           =1611       # from enum VisUICmds
	visCmdHyperlinkList           =1719       # from enum VisUICmds
	visCmdINETAddToFavorites      =1506       # from enum VisUICmds
	visCmdINETCopyHyperlink       =1610       # from enum VisUICmds
	visCmdINETDeleteHlink         =1609       # from enum VisUICmds
	visCmdINETDiagrammingResources=1606       # from enum VisUICmds
	visCmdINETEditHyperlink       =1619       # from enum VisUICmds
	visCmdINETGoBack              =1599       # from enum VisUICmds
	visCmdINETGoForward           =1598       # from enum VisUICmds
	visCmdINETKnowledgeBase       =1605       # from enum VisUICmds
	visCmdINETOfficeOnTheWeb      =1802       # from enum VisUICmds
	visCmdINETOpenHlink           =1607       # from enum VisUICmds
	visCmdINETOpenHlinkNewWnd     =1608       # from enum VisUICmds
	visCmdINETPasteAsHyperlink    =1620       # from enum VisUICmds
	visCmdINETUserSearchPage      =1595       # from enum VisUICmds
	visCmdINETVisioHomePage       =1596       # from enum VisUICmds
	visCmdINETVisioOnTheWeb       =1831       # from enum VisUICmds
	visCmdINETVisioSolutionsLibrary=1604       # from enum VisUICmds
	visCmdIconBucketTool          =1543       # from enum VisUICmds
	visCmdIconLassoTool           =1544       # from enum VisUICmds
	visCmdIconLeftColor           =1143       # from enum VisUICmds
	visCmdIconPencilTool          =1145       # from enum VisUICmds
	visCmdIconRightColor          =1144       # from enum VisUICmds
	visCmdIconSelectNet           =1545       # from enum VisUICmds
	visCmdIgnoreValidationIssue   =2254       # from enum VisUICmds
	visCmdIgnoreValidationRule    =2256       # from enum VisUICmds
	visCmdImageProperties         =1887       # from enum VisUICmds
	visCmdImagePropertiesDlg      =1883       # from enum VisUICmds
	visCmdIncreaseIndent          =1094       # from enum VisUICmds
	visCmdIncreaseParaSpacing     =1096       # from enum VisUICmds
	visCmdInkCustomizePen         =1664       # from enum VisUICmds
	visCmdInkEraser               =1970       # from enum VisUICmds
	visCmdInkReviewPen            =1971       # from enum VisUICmds
	visCmdInkStockPen0            =1973       # from enum VisUICmds
	visCmdInkStockPen1            =1974       # from enum VisUICmds
	visCmdInkStockPen2            =1975       # from enum VisUICmds
	visCmdInkStockPen3            =1976       # from enum VisUICmds
	visCmdInkStockPen4            =1977       # from enum VisUICmds
	visCmdInkTool                 =1661       # from enum VisUICmds
	visCmdInserTextBoxControl     =2145       # from enum VisUICmds
	visCmdInsertAutoCADAddOn      =1521       # from enum VisUICmds
	visCmdInsertCheckBoxControl   =2150       # from enum VisUICmds
	visCmdInsertClipArt           =1497       # from enum VisUICmds
	visCmdInsertClipArtDlg        =2345       # from enum VisUICmds
	visCmdInsertComboBoxControl   =2152       # from enum VisUICmds
	visCmdInsertComment           =1501       # from enum VisUICmds
	visCmdInsertControlDlg        =1522       # from enum VisUICmds
	visCmdInsertDataMap           =1282       # from enum VisUICmds
	visCmdInsertHyperLink         =1585       # from enum VisUICmds
	visCmdInsertImageControl      =2148       # from enum VisUICmds
	visCmdInsertLabelControl      =2144       # from enum VisUICmds
	visCmdInsertLegendHorizontal  =2331       # from enum VisUICmds
	visCmdInsertLegendVertical1   =2335       # from enum VisUICmds
	visCmdInsertListBoxControl    =2153       # from enum VisUICmds
	visCmdInsertMemberIntoList    =2174       # from enum VisUICmds
	visCmdInsertMicrosoftGraph    =1499       # from enum VisUICmds
	visCmdInsertNewBackgroundPage =2165       # from enum VisUICmds
	visCmdInsertPageTab           =2202       # from enum VisUICmds
	visCmdInsertPushButtonControl =2147       # from enum VisUICmds
	visCmdInsertRadioButtonControl=2151       # from enum VisUICmds
	visCmdInsertScrollBarControl  =2149       # from enum VisUICmds
	visCmdInsertSpinControl       =2146       # from enum VisUICmds
	visCmdInsertTextBox           =2006       # from enum VisUICmds
	visCmdInsertToggleButtonControl=2154       # from enum VisUICmds
	visCmdInsertVertTextBox       =2007       # from enum VisUICmds
	visCmdInsertWordArt           =1498       # from enum VisUICmds
	visCmdIntersect               =1453       # from enum VisUICmds
	visCmdJoin                    =1533       # from enum VisUICmds
	visCmdLanguagePreferencesDlg  =2363       # from enum VisUICmds
	visCmdLast                    =65535      # from enum VisUICmds
	visCmdLastTile                =1516       # from enum VisUICmds
	visCmdLayerDlg                =1446       # from enum VisUICmds
	visCmdLayerSetupDlg           =1448       # from enum VisUICmds
	visCmdLayoutDynamic           =1493       # from enum VisUICmds
	visCmdLayoutSpacingDlg        =2233       # from enum VisUICmds
	visCmdLicenseVerification     =1877       # from enum VisUICmds
	visCmdLinkRowToShape          =1997       # from enum VisUICmds
	visCmdListInsertAfter         =2271       # from enum VisUICmds
	visCmdListInsertBefore        =2270       # from enum VisUICmds
	visCmdLockContainer           =2220       # from enum VisUICmds
	visCmdMDIMaximize             =1901       # from enum VisUICmds
	visCmdMDIMinimize             =1902       # from enum VisUICmds
	visCmdMDIRestore              =1903       # from enum VisUICmds
	visCmdMSOInsertEquation       =1646       # from enum VisUICmds
	visCmdMSOInsertSymbol         =1504       # from enum VisUICmds
	visCmdMSOInsertSymbolDlg      =1505       # from enum VisUICmds
	visCmdMasterExplorer          =1916       # from enum VisUICmds
	visCmdMasterSetup             =1343       # from enum VisUICmds
	visCmdMinimizeRibbonToggle    =2232       # from enum VisUICmds
	visCmdModConnectPt            =1264       # from enum VisUICmds
	visCmdModControlPt            =1267       # from enum VisUICmds
	visCmdMovConnectPt            =1269       # from enum VisUICmds
	visCmdMove1D                  =1186       # from enum VisUICmds
	visCmdMove2D                  =1187       # from enum VisUICmds
	visCmdMoveComment             =1502       # from enum VisUICmds
	visCmdMoveObject              =1185       # from enum VisUICmds
	visCmdMoveOffPageBreaks       =2225       # from enum VisUICmds
	visCmdMsoAutoCorrect          =1872       # from enum VisUICmds
	visCmdMsoAutoCorrectDlg       =1866       # from enum VisUICmds
	visCmdMsoAutoFormat           =1873       # from enum VisUICmds
	visCmdMsoClipboard            =1859       # from enum VisUICmds
	visCmdMsoCustomItem           =1898       # from enum VisUICmds
	visCmdMsoMediaGallery         =1885       # from enum VisUICmds
	visCmdMsoSearch               =1860       # from enum VisUICmds
	visCmdMultipleFileImport      =2201       # from enum VisUICmds
	visCmdNMMeetNow               =1882       # from enum VisUICmds
	visCmdNewDefDocBlankDrawing   =1906       # from enum VisUICmds
	visCmdNewForegroundPage       =2361       # from enum VisUICmds
	visCmdNewFromExisting         =1897       # from enum VisUICmds
	visCmdNewSubProcess           =2245       # from enum VisUICmds
	visCmdNewThemeColors          =2065       # from enum VisUICmds
	visCmdNewThemeEffects         =2064       # from enum VisUICmds
	visCmdNextCommentMarkup       =2180       # from enum VisUICmds
	visCmdNextMarkup              =1914       # from enum VisUICmds
	visCmdNextTile                =1514       # from enum VisUICmds
	visCmdNextWindow              =1886       # from enum VisUICmds
	visCmdObjectAddToGroup        =1053       # from enum VisUICmds
	visCmdObjectAlignObjects      =1049       # from enum VisUICmds
	visCmdObjectBringForward      =1045       # from enum VisUICmds
	visCmdObjectBringToFront      =1046       # from enum VisUICmds
	visCmdObjectCombine           =1061       # from enum VisUICmds
	visCmdObjectConnectObjects    =1050       # from enum VisUICmds
	visCmdObjectConvertToGroup    =1055       # from enum VisUICmds
	visCmdObjectDistributeDlg     =1230       # from enum VisUICmds
	visCmdObjectFlipHorizontal    =1058       # from enum VisUICmds
	visCmdObjectFlipVertical      =1057       # from enum VisUICmds
	visCmdObjectFragment          =1062       # from enum VisUICmds
	visCmdObjectGroup             =1051       # from enum VisUICmds
	visCmdObjectHelp              =1428       # from enum VisUICmds
	visCmdObjectInfoDlg           =1425       # from enum VisUICmds
	visCmdObjectRemoveFromGroup   =1054       # from enum VisUICmds
	visCmdObjectReverse           =1059       # from enum VisUICmds
	visCmdObjectRotate90          =1056       # from enum VisUICmds
	visCmdObjectSendBackward      =1047       # from enum VisUICmds
	visCmdObjectSendToBack        =1048       # from enum VisUICmds
	visCmdObjectSwapEnds          =1870       # from enum VisUICmds
	visCmdObjectUngroup           =1052       # from enum VisUICmds
	visCmdObjectUnion             =1060       # from enum VisUICmds
	visCmdOfficeCenterOptions     =2141       # from enum VisUICmds
	visCmdOfficeDiagnostics       =1890       # from enum VisUICmds
	visCmdOffsetDlg               =1387       # from enum VisUICmds
	visCmdOpenActiveObject        =1601       # from enum VisUICmds
	visCmdOpenCommentForEdit      =1503       # from enum VisUICmds
	visCmdOpenInVisio             =1491       # from enum VisUICmds
	visCmdOptionsColorPaletteDlg  =1082       # from enum VisUICmds
	visCmdOptionsDeletePages      =1079       # from enum VisUICmds
	visCmdOptionsEditBackground   =1075       # from enum VisUICmds
	visCmdOptionsEditDrawing      =1074       # from enum VisUICmds
	visCmdOptionsGoToDrawing      =1077       # from enum VisUICmds
	visCmdOptionsNewPage          =1078       # from enum VisUICmds
	visCmdOptionsPageSetup        =1076       # from enum VisUICmds
	visCmdOptionsPreferences      =1081       # from enum VisUICmds
	visCmdOptionsProtectDocument  =1083       # from enum VisUICmds
	visCmdOptionsReorderPages     =1080       # from enum VisUICmds
	visCmdOptionsSnapGlueSetup    =1084       # from enum VisUICmds
	visCmdPageAutoSizeToggle      =2333       # from enum VisUICmds
	visCmdPageMeasureUnitsDlg     =1274       # from enum VisUICmds
	visCmdPageSizeDlg             =2176       # from enum VisUICmds
	visCmdPageSizeToFitDrawing    =2332       # from enum VisUICmds
	visCmdPagesList               =1654       # from enum VisUICmds
	visCmdPanObject               =1193       # from enum VisUICmds
	visCmdPanZoom                 =1653       # from enum VisUICmds
	visCmdPasteShortcut           =1790       # from enum VisUICmds
	visCmdPasteToLocation         =2221       # from enum VisUICmds
	visCmdPauseRecordingMacro     =1778       # from enum VisUICmds
	visCmdPostDrag                =2337       # from enum VisUICmds
	visCmdPreviousCommentMarkup   =2179       # from enum VisUICmds
	visCmdPreviousMarkup          =1915       # from enum VisUICmds
	visCmdPreviousTile            =1513       # from enum VisUICmds
	visCmdPrintPage               =1443       # from enum VisUICmds
	visCmdPrintPreview            =1490       # from enum VisUICmds
	visCmdPrivacySettings         =1963       # from enum VisUICmds
	visCmdProgRefHelp             =1584       # from enum VisUICmds
	visCmdPublishToProcessRepository=2294       # from enum VisUICmds
	visCmdPublishToVisioServices  =2293       # from enum VisUICmds
	visCmdRHI                     =2009       # from enum VisUICmds
	visCmdRHIDlg                  =2010       # from enum VisUICmds
	visCmdReOrderPage             =1795       # from enum VisUICmds
	visCmdRecalcObjectWH          =1146       # from enum VisUICmds
	visCmdRecordNewMacro          =1775       # from enum VisUICmds
	visCmdReinstateValidationIssue=2255       # from enum VisUICmds
	visCmdRelayoutShapes          =2068       # from enum VisUICmds
	visCmdRemoveDataGraphicFromSel=2107       # from enum VisUICmds
	visCmdRemoveFromAllContainers =2252       # from enum VisUICmds
	visCmdRemoveMemberFromContainer=2175       # from enum VisUICmds
	visCmdRemoveMemberFromList    =2346       # from enum VisUICmds
	visCmdRemoveThemeFromSel      =2119       # from enum VisUICmds
	visCmdRemoveVBAFromActiveDoc  =1590       # from enum VisUICmds
	visCmdReorderList             =2197       # from enum VisUICmds
	visCmdReplaceShape            =2051       # from enum VisUICmds
	visCmdResearchLookUp          =1967       # from enum VisUICmds
	visCmdResearchPaneToggle      =1969       # from enum VisUICmds
	visCmdResearchThesaurus       =2178       # from enum VisUICmds
	visCmdResearchTranslate       =1968       # from enum VisUICmds
	visCmdResumeRecordingMacro    =1779       # from enum VisUICmds
	visCmdReviewerPaneToggle      =1939       # from enum VisUICmds
	visCmdReviewerVisibilityAll   =1836       # from enum VisUICmds
	visCmdReviewerVisibilityNone  =1919       # from enum VisUICmds
	visCmdRightDragCancel         =1881       # from enum VisUICmds
	visCmdRightDragCopy           =1879       # from enum VisUICmds
	visCmdRightDragLink           =1880       # from enum VisUICmds
	visCmdRightDragMove           =1878       # from enum VisUICmds
	visCmdRotate90Clockwise       =1494       # from enum VisUICmds
	visCmdRotateObject            =1190       # from enum VisUICmds
	visCmdRulSub                  =1766       # from enum VisUICmds
	visCmdRulerGridDlg            =1318       # from enum VisUICmds
	visCmdRunAddOnDlg             =1484       # from enum VisUICmds
	visCmdRunAddOnMenu            =1090       # from enum VisUICmds
	visCmdSSWindowAddSection      =1384       # from enum VisUICmds
	visCmdSSWindowChangeRowType   =1383       # from enum VisUICmds
	visCmdSSWindowCollapse        =1250       # from enum VisUICmds
	visCmdSSWindowDeselect        =1253       # from enum VisUICmds
	visCmdSSWindowExpand          =1251       # from enum VisUICmds
	visCmdSSWindowPasteFunction   =1382       # from enum VisUICmds
	visCmdSSWindowPasteName       =1381       # from enum VisUICmds
	visCmdSSWindowSelect          =1252       # from enum VisUICmds
	visCmdSSWindowShowSection     =1380       # from enum VisUICmds
	visCmdSSWindowShowTraceWindow =1781       # from enum VisUICmds
	visCmdSWAccept                =1140       # from enum VisUICmds
	visCmdSWAddSectionDlg         =1116       # from enum VisUICmds
	visCmdSWCancel                =1139       # from enum VisUICmds
	visCmdSWChangeRowTypeDlg      =1114       # from enum VisUICmds
	visCmdSWDeleteRow             =1115       # from enum VisUICmds
	visCmdSWDeleteSection         =1117       # from enum VisUICmds
	visCmdSWExpandRow             =1718       # from enum VisUICmds
	visCmdSWFormula               =1141       # from enum VisUICmds
	visCmdSWInsertRow             =1112       # from enum VisUICmds
	visCmdSWInsertRowAfter        =1113       # from enum VisUICmds
	visCmdSWPasteFunctionDlg      =1111       # from enum VisUICmds
	visCmdSWPasteNameDlg          =1110       # from enum VisUICmds
	visCmdSWShapeActionDlg        =1444       # from enum VisUICmds
	visCmdSWShowFormulas          =1108       # from enum VisUICmds
	visCmdSWShowSectionsDlg       =1109       # from enum VisUICmds
	visCmdSWShowToggle            =1142       # from enum VisUICmds
	visCmdSWShowValues            =1107       # from enum VisUICmds
	visCmdSaveAsFixedFormatDlg    =2117       # from enum VisUICmds
	visCmdSaveForAutoRecover      =1857       # from enum VisUICmds
	visCmdSelectContainerMembers  =2219       # from enum VisUICmds
	visCmdSelectionModeExtend     =1909       # from enum VisUICmds
	visCmdSelectionModeLasso      =1908       # from enum VisUICmds
	visCmdSelectionModeRect       =1907       # from enum VisUICmds
	visCmdSendAsMail              =1292       # from enum VisUICmds
	visCmdSendToExchange          =1589       # from enum VisUICmds
	visCmdSetAddMarkup            =1744       # from enum VisUICmds
	visCmdSetAutoSize             =2266       # from enum VisUICmds
	visCmdSetCharColor            =1404       # from enum VisUICmds
	visCmdSetCharSizeDown         =1406       # from enum VisUICmds
	visCmdSetCharSizeUp           =1405       # from enum VisUICmds
	visCmdSetContainerProperties  =2181       # from enum VisUICmds
	visCmdSetDiagramServices      =2265       # from enum VisUICmds
	visCmdSetDynConnAppearanceCurved=1895       # from enum VisUICmds
	visCmdSetDynConnAppearanceDefault=1893       # from enum VisUICmds
	visCmdSetDynConnAppearanceStraight=1894       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_2pt=1713       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_3pt=1714       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_4pt=1715       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_5pt=1716       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_6pt=1717       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_Arc=1709       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_Gap=1710       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_Page=1708       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_Square=1711       # from enum VisUICmds
	visCmdSetDynConnLineJumpStyle_Triangle=1712       # from enum VisUICmds
	visCmdSetDynConnRerouteAsNeeded=1697       # from enum VisUICmds
	visCmdSetDynConnRerouteFreely =1696       # from enum VisUICmds
	visCmdSetDynConnRerouteNever  =1698       # from enum VisUICmds
	visCmdSetDynConnRerouteOnCrossover=1837       # from enum VisUICmds
	visCmdSetDynConnRoutingStyle  =1700       # from enum VisUICmds
	visCmdSetFillColor            =1385       # from enum VisUICmds
	visCmdSetFillPattern          =1399       # from enum VisUICmds
	visCmdSetFillShadow           =1379       # from enum VisUICmds
	visCmdSetHeaderFooter         =1858       # from enum VisUICmds
	visCmdSetIndexInStencil       =1871       # from enum VisUICmds
	visCmdSetLanguageDlg          =1888       # from enum VisUICmds
	visCmdSetLineColor            =1359       # from enum VisUICmds
	visCmdSetLineCornerStyle      =1358       # from enum VisUICmds
	visCmdSetLineEnds             =1357       # from enum VisUICmds
	visCmdSetLinePattern          =1356       # from enum VisUICmds
	visCmdSetLineWeight           =1355       # from enum VisUICmds
	visCmdSetPageLineJumpCode_Disp=1703       # from enum VisUICmds
	visCmdSetPageLineJumpCode_Horz=1705       # from enum VisUICmds
	visCmdSetPageLineJumpCode_Last=1707       # from enum VisUICmds
	visCmdSetPageLineJumpCode_None=1704       # from enum VisUICmds
	visCmdSetPageLineJumpCode_Vert=1706       # from enum VisUICmds
	visCmdSetPageOrientation      =2170       # from enum VisUICmds
	visCmdSetPagePlow             =1699       # from enum VisUICmds
	visCmdSetPageSize             =2171       # from enum VisUICmds
	visCmdSetPlaceableShapeBehavior=1702       # from enum VisUICmds
	visCmdSetThemeBehavior        =2382       # from enum VisUICmds
	visCmdShapeActions            =1309       # from enum VisUICmds
	visCmdShapeComment            =1686       # from enum VisUICmds
	visCmdShapeCommentDelete      =1688       # from enum VisUICmds
	visCmdShapeCommentDlg         =1685       # from enum VisUICmds
	visCmdShapeExplorer           =1389       # from enum VisUICmds
	visCmdShapeGalleryAddOn       =1867       # from enum VisUICmds
	visCmdShapeGeo                =1769       # from enum VisUICmds
	visCmdShapeHand               =1772       # from enum VisUICmds
	visCmdShapeIntersect          =1830       # from enum VisUICmds
	visCmdShapeLayerToolbar       =1634       # from enum VisUICmds
	visCmdShapeSearchWindowToggle =2344       # from enum VisUICmds
	visCmdShapeStudioAddon        =1985       # from enum VisUICmds
	visCmdShapeTransparency       =1875       # from enum VisUICmds
	visCmdShapeTransparencyDlg    =1874       # from enum VisUICmds
	visCmdShapeVert               =1773       # from enum VisUICmds
	visCmdShapesWindow            =1669       # from enum VisUICmds
	visCmdSharedWorkspacePaneToggle=1972       # from enum VisUICmds
	visCmdShowIgnoredIssuesToggle =2258       # from enum VisUICmds
	visCmdShowLineJumpsToggle     =2231       # from enum VisUICmds
	visCmdShowShapeSheetDocument  =2169       # from enum VisUICmds
	visCmdShowShapeSheetPage      =2168       # from enum VisUICmds
	visCmdShowShapeSheetShape     =2167       # from enum VisUICmds
	visCmdSize1D                  =1188       # from enum VisUICmds
	visCmdSize2D                  =1189       # from enum VisUICmds
	visCmdSizeObjects             =1925       # from enum VisUICmds
	visCmdSizePos                 =1670       # from enum VisUICmds
	visCmdSizeTextBlock           =1194       # from enum VisUICmds
	visCmdSpaceShapesAvoidPageBreaksToggle=2340       # from enum VisUICmds
	visCmdSpellingChange          =1889       # from enum VisUICmds
	visCmdSpellingOptionsDlg      =2042       # from enum VisUICmds
	visCmdStampTool               =1424       # from enum VisUICmds
	visCmdStartRecordingMacro     =1776       # from enum VisUICmds
	visCmdStenActivate            =1458       # from enum VisUICmds
	visCmdStenAutoArrange         =1483       # from enum VisUICmds
	visCmdStenCleanup             =1106       # from enum VisUICmds
	visCmdStenClose               =1452       # from enum VisUICmds
	visCmdStenDrawingExplorer     =1796       # from enum VisUICmds
	visCmdStenEditDrawing         =1102       # from enum VisUICmds
	visCmdStenEditIcon            =1101       # from enum VisUICmds
	visCmdStenEditOff             =1681       # from enum VisUICmds
	visCmdStenEditOn              =1680       # from enum VisUICmds
	visCmdStenEditToggle          =1679       # from enum VisUICmds
	visCmdStenIconAndDetail       =1892       # from enum VisUICmds
	visCmdStenIconAndName         =1480       # from enum VisUICmds
	visCmdStenIconOnly            =1481       # from enum VisUICmds
	visCmdStenImageMaster         =1105       # from enum VisUICmds
	visCmdStenNameMaster          =1103       # from enum VisUICmds
	visCmdStenNameOnly            =1482       # from enum VisUICmds
	visCmdStenNamesUnderIcons     =2005       # from enum VisUICmds
	visCmdStenNewMaster           =1104       # from enum VisUICmds
	visCmdStenProperties          =1678       # from enum VisUICmds
	visCmdStenSave                =1676       # from enum VisUICmds
	visCmdStenSaveAs              =1677       # from enum VisUICmds
	visCmdStopIgnoringValidationRule=2257       # from enum VisUICmds
	visCmdStopRecordingMacro      =1777       # from enum VisUICmds
	visCmdSubtract                =1454       # from enum VisUICmds
	visCmdTaskPane                =1896       # from enum VisUICmds
	visCmdTaskPaneDataGraphic     =2024       # from enum VisUICmds
	visCmdTaskPaneDocumentManagement=1972       # from enum VisUICmds
	visCmdTaskPaneResearch        =1969       # from enum VisUICmds
	visCmdTaskPaneReviewer        =1939       # from enum VisUICmds
	visCmdTaskPaneThemeColors     =2054       # from enum VisUICmds
	visCmdTaskPaneThemeEffects    =2055       # from enum VisUICmds
	visCmdTaskPaneToggle          =1896       # from enum VisUICmds
	visCmdTaskTogglePreviewSize   =2053       # from enum VisUICmds
	visCmdTextAllCaps             =1862       # from enum VisUICmds
	visCmdTextBlockTool           =1451       # from enum VisUICmds
	visCmdTextBold                =1131       # from enum VisUICmds
	visCmdTextDoubleStrikethrough =1951       # from enum VisUICmds
	visCmdTextDoubleUline         =1863       # from enum VisUICmds
	visCmdTextEditRuler           =1810       # from enum VisUICmds
	visCmdTextEditState           =1214       # from enum VisUICmds
	visCmdTextFont                =1129       # from enum VisUICmds
	visCmdTextHAlignCenter        =1408       # from enum VisUICmds
	visCmdTextHAlignDistribute    =1952       # from enum VisUICmds
	visCmdTextHAlignJustify       =1412       # from enum VisUICmds
	visCmdTextHAlignLeft          =1407       # from enum VisUICmds
	visCmdTextHAlignRight         =1409       # from enum VisUICmds
	visCmdTextItalic              =1132       # from enum VisUICmds
	visCmdTextRotate90            =1098       # from enum VisUICmds
	visCmdTextSize                =1130       # from enum VisUICmds
	visCmdTextSmallCaps           =1133       # from enum VisUICmds
	visCmdTextStrikethrough       =1741       # from enum VisUICmds
	visCmdTextStyle               =1128       # from enum VisUICmds
	visCmdTextSubscript           =1135       # from enum VisUICmds
	visCmdTextSuperscript         =1134       # from enum VisUICmds
	visCmdTextUline               =1136       # from enum VisUICmds
	visCmdTextVAlignBottom        =1422       # from enum VisUICmds
	visCmdTextVAlignMiddle        =1414       # from enum VisUICmds
	visCmdTextVAlignTop           =1413       # from enum VisUICmds
	visCmdToggleDocumentStencil   =1690       # from enum VisUICmds
	visCmdToolSnapLines           =1807       # from enum VisUICmds
	visCmdToolbarsDlg             =1500       # from enum VisUICmds
	visCmdToolsArrayShapesAddOn   =1354       # from enum VisUICmds
	visCmdToolsInventory          =1335       # from enum VisUICmds
	visCmdToolsLayoutShapesDlg    =1574       # from enum VisUICmds
	visCmdToolsMacroDlg           =1577       # from enum VisUICmds
	visCmdToolsRunVBE             =1576       # from enum VisUICmds
	visCmdToolsSecurity           =1884       # from enum VisUICmds
	visCmdToolsShowAddins         =1876       # from enum VisUICmds
	visCmdToolsSpelling           =1270       # from enum VisUICmds
	visCmdTranslateOptions        =2352       # from enum VisUICmds
	visCmdTrim                    =1534       # from enum VisUICmds
	visCmdTrustCenterDlg          =2104       # from enum VisUICmds
	visCmdTurnToNextPage          =1148       # from enum VisUICmds
	visCmdTurnToPrevPage          =1147       # from enum VisUICmds
	visCmdUFEditClear             =1023       # from enum VisUICmds
	visCmdUFEditCopy              =1021       # from enum VisUICmds
	visCmdUFEditCut               =1020       # from enum VisUICmds
	visCmdUFEditDuplicate         =1024       # from enum VisUICmds
	visCmdUFEditPaste             =1022       # from enum VisUICmds
	visCmdUFEditSelectAll         =1025       # from enum VisUICmds
	visCmdUpdateColumnsInLinkedShapes=2061       # from enum VisUICmds
	visCmdUpdateContentCache      =1241       # from enum VisUICmds
	visCmdUpgradeThemeModel       =2384       # from enum VisUICmds
	visCmdValidateDiagram         =2253       # from enum VisUICmds
	visCmdValidationIssueNavigateToShape=2326       # from enum VisUICmds
	visCmdValidationIssuesArrangeByCategory=2279       # from enum VisUICmds
	visCmdValidationIssuesArrangeByIgnored=2281       # from enum VisUICmds
	visCmdValidationIssuesArrangeByPage=2280       # from enum VisUICmds
	visCmdValidationIssuesArrangeByRule=2278       # from enum VisUICmds
	visCmdValidationIssuesArrangeOriginalOrder=2282       # from enum VisUICmds
	visCmdValidationIssuesWindowToggle=2263       # from enum VisUICmds
	visCmdView100                 =1035       # from enum VisUICmds
	visCmdView150                 =1036       # from enum VisUICmds
	visCmdView200                 =1037       # from enum VisUICmds
	visCmdView400                 =1280       # from enum VisUICmds
	visCmdView50                  =1279       # from enum VisUICmds
	visCmdView75                  =1034       # from enum VisUICmds
	visCmdViewConnections         =1042       # from enum VisUICmds
	visCmdViewCustom              =1038       # from enum VisUICmds
	visCmdViewDirectionToggle     =2012       # from enum VisUICmds
	visCmdViewFitInWindow         =1033       # from enum VisUICmds
	visCmdViewGrid                =1040       # from enum VisUICmds
	visCmdViewGuides              =1041       # from enum VisUICmds
	visCmdViewLeftToRight         =2013       # from enum VisUICmds
	visCmdViewPageBreaks          =1509       # from enum VisUICmds
	visCmdViewRightToLeft         =2014       # from enum VisUICmds
	visCmdViewRulers              =1039       # from enum VisUICmds
	visCmdViewStatusBar           =1044       # from enum VisUICmds
	visCmdWindowCascadeAll        =1086       # from enum VisUICmds
	visCmdWindowNewWindow         =1085       # from enum VisUICmds
	visCmdWindowShowDrawPage      =1091       # from enum VisUICmds
	visCmdWindowShowMasterObjects =1089       # from enum VisUICmds
	visCmdWindowShowShapeSheet    =1088       # from enum VisUICmds
	visCmdWindowTileAll           =1087       # from enum VisUICmds
	visCmdZoomArea                =1218       # from enum VisUICmds
	visCmdZoomIn                  =1216       # from enum VisUICmds
	visCmdZoomInIgnoreSel         =1917       # from enum VisUICmds
	visCmdZoomLast                =1495       # from enum VisUICmds
	visCmdZoomOut                 =1217       # from enum VisUICmds
	visCmdZoomOutIgnoreSel        =1918       # from enum VisUICmds
	visCmdZoomPageWidth           =1496       # from enum VisUICmds
	visCmdZoomPt                  =1215       # from enum VisUICmds
	visCmdZoomSingleTile          =1512       # from enum VisUICmds
	visCtrlAlignmentBOX           =128        # from enum VisUICtrlAtts
	visCtrlAlignmentCENTER        =2          # from enum VisUICtrlAtts
	visCtrlAlignmentCENTERBOX     =130        # from enum VisUICtrlAtts
	visCtrlAlignmentLEFT          =1          # from enum VisUICtrlAtts
	visCtrlAlignmentLEFTBOX       =129        # from enum VisUICtrlAtts
	visCtrlAlignmentRIGHT         =4          # from enum VisUICtrlAtts
	visCtrlAlignmentRIGHTBOX      =132        # from enum VisUICtrlAtts
	visCtrlIDACCEPTFORMULA        =85         # from enum VisUICtrlIDs
	visCtrlIDALIGN                =63         # from enum VisUICtrlIDs
	visCtrlIDALIGNBOTTOM          =69         # from enum VisUICtrlIDs
	visCtrlIDALIGNCENTER          =65         # from enum VisUICtrlIDs
	visCtrlIDALIGNLEFT            =64         # from enum VisUICtrlIDs
	visCtrlIDALIGNMIDDLE          =68         # from enum VisUICtrlIDs
	visCtrlIDALIGNRIGHT           =66         # from enum VisUICtrlIDs
	visCtrlIDALIGNSHAPES          =260        # from enum VisUICtrlIDs
	visCtrlIDALIGNTOP             =67         # from enum VisUICtrlIDs
	visCtrlIDALLSTYLESCOMBO       =200        # from enum VisUICtrlIDs
	visCtrlIDALLSTYLESLABEL       =400        # from enum VisUICtrlIDs
	visCtrlIDALLSTYLESLIST        =220        # from enum VisUICtrlIDs
	visCtrlIDARRANGEICONS         =83         # from enum VisUICtrlIDs
	visCtrlIDBOLD                 =50         # from enum VisUICtrlIDs
	visCtrlIDBRINGFRONT           =90         # from enum VisUICtrlIDs
	visCtrlIDBULLETS              =113        # from enum VisUICtrlIDs
	visCtrlIDCANCELFORMULA        =84         # from enum VisUICtrlIDs
	visCtrlIDCASCADE              =94         # from enum VisUICtrlIDs
	visCtrlIDCLEAR                =9          # from enum VisUICtrlIDs
	visCtrlIDCLOSE                =240        # from enum VisUICtrlIDs
	visCtrlIDCOLOR1               =302        # from enum VisUICtrlIDs
	visCtrlIDCOLOR10              =311        # from enum VisUICtrlIDs
	visCtrlIDCOLOR11              =312        # from enum VisUICtrlIDs
	visCtrlIDCOLOR12              =313        # from enum VisUICtrlIDs
	visCtrlIDCOLOR13              =314        # from enum VisUICtrlIDs
	visCtrlIDCOLOR14              =315        # from enum VisUICtrlIDs
	visCtrlIDCOLOR15              =316        # from enum VisUICtrlIDs
	visCtrlIDCOLOR16              =317        # from enum VisUICtrlIDs
	visCtrlIDCOLOR2               =303        # from enum VisUICtrlIDs
	visCtrlIDCOLOR3               =304        # from enum VisUICtrlIDs
	visCtrlIDCOLOR4               =305        # from enum VisUICtrlIDs
	visCtrlIDCOLOR5               =306        # from enum VisUICtrlIDs
	visCtrlIDCOLOR6               =307        # from enum VisUICtrlIDs
	visCtrlIDCOLOR7               =308        # from enum VisUICtrlIDs
	visCtrlIDCOLOR8               =309        # from enum VisUICtrlIDs
	visCtrlIDCOLOR9               =310        # from enum VisUICtrlIDs
	visCtrlIDCONNECT              =36         # from enum VisUICtrlIDs
	visCtrlIDCONNECTIONPTTOOL     =30         # from enum VisUICtrlIDs
	visCtrlIDCONNECTORTOOL        =96         # from enum VisUICtrlIDs
	visCtrlIDCONNECTSHAPES        =75         # from enum VisUICtrlIDs
	visCtrlIDCOPY                 =7          # from enum VisUICtrlIDs
	visCtrlIDCORNERSTYLE          =40         # from enum VisUICtrlIDs
	visCtrlIDCROPTOOL             =29         # from enum VisUICtrlIDs
	visCtrlIDCUSTPROP             =111        # from enum VisUICtrlIDs
	visCtrlIDCUT                  =6          # from enum VisUICtrlIDs
	visCtrlIDDECRINDENT           =114        # from enum VisUICtrlIDs
	visCtrlIDDECRPARA             =116        # from enum VisUICtrlIDs
	visCtrlIDDESIGNMODE           =119        # from enum VisUICtrlIDs
	visCtrlIDDHORZ_CENTER         =72         # from enum VisUICtrlIDs
	visCtrlIDDHORZ_EQSPACE        =71         # from enum VisUICtrlIDs
	visCtrlIDDISTRIBUTE           =70         # from enum VisUICtrlIDs
	visCtrlIDDISTRIBUTESHAPES     =261        # from enum VisUICtrlIDs
	visCtrlIDDVERT_EQSPACE        =73         # from enum VisUICtrlIDs
	visCtrlIDDVERT_MIDDLE         =74         # from enum VisUICtrlIDs
	visCtrlIDFILLCOLOR            =43         # from enum VisUICtrlIDs
	visCtrlIDFILLCOLORS           =244        # from enum VisUICtrlIDs
	visCtrlIDFILLPATTERN          =47         # from enum VisUICtrlIDs
	visCtrlIDFILLPATTERNS         =245        # from enum VisUICtrlIDs
	visCtrlIDFILLSTYLECOMBO       =203        # from enum VisUICtrlIDs
	visCtrlIDFILLSTYLELABEL       =403        # from enum VisUICtrlIDs
	visCtrlIDFILLSTYLELIST        =223        # from enum VisUICtrlIDs
	visCtrlIDFIRSTPAGE            =76         # from enum VisUICtrlIDs
	visCtrlIDFLIPHORZ             =18         # from enum VisUICtrlIDs
	visCtrlIDFLIPVERT             =19         # from enum VisUICtrlIDs
	visCtrlIDFONTCOMBO            =205        # from enum VisUICtrlIDs
	visCtrlIDFONTLABEL            =405        # from enum VisUICtrlIDs
	visCtrlIDFONTLIST             =225        # from enum VisUICtrlIDs
	visCtrlIDFORMATPAINTER        =101        # from enum VisUICtrlIDs
	visCtrlIDFORMULA              =190        # from enum VisUICtrlIDs
	visCtrlIDGLUE                 =32         # from enum VisUICtrlIDs
	visCtrlIDGOBACK               =107        # from enum VisUICtrlIDs
	visCtrlIDGOFORWARD            =108        # from enum VisUICtrlIDs
	visCtrlIDGOTOPAGE             =207        # from enum VisUICtrlIDs
	visCtrlIDGOTOPAGELIST         =227        # from enum VisUICtrlIDs
	visCtrlIDGRID                 =34         # from enum VisUICtrlIDs
	visCtrlIDGROUP                =92         # from enum VisUICtrlIDs
	visCtrlIDGUIDE                =35         # from enum VisUICtrlIDs
	visCtrlIDHELPMODE             =102        # from enum VisUICtrlIDs
	visCtrlIDICONBUCKET           =87         # from enum VisUICtrlIDs
	visCtrlIDICONLASSO            =88         # from enum VisUICtrlIDs
	visCtrlIDICONNAME             =80         # from enum VisUICtrlIDs
	visCtrlIDICONONLY             =81         # from enum VisUICtrlIDs
	visCtrlIDICONPENCIL           =86         # from enum VisUICtrlIDs
	visCtrlIDICONSELNET           =89         # from enum VisUICtrlIDs
	visCtrlIDINCRINDENT           =115        # from enum VisUICtrlIDs
	visCtrlIDINCRPARA             =117        # from enum VisUICtrlIDs
	visCtrlIDINSERTCONTROL        =118        # from enum VisUICtrlIDs
	visCtrlIDINSERTHYPERLINK      =105        # from enum VisUICtrlIDs
	visCtrlIDITALIC               =51         # from enum VisUICtrlIDs
	visCtrlIDLASTPAGE             =77         # from enum VisUICtrlIDs
	visCtrlIDLAYERPROPERTIES      =103        # from enum VisUICtrlIDs
	visCtrlIDLAYOUTSHAPES         =104        # from enum VisUICtrlIDs
	visCtrlIDLEFTCOLORBOX         =300        # from enum VisUICtrlIDs
	visCtrlIDLEFTCOLORLABEL       =407        # from enum VisUICtrlIDs
	visCtrlIDLINECOLOR            =44         # from enum VisUICtrlIDs
	visCtrlIDLINECOLORS           =241        # from enum VisUICtrlIDs
	visCtrlIDLINEEND              =41         # from enum VisUICtrlIDs
	visCtrlIDLINEPATTERN          =46         # from enum VisUICtrlIDs
	visCtrlIDLINEPATTERNS         =243        # from enum VisUICtrlIDs
	visCtrlIDLINESTYLECOMBO       =202        # from enum VisUICtrlIDs
	visCtrlIDLINESTYLELABEL       =402        # from enum VisUICtrlIDs
	visCtrlIDLINESTYLELIST        =222        # from enum VisUICtrlIDs
	visCtrlIDLINETOOL             =22         # from enum VisUICtrlIDs
	visCtrlIDLINEWEIGHT           =45         # from enum VisUICtrlIDs
	visCtrlIDLINEWEIGHTS          =242        # from enum VisUICtrlIDs
	visCtrlIDMACROS               =121        # from enum VisUICtrlIDs
	visCtrlIDMSG_PAGES            =510        # from enum VisUICtrlIDs
	visCtrlIDNAMEONLY             =82         # from enum VisUICtrlIDs
	visCtrlIDNEW                  =8383       # from enum VisUICtrlIDs
	visCtrlIDNEWWINDOW            =39         # from enum VisUICtrlIDs
	visCtrlIDNEXTPAGE             =14         # from enum VisUICtrlIDs
	visCtrlIDOPEN                 =1          # from enum VisUICtrlIDs
	visCtrlIDOPENSTEN             =2          # from enum VisUICtrlIDs
	visCtrlIDOVALTOOL             =25         # from enum VisUICtrlIDs
	visCtrlIDPAGEBREAKS           =78         # from enum VisUICtrlIDs
	visCtrlIDPASTE                =8          # from enum VisUICtrlIDs
	visCtrlIDPENCILTOOL           =21         # from enum VisUICtrlIDs
	visCtrlIDPOINTERTOOL          =20         # from enum VisUICtrlIDs
	visCtrlIDPOINTSIZECOMBO       =206        # from enum VisUICtrlIDs
	visCtrlIDPOINTSIZEDOWN        =48         # from enum VisUICtrlIDs
	visCtrlIDPOINTSIZELABEL       =406        # from enum VisUICtrlIDs
	visCtrlIDPOINTSIZELIST        =226        # from enum VisUICtrlIDs
	visCtrlIDPOINTSIZEUP          =49         # from enum VisUICtrlIDs
	visCtrlIDPREVIEW              =5          # from enum VisUICtrlIDs
	visCtrlIDPREVIEWLABEL         =410        # from enum VisUICtrlIDs
	visCtrlIDPREVIOUSPAGE         =13         # from enum VisUICtrlIDs
	visCtrlIDPRINT                =4          # from enum VisUICtrlIDs
	visCtrlIDQTRARCTOOL           =23         # from enum VisUICtrlIDs
	visCtrlIDRECTTOOL             =24         # from enum VisUICtrlIDs
	visCtrlIDREDO                 =11         # from enum VisUICtrlIDs
	visCtrlIDREPEAT               =12         # from enum VisUICtrlIDs
	visCtrlIDRIGHTCOLORBOX        =301        # from enum VisUICtrlIDs
	visCtrlIDRIGHTCOLORLABEL      =408        # from enum VisUICtrlIDs
	visCtrlIDROTATECLOCKWISE      =37         # from enum VisUICtrlIDs
	visCtrlIDROTATECOUNTER        =38         # from enum VisUICtrlIDs
	visCtrlIDROTATETEXT           =112        # from enum VisUICtrlIDs
	visCtrlIDROTATETOOL           =28         # from enum VisUICtrlIDs
	visCtrlIDRULER                =33         # from enum VisUICtrlIDs
	visCtrlIDSAVE                 =3          # from enum VisUICtrlIDs
	visCtrlIDSEARCHTHEWEB         =106        # from enum VisUICtrlIDs
	visCtrlIDSENDBACK             =91         # from enum VisUICtrlIDs
	visCtrlIDSHADOWSTYLE          =42         # from enum VisUICtrlIDs
	visCtrlIDSHAPEEXPL            =110        # from enum VisUICtrlIDs
	visCtrlIDSHAPELAYER           =247        # from enum VisUICtrlIDs
	visCtrlIDSHAPELAYERCOMBO      =208        # from enum VisUICtrlIDs
	visCtrlIDSHAPELAYERLIST       =228        # from enum VisUICtrlIDs
	visCtrlIDSHAPESHEET           =120        # from enum VisUICtrlIDs
	visCtrlIDSINGLETILE           =99         # from enum VisUICtrlIDs
	visCtrlIDSNAP                 =31         # from enum VisUICtrlIDs
	visCtrlIDSPACER               =191        # from enum VisUICtrlIDs
	visCtrlIDSPELLING             =100        # from enum VisUICtrlIDs
	visCtrlIDSPLINETOOL           =79         # from enum VisUICtrlIDs
	visCtrlIDSTAMPTOOL            =26         # from enum VisUICtrlIDs
	visCtrlIDSTATUSLABEL          =409        # from enum VisUICtrlIDs
	visCtrlIDSTATUSMSG_1          =501        # from enum VisUICtrlIDs
	visCtrlIDSTATUSMSG_2          =502        # from enum VisUICtrlIDs
	visCtrlIDSTATUSMSG_3          =503        # from enum VisUICtrlIDs
	visCtrlIDSTATUSMSG_4          =504        # from enum VisUICtrlIDs
	visCtrlIDSTATUSMSG_5          =505        # from enum VisUICtrlIDs
	visCtrlIDSTATUSMSG_6          =506        # from enum VisUICtrlIDs
	visCtrlIDSTATUSMSG_7          =507        # from enum VisUICtrlIDs
	visCtrlIDSTATUSMSG_8          =508        # from enum VisUICtrlIDs
	visCtrlIDSTATUSMSG_9          =509        # from enum VisUICtrlIDs
	visCtrlIDSTATUSREADOUT        =500        # from enum VisUICtrlIDs
	visCtrlIDSUBSCRIPT            =54         # from enum VisUICtrlIDs
	visCtrlIDSUPERSCRIPT          =53         # from enum VisUICtrlIDs
	visCtrlIDTEXTBLOCKTOOL        =97         # from enum VisUICtrlIDs
	visCtrlIDTEXTBOTTOM           =62         # from enum VisUICtrlIDs
	visCtrlIDTEXTCENTER           =57         # from enum VisUICtrlIDs
	visCtrlIDTEXTCOLOR            =55         # from enum VisUICtrlIDs
	visCtrlIDTEXTCOLORS           =246        # from enum VisUICtrlIDs
	visCtrlIDTEXTJUSTIFY          =59         # from enum VisUICtrlIDs
	visCtrlIDTEXTLEFT             =56         # from enum VisUICtrlIDs
	visCtrlIDTEXTMIDDLE           =61         # from enum VisUICtrlIDs
	visCtrlIDTEXTRIGHT            =58         # from enum VisUICtrlIDs
	visCtrlIDTEXTSTYLECOMBO       =201        # from enum VisUICtrlIDs
	visCtrlIDTEXTSTYLELABEL       =401        # from enum VisUICtrlIDs
	visCtrlIDTEXTSTYLELIST        =221        # from enum VisUICtrlIDs
	visCtrlIDTEXTTOOL             =27         # from enum VisUICtrlIDs
	visCtrlIDTEXTTOP              =60         # from enum VisUICtrlIDs
	visCtrlIDTILE                 =95         # from enum VisUICtrlIDs
	visCtrlIDTRANSPARENT          =318        # from enum VisUICtrlIDs
	visCtrlIDULINE                =52         # from enum VisUICtrlIDs
	visCtrlIDUNDO                 =10         # from enum VisUICtrlIDs
	visCtrlIDUNGROUP              =93         # from enum VisUICtrlIDs
	visCtrlIDVBEDITOR             =122        # from enum VisUICtrlIDs
	visCtrlIDWEBTOOLBAR           =109        # from enum VisUICtrlIDs
	visCtrlIDWHOLEPAGE            =98         # from enum VisUICtrlIDs
	visCtrlIDZOOM100              =17         # from enum VisUICtrlIDs
	visCtrlIDZOOMCOMBO            =204        # from enum VisUICtrlIDs
	visCtrlIDZOOMIN               =16         # from enum VisUICtrlIDs
	visCtrlIDZOOMLABEL            =404        # from enum VisUICtrlIDs
	visCtrlIDZOOMLIST             =224        # from enum VisUICtrlIDs
	visCtrlIDZOOMOUT              =15         # from enum VisUICtrlIDs
	visCtrlTypeBUTTON             =2          # from enum VisUICtrlTypes
	visCtrlTypeBUTTON_OWNERDRAW   =33         # from enum VisUICtrlTypes
	visCtrlTypeCOLORBOX           =1024       # from enum VisUICtrlTypes
	visCtrlTypeCOMBOBOX           =128        # from enum VisUICtrlTypes
	visCtrlTypeCOMBOBOX_SORTED    =129        # from enum VisUICtrlTypes
	visCtrlTypeCOMBODRAW          =256        # from enum VisUICtrlTypes
	visCtrlTypeDROPBUTTON         =8          # from enum VisUICtrlTypes
	visCtrlTypeDROPDOWN           =272        # from enum VisUICtrlTypes
	visCtrlTypeDROPDOWN_OWNERDRAW =256        # from enum VisUICtrlTypes
	visCtrlTypeDROPDOWN_SORTED    =273        # from enum VisUICtrlTypes
	visCtrlTypeDROPDOWN_SORTED_OWNERDRAW=257        # from enum VisUICtrlTypes
	visCtrlTypeEDITBOX            =64         # from enum VisUICtrlTypes
	visCtrlTypeEND                =0          # from enum VisUICtrlTypes
	visCtrlTypeHIERBUTTON         =4          # from enum VisUICtrlTypes
	visCtrlTypeLABEL              =2048       # from enum VisUICtrlTypes
	visCtrlTypeLISTBOX            =512        # from enum VisUICtrlTypes
	visCtrlTypeLISTBOXDRAW        =513        # from enum VisUICtrlTypes
	visCtrlTypeMESSAGE            =4096       # from enum VisUICtrlTypes
	visCtrlTypeOWNERDRAW_BUTTON   =33         # from enum VisUICtrlTypes
	visCtrlTypePALETTEBUTTON      =16         # from enum VisUICtrlTypes
	visCtrlTypePALETTEBUTTONICON  =18         # from enum VisUICtrlTypes
	visCtrlTypePALETTEBUTTONNOMRU =17         # from enum VisUICtrlTypes
	visCtrlTypePUSHBUTTON         =32         # from enum VisUICtrlTypes
	visCtrlTypeSPACER             =16384      # from enum VisUICtrlTypes
	visCtrlTypeSPINBUTTON         =16         # from enum VisUICtrlTypes
	visCtrlTypeSPLITBUTTON        =17         # from enum VisUICtrlTypes
	visCtrlTypeSPLITBUTTON_MRU_COLOR=16         # from enum VisUICtrlTypes
	visCtrlTypeSPLITBUTTON_MRU_COMMAND=18         # from enum VisUICtrlTypes
	visCtrlTypeSTATE              =1          # from enum VisUICtrlTypes
	visCtrlTypeSTATE_BUTTON       =3          # from enum VisUICtrlTypes
	visCtrlTypeSTATE_DROPBUTTON   =9          # from enum VisUICtrlTypes
	visCtrlTypeSTATE_HIERBUTTON   =5          # from enum VisUICtrlTypes
	visCtrlTypeSWATCH             =32768      # from enum VisUICtrlTypes
	visCtrlTypeSWATCH_COLORS      =32769      # from enum VisUICtrlTypes
	visIconIXACCEPT               =85         # from enum VisUIIconIDs
	visIconIXADDIN                =149        # from enum VisUIIconIDs
	visIconIXALIGN                =63         # from enum VisUIIconIDs
	visIconIXALIGNBOTTOM          =69         # from enum VisUIIconIDs
	visIconIXALIGNBOX             =224        # from enum VisUIIconIDs
	visIconIXALIGNCENTER          =65         # from enum VisUIIconIDs
	visIconIXALIGNLEFT            =64         # from enum VisUIIconIDs
	visIconIXALIGNMIDDLE          =68         # from enum VisUIIconIDs
	visIconIXALIGNRIGHT           =66         # from enum VisUIIconIDs
	visIconIXALIGNTOP             =67         # from enum VisUIIconIDs
	visIconIXARRANGE              =83         # from enum VisUIIconIDs
	visIconIXBOLD                 =50         # from enum VisUIIconIDs
	visIconIXBRINGFRONT           =90         # from enum VisUIIconIDs
	visIconIXBRING_FORWARD        =245        # from enum VisUIIconIDs
	visIconIXBULLETS              =113        # from enum VisUIIconIDs
	visIconIXCANCEL               =84         # from enum VisUIIconIDs
	visIconIXCANTFIND             =129        # from enum VisUIIconIDs
	visIconIXCASCADE              =94         # from enum VisUIIconIDs
	visIconIXCHART                =134        # from enum VisUIIconIDs
	visIconIXCHECKMARK            =128        # from enum VisUIIconIDs
	visIconIXCLEAR                =9          # from enum VisUIIconIDs
	visIconIXCLIPART              =130        # from enum VisUIIconIDs
	visIconIXCLOSE                =143        # from enum VisUIIconIDs
	visIconIXCONNECTIONPOINTS     =36         # from enum VisUIIconIDs
	visIconIXCONNECTIONPTTOOL     =30         # from enum VisUIIconIDs
	visIconIXCONNECTORTOOL        =96         # from enum VisUIIconIDs
	visIconIXCONNECTSHAPES        =75         # from enum VisUIIconIDs
	visIconIXCONNPOINTS           =229        # from enum VisUIIconIDs
	visIconIXCOPY                 =7          # from enum VisUIIconIDs
	visIconIXCORNERSTYLE          =40         # from enum VisUIIconIDs
	visIconIXCROP                 =29         # from enum VisUIIconIDs
	visIconIXCUSTOMPROP_WINDOW    =215        # from enum VisUIIconIDs
	visIconIXCUSTOM_BALLOON       =162        # from enum VisUIIconIDs
	visIconIXCUSTOM_BANK          =153        # from enum VisUIIconIDs
	visIconIXCUSTOM_BELL          =159        # from enum VisUIIconIDs
	visIconIXCUSTOM_BOX           =173        # from enum VisUIIconIDs
	visIconIXCUSTOM_CALC          =164        # from enum VisUIIconIDs
	visIconIXCUSTOM_CAMCORD       =163        # from enum VisUIIconIDs
	visIconIXCUSTOM_CARDS         =169        # from enum VisUIIconIDs
	visIconIXCUSTOM_CLUB          =168        # from enum VisUIIconIDs
	visIconIXCUSTOM_DIAMOND       =166        # from enum VisUIIconIDs
	visIconIXCUSTOM_DOWN          =178        # from enum VisUIIconIDs
	visIconIXCUSTOM_EIGHTBALL     =191        # from enum VisUIIconIDs
	visIconIXCUSTOM_EYE           =190        # from enum VisUIIconIDs
	visIconIXCUSTOM_FEET          =174        # from enum VisUIIconIDs
	visIconIXCUSTOM_FISH          =182        # from enum VisUIIconIDs
	visIconIXCUSTOM_FROWN         =152        # from enum VisUIIconIDs
	visIconIXCUSTOM_GEARS         =184        # from enum VisUIIconIDs
	visIconIXCUSTOM_HEART         =165        # from enum VisUIIconIDs
	visIconIXCUSTOM_HOURGLASS     =186        # from enum VisUIIconIDs
	visIconIXCUSTOM_KEY           =183        # from enum VisUIIconIDs
	visIconIXCUSTOM_KEYBOARD      =180        # from enum VisUIIconIDs
	visIconIXCUSTOM_LEFT          =175        # from enum VisUIIconIDs
	visIconIXCUSTOM_LOAD          =155        # from enum VisUIIconIDs
	visIconIXCUSTOM_MAN           =187        # from enum VisUIIconIDs
	visIconIXCUSTOM_MIC           =157        # from enum VisUIIconIDs
	visIconIXCUSTOM_MUG           =170        # from enum VisUIIconIDs
	visIconIXCUSTOM_NOTE          =160        # from enum VisUIIconIDs
	visIconIXCUSTOM_PAGES         =181        # from enum VisUIIconIDs
	visIconIXCUSTOM_PASTE         =154        # from enum VisUIIconIDs
	visIconIXCUSTOM_PENCIL        =172        # from enum VisUIIconIDs
	visIconIXCUSTOM_PHONE         =161        # from enum VisUIIconIDs
	visIconIXCUSTOM_QUESTION      =192        # from enum VisUIIconIDs
	visIconIXCUSTOM_RIGHT         =176        # from enum VisUIIconIDs
	visIconIXCUSTOM_RUN           =189        # from enum VisUIIconIDs
	visIconIXCUSTOM_SAVE          =156        # from enum VisUIIconIDs
	visIconIXCUSTOM_SCALES        =185        # from enum VisUIIconIDs
	visIconIXCUSTOM_SMILE         =151        # from enum VisUIIconIDs
	visIconIXCUSTOM_SPADE         =167        # from enum VisUIIconIDs
	visIconIXCUSTOM_SPEAKER       =158        # from enum VisUIIconIDs
	visIconIXCUSTOM_TACK          =179        # from enum VisUIIconIDs
	visIconIXCUSTOM_TRASH         =171        # from enum VisUIIconIDs
	visIconIXCUSTOM_UP            =177        # from enum VisUIIconIDs
	visIconIXCUSTOM_WOMAN         =188        # from enum VisUIIconIDs
	visIconIXCUSTPROP             =111        # from enum VisUIIconIDs
	visIconIXCUT                  =6          # from enum VisUIIconIDs
	visIconIXDCREROUTE            =236        # from enum VisUIIconIDs
	visIconIXDCREROUTE_ASNEEDED   =214        # from enum VisUIIconIDs
	visIconIXDCREROUTE_FREELY     =213        # from enum VisUIIconIDs
	visIconIXDCREROUTE_NEVER      =235        # from enum VisUIIconIDs
	visIconIXDECRINDENT           =114        # from enum VisUIIconIDs
	visIconIXDECRPARA             =116        # from enum VisUIIconIDs
	visIconIXDELETE               =196        # from enum VisUIIconIDs
	visIconIXDELETECOMMENT        =195        # from enum VisUIIconIDs
	visIconIXDESIGNMODE           =119        # from enum VisUIIconIDs
	visIconIXDHORZ_CENTER         =72         # from enum VisUIIconIDs
	visIconIXDHORZ_EQSPACE        =71         # from enum VisUIIconIDs
	visIconIXDISTRIBUTE           =70         # from enum VisUIIconIDs
	visIconIXDOUBLE_UNDERLINE     =253        # from enum VisUIIconIDs
	visIconIXDRAWINGEXPLORER      =219        # from enum VisUIIconIDs
	visIconIXDVERT_EQSPACE        =73         # from enum VisUIIconIDs
	visIconIXDVERT_MIDDLE         =74         # from enum VisUIIconIDs
	visIconIXDYNGRID              =221        # from enum VisUIIconIDs
	visIconIXEDITCOMMENT          =194        # from enum VisUIIconIDs
	visIconIXEDITSTEN             =197        # from enum VisUIIconIDs
	visIconIXEXCHANGEFOLDER       =137        # from enum VisUIIconIDs
	visIconIXFILLCOLOR            =43         # from enum VisUIIconIDs
	visIconIXFILLPATTERN          =47         # from enum VisUIIconIDs
	visIconIXFIND                 =138        # from enum VisUIIconIDs
	visIconIXFIRSTPAGE            =76         # from enum VisUIIconIDs
	visIconIXFLIPHORIZONTAL       =18         # from enum VisUIIconIDs
	visIconIXFLIPVERTICAL         =19         # from enum VisUIIconIDs
	visIconIXFOLDER               =144        # from enum VisUIIconIDs
	visIconIXFORMATPAINTER        =101        # from enum VisUIIconIDs
	visIconIXFULLSCREEN           =124        # from enum VisUIIconIDs
	visIconIXGLUE                 =32         # from enum VisUIIconIDs
	visIconIXGOBACK               =107        # from enum VisUIIconIDs
	visIconIXGOFORWARD            =108        # from enum VisUIIconIDs
	visIconIXGRID                 =34         # from enum VisUIIconIDs
	visIconIXGROUP                =92         # from enum VisUIIconIDs
	visIconIXGUIDE                =35         # from enum VisUIIconIDs
	visIconIXGUIDES               =226        # from enum VisUIIconIDs
	visIconIXHELPASSISTANT        =133        # from enum VisUIIconIDs
	visIconIXHELPBOOK             =125        # from enum VisUIIconIDs
	visIconIXHELPMODE             =102        # from enum VisUIIconIDs
	visIconIXICONBUCKET           =87         # from enum VisUIIconIDs
	visIconIXICONLASSO            =88         # from enum VisUIIconIDs
	visIconIXICONNAME             =80         # from enum VisUIIconIDs
	visIconIXICONONLY             =81         # from enum VisUIIconIDs
	visIconIXICONPENCIL           =86         # from enum VisUIIconIDs
	visIconIXICONSELNET           =89         # from enum VisUIIconIDs
	visIconIXIMAGE                =131        # from enum VisUIIconIDs
	visIconIXINCRINDENT           =115        # from enum VisUIIconIDs
	visIconIXINCRPARA             =117        # from enum VisUIIconIDs
	visIconIXINSERTCOMMENT        =193        # from enum VisUIIconIDs
	visIconIXINSERTCONTROL        =118        # from enum VisUIIconIDs
	visIconIXINSERTHYPERLINK      =105        # from enum VisUIIconIDs
	visIconIXINSERT_EQUATION      =250        # from enum VisUIIconIDs
	visIconIXINSERT_OBJECT        =248        # from enum VisUIIconIDs
	visIconIXITALIC               =51         # from enum VisUIIconIDs
	visIconIXLARGE_PADLOCK        =249        # from enum VisUIIconIDs
	visIconIXLASTPAGE             =77         # from enum VisUIIconIDs
	visIconIXLAYERPROPERTIES      =103        # from enum VisUIIconIDs
	visIconIXLAYOUTSHAPES         =104        # from enum VisUIIconIDs
	visIconIXLINECOLOR            =44         # from enum VisUIIconIDs
	visIconIXLINEEND              =41         # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_2PT    =208        # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_3PT    =209        # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_4PT    =210        # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_5PT    =211        # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_6PT    =212        # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_ARC    =204        # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_GAP    =205        # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_PAGE   =218        # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_SQUARE =206        # from enum VisUIIconIDs
	visIconIXLINEJUMPSTYLE_TRIANGLE=207        # from enum VisUIIconIDs
	visIconIXLINEPATTERN          =46         # from enum VisUIIconIDs
	visIconIXLINETOOL             =22         # from enum VisUIIconIDs
	visIconIXLINEWEIGHT           =45         # from enum VisUIIconIDs
	visIconIXMACROS               =121        # from enum VisUIIconIDs
	visIconIXMAILRECPT            =135        # from enum VisUIIconIDs
	visIconIXMAXIMIZE             =142        # from enum VisUIIconIDs
	visIconIXMINIMIZE             =141        # from enum VisUIIconIDs
	visIconIXNAMEONLY             =82         # from enum VisUIIconIDs
	visIconIXNEW                  =0          # from enum VisUIIconIDs
	visIconIXNEWSTEN              =198        # from enum VisUIIconIDs
	visIconIXNEWWINDOW            =39         # from enum VisUIIconIDs
	visIconIXNEXTPAGE             =14         # from enum VisUIIconIDs
	visIconIXOPEN                 =1          # from enum VisUIIconIDs
	visIconIXOPENSTENCIL          =2          # from enum VisUIIconIDs
	visIconIXOVALTOOL             =25         # from enum VisUIIconIDs
	visIconIXPAGEBREAKS           =78         # from enum VisUIIconIDs
	visIconIXPAGELINEJUMPCODE_DISP=217        # from enum VisUIIconIDs
	visIconIXPAGELINEJUMPCODE_HORZ=201        # from enum VisUIIconIDs
	visIconIXPAGELINEJUMPCODE_LASTROUTED=203        # from enum VisUIIconIDs
	visIconIXPAGELINEJUMPCODE_NONE=200        # from enum VisUIIconIDs
	visIconIXPAGELINEJUMPCODE_RDISP=231        # from enum VisUIIconIDs
	visIconIXPAGELINEJUMPCODE_VERT=202        # from enum VisUIIconIDs
	visIconIXPAGEPLOW             =216        # from enum VisUIIconIDs
	visIconIXPANZOOM              =139        # from enum VisUIIconIDs
	visIconIXPASTE                =8          # from enum VisUIIconIDs
	visIconIXPENCILTOOL           =21         # from enum VisUIIconIDs
	visIconIXPOINTERTOOL          =20         # from enum VisUIIconIDs
	visIconIXPOINTSIZEDOWN        =48         # from enum VisUIIconIDs
	visIconIXPOINTSIZEUP          =49         # from enum VisUIIconIDs
	visIconIXPREVIOUSPAGE         =13         # from enum VisUIIconIDs
	visIconIXPRINT                =4          # from enum VisUIIconIDs
	visIconIXPRINTPREVIEW         =5          # from enum VisUIIconIDs
	visIconIXQTRARCTOOL           =23         # from enum VisUIIconIDs
	visIconIXRECTANGLETOOL        =24         # from enum VisUIIconIDs
	visIconIXREDO                 =11         # from enum VisUIIconIDs
	visIconIXREPEAT               =12         # from enum VisUIIconIDs
	visIconIXREPLACE              =252        # from enum VisUIIconIDs
	visIconIXRESTORE              =140        # from enum VisUIIconIDs
	visIconIXROTATECLOCKWISE      =37         # from enum VisUIIconIDs
	visIconIXROTATECOUNTERCLOCKWISE=38         # from enum VisUIIconIDs
	visIconIXROTATETEXT           =112        # from enum VisUIIconIDs
	visIconIXROTATETOOL           =28         # from enum VisUIIconIDs
	visIconIXROUTINGRECPT         =136        # from enum VisUIIconIDs
	visIconIXRULER                =33         # from enum VisUIIconIDs
	visIconIXRULSUB               =222        # from enum VisUIIconIDs
	visIconIXSAVE                 =3          # from enum VisUIIconIDs
	visIconIXSEARCHTHEWEB         =106        # from enum VisUIIconIDs
	visIconIXSENDBACK             =91         # from enum VisUIIconIDs
	visIconIXSEND_BACKWARD        =246        # from enum VisUIIconIDs
	visIconIXSHADOWSTYLE          =42         # from enum VisUIIconIDs
	visIconIXSHAPEEXPL            =110        # from enum VisUIIconIDs
	visIconIXSHAPEEXPLORER        =126        # from enum VisUIIconIDs
	visIconIXSHAPEEXT             =230        # from enum VisUIIconIDs
	visIconIXSHAPEGEO             =225        # from enum VisUIIconIDs
	visIconIXSHAPEHAND            =227        # from enum VisUIIconIDs
	visIconIXSHAPESHEET           =120        # from enum VisUIIconIDs
	visIconIXSHAPEVERT            =228        # from enum VisUIIconIDs
	visIconIXSHAPE_INTERSECT      =220        # from enum VisUIIconIDs
	visIconIXSHOWDOCSTEN          =199        # from enum VisUIIconIDs
	visIconIXSINGLETILE           =99         # from enum VisUIIconIDs
	visIconIXSIZEPOS              =150        # from enum VisUIIconIDs
	visIconIXSMALLCAPS            =234        # from enum VisUIIconIDs
	visIconIXSMALL_PADLOCK        =247        # from enum VisUIIconIDs
	visIconIXSNAP                 =31         # from enum VisUIIconIDs
	visIconIXSNAPTOGRID           =223        # from enum VisUIIconIDs
	visIconIXSNAP_LINES           =232        # from enum VisUIIconIDs
	visIconIXSPELLING             =100        # from enum VisUIIconIDs
	visIconIXSPLINETOOL           =79         # from enum VisUIIconIDs
	visIconIXSTAMPTOOL            =26         # from enum VisUIIconIDs
	visIconIXSTRIKETHROUGH        =233        # from enum VisUIIconIDs
	visIconIXSTYLE                =251        # from enum VisUIIconIDs
	visIconIXSUBSCRIPT            =54         # from enum VisUIIconIDs
	visIconIXSUPERSCRIPT          =53         # from enum VisUIIconIDs
	visIconIXTEXTALIGNBOTTOM      =62         # from enum VisUIIconIDs
	visIconIXTEXTALIGNCENTER      =57         # from enum VisUIIconIDs
	visIconIXTEXTALIGNJUSTIFY     =59         # from enum VisUIIconIDs
	visIconIXTEXTALIGNLEFT        =56         # from enum VisUIIconIDs
	visIconIXTEXTALIGNMIDDLE      =61         # from enum VisUIIconIDs
	visIconIXTEXTALIGNRIGHT       =58         # from enum VisUIIconIDs
	visIconIXTEXTALIGNTOP         =60         # from enum VisUIIconIDs
	visIconIXTEXTBLOCKTOOL        =97         # from enum VisUIIconIDs
	visIconIXTEXTCOLOR            =55         # from enum VisUIIconIDs
	visIconIXTEXTOOL              =27         # from enum VisUIIconIDs
	visIconIXTILE                 =95         # from enum VisUIIconIDs
	visIconIXUNDERLINE            =52         # from enum VisUIIconIDs
	visIconIXUNDO                 =10         # from enum VisUIIconIDs
	visIconIXUNGROUP              =93         # from enum VisUIIconIDs
	visIconIXVBAMACRO             =148        # from enum VisUIIconIDs
	visIconIXVBEDITOR             =122        # from enum VisUIIconIDs
	visIconIXVERTICALTEXT         =123        # from enum VisUIIconIDs
	visIconIXVSD                  =145        # from enum VisUIIconIDs
	visIconIXVSS                  =146        # from enum VisUIIconIDs
	visIconIXVST                  =147        # from enum VisUIIconIDs
	visIconIXWEBPAGE              =127        # from enum VisUIIconIDs
	visIconIXWEBTOOLBAR           =109        # from enum VisUIIconIDs
	visIconIXWHOLEPAGE            =98         # from enum VisUIIconIDs
	visIconIXWORDART              =132        # from enum VisUIIconIDs
	visIconIXZOOM100              =17         # from enum VisUIIconIDs
	visIconIXZOOMIN               =16         # from enum VisUIIconIDs
	visIconIXZOOMOUT              =15         # from enum VisUIIconIDs
	visMenuAnimationNone          =0          # from enum VisUIMenuAnimation
	visMenuAnimationRandom        =1          # from enum VisUIMenuAnimation
	visMenuAnimationSlide         =3          # from enum VisUIMenuAnimation
	visMenuAnimationUnfold        =2          # from enum VisUIMenuAnimation
	visUIObjSetActiveXDoc         =18         # from enum VisUIObjSets
	visUIObjSetBinderInPlace      =18         # from enum VisUIObjSets
	visUIObjSetCntx_AddCommands   =1000       # from enum VisUIObjSets
	visUIObjSetCntx_AnchorBar_Base=61         # from enum VisUIObjSets
	visUIObjSetCntx_AnchorBar_CustProp=62         # from enum VisUIObjSets
	visUIObjSetCntx_AnchorBar_Shapes=69         # from enum VisUIObjSets
	visUIObjSetCntx_AnchorBar_SizePos=63         # from enum VisUIObjSets
	visUIObjSetCntx_BuiltinMenus  =1010       # from enum VisUIObjSets
	visUIObjSetCntx_CommentMarker =68         # from enum VisUIObjSets
	visUIObjSetCntx_ConnectPtType =44         # from enum VisUIObjSets
	visUIObjSetCntx_DEDocument    =49         # from enum VisUIObjSets
	visUIObjSetCntx_DELayer       =55         # from enum VisUIObjSets
	visUIObjSetCntx_DELayers      =54         # from enum VisUIObjSets
	visUIObjSetCntx_DEMaster      =59         # from enum VisUIObjSets
	visUIObjSetCntx_DEMasters     =58         # from enum VisUIObjSets
	visUIObjSetCntx_DEPage        =51         # from enum VisUIObjSets
	visUIObjSetCntx_DEPages       =50         # from enum VisUIObjSets
	visUIObjSetCntx_DEPatterns    =60         # from enum VisUIObjSets
	visUIObjSetCntx_DEShape       =53         # from enum VisUIObjSets
	visUIObjSetCntx_DEShapes      =52         # from enum VisUIObjSets
	visUIObjSetCntx_DEStyle       =57         # from enum VisUIObjSets
	visUIObjSetCntx_DEStyles      =56         # from enum VisUIObjSets
	visUIObjSetCntx_DataExplorerList=71         # from enum VisUIObjSets
	visUIObjSetCntx_DataExplorerTabs=70         # from enum VisUIObjSets
	visUIObjSetCntx_Debug         =19         # from enum VisUIObjSets
	visUIObjSetCntx_DrawNoObjSel  =11         # from enum VisUIObjSets
	visUIObjSetCntx_DrawObjSel    =9          # from enum VisUIObjSets
	visUIObjSetCntx_DrawOleObjSel =10         # from enum VisUIObjSets
	visUIObjSetCntx_FullScreen    =17         # from enum VisUIObjSets
	visUIObjSetCntx_Hyperlink     =23         # from enum VisUIObjSets
	visUIObjSetCntx_InPlaceNoObj  =12         # from enum VisUIObjSets
	visUIObjSetCntx_Issues        =76         # from enum VisUIObjSets
	visUIObjSetCntx_MEDocument    =66         # from enum VisUIObjSets
	visUIObjSetCntx_MEMasters     =67         # from enum VisUIObjSets
	visUIObjSetCntx_Master        =14         # from enum VisUIObjSets
	visUIObjSetCntx_Page          =75         # from enum VisUIObjSets
	visUIObjSetCntx_PageTabNavigation=74         # from enum VisUIObjSets
	visUIObjSetCntx_PageTabs      =47         # from enum VisUIObjSets
	visUIObjSetCntx_ShapeSheet    =15         # from enum VisUIObjSets
	visUIObjSetCntx_ShortcutMenus =1011       # from enum VisUIObjSets
	visUIObjSetCntx_Stencil       =21         # from enum VisUIObjSets
	visUIObjSetCntx_StencilDocked =21         # from enum VisUIObjSets
	visUIObjSetCntx_StencilRO     =14         # from enum VisUIObjSets
	visUIObjSetCntx_StencilRW     =20         # from enum VisUIObjSets
	visUIObjSetCntx_TextEdit      =13         # from enum VisUIObjSets
	visUIObjSetCntx_Toolbar       =16         # from enum VisUIObjSets
	visUIObjSetCntx_ToolbarHostingInPlace=36         # from enum VisUIObjSets
	visUIObjSetCntx_ToolbarInPlace=35         # from enum VisUIObjSets
	visUIObjSetDrawing            =2          # from enum VisUIObjSets
	visUIObjSetHostingInPlace     =22         # from enum VisUIObjSets
	visUIObjSetIcon               =5          # from enum VisUIObjSets
	visUIObjSetInPlace            =6          # from enum VisUIObjSets
	visUIObjSetNoDocument         =1          # from enum VisUIObjSets
	visUIObjSetPal_AlignShapes    =30         # from enum VisUIObjSets
	visUIObjSetPal_ConnectorTool  =40         # from enum VisUIObjSets
	visUIObjSetPal_CornerRounding =34         # from enum VisUIObjSets
	visUIObjSetPal_DistributeShapes=31         # from enum VisUIObjSets
	visUIObjSetPal_FillColors     =27         # from enum VisUIObjSets
	visUIObjSetPal_FillPatterns   =28         # from enum VisUIObjSets
	visUIObjSetPal_LineColors     =24         # from enum VisUIObjSets
	visUIObjSetPal_LineEnds       =33         # from enum VisUIObjSets
	visUIObjSetPal_LinePatterns   =26         # from enum VisUIObjSets
	visUIObjSetPal_LineTool       =42         # from enum VisUIObjSets
	visUIObjSetPal_LineWeights    =25         # from enum VisUIObjSets
	visUIObjSetPal_Rectangle_Tool =37         # from enum VisUIObjSets
	visUIObjSetPal_Redo           =46         # from enum VisUIObjSets
	visUIObjSetPal_RotationTool   =43         # from enum VisUIObjSets
	visUIObjSetPal_Shadow         =32         # from enum VisUIObjSets
	visUIObjSetPal_ShapeExt       =48         # from enum VisUIObjSets
	visUIObjSetPal_TextColors     =29         # from enum VisUIObjSets
	visUIObjSetPal_TextTool       =41         # from enum VisUIObjSets
	visUIObjSetPal_Undo           =45         # from enum VisUIObjSets
	visUIObjSetPopup_LineJumpCode =38         # from enum VisUIObjSets
	visUIObjSetPopup_LineJumpStyle=39         # from enum VisUIObjSets
	visUIObjSetPrintPreview       =7          # from enum VisUIObjSets
	visUIObjSetShapeSheet         =4          # from enum VisUIObjSets
	visUIObjSetStencil            =3          # from enum VisUIObjSets
	visUIObjSetText               =8          # from enum VisUIObjSets
	visCtrlSpacingFIXED_AFTER     =8          # from enum VisUISpacingTypes
	visCtrlSpacingFIXED_BEFORE    =4          # from enum VisUISpacingTypes
	visCtrlSpacingNEW_ROW         =16         # from enum VisUISpacingTypes
	visCtrlSpacingNEW_ROW_PALETTERIGHT=80         # from enum VisUISpacingTypes
	visCtrlSpacingNONE            =0          # from enum VisUISpacingTypes
	visCtrlSpacingPALETTERIGHT    =64         # from enum VisUISpacingTypes
	visCtrlSpacingTB_NOTFIXED     =32         # from enum VisUISpacingTypes
	visCtrlSpacingVARIABLE_AFTER  =2          # from enum VisUISpacingTypes
	visCtrlSpacingVARIABLE_BEFORE =1          # from enum VisUISpacingTypes
	visStrIDPlaceHolder           =0          # from enum VisUIStringIDs
	visDeleteGUID                 =2          # from enum VisUniqueIDArgs
	visDeleteGUIDWithUndo         =4          # from enum VisUniqueIDArgs
	visGetGUID                    =0          # from enum VisUniqueIDArgs
	visGetOrMakeGUID              =1          # from enum VisUniqueIDArgs
	visGetOrMakeGUIDWithUndo      =3          # from enum VisUniqueIDArgs
	visAcre                       =36         # from enum VisUnitCodes
	visAngleUnits                 =80         # from enum VisUnitCodes
	visCentimeters                =69         # from enum VisUnitCodes
	visCiceros                    =54         # from enum VisUnitCodes
	visCicerosAndDidots           =52         # from enum VisUnitCodes
	visCurrency                   =111        # from enum VisUnitCodes
	visDate                       =40         # from enum VisUnitCodes
	visDegreeMinSec               =82         # from enum VisUnitCodes
	visDegrees                    =81         # from enum VisUnitCodes
	visDidots                     =53         # from enum VisUnitCodes
	visDrawingUnits               =64         # from enum VisUnitCodes
	visDurationUnits              =42         # from enum VisUnitCodes
	visElapsedDay                 =44         # from enum VisUnitCodes
	visElapsedHour                =45         # from enum VisUnitCodes
	visElapsedMin                 =46         # from enum VisUnitCodes
	visElapsedSec                 =47         # from enum VisUnitCodes
	visElapsedWeek                =43         # from enum VisUnitCodes
	visFeet                       =66         # from enum VisUnitCodes
	visFeetAndInches              =67         # from enum VisUnitCodes
	visHectare                    =37         # from enum VisUnitCodes
	visInchFrac                   =73         # from enum VisUnitCodes
	visInches                     =65         # from enum VisUnitCodes
	visKilometers                 =72         # from enum VisUnitCodes
	visMeters                     =71         # from enum VisUnitCodes
	visMileFrac                   =74         # from enum VisUnitCodes
	visMiles                      =68         # from enum VisUnitCodes
	visMillimeters                =70         # from enum VisUnitCodes
	visMin                        =84         # from enum VisUnitCodes
	visNautMiles                  =76         # from enum VisUnitCodes
	visNoCast                     =252        # from enum VisUnitCodes
	visNumber                     =32         # from enum VisUnitCodes
	visPageUnits                  =63         # from enum VisUnitCodes
	visPercent                    =33         # from enum VisUnitCodes
	visPicas                      =51         # from enum VisUnitCodes
	visPicasAndPoints             =49         # from enum VisUnitCodes
	visPoints                     =50         # from enum VisUnitCodes
	visRadians                    =83         # from enum VisUnitCodes
	visSec                        =85         # from enum VisUnitCodes
	visTypeUnits                  =48         # from enum VisUnitCodes
	visUnitsColor                 =251        # from enum VisUnitCodes
	visUnitsGUID                  =95         # from enum VisUnitCodes
	visUnitsInval                 =255        # from enum VisUnitCodes
	visUnitsNURBS                 =138        # from enum VisUnitCodes
	visUnitsPoint                 =225        # from enum VisUnitCodes
	visUnitsPolyline              =139        # from enum VisUnitCodes
	visUnitsString                =231        # from enum VisUnitCodes
	visYards                      =75         # from enum VisUnitCodes
	visValidationDefault          =0          # from enum VisValidationFlags
	visValidationNoOpenWindow     =1          # from enum VisValidationFlags
	visVertAlignBottom            =3          # from enum VisVerticalAlignTypes
	visVertAlignMiddle            =2          # from enum VisVerticalAlignTypes
	visVertAlignNone              =0          # from enum VisVerticalAlignTypes
	visVertAlignTop               =1          # from enum VisVerticalAlignTypes
	visAnchorBarAddon             =10         # from enum VisWinTypes
	visAnchorBarBuiltIn           =6          # from enum VisWinTypes
	visApplication                =5          # from enum VisWinTypes
	visDockedStencilAddon         =11         # from enum VisWinTypes
	visDockedStencilBuiltIn       =7          # from enum VisWinTypes
	visDrawing                    =1          # from enum VisWinTypes
	visDrawingAddon               =8          # from enum VisWinTypes
	visIcon                       =4          # from enum VisWinTypes
	visInvalWinID                 =-1         # from enum VisWinTypes
	visMasterGroupWin             =96         # from enum VisWinTypes
	visMasterWin                  =64         # from enum VisWinTypes
	visPageGroupWin               =160        # from enum VisWinTypes
	visPageWin                    =128        # from enum VisWinTypes
	visSheet                      =3          # from enum VisWinTypes
	visStencil                    =2          # from enum VisWinTypes
	visStencilAddon               =9          # from enum VisWinTypes
	visWinIDCustProp              =1658       # from enum VisWinTypes
	visWinIDDrawingExplorer       =1721       # from enum VisWinTypes
	visWinIDExternalData          =2044       # from enum VisWinTypes
	visWinIDFormulaTracing        =1781       # from enum VisWinTypes
	visWinIDMasterExplorer        =1916       # from enum VisWinTypes
	visWinIDPanZoom               =1653       # from enum VisWinTypes
	visWinIDShapeSearch           =1669       # from enum VisWinTypes
	visWinIDSizePos               =1670       # from enum VisWinTypes
	visWinIDStencilExplorer       =1796       # from enum VisWinTypes
	visWinIDValidationIssues      =2263       # from enum VisWinTypes
	visWinOther                   =0          # from enum VisWinTypes
	visArrangeCascade             =3          # from enum VisWindowArrange
	visArrangeTileHorizontal      =2          # from enum VisWindowArrange
	visArrangeTileVertical        =1          # from enum VisWindowArrange
	visFitNone                    =0          # from enum VisWindowFit
	visFitPage                    =1          # from enum VisWindowFit
	visFitWidth                   =2          # from enum VisWindowFit
	visScrollLeft                 =0          # from enum VisWindowScrollX
	visScrollLeftPage             =2          # from enum VisWindowScrollX
	visScrollNoneX                =9          # from enum VisWindowScrollX
	visScrollRight                =1          # from enum VisWindowScrollX
	visScrollRightPage            =3          # from enum VisWindowScrollX
	visScrollToLeft               =6          # from enum VisWindowScrollX
	visScrollToRight              =7          # from enum VisWindowScrollX
	visScrollDown                 =1          # from enum VisWindowScrollY
	visScrollDownPage             =3          # from enum VisWindowScrollY
	visScrollNoneY                =9          # from enum VisWindowScrollY
	visScrollToBottom             =7          # from enum VisWindowScrollY
	visScrollToTop                =6          # from enum VisWindowScrollY
	visScrollUp                   =0          # from enum VisWindowScrollY
	visScrollUpPage               =2          # from enum VisWindowScrollY
	visWSActive                   =67108864   # from enum VisWindowStates
	visWSAnchorAutoHide           =512        # from enum VisWindowStates
	visWSAnchorBottom             =256        # from enum VisWindowStates
	visWSAnchorLeft               =32         # from enum VisWindowStates
	visWSAnchorMerged             =1024       # from enum VisWindowStates
	visWSAnchorRight              =128        # from enum VisWindowStates
	visWSAnchorTop                =64         # from enum VisWindowStates
	visWSDockedBottom             =8          # from enum VisWindowStates
	visWSDockedLeft               =1          # from enum VisWindowStates
	visWSDockedRight              =4          # from enum VisWindowStates
	visWSDockedTop                =2          # from enum VisWindowStates
	visWSFloating                 =16         # from enum VisWindowStates
	visWSMaximized                =1073741824 # from enum VisWindowStates
	visWSMinimized                =536870912  # from enum VisWindowStates
	visWSNone                     =0          # from enum VisWindowStates
	visWSRestored                 =268435456  # from enum VisWindowStates
	visWSVisible                  =134217728  # from enum VisWindowStates
	visZoomInPlaceContainer       =1          # from enum VisZoomBehavior
	visZoomNone                   =0          # from enum VisZoomBehavior
	visZoomVisio                  =2          # from enum VisZoomBehavior
	visZoomVisioExact             =4          # from enum VisZoomBehavior

RecordMap = {
}

CLSIDToClassMap = {}
CLSIDToPackageMap = {
	'{000D0700-0000-0000-C000-000000000046}' : 'IVApplication',
	'{000D0705-0000-0000-C000-000000000046}' : 'IVDocument',
	'{000D0708-0000-0000-C000-000000000046}' : 'IVMasters',
	'{000D0707-0000-0000-C000-000000000046}' : 'IVMaster',
	'{000D070D-0000-0000-C000-000000000046}' : 'IVShapes',
	'{000D070C-0000-0000-C000-000000000046}' : 'IVShape',
	'{000D0701-0000-0000-C000-000000000046}' : 'IVCell',
	'{000D070E-0000-0000-C000-000000000046}' : 'IVStyle',
	'{000D071B-0000-0000-C000-000000000046}' : 'IVEventList',
	'{000D071A-0000-0000-C000-000000000046}' : 'IVEvent',
	'{000D0724-0000-0000-C000-000000000046}' : 'IVSection',
	'{000D0725-0000-0000-C000-000000000046}' : 'IVRow',
	'{000D0702-0000-0000-C000-000000000046}' : 'IVCharacters',
	'{000D0704-0000-0000-C000-000000000046}' : 'IVConnects',
	'{000D0703-0000-0000-C000-000000000046}' : 'IVConnect',
	'{000D0709-0000-0000-C000-000000000046}' : 'IVPage',
	'{000D0713-0000-0000-C000-000000000046}' : 'IVLayers',
	'{000D0712-0000-0000-C000-000000000046}' : 'IVLayer',
	'{000D0710-0000-0000-C000-000000000046}' : 'IVWindow',
	'{000D070B-0000-0000-C000-000000000046}' : 'IVSelection',
	'{000D0711-0000-0000-C000-000000000046}' : 'IVWindows',
	'{000D0727-0000-0000-C000-000000000046}' : 'IVMasterShortcut',
	'{000D072F-0000-0000-C000-000000000046}' : 'IVDataRecordset',
	'{000D0730-0000-0000-C000-000000000046}' : 'IVDataConnection',
	'{000D0731-0000-0000-C000-000000000046}' : 'IVDataColumns',
	'{000D0732-0000-0000-C000-000000000046}' : 'IVDataColumn',
	'{000D0740-0000-0000-C000-000000000046}' : 'IVValidationIssue',
	'{000D073E-0000-0000-C000-000000000046}' : 'IVValidationRule',
	'{000D073C-0000-0000-C000-000000000046}' : 'IVValidationRuleSet',
	'{000D073D-0000-0000-C000-000000000046}' : 'IVValidationRules',
	'{000D071E-0000-0000-C000-000000000046}' : 'IVOLEObjects',
	'{000D071F-0000-0000-C000-000000000046}' : 'IVOLEObject',
	'{000D0743-0000-0000-C000-000000000046}' : 'IVComments',
	'{000D0744-0000-0000-C000-000000000046}' : 'IVComment',
	'{000D074A-0000-0000-C000-000000000046}' : 'IVDataVisualizerSettings',
	'{000D0746-0000-0000-C000-000000000046}' : 'IVShapeBindingSettings',
	'{000D0745-0000-0000-C000-000000000046}' : 'IVMasterMapSettings',
	'{000D0747-0000-0000-C000-000000000046}' : 'IVConnectorBindingSettings',
	'{000D0748-0000-0000-C000-000000000046}' : 'IVCrossFunctionalFlowchartBindingSettings',
	'{000D0749-0000-0000-C000-000000000046}' : 'IVLayoutSettings',
	'{000D071D-0000-0000-C000-000000000046}' : 'IVHyperlink',
	'{000D0720-0000-0000-C000-000000000046}' : 'IVPaths',
	'{000D0721-0000-0000-C000-000000000046}' : 'IVPath',
	'{000D0722-0000-0000-C000-000000000046}' : 'IVCurve',
	'{000D0723-0000-0000-C000-000000000046}' : 'IVHyperlinks',
	'{000D0736-0000-0000-C000-000000000046}' : 'IVContainerProperties',
	'{000D0734-0000-0000-C000-000000000046}' : 'IVGraphicItems',
	'{000D0735-0000-0000-C000-000000000046}' : 'IVGraphicItem',
	'{000D070A-0000-0000-C000-000000000046}' : 'IVPages',
	'{000D070F-0000-0000-C000-000000000046}' : 'IVStyles',
	'{000D0202-0000-0000-C000-000000000046}' : 'IVUIObject',
	'{000D0236-0000-0000-C000-000000000046}' : 'IVMenuSets',
	'{000D0232-0000-0000-C000-000000000046}' : 'IVMenuSet',
	'{000D0225-0000-0000-C000-000000000046}' : 'IVMenus',
	'{000D0222-0000-0000-C000-000000000046}' : 'IVMenu',
	'{000D0216-0000-0000-C000-000000000046}' : 'IVMenuItems',
	'{000D0212-0000-0000-C000-000000000046}' : 'IVMenuItem',
	'{000D0266-0000-0000-C000-000000000046}' : 'IVToolbarSets',
	'{000D0262-0000-0000-C000-000000000046}' : 'IVToolbarSet',
	'{000D0255-0000-0000-C000-000000000046}' : 'IVToolbars',
	'{000D0252-0000-0000-C000-000000000046}' : 'IVToolbar',
	'{000D0245-0000-0000-C000-000000000046}' : 'IVToolbarItems',
	'{000D0242-0000-0000-C000-000000000046}' : 'IVToolbarItem',
	'{000D0285-0000-0000-C000-000000000046}' : 'IVStatusBars',
	'{000D0282-0000-0000-C000-000000000046}' : 'IVStatusBar',
	'{000D0275-0000-0000-C000-000000000046}' : 'IVStatusBarItems',
	'{000D0272-0000-0000-C000-000000000046}' : 'IVStatusBarItem',
	'{000D02A5-0000-0000-C000-000000000046}' : 'IVAccelTables',
	'{000D02A2-0000-0000-C000-000000000046}' : 'IVAccelTable',
	'{000D0295-0000-0000-C000-000000000046}' : 'IVAccelItems',
	'{000D0292-0000-0000-C000-000000000046}' : 'IVAccelItem',
	'{000D0715-0000-0000-C000-000000000046}' : 'IVFonts',
	'{000D0714-0000-0000-C000-000000000046}' : 'IVFont',
	'{000D0717-0000-0000-C000-000000000046}' : 'IVColors',
	'{000D0716-0000-0000-C000-000000000046}' : 'IVColor',
	'{000D0726-0000-0000-C000-000000000046}' : 'IVMasterShortcuts',
	'{000D072E-0000-0000-C000-000000000046}' : 'IVDataRecordsets',
	'{000D0739-0000-0000-C000-000000000046}' : 'IVServerPublishOptions',
	'{000D073A-0000-0000-C000-000000000046}' : 'IVValidation',
	'{000D073B-0000-0000-C000-000000000046}' : 'IVValidationRuleSets',
	'{000D073F-0000-0000-C000-000000000046}' : 'IVValidationIssues',
	'{000D0706-0000-0000-C000-000000000046}' : 'IVDocuments',
	'{000D0719-0000-0000-C000-000000000046}' : 'IVAddons',
	'{000D0718-0000-0000-C000-000000000046}' : 'IVAddon',
	'{000D072D-0000-0000-C000-000000000046}' : 'IVApplicationSettings',
	'{000D0729-0000-0000-C000-000000000046}' : 'IVMSGWrap',
	'{000D072A-0000-0000-C000-000000000046}' : 'IVMouseEvent',
	'{000D072B-0000-0000-C000-000000000046}' : 'IVKeyboardEvent',
	'{000D072C-0000-0000-C000-000000000046}' : 'IVInvisibleApp',
	'{000D0733-0000-0000-C000-000000000046}' : 'IVDataRecordsetChangedEvent',
	'{000D0737-0000-0000-C000-000000000046}' : 'IVRelatedShapePairEvent',
	'{000D0738-0000-0000-C000-000000000046}' : 'IVMovedSelectionEvent',
	'{000D0741-0000-0000-C000-000000000046}' : 'IVReplaceShapesEvent',
	'{000D0742-0000-0000-C000-000000000046}' : 'IVCoauthMergeEvent',
	'{000D074B-0000-0000-C000-000000000046}' : 'IVDataVisualizerProperties',
	'{000D071C-0000-0000-C000-000000000046}' : 'IVGlobal',
	'{000D0750-0000-0000-C000-000000000046}' : 'EDocument',
	'{000D0B00-0000-0000-C000-000000000046}' : 'EApplication',
	'{000D0B01-0000-0000-C000-000000000046}' : 'EWindows',
	'{000D0B02-0000-0000-C000-000000000046}' : 'EWindow',
	'{000D0B03-0000-0000-C000-000000000046}' : 'EDocuments',
	'{000D0B05-0000-0000-C000-000000000046}' : 'EStyles',
	'{000D0B06-0000-0000-C000-000000000046}' : 'EStyle',
	'{000D0B07-0000-0000-C000-000000000046}' : 'EMasters',
	'{000D0B08-0000-0000-C000-000000000046}' : 'EMaster',
	'{000D0B09-0000-0000-C000-000000000046}' : 'EPages',
	'{000D0B0A-0000-0000-C000-000000000046}' : 'EPage',
	'{000D0B0B-0000-0000-C000-000000000046}' : 'EShape',
	'{000D0B0C-0000-0000-C000-000000000046}' : 'ECharacters',
	'{000D0B0D-0000-0000-C000-000000000046}' : 'ECell',
	'{00021A20-0000-0000-C000-000000000046}' : 'Application',
	'{00021A21-0000-0000-C000-000000000046}' : 'Document',
	'{000D0A00-0000-0000-C000-000000000046}' : 'Documents',
	'{000D0A01-0000-0000-C000-000000000046}' : 'Styles',
	'{000D0A02-0000-0000-C000-000000000046}' : 'Style',
	'{000D0A03-0000-0000-C000-000000000046}' : 'Masters',
	'{000D0A04-0000-0000-C000-000000000046}' : 'Master',
	'{000D0A05-0000-0000-C000-000000000046}' : 'Pages',
	'{000D0A06-0000-0000-C000-000000000046}' : 'Page',
	'{000D0A07-0000-0000-C000-000000000046}' : 'Layers',
	'{000D0A08-0000-0000-C000-000000000046}' : 'Layer',
	'{000D0A09-0000-0000-C000-000000000046}' : 'Shapes',
	'{000D0A0A-0000-0000-C000-000000000046}' : 'Shape',
	'{000D0A0B-0000-0000-C000-000000000046}' : 'Windows',
	'{000D0A0C-0000-0000-C000-000000000046}' : 'Window',
	'{000D0A0D-0000-0000-C000-000000000046}' : 'Cell',
	'{000D0A0E-0000-0000-C000-000000000046}' : 'Selection',
	'{000D0A0F-0000-0000-C000-000000000046}' : 'Font',
	'{000D0A10-0000-0000-C000-000000000046}' : 'Fonts',
	'{000D0A11-0000-0000-C000-000000000046}' : 'Color',
	'{000D0A12-0000-0000-C000-000000000046}' : 'Colors',
	'{000D0A13-0000-0000-C000-000000000046}' : 'Addon',
	'{000D0A14-0000-0000-C000-000000000046}' : 'Addons',
	'{000D0A15-0000-0000-C000-000000000046}' : 'Event',
	'{000D0A16-0000-0000-C000-000000000046}' : 'EventList',
	'{000D0A17-0000-0000-C000-000000000046}' : 'Characters',
	'{000D0A18-0000-0000-C000-000000000046}' : 'Connect',
	'{000D0A19-0000-0000-C000-000000000046}' : 'Connects',
	'{000D0A1A-0000-0000-C000-000000000046}' : 'Global',
	'{000D0201-0000-0000-C000-000000000046}' : 'UIObject',
	'{000D0210-0000-0000-C000-000000000046}' : 'MenuItem',
	'{000D0215-0000-0000-C000-000000000046}' : 'MenuItems',
	'{000D0220-0000-0000-C000-000000000046}' : 'Menu',
	'{000D0224-0000-0000-C000-000000000046}' : 'Menus',
	'{000D0230-0000-0000-C000-000000000046}' : 'MenuSet',
	'{000D0235-0000-0000-C000-000000000046}' : 'MenuSets',
	'{000D0240-0000-0000-C000-000000000046}' : 'ToolbarItem',
	'{000D0244-0000-0000-C000-000000000046}' : 'ToolbarItems',
	'{000D0250-0000-0000-C000-000000000046}' : 'Toolbar',
	'{000D0254-0000-0000-C000-000000000046}' : 'Toolbars',
	'{000D0260-0000-0000-C000-000000000046}' : 'ToolbarSet',
	'{000D0265-0000-0000-C000-000000000046}' : 'ToolbarSets',
	'{000D0270-0000-0000-C000-000000000046}' : 'StatusBarItem',
	'{000D0274-0000-0000-C000-000000000046}' : 'StatusBarItems',
	'{000D0280-0000-0000-C000-000000000046}' : 'StatusBar',
	'{000D0284-0000-0000-C000-000000000046}' : 'StatusBars',
	'{000D0290-0000-0000-C000-000000000046}' : 'AccelItem',
	'{000D0294-0000-0000-C000-000000000046}' : 'AccelItems',
	'{000D02A0-0000-0000-C000-000000000046}' : 'AccelTable',
	'{000D02A4-0000-0000-C000-000000000046}' : 'AccelTables',
	'{000D0D0E-0000-0000-C000-000000000046}' : 'IVExtender',
	'{000D0D0F-0000-0000-C000-000000000046}' : 'IVDispExtender',
	'{000D0D10-0000-0000-C000-000000000046}' : 'IVAmbients',
	'{000D0D06-0000-0000-C000-000000000046}' : 'Extender',
	'{000D0A1B-0000-0000-C000-000000000046}' : 'Hyperlink',
	'{000D0A1C-0000-0000-C000-000000000046}' : 'OLEObjects',
	'{000D0A1D-0000-0000-C000-000000000046}' : 'OLEObject',
	'{000D0A1E-0000-0000-C000-000000000046}' : 'Paths',
	'{000D0A1F-0000-0000-C000-000000000046}' : 'Path',
	'{000D0A20-0000-0000-C000-000000000046}' : 'Curve',
	'{000D1306-0000-0000-C000-000000000046}' : 'IVBUndoManager',
	'{000D1305-0000-0000-C000-000000000046}' : 'IVBUndoUnit',
	'{000D0728-0000-0000-C000-000000000046}' : 'IVisEventProc',
	'{000D0B0E-0000-0000-C000-000000000046}' : 'ESection',
	'{000D0B0F-0000-0000-C000-000000000046}' : 'ERow',
	'{000D0A21-0000-0000-C000-000000000046}' : 'Hyperlinks',
	'{000D0A22-0000-0000-C000-000000000046}' : 'Section',
	'{000D0A23-0000-0000-C000-000000000046}' : 'Row',
	'{000D0A24-0000-0000-C000-000000000046}' : 'MasterShortcuts',
	'{000D0A25-0000-0000-C000-000000000046}' : 'MasterShortcut',
	'{000D0A26-0000-0000-C000-000000000046}' : 'InvisibleApp',
	'{000D0A27-0000-0000-C000-000000000046}' : 'MSGWrap',
	'{000D0A28-0000-0000-C000-000000000046}' : 'MouseEvent',
	'{000D0A29-0000-0000-C000-000000000046}' : 'KeyboardEvent',
	'{000D0A2A-0000-0000-C000-000000000046}' : 'ApplicationSettings',
	'{000D0B11-0000-0000-C000-000000000046}' : 'EDataRecordset',
	'{000D0B10-0000-0000-C000-000000000046}' : 'EDataRecordsets',
	'{000D0A2B-0000-0000-C000-000000000046}' : 'DataRecordsets',
	'{000D0A2C-0000-0000-C000-000000000046}' : 'DataRecordset',
	'{000D0A2D-0000-0000-C000-000000000046}' : 'DataConnection',
	'{000D0A2E-0000-0000-C000-000000000046}' : 'DataColumns',
	'{000D0A2F-0000-0000-C000-000000000046}' : 'DataColumn',
	'{000D0A30-0000-0000-C000-000000000046}' : 'DataRecordsetChangedEvent',
	'{000D0A31-0000-0000-C000-000000000046}' : 'GraphicItems',
	'{000D0A32-0000-0000-C000-000000000046}' : 'GraphicItem',
	'{000D0A33-0000-0000-C000-000000000046}' : 'ContainerProperties',
	'{000D0A34-0000-0000-C000-000000000046}' : 'RelatedShapePairEvent',
	'{000D0A35-0000-0000-C000-000000000046}' : 'MovedSelectionEvent',
	'{000D0A36-0000-0000-C000-000000000046}' : 'ServerPublishOptions',
	'{000D0A37-0000-0000-C000-000000000046}' : 'Validation',
	'{000D0A38-0000-0000-C000-000000000046}' : 'ValidationRuleSets',
	'{000D0A39-0000-0000-C000-000000000046}' : 'ValidationRuleSet',
	'{000D0A3A-0000-0000-C000-000000000046}' : 'ValidationRules',
	'{000D0A3B-0000-0000-C000-000000000046}' : 'ValidationRule',
	'{000D0A3C-0000-0000-C000-000000000046}' : 'ValidationIssues',
	'{000D0A3D-0000-0000-C000-000000000046}' : 'ValidationIssue',
	'{000D0A3E-0000-0000-C000-000000000046}' : 'ReplaceShapesEvent',
	'{000D0A3F-0000-0000-C000-000000000046}' : 'CoauthMergeEvent',
	'{000D0A40-0000-0000-C000-000000000046}' : 'Comments',
	'{000D0A41-0000-0000-C000-000000000046}' : 'Comment',
	'{000D0A42-0000-0000-C000-000000000046}' : 'MasterMapSettings',
	'{000D0A43-0000-0000-C000-000000000046}' : 'ShapeBindingSettings',
	'{000D0A44-0000-0000-C000-000000000046}' : 'ConnectorBindingSettings',
	'{000D0A45-0000-0000-C000-000000000046}' : 'CrossFunctionalFlowchartBindingSettings',
	'{000D0A46-0000-0000-C000-000000000046}' : 'LayoutSettings',
	'{000D0A47-0000-0000-C000-000000000046}' : 'DataVisualizerSettings',
	'{000D0A48-0000-0000-C000-000000000046}' : 'DataVisualizerProperties',
}
VTablesToClassMap = {}
VTablesToPackageMap = {
	'{000D0700-0000-0000-C000-000000000046}' : 'IVApplication',
	'{000D0705-0000-0000-C000-000000000046}' : 'IVDocument',
	'{000D0708-0000-0000-C000-000000000046}' : 'IVMasters',
	'{000D0707-0000-0000-C000-000000000046}' : 'IVMaster',
	'{000D070D-0000-0000-C000-000000000046}' : 'IVShapes',
	'{000D070C-0000-0000-C000-000000000046}' : 'IVShape',
	'{000D0701-0000-0000-C000-000000000046}' : 'IVCell',
	'{000D070E-0000-0000-C000-000000000046}' : 'IVStyle',
	'{000D071B-0000-0000-C000-000000000046}' : 'IVEventList',
	'{000D071A-0000-0000-C000-000000000046}' : 'IVEvent',
	'{000D0724-0000-0000-C000-000000000046}' : 'IVSection',
	'{000D0725-0000-0000-C000-000000000046}' : 'IVRow',
	'{000D0702-0000-0000-C000-000000000046}' : 'IVCharacters',
	'{000D0704-0000-0000-C000-000000000046}' : 'IVConnects',
	'{000D0703-0000-0000-C000-000000000046}' : 'IVConnect',
	'{000D0709-0000-0000-C000-000000000046}' : 'IVPage',
	'{000D0713-0000-0000-C000-000000000046}' : 'IVLayers',
	'{000D0712-0000-0000-C000-000000000046}' : 'IVLayer',
	'{000D0710-0000-0000-C000-000000000046}' : 'IVWindow',
	'{000D070B-0000-0000-C000-000000000046}' : 'IVSelection',
	'{000D0711-0000-0000-C000-000000000046}' : 'IVWindows',
	'{000D0727-0000-0000-C000-000000000046}' : 'IVMasterShortcut',
	'{000D072F-0000-0000-C000-000000000046}' : 'IVDataRecordset',
	'{000D0730-0000-0000-C000-000000000046}' : 'IVDataConnection',
	'{000D0731-0000-0000-C000-000000000046}' : 'IVDataColumns',
	'{000D0732-0000-0000-C000-000000000046}' : 'IVDataColumn',
	'{000D0740-0000-0000-C000-000000000046}' : 'IVValidationIssue',
	'{000D073E-0000-0000-C000-000000000046}' : 'IVValidationRule',
	'{000D073C-0000-0000-C000-000000000046}' : 'IVValidationRuleSet',
	'{000D073D-0000-0000-C000-000000000046}' : 'IVValidationRules',
	'{000D071E-0000-0000-C000-000000000046}' : 'IVOLEObjects',
	'{000D071F-0000-0000-C000-000000000046}' : 'IVOLEObject',
	'{000D0743-0000-0000-C000-000000000046}' : 'IVComments',
	'{000D0744-0000-0000-C000-000000000046}' : 'IVComment',
	'{000D074A-0000-0000-C000-000000000046}' : 'IVDataVisualizerSettings',
	'{000D0746-0000-0000-C000-000000000046}' : 'IVShapeBindingSettings',
	'{000D0745-0000-0000-C000-000000000046}' : 'IVMasterMapSettings',
	'{000D0747-0000-0000-C000-000000000046}' : 'IVConnectorBindingSettings',
	'{000D0748-0000-0000-C000-000000000046}' : 'IVCrossFunctionalFlowchartBindingSettings',
	'{000D0749-0000-0000-C000-000000000046}' : 'IVLayoutSettings',
	'{000D071D-0000-0000-C000-000000000046}' : 'IVHyperlink',
	'{000D0720-0000-0000-C000-000000000046}' : 'IVPaths',
	'{000D0721-0000-0000-C000-000000000046}' : 'IVPath',
	'{000D0722-0000-0000-C000-000000000046}' : 'IVCurve',
	'{000D0723-0000-0000-C000-000000000046}' : 'IVHyperlinks',
	'{000D0736-0000-0000-C000-000000000046}' : 'IVContainerProperties',
	'{000D0734-0000-0000-C000-000000000046}' : 'IVGraphicItems',
	'{000D0735-0000-0000-C000-000000000046}' : 'IVGraphicItem',
	'{000D070A-0000-0000-C000-000000000046}' : 'IVPages',
	'{000D070F-0000-0000-C000-000000000046}' : 'IVStyles',
	'{000D0202-0000-0000-C000-000000000046}' : 'IVUIObject',
	'{000D0236-0000-0000-C000-000000000046}' : 'IVMenuSets',
	'{000D0232-0000-0000-C000-000000000046}' : 'IVMenuSet',
	'{000D0225-0000-0000-C000-000000000046}' : 'IVMenus',
	'{000D0222-0000-0000-C000-000000000046}' : 'IVMenu',
	'{000D0216-0000-0000-C000-000000000046}' : 'IVMenuItems',
	'{000D0212-0000-0000-C000-000000000046}' : 'IVMenuItem',
	'{000D0266-0000-0000-C000-000000000046}' : 'IVToolbarSets',
	'{000D0262-0000-0000-C000-000000000046}' : 'IVToolbarSet',
	'{000D0255-0000-0000-C000-000000000046}' : 'IVToolbars',
	'{000D0252-0000-0000-C000-000000000046}' : 'IVToolbar',
	'{000D0245-0000-0000-C000-000000000046}' : 'IVToolbarItems',
	'{000D0242-0000-0000-C000-000000000046}' : 'IVToolbarItem',
	'{000D0285-0000-0000-C000-000000000046}' : 'IVStatusBars',
	'{000D0282-0000-0000-C000-000000000046}' : 'IVStatusBar',
	'{000D0275-0000-0000-C000-000000000046}' : 'IVStatusBarItems',
	'{000D0272-0000-0000-C000-000000000046}' : 'IVStatusBarItem',
	'{000D02A5-0000-0000-C000-000000000046}' : 'IVAccelTables',
	'{000D02A2-0000-0000-C000-000000000046}' : 'IVAccelTable',
	'{000D0295-0000-0000-C000-000000000046}' : 'IVAccelItems',
	'{000D0292-0000-0000-C000-000000000046}' : 'IVAccelItem',
	'{000D0715-0000-0000-C000-000000000046}' : 'IVFonts',
	'{000D0714-0000-0000-C000-000000000046}' : 'IVFont',
	'{000D0717-0000-0000-C000-000000000046}' : 'IVColors',
	'{000D0716-0000-0000-C000-000000000046}' : 'IVColor',
	'{000D0726-0000-0000-C000-000000000046}' : 'IVMasterShortcuts',
	'{000D072E-0000-0000-C000-000000000046}' : 'IVDataRecordsets',
	'{000D0739-0000-0000-C000-000000000046}' : 'IVServerPublishOptions',
	'{000D073A-0000-0000-C000-000000000046}' : 'IVValidation',
	'{000D073B-0000-0000-C000-000000000046}' : 'IVValidationRuleSets',
	'{000D073F-0000-0000-C000-000000000046}' : 'IVValidationIssues',
	'{000D0706-0000-0000-C000-000000000046}' : 'IVDocuments',
	'{000D0719-0000-0000-C000-000000000046}' : 'IVAddons',
	'{000D0718-0000-0000-C000-000000000046}' : 'IVAddon',
	'{000D072D-0000-0000-C000-000000000046}' : 'IVApplicationSettings',
	'{000D0213-0000-0000-C000-000000000046}' : 'IEnumVMenuItem',
	'{000D0223-0000-0000-C000-000000000046}' : 'IEnumVMenu',
	'{000D0233-0000-0000-C000-000000000046}' : 'IEnumVMenuSet',
	'{000D0243-0000-0000-C000-000000000046}' : 'IEnumVToolbarItem',
	'{000D0253-0000-0000-C000-000000000046}' : 'IEnumVToolbar',
	'{000D0263-0000-0000-C000-000000000046}' : 'IEnumVToolbarSet',
	'{000D0273-0000-0000-C000-000000000046}' : 'IEnumVStatusBarItem',
	'{000D0283-0000-0000-C000-000000000046}' : 'IEnumVStatusBar',
	'{000D0293-0000-0000-C000-000000000046}' : 'IEnumVAccelItem',
	'{000D02A3-0000-0000-C000-000000000046}' : 'IEnumVAccelTable',
	'{000D0729-0000-0000-C000-000000000046}' : 'IVMSGWrap',
	'{000D0733-0000-0000-C000-000000000046}' : 'IVDataRecordsetChangedEvent',
	'{000D0737-0000-0000-C000-000000000046}' : 'IVRelatedShapePairEvent',
	'{000D0738-0000-0000-C000-000000000046}' : 'IVMovedSelectionEvent',
	'{000D0741-0000-0000-C000-000000000046}' : 'IVReplaceShapesEvent',
	'{000D0742-0000-0000-C000-000000000046}' : 'IVCoauthMergeEvent',
	'{000D074B-0000-0000-C000-000000000046}' : 'IVDataVisualizerProperties',
	'{000D071C-0000-0000-C000-000000000046}' : 'IVGlobal',
	'{000D0D0E-0000-0000-C000-000000000046}' : 'IVExtender',
	'{000D0D10-0000-0000-C000-000000000046}' : 'IVAmbients',
	'{000D0D11-0000-0000-C000-000000000046}' : 'IVClientSite',
	'{000D1306-0000-0000-C000-000000000046}' : 'IVBUndoManager',
	'{000D1305-0000-0000-C000-000000000046}' : 'IVBUndoUnit',
	'{000D0728-0000-0000-C000-000000000046}' : 'IVisEventProc',
	'{000D0D21-0000-0000-C000-000000000046}' : 'IVisLibOcxSupport',
}


NamesToIIDMap = {
	'IVApplication' : '{000D0700-0000-0000-C000-000000000046}',
	'IVDocument' : '{000D0705-0000-0000-C000-000000000046}',
	'IVMasters' : '{000D0708-0000-0000-C000-000000000046}',
	'IVMaster' : '{000D0707-0000-0000-C000-000000000046}',
	'IVShapes' : '{000D070D-0000-0000-C000-000000000046}',
	'IVShape' : '{000D070C-0000-0000-C000-000000000046}',
	'IVCell' : '{000D0701-0000-0000-C000-000000000046}',
	'IVStyle' : '{000D070E-0000-0000-C000-000000000046}',
	'IVEventList' : '{000D071B-0000-0000-C000-000000000046}',
	'IVEvent' : '{000D071A-0000-0000-C000-000000000046}',
	'IVSection' : '{000D0724-0000-0000-C000-000000000046}',
	'IVRow' : '{000D0725-0000-0000-C000-000000000046}',
	'IVCharacters' : '{000D0702-0000-0000-C000-000000000046}',
	'IVConnects' : '{000D0704-0000-0000-C000-000000000046}',
	'IVConnect' : '{000D0703-0000-0000-C000-000000000046}',
	'IVPage' : '{000D0709-0000-0000-C000-000000000046}',
	'IVLayers' : '{000D0713-0000-0000-C000-000000000046}',
	'IVLayer' : '{000D0712-0000-0000-C000-000000000046}',
	'IVWindow' : '{000D0710-0000-0000-C000-000000000046}',
	'IVSelection' : '{000D070B-0000-0000-C000-000000000046}',
	'IVWindows' : '{000D0711-0000-0000-C000-000000000046}',
	'IVMasterShortcut' : '{000D0727-0000-0000-C000-000000000046}',
	'IVDataRecordset' : '{000D072F-0000-0000-C000-000000000046}',
	'IVDataConnection' : '{000D0730-0000-0000-C000-000000000046}',
	'IVDataColumns' : '{000D0731-0000-0000-C000-000000000046}',
	'IVDataColumn' : '{000D0732-0000-0000-C000-000000000046}',
	'IVValidationIssue' : '{000D0740-0000-0000-C000-000000000046}',
	'IVValidationRule' : '{000D073E-0000-0000-C000-000000000046}',
	'IVValidationRuleSet' : '{000D073C-0000-0000-C000-000000000046}',
	'IVValidationRules' : '{000D073D-0000-0000-C000-000000000046}',
	'IVOLEObjects' : '{000D071E-0000-0000-C000-000000000046}',
	'IVOLEObject' : '{000D071F-0000-0000-C000-000000000046}',
	'IVComments' : '{000D0743-0000-0000-C000-000000000046}',
	'IVComment' : '{000D0744-0000-0000-C000-000000000046}',
	'IVDataVisualizerSettings' : '{000D074A-0000-0000-C000-000000000046}',
	'IVShapeBindingSettings' : '{000D0746-0000-0000-C000-000000000046}',
	'IVMasterMapSettings' : '{000D0745-0000-0000-C000-000000000046}',
	'IVConnectorBindingSettings' : '{000D0747-0000-0000-C000-000000000046}',
	'IVCrossFunctionalFlowchartBindingSettings' : '{000D0748-0000-0000-C000-000000000046}',
	'IVLayoutSettings' : '{000D0749-0000-0000-C000-000000000046}',
	'IVHyperlink' : '{000D071D-0000-0000-C000-000000000046}',
	'IVPaths' : '{000D0720-0000-0000-C000-000000000046}',
	'IVPath' : '{000D0721-0000-0000-C000-000000000046}',
	'IVCurve' : '{000D0722-0000-0000-C000-000000000046}',
	'IVHyperlinks' : '{000D0723-0000-0000-C000-000000000046}',
	'IVContainerProperties' : '{000D0736-0000-0000-C000-000000000046}',
	'IVGraphicItems' : '{000D0734-0000-0000-C000-000000000046}',
	'IVGraphicItem' : '{000D0735-0000-0000-C000-000000000046}',
	'IVPages' : '{000D070A-0000-0000-C000-000000000046}',
	'IVStyles' : '{000D070F-0000-0000-C000-000000000046}',
	'IVUIObject' : '{000D0202-0000-0000-C000-000000000046}',
	'IVMenuSets' : '{000D0236-0000-0000-C000-000000000046}',
	'IVMenuSet' : '{000D0232-0000-0000-C000-000000000046}',
	'IVMenus' : '{000D0225-0000-0000-C000-000000000046}',
	'IVMenu' : '{000D0222-0000-0000-C000-000000000046}',
	'IVMenuItems' : '{000D0216-0000-0000-C000-000000000046}',
	'IVMenuItem' : '{000D0212-0000-0000-C000-000000000046}',
	'IVToolbarSets' : '{000D0266-0000-0000-C000-000000000046}',
	'IVToolbarSet' : '{000D0262-0000-0000-C000-000000000046}',
	'IVToolbars' : '{000D0255-0000-0000-C000-000000000046}',
	'IVToolbar' : '{000D0252-0000-0000-C000-000000000046}',
	'IVToolbarItems' : '{000D0245-0000-0000-C000-000000000046}',
	'IVToolbarItem' : '{000D0242-0000-0000-C000-000000000046}',
	'IVStatusBars' : '{000D0285-0000-0000-C000-000000000046}',
	'IVStatusBar' : '{000D0282-0000-0000-C000-000000000046}',
	'IVStatusBarItems' : '{000D0275-0000-0000-C000-000000000046}',
	'IVStatusBarItem' : '{000D0272-0000-0000-C000-000000000046}',
	'IVAccelTables' : '{000D02A5-0000-0000-C000-000000000046}',
	'IVAccelTable' : '{000D02A2-0000-0000-C000-000000000046}',
	'IVAccelItems' : '{000D0295-0000-0000-C000-000000000046}',
	'IVAccelItem' : '{000D0292-0000-0000-C000-000000000046}',
	'IVFonts' : '{000D0715-0000-0000-C000-000000000046}',
	'IVFont' : '{000D0714-0000-0000-C000-000000000046}',
	'IVColors' : '{000D0717-0000-0000-C000-000000000046}',
	'IVColor' : '{000D0716-0000-0000-C000-000000000046}',
	'IVMasterShortcuts' : '{000D0726-0000-0000-C000-000000000046}',
	'IVDataRecordsets' : '{000D072E-0000-0000-C000-000000000046}',
	'IVServerPublishOptions' : '{000D0739-0000-0000-C000-000000000046}',
	'IVValidation' : '{000D073A-0000-0000-C000-000000000046}',
	'IVValidationRuleSets' : '{000D073B-0000-0000-C000-000000000046}',
	'IVValidationIssues' : '{000D073F-0000-0000-C000-000000000046}',
	'IVDocuments' : '{000D0706-0000-0000-C000-000000000046}',
	'IVAddons' : '{000D0719-0000-0000-C000-000000000046}',
	'IVAddon' : '{000D0718-0000-0000-C000-000000000046}',
	'IVApplicationSettings' : '{000D072D-0000-0000-C000-000000000046}',
	'IVMSGWrap' : '{000D0729-0000-0000-C000-000000000046}',
	'IVMouseEvent' : '{000D072A-0000-0000-C000-000000000046}',
	'IVKeyboardEvent' : '{000D072B-0000-0000-C000-000000000046}',
	'IVInvisibleApp' : '{000D072C-0000-0000-C000-000000000046}',
	'IVDataRecordsetChangedEvent' : '{000D0733-0000-0000-C000-000000000046}',
	'IVRelatedShapePairEvent' : '{000D0737-0000-0000-C000-000000000046}',
	'IVMovedSelectionEvent' : '{000D0738-0000-0000-C000-000000000046}',
	'IVReplaceShapesEvent' : '{000D0741-0000-0000-C000-000000000046}',
	'IVCoauthMergeEvent' : '{000D0742-0000-0000-C000-000000000046}',
	'IVDataVisualizerProperties' : '{000D074B-0000-0000-C000-000000000046}',
	'IVGlobal' : '{000D071C-0000-0000-C000-000000000046}',
	'EDocument' : '{000D0750-0000-0000-C000-000000000046}',
	'EApplication' : '{000D0B00-0000-0000-C000-000000000046}',
	'EWindows' : '{000D0B01-0000-0000-C000-000000000046}',
	'EWindow' : '{000D0B02-0000-0000-C000-000000000046}',
	'EDocuments' : '{000D0B03-0000-0000-C000-000000000046}',
	'EStyles' : '{000D0B05-0000-0000-C000-000000000046}',
	'EStyle' : '{000D0B06-0000-0000-C000-000000000046}',
	'EMasters' : '{000D0B07-0000-0000-C000-000000000046}',
	'EMaster' : '{000D0B08-0000-0000-C000-000000000046}',
	'EPages' : '{000D0B09-0000-0000-C000-000000000046}',
	'EPage' : '{000D0B0A-0000-0000-C000-000000000046}',
	'EShape' : '{000D0B0B-0000-0000-C000-000000000046}',
	'ECharacters' : '{000D0B0C-0000-0000-C000-000000000046}',
	'ECell' : '{000D0B0D-0000-0000-C000-000000000046}',
	'IVExtender' : '{000D0D0E-0000-0000-C000-000000000046}',
	'IVDispExtender' : '{000D0D0F-0000-0000-C000-000000000046}',
	'IVAmbients' : '{000D0D10-0000-0000-C000-000000000046}',
	'IVBUndoManager' : '{000D1306-0000-0000-C000-000000000046}',
	'IVBUndoUnit' : '{000D1305-0000-0000-C000-000000000046}',
	'IVisEventProc' : '{000D0728-0000-0000-C000-000000000046}',
	'ESection' : '{000D0B0E-0000-0000-C000-000000000046}',
	'ERow' : '{000D0B0F-0000-0000-C000-000000000046}',
	'EDataRecordset' : '{000D0B11-0000-0000-C000-000000000046}',
	'EDataRecordsets' : '{000D0B10-0000-0000-C000-000000000046}',
	'IEnumVMenuItem' : '{000D0213-0000-0000-C000-000000000046}',
	'IEnumVMenu' : '{000D0223-0000-0000-C000-000000000046}',
	'IEnumVMenuSet' : '{000D0233-0000-0000-C000-000000000046}',
	'IEnumVToolbarItem' : '{000D0243-0000-0000-C000-000000000046}',
	'IEnumVToolbar' : '{000D0253-0000-0000-C000-000000000046}',
	'IEnumVToolbarSet' : '{000D0263-0000-0000-C000-000000000046}',
	'IEnumVStatusBarItem' : '{000D0273-0000-0000-C000-000000000046}',
	'IEnumVStatusBar' : '{000D0283-0000-0000-C000-000000000046}',
	'IEnumVAccelItem' : '{000D0293-0000-0000-C000-000000000046}',
	'IEnumVAccelTable' : '{000D02A3-0000-0000-C000-000000000046}',
	'IVClientSite' : '{000D0D11-0000-0000-C000-000000000046}',
	'IVisLibOcxSupport' : '{000D0D21-0000-0000-C000-000000000046}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

