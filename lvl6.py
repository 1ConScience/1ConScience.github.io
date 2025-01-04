from classiq import *



def lvl6():


    P1 = Player()
    all_sprites.add(P1)

    P1.blacked = True

    spanw_txt = Texte("†",27, 360,(255, 255, 255))
    all_sprites.add(spanw_txt)

    spanw_txt = Texte("Attends, je n'ai pas fini de dessiner ce monde",100, 500,(0, 0, 0))
    all_sprites.add(spanw_txt)


    def create_block(x, y):
        plat_ = PlatformBlack((10, 20),(x, y))
        all_sprites.add(plat_)
        platforms.add(plat_)




    




 


    index_x=27
    index_y=HEIGHT

    partir_a_gauche=False
    generation_done=False

    last_plus_a_droite = 0

    while not P1.greened:




        







        if not generation_done:



            status= random.randint(1, 4)

            
            match status:
                case 1:
                    index_y-=1
                case 2:
                    pass
                case 3:
                    index_y-=1
                case 4:
                    index_y+=1












            alea_reverse_sens= random.randint(1, 200)
            if(alea_reverse_sens==200):
                if(partir_a_gauche):
                    partir_a_gauche=False
                else:
                    partir_a_gauche=True






            if index_x > last_plus_a_droite:
                last_plus_a_droite = index_x

            alea_down= random.randint(1, 100)
            if(alea_down==100):
                index_y+=200
                index_x = last_plus_a_droite

                #reinit
                partir_a_gauche=False



            if partir_a_gauche:
                index_x-=4
            else :
                index_x+=4

            create_block(index_x, index_y)



            if index_y>5000:
                porte = Porte((index_x,index_y-40))
                all_sprites.add(porte)
                portes.add(porte)
                generation_done=True

                plat_ = PlatformBlack((100, 20),(index_x, index_y))
                all_sprites.add(plat_)
                platforms.add(plat_)





        #quand P1 entre en collision avec platforms
        P1.update()


        for event in pygame.event.get():
            P1.controls(event)

        P1.joystick()


        #fond noir

        moncul = 255
        moncul2 = 255
        moncul3 = 255
        screen.fill((moncul,moncul2,moncul3))
        

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