from pandaEditor.game.nodes.actor import Actor
from pandaEditor.game.nodes.base import Base
from pandaEditor.game.nodes.bullet import (
    BulletBoxShape,
    BulletCapsuleShape,
    BulletDebugNode,
    BulletPlaneShape,
    BulletRigidBodyNode,
    BulletSphereShape,
    BulletWorld,
)
from pandaEditor.game.nodes.camera import Camera
from pandaEditor.game.nodes.collision import (
    CollisionBox,
    CollisionCapsule,
    CollisionInvSphere,
    CollisionNode,
    CollisionRay,
    CollisionSphere,
)
from pandaEditor.game.nodes.constants import TAG_NODE_TYPE
from pandaEditor.game.nodes.fog import Fog
from pandaEditor.game.nodes.lensnode import LensNode
from pandaEditor.game.nodes.lights import (
    AmbientLight,
    DirectionalLight,
    PointLight,
    Spotlight
)
from pandaEditor.game.nodes.modelnode import ModelNode
from pandaEditor.game.nodes.modelroot import ModelRoot
from pandaEditor.game.nodes.nodepath import NodePath
from pandaEditor.game.nodes.nongraphobject import NonGraphObject
from pandaEditor.game.nodes.pandanode import PandaNode
from pandaEditor.game.nodes.particleeffect import ParticleEffect
from pandaEditor.game.nodes.sceneroot import SceneRoot
from pandaEditor.game.nodes.showbasedefaults import (
    Aspect2d,
    BaseCam,
    BaseCamera,
    Cam2d,
    Camera2d,
    Pixel2d,
    Render,
    Render2d,
)
from pandaEditor.game.nodes.texture import Texture


class Manager:
    def __init__(self):
        """
        Initialize the Manager with a dictionary mapping component type names
        to their corresponding wrapper classes.

        Attributes:
            wrappers (dict): Mapping of component type names (str) to wrapper classes.
        """
        self.wrappers = {
            'Actor': Actor,
            'AmbientLight': AmbientLight,
            'Aspect2d': Aspect2d,
            'Base': Base,
            'BaseCam': BaseCam,
            'BaseCamera': BaseCamera,
            'BulletBoxShape': BulletBoxShape,
            'BulletCapsuleShape': BulletCapsuleShape,
            'BulletDebugNode': BulletDebugNode,
            'BulletPlaneShape': BulletPlaneShape,
            'BulletSphereShape': BulletSphereShape,
            'BulletRigidBodyNode': BulletRigidBodyNode,
            'BulletWorld': BulletWorld,
            'Cam2d': Cam2d,
            'Camera': Camera,
            'Camera2d': Camera2d,
            'CollisionBox': CollisionBox,
            'CollisionCapsule': CollisionCapsule,
            'CollisionInvSphere': CollisionInvSphere,
            'CollisionNode': CollisionNode,
            'CollisionRay': CollisionRay,
            'CollisionSphere': CollisionSphere,
            'DirectionalLight': DirectionalLight,
            'Fog': Fog,
            'LensNode': LensNode,
            'ModelNode': ModelNode,
            'ModelRoot': ModelRoot,
            'NodePath': NodePath,
            'NonGraphObject': NonGraphObject,
            'PandaNode': PandaNode,
            'ParticleEffect': ParticleEffect,
            'Pixel2d': Pixel2d,
            'PointLight': PointLight,
            'Render': Render,
            'Render2d': Render2d,
            'SceneRoot': SceneRoot,
            'Spotlight': Spotlight,
            'Texture': Texture,
        }

    def wrap(self, obj):
        """
        Return a wrapper instance suitable for the given object.

        Args:
            obj (object): The object to wrap.

        Returns:
            object: An instance of the appropriate wrapper class for the object.

        Notes:
            - If a specific wrapper class is found for the object's type, it is used.
            - If no specific wrapper is found, returns a NodePath wrapper for NodePath objects,
              or a Base wrapper for all other objects.
        """
        comp_cls = self.get_wrapper(obj)
        if comp_cls is not None:
            return comp_cls(obj)
        else:
            comp_cls = self.get_default_wrapper(obj)
            return comp_cls(obj)

    def get_wrapper(self, obj):
        """
        Get the wrapper class for the given object based on its type string.

        Args:
            obj (object): The object to get the wrapper class for.

        Returns:
            class or None: The wrapper class if found, else None.
        """
        type_ = self.get_type_string(obj)
        return self.wrappers.get(type_)

    def get_component_by_name(self, c_type):
        """
        Get the wrapper class by its component type name.

        Args:
            c_type (str): The component type name.

        Returns:
            class or None: The wrapper class if found, else None.
        """
        return self.wrappers.get(c_type)

    def get_type_string(self, comp):
        """
        Determine the type string of a component.

        Args:
            comp (object): The component instance.

        Returns:
            str: The type string of the component.

        Logic:
            - If the component class has a 'cType' attribute, return it.
            - Otherwise, use the class name of the component.
            - If the type is 'NodePath', check for an overriding tag on the node.
            - If the tag is missing, use the class name of the node.
        """
        if hasattr(comp.__class__, 'cType'):
            return comp.cType

        type_str = type(comp).__name__
        if type_str == 'NodePath':
            type_str = comp.node().get_tag(TAG_NODE_TYPE)
            if not type_str:
                type_str = type(comp.node()).__name__
        return type_str
