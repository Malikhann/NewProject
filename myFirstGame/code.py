from pygame import *
BLUE = (0, 0, 255)
back = BLUE
resolution = (700, 500)
window = display.set_mode(resolution)
picture = transform.scale(image.load('background.jpg'), resolution)
display.set_caption('Моя первая игра')

#class square()

run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
    window.blit(picture, (0, 0))
    display.update()