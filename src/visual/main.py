from gizmo.utils import tag
from plug.qt.plugs.visual import Visual as Mode

class Visual(Mode):

    def event_functor(self, e, ear):

        t=e.text()
        sm=self.submode()
        c = sm in ['Hint', 'Jump']
        if c and t: 
            self.key+=t
            self.view.updateHint(self.key)
            return True
        return False

    def finishHinting(self):

        self.view.hintSelected.disconnect(
                self.selectHinted)
        self.view.hintFinished.disconnect(
                self.finishHinting)

    def selectHinted(self, data):

        i=data['item']
        sm=self.submode()
        if sm=='Jump': 
            self.jump(data)
        elif sm=='Hint':
            self.view.select(i, data)

    def listen(self):

        super().listen()
        self.setSubmode('Select')
        
    def delisten(self):

        super().delisten()
        self.setSubmode()

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

    @tag('w', modes=['visual[Hint]'])
    def hintWord(self):

        self.key=''
        self.view.hintSelected.connect(
                self.selectHinted)
        self.view.hintFinished.connect(
                self.finishHinting)
        self.view.hint(kind='words')

    @tag('o', modes=['visual[Select]'])
    def gotoStart(self): 
        self.go(kind='first')

    @tag('$', modes=['visual[Select]'])
    def gotoEnd(self):
        self.go(kind='last')

    @tag('j', modes=['visual[Select]']) 
    def selectDown(self, digit=1):
        self.go(kind='down', digit=digit)

    @tag('k', modes=['visual[Select]']) 
    def selectUp(self, digit=1):
        self.go(kind='up', digit=digit)

    @tag('J', modes=['visual[Select]']) 
    def deselectDown(self, digit=1):
        self.go(kind='cancelDown', digit=digit)

    @tag('K', modes=['visual[Select]']) 
    def deselectUp(self, digit=1):
        self.go(kind='cancelUp', digit=digit)

    @tag('w', modes=['visual[Select]']) 
    def selectNext(self, digit=1):
        self.go(kind='next', digit=digit)
        
    @tag('W', modes=['visual[Select]'])
    def deselectNext(self, digit=1):
        self.go(kind='cancelNext', digit=digit)

    @tag('b', modes=['visual[Select]']) 
    def selectPrev(self, digit=1):
        self.go(kind='prev', digit=digit)
        
    @tag('B', modes=['visual[Select]']) 
    def deselectPrev(self, digit=1):
        self.go(kind='cancelPrev', digit=digit)

    def jump(self, data):

        i=data['item']
        e=i.element()
        c=self.view.selection()
        e.jumpToBlock(c, data)
        
    def goto(self, kind, digit=1):

        for i in range(digit):
            data=self.view.selection()
            if data:
                i=data['item']
                e=i.element()
                e.updateBlock(kind, data)
                i.update()
