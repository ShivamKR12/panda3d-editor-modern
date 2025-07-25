import wx

from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.dragdroptarget import DragDropTarget
from pandaEditor.game.nodes.nodepath import NodePath
from pandaEditor import commands as cmds
from pandaEditor.ui.sceneGraphBasePanel import SceneGraphBasePanel
from wxExtra import utils as wxutils


class SceneGraphPanel(SceneGraphBasePanel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tc.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged)
        self.tc.Bind(wx.EVT_RIGHT_UP, self.on_right_up)

        # Build tree control drop target.
        dt = DragDropTarget(
            self.drag_drop_validate,
            self.on_drop
        )
        self.tc.SetDropTarget(dt)

    def on_right_up(self, evt):

        # Get the item under the mouse - bail if the item is not ok
        item = wxutils.get_clicked_item(self.tc, evt)
        if item is None or not item.IsOk():
            return

        menu = wx.Menu()
        m_item = wx.MenuItem(menu, wx.NewId(), 'Sort Children')
        menu.Append(m_item)
        wxutils.IdBind(
            menu,
            wx.EVT_MENU,
            m_item.GetId(),
            self.on_sort_children,
            item
        )
        self.PopupMenu(menu)
        menu.Destroy()

    def on_sort_children(self, evt, item):

        # TODO: Make undoable.
        comp = item.GetData()
        children = comp.children
        for child in children:
            child.detach()
        for child in sorted(children, key=lambda c: c.label):
            comp.add_child(child)
        get_base().doc.on_modified()

    def drag_drop_validate(self, x, y, data):
        item = self.tc.HitTest(wx.Point(x, y))[0]
        drop_ok = item is None or isinstance(item.GetData(), NodePath)
        drag_ok = all([isinstance(elem, NodePath) for elem in data])
        return drop_ok and drag_ok

    def on_drop(self, x, y, data):
        item = self.tc.HitTest(wx.Point(x, y))[0]
        parent = item.GetData() if item is not None else None
        cmds.parent(data, parent)
        
    def OnTreeSelChanged(self, evt):
        """
        Tree item selection handler. If the selection of the tree changes,
        tell the app to select those components.

        """
        def IndexInSelection(x, comps):
            """
            Sort components by their position in the selection, if they appear
            there. This will make the new selection order closer to the 
            original.

            """
            if x in get_base().selection.comps:
                i = get_base().selection.comps.index(x)
            else:
                i = len(get_base().selection.comps)
            return i
            
        items = self.GetValidSelections()
        if items:
            comps = [item.GetData() for item in items]
            comps.sort(key=lambda x: IndexInSelection(x, comps))
            cmds.select(comps)
            
    def OnUpdate(self, comps=None):
        """
        Update the TreeCtrl then hilight those items whose components are 
        selected.

        """
        self.tc.Freeze()
        super().OnUpdate(comps)

        items = [
            self._comps[comp] 
            for comp in get_base().selection.comps
            if comp in self._comps
        ]
        self.SelectItems(items)
        
        self.tc.Thaw()
