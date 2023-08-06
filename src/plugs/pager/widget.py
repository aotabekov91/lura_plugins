from PyQt5 import QtWidgets, QtCore

class OverlayedWidget(QtWidgets.QLabel):

    def __init__(self, parent):
        super().__init__(parent)

        self.paddingBottom = 35
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet('''
            QLabel{
                color: white;
                border-radius: 15px;
                border-style: outset;
                background-color: black; 
                }
            ''')
        self.parent().installEventFilter(self)

    def updatePosition(self):

        if hasattr(self.parent(), 'viewport'):
            parent_rect = self.parent().viewport().rect()
        else:
            parent_rect = self.parent().rect()

        if not parent_rect: return

        pwidth=parent_rect.width()
        pheight=parent_rect.height()

        x=int(pwidth/2-self.width()/2)
        y=int(pheight-self.height()-self.paddingBottom)

        self.setGeometry(x, y, self.width(), self.height())

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.Resize
        if c1:
            if widget==self.parent():
                self.updatePosition()
                event.accept()
                return True
        return False
        
