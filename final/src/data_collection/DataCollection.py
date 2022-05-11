
# Import and initialize the pygame library
import pygame, os, signal
import csv
import time
import numpy as np

from setting import *

from text import draw_text

from brainbox.brainbox import brainbox_loop

from .Follow import Follow
from .KeyLogger import KeyLogger


class DataCollection:

    # The person being recorded
    # e.g. "Josh"
    PERSON = "Josh"

    # Make sure you change this each time you move the electrodes
    # e.g. 3
    ELECTRODE_PLACEMENT = 0




    BACKGROUND_COLOR = LIGHT_GREY

    # Time between action selections
    ACTION_TIMER_LOW = 0.5
    ACTION_TIMER_HIGH = 5
    ACTION_TIMER_LENGTH = ACTION_TIMER_HIGH - ACTION_TIMER_LOW

    # Time to prepare user to perform action
    ACTION_COUNTDOWN = 1


    ACTION_CHOICES = ["L","R","S"]
    ACTION_NAME_MAP = {
        None: None,
        "L": "Left Wink",
        "R": "Right Wink",
        "S": "Double Blink",
    }


    def __init__(self):
        self.running = True

        self.key_logger = KeyLogger(
            person = DataCollection.PERSON,
            electrode_placement = DataCollection.ELECTRODE_PLACEMENT,
        )

        self.follow = Follow()


        self.action_timer = 0
        self.action = None

        self.action_counter = {i:0 for i in DataCollection.ACTION_CHOICES}


    def start(self):
        self.clock = pygame.time.Clock()

        # First action appears after ACTION_TIMER_HIGH seconds
        self.action_timer = time.time() + DataCollection.ACTION_TIMER_HIGH

        while self.running:
            
            # brainbox_loop()

            # event handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.event_quit()

            self.update()
            self.render()

            if FPS is not None:
                self.clock.tick(FPS)

        # Done! Time to quit.
        pygame.quit()

        self.key_logger.close()


    def event_quit(self):
        self.running = False

    @property
    def action_name(self):
        return DataCollection.ACTION_NAME_MAP[self.action]

    def update(self):
        if time.time() < self.action_timer:
            return        
        self.action_timer = time.time()

        if self.action is None:
            self.action_start()
        else:
            self.action_end()


    def action_start(self):
        """ Pick an action and begin a countdown """
        self.action_timer += DataCollection.ACTION_COUNTDOWN

        self.action = np.random.choice(DataCollection.ACTION_CHOICES)

        print(f"Picked action {self.action}, waiting for {DataCollection.ACTION_COUNTDOWN}s")


    def action_end(self):
        """ Log the action and go back to waiting for an action to start """
        self.key_logger.write(self.action, self.action_name)
        print(f"Action {self.action} completed and logged.")

        self.action_counter[self.action] += 1
        self.action = None

        # Reset action timer
        self.action_timer += DataCollection.ACTION_TIMER_LOW
        self.action_timer += DataCollection.ACTION_TIMER_LENGTH*np.random.random()



    def render(self):

        # fill the background with white
        SCREEN.fill(DataCollection.BACKGROUND_COLOR)

        # draw the text input box
        draw_text(
            "Keep looking at the circle do what it says pls",
            (WIDTH/2, 100),
            40,
            color = (150,150,150)
        )


        for i,c in enumerate(DataCollection.ACTION_CHOICES):
            ac = self.action_counter[c]
            an = DataCollection.ACTION_NAME_MAP[c]
            draw_text(
                f"{an} ({c}): {ac}",
                (20, 20 + 50*i),
                40,
                color = (150,150,150),
                center = False,
            )


        # Add action countdown
        self.follow.set_action(self.action_name)
        self.follow.set_action_countdown(self.action_timer - time.time())

        self.follow.render()


        # Flip the display
        pygame.display.flip()

