import asyncio
import re
import nodriver as uc
from time import perf_counter
import sqlite3



async def main():
    browser = await uc.start()


    #on arrive sur la page
    page = await browser.get('https://www.leboncoin.fr/recherche?text='+motclebis+'%20'+motcle+'&locations=Orl%C3%A9ans_45000__47.90143_1.90498_5000_50000&shippable=1&transaction_status=search__no_value&price=199-399&owner_type=all&sort=time')
    await page.get_content()


    #on accepte les cookies
    btn_cookies = await page.find('Accepter & Fermer', best_match=True)
    await btn_cookies.mouse_click()

    
    cpt_offres = 0
    somme_des_prix = 0
    plus_bas_prix = 99999999999
    plus_haut_prix = 0
    

    #on recup le nb dannonces pour calculer le nb de pages (ya 35 articles par page)
    element_nb_annonces = await page.find(" annonces", best_match=True)
    print(element_nb_annonces.text)
    str_nb_annonces = element_nb_annonces.text
    str_nb_annonces=str_nb_annonces.replace(" annonces"," ")
    nb_annonces = int(str_nb_annonces)
    print("nb annonces int")
    print(nb_annonces)

    print("quotient")
    print(nb_annonces//35)
    print("modulo (reste)")
    print(nb_annonces%35)

    nb_pages=nb_annonces//35
    if((nb_annonces%35)>0):
        nb_pages+=1
    print("nombre de pages à parcourir")
    print(nb_pages)

    
    index_page=1
    #on parcourt toutes les pages de la recherche
    while index_page<=nb_pages:
        index_page+=1

        #on recup le prix de chaque offre qui saffiche sur la page actuelle
        elems = await page.select_all('.styles_adCard__klAb3')
        for elem in elems:
            print()
            #await page.scroll_down(18)

            date = ""
            elem_date = await elem.query_selector_all('p.text-caption.text-neutral')
            if len(elem_date)>2:
                print(elem_date[2].attrs.title)
                date = elem_date[2].attrs.title

            elem_href = await elem.query_selector('[data-qa-id="aditem_container"]')
            print(elem_href.attrs.href)
            lien = elem_href.attrs.href

            elem_title = await elem.query_selector('[data-qa-id="aditem_title"]')
            title=elem_title.text
            print(title)
            if re.search(motcle, title, re.IGNORECASE) and re.search(motclebis, title, re.IGNORECASE) and not(re.search(notmotcle, title, re.IGNORECASE)) :

                cpt_offres+=1

                elem_price = await elem.query_selector('[data-test-id="price"]')
                s = elem_price.text
                print(s)

                s=s.replace("€","")
                s=s.replace(",",".")
                f=float(s)
                somme_des_prix+=f

                if f>plus_haut_prix:
                    plus_haut_prix=f

                if f<plus_bas_prix:
                    plus_bas_prix=f

                req_chaine = "INSERT INTO "+table_name+" (titre, prix, date, lien) VALUES('"+title+"', '"+s+"', '"+date+"', '"+lien+"')"  
                cursor.execute(req_chaine)
                conn.commit()

            else : 
                print("PI - PAS INTERESSE") 

            
            

        #on passe à la page suivante
        elem_pagination = await page.select('[data-spark-component="pagination"]')
        await elem_pagination.scroll_into_view()  
        btn_next_page = await page.select('[data-spark-component="pagination-next-trigger"]')
        await btn_next_page.mouse_click()
        #page = await browser.get('https://www.leboncoin.fr/recherche?text=rtx%203070&locations=Orl%C3%A9ans_45000__47.90143_1.90498_5000_50000&shippable=1&transaction_status=search__no_value&price=199-399&owner_type=all&sort=time&page='+str(index_page))
        await page.get_content()



    print()
    print()
    print("nb offres : ")
    print(cpt_offres)

    print("Moyenne du prix :")
    print(somme_des_prix/cpt_offres)

    print("Plus bas prix :")
    print(plus_bas_prix)

    print("Plus haut prix :")
    print(plus_haut_prix)




if __name__ == '__main__':

    
    motclebis = "rtx"
    motcle = "3070"
    table_name = motclebis+motcle
    notmotcle = "ti"

    conn = sqlite3.connect('lbc_base.db')

    cursor = conn.cursor()

    req_chaine = "CREATE TABLE IF NOT EXISTS "+table_name+"(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, date TEXT, lien TEXT, titre TEXT, prix REAL)"
    cursor.execute(req_chaine)
    conn.commit()


    t1_start = perf_counter() 

    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())

    t1_stop = perf_counter()
    print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)


    conn.close()