import subprocess

from PyQt5 import QtCore

from plug.qt import Plug
from plug.qt.utils import register
from gizmo.widget import ListWidget, Item

class Links(Plug):

    hintSelected=QtCore.pyqtSignal()

    def __init__(self, app, **kwargs):

        super().__init__(
                app=app, 
                show_statusbar=True,
                **kwargs,
                )

        self.links=None
        self.selection=None
        self.activated=False

        self.setUI()
            
    def addKeys(self, event):

        self.timer.stop()

        if self.activated:
            if self.registerKey(event): self.updateHint()
        else:
            super().addKeys(event)

    def updateHint(self):

        key=''.join(self.keys_pressed)

        links={}
        for i, h in self.links.items():
            if key==i[:len(key)]: links[i]=h

        self.links=links

        self.app.window.main.display.view.updateAll()

        if len(self.links)<=1:

            if len(self.links)==1: self.open(links[key])
            self.delisten()

    def open(self, link): 

        if 'url' in link: 
            cmd=['qutebrowser', link['url']]
            subprocess.Popen(cmd)
        elif 'page' in link:
            y=link['top']
            page=link['page']
            self.app.window.main.display.view.goto(page, changeTop=y)

    @register('l')
    def delisten(self, *args, **kwargs): 

        super().delisten(*args, **kwargs)
        
        if self.activated:

            self.links=None
            self.activated=False

            self.ui.deactivate()

            self.app.window.main.display.itemPainted.disconnect(self.paint)
            self.app.window.main.display.view.updateAll()

    @register('l', modes=['command'])
    def listen(self):

        super().listen()

        self.links=None
        self.activated=True

        self.app.window.main.display.itemPainted.connect(self.paint)
        self.app.window.main.display.view.updateAll()

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

        for i in range(len(alphabet)): char_to_pos[alphabet[i]] = i

        links=item.page().links()

        return {number_to_string(i):h  for i, h in enumerate(links)}

    def paint(self, painter, options, widget, pageItem, view):

        if self.activated:

            if self.links is None: self.links=self.generate(pageItem)

            painter.save()

            for i, link in self.links.items():

                transformed_rect=pageItem.mapToItem(link['boundary'], isUnified=True)
                page_rect=pageItem.mapToPage(transformed_rect, unify=False)

                link['down']=i
                link['up']=text=pageItem.page().find(page_rect)

                pen=QPen(QColor(88, 139, 174, 220), 0.0)
                painter.setPen(pen)
                painter.drawRect(transformed_rect)

                pen=QPen(Qt.red, 0.0)
                painter.setPen(pen)
                painter.drawText(transformed_rect.topLeft(), i)

            painter.restore()
