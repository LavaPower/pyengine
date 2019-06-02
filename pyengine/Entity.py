import pygame
from pyengine.Exceptions import WrongObjectError
from pyengine.Components import *
from pyengine.World import WorldCallbacks

__all__ = ["Entity"]


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super(Entity, self).__init__()
        self.identity = -1
        self.components = []
        self.attachedentities = []
        self.system = None
        self.image = None

    @property
    def identity(self):
        return self.__identity

    @identity.setter
    def identity(self, identity):
        self.__identity = identity

    @property
    def system(self):
        return self.__system

    @system.setter
    def system(self, system):
        self.__system = system

    def attach_entity(self, entity):
        self.attachedentities.append(entity)

    def add_component(self, component):
        found = False
        for i in [PositionComponent, SpriteComponent, ControlComponent, PhysicsComponent,
                  TextComponent, LifeComponent, MoveComponent]:
            if isinstance(component, i):
                found = True
                break
        if not found:
            raise WrongObjectError("Entity can't have "+str(component)+" as component.")
        component.entity = self
        self.components.append(component)
        return component

    def has_component(self, component):
        for i in self.components:
            if isinstance(i, component):
                return True
        return False

    def get_component(self, component):
        for i in self.components:
            if isinstance(i, component):
                return i

    def update(self):
        if self.has_component(PhysicsComponent):
            self.get_component(PhysicsComponent).update_gravity()

        if self.has_component(PositionComponent):
            # Verify if entity is not out of window
            position = self.get_component(PositionComponent)
            if position.y >= self.system.world.window.height - self.image.get_rect().height:
                self.system.world.call(WorldCallbacks.OUTOFWINDOW, self, position.position)
            elif position.y < 0:
                self.system.world.call(WorldCallbacks.OUTOFWINDOW, self, position.position)
            if position.x >= self.system.world.window.width - self.image.get_rect().width:
                self.system.world.call(WorldCallbacks.OUTOFWINDOW, self, position.position)
            elif position.x < 0:
                self.system.world.call(WorldCallbacks.OUTOFWINDOW, self, position.position)

        if self.has_component(ControlComponent):
            self.get_component(ControlComponent).update()

        if self.has_component(MoveComponent):
            self.get_component(MoveComponent).update()
