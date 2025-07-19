import panda3d.core as pm

from pandaEditor.game.nodes.nodepath import NodePath
from pandaEditor.game.nodes.componentmetaclass import ComponentMetaClass


class ModelNode(NodePath, metaclass=ComponentMetaClass):
    
    type_ = pm.ModelNode
