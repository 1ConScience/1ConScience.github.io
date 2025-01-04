from classiq import *

def lvl2():

    home = Path.home()

    # get the path/directory
    folder_dir = glob.escape(home) + "/Pictures"


    liste_images = []

    nb_photos = 0


    #liste un a un de facon recursive les dossiers se trouvant dans le dossier image de l'utilisateur
    def get_dirlist(rootdir):

        dirlist = []

        with os.scandir(rootdir) as rit:
            for entry in rit:
                if not entry.name.startswith('.') and entry.is_dir():
                    dirlist.append(entry.path)
                    dirlist += get_dirlist(entry.path)

        return dirlist





    for prout in get_dirlist(folder_dir):

        # iterate over files in
        # that directory
        for img in glob.iglob(f'{prout}/*'):
        
            # check if the image ends with png
            if (img.endswith(".jpg")):
                image = pygame.image.load(img).convert()
                image = pygame.transform.scale(image, (1280/10, 720/10)) 
                liste_images.append(image)

                nb_photos +=1

            if nb_photos>10:
                break

        if nb_photos>10:
            break




    for index, image in enumerate(liste_images):
        tableau = Tableau(image,2000+index*300, 650 - 200*26-40-100)
        all_sprites.add(tableau)






    P1 = Player()
    all_sprites.add(P1)

    phi = PhiBot(4500,650 - 200*26-40-100)
    all_sprites.add(phi)

    spanw_txt = Texte("†",27, 360,(255, 255, 255))
    all_sprites.add(spanw_txt)

    PT1 = Platform((20000, 20),(0, 600 - 200*26))
    all_sprites.add(PT1)
    platforms.add(PT1)

    porte = Porte((5500, 600 - 200*26-40))
    all_sprites.add(porte)
    portes.add(porte)


    for i in range(27):
        PT = Platform((200, 15),((WIDTH/30)*i, 600 - 200*i))
        all_sprites.add(PT)
        platforms.add(PT)



    never_txt = Texte("Quel endroit étonnant...",(800/30)*26+500,  650 - 200*26-40-100,(43,255,255))
    all_sprites.add(never_txt)



    while not P1.greened:

        #quand P1 entre en collision avec platforms
        P1.update()
        phi.update()

        for event in pygame.event.get():
            P1.controls(event)

        P1.joystick()

        phi.deplacements()

        #fond noir
        screen.fill((0,0,0))

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