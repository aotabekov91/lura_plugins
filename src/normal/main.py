from gizmo.utils import register
from plug.qt.plugs.modes import Normal as Base

class Normal(Base):

    @register(key='yy')
    def yank(self):

        view=self.currentView()
        if view and view.selected(): 
            t=[]
            for s in view.selected(): 
                t+=[s['text']]
            t=' '.join(t)
            self.app.clipboard().setText(t)
            view.select()

    @register(key='w')
    def fitToPageWidth(self): 

        view=self.currentView()
        if view: 
            view.fitToPageWidth()

    @register(key='s')
    def fitToPageHeight(self): 

        view=self.currentView()
        if view: 
            view.fitToPageHeight()

    @register(key='c')
    def toggleContinuousMode(self): 

        view=self.currentView()
        if view: 
            view.toggleContinuousMode()

    @register('C')
    def cleanUp(self): 

        view=self.currentView()
        if view: 
            view.cleanUp()
