import pygame
from pyengine.Exceptions import NoObjectError
from pyengine.Components import PositionComponent, SpriteComponent, TextComponent, ControlComponent
from pyengine import World
from pyengine.Entity import Entity
from pyengine.Utils import loggers, Colors

__all__ = ["EntitySystem"]


class EntitySystem:
    def __init__(self, world: World):
        self.world = world
        self.entities = pygame.sprite.Group()

    def get_entity(self, identity: int) -> Entity:
        for i in self.entities:
            if i.identity == identity:
                return i
        loggers.get_logger("PyEngine").warning("Try to get entity with id "+str(identity)+" but it doesn't exist")

    def add_entity(self, entity: Entity) -> Entity:
        if not isinstance(entity, Entity):
            raise TypeError("Argument is not type of "+str(Entity)+" but "+str(type(entity))+".")
        if not entity.has_component(PositionComponent):
            raise NoObjectError("Entity must have PositionComponent to be add in a world.")
        if not entity.has_component(SpriteComponent) and not entity.has_component(TextComponent):
            raise NoObjectError("Entity must have SpriteComponent or TextComponent to be add in a world.")
        if len(self.entities):
            entity.identity = self.entities.sprites()[-1].identity + 1
        else:
            entity.identity = 0
        self.entities.add(entity)
        entity.system = self
        return entity

    def has_entity(self, entity: Entity) -> bool:
        return entity in self.entities

    def remove_entity(self, entity: Entity) -> None:
        if entity in self.entities:
            self.entities.remove(entity)
        else:
            raise ValueError("Entity has not in EntitySystem")

    def update(self):
        for i in self.entities:
            i.update()

            from pyengine.Systems import CameraSystem
            if self.world.get_system(CameraSystem).entity_follow is None and i.has_component(PositionComponent):
                from pyengine import WindowCallbacks
                # Verify if entity is not out of window
                position = i.get_component(PositionComponent)
                if (position.position.y >= self.world.window.height - i.image.get_rect().height or
                        position.position.y < 0 or
                        position.position.x >= self.world.window.width - i.image.get_rect().width or
                        position.position.x < 0):
                    self.world.window.call(WindowCallbacks.OUTOFWINDOW, self, position.position)

    def stop_world(self):
        for i in self.entities:
            if i.has_component(ControlComponent):
                i.get_component(ControlComponent).keypressed = []

    def keypress(self, evt):
        for i in self.entities:
            if i.has_component(ControlComponent):
                i.get_component(ControlComponent).keypress(evt)

    def keyup(self, evt):
        for i in self.entities:
            if i.has_component(ControlComponent):
                i.get_component(ControlComponent).keyup(evt)

    def mousepress(self, evt):
        for i in self.entities:
            if i.has_component(ControlComponent):
                i.get_component(ControlComponent).mousepress(evt)

    def show(self, screen):
        self.entities.draw(screen)

    def show_debug(self, screen):
        for i in self.entities.sprites():
            render = self.world.window.debugfont.render("ID : "+str(i.identity), 1, Colors.RED.value.get())
            screen.blit(render, (i.rect.x + i.rect.width / 2 - render.get_width()/2, i.rect.y - 20))
