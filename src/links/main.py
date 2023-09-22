import subprocess

from PyQt5 import QtCore, QtGui

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
                app=app,
                listen_leader=listen_leader,
                **kwargs
                )

        self.key=''
        self.links=None
        self.selection=None

    def setup(self):

        super().setup()
        self.display=self.app.window.main.display
        self.setConnect()

    def setConnect(self):

        self.display.itemPainted.connect(
                self.paint)
        self.listenerAddKeys=self.ear.addKeys
        self.ear.addKeys=self.ownAddKeys

    def ownAddKeys(self, event):

        text=event.text()
        if text:
            self.key+=text
            self.updateHint(self.key)
            event.accept()
            return True
        else:
            return self.listenerAddKeys(event)

    def updateHint(self, key):

        links={}
        for i, h in self.links.items():
            if key==i[:len(key)]: 
                links[i]=h
        self.links=links
        self.display.view.updateAll()
        if len(self.links)<=1:
            if len(self.links)==1: 
                self.open(links[key])
            self.delistenWanted.emit()

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
        self.key=''
        self.links=None
        self.selection=None

    def listen(self):

        super().listen()
        self.display.view.updateAll()

    def generate(self, item):

        def number_to_string(n):
            chars = []
            for _ in range(len_of_codes):
                chars.append(alphabet[n % len(alphabet)])
                n = n // len(alphabet)
            return "".join(reversed(chars))

        alphabet = 'abcdefghijkmnopqrstuvwxyz'
        len_of_codes = 2
        char_to_pos = {}

        for i in range(len(alphabet)): 
            char_to_pos[alphabet[i]] = i
        links=item.page().links()
        return {number_to_string(i):h  for i, h in enumerate(links)}

    def paint(self, painter, options, widget, item, view):

        if self.listening:
            if self.links is None: 
                self.links=self.generate(item)
            painter.save()
            for i, link in self.links.items():
                rect=item.mapToItem(link['boundary'], isUnified=True)
                page_rect=item.mapToPage(rect, unify=False)
                link['down']=i
                link['up']=text=item.page().find(page_rect)
                pen=QtGui.QPen(QtGui.QColor(88, 139, 174, 220), 0.0)
                painter.setPen(pen)
                painter.drawRect(rect)
                pen=QtGui.QPen(QtCore.Qt.red, 0.0)
                painter.setPen(pen)
                painter.drawText(rect.topLeft(), i)
            painter.restore()

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.listening:
                return True
            current=self.app.plugman.current
            if current and current.name=='normal':
                return True
        return False
