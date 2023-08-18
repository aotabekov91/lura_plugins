from plug.qt import PlugObj 
from plug.qt.utils import register

class Lookup(PlugObj):

    def setConnection(self):

        super().setConnection(kind='PULL')
        self.lookup = self.getConnection('PUSH')
        self.lookup.connect(f'tcp://localhost:{self.lookup_port}')

    @register('ll', modes=['command'])
    def open(self):

        view=self.app.main.display.view
        if view and view.selected():

            text=[]
            for s in view.selected(): text+=[s['text']]
            text=' '.join(text)

            cmd={'action':'translate',
                 'lan':'en', 
                 'term': text}

            print(cmd)
            self.lookup.send_json(cmd)
