import pygame # type: ignore
import sys
import random

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("笨鸟先飞")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BIRD_SIZE = 40
BIRD_X = 100
GRAVITY = 0.5
FLAP_STRENGTH = -10

PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_SPEED = 5

def get_font(size):
    chinese_fonts = ['SimHei', 'SimSun', 'KaiTi', 'Microsoft YaHei', 'Arial Unicode MS']
    for font_name in chinese_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            return font
        except:
            continue
    try:
        font = pygame.font.Font(None, size)
    except:
        font = pygame.font.SysFont('arial', size)
    return font

class Bird:
    def __init__(self):
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(BIRD_X, self.y, BIRD_SIZE, BIRD_SIZE)
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > SCREEN_HEIGHT - BIRD_SIZE:
            self.y = SCREEN_HEIGHT - BIRD_SIZE
            self.velocity = 0
    
    def draw(self):
        pygame.draw.circle(SCREEN, RED, (self.rect.x + BIRD_SIZE // 2, self.rect.y + BIRD_SIZE // 2), BIRD_SIZE // 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, SCREEN_HEIGHT - 150 - PIPE_GAP)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)
        self.passed = False
    
    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
    
    def draw(self):
        pygame.draw.rect(SCREEN, GREEN, self.top_rect)
        pygame.draw.rect(SCREEN, GREEN, self.bottom_rect)

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_state = "start"
        self.clock = pygame.time.Clock()
        self.font = get_font(74)
        self.small_font = get_font(36)
        self.pipe_timer = 0
    
    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.pipe_timer = 0
    
    def spawn_pipe(self):
        if self.pipe_timer == 0:
            self.pipes.append(Pipe(SCREEN_WIDTH))
        self.pipe_timer = (self.pipe_timer + 1) % 60
    
    def check_collision(self):
        bird_rect = self.bird.rect
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe.top_rect) or bird_rect.colliderect(pipe.bottom_rect):
                return True
        return False
    
    def update_score(self):
        for pipe in self.pipes:
            if not pipe.passed and pipe.x + PIPE_WIDTH < BIRD_X:
                pipe.passed = True
                self.score += 1
    
    def run(self):
        self.p_pressed_last = False
        
        while True:
            SCREEN.fill(WHITE)
            
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_state == "start":
                            self.game_state = "playing"
                        elif self.game_state == "playing":
                            self.bird.flap()
                        elif self.game_state == "paused":
                            self.game_state = "playing"
                        elif self.game_state == "game_over":
                            self.reset()
                            self.game_state = "start"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == "start":
                        start_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 350, 200, 60)
                        if start_button_rect.collidepoint(mouse_pos):
                            self.game_state = "playing"
                    elif self.game_state == "playing":
                        pause_button_rect = pygame.Rect(SCREEN_WIDTH - 60, 10, 50, 30)
                        if pause_button_rect.collidepoint(mouse_pos):
                            self.game_state = "paused"
                    elif self.game_state == "paused":
                        resume_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, 300, 160, 50)
                        restart_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, 380, 160, 50)
                        if resume_button_rect.collidepoint(mouse_pos):
                            self.game_state = "playing"
                        elif restart_button_rect.collidepoint(mouse_pos):
                            self.reset()
                            self.game_state = "start"
                    elif self.game_state == "game_over":
                        restart_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, 380, 160, 50)
                        if restart_button_rect.collidepoint(mouse_pos):
                            self.reset()
                            self.game_state = "start"
            
            if keys[pygame.K_p] and not self.p_pressed_last:
                if self.game_state == "playing":
                    self.game_state = "paused"
                elif self.game_state == "paused":
                    self.game_state = "playing"
            self.p_pressed_last = keys[pygame.K_p]
            
            if self.game_state == "start":
                pygame.draw.circle(SCREEN, RED, (SCREEN_WIDTH//2, 280), BIRD_SIZE//2)
                
                start_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 350, 200, 60)
                pygame.draw.rect(SCREEN, GREEN, start_button_rect, border_radius=10)
                pygame.draw.rect(SCREEN, BLACK, start_button_rect, 3, border_radius=10)
                
                start_text = self.font.render("笨鸟先飞", True, BLACK)
                title_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, 180))
                SCREEN.blit(start_text, title_rect)
                
                start_button_text = self.small_font.render("开始游戏", True, BLACK)
                button_text_rect = start_button_text.get_rect(center=start_button_rect.center)
                SCREEN.blit(start_button_text, button_text_rect)
                
                hint_text = self.small_font.render("按空格键或点击按钮开始", True, (100, 100, 100))
                hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, 430))
                SCREEN.blit(hint_text, hint_rect)
            
            elif self.game_state == "playing":
                self.spawn_pipe()
                self.bird.update()
                self.bird.draw()
                
                for pipe in self.pipes[:]:
                    pipe.update()
                    pipe.draw()
                    if pipe.x + PIPE_WIDTH < 0:
                        self.pipes.remove(pipe)
                
                self.update_score()
                
                pause_button_rect = pygame.Rect(SCREEN_WIDTH - 60, 10, 50, 30)
                pygame.draw.rect(SCREEN, (200, 200, 200), pause_button_rect, border_radius=5)
                pygame.draw.rect(SCREEN, BLACK, pause_button_rect, 2, border_radius=5)
                pause_text = self.small_font.render("暂停", True, BLACK)
                pause_text_rect = pause_text.get_rect(center=pause_button_rect.center)
                SCREEN.blit(pause_text, pause_text_rect)
                
                score_display = self.small_font.render(f"分数: {self.score}", True, BLACK)
                SCREEN.blit(score_display, (10, 10))
                
                if self.check_collision() or self.bird.y >= SCREEN_HEIGHT - BIRD_SIZE:
                    self.game_state = "game_over"
            
            elif self.game_state == "paused":
                self.bird.draw()
                for pipe in self.pipes:
                    pipe.draw()
                
                resume_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, 300, 160, 50)
                pygame.draw.rect(SCREEN, GREEN, resume_button_rect, border_radius=10)
                pygame.draw.rect(SCREEN, BLACK, resume_button_rect, 3, border_radius=10)
                
                restart_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, 380, 160, 50)
                pygame.draw.rect(SCREEN, (255, 165, 0), restart_button_rect, border_radius=10)
                pygame.draw.rect(SCREEN, BLACK, restart_button_rect, 3, border_radius=10)
                
                paused_text = self.font.render("游戏暂停", True, BLACK)
                paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH//2, 200))
                SCREEN.blit(paused_text, paused_rect)
                
                resume_text = self.small_font.render("继续游戏", True, BLACK)
                resume_text_rect = resume_text.get_rect(center=resume_button_rect.center)
                SCREEN.blit(resume_text, resume_text_rect)
                
                restart_text = self.small_font.render("重新开始", True, BLACK)
                restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
                SCREEN.blit(restart_text, restart_text_rect)
                
                hint_text = self.small_font.render("按P键继续", True, (100, 100, 100))
                hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, 460))
                SCREEN.blit(hint_text, hint_rect)
                
                score_display = self.small_font.render(f"分数: {self.score}", True, BLACK)
                SCREEN.blit(score_display, (10, 10))
            
            elif self.game_state == "game_over":
                self.bird.draw()
                for pipe in self.pipes:
                    pipe.draw()
                
                restart_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, 350, 160, 50)
                pygame.draw.rect(SCREEN, GREEN, restart_button_rect, border_radius=10)
                pygame.draw.rect(SCREEN, BLACK, restart_button_rect, 3, border_radius=10)
                
                over_text = self.font.render("游戏结束", True, BLACK)
                over_rect = over_text.get_rect(center=(SCREEN_WIDTH//2, 200))
                SCREEN.blit(over_text, over_rect)
                
                score_text = self.small_font.render(f"最终得分: {self.score}", True, BLACK)
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 280))
                SCREEN.blit(score_text, score_rect)
                
                restart_text = self.small_font.render("重新开始", True, BLACK)
                restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
                SCREEN.blit(restart_text, restart_text_rect)
                
                hint_text = self.small_font.render("按空格键或点击按钮重新开始", True, (100, 100, 100))
                hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, 430))
                SCREEN.blit(hint_text, hint_rect)
                
                score_display = self.small_font.render(f"分数: {self.score}", True, BLACK)
                SCREEN.blit(score_display, (10, 10))
            
            else:
                score_display = self.small_font.render(f"分数: {self.score}", True, BLACK)
                SCREEN.blit(score_display, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"游戏出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")