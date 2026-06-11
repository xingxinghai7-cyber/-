import pygame # type: ignore
import random
import settings

PIPE_TOP_SCALED = None
PIPE_BOTTOM_SCALED = None

def load_pipe_images():
    global PIPE_TOP_SCALED, PIPE_BOTTOM_SCALED
    try:
        original = pygame.image.load("assets/pipe_top.png").convert_alpha()
        original_width = original.get_width()
        original_height = original.get_height()
        scale_ratio = settings.PIPE_WIDTH / original_width
        new_height = int(original_height * scale_ratio)
        PIPE_TOP_SCALED = pygame.transform.smoothscale(original, (settings.PIPE_WIDTH, new_height))
    except:
        PIPE_TOP_SCALED = None
    
    try:
        original = pygame.image.load("assets/pipe_bottom.png").convert_alpha()
        original_width = original.get_width()
        original_height = original.get_height()
        scale_ratio = settings.PIPE_WIDTH / original_width
        new_height = int(original_height * scale_ratio)
        PIPE_BOTTOM_SCALED = pygame.transform.smoothscale(original, (settings.PIPE_WIDTH, new_height))
    except:
        PIPE_BOTTOM_SCALED = None

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, settings.SCREEN_HEIGHT - 150 - settings.PIPE_GAP)
        self.top_rect = pygame.Rect(self.x, 0, settings.PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + settings.PIPE_GAP, 
                                      settings.PIPE_WIDTH, 
                                      settings.SCREEN_HEIGHT - self.height - settings.PIPE_GAP)
        self.passed = False
    
    def update(self, speed):
        self.x -= speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
    
    def draw(self, screen):
        if PIPE_TOP_SCALED:
            screen.blit(PIPE_TOP_SCALED, (self.top_rect.x, self.top_rect.bottom - PIPE_TOP_SCALED.get_height()))
        else:
            pygame.draw.rect(screen, settings.GREEN, self.top_rect)
        
        if PIPE_BOTTOM_SCALED:
            screen.blit(PIPE_BOTTOM_SCALED, (self.bottom_rect.x, self.bottom_rect.top))
        else:
            pygame.draw.rect(screen, settings.GREEN, self.bottom_rect)
