from hutil.Qt import QtCore
from hutil.Qt import QtWidgets
from hutil.Qt import _loadUi as uic

import hou
import os


class NodeStore(QtWidgets.QWidget):
    """
    A helper for exchangin houdini nodes.
    """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        UI_FILE = os.sep.join((os.path.dirname(os.path.abspath(__file__)), 'resources/nodeStore_main.ui'))

        self.ui = uic(UI_FILE, self)
        self.server_location = "P:\hou_share"
        self.extension = ".txt"

        self._get_stores()
        self.ui.btn_save.clicked.connect(self._store_nodes)
        self.ui.ln_serverLocation.setText(self.server_location)

        self.setObjectName("Node_Store")

    def _get_stores(self):
        saves = []
        self.ui.lst_saves.clear()

        for f in os.listdir(self.server_location):
            if f.endswith(self.extension):
                saves.append(f)

        return self.ui.lst_saves.addItems(saves)

    def _store_nodes(self):
        store_name = self.ui.ln_name.text()
        nodes = hou.selectedNodes()
        if nodes:
            for node in nodes:
                with open(os.path.join(self.server_location, "{}{}".format(store_name, self.extension)), "w") as node_desc:
                    node_desc.write(node.asCode(recurse=True))
                # print node.asCode()
        self._get_stores()

    def closeEvent(self, event):
        self.setParent(None)



dialog = hou.qt.mainWindow().findChild(QtWidgets.QWidget, "Node_Store")

if dialog:
    dialog.activateWindow()
else:
    dialog = NodeStore()
    dialog.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
    dialog.show()

