class LEDSequence(dict):

    def __init__(self, list_steps, name="default"):
        super().__init__()
        self.current_step_index = 0
        self.list_steps = list_steps
        self.frequency = 2  # update n Hz
        self.name = name

        self.stop = True
        self.n_leds = 0

    def set_n_leds(self, n_leds):
        self.n_leds = n_leds

    def generate_step(self):
        pass

    def run(self):
        self.stop = False
        while not self.stop:
            step_values = self.list_steps[self.current_step_index % len(self.list_steps)]
            self.current_step_index += 1

            pass

    def stop(self):
        pass

    def restart(self):
        self.current_step_index = 0
        pass

    def increase_frequency(self):
        self.frequency *= 2

    def decrease_frequency(self):
        self.frequency /= 2
