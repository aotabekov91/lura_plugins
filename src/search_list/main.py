from PyQt5 import QtCore, QtGui

from plug.qt import Plug
from plug.qt.utils import register

from .widget import ListWidget

class SearchList(Plug):

    def setup(self):

        self.text_color='green'
        super().setup()
        self.display=self.app.window.main.display
        self.app.plugman.plugsLoaded.connect(
                self.on_plugsLoaded)
        self.setUI()

    def on_plugsLoaded(self, plugs):

        self.search=plugs.get('Search', None)

        if self.search:
            listener=self.search.event_listener
            listener.returnPressed.connect(
                    self.find)

    def jump(self, *args, **kwargs):

        self.searchJump(*args, **kwargs)
        idx=self.search.index
        self.ui.list.setCurrentRow(idx)

    def find(self):

        self.ui.model.clear()
        self.ui.proxy.clear()

        if self.search.matches:
            v=self.display.currentView()
            t=self.app.window.bar.edit.text()
            for f in self.search.matches:
                pn, r = f
                p=v.model().page(pn)
                t=self.getLine(t, p, r)
                l=QtGui.QStandardItem(t)
                self.ui.model.appendRow(l)
            self.ui.updatePosition()
            self.ui.show()

    def setUI(self):

        super().setUI(ui=ListWidget())
        self.ui.setParent(self.app.window)
        self.ui.hide()
        
    def getLine(self, text, page, rectF):

        w=page.size().width()
        lrec=QtCore.QRectF(
                0, rectF.y(), w, rectF.height())
        line=f'<html>{page.find(lrec)}</html>'
        rep=f'<font color="{self.text_color}">{text}</font>'
        return line.replace(text, rep)
