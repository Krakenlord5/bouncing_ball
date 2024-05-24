import pygame

pygame.init()
font = pygame.font.Font(None, 40)

def debug(info, y = 10, x = 10):
    display_surface = pygame.display.get_surface()
    # create text
    debug_surf = font.render(str(info), True, "black", "white")
    # create rect with pos
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    # blit
    display_surface.blit(debug_surf, debug_rect)