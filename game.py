import pygame
import sys
from bird import Bird
from pipe import Pipe
from ui import UI
from collectible import CoinGenerator
import settings

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_state = "menu"
        self.game_mode = "normal"
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.p_pressed_last = False
        self.coin_generator = CoinGenerator()
        
        self.active_buffs = {}
        self.buff_end_times = {}
        self.current_gravity = settings.GRAVITY
        self.current_pipe_speed = settings.PIPE_SPEED
        self.pipe_spawn_distance = 300
        
        self.flash_screen = False
        self.flash_start_time = 0
        self.normal_high_score = 0
        self.extended_high_score = 0
        self.new_record = False
        
        self.countdown_start_time = 0
        self.countdown_duration = 3000
        
        self.game_over_start_time = 0
        
        self.pause_start_time = 0
    
    def get_current_high_score(self):
        if self.game_mode == "extended":
            return self.extended_high_score
        return self.normal_high_score
    
    def set_current_high_score(self, score):
        if self.game_mode == "extended":
            self.extended_high_score = score
        else:
            self.normal_high_score = score
    
    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.new_record = False
        self.coin_generator.clear()
        self.active_buffs = {}
        self.buff_end_times = {}
        self.current_gravity = settings.GRAVITY
        self.current_pipe_speed = settings.PIPE_SPEED
        self.pipe_spawn_distance = 300
        if self.game_mode == "extended":
            self.current_pipe_speed = settings.EXTENDED_PIPE_SPEED
    
    def activate_buff(self, buff_type):
        current_time = pygame.time.get_ticks()
        
        if buff_type in ["slow", "fast"]:
            if "slow" in self.active_buffs:
                del self.active_buffs["slow"]
                del self.buff_end_times["slow"]
            if "fast" in self.active_buffs:
                self.clear_front_pipes()
                del self.active_buffs["fast"]
                del self.buff_end_times["fast"]
        
        if buff_type == "reverse":
            self.clear_front_pipes()
            self.flash_screen = True
            self.flash_start_time = pygame.time.get_ticks()
            return
        
        self.active_buffs[buff_type] = True
        self.buff_end_times[buff_type] = current_time + settings.BUFF_DURATION
        
        if buff_type == "slow":
            self.current_pipe_speed = settings.SLOW_SPEED
        elif buff_type == "fast":
            self.current_pipe_speed = settings.FAST_SPEED
        elif buff_type == "double":
            pass
    
    def clear_pipes_and_score(self):
        multiplier = 2 if "double" in self.active_buffs else 1
        for pipe in self.pipes:
            if not pipe.passed:
                self.score += 1 * multiplier
        self.pipes.clear()
        self.coin_generator.clear()
    
    def clear_front_pipes(self):
        multiplier = 2 if "double" in self.active_buffs else 1
        sorted_pipes = sorted(self.pipes, key=lambda p: p.x, reverse=True)
        for i, pipe in enumerate(sorted_pipes[:3]):
            if pipe in self.pipes:
                self.pipes.remove(pipe)
                if not pipe.passed:
                    self.score += 2 * multiplier
    
    def update_buffs(self):
        current_time = pygame.time.get_ticks()
        buffs_to_remove = []
        
        for buff_type, end_time in self.buff_end_times.items():
            if current_time >= end_time:
                buffs_to_remove.append(buff_type)
        
        for buff_type in buffs_to_remove:
            if buff_type == "fast":
                self.clear_front_pipes()
                self.flash_screen = True
                self.flash_start_time = pygame.time.get_ticks()
            del self.active_buffs[buff_type]
            del self.buff_end_times[buff_type]
        
        if "slow" not in self.active_buffs and "fast" not in self.active_buffs:
            if self.game_mode == "extended":
                self.current_pipe_speed = settings.EXTENDED_PIPE_SPEED
            else:
                self.current_pipe_speed = settings.PIPE_SPEED
    
    def spawn_pipe(self):
        if self.pipes:
            last_pipe = self.pipes[-1]
            if settings.SCREEN_WIDTH - last_pipe.x >= self.pipe_spawn_distance:
                new_pipe = Pipe(settings.SCREEN_WIDTH)
                self.pipes.append(new_pipe)
                self.coin_generator.spawn_collectibles(new_pipe.x, new_pipe.height, self.game_mode == "extended")
        else:
            new_pipe = Pipe(settings.SCREEN_WIDTH)
            self.pipes.append(new_pipe)
            self.coin_generator.spawn_collectibles(new_pipe.x, new_pipe.height, self.game_mode == "extended")
    
    def check_collision(self):
        bird_rect = self.bird.rect
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe.top_rect) or bird_rect.colliderect(pipe.bottom_rect):
                if "fast" in self.active_buffs:
                    self.pipes.remove(pipe)
                    if not pipe.passed:
                        multiplier = 2 if "double" in self.active_buffs else 1
                        self.score += 1 * multiplier
                else:
                    return True
        return False
    
    def update_score(self):
        multiplier = 2 if "double" in self.active_buffs else 1
        for pipe in self.pipes:
            if not pipe.passed and pipe.x + settings.PIPE_WIDTH < settings.BIRD_X:
                pipe.passed = True
                self.score += 1 * multiplier
    
    def run(self):
        while True:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.game_state == "menu":
                    self.ui.get_normal_button().handle_event(event)
                    self.ui.get_extended_button().handle_event(event)
                    self.ui.get_help_button().handle_event(event)
                elif self.game_state == "start":
                    self.ui.get_start_button().handle_event(event)
                    self.ui.get_help_button().handle_event(event)
                elif self.game_state == "playing":
                    self.ui.get_pause_button().handle_event(event)
                elif self.game_state == "paused":
                    self.ui.get_resume_button().handle_event(event)
                    self.ui.get_restart_button().handle_event(event)
                    self.ui.get_menu_button().handle_event(event)
                elif self.game_state == "game_over":
                    self.ui.get_restart_button(420).handle_event(event)
                    self.ui.get_game_over_menu_button().handle_event(event)
                elif self.game_state == "help":
                    self.ui.get_help_button().handle_event(event)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_state == "start":
                            self.game_state = "playing"
                        elif self.game_state == "playing":
                            if "reverse" in self.active_buffs:
                                self.bird.velocity = -settings.FLAP_STRENGTH
                            else:
                                self.bird.flap()
                        elif self.game_state == "paused":
                            self.game_state = "playing"
                        elif self.game_state == "game_over":
                            if pygame.time.get_ticks() - self.game_over_start_time >= 1000:
                                self.reset()
                                self.countdown_start_time = pygame.time.get_ticks()
                                self.game_state = "countdown"
                        elif self.game_state == "help":
                            self.game_state = "menu"
                    elif event.key == pygame.K_ESCAPE:
                        if self.game_state == "help":
                            self.game_state = "menu"
                
                if event.type == pygame.MOUSEWHEEL:
                    if self.game_state == "help":
                        self.ui.scroll_help(event.y)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == "menu":
                        if self.ui.get_normal_button().collidepoint(mouse_pos):
                            self.game_mode = "normal"
                            self.reset()
                            self.countdown_start_time = pygame.time.get_ticks()
                            self.game_state = "countdown"
                        elif self.ui.get_extended_button().collidepoint(mouse_pos):
                            self.game_mode = "extended"
                            self.reset()
                            self.countdown_start_time = pygame.time.get_ticks()
                            self.game_state = "countdown"
                        elif self.ui.get_help_button().collidepoint(mouse_pos):
                            self.ui.help_scroll_offset = 0
                            self.game_state = "help"
                    elif self.game_state == "start":
                        if self.ui.get_start_button().collidepoint(mouse_pos):
                            self.game_state = "playing"
                        elif self.ui.get_help_button().collidepoint(mouse_pos):
                            self.ui.help_scroll_offset = 0
                            self.game_state = "help"
                    elif self.game_state == "playing":
                        if self.ui.get_pause_button().collidepoint(mouse_pos):
                            self.pause_start_time = pygame.time.get_ticks()
                            self.game_state = "paused"
                    elif self.game_state == "paused":
                        if self.ui.get_resume_button().collidepoint(mouse_pos):
                            pause_duration = pygame.time.get_ticks() - self.pause_start_time
                            for buff_type in self.buff_end_times:
                                self.buff_end_times[buff_type] += pause_duration
                            self.game_state = "playing"
                        elif self.ui.get_restart_button().collidepoint(mouse_pos):
                            self.reset()
                            self.game_state = "playing"
                        elif self.ui.get_menu_button().collidepoint(mouse_pos):
                            self.reset()
                            self.game_state = "menu"
                    elif self.game_state == "game_over":
                        if pygame.time.get_ticks() - self.game_over_start_time >= 1000:
                            if self.ui.get_restart_button(420).collidepoint(mouse_pos):
                                self.reset()
                                self.countdown_start_time = pygame.time.get_ticks()
                                self.game_state = "countdown"
                            elif self.ui.get_game_over_menu_button().collidepoint(mouse_pos):
                                self.reset()
                                self.game_state = "menu"
                    elif self.game_state == "help":
                        close_rect = pygame.Rect(settings.SCREEN_WIDTH//2 - 80, settings.SCREEN_HEIGHT//2 + 200, 160, 80)
                        if close_rect.collidepoint(mouse_pos):
                            self.game_state = "menu"
            
            if keys[pygame.K_p] and not self.p_pressed_last:
                if self.game_state == "playing":
                    self.pause_start_time = pygame.time.get_ticks()
                    self.game_state = "paused"
                elif self.game_state == "paused":
                    pause_duration = pygame.time.get_ticks() - self.pause_start_time
                    for buff_type in self.buff_end_times:
                        self.buff_end_times[buff_type] += pause_duration
                    self.game_state = "playing"
            self.p_pressed_last = keys[pygame.K_p]
            
            if self.game_state == "menu":
                self.ui.draw_menu_screen(self.screen)
            
            elif self.game_state == "countdown":
                self.ui.draw_background(self.screen)
                self.bird.draw(self.screen)
                
                current_time = pygame.time.get_ticks()
                elapsed = current_time - self.countdown_start_time
                countdown = max(0, 3 - int(elapsed / 1000))
                
                if countdown > 0:
                    font = pygame.font.Font(None, 150)
                    text = font.render(str(countdown), True, settings.WHITE)
                    text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))
                    self.screen.blit(text, text_rect)
                else:
                    self.game_state = "playing"
            
            elif self.game_state == "playing":
                self.update_buffs()
                self.ui.draw_background(self.screen)
                
                self.bird.velocity += self.current_gravity
                self.bird.y += self.bird.velocity
                self.bird.rect.y = self.bird.y
                
                if self.bird.y < 0:
                    self.bird.y = 0
                    self.bird.velocity = 0
                hit_ground = self.bird.y > settings.SCREEN_HEIGHT - settings.BIRD_SIZE
                if hit_ground:
                    self.bird.y = settings.SCREEN_HEIGHT - settings.BIRD_SIZE
                    self.bird.velocity = 0
                
                self.spawn_pipe()
                pipes_to_remove = []
                for pipe in self.pipes:
                    pipe.update(self.current_pipe_speed)
                    pipe.draw(self.screen)
                    if pipe.x + settings.PIPE_WIDTH < 0:
                        pipes_to_remove.append(pipe)
                for pipe in pipes_to_remove:
                    self.pipes.remove(pipe)
                
                coin_score, effects = self.coin_generator.update(self.bird.rect, self.current_pipe_speed)
                multiplier = 2 if "double" in self.active_buffs else 1
                self.score += coin_score * multiplier
                for effect in effects:
                    self.activate_buff(effect)
                self.coin_generator.draw(self.screen)
                
                self.bird.draw(self.screen)
                
                self.update_score()
                self.ui.draw_playing_ui(self.screen, self.score, self.game_mode, self.active_buffs)
                
                if self.check_collision() or hit_ground:
                    self.bird.y = max(0, min(self.bird.y, settings.SCREEN_HEIGHT - settings.BIRD_SIZE))
                    self.bird.rect.y = self.bird.y
                    current_high_score = self.get_current_high_score()
                    if self.score > current_high_score:
                        self.set_current_high_score(self.score)
                        self.new_record = True
                    else:
                        self.new_record = False
                    self.game_over_start_time = pygame.time.get_ticks()
                    self.game_state = "game_over"
            
            elif self.game_state == "paused":
                self.ui.draw_background(self.screen)
                for pipe in self.pipes:
                    pipe.draw(self.screen)
                self.coin_generator.draw(self.screen)
                self.bird.draw(self.screen)
                self.ui.draw_pause_screen(self.screen, self.score)
            
            elif self.game_state == "game_over":
                self.ui.draw_background(self.screen)
                self.ui.draw_game_over_screen(self.screen, self.score, self.get_current_high_score(), self.new_record, self.game_mode)
            
            elif self.game_state == "help":
                self.ui.draw_help_screen(self.screen)
            
            if self.flash_screen:
                flash_duration = 200
                elapsed = pygame.time.get_ticks() - self.flash_start_time
                if elapsed < flash_duration:
                    alpha = int(100 * (1 - elapsed / flash_duration))
                    flash_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
                    flash_surface.set_alpha(alpha)
                    flash_surface.fill((255, 255, 255))
                    self.screen.blit(flash_surface, (0, 0))
                else:
                    self.flash_screen = False
            
            pygame.display.flip()
            self.clock.tick(60)
