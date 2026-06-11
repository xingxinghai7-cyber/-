import pygame           # type: ignore
import settings

def get_font(size):
    for font_name in settings.CHINESE_FONTS:
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

class Button:
    def __init__(self, x, y, width, height, text="", color=(34, 193, 34), hover_color=None, text_color=settings.WHITE, border_radius=15, image_path=None, hover_image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color if hover_color else self.adjust_color(color, 30)
        self.click_color = self.adjust_color(color, -30)
        self.text_color = text_color
        self.border_radius = border_radius
        self.font = get_font(32)
        self.hovered = False
        self.pressed = False
        
        self.image = None
        self.hover_image = None
        if image_path:
            try:
                import os
                full_path = os.path.join(os.getcwd(), image_path)
                if os.path.exists(full_path):
                    self.image = pygame.image.load(full_path).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (width, height))
            except:
                pass
        if hover_image_path:
            try:
                import os
                full_path = os.path.join(os.getcwd(), hover_image_path)
                if os.path.exists(full_path):
                    self.hover_image = pygame.image.load(full_path).convert_alpha()
                    self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
            except:
                pass
    
    def adjust_color(self, color, amount):
        return tuple(max(0, min(255, c + amount)) for c in color)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.hovered
            self.hovered = self.rect.collidepoint(event.pos)
            if self.hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif was_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.pressed = False
    
    def draw(self, screen):
        if self.image:
            current_image = self.hover_image if (self.hovered and self.hover_image) else self.image
            
            if self.pressed:
                offset = 2
            elif self.hovered:
                offset = 0
            else:
                offset = 0
            
            draw_rect = self.rect.copy()
            draw_rect.x += offset
            draw_rect.y += offset
            
            screen.blit(current_image, (draw_rect.x, draw_rect.y))
            
            if self.hovered:
                highlight_surface = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
                highlight_surface.fill((255, 255, 255, 30))
                screen.blit(highlight_surface, (draw_rect.x, draw_rect.y))
            
            if self.pressed:
                pressed_surface = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
                pressed_surface.fill((0, 0, 0, 20))
                screen.blit(pressed_surface, (draw_rect.x, draw_rect.y))
        else:
            if self.pressed:
                current_color = self.click_color
                offset = 2
            elif self.hovered:
                current_color = self.hover_color
                offset = 0
            else:
                current_color = self.color
                offset = 0
            
            shadow_offset = 3 if not self.pressed else 1
            shadow_rect = self.rect.copy()
            shadow_rect.x += shadow_offset
            shadow_rect.y += shadow_offset
            pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=self.border_radius)
            
            draw_rect = self.rect.copy()
            draw_rect.x += offset
            draw_rect.y += offset
            pygame.draw.rect(screen, current_color, draw_rect, border_radius=self.border_radius)
            
            highlight_rect = draw_rect.copy()
            highlight_rect.height = draw_rect.height // 2
            highlight_surface = pygame.Surface((draw_rect.width, draw_rect.height // 2), pygame.SRCALPHA)
            highlight_intensity = 60 if self.hovered else 40
            highlight_surface.fill((255, 255, 255, highlight_intensity))
            screen.blit(highlight_surface, (draw_rect.x, draw_rect.y))
            
            if self.text:
                text_surface = self.font.render(self.text, True, self.text_color)
                text_rect = text_surface.get_rect(center=draw_rect.center)
                screen.blit(text_surface, text_rect)
    
    def collidepoint(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

class UI:
    def __init__(self):
        self.font = get_font(74)
        self.small_font = get_font(36)
        self.tiny_font = get_font(24)
        self.background_image = None
        self.load_background()
        self.help_scroll_offset = 0
        self.help_max_scroll = 200
        
        self.normal_button = None
        self.extended_button = None
        self.help_button = None
        self.start_button = None
        self.pause_button = None
        self.resume_button = None
        self.restart_button = None
        self.menu_button = None
        self.game_over_restart_button = None
        self.game_over_menu_button = None
    
    def load_background(self):
        try:
            self.background_image = pygame.image.load("assets/background.png")
            self.background_image = pygame.transform.scale(self.background_image, 
                                                         (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        except:
            self.background_image = None
    
    def draw_background(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            gradient = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            for y in range(settings.SCREEN_HEIGHT):
                ratio = y / settings.SCREEN_HEIGHT
                color = (
                    int(135 + 60 * ratio),
                    int(206 + 40 * ratio),
                    int(235 + 20 * ratio)
                )
                pygame.draw.line(gradient, color, (0, y), (settings.SCREEN_WIDTH, y))
            screen.blit(gradient, (0, 0))
    
    def draw_menu_screen(self, screen):
        self.draw_background(screen)
        
        help_button = self.get_help_button()
        help_button.draw(screen)
        
        title_font = get_font(80)
        title_text = title_font.render(settings.GAME_TITLE, True, settings.WHITE)
        title_shadow = title_font.render(settings.GAME_TITLE, True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(settings.SCREEN_WIDTH//2, 150))
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title_text, title_rect)
        
        normal_button = self.get_normal_button()
        normal_button.draw(screen)
        
        extended_button = self.get_extended_button()
        extended_button.draw(screen)
        
        hint_text = self.small_font.render("选择游戏模式开始", True, settings.WHITE)
        hint_shadow = self.small_font.render("选择游戏模式开始", True, (0, 0, 0))
        hint_rect = hint_text.get_rect(center=(settings.SCREEN_WIDTH//2, 600))
        screen.blit(hint_shadow, (hint_rect.x + 2, hint_rect.y + 2))
        screen.blit(hint_text, hint_rect)
    
    def draw_start_screen(self, screen):
        self.draw_background(screen)
        
        help_button = self.get_help_button()
        help_button.draw(screen)
        
        title_font = get_font(80)
        title_text = title_font.render(settings.GAME_TITLE, True, settings.WHITE)
        title_shadow = title_font.render(settings.GAME_TITLE, True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(settings.SCREEN_WIDTH//2, 180))
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title_text, title_rect)
        
        pygame.draw.circle(screen, settings.ORANGE, (settings.SCREEN_WIDTH//2, 280), 50)
        pygame.draw.circle(screen, settings.BLACK, (settings.SCREEN_WIDTH//2 - 18, 270), 10)
        pygame.draw.circle(screen, settings.BLACK, (settings.SCREEN_WIDTH//2 + 18, 270), 10)
        pygame.draw.arc(screen, settings.BLACK, 
                       (settings.SCREEN_WIDTH//2 - 18, 285, 36, 24), 0, 3.14, 3)
        
        start_button = self.get_start_button()
        start_button.draw(screen)
        
        hint_text = self.small_font.render("按空格键或点击按钮开始", True, settings.WHITE)
        hint_shadow = self.small_font.render("按空格键或点击按钮开始", True, (0, 0, 0))
        hint_rect = hint_text.get_rect(center=(settings.SCREEN_WIDTH//2, 470))
        screen.blit(hint_shadow, (hint_rect.x + 2, hint_rect.y + 2))
        screen.blit(hint_text, hint_rect)
    
    def draw_playing_ui(self, screen, score, game_mode="normal", active_buffs=None):
        if active_buffs is None:
            active_buffs = {}
        
        pause_button = self.get_pause_button()
        pause_button.draw(screen)
        
        score_text = self.small_font.render(f"分数: {score}", True, settings.BLACK)
        score_width = score_text.get_width() + 20
        score_bg = pygame.Rect(10, 10, score_width, 45)
        pygame.draw.rect(screen, (255, 255, 255, 90), score_bg, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), score_bg, 2, border_radius=10)
        screen.blit(score_text, (20, 12))
        
        mode_text = self.tiny_font.render(f"模式: {'拓展' if game_mode == 'extended' else '普通'}", True, 
                                        (147, 51, 234) if game_mode == 'extended' else (34, 193, 34))
        mode_width = mode_text.get_width() + 10
        mode_bg = pygame.Rect(10, 60, mode_width, 35)
        pygame.draw.rect(screen, (255, 255, 255, 90), mode_bg, border_radius=8)
        screen.blit(mode_text, (15, 63))
        
        buff_y = 100
        for buff_type in active_buffs:
            buff_bg = pygame.Rect(10, buff_y, 100, 30)
            pygame.draw.rect(screen, (255, 255, 255, 90), buff_bg, border_radius=8)
            
            if buff_type == "slow":
                pygame.draw.polygon(screen, settings.BLUE, [
                    (20, buff_y + 15), (35, buff_y + 5), (35, buff_y + 25)
                ])
                buff_text = self.tiny_font.render("减速", True, settings.BLUE)
            elif buff_type == "fast":
                pygame.draw.polygon(screen, settings.PURPLE, [
                    (20, buff_y + 5), (35, buff_y + 15), (20, buff_y + 25)
                ])
                buff_text = self.tiny_font.render("冲刺", True, settings.PURPLE)
            elif buff_type == "double":
                pygame.draw.rect(screen, settings.GOLD, (18, buff_y + 5, 20, 20))
                double_text = self.tiny_font.render("2x", True, settings.WHITE)
                screen.blit(double_text, (22, buff_y + 3))
                buff_text = self.tiny_font.render("双倍", True, settings.GOLD)
            
            screen.blit(buff_text, (45, buff_y + 2))
            buff_y += 35
    
    def draw_pause_screen(self, screen, score):
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        box_width = 320
        box_height = 480
        box_x = settings.SCREEN_WIDTH // 2 - box_width // 2
        box_y = settings.SCREEN_HEIGHT // 2 - box_height // 2
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        shadow_rect = box_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=20)
        
        pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=20)
        
        gradient = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        for y in range(box_height):
            ratio = y / box_height
            gradient.fill((255, 255, 255, int(255 * (1 - ratio * 0.1))), (0, y, box_width, 1))
        screen.blit(gradient, (box_x, box_y))
        
        title_font = get_font(52)
        paused_text = title_font.render("游戏暂停", True, (50, 50, 50))
        paused_rect = paused_text.get_rect(center=(settings.SCREEN_WIDTH//2, box_y + 55))
        screen.blit(paused_text, paused_rect)
        
        score_text = self.small_font.render(f"当前得分: {score}", True, (50, 50, 50))
        score_width = score_text.get_width() + 40
        score_bg = pygame.Rect(settings.SCREEN_WIDTH//2 - score_width//2, box_y + 95, score_width, 50)
        pygame.draw.rect(screen, (240, 240, 240), score_bg, border_radius=10)
        
        score_rect = score_text.get_rect(center=(settings.SCREEN_WIDTH//2, box_y + 120))
        screen.blit(score_text, score_rect)
        
        resume_button = self.get_resume_button()
        resume_button.draw(screen)
        
        restart_button = self.get_restart_button()
        restart_button.draw(screen)
        
        menu_button = self.get_menu_button()
        menu_button.draw(screen)
    
    def draw_game_over_screen(self, screen, score, high_score=0, new_record=False, game_mode="normal"):
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        mode_name = "普通模式" if game_mode == "normal" else "拓展模式"
        mode_text = self.small_font.render(f"[ {mode_name} ]", True, (180, 180, 180))
        mode_rect = mode_text.get_rect(center=(settings.SCREEN_WIDTH//2, 145))
        screen.blit(mode_text, mode_rect)
        
        over_font = get_font(70)
        over_text = over_font.render("游戏结束", True, settings.WHITE)
        over_shadow = over_font.render("游戏结束", True, (0, 0, 0))
        over_rect = over_text.get_rect(center=(settings.SCREEN_WIDTH//2, 195))
        screen.blit(over_shadow, (over_rect.x + 3, over_rect.y + 3))
        screen.blit(over_text, over_rect)
        
        if new_record:
            record_font = get_font(32)
            record_text = record_font.render("新纪录！", True, (255, 215, 0))
            record_rect = record_text.get_rect(center=(settings.SCREEN_WIDTH//2, 245))
            screen.blit(record_text, record_rect)
        
        score_text = get_font(48).render(f"最终得分: {score}", True, (50, 50, 50))
        score_width = score_text.get_width() + 40
        score_bg = pygame.Rect(settings.SCREEN_WIDTH//2 - score_width//2, 275, score_width, 60)
        pygame.draw.rect(screen, (255, 255, 255, 90), score_bg, border_radius=15)
        
        score_rect = score_text.get_rect(center=(settings.SCREEN_WIDTH//2, 305))
        screen.blit(score_text, score_rect)
        
        high_score_text = self.small_font.render(f"{mode_name}最高分: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(settings.SCREEN_WIDTH//2, 380))
        screen.blit(high_score_text, high_score_rect)
        
        restart_button = self.get_restart_button(420)
        restart_button.draw(screen)
        
        menu_button = self.get_game_over_menu_button()
        menu_button.draw(screen)
    
    def draw_help_screen(self, screen):
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        box_width = 420
        box_height = 580
        box_x = settings.SCREEN_WIDTH // 2 - box_width // 2
        box_y = settings.SCREEN_HEIGHT // 2 - box_height // 2
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        shadow_rect = box_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=20)
        
        pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=20)
        
        title_font = get_font(44)
        title_text = title_font.render("游戏说明", True, (50, 50, 50))
        title_rect = title_text.get_rect(center=(settings.SCREEN_WIDTH//2, box_y + 45))
        screen.blit(title_text, title_rect)
        
        pygame.draw.line(screen, (200, 200, 200), 
                        (box_x + 30, box_y + 80), 
                        (box_x + box_width - 30, box_y + 80), 2)
        
        content_height = 500
        content_surface = pygame.Surface((box_width - 20, content_height + 200), pygame.SRCALPHA)
        content_surface.fill((255, 255, 255, 0))
        
        normal_title = get_font(32)
        normal_title_text = normal_title.render("普通模式", True, (34, 193, 34))
        content_surface.blit(normal_title_text, (20, 15))
        
        normal_desc = self.tiny_font
        desc_lines = [
            "• 经典玩法，控制小鸟飞行",
            "• 按空格键跳跃，穿过管道得分",
            "• 收集金币获得额外分数",
            "• 避开管道，不要撞到上下管道"
        ]
        
        y_offset = 55
        for line in desc_lines:
            text = normal_desc.render(line, True, (80, 80, 80))
            content_surface.blit(text, (20, y_offset))
            y_offset += 28
        
        pygame.draw.line(content_surface, (200, 200, 200), 
                        (20, y_offset + 10), 
                        (box_width - 40, y_offset + 10), 2)
        
        y_offset += 25
        extended_title = get_font(32)
        extended_title_text = extended_title.render("拓展模式", True, (147, 51, 234))
        content_surface.blit(extended_title_text, (20, y_offset))
        y_offset += 40
        
        buff_lines = [
            "• 包含普通模式所有内容",
            "",
            "• 减速buff：",
            "  管道速度减慢，持续5秒",
            "",
            "• 冲刺buff：",
            "  管道速度加快，撞碎管道不会判",
            "  负，结束时自动清屏",
            "",
            "• 清屏buff：",
            "  消除前方最多3个管道，每个+2分",
            "",
            "• 双倍积分buff：",
            "  获得的分数翻倍，包括过管道、",
            "  吃金币和撞管道得分，持续5秒"
        ]
        
        for line in buff_lines:
            text = normal_desc.render(line, True, (80, 80, 80))
            content_surface.blit(text, (20, y_offset))
            y_offset += 28
        
        self.help_max_scroll = max(0, y_offset - content_height + 100)
        self.help_scroll_offset = max(0, min(self.help_scroll_offset, self.help_max_scroll))
        
        content_display_height = box_height - 180
        clip_rect = pygame.Rect(0, self.help_scroll_offset, box_width - 20, content_display_height)
        clipped_content = content_surface.subsurface(clip_rect)
        screen.blit(clipped_content, (box_x + 10, box_y + 90))
        
        close_rect = pygame.Rect(settings.SCREEN_WIDTH//2 - 80, box_y + box_height - 90, 160, 50)
        pygame.draw.rect(screen, (80, 80, 80), close_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), close_rect, border_radius=10, width=2)
        
        close_font = get_font(24)
        close_text = close_font.render("关闭", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_rect.center)
        screen.blit(close_text, close_text_rect)
    
    def scroll_help(self, direction):
        scroll_amount = 30
        if direction > 0:
            self.help_scroll_offset = max(self.help_scroll_offset - scroll_amount, 0)
        else:
            self.help_scroll_offset = min(self.help_scroll_offset + scroll_amount, self.help_max_scroll)
    
    def get_start_button(self):
        if self.start_button is None:
            self.start_button = Button(settings.SCREEN_WIDTH//2 - 120, 380, 240, 120, image_path="assets/btn_start.png")
        return self.start_button
    
    def get_normal_button(self):
        if self.normal_button is None:
            self.normal_button = Button(settings.SCREEN_WIDTH//2 - 120, 320, 240, 120, image_path="assets/btn_normal.png")
        return self.normal_button
    
    def get_extended_button(self):
        if self.extended_button is None:
            self.extended_button = Button(settings.SCREEN_WIDTH//2 - 120, 460, 240, 120, image_path="assets/btn_extended.png")
        return self.extended_button
    
    def get_pause_button(self):
        if self.pause_button is None:
            self.pause_button = Button(settings.SCREEN_WIDTH - 55, 15, 40, 40, image_path="assets/btn_pause.png")
        return self.pause_button
    
    def get_resume_button(self):
        if self.resume_button is None:
            box_height = 480
            box_y = settings.SCREEN_HEIGHT // 2 - box_height // 2
            self.resume_button = Button(settings.SCREEN_WIDTH//2 - 90, box_y + 160, 180, 90, image_path="assets/btn_resume.png")
        return self.resume_button
    
    def get_restart_button(self, y_pos=None):
        if y_pos is None:
            if self.restart_button is None:
                box_height = 480
                box_y = settings.SCREEN_HEIGHT // 2 - box_height // 2
                self.restart_button = Button(settings.SCREEN_WIDTH//2 - 90, box_y + 260, 180, 90, image_path="assets/btn_restart.png")
            return self.restart_button
        if self.game_over_restart_button is None:
            self.game_over_restart_button = Button(settings.SCREEN_WIDTH//2 - 90, y_pos, 180, 90, image_path="assets/btn_restart.png")
        return self.game_over_restart_button
    
    def get_help_button(self):
        if self.help_button is None:
            self.help_button = Button(settings.SCREEN_WIDTH - 55, 15, 40, 40, image_path="assets/btn_help.png")
        return self.help_button
    
    def get_close_button(self):
        return Button(settings.SCREEN_WIDTH//2 - 80, settings.SCREEN_HEIGHT//2 + 220, 160, 80, image_path="assets/btn_close.png")
    
    def get_menu_button(self):
        if self.menu_button is None:
            box_height = 480
            box_y = settings.SCREEN_HEIGHT // 2 - box_height // 2
            self.menu_button = Button(settings.SCREEN_WIDTH//2 - 90, box_y + 360, 180, 90, image_path="assets/btn_menu.png")
        return self.menu_button
    
    def get_game_over_menu_button(self):
        if self.game_over_menu_button is None:
            self.game_over_menu_button = Button(settings.SCREEN_WIDTH//2 - 90, 525, 180, 90, image_path="assets/btn_menu.png")
        return self.game_over_menu_button
