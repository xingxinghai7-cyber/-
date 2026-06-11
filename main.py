import pygame # type: ignore
import settings
from game import Game
from pipe import load_pipe_images

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.GAME_TITLE)
    
    load_pipe_images()
    
    try:
        game = Game(screen)
        game.run()
    except Exception as e:
        print(f"游戏出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")

if __name__ == "__main__":
    main()