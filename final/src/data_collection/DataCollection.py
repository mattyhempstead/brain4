
# Import and initialize the pygame library
import pygame, os, signal
import csv
import time
import numpy as np
from brainbox.BrainboxStream import BrainboxStream

from setting import *

from text import draw_text


from .Follow import Follow
from .KeyLogger import KeyLogger


class DataCollection:

    # The person being recorded
    # e.g. "Josh"
    PERSON = "Marcus"

    # The brainbox ID
    BRAINBOX_NUMBER = '0005'

    # Make sure you change this each time you move/restick the electrodes
    # e.g. 3
    ELECTRODE_PLACEMENT = 3

    # The time the data collection recording started
    # This lets us match up the wave and event files
    START_TIME = int(time.time())




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
        self.start_time = time.time()
        self.running = True

        self.key_logger = KeyLogger(
            person = DataCollection.PERSON,
            electrode_placement = DataCollection.ELECTRODE_PLACEMENT,
            brainbox_number = DataCollection.BRAINBOX_NUMBER,
            start_time = DataCollection.START_TIME,
        )

        self.brainbox_stream = BrainboxStream()

        self.follow = Follow()


        self.action_timer = 0
        self.action = None

        self.action_counter = {i:0 for i in DataCollection.ACTION_CHOICES}
        self.sample_counter = 0


    def start(self):
        self.clock = pygame.time.Clock()

        # First action appears after ACTION_TIMER_HIGH seconds
        self.action_timer = time.time() + DataCollection.ACTION_TIMER_HIGH

        while self.running:
            
            # brainbox_loop()
            # Get brainBox amplitude data (before downsampling)
            # Write to csv 
            data = self.brainbox_stream.read_amplitudes()
            if data is not None:
                self.key_logger.write_sample(data, self.brainbox_stream.Fs)
                self.sample_counter += len(data)

            # event handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.event_quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
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
            (WIDTH/2, 50),
            40,
            color = (150,150,150)
        )

        draw_text(
            "Press Q to quit",
            (WIDTH/2, 100),
            40,
            color = (150,150,150)
        )


        # Draw action counts
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

        # Sample counter
        draw_text(
            f"Sample: {self.sample_counter}",
            (20, 200),
            40,
            color = (150,150,150),
            center = False,
        )

        # Time
        draw_text(
            f"Recording time: {time.time() - self.start_time:.2f}s",
            (20, 250),
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

