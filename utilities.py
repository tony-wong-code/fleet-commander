try:
    import os
    import sys
    import pygame
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

def load_png(name, resolution, pos=(0, 0)):
    fullname = os.path.join('images/', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        res = (int(resolution[0]), int(resolution[1]))
        image = pygame.transform.scale(image, res)
        rect = image.get_rect()
        if pos != (0, 0):
            rect.center = pos
    except(pygame.error, message):
        print('Failed to load image: ', fullname)
        raise(SystemExit, message)
    return image, rect