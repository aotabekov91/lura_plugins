from PyQt5 import QtCore, QtGui

from gizmo.utils import tag
from plug.qt.plugs.visual import Visual as Mode

class Visual(Mode):

    key=''
    jumping=False
    hinting=False
    seletion=None
    hintSelected=QtCore.pyqtSignal()

    def addOwnKeys(self, event):

        if self.hinting:
            if event.text():
                self.key+=event.text()
                self.view.updateHint(self.key)
                event.accept()
                return True
        return self.listenerAddKeys(event)

    def finishHinting(self):

        self.hinting=False
        self.view.hintSelected.disconnect(
                self.selectHinted)
        self.view.hintFinished.disconnect(
                self.finishHinting)

    def selectHinted(self, data):

        i=data['item']
        if not self.jumping:
            if self.view.check('canSelect'):
                self.view.select(i, data)
        else:
            self._jump(data)

    @tag('f')
    def hint(self):

        self.key=''
        self.hinting=True
        self.view.hintSelected.connect(
                self.selectHinted)
        self.view.hintFinished.connect(
                self.finishHinting)
        self.view.hint()

    @tag('o')
    def gotoStart(self): 
        self.goto(kind='first')

    @tag('$')
    def gotoEnd(self):
        self.goto(kind='last')

    @tag('j') 
    def selectDown(self, digit=1):
        self.goto(kind='down', digit=digit)

    @tag('k') 
    def selectUp(self, digit=1):
        self.goto(kind='up', digit=digit)

    @tag('J') 
    def deselectDown(self, digit=1):
        self.goto(kind='cancelDown', digit=digit)

    @tag('K') 
    def deselectUp(self, digit=1):
        self.goto(kind='cancelUp', digit=digit)

    @tag('w') 
    def selectNext(self, digit=1):
        self.goto(kind='next', digit=digit)
        
    @tag('W')
    def deselectNext(self, digit=1):
        self.goto(kind='cancelNext', digit=digit)

    @tag('b') 
    def selectPrev(self, digit=1):
        self.goto(kind='prev', digit=digit)
        
    @tag('B') 
    def deselectPrev(self, digit=1):
        self.goto(kind='cancelPrev', digit=digit)

    @tag('g')
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
