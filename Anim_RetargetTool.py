# use characterset based

import maya.cmds as maya
from functools import partial
import random

windowID = 'anim_retargetPanel'
pasteOptions=['merge','replaceCompletely','scaleMerge','scaleReplace']
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

def onOffsetMethodChanged(*arg):
    methodindex=maya.radioButtonGrp(timeOffsetMehod,q=True,sl=True)
    global RandomtimeOffset
    if methodindex==1:
        maya.intFieldGrp(fixedtimeOffset,e=True,en=True)
        maya.intFieldGrp(RandomtimeOffset,e=True,en=False)
    else:
        maya.intFieldGrp(fixedtimeOffset,e=True,en=False)
        maya.intFieldGrp(RandomtimeOffset,e=True,en=True)

def onCkChanged(*arg):
    #global copyKeyOptions
    index = maya.radioButtonGrp(copyKeyOptions, q=True, sl=True)
    if index == 1:
        maya.floatFieldGrp(timeStart, e=True, en=False)
        maya.floatFieldGrp(timeEnd, e=True, en=False)
    else:
        maya.floatFieldGrp(timeStart, e=True, en=True)
        maya.floatFieldGrp(timeEnd, e=True, en=True)

def onPkChanged(*arg):
    #global copyKeyOptions
    index = maya.radioButtonGrp(timeRange, q=True, sl=True)
    if index == 1:
        maya.floatFieldGrp(pastetimeStart, e=True, en=False)
        maya.floatFieldGrp(pastetimeEnd, e=True, en=False)
        maya.radioButtonGrp(pasteKeyOptions,e=True,en3=False)
        maya.radioButtonGrp(pasteKeyOptions,e=True,en4=False)
    else:
        maya.floatFieldGrp(pastetimeStart, e=True, en=True)
        maya.floatFieldGrp(pastetimeEnd, e=True, en=True)
        maya.radioButtonGrp(pasteKeyOptions,e=True,en3=True)
        maya.radioButtonGrp(pasteKeyOptions,e=True,en4=True)

def btnRemove(*arg):
    dtnItem = maya.textScrollList(dtnBox, q=True, si=True)
    if dtnItem==None:
        return
    for dtnObj in dtnItem:
        maya.cutKey(dtnObj)

def btnRetarget(*arg):
    currentTime = cmds.currentTime(query=True)
    sourceItem = maya.textScrollList(srcBox, q=True, si=True)
    pasteindex=maya.radioButtonGrp(pasteKeyOptions,q=True,sl=True)
    if sourceItem == None:
        return
    # copyKeyOptions
    index = maya.radioButtonGrp(copyKeyOptions, q=True, sl=True)
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
    index = maya.radioButtonGrp(timeRange, q=True, sl=True)
    print index
    if index == 1:
        for dtnObj in dtnItem:
            # Paste animation
            global pasteOptions
            #paste animation from current time
            qt=maya.currentTime(q=True)
            #get offsettime
            #use fixed offsettime or random offset from range
            if(maya.radioButtonGrp(timeOffsetMehod,q=True,sl=True)==1):
                offsettime = maya.intFieldGrp(fixedtimeOffset, q=True, value1=True)
            else:
                startint=maya.intFieldGrp(RandomtimeOffset,q=True,value1=True)
                endint=maya.intFieldGrp(RandomtimeOffset,q=True,value2=True)
                offsettime=random.randint(startint,endint)
            nt=qt+offsettime
            print offsettime
            #paste animation recursively
            if(maya.radioButtonGrp(timeOffsetOptions,q=True,sl=True)==2):
                maya.currentTime(nt,e=True)
            maya.pasteKey(dtnObj, t=(nt,),o=pasteOptions[pasteindex-1])
    else:
        #paste animation from specified time
        st=maya.floatFieldGrp(pastetimeStart,q=True,value1=True)
        print st
        et=maya.floatFieldGrp(pastetimeEnd,q=True,value1=True)
        for dtnObj in dtnItem:
            if(maya.radioButtonGrp(timeOffsetMehod,q=True,sl=True)==1):
                offsettime = maya.intFieldGrp(fixedtimeOffset, q=True, value1=True)
            else:
                startint=maya.intFieldGrp(RandomtimeOffset,q=True,value1=True)
                endint=maya.intFieldGrp(RandomtimeOffset,q=True,value2=True)
                offsettime=random.randint(startint,endint)
            nst=st+offsettime
            net=et+offsettime
            #paste animation recursively
            if(maya.radioButtonGrp(timeOffsetOptions,q=True,sl=True)==2):
                maya.currentTime(st,e=True)
            maya.pasteKey(dtnObj, t=(nst,net),o=pasteOptions[pasteindex-1])
            print st
            print et           



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
        430, 610), title='animRetargetPanel', s=True)
    layout = maya.columnLayout(w=430, h=610, rs=5)
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

    global timeRange
    timeRange=maya.radioButtonGrp(numberOfRadioButtons=2, label='Time range:', labelArray2=[
                                         'Current', 'Start/End'], sl=1, cc=onPkChanged)
    global pasteKeyOptions
    pasteKeyOptions = maya.radioButtonGrp(w=430,numberOfRadioButtons=4, l='Paste method:',labelArray4=[
                                         'merge','replace','scaleMerge','scaleReplace'], cw5=[75,65,65,100,100],sl=2)
    global pastetimeStart
    pastetimeStart = maya.floatFieldGrp(
        numberOfFields=1, label='Start time:', value1=0.000, en=False)
    global pastetimeEnd
    pastetimeEnd = maya.floatFieldGrp(
        numberOfFields=1, label='End time:', value1=10.000, en=False)

    global timeOffsetOptions
    timeOffsetOptions=maya.radioButtonGrp(numberOfRadioButtons=2, label='Offset type:', labelArray2=[
                                         'Same', 'Recursively'], sl=1)
    global timeOffsetMehod
    timeOffsetMehod=maya.radioButtonGrp(numberOfRadioButtons=2, label='Offset method:', labelArray2=[
                                         'Fixed', 'Random'], sl=1, cc=onOffsetMethodChanged)
    maya.setParent('..')
    maya.columnLayout(cat=['left', 80])
    global fixedtimeOffset
    fixedtimeOffset = maya.intFieldGrp(
        numberOfFields=1, label='Fixed Offset Amount:', value1=0.00)
    global RandomtimeOffset
    RandomtimeOffset = maya.intFieldGrp(
        numberOfFields=2, label='Random Offset Range:', value1=0.00,value2=0.00,en=False)
    maya.setParent('..')
    maya.separator(w=430,st='in')
    maya.columnLayout(h=5)
    maya.setParent('..')
    maya.columnLayout(cat=['left', 150],rs=5)
    maya.button(
        l='Remove Animation', al='center', w=130, h=30, c=btnRemove)

    maya.button(
        l='Retarget Animation', al='center', w=130, h=30, c=btnRetarget)

    maya.showWindow(windowID)


def animRetargetUI():
    if (maya.window(windowID, ex=True)):
        maya.deleteUI(windowID, wnd=True)
    animRetargetPanel()

animRetargetUI()



###import maya.cmds as maya

###selectobj=maya.ls(sl=True)

###characterset=[]

###for obj in selectobj:
    ###namespace=obj.split(':')[0]
    ###characterset.append(namespace+':generalCharacter')
 
###maya.select(characterset)
