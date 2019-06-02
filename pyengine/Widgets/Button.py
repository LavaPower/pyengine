import pygame
from pyengine.Widgets.Widget import Widget
from pyengine.Widgets import Label

__all__ = ["Button"]


class Button(Widget):
    def __init__(self, position, text, command=None, size=None, image=None):
        super(Button, self).__init__(position)

        if size is None:
            size = [100, 40]
        if image is None:
            image = pygame.Surface(size)
            image.fill((50, 50, 50))
        else:
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, size)

        self.image = image
        self.rect = self.image.get_rect()
        self.label = Label(position, text)
        self.label.parent = self
        self.position = position
        self.size = size
        self.command = command
        self.update_render()

    def get_label(self):
        return self.label

    def update_render(self):
        self.update_rect()
        self.label.position = [self.rect.x+self.rect.width/2-self.label.rect.width/2,
                               self.rect.y+self.rect.height/2-self.label.rect.height/2]

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size
        self.image = pygame.transform.scale(self.image, size)
        self.update_render()

    @property
    def command(self):
        return self.__command

    @command.setter
    def command(self, command):
        self.__command = command

    @property
    def system(self):
        return self.__system

    @system.setter
    def system(self, system):
        self.__system = system
        system.add_widget(self.label)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.label.position = [self.rect.x+self.rect.width/2-self.label.rect.width/2,
                               self.rect.y+self.rect.height/2-self.label.rect.height/2]

    def mousepress(self, evt):
        if self.rect.x <= evt.pos[0] <= self.rect.x + self.rect.width and self.rect.y <= evt.pos[1] <= self.rect.y +\
                self.rect.height and self.command:
            self.command(self, evt.button)
            return True


