import typing

import pygame
import xmltodict

from PyGE.Screens.Room import Room
from PyGE.Errors import RoomNotDeclaredException, InvalidXMLException
from PyGE.Globals.Objects import PREMADE_OBJECTS

pygame.init()


class SideScroller:
    def __init__(self, screen: pygame.Surface, level_data:str, starting_room: str, custom_objects:typing.List):

        self.screen = screen
        self.level_data = level_data
        self.rooms = {}
        self.custom_objects = PREMADE_OBJECTS + custom_objects
        self.load_game()
        self.room = None

        self.set_room(starting_room)

    def load_game(self, level_data: str=None):
        if level_data is None:
            level_data = self.level_data

        self.level_data = level_data
        try:
            json = xmltodict.parse(level_data)
        except xmltodict.expat.ExpatError:
            raise InvalidXMLException("The XML Provided Is Invalid (Syntax Error?). Please Check The XML, And Try Again")
        building = json["building"]["room"]

        if "@name" in building:
            building = [building]
        for room in building:
            self.rooms[str(room["@name"])] = Room(self.screen, room, self.custom_objects, self)

    def update(self, events:list):
        self.room.update(events)

    def draw(self):
        self.room.draw()

    def set_room(self, room):
        if self.room is not None:
            self.room.leave_room(room)
        try:
            self.room = self.rooms[room]
        except KeyError:
            raise RoomNotDeclaredException(
                "The Specified Room '{}' Has Not Been Declared In The Provided XML. NOTE: Names Are Case Sensitive"
                    .format(room)
            )
        self.room.enter_room()

    def add_room(self, name):
        self.rooms[name] = Room(self.screen, {"@name": name}, self.custom_objects, self)
        return self.rooms[name]

    def delete_room(self, name):
        del self.rooms[name]

    def rename_room(self, old, new):
        self.rooms[new] = self.rooms[old]
        self.rooms[new].name = new
        self.delete_room(old)

    def reload_room(self, name:str):
        self.rooms[name].reload_room()

    def attempt_quit(self):
        if self.room.quit_action():
            quit()
