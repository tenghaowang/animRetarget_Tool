# use characterset based

import maya.cmds as maya
from functools import partial
windowID = 'anim_retargetPanel'

# the function helps to find the first and last key of the current source


def endKey(obj, *arg):
    return cmds.findKeyframe(obj, which='last')


def firstKey(obj, *arg):
    return cmds.findKeyframe(obj, which='first')


def selection(*arg):
    selectObjDtn = maya.textScrollList(dtnBox, q=True, si=True)
    selectObjSrc = maya.textScrollList(srcBox, q=True, si=True)
    # print selectObj
    if selectObjSrc == None:
        selectObjSrc = []
    if selectObjDtn == None:
        selectObjDtn = []
    selectobj = selectObjDtn+selectObjSrc
    print selectobj
    maya.select(selectobj)
    # maya.select(selectObjSrc)


def onPkChanged(*arg):
	print '123'

def onCkChanged(*arg):
    #global copyKeyOptions
    index = maya.radioButtonGrp(copyKeyOptions, q=True, sl=True)
    print index
    if index == 1:
        maya.floatFieldGrp(timeStart, e=True, en=False)
        maya.floatFieldGrp(timeEnd, e=True, en=False)
    else:
        maya.floatFieldGrp(timeStart, e=True, en=True)
        maya.floatFieldGrp(timeEnd, e=True, en=True)


def btnRetarget(*arg):
    currentTime = cmds.currentTime(query=True)
    sourceItem = maya.textScrollList(srcBox, q=True, si=True)
    if sourceItem == None:
        return
    # copyKeyOptions
    index = maya.radioButtonGrp(copyKeyOptions, q=True, sl=True)
    offsettime = maya.intFieldGrp(timeOffset, q=True, value1=True)
    if(index == 1):
        starttime = firstKey(sourceItem[0])
        endtime = endKey(sourceItem[0])
    else:
        starttime = maya.floatFieldGrp(timeStart, q=True, value1=True)
        endtime = maya.floatFieldGrp(timeEnd, q=True, value1=True)

    maya.copyKey(sourceItem[0], t=(starttime, endtime))
    dtnItem = maya.textScrollList(dtnBox, q=True, si=True)
    if dtnItem == None:
        return
    for dtnObj in dtnItem:
        # Paste animation
        print dtnObj
        maya.pasteKey(dtnObj, o='merge', to=offsettime)


def addItem(Item, *arg):
    global srcBox
    selectobj = maya.ls(sl=True)
    exisingobj = maya.textScrollList(Item, q=True, ai=True)
    if exisingobj == None:
        exisingobj = []
    # find unique object in the list
    newobj = list(set(selectobj)-set(exisingobj))
    maya.textScrollList(Item, e=True, a=newobj)


def removeItem(Item, *arg):
    selectobj = maya.textScrollList(Item, q=True, si=True)
    print selectobj
    if selectobj != None:
        maya.textScrollList(Item, e=True, ri=selectobj)


def animRetargetPanel():
    maya.window(windowID, widthHeight=(
        430, 600), title='animRetargetPanel', s=True)
    layout = maya.columnLayout(w=430, h=500, rs=5)
    maya.columnLayout(h=5)
    maya.setParent('..')
    maya.text(l='animRetarget Tool', al='center',
              w=430, h=10, fn='boldLabelFont')
    srcDtnForm = maya.formLayout()
    # define UI for source
    srcLayout = maya.columnLayout(w=200, h=280, rs=5)
    maya.text(l='Source', al='center', w=200, h=20, fn='boldLabelFont')
    global srcBox
    srcBox = maya.textScrollList(w=200, h=200, sc=selection)
    maya.button(l='Add Source', w=200, h=20, c=partial(addItem, srcBox))
    maya.button(l='Remove Source', w=200, h=20, c=partial(removeItem, srcBox))
    maya.setParent('..')
    # define UI for destination
    dtnLayout = maya.columnLayout(w=200, h=280, rs=5)
    maya.text(l='Destination', al='center', w=200, h=20, fn='boldLabelFont')
    global dtnBox
    dtnBox = maya.textScrollList(w=200, h=200, ams=True, sc=selection)
    maya.button(l='Add Destination', w=200, h=20, c=partial(addItem, dtnBox))
    maya.button(
        l='Remove Destination', w=200, h=20, c=partial(removeItem, dtnBox))
    maya.setParent('..')
    maya.formLayout(srcDtnForm, e=True, ac=[dtnLayout, 'left', 10, srcLayout], af=[
                    (srcLayout, 'left', 10), (dtnLayout, 'right', 10)])
    maya.setParent('..')
    # Copy Options
    maya.separator(w=430, st='in')
    maya.columnLayout(rs=2)
    maya.text(l='Copy Keys Options', w=430, h=20, fn='boldLabelFont')
    global copyKeyOptions
    copyKeyOptions = maya.radioButtonGrp(numberOfRadioButtons=2, label='Time range:', labelArray2=[
                                         'All', 'Start/End'], sl=1, cc=onCkChanged)
    global timeStart
    timeStart = maya.floatFieldGrp(
        numberOfFields=1, label='Start time:', value1=0.000, en=False)
    global timeEnd
    timeEnd = maya.floatFieldGrp(
        numberOfFields=1, label='End time:', value1=10.000, en=False)
    maya.setParent('..')
    maya.separator(w=430, st='in')
    maya.columnLayout(rs=2)
    maya.text(l='Paste Keys Options', w=430, h=20, fn='boldLabelFont')
    maya.columnLayout(cat=['left',20])
    #maya.radioButtonGrp(w=430,label='Four Buttons', labelArray4=['I', 'II', 'III', 'IV'], numberOfRadioButtons=4 )
	#maya.radioButtonGrp( label='Four Buttons', labelArray4=['I', 'II', 'III', 'IV'], numberOfRadioButtons=4 )
    pastKeyOptions = maya.radioButtonGrp(w=430,numberOfRadioButtons=4, l='Paste method:',labelArray4=[
                                         'merge','replace','scaleMerge','fitMerge'], cw5=[75,65,65,100,100],sl=1, cc=onPkChanged)
    global timeStart
    maya.setParent('..')
    maya.columnLayout(cat=['left', 80])
    global timeOffset
    timeOffset = maya.intFieldGrp(
        numberOfFields=1, label='Time Offset Amount:', value1=0.00)
    maya.setParent('..')
    maya.columnLayout(cat=['left', 150])
    maya.button(
        l='Retarget Animation', al='center', w=130, h=20, c=btnRetarget)
    maya.showWindow(windowID)


def animRetargetUI():
    if (maya.window(windowID, ex=True)):
        maya.deleteUI(windowID, wnd=True)
    animRetargetPanel()

animRetargetUI()
