from gizmo.utils import tag
from plug.qt.plugs import visual

class Visual(visual.Visual):

    def event_functor(self, e, ear):

        t=e.text()
        sm=self.submode()
        if sm in ['Hint', 'Jump'] and t: 
            self.key+=t
            self.view.updateHint(self.key)
            return True

    def finishHinting(self):

        self.setSubmode('Select')
        self.app.earman.clearKeys()
        self.view.hintSelected.disconnect(
                self.selectHinted)
        self.view.hintFinished.disconnect(
                self.finishHinting)

    def selectHinted(self, sel):

        i=sel['item']
        sm=self.submode()
        if sm=='Jump': 
            self.jump(sel)
        elif sm=='Hint':
            self.view.select(i, sel)

    def activate(self):

        super().activate()
        if not self.view.selection():
            self.hintWord()
            self.setSubmode('Hint')
        else:
            self.setSubmode('Select')
        
    def octivate(self):

        super().octivate()
        self.setSubmode()

    @tag('w', modes=['visual[Hint]'])
    def hintWord(self):

        self.key=''
        self.view.hintSelected.connect(
                self.selectHinted)
        self.view.hintFinished.connect(
                self.finishHinting)
        self.view.hint(kind='words')

    def jump(self, data):

        i=data['item']
        e=i.element()
        c=self.view.selection()
        e.jumpToBlock(c, data)
        
    def goTo(self, kind, digit=1):

        for i in range(digit):
            s=self.view.selection()
            if not s: return
            i=s['item']
            e=i.element()
            e.updateBlock(kind, s)
            i.update()

    @tag('<c-j>', modes=['visual']) 
    def activateJump(self):
        self.setSubmode('Jump')

    @tag('<c-h>', modes=['visual']) 
    def activateHint(self):
        self.setSubmode('Hint')

    @tag('<c-s>', modes=['visual']) 
    def activateSelect(self):
        self.setSubmode('Select')

    @tag('w', modes=['visual[Jump]']) 
    def jumpWord(self):
        self.hintWord()

    @tag('o', modes=['visual[Select]'])
    def gotoStart(self): 
        self.goTo(kind='first')

    @tag('$', modes=['visual[Select]'])
    def gotoEnd(self):
        self.goTo(kind='last')

    @tag('j', modes=['visual[Select]']) 
    def selectDown(self, digit=1):
        self.goTo(kind='down', digit=digit)

    @tag('k', modes=['visual[Select]']) 
    def selectUp(self, digit=1):
        self.goTo(kind='up', digit=digit)

    @tag('J', modes=['visual[Select]']) 
    def deselectDown(self, digit=1):
        self.goTo(kind='cancelDown', digit=digit)

    @tag('K', modes=['visual[Select]']) 
    def deselectUp(self, digit=1):
        self.goTo(kind='cancelUp', digit=digit)

    @tag('w', modes=['visual[Select]']) 
    def selectNext(self, digit=1):
        self.goTo(kind='next', digit=digit)
        
    @tag('W', modes=['visual[Select]'])
    def deselectNext(self, digit=1):
        self.goTo(kind='cancelNext', digit=digit)

    @tag('b', modes=['visual[Select]']) 
    def selectPrev(self, digit=1):
        self.goTo(kind='prev', digit=digit)
        
    @tag('B', modes=['visual[Select]']) 
    def deselectPrev(self, digit=1):
        self.goTo(kind='cancelPrev', digit=digit)
