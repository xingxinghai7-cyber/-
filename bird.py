import pygame # type: ignore
import settings

class Bird:
    def __init__(self):
        self.y = settings.SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(settings.BIRD_X, self.y, settings.BIRD_SIZE, settings.BIRD_SIZE)
        self.image = None
        self.image_width = 0
        self.load_image()
    
    def load_image(self):
        try:
            self.image = pygame.image.load("assets/bird.png").convert_alpha()
            original_width = self.image.get_width()
            original_height = self.image.get_height()
            scale_ratio = settings.BIRD_SIZE / original_height
            self.image_width = int(original_width * scale_ratio)
            self.image = pygame.transform.smoothscale(self.image, (self.image_width, settings.BIRD_SIZE))
        except:
            self.image = None
            self.image_width = settings.BIRD_SIZE
    
    def flap(self):
        self.velocity = settings.FLAP_STRENGTH
    
    def update(self):
        self.velocity += settings.GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > settings.SCREEN_HEIGHT - settings.BIRD_SIZE:
            self.y = settings.SCREEN_HEIGHT - settings.BIRD_SIZE
            self.velocity = 0
    
    def draw(self, screen):
        if self.image:
            image_x = self.rect.right - self.image_width
            screen.blit(self.image, (image_x, self.rect.y))
        else:
            pygame.draw.circle(screen, settings.RED, 
                             (self.rect.x + settings.BIRD_SIZE // 2, 
                              self.rect.y + settings.BIRD_SIZE // 2), 
                             settings.BIRD_SIZE // 2)
