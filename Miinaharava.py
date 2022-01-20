import random
import haravasto
import json
import time

tiedoston_nimi = "tulokset.txt"

tila = {
    "kentta": [],
    "jaljella": [],
    "nakyva_kentta": [],
    "tutkittava_kentta": []
}

kentan_speksit = {
    "leveys": 0,
    "korkeus": 0,
    "miinat_kpl": 0
}

pelin_tiedot = {
    "pvm": 0,
    "leveys": 0,
    "korkeus": 0,
    "miinat": 0,
    "kesto": 0,
    "siirrot": 0,
    "tulos": 0
    }
"""
Pelin alkaessa tämä ensin pitää nollata 
ja sitten syötetään pelin tiedot tähän,
jotta ne voidaan pelin päättyessä tallentaa
"""

def alkuvalikko():
    """
    Alku_valikko, mistä valitaan mitä halutaan elämällä tehdä
    """
    print("Halluukko nää pelata miinaharavaa, sillee")
    print("""
            1. Uusi peli
            2. Quit
            3. Highscores
            """)
    while True:
        valinta = input("Valinta 1, 2 tai 3: ").strip()
        if valinta == "1":
            main()
            print(" ")
            break
            #aloittaa uuden pelin
        elif valinta == "2":
            print("aijjaa")
            break
            #lopettaa ohjelman
        elif valinta == "3":
            tulostusfunktioxd(tulos_lataus(tiedoston_nimi))
            #tulostaa tulokset tiedostosta


def aikatiedot():
    '''
    Ottaa talteen aloitetun pelin päivämäärän ja aloitus sekunnit
    '''
    paiva = time.localtime()[2]
    kuukausi = time.localtime()[1]
    vuosi = time.localtime()[0]
    pelin_tiedot["pvm"] = "{}.{}.{}".format(paiva, kuukausi, vuosi)
    pelin_tiedot["kesto"] = time.time()


def nollaa_tiedot():
    '''
    Nollaa pelikerran tiedot
    '''
    pelin_tiedot["pvm"] = 0
    pelin_tiedot["leveys"] = 0
    pelin_tiedot["korkeus"] = 0
    pelin_tiedot["miinat"] = 0
    pelin_tiedot["kesto"] = 0
    pelin_tiedot["siirrot"] = 0
    pelin_tiedot["tulos"] = 0


def tallennus(lista, tiedosto):
    """
    Tallentaa pelin statsit tiedostoon.
    Lista sisältää tulokset, jotka halutaan tallentaa
    """
    tuloksia = []
    try:
        with open(tiedosto, "r+") as lahde:
            data = json.load(lahde)
            data.append(lista)
            lahde.seek(0)
            json.dump(data, lahde)
            #Päivittää juuri pelatun pelin tiedot aikaisempien pelien joukkoon
    except IOError:
        with open(tiedosto, "w") as lahde:
            tuloksia.append(lista)
            json.dump(tuloksia, lahde)
            #Luo uuden tiedoston tuloksia varten ja tallettaa sinne ensimmäisen pelin
    

def tulos_lataus(tiedosto):
    """
    Lataa tulokset tiedostosta
    """
    try:
        with open(tiedosto, "r") as lahde:
            tulostaulu = json.load(lahde)
            return tulostaulu
    except (IOError, json.JSONDecodeError):
        print("Homma ei niin sanotusti pelitä")
    
def tulostusfunktioxd(tulostettavat):
    """
    Tulostaa pelaajan _mahtavat_ saavutukset
    """
    try:
        for i, tulos in enumerate(tulostettavat):
            if tulos == None:
                continue
            else:
                print("pelikerta #{}. pvm: {}\nkenttä {}x{}, miinojen lkm: {}kpl\nkesto: {}s, siirrot: {}, lopputulos: {}\n".format(
                i + 1,
                tulos["pvm"],
                tulos["leveys"],
                tulos["korkeus"],
                tulos["miinat"],
                tulos["kesto"],
                tulos["siirrot"],
                tulos["tulos"]
                ))
    except TypeError:
        return

def kasittele_hiiri(x, y, painike, muokkaus):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Sisältää toiminnot hiiren oikealle ja vasemmalle napille
    """
    if painike == haravasto.HIIRI_VASEN:
        painike = "vasen"
        tulvataytto(tila["kentta"], x // 40, y // 40)
        pelin_tiedot["siirrot"] += 1
        if tila["tutkittava_kentta"] == tila["kentta"]:
            print("Voitit pelin")
            haravasto.aseta_hiiri_kasittelija(kasittele_hiiri_loppu)
            pelin_tiedot["kesto"] = round(time.time() - pelin_tiedot["kesto"], 1)
            pelin_tiedot["tulos"] = "Voitto"
            tallennus(pelin_tiedot, tiedoston_nimi)
            #Tutkii onko kentältä avattu kaikki ruudut, joissa ei ole miinaa
            #Jos on, niin peli tulkitaan voitetuksi
            #Ottaa myös pelatun pelin tiedot talteen ja tallentaa ne
    elif painike == haravasto.HIIRI_OIKEA:
        painike = "oikea"
        pelin_tiedot["siirrot"] += 1
        if tila["nakyva_kentta"][y // 40][x // 40] == " ":
            tila["nakyva_kentta"][y // 40][x // 40] = "f"
            #Laittaa avaamattomaan ruutuun lipun
        elif tila["nakyva_kentta"][y // 40][x // 40] == "f":
            tila["nakyva_kentta"][y // 40][x // 40] = " "
            #Ottaa lipun pois ruudusta


def kasittele_hiiri_loppu(x, y, painike, muokkaus):
    '''
    Poistaa hiiren toiminnot käytöstä.
    Käytetään kun peli on päättynyt (hävitty tai voitettu)
    '''
    if painike == haravasto.HIIRI_VASEN:
        painike = None
    elif painike == haravasto.HIIRI_OIKEA:
        painike = None


def maaraa_kentta():
    '''
    Pelaaja määrittelee pelattavan kentän leveyden, korkeuden ja miinojen lukumäärän
    '''
    while True:
        leveys = input("Anna kentän leveys: ")
        try:
            leveys = int(leveys)
            kentan_speksit["leveys"] = leveys
            break;
        except ValueError:
            print("Anna kokonaisluku")
    #Pelaaja määrittelee pelattavan kentän leveyden

    while True:
        korkeus = input("Anna kentän korkeus: ")
        try:
            korkeus = int(korkeus)
            kentan_speksit["korkeus"] = korkeus
            break;
        except ValueError:
            print("Anna kokonaisluku")
    #Pelaaja määrittelee pelattavan kentän korkeuden

    while True:
        miinat_kpl = input("Anna miinojen lukumäärä: ")
        try:
            miinat_kpl = int(miinat_kpl)
            if miinat_kpl > leveys * korkeus:
                print("Miinojen lukumäärä ei voi olla isompi kuin kentän ruutujen määrä.")
                continue
            kentan_speksit["miinat_kpl"] = miinat_kpl
            break;
        except ValueError:
            print("Anna kokonaisluku")
    #Pelaaja määrittelee pelattavan kentän miinojen lukumäärän

    pelin_tiedot["leveys"] = kentan_speksit["leveys"]
    pelin_tiedot["korkeus"] = kentan_speksit["korkeus"]
    pelin_tiedot["miinat"] = kentan_speksit["miinat_kpl"]
    #Päivittää pelattavan pelin tiedot tuloksia varten
    

def miinoita(kentta, jaljella, miinat_kpl):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """
    kerrat = 0
    while kerrat < miinat_kpl:
        miina = random.choice(jaljella)
        x = miina[0]
        y = miina[1]
        kentta[y][x] = "x"
        tila["tutkittava_kentta"][y][x] = "x"
        jaljella.remove(miina)
        kerrat += 1


def luo_kentta():
    maaraa_kentta()
    
    kentta = []
    for rivi in range(kentan_speksit["korkeus"]):
        kentta.append([])
        for sarake in range(kentan_speksit["leveys"]):
            kentta[-1].append(" ")

    tila["kentta"] = kentta
    #luo todellisen kentän

    kentta2 = []
    for rivi in range(kentan_speksit["korkeus"]):
        kentta2.append([])
        for sarake in range(kentan_speksit["leveys"]):
            kentta2[-1].append(" ")

    tila["nakyva_kentta"] = kentta2
    #luo pelaajalle näkyvän kentän

    kentta3 = []
    for rivi in range(kentan_speksit["korkeus"]):
        kentta3.append([])
        for sarake in range(kentan_speksit["leveys"]):
            kentta3[-1].append(" ")
    
    tila["tutkittava_kentta"] = kentta3
    #Luo kentän jota käytetään pelin loppumisen tutkintaan

    jaljella = []
    for x in range(kentan_speksit["leveys"]):
        for y in range(kentan_speksit["korkeus"]):
            jaljella.append((x, y))
    
    tila["jaljella"] = jaljella
    #luo listan, josta ohjelma tunnistaa laatat, joihin ei ole vielä generoitu miinaa miinoita-funktiossa

    miinoita(tila["kentta"], tila["jaljella"], kentan_speksit["miinat_kpl"])
    
    numerot()


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """

    haravasto.tyhjaa_ikkuna()
    haravasto.aloita_ruutujen_piirto()
    for j, rivi in enumerate(tila["nakyva_kentta"]):
        for i, ruutu in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(ruutu, i * 40, j * 40)
    
    haravasto.piirra_ruudut()


def tulvataytto(kentta, sx, sy):
    """
    Sisältää toiminnot, joita tapahtuu, kun kentällä klikkaa eri asioita
    """

    safe = []
    safe.append((sx, sy)) #Lisää listaan argumentteina annetut kordinaatit
    if "x" in kentta[sy][sx]:
        tila["nakyva_kentta"] = tila["kentta"]
        print("Hävisit pelin")
        haravasto.aseta_hiiri_kasittelija(kasittele_hiiri_loppu)
        pelin_tiedot["kesto"] = round(time.time() - pelin_tiedot["kesto"], 1)
        pelin_tiedot["tulos"] = "Häviö"
        tallennus(pelin_tiedot, tiedoston_nimi)
        #Tunnistaa pelin hävityksi, jos klikataan ruutua, jossa on miina
        #Ottaa pelin tiedot talteen ja tallentaa ne
        return
    for rr in range(1, 8):
        if "{}".format(rr) in kentta[sy][sx]:
            tila["nakyva_kentta"][sy][sx] = "{}".format(rr)
            tila["tutkittava_kentta"][sy][sx] = "{}".format(rr)
            return
        #jos on klikattu numeroruutua, laitetaan se näkyviin
        #lisätään ruutu myös tutkittavaan kenttään pelin loppumisen tutkimista varten
    alkio = 0
    while alkio < len(safe):
        x, y = safe[alkio]
        tila["nakyva_kentta"][y][x] = "0" #Merkitsee ruudun turvalliseksi
        tila["tutkittava_kentta"][y][x] = "0"
        for i in range(y - 1, y + 2): #Käy läpi alkukordinaattien viereiset ruudut (8 kpl)
            for j in range(x - 1, x + 2):
                try:
                    if kentta[i][j] == "0" and (j, i) not in safe and i >= 0 and j >= 0:
                        safe.append((j, i))
                        #Lisää avattujen laattojen listaan ruudut, jotka
                        #1. eivät ole pommeja tai numeroita, 2. eivät ole jo listassa, 3. eivät ole kentän ulkopuolella
                    for rr in range(1, 8):
                        if "{}".format(rr) in kentta[i][j] and i >= 0 and j >= 0:
                            tila["nakyva_kentta"][i][j] = "{}".format(rr)
                            tila["tutkittava_kentta"][i][j] = "{}".format(rr)
                    #Lisää avattujen laattojen listaan numero
                except IndexError:
                    continue
        alkio += 1
        #jos on klikattu tyhjää ruutua, avataan koko kyseinen numeroiden ympäröimä tyhjien ruutujen alue
        #lisätään ruutu myös tutkittavaan kenttään pelin loppumisen tutkimista varten

    safe = []


def main():
    """
    Lataa pelin grafiikat, nollaa pelin tiedot ja tallentaa uuden pelin aikatiedot,
    luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """

    haravasto.lataa_kuvat("spritet")
    nollaa_tiedot()
    luo_kentta()
    haravasto.luo_ikkuna(kentan_speksit["leveys"] * 40, kentan_speksit["korkeus"] * 40)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    aikatiedot()
    haravasto.aloita()
    


def numerot():
    '''
    Asettaa ruutuun numeron sen mukaan, montako pommia sen ympärillä on.
    '''

    pommit = 0
    for a, rivi in enumerate(tila["kentta"]):
        for b, ruutu in enumerate(rivi):
            #käy kaikki ruudut läpi
            for i in range(a - 1, a + 2):
                for j in range(b - 1, b + 2):
                    #tutkii, onko ruudun ympärillä pommia
                    try:
                        if tila["kentta"][i][j] == "x" and i >= 0 and j >= 0:
                            pommit += 1
                    except IndexError:
                        continue
                    except a == i and b == j:
                        continue
                    else:
                        continue
            if tila["kentta"][a][b] != "x":
                tila["kentta"][a][b] = "{}".format(pommit)
                #sijoittaa ruutuun numeron, jos ruudussa ei ole pommia
            if tila["kentta"][a][b] == "x":
                pommit = 0
                #jos ruudussa on pommi, nollataan ruutua ympäröivien pommien lukumäärä
            for tt in range(1, 8):
                if tila["kentta"][a][b] == "{}".format(tt):
                    pommit = 0
                    #jos ruutuun on sijoitettu numero, nollataan ruutua ympäröivien pommien lukumäärä


if __name__ == "__main__":
    alkuvalikko()
