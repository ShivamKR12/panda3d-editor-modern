import panda3d.core as pm
from direct.actor.Actor import Actor as P3dActor

from pandaEditor.game.nodes.constants import (
    TAG_ACTOR, TAG_MODEL_PATH, TAG_NODE_TYPE, TAG_NODE_UUID
)
from pandaEditor.game.nodes.modelroot import ModelRoot


class Actor(ModelRoot):
    def __init__(self, *args, **kwargs):
        """
        Initialize an Actor instance, extending ModelRoot.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Adds an 'Anims' attribute with getter and setter for animation dictionary.
        """
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            PyTagAttribute(
                'Anims',
                dict,
                self.GetAnimDict,
                self.SetAnimDict,
                pyTagName=TAG_ACTOR
            ),
            parent='Actor'
        )

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create a new Actor instance wrapping a Panda3D Actor.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Actor: A new Actor instance wrapping the Panda3D Actor.

        Logic:
            - Calls the superclass create method.
            - Sets various tags on the Panda3D Actor for identification.
            - Returns an Actor instance wrapping the geometry node.
        """
        wrpr = super(Actor, cls).create(*args, **kwargs)

        actor = P3dActor(wrpr.data)
        actor.setTag(TAG_NODE_TYPE, 'Actor')
        actor.setTag(TAG_NODE_UUID, wrpr.data.getTag(TAG_NODE_UUID))
        actor.setPythonTag(TAG_MODEL_PATH, str(wrpr.data.node().getFullpath()))
        actor.setPythonTag(TAG_ACTOR, actor)

        return cls(actor.getGeomNode())

    def duplicate(self):
        """
        Duplicate the Actor instance, including its animations.

        Returns:
            pm.GeomNode: The geometry node of the duplicated actor.

        Logic:
            - Duplicates the underlying ModelRoot.
            - Creates a new Panda3D Actor from the duplicate.
            - Copies tags and transforms.
            - Copies animations from the original to the duplicate.
        """
        dupeNp = ModelRoot.duplicate(self)

        actor = P3dActor(dupeNp)
        actor.setTag(TAG_NODE_TYPE, 'Actor')
        actor.setPythonTag(TAG_ACTOR, actor)
        actor.reparentTo(self.data.getParent())
        actor.setTransform(dupeNp.getTransform())
        actor.setName(dupeNp.getName())

        dupeNp.detachNode()

        # Copy animations over to the new actor.
        oldAnims = self.GetAnimDict(self.data.getPythonTag(TAG_ACTOR))
        self.SetAnimDict(actor, oldAnims)

        return actor.getGeomNode()

    def GetAnimDict(self, actor):
        """
        Retrieve the animation dictionary from a Panda3D Actor.

        Args:
            actor (P3dActor): The Panda3D Actor instance.

        Returns:
            dict: A dictionary mapping animation names to relative model paths.
        """
        animDict = {}
        for name in P3dActor.getAnimNames(actor):
            filePath = actor.getAnimFilename(name)
            animDict[name] = base.project.get_rel_model_path(filePath)

        return animDict

    def SetAnimDict(self, actor, animDict):
        """
        Set the animation dictionary on a Panda3D Actor.

        Args:
            actor (P3dActor): The Panda3D Actor instance.
            animDict (dict): A dictionary mapping animation names to file paths.

        Logic:
            - Removes existing animation controls.
            - Converts file paths to Panda3D Filename objects where possible.
            - Loads animations into the actor.
        """
        actor.removeAnimControlDict()

        myDict = {}
        for key, value in animDict.items():
            try:
                pandaPath = pm.Filename.fromOsSpecific(value)
            except TypeError:
                pandaPath = value
            myDict[key] = pandaPath

        actor.loadAnims(myDict)
