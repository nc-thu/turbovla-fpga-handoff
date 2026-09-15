"""Native Visio reconstruction of approved Figure 1; photograph is the only bitmap."""
from pathlib import Path
import math,json,datetime
import pythoncom,win32com.client,win32com
P=Path(__file__).resolve().parents[1]
O=P/'visio_figure1';O.mkdir(exist_ok=True)
cache=O/'com_cache';cache.mkdir(exist_ok=True)
win32com.__gen_path__=str(cache)
import win32com.gen_py
win32com.gen_py.__path__.append(str(cache))
win32com.client.gencache.is_readonly=False
W,H=1920,820
app=win32com.client.gencache.EnsureDispatch(win32com.client.DispatchEx('Visio.Application'));app.Visible=False;app.AlertResponse=7
doc=app.Documents.Add('');page=doc.Pages.Item(1);page.Name='Figure 1'
page.PageSheet.CellsU('PageWidth').ResultIU=W/100
page.PageSheet.CellsU('PageHeight').ResultIU=H/100
green='#d6e5c4';blue='#a9ddf3';orange='#f9d8b7';purple='#dfd8ee';dark='#171717'
def rgb(c):return 'RGB(%d,%d,%d)'%tuple(int(c[i:i+2],16) for i in (1,3,5))
def style(s,fill=None,line=dark,dash=False):
 s.CellsU('LineWeight').FormulaU='2.25 pt';s.CellsU('LineColor').FormulaU=rgb(line)
 s.CellsU('LinePattern').ResultIU=2 if dash else 1
 s.CellsU('FillPattern').ResultIU=1 if fill else 0
 if fill:s.CellsU('FillForegnd').FormulaU=rgb(fill)
 s.CellsU('ShdwPattern').ResultIU=0
 return s
def rect(x,y,w,h,fill=None,dash=False,round=False,line=dark):
 s=page.DrawRectangle(x/100,(H-y-h)/100,(x+w)/100,(H-y)/100);style(s,fill,line,dash)
 if round:s.CellsU('Rounding').ResultIU=.05
 return s
def text(x,y,w,h,t,size=20,fill=None):
 s=rect(x,y,w,h,fill);s.CellsU('LinePattern').ResultIU=0;s.Text=t
 s.CellsU('Char.Font').FormulaU='FONT("Arial")';s.CellsU('Char.Style').ResultIU=1
 # Layout uses 100 units/inch; the reference labels are specified in layout units.
 s.CellsU('Char.Size').FormulaU=f'{size*.72} pt'
 s.CellsU('Para.HorzAlign').ResultIU=1;s.CellsU('VerticalAlign').ResultIU=1
 for c in ['LeftMargin','RightMargin','TopMargin','BottomMargin']:s.CellsU(c).ResultIU=0
 return s
def box(x,y,w,h,t,fill=None,size=20,round=False):
 s=rect(x,y,w,h,fill,round=round);text(x+3,y+3,w-6,h-6,t,size);return s
def line(points,arrow=False,dash=False,color=dark,weight=2.25):
 out=[]
 for i,(a,b) in enumerate(zip(points[:-1],points[1:])):
  s=page.DrawLine(a[0]/100,(H-a[1])/100,b[0]/100,(H-b[1])/100);style(s,None,color,dash)
  s.CellsU('LineWeight').FormulaU=f'{weight} pt'
  if arrow and i==len(points)-2:s.CellsU('EndArrow').ResultIU=4;s.CellsU('EndArrowSize').ResultIU=2
  out.append(s)
 return out
def polygon(points,fill,linecolor=dark):
 coords=[v for x,y in points+[points[0]] for v in (x/100,(H-y)/100)]
 arr=win32com.client.VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,coords)
 s=page.DrawPolyline(tuple(coords),0);style(s,fill,linecolor);return s
def ellipse(x,y,r,fill):
 s=page.DrawOval((x-r)/100,(H-y-r)/100,(x+r)/100,(H-y+r)/100);return style(s,fill)
def robot(x,y,scale=1,pose=0):
 # Native editable arm links, bearings, pedestal and gripper.
 def pt(a,b):return (x+a*scale,y+b*scale)
 angles=[[(22,61),(7,36),(36,9),(58,12)],[(22,61),(12,37),(39,12),(62,20)],[(22,61),(4,33),(37,9),(58,7)]]
 joints=angles[pose%3]
 def link(a,b):
  dx=b[0]-a[0];dy=b[1]-a[1];l=math.hypot(dx,dy);nx=-dy/l*4;ny=dx/l*4
  polygon([pt(a[0]+nx,a[1]+ny),pt(b[0]+nx,b[1]+ny),pt(b[0]-nx,b[1]-ny),pt(a[0]-nx,a[1]-ny)],'#dde4e9')
 rect(x+9*scale,y+68*scale,29*scale,5*scale,'#c6ced6')
 polygon([pt(15,67),pt(17,59),pt(27,59),pt(31,67)],'#d2d9df')
 for a,b in zip(joints[:-1],joints[1:]):link(a,b)
 for a,b in joints:ellipse(*pt(a,b),5*scale,'#9ccde4')
 ax,ay=joints[-1];line([pt(ax,ay),pt(ax+10,ay+2)],weight=2.25)
 line([pt(ax+9,ay-4),pt(ax+17,ay-2),pt(ax+16,ay+2)],weight=2.25)
 line([pt(ax+8,ay+6),pt(ax+15,ay+8),pt(ax+17,ay+4)],weight=2.25)

# Panel frames and grouped backgrounds first.
rect(5,5,1910,470,round=True);rect(5,497,1910,318,round=True)
rect(635,156,430,195,dash=True,line='#999999')
rect(1100,183,315,155,dash=True,line='#999999')
rect(1674,183,214,155,dash=True,line='#999999')
rect(275,510,1020,229,dash=True,line='#999999')
rect(1386,544,220,150,dash=True,line='#999999')
# Top input stack, use original scene capture as one clearly identified image object.
rect(32,21,260,204,round=True);text(36,24,252,29,'RGB (camera)',23)
im=page.Import(str(P/'data/scene_head.png'))
im.CellsU('Width').ResultIU=2.44;im.CellsU('Height').ResultIU=1.61
im.CellsU('PinX').ResultIU=1.62;im.CellsU('PinY').ResultIU=(H-136)/100
rect(32,235,260,124,round=True);text(35,238,254,28,'Depth input (schematic)',18)
grid=[(79,279),(229,279),(259,326),(60,326)];polygon(grid,'#edf0f2', '#707980')
for i in range(1,10):
 t=i/10;line([(79+(229-79)*t,279),(60+(259-60)*t,326)],color='#9ba3a9',weight=.6)
for i in range(1,5):
 t=i/5;line([(79+(60-79)*t,279+47*t),(229+30*t,279+47*t)],color='#9ba3a9',weight=.6)
text(62,329,198,23,'H × W × 1',17)
box(32,370,260,65,'',round=True);text(35,373,254,26,'Instruction',22);text(42,402,240,26,'“place_empty_cup”',19,'#f2f2f2')
for y,t,c in [(32,'Swin\nEncoder',green),(174,'Swin\nEncoder',green),(348,'BERT',orange)]:
 polygon([(360,y),(550,y+28),(550,y+88),(360,y+116)],c)
 text(370,y+25,165,64,t,23)
line([(292,92),(354,92)],True);line([(292,232),(354,232)],True);line([(292,396),(354,396)],True)
line([(550,91),(595,91),(595,201),(637,201)],True)
line([(550,232),(595,232),(595,290),(637,290)],True)
line([(550,394),(595,394),(595,290)],False)
box(657,181,175,150,'Spatial /\nMultimodal\nFusion',blue,22)
box(888,181,162,150,'Action\nDecoder',blue,23)
line([(832,258),(882,258)],True)
rect(821,20,417,91);text(825,24,408,27,'Robot state',23)
for x,w,t in [(830,89,'EE pose'),(930,105,'Joint state'),(1047,131,'Gripper state')]:box(x,60,w,32,t,'#ededed',16,True)
text(1183,62,40,27,'…',23);line([(968,111),(968,174)],True)
text(1105,189,305,55,'Predicted action sequence\n(64 steps)',20)
for x,pose in [(1123,0),(1205,1),(1330,2)]:robot(x,250,.9,pose)
text(1280,267,35,32,'…',26)
box(1450,220,174,89,'Robot\nController',purple,23,True)
text(1679,188,204,59,'Executed actions\n(up to 32)',20)
robot(1686,254,.9,0);robot(1805,254,.9,1);text(1764,267,34,35,'…',24)
line([(1050,260),(1095,260)],True);line([(1415,260),(1444,260)],True);line([(1624,260),(1668,260)],True)
rect(1564,20,326,137,round=True);text(1570,26,314,29,'Colors denote model roles',19)
for x,c in zip([1582,1659,1736,1813],[blue,green,orange,purple]):rect(x,62,57,26,c)
rect(1582,112,53,25,dash=True,line='#999999');text(1641,101,240,45,'FPGA GEMMs + HostOp\nboundaries inside modules',16)
text(480,437,1050,31,'(a) HoloBrain-0 inputs and execution partition',25)
# Bottom detailed decoder and loops.
rect(20,512,209,203,round=True);text(24,517,201,29,'Inputs (features)',21)
box(32,550,184,45,'RGB feature',green,20,True)
box(32,604,184,45,'Depth feature',green,20,True)
box(32,659,184,44,'Language feature',orange,19,True)
line([(230,615),(306,615)],True)
text(560,515,430,29,'10 denoising steps',24)
rect(312,552,446,118,blue,round=True);text(318,557,434,28,'Decoder block 1',22)
for x,w,t in [(325,95,'Joint\nattention'),(425,109,'Image\nattention'),(539,108,'Text\nattention'),(652,91,'FFN')]:box(x,594,w,62,t,purple,18,True)
box(784,563,82,100,'Block 2',blue,19,True);box(916,563,82,100,'Block 6',blue,19,True)
text(874,593,35,31,'…',25)
box(1027,567,112,92,'Upsample\nhead',purple,20,True)
box(1165,567,111,92,'Scheduler\nupdate',purple,19,True)
for a,b,y in [(758,779,615),(998,1022,615),(1139,1160,615)]:line([(a,y),(b,y)],True)
line([(1220,659),(1220,702),(386,702),(386,675)],True)
text(672,705,290,25,'Next denoising step',19)
line([(1276,615),(1380,615)],True);text(1303,572,76,40,'After\nstep 10',17)
text(1391,548,210,52,'Predicted sequence:\n64 steps',20)
robot(1405,609,.93,0);robot(1514,609,.93,2);text(1480,620,33,32,'…',24)
box(1640,557,155,112,'Execute up to\n32 actions /\nchunk',purple,20,True)
line([(1606,615),(1634,615)],True)
line([(1795,615),(1871,615),(1871,762),(125,762),(125,719)],True)
text(1799,558,104,47,'Next\nobservation',18)
text(490,781,1070,28,'(b) Policy call and action-head iteration',25)

out=O/'figure1_native.vsdx';doc.SaveAs(str(out))
page.Export(str(O/'figure1_native.svg'))
doc.ExportAsFixedFormat(1,str(O/'figure1_native.pdf'),1,0)
count=page.Shapes.Count
doc.Close()
# Reopen the real VSDX and inspect native shape/style values.
doc=app.Documents.Open(str(out));p=doc.Pages.Item(1)
audit={'created_at':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'shape_count':p.Shapes.Count,'original_count':count,'text_shapes':0,'native_nontext_shapes':0,'foreign_images':0,'wrong_line_weights':[],'nonbold_text':[]}
for s in p.Shapes:
 if s.Type==4:audit['foreign_images']+=1;continue
 if s.Text:
  audit['text_shapes']+=1
  if not int(s.CellsU('Char.Style').ResultIU)&1:audit['nonbold_text'].append(s.ID)
 else:audit['native_nontext_shapes']+=1
 if int(s.CellsU('LinePattern').ResultIU) and abs(s.CellsU('LineWeight').ResultIU*72-2.25)>.01 and abs(s.CellsU('LineWeight').ResultIU*72-.6)>.01:audit['wrong_line_weights'].append(s.ID)
doc.Close();app.Quit()
(O/'audit.json').write_text(json.dumps(audit,indent=2),encoding='utf8')
print(json.dumps(audit))
# Render the actual Visio PDF (no substitute diagram renderer).
import fitz
d=fitz.open(O/'figure1_native.pdf');pg=d[0];pg.get_pixmap(matrix=fitz.Matrix(2,2)).save(O/'figure1_native.png');d.close()
