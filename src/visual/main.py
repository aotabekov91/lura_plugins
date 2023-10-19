from PyQt5 import QtCore, QtGui

from gizmo.utils import register
from plug.qt.plugs.visual import Visual as Mode

class Visual(Mode):

    hintSelected=QtCore.pyqtSignal()

    def __init__(
            self, 
            app,
            *args,
            listen_leader='<c-V>',
            **kwargs
            ):

        self.key=''
        self.s=None
        self.hints=None
        self.hinting=False
        super().__init__(
                app=app, 
                listen_leader=listen_leader,
                **kwargs,
                )

    def setup(self):

        super().setup()
        self.display=self.app.display
        self.listenerAddKeys=self.ear.addKeys
        self.ear.addKeys=self.addOwnKeys

    def addOwnKeys(self, event):

        if self.hinting:
            if event.text():
                self.key+=event.text()
                self.updateHint(self.key)
                event.accept()
                return True
        return self.listenerAddKeys(event)

    def delisten(self): 

        super().delisten()
        self.key=''
        self.s=None
        self.hints=None
        self.hinting=False

    def listen(self):

        super().listen()
        view=self.display.view
        if view and not view.selected(): 
            self.hint()

    def jump(self):

        s=self.display.view.selected()
        item=s[-1]['item']
        page=item.page()
        # b=self.s[0]['box']
        # start, end, rect = b[0], b[-1], 
        start=self.s[0]['box'][0]
        end=self.s[0]['box'][-1]
        rect=s[0]['box'][0]
        if rect.y()>end.y():
            # item.select([page.getRows(start, rect)])
            selected=[page.getRows(start, rect)]
        elif rect.y()<start.y():
            # item.select([page.getRows(rect, end)])
            selected=[page.getRows(rect, end)]
        else:
            # item.select([page.getRows(start, rect)])
            selected=[page.getRows(start, rect)]
        item.select(selected)
        self.hintSelected.disconnect(self.jump)

    @register('o')
    def gotoStart(self): 

        s=self.display.view.selected()
        if s: 
            self.getWord(s, word='first')

    @register('$')
    def gotoEnd(self):

        s=self.display.view.selected()
        if s: 
            self.getWord(s, word='last')

    @register('j') 
    def selectNextRow(self, digit=1):

        for i in range(digit):
            self.getRow(direction='next')
        
    @register('J') 
    def deselectNextRow(self, digit=1):

        for i in range(digit): 
            self.getRow(direction='next', kind='deselect')
        
    @register('k') 
    def selectPrevRow(self, digit=1):

        for i in range(digit): 
            self.getRow(direction='prev')

    @register('K') 
    def deselectPrevRow(self, digit=1):

        for i in range(digit): 
            self.getRow(direction='prev', kind='deselect')

    def getRow(self, direction='next', kind='select'):

        s=self.display.view.selected()
        if s:
            item=s[-1]['item']
            page=item.page()
            start=s[-1]['box'][0]
            end=s[-1]['box'][-1]
            if kind=='select':
                if direction=='next':
                    edge=QtCore.QRectF(end.x(), 
                                end.y()+end.height()+2, 
                                end.width(), 
                                end.height())
                    data=page.getRow(edge.bottomLeft())
                    # data=page.getRow(edge.bottomRight())
                    if data: 
                        edge=data['box'][-1]
                        selected=[page.getRows(start, edge)]
                        if selected: item.select(selected)
                elif direction=='prev':
                    edge=QtCore.QRectF(start.x(),
                                start.y()-start.height()-2, 
                                start.width(), 
                                start.height())
                    data=page.getRow(edge.topLeft())
                    if data: 
                        edge=data['box'][-1]
                        selected=[page.getRows(edge, end)]
                        if selected: item.select(selected)
            elif kind=='deselect':
                if len(s[-1]['box'])>1:
                    if direction=='next':
                        edge=s[-1]['box'][-2]
                        selected=[page.getRows(start, edge)]
                        if selected: item.select(selected)
                    elif direction=='prev':
                        edge=s[-1]['box'][1]
                        selected=[page.getRows(edge, end)]
                        if selected: item.select(selected)

    @register('e')
    def jumpSelect(self):

        s=self.display.view.selected()
        if s:
            self.s=s
            self.hintSelected.connect(self.jump)
            self.hint()

    @register('w') 
    def selectNextWord(self, digit=1):
        
        for d in range(digit):
            s=self.display.view.selected()
            if s: 
                self.getWord(s, kind='select')

    @register('W')
    def deselectNextWord(self, digit=1):

        for d in range(digit):
            s=self.display.view.selected()
            if s: 
                self.getWord(s, kind='deselect')

    @register('b') 
    def selectPrevWord(self, digit=1):
        
        for d in range(digit):
            s=self.display.view.selected()
            if s: 
                self.getWord(s, kind='select', direction='backward')

    @register('B') 
    def deselectPrevWord(self, digit=1):
        
        for d in range(digit):

            s=self.display.view.selected()
            if s: 
                self.getWord(s, kind='deselect', direction='backward')

    def getWord(self, s, kind='select', direction='forward', word=None):

        item=s[-1]['item']
        page=item.page()
        selected=None
        boxes=s[-1]['data']
        start=s[-1]['box'][0]
        end=s[-1]['box'][-1]

        if word=='first':

            rect=QtCore.QRectF(0, start.y(), start.x(), start.height())
            selected=page.getRows(rect, end)
            if selected:
                first_word=selected['data'][0].boundingBox()
                selected=[page.getRows(first_word, end)]

        elif word=='last':

            rect=QtCore.QRectF(end.x(), end.y(), page.size().width(), end.height())
            selected=page.getRows(rect, end)
            if selected:
                last_word=selected['data'][-1].boundingBox()
                selected=[page.getRows(start, last_word)]

        elif kind=='select':

            if direction=='forward':

                edge_horizontal=QtCore.QRectF(end.x()+end.width()+2, end.y(), 5, end.height())
                data=page.getRow(edge_horizontal.bottomRight())

                if data: 
                    edge=data['box'][-1]
                    selected=[page.getRows(start, edge)]

                else:
                    for i in range(1, int(end.x())):
                        edge=QtCore.QRectF(i, end.y()+end.height()+2, 2, end.height())
                        data=page.getRow(edge.bottomRight())

                        if data: 
                            edge=data['box'][-1]
                            selected=[page.getRows(start, edge)]
                            break

            elif direction=='backward':

                edge_horizontal=QtCore.QRectF(start.x()-7, start.y(), 5, start.height())
                data=page.getRow(edge_horizontal.topLeft())
                if data: 
                    edge=data['box'][-1]
                    selected=[page.getRows(edge, end)]

                else:
                    width=page.size().width()
                    for i in range(int(width), int(start.x()), -1):
                        edge=QtCore.QRectF(i, start.y()-start.height(), 2, start.height()/2.)
                        data=page.getRow(edge.bottomRight())

                        if data: 
                            edge=data['box'][-1]
                            selected=[page.getRows(edge, end)]
                            break

        elif kind=='deselect':

            if direction=='forward':

                if len(boxes)>=2:
                    start=boxes[0].boundingBox()
                    edge=boxes[-2].boundingBox()
                    selected=[page.getRows(start, edge)]

            elif direction=='backward':

                if len(boxes)>=2:
                    edge=boxes[1].boundingBox()
                    end=boxes[-1].boundingBox()
                    selected=[page.getRows(edge, end)]

        if selected: 
            item.select(selected)

    @register('u')
    def updateHint(self, key=''):

        hints={}
        for item, data in self.hints.items():
            for i, h in data.items():
                if key==i[:len(key)]: 
                    if not item in hints: 
                        hints[item]={}
                    hints[item][i]=h
        self.hints=hints
        self.display.view.updateAll()
        keys=list(self.hints.keys())
        if len(keys)<=1:
            if not keys:
                self.ear.clearKeys()
                self.hints=None
                self.hinting=False
            elif len(self.hints[keys[0]])<=1:
                if len(self.hints[keys[0]])==1:
                    data=list(self.hints[keys[0]].values())[0]
                    hint=data[0]
                    item=data[1]
                    top_point=hint.boundingBox().topLeft()
                    data=item.page().getRow(top_point)
                    item.select([data])
                    self.hintSelected.emit()
                self.unhint()

    def unhint(self):

        self.key=''
        self.hints=None
        self.hinting=False
        self.display.itemPainted.disconnect(
                self.paint)

    def hint(self):

        self.hinting=True
        self.display.itemPainted.connect(
                self.paint)
        self.display.view.updateAll()

    def generate(self, view):

        alphabet = 'abcdefghijklmnopqrstuwxyz'
        len_of_codes = 3
        char_to_pos = {}

        def number_to_string(n):
            chars = []
            for _ in range(len_of_codes):
                chars.append(alphabet[n % len(alphabet)])
                n = n // len(alphabet)
            return "".join(reversed(chars))
        for i in range(len(alphabet)): 
            char_to_pos[alphabet[i]] = i

        i=0
        hints={}
        for item in view.visibleItems(): 
            hints[item]={}
            text_list=item.page().textList()
            for j, h in enumerate(text_list):
                n=i+j
                hint=number_to_string(n)
                hints[item][hint]=[h, item]
            i=n
        return hints

    def paint(self, painter, options, widget, item, view):

        if self.hinting:
            if self.hints is None: 
                self.hints=self.generate(view)
            painter.save()
            pen=QtGui.QPen(QtCore.Qt.red, 0.0)
            painter.setPen(pen)
            item_hints=self.hints.get(item, None)
            if item_hints:
                for i, data in item_hints.items():
                    transformed_rect=item.mapToItem(
                            data[0].boundingBox())
                    painter.drawText(
                            transformed_rect.topLeft(), i)
            painter.restore()

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening:
                return True
            current=self.app.moder.current
            if current and current.name=='Normal':
                return True
        return False
