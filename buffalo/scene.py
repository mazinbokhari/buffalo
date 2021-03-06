__author__ = "Thomas Fischer"

import pygame

from buffalo import utils
from buffalo.label import Label
from buffalo.button import Button

class Scene(object):
    """
    Scene is a class which describes the procedure
    to update
    """

    def __init__(self):
        """
        This the constructor of Scene. It comes
        with a background color and three fairly
        intuitive sets.
        """
        self.BACKGROUND_COLOR = (25, 150, 25, 255)
        self.labels = set()
        self.buttons = set()
        self.options = set()
        self.inputs = set()
        self.trays = set()
        self.mouse_pos = (0, 0)
        self.mouse_rel = (0, 0)
        self.click_pos = (0, 0)
        self.mouse_buttons = [0, 0, 0]

    def on_escape(self):
        """
        This method is called when the escape key
        is pressed.
        """
        raise NotImplementedError

    def logic(self):
        """
        This method handles all keyboard and mouse input.
        It detects if buttons are clicked, etc.
        """
        self.mouse_rel = pygame.mouse.get_rel()
        self.mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                utils.end = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.on_escape()
                else:
                    for inpt in self.inputs:
                        if inpt.selected:
                            inpt.process_char( event.key )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_buttons[0] = True
                self.click_pos = self.mouse_pos

                x, y = self.mouse_pos
                for tray in self.trays:
                    for button in tray.buttons:
                        if button.get_rect().collidepoint( (x - tray.x, y - tray.y) ):
                            button.set_selected(True)
                            button.blit(tray.surface)
                    for option in tray.options:
                        if option.get_left_rect().collidepoint( (x - tray.x, y - tray.y) ):
                            option.set_left_selected(True)
                            option.blit(tray.surface)
                        if option.get_right_rect().collidepoint( (x - tray.x, y - tray.y) ):
                            option.set_right_selected(True)
                            option.blit(tray.surface)

                for button in self.buttons:
                    if button.get_rect().collidepoint( self.mouse_pos ):
                        button.set_selected(True)
                for option in self.options:
                    if option.get_left_rect().collidepoint( self.mouse_pos ):
                        option.set_left_selected(True)
                        if option.get_right_rect().collidepoint( self.mouse_pos ):
                            option.set_right_selected(True)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_buttons[0] = False

                x, y = self.mouse_pos
                for tray in self.trays:
                    for button in tray.buttons:
                        button.set_selected(False)
                        button.blit(tray.surface)
                        if button.get_rect().collidepoint( (x - tray.x, y - tray.y) ):
                            if button.func is not None:
                                button.func()
                    for inpt in tray.inputs:
                        if inpt.get_rect().collidepoint( (x - tray.x, y - tray.y) ):
                            inpt.select()
                        else:
                            inpt.deselect()
                    for option in tray.options:
                        if option.get_left_rect().collidepoint( (x - tray.x, y - tray.y) ):
                            option.go_left()
                            option.blit(tray.surface)
                        if option.get_right_rect().collidepoint( (x - tray.x, y - tray.y) ):
                            option.go_right()
                            option.blit(tray.surface)
                
                for button in self.buttons:
                    button.set_selected(False)
                    if button.get_rect().collidepoint( self.mouse_pos ):
                        if button.func is not None:
                            button.func()
                for inpt in self.inputs:
                    if inpt.get_rect().collidepoint( self.mouse_pos ):
                        inpt.select()
                    else:
                        inpt.deselect()
                for option in self.options:
                    if option.get_left_rect().collidepoint( self.mouse_pos ):
                        option.go_left()
                    if option.get_right_rect().collidepoint( self.mouse_pos ):
                        option.go_right()

    def update(self):
        """
        update is called a certain number of times every
        second. Its intention is to update the state of
        the program (if Pong was implemented with Buffalo,
        the ball's position would be updated here).
        It is important to note that this method contains
        code that will be executed *independent*
        of the program's framerate, so the program's
        update speed does not vary between computers.
        """
        if self.mouse_buttons[0]:
            for tray in self.trays:
                tray.handle(self.mouse_pos, self.mouse_rel, self.click_pos)
        else:
            for tray in self.trays:
                tray.should_move = False
                tray.should_resize = False
                tray.edge = 0b0000


    def blit(self):
        """
        This is the method in which everything that is
        NOT a Buffalo objcet should be drawn.
        """
        raise NotImplementedError

    def render(self):
        """
        This method SHOULD NOT be overridden.
        It clears the display, draws all Buffalo
        objects (Labels, Button,s Options, Inputs),
        calls self.blit (this is probably what
        you're looking for), and then updates
        the display.
        """
        utils.screen.fill( self.BACKGROUND_COLOR )
        self.blit()

        for label in self.labels:
            label.blit(utils.screen)
        for button in self.buttons:
            button.blit(utils.screen)
        for option in self.options:
            option.blit(utils.screen)
        for inpt in self.inputs:
            inpt.blit(utils.screen)
        for tray in self.trays:
            tray.blit(utils.screen)

        pygame.display.update()
