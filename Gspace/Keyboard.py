#encoding: utf-8

class Keyboard:
    def __init__(self, pygame):
        self.keys_down = {}

        self.up_keys = [pygame.K_UP]
        self.down_keys = [pygame.K_DOWN]
        self.left_keys = [pygame.K_LEFT]
        self.right_keys = [pygame.K_RIGHT]
        self.action_keys = [pygame.K_SPACE]

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
            if event.key in self.up_keys:
                self.keys_down['ctrl-up'] += 1 if event.type == pygame.KEYDOWN else -1
            elif event.key in self.down_keys:
                self.keys_down['ctrl-down'] += 1 if event.type == pygame.KEYDOWN else -1
            elif event.key in self.left_keys:
                self.keys_down['ctrl-left'] += 1 if event.type == pygame.KEYDOWN else -1
            elif event.key in self.right_keys:
                self.keys_down['ctrl-right'] += 1 if event.type == pygame.KEYDOWN else -1
            elif event.key in self.action_keys:
                self.keys_down['ctrl-action'] += 1 if event.type == pygame.KEYDOWN else -1
            elif event.key == pygame.K_0:
                self.keys_down['ctrl-debug'] += 1 if event.type == pygame.KEYDOWN else -1

        return True

    def __getitem__(self, key):
        if key not in self.keys_down: return False
        return (self.keys_down[key] > 0)