import subprocess

from PyQt5 import QtCore

from plug.qt import Plug
from plug.qt.utils import register

class Links(Plug):

    hintSelected=QtCore.pyqtSignal()

    def __init__(self,
                 app,
                 *args,
                 listen_leader='<c-l>',
                 **kwargs):

        super().__init__(
                *args,
                app=app
                listen_leader=listen_leader,
                **kwargs
                )

        self.links=None
        self.selection=None

    def setup(self):

        super().setup()
        self.display=self.app.window.main.display
        self.setConnect(self)

    def setConnect(self):

        pass
            
    def addKeys(self, event):

        self.timer.stop()
        if self.activated:
            if self.registerKey(event): 
                self.updateHint()
        else:
            super().addKeys(event)

    def updateHint(self):

        key=''.join(self.keys_pressed)
        links={}
        for i, h in self.links.items():
            if key==i[:len(key)]: links[i]=h
        self.links=links
        self.display.view.updateAll()
        if len(self.links)<=1:
            if len(self.links)==1: 
                self.open(links[key])
            self.delisten()

    def open(self, link): 

        if 'url' in link: 
            cmd=['qutebrowser', link['url']]
            subprocess.Popen(cmd)
        elif 'page' in link:
            y=link['top']
            page=link['page']
            self.display.view.goto(
                    page, changeTop=y)

    def delisten(self): 

        super().delisten()
        if self.activated:
            self.links=None
            self.activated=False
            self.ui.deactivate()
            self.display.itemPainted.disconnect(
                    self.paint)
            self.display.view.updateAll()

    @register('l', modes=['command'])
    def listen(self):

        super().listen()
        self.links=None
        self.activated=True
        self.display.itemPainted.connect(
                self.paint)
        self.display.view.updateAll()

    def generate(self, item):

        alphabet = 'abcdefghijkmnopqrstuvwxyz'
        len_of_codes = 2
        char_to_pos = {}
        def number_to_string(n):
            chars = []
            for _ in range(len_of_codes):
                chars.append(alphabet[n % len(alphabet)])
                n = n // len(alphabet)
            return "".join(reversed(chars))
        for i in range(len(alphabet)): 
            char_to_pos[alphabet[i]] = i
        links=item.page().links()
        return {number_to_string(i):h  for i, h in enumerate(links)}

    def paint(self, painter, options, widget, item, v):

        if self.activated:
            if self.links is None: 
                self.links=self.generate(item)
            painter.save()
            for i, link in self.links.items():
                rect=item.mapToItem(link['boundary'], isUnified=True)
                page_rect=item.mapToPage(rect, unify=False)
                link['down']=i
                link['up']=text=item.page().find(page_rect)
                pen=QPen(QColor(88, 139, 174, 220), 0.0)
                painter.setPen(pen)
                painter.drawRect(rect)
                pen=QPen(Qt.red, 0.0)
                painter.setPen(pen)
                painter.drawText(rect.topLeft(), i)
            painter.restore()
