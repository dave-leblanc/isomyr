import pygame


class Keys(object):
    """keys class

    left, right, up, down, jump, pick_up, drop, examine, using: key codes for
        the player keys: key
    """
    def __init__(self, left=pygame.K_o, right=pygame.K_p, up=pygame.K_q,
                 down=pygame.K_a, jump=pygame.K_m, pick_up=pygame.K_g,
                 drop=pygame.K_d, examine=pygame.K_x, using=pygame.K_u):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.jump = jump
        self.pick_up = pick_up
        self.drop = drop
        self.examine = examine
        self.using = using
