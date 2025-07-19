import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.game.nodes.attributes import Attribute
from pandaEditor.game.nodes.constants import TAG_MODEL_ROOT_CHILD
from pandaEditor.game.nodes.nodepath import NodePath


class ModelRoot(NodePath):
    """
    ModelRoot class extending NodePath, representing the root of a model hierarchy.

    Attributes:
        type_ (pc.ModelRoot): The Panda3D ModelRoot type.
        fullpath (Attribute): Attribute representing the full path of the model.
    """

    type_ = pc.ModelRoot
    fullpath = Attribute(
        pc.Filename,
        pc.ModelRoot.get_fullpath,
        required=True,
        node_data=True,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create a ModelRoot instance, optionally loading a model from a full path.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. Supports 'fullpath' to specify model path.

        Returns:
            ModelRoot: A new ModelRoot instance.

        Logic:
            - If 'fullpath' is provided, loads the model using Panda3D loader.
            - Calls superclass create method.
            - Sets the name of the data node based on the model's basename without extension.
            - (Commented out) Recurses over child nodes to create wrappers.
        """
        fullpath = kwargs.pop('fullpath', None)
        if fullpath is not None:
            panda_fullpath = pc.Filename.from_os_specific(fullpath)
            np = get_base().loader.load_model(panda_fullpath)
            kwargs['data'] = np

        comp = super().create(*args, **kwargs)
        fullpath = comp.data.node().get_fullpath()
        comp.data.set_name(fullpath.get_basename_wo_extension())

        # Iterate over child nodes
        # TBH I'm not even sure I know what this does.
        # comp.extraNps = []
        # def Recurse(node):
        #     nTypeStr = node.getTag(TAG_NODE_TYPE)
        #     cWrprCls = get_base().node_manager.get_component_by_name(nTypeStr)
        #     if cWrprCls is not None:
        #         cWrpr = cWrprCls.create(inputNp=node)
        #         comp.extraNps.append(cWrpr.data)
        #
        #     # Recurse
        #     for child in node.getChildren():
        #         Recurse(child)
        #
        # Recurse(comp.data)

        return comp

    def add_child(self, child):
        """
        Parent the indicated NodePath to the NodePath wrapped by this object.

        Args:
            child (NodePath): The child NodePath to parent.

        Notes:
            - NodePaths with the model root tag do not need to be reparented as they have correct hierarchy.
        """
        if not child.data.get_python_tag(TAG_MODEL_ROOT_CHILD):
            child.data.reparent_to(self.data)
