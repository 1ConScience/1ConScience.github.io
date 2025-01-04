from classiq import *


def lvl5():


    P1 = Player()
    all_sprites.add(P1)

    spanw_txt = Texte("†",27, 360,(255, 255, 255))
    all_sprites.add(spanw_txt)



    Phi = PhiBot(-11706,1451)
    all_sprites.add(Phi)

    def create_block(x, y):
        plat = PlatformBlacknWhite((20, 100),(x, y))
        all_sprites.add(plat)
        platforms.add(plat)


    # Fonction puissance de 2
    def pouissancededeux(n):
        somme = 1
        for count in range(int(n)):
            somme = somme * 2
        return somme

    def fractal(x,y,profondeur):

        for niveau in range(profondeur):

            nb_nouvelles_branches = pouissancededeux(niveau)      

            for branche in range(nb_nouvelles_branches):

                create_block(1000+x-25*nb_nouvelles_branches+branche*25, y+100*niveau)
        
    fractal(0, HEIGHT,10)

    

    porte = Porte((-11802,1421))
    all_sprites.add(porte)
    portes.add(porte)



    while not P1.greened:


        #quand P1 entre en collision avec platforms
        P1.update()
        Phi.update()


        for event in pygame.event.get():
            P1.controls(event)

        P1.joystick()


        #fond noir
        screen.fill((100,100,100))
        

        #ajust camera
        camera.x = P1.pos.x - WIDTH / 2
        camera.y = P1.pos.y - HEIGHT / 2
        
        #deplacer les sprites 
        for entity in all_sprites:
            entity.move()
            screen.blit(entity.surf, (entity.rect.x - camera.x, entity.rect.y - camera.y))

        if (P1.rect.y - camera.y) > HEIGHT:
            P1.into_the_void()


        pygame.display.update()
        FramePerSec.tick(FPS)