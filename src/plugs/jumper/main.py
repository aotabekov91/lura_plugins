from tables import Jumper as Table

from qplug import PlugObj
from qplug.utils import register

class Leaper(PlugObj):

    # TODO
    def __init__(self, app):

        super(Leaper, self).__init__(app=app, 
                                     mode_keys={'command': 'j'})

        self.index=0
        self.jumps={}
        self.table=Table()
        self.app.main.display.itemChanged.connect(self.on_itemChanged)

    def on_itemChanged(self, view, item):

        left, top = view.saveLeftAndTop()
        data={'hash': view.model().hash(),
              'path': view.model().filePath(),
              'page': view.currentPage(), 
              'position': f'{left}:{top}'}

        if self.jumps.get(self.index, None)!=data:
            for i in range(len(self.jumps)-1, self.index, -1):
                self.jumps.pop(i)

        self.jumps[self.index]=data
        self.index+=1

    @register('p', modes=['normal', 'command'])
    def jump_prev(self): self.jump(increment=-1)

    @register('n', modes=['normal', 'command'])
    def jump_next(self): self.jump(increment=1)

    def jump(self, increment=1):

        self.index+=increment

        if self.index<0:
            self.index=0
        elif self.index>len(self.jumps)-1:
            self.index=len(self.jumps)-1

        data=self.jumps[self.index]
        pos=data['position'].split(':')
        left, top =float(pos[0]), float(pos[1])
        view=self.app.main.display.view
        view.goto(data['page'], left, top) 
