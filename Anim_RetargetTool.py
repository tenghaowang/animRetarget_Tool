#use characterset based

import maya.cmds as maya
from functools import partial
windowID='anim_retargetPanel'


def btnRetarget(*arg):
	sourceItem=maya.textScrollList(srcBox,q=True,si=True)
	if sourceItem==None:
		return
	print sourceItem[0]
	maya.copyKey(sourceItem[0])
	dtnItem=maya.textScrollList(dtnBox,q=True,si=True)
	if dtnItem==None:
		return
	for dtnObj in dtnItem:
		#Paste animation
		print  dtnObj
		maya.pasteKey(dtnObj)

def addItem(Item,*arg):
	global srcBox
	selectobj=maya.ls(sl=True)
	exisingobj=maya.textScrollList(Item,q=True,ai=True)
	if exisingobj==None:
		exisingobj=[]
	#find unique object in the list
	newobj=list(set(selectobj)-set(exisingobj))
	maya.textScrollList(Item,e=True,a=newobj)

def removeItem(Item,*arg):
	selectobj=maya.textScrollList(Item,q=True,si=True)
	print selectobj
	if selectobj!=None:
		maya.textScrollList(Item,e=True,ri=selectobj)

def animRetargetPanel():	
	maya.window(windowID,widthHeight=(430,600),title='animRetargetPanel',s=True)
	layout=maya.columnLayout(w=430,h=500,rs=5)
	maya.columnLayout(h=5)
	maya.setParent('..')
	maya.text(l='animRetarget Tool',al='center',w=430,h=10,fn='boldLabelFont')
	srcDtnForm=maya.formLayout()
	#define UI for source
	srcLayout=maya.columnLayout(w=200,h=280,rs=5)
	maya.text(l='Source',al='center',w=200,h=20,fn='boldLabelFont')
	global srcBox
	srcBox=maya.textScrollList(w=200,h=200)
	maya.button(l='Add Source',w=200,h=20,c=partial(addItem,srcBox))
	maya.button(l='Remove Source',w=200,h=20,c=partial(removeItem,srcBox))	
	maya.setParent('..')
	#define UI for destination
	dtnLayout=maya.columnLayout(w=200,h=280,rs=5)
	maya.text(l='Destination',al='center',w=200,h=20,fn='boldLabelFont')
	global dtnBox
	dtnBox=maya.textScrollList(w=200,h=200,ams=True)
	maya.button(l='Add Destination',w=200,h=20,c=partial(addItem,dtnBox))
	maya.button(l='Remove Destination',w=200,h=20,c=partial(removeItem,dtnBox))
	maya.setParent('..')
	maya.formLayout(srcDtnForm,e=True,ac=[dtnLayout,'left',10,srcLayout],af=[(srcLayout,'left',10),(dtnLayout,'right',10)])
	maya.setParent('..')
	maya.columnLayout(cat=['left',150])
	maya.button(l='Retarget Animation', al='center',w=130,h=20,c=btnRetarget)
	maya.showWindow(windowID)


def animRetargetUI():
	if (maya.window(windowID,ex=True)):
		maya.deleteUI(windowID, wnd=True)
	animRetargetPanel()
	
animRetargetUI()	 