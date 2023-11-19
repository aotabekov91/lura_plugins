from plug.qt import Plug 
from gizmo.utils import tag

class WLookup(Plug):

    def setConnection(self):

        super().setConnection(kind='PULL')
        self.lookup = self.getConnection('PUSH')
        self.lookup.connect(f'tcp://localhost:{self.lookup_port}')

    @tag('ll', modes=['command'])
    def open(self):

        view=self.app.display.view
        if view and view.selected():
            text=[]
            for s in view.selected(): text+=[s['text']]
            text=' '.join(text)
            cmd={'action':'translate',
                 'lan':'en', 
                 'term': text}
            self.lookup.send_json(cmd)
