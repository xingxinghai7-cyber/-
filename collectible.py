import pygame # type: ignore
import random
import settings

class Collectible:
    def __init__(self, x, y, collectible_type="coin"):
        self.x = x
        self.y = y
        self.type = collectible_type
        self.collected = False
        
        self.size = 30
        self.value = 1
        self.color = settings.ORANGE
        self.effect = None
        
        if self.type == "coin":
            self.size = 30
            self.value = 1
            self.color = settings.ORANGE
            self.effect = None
        elif self.type == "slow":
            self.size = 35
            self.value = 0
            self.color = settings.BLUE
            self.effect = "slow"
        elif self.type == "fast":
            self.size = 35
            self.value = 0
            self.color = settings.PURPLE
            self.effect = "fast"
        elif self.type == "reverse":
            self.size = 35
            self.value = 0
            self.color = settings.PINK
            self.effect = "reverse"
        elif self.type == "double":
            self.size = 35
            self.value = 0
            self.color = settings.GOLD
            self.effect = "double"
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.image = None
        self.load_image()
    
    def load_image(self):
        try:
            self.image = pygame.image.load(f"assets/{self.type}.png")
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        except:
            self.image = None
    
    def update(self, speed):
        self.x -= speed
        self.rect.x = self.x
    
    def draw(self, screen):
        if not self.collected:
            if self.image:
                screen.blit(self.image, self.rect)
            else:
                if self.type == "coin":
                    pygame.draw.circle(screen, self.color, 
                                     (self.rect.x + self.size // 2, 
                                      self.rect.y + self.size // 2), 
                                     self.size // 2)
                    pygame.draw.circle(screen, (255, 215, 0), 
                                     (self.rect.x + self.size // 2, 
                                      self.rect.y + self.size // 2), 
                                     self.size // 2 - 3)
                else:
                    pygame.draw.polygon(screen, self.color, [
                        (self.rect.x + self.size // 2, self.rect.y),
                        (self.rect.x + self.size, self.rect.y + self.size // 2),
                        (self.rect.x + self.size // 2, self.rect.y + self.size),
                        (self.rect.x, self.rect.y + self.size // 2)
                    ])
                    if self.type == "slow":
                        pygame.draw.line(screen, settings.WHITE, 
                                       (self.rect.x + 5, self.rect.y + self.size // 2),
                                       (self.rect.x + self.size - 5, self.rect.y + self.size // 2), 2)
                    elif self.type == "fast":
                        pygame.draw.polygon(screen, settings.WHITE, [
                            (self.rect.x + 5, self.rect.y + self.size // 2),
                            (self.rect.x + self.size - 10, self.rect.y + 5),
                            (self.rect.x + self.size - 10, self.rect.y + self.size - 5)
                        ])
                    elif self.type == "reverse":
                        pygame.draw.line(screen, settings.WHITE,
                                       (self.rect.x + 5, self.rect.y + 5),
                                       (self.rect.x + self.size - 5, self.rect.y + self.size - 5), 3)
                        pygame.draw.line(screen, settings.WHITE,
                                       (self.rect.x + self.size - 5, self.rect.y + 5),
                                       (self.rect.x + 5, self.rect.y + self.size - 5), 3)
                    elif self.type == "double":
                        font = pygame.font.Font(None, 22)
                        double_text = font.render("2x", True, settings.WHITE)
                        screen.blit(double_text, (self.rect.x + 7, self.rect.y + 5))
    
    def check_collision(self, bird_rect):
        if not self.collected and self.rect.colliderect(bird_rect):
            self.collected = True
            return self.value, self.effect
        return 0, None

class CoinGenerator:
    def __init__(self):
        self.collectibles = []
        self.spawn_timer = 0
    
    def spawn_collectibles(self, pipe_x, pipe_gap_y, extended_mode=False):
        rand = random.random()
        coin_spawned = False
        
        if rand < 0.3:
            coin_y = pipe_gap_y + settings.PIPE_GAP // 2 - 15
            coin_x = pipe_x + settings.PIPE_WIDTH + 30
            self.collectibles.append(Collectible(coin_x, coin_y, "coin"))
            coin_spawned = True
        
        if extended_mode:
            buff_rand = random.random() if coin_spawned else rand
            
            if buff_rand < 0.2:
                buff_y = pipe_gap_y + settings.PIPE_GAP // 2 - 17
                buff_x = pipe_x + settings.PIPE_WIDTH + 70
                self.collectibles.append(Collectible(buff_x, buff_y, "slow"))
            elif buff_rand < 0.35:
                buff_y = pipe_gap_y + settings.PIPE_GAP // 2 - 17
                buff_x = pipe_x + settings.PIPE_WIDTH + 70
                self.collectibles.append(Collectible(buff_x, buff_y, "fast"))
            elif buff_rand < 0.5:
                buff_y = pipe_gap_y + settings.PIPE_GAP // 2 - 17
                buff_x = pipe_x + settings.PIPE_WIDTH + 70
                self.collectibles.append(Collectible(buff_x, buff_y, "reverse"))
            elif buff_rand < 0.6:
                buff_y = pipe_gap_y + settings.PIPE_GAP // 2 - 17
                buff_x = pipe_x + settings.PIPE_WIDTH + 70
                self.collectibles.append(Collectible(buff_x, buff_y, "double"))
    
    def update(self, bird_rect, speed):
        total_value = 0
        effects = []
        for collectible in self.collectibles[:]:
            collectible.update(speed)
            value, effect = collectible.check_collision(bird_rect)
            total_value += value
            if effect:
                effects.append(effect)
            if collectible.x + collectible.size < 0:
                self.collectibles.remove(collectible)
        return total_value, effects
    
    def draw(self, screen):
        for collectible in self.collectibles:
            collectible.draw(screen)
    
    def clear(self):
        self.collectibles = []
