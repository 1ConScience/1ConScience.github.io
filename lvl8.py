from classiq import *


def lvl8():

    infoObject = pygame.display.Info()
    offset_x_manquant = (infoObject.current_w-WIDTH)/2
    offset_y_manquant = (infoObject.current_h-HEIGHT)/2


 







    P1 = Player()
    P1.pos.x= -2602.93827160495
    P1.pos.y= 321.75
    P1.surf=image_gauche
    all_sprites.add(P1)

    plat_ = Platform((2000, 20),(27-250-20*27-1000+10, HEIGHT-10*27))
    all_sprites.add(plat_)
    platforms.add(plat_)

    spanw_txt = Texte("OK, j'arrête de filmer",27-250-20*27-2100+10, HEIGHT-10*27-50,(255, 255, 255))
    all_sprites.add(spanw_txt)

    for i in range(10):
        plat_ = Platform((20, 20),(-2700+20*i, 320-10*i))
        all_sprites.add(plat_)
        platforms.add(plat_)

    for i in range(10):
        plat_ = Platform((20, 20),(-2700-20*i+20*7, 320-10*i-10*7))
        all_sprites.add(plat_)
        platforms.add(plat_)

    for i in range(10):
        plat_ = Platform((20, 20),(-2700+20*i, 320-10*i-10*14))
        all_sprites.add(plat_)
        platforms.add(plat_)
    for i in range(10):
        plat_ = Platform((20, 20),(-2700-20*i+20*7, 320-10*i-10*21))
        all_sprites.add(plat_)
        platforms.add(plat_)










    fenetre = pygame.Surface((WIDTH, HEIGHT))

    bg_img = pygame.image.load("monitor-1.png").convert_alpha()

    #ajust camera
    camera.x = -2602.93827160495 - WIDTH / 2
    camera.y = 321.75 - HEIGHT / 2

    while True:

        
        #quand P1 entre en collision avec platforms
        P1.update()

        for event in pygame.event.get():
            P1.controls(event)

        P1.joystick()        

        #fond noir
        screen.fill((0,0,0))
        fenetre.fill((0,0,0))
        
        screen.blit(bg_img, (0, 0))

        #deplacer les sprites 
        for entity in all_sprites:
            entity.move()
            fenetre.blit(entity.surf, (entity.rect.x - camera.x, entity.rect.y - camera.y))

        screen.blit(fenetre, (offset_x_manquant, offset_y_manquant))


        pygame.display.update()
        FramePerSec.tick(FPS)
