try:
    import os
    import sys
    import pygame
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

def load_png(name, resolution):
    fullname = os.path.join('images/', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        image = pygame.transform.scale(image, resolution)
    except(pygame.error, message):
        print('Failed to load image: ', fullname)
        raise(SystemExit, message)
    return image, image.get_rect()