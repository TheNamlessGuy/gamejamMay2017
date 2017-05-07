#encoding: utf-8

class Keyboard:
    def __init__(self, pygame):
        self.keys_down = {}
        self.key_variables = {}

        self.key_variables['ctrl-up'] = [pygame.K_UP, pygame.K_w]
        self.key_variables['ctrl-down'] = [pygame.K_DOWN, pygame.K_s]
        self.key_variables['ctrl-left'] = [pygame.K_LEFT, pygame.K_a]
        self.key_variables['ctrl-right'] = [pygame.K_RIGHT, pygame.K_d]
        self.key_variables['ctrl-action'] = [pygame.K_SPACE]
        self.key_variables['ctrl-debug'] = [pygame.K_0]

        self.keys_down['ctrl-up'] = 0
        self.keys_down['ctrl-down'] = 0
        self.keys_down['ctrl-left'] = 0
        self.keys_down['ctrl-right'] = 0
        self.keys_down['ctrl-action'] = 0
        self.keys_down['ctrl-debug'] = 0

    def update(self, pygame):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False

            if event.type != pygame.KEYDOWN and event.type != pygame.KEYUP: continue
            for key in self.key_variables:
                if event.key in self.key_variables[key]:
                    self.keys_down[key] += 1 if event.type == pygame.KEYDOWN else -1
                    break

        return True

    def __getitem__(self, key):
        if key not in self.keys_down: return False
        return (self.keys_down[key] > 0)