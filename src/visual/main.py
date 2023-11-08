from PyQt5 import QtCore, QtGui

from gizmo.utils import register
from plug.qt.plugs.visual import Visual as Mode

class Visual(Mode):

    hintSelected=QtCore.pyqtSignal()

    def __init__(
            self, *args, **kwargs):

        self.key=''
        self.s=None
        self.view=None
        self.jumping=False
        self.hinting=False
        super().__init__(
                *args, **kwargs)
        self.listenerAddKeys=self.ear.addKeys
        self.ear.addKeys=self.addOwnKeys

    def addOwnKeys(self, event):

        if self.hinting:
            if event.text():
                self.key+=event.text()
                self.view.updateHint(self.key)
                event.accept()
                return True
        return self.listenerAddKeys(event)

    def delisten(self): 

        super().delisten()
        self.view.hintSelected.disconnect(
                self.selectHinted)
        self.view.hintFinished.disconnect(
                self.selectHinted)

    def listen(self):

        super().listen()
        self.view.hintSelected.connect(
                self.selectHinted)
        self.view.hintFinished.connect(
                self.selectHinted)
        if not self.view.selection():
            self.hint()

    def selectHinted(self, data=None):

        self.hinting=False
        if data:
            i=data['item']
            if not self.jumping:
                if self.view.check('canSelect'):
                    self.view.select(i, data)
            else:
                self._jump(data)

    @register('f')
    def hint(self):

        self.key=''
        self.hinting=True
        self.view.hint()

    @register('o')
    def gotoStart(self): 
        self.goto(kind='first')

    @register('$')
    def gotoEnd(self):
        self.goto(kind='last')

    @register('j') 
    def selectDown(self, digit=1):
        self.goto(kind='down', digit=digit)

    @register('k') 
    def selectUp(self, digit=1):
        self.goto(kind='up', digit=digit)

    @register('J') 
    def deselectDown(self, digit=1):
        self.goto(kind='cancelDown', digit=digit)

    @register('K') 
    def deselectUp(self, digit=1):
        self.goto(kind='cancelUp', digit=digit)

    @register('w') 
    def selectNext(self, digit=1):
        self.goto(kind='next', digit=digit)
        
    @register('W')
    def deselectNext(self, digit=1):
        self.goto(kind='cancelNext', digit=digit)

    @register('b') 
    def selectPrev(self, digit=1):
        self.goto(kind='prev', digit=digit)
        
    @register('B') 
    def deselectPrev(self, digit=1):
        self.goto(kind='cancelPrev', digit=digit)

    @register('g')
    def jump(self):

        self.jumping=True
        self.hint()

    def _jump(self, sel):

        self.jumping=False
        item=sel['item']
        e=item.element()
        c=self.view.selection()
        e.jumpToBlock(c, sel)
        
    def goto(self, kind, digit=1):

        for i in range(digit):
            sel=self.view.selection()
            if sel:
                item=sel['item']
                e=item.element()
                e.updateBlock(kind, sel)
                item.update()

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening:
                return True
            m=self.app.moder.current
            if m and m.name=='normal':
                v=m.getView()
                if v.check('canHint'):
                    self.view=v
                    return True
        return False
