# -*- coding: cp1250 -*-

import sqlite3

conn = sqlite3.connect('baza.db')
cur = conn.cursor()

def create_table():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ODDZIALY (
      numer INTEGER PRIMARY KEY AUTOINCREMENT,
      nazwa TEXT NOT NULL UNIQUE)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS STANOWISKA (
      numer INTEGER PRIMARY KEY AUTOINCREMENT, 
      nazwa_stanowiska TEXT NOT NULL UNIQUE)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS CHOROBY (
      id_choroby INTEGER PRIMARY KEY AUTOINCREMENT,
      nazwa TEXT NOT NULL UNIQUE)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS SKIEROWANIA (
      id_skierowania INTEGER PRIMARY KEY AUTOINCREMENT, 
      data TEXT(10) NOT NULL)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ZABIEGI (
      numer_zabiegu INTEGER PRIMARY KEY AUTOINCREMENT, 
      wynik TEXT(500) NOT NULL, 
      data TEXT(10) NOT NULL, 
      czas INTEGER(10) NOT NULL, 
      nazwa TEXT)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS SRODKI_HIGIENICZNE (
      numer PRIMARY KEY, 
      nazwa TEXT NOT NULL, 
      koszt_jednostkowy INTEGER NOT NULL)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS PRACOWNICY (
      IDpracownika INTEGER PRIMARY KEY AUTOINCREMENT, 
      imie TEXT NOT NULL, 
      nazwisko TEXT NOT NULL, 
      miejscowosc TEXT NOT NULL, 
      kod_pocztowy TEXT NOT NULL,
      ulica TEXT NOT NULL,
      pensja INTEGER NOT NULL, 
      STANOWISKAnumer INTEGER,
      FOREIGN KEY (STANOWISKAnumer) REFERENCES STANOWISKA(numer)
      ON DELETE RESTRICT ON UPDATE CASCADE)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS LEKARZE (
      IDlekarza INTEGER PRIMARY KEY AUTOINCREMENT, 
      specjalizacja TEXT NOT NULL, 
      numer_telefonu INTEGER(10) NOT NULL UNIQUE, 
      PRACOWNICYIDpracownika INTEGER,
      FOREIGN KEY (PRACOWNICYIDpracownika) REFERENCES
      PRACOWNICY(IDpracownika) ON DELETE RESTRICT ON UPDATE CASCADE)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ODDZIALY_PRACOWNICY (
      ODDZIALYnumer INTEGER NOT NULL,
      PRACOWNICYIDpracownika INTEGER NOT NULL,
      ilosc_godzin REAL NOT NULL,
      miesiac TEXT,
      FOREIGN KEY (ODDZIALYnumer) REFERENCES ODDZIALY(numer) ON DELETE RESTRICT ON UPDATE CASCADE,
      FOREIGN KEY (PRACOWNICYIDpracownika) REFERENCES PRACOWNICY(IDpracownika) ON DELETE RESTRICT ON UPDATE CASCADE
      CHECK (ilosc_godzin < 300))""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS TESTY_MEDYCZNE (
      numer_testu INTEGER PRIMARY KEY AUTOINCREMENT, 
      nazwa TEXT, 
      data TEXT(10) NOT NULL, 
      wynik_testu TEXT(500) NOT NULL, 
      PRACOWNICYIDpracownika INTEGER,
      FOREIGN KEY (PRACOWNICYIDpracownika)
      REFERENCES PRACOWNICY(IDpracownika)
      ON DELETE RESTRICT ON UPDATE CASCADE)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS PACJENCI (
      pesel INTEGER PRIMARY KEY, 
      imie TEXT NOT NULL,
      nazwisko TEXT NOT NULL, 
      miejscowosc TEXT NOT NULL, 
      kod_pocztowy TEXT NOT NULL,
      ulica TEXT NOT NULL,
      krewny TEXT NOT NULL, 
      forma_opieki TEXT,
      CHECK (forma_opieki='ambulatoryjna' or forma_opieki=='szpital'))""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ODDZIALY_PACJENCI (
     ODDZIALYnumer INTEGER NOT NULL,
      PACJENCIpesel INTEGER NOT NULL,
      numer_pokoju INTEGER, 
      numer_lozka INTEGER,
      FOREIGN KEY (ODDZIALYnumer) REFERENCES ODDZIALY(numer)
      ON DELETE RESTRICT ON UPDATE CASCADE,
      FOREIGN KEY (PACJENCIpesel) REFERENCES PACJENCI(pesel)
      ON DELETE RESTRICT ON UPDATE CASCADE)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS PACJENCI_SRODKI_HIGIENICZNE (
      PACJENCIpesel INTEGER NOT NULL,
      SRODKI_HIGIENICZNEnumer INTEGER NOT NULL,
      data TEXT(10) NOT NULL, 
      godzina INTEGER NOT NULL, 
      ilosc INTEGER NOT NULL, 
      FOREIGN KEY (PACJENCIpesel) REFERENCES PACJENCI(pesel)
      ON DELETE RESTRICT ON UPDATE CASCADE,
      FOREIGN KEY (SRODKI_HIGIENICZNEnumer) REFERENCES
      SRODKI_HIGIENICZNE(numer) ON DELETE RESTRICT ON UPDATE CASCADE)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS WIZYTY (
      numer_wizyty INTEGER PRIMARY KEY AUTOINCREMENT, 
      data TEXT(10) NOT NULL, 
      recepta TEXT NOT NULL, 
      CHOROBYidchoroby INTEGER,
      SKIEROWANIAid_skierowania INTEGER,
      FOREIGN KEY (CHOROBYidchoroby) REFERENCES CHOROBY(idchoroby)
      ON DELETE RESTRICT ON UPDATE CASCADE, 
      FOREIGN KEY (SKIEROWANIAid_skierowania) REFERENCES
      SKIEROWANIA(id_skierowania) ON DELETE RESTRICT ON UPDATE CASCADE,
      CHECK (recepta == 'T' or recepta == 'N' ))""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS TYPY_BADAN (
      id_typ_badania INTEGER PRIMARY KEY AUTOINCREMENT, 
      TESTY_MEDYCZNEnumer_testu INTEGER,
      WIZYTYnumer_wizyty INTEGER,
      ZABIEGInumer_zabiegu INTEGER,
      FOREIGN KEY (TESTY_MEDYCZNEnumer_testu) REFERENCES
      TESTY_MEDYCZNE(numer_testu) ON DELETE RESTRICT ON UPDATE CASCADE, 
      FOREIGN KEY (WIZYTYnumer_wizyty) REFERENCES
      WIZYTY(numer_wizyty) ON DELETE RESTRICT ON UPDATE CASCADE,
      FOREIGN KEY (ZABIEGInumer_zabiegu) REFERENCES
      ZABIEGI(numer_zabiegu) ON DELETE RESTRICT ON UPDATE CASCADE)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS LEKARZE_PACJENCI (
      LEKARZEIDlekarza INTEGER NOT NULL,
      PACJENCIpesel INTEGER NOT NULL,
      TYPY_BADANid_typ_badania INTEGER NOT NULL,
      FOREIGN KEY (LEKARZEIDlekarza) REFERENCES LEKARZE(IDlekarza)
      ON DELETE RESTRICT ON UPDATE CASCADE,
      FOREIGN KEY (PACJENCIpesel) REFERENCES PACJENCI(pesel)
      ON DELETE RESTRICT ON UPDATE CASCADE,
      FOREIGN KEY (TYPY_BADANid_typ_badania) REFERENCES
      TYPY_BADAN(id_typ_badania) ON DELETE RESTRICT ON UPDATE CASCADE)""")


def data_entry_oddzialy():
    oddzialy = [( 1 , 'Ogolny' ),( 2 , 'Chirurgia' ),
                ( 3 , 'Pediatria' ),( 4 , 'Poloznictwo' ),
                ( 5 , 'Neurologia' )]
    cur.executemany("INSERT INTO oddzialy (numer, nazwa) VALUES (?, ?)", oddzialy)
    conn.commit()

def data_entry_stanowiska():
    stanowiska = [( 1 , 'Ordynator' ),( 2 , 'Oddzialowa' ),
                  ( 3 , 'Lekarz' ),( 4 , 'Pielegniarka' ),
                  ( 5 , 'Polozna' ),( 6 , 'Technik' ),
                  ( 7 , 'Sprzataczka' ),( 8 , 'Kuchnia' ),
                  ( 9 , 'Informatyk' ),( 10 , 'Fizjoterapeuta' )]
    cur.executemany("""INSERT INTO stanowiska (numer, nazwa_stanowiska)
                    VALUES (?, ?)""", stanowiska)
    conn.commit()

def data_entry_choroby():
    choroby = [(1, 'Choroba Parkinsona'),(2, 'Dyskopatia'),(3, 'Choroba Alzheimera'),
               (4, 'Choroba Huntingtona'),(5, 'Borelioza z Lyme'),(6, 'Niedokrwistosc'),
               (7, 'Ostre i przewlekle zapalenie blony sluzowej nosa i zatok przynosowych u dzieci'),
               (8, 'Astma oskrzelowa u dzieci'),(9, 'Biegunka ostra'),(10, 'Odra'),
               (11, 'Ospa wietrzna'),(12, 'Botulizm'),(13, 'Swinka'),(14, 'Rozyczka'),
               (15, 'Operacja szyszynki'),(16, 'Wyciecie przysadki mozgowej'),
               (17, 'Operacja przegrody nosa'),(18, 'Operacja zatoki nosa'),
               (19, 'Wycięcie migdalkow'),(20, 'Cukrzyca')]
    cur.executemany("""INSERT INTO choroby (id_choroby, nazwa) VALUES(?, ?)""", choroby)
    conn.commit()

def data_entry_skierowania():
    skierowania = [(1, '20.01.2019'),(2, '24.12.2018'),(3, '13.05.2018'),
                   (4, '05.10.2018'),(5, '01-03-2017'),(6, '19-01-2018'),
                   (7, '08-06-2017'),(8, '10-10-2017'),(9, '15-05-2018'),
                   (10, '01-03-2017'),(11, '24-04-2018'),(12, '31-03-2018'),
                   (13, '15-04-2018'),(14, '01-09-2018'),(15, '21.10.2018'),
                   (16, '17/11/2018'),(17, '10-05-2018'),(18, '31-07-2018'),
                   (19, '19-09-2018'),(20, '17-03-2018'),(21, '2019-02-03'),
                   (22, '2018-12-13')]
    cur.executemany("""INSERT INTO skierowania (id_skierowania, data)
                    VALUES(?, ?)""", skierowania)
    conn.commit()

def data_entry_zabiegi():
    zabiegi = [(1, 'Wyciecie migdalkow', 'Pozytywny. Zabieg przebiegl zgodnie z zalozeniami.', '20.03.2018', '23 minuty'),
               (2, 'Operacja przegrody nosa', 'Negatywny. Uszkodzenie kości twarzoczaszki.', '11.05.2018', '3 godziny'),
               (3, 'Operacja przepukliny pachwiowej', 'Pozytywny z komplikacjami. Uwięzienie przepukliny.', '21.10.2017', '4 godziny')]
    cur.executemany("""INSERT INTO zabiegi (numer_zabiegu, wynik, data, czas, nazwa)
                    VALUES(?, ?, ?, ?, ?)""", zabiegi)
    conn.commit()

def data_entry_srodki_higieniczne():
    srodki_higieniczne = [(1, 'ibuprom', 0.9),(2, 'apap', 0.5),
                          (3, 'reczkawiczki', 0.1),(4, 'ketonal', 1.0),(5, 'cetol-2', 1.2)]
    cur.executemany("""INSERT INTO srodki_higieniczne(numer, nazwa, koszt_jednostkowy)
                    VALUES(?, ?, ?)""", srodki_higieniczne)
    conn.commit()

def data_entry_pracownicy():
    pracownicy = [( 1 , 'Mariusz' , 'Dowolny' , 'Rawicz' , '63-900' , 'Rolnicza 3/6' , 20 , 6 ),
                  ( 2 , 'Zdzislawa' , 'Przekorny' , 'Wroclaw' , '51-200' , 'Mieroslawskiego 17' , 2100 , 7 ),
                  ( 3 , 'Jakub' , 'Spokojny' , 'Wroclaw' , '51-200' , 'Dabrowskiego 51' , 25 , 9 ),
                  ( 4 , 'Malgorzata' , 'Nowak' , 'Trzebnica', '55-100' , 'Jelenia 12' , 13 , 7 ),
                  ( 5 , 'Ewa' , 'Swobodna' , 'Wroclaw', '51-200' , 'Marysienki 15' , 3900 , 4 ),
                  ( 6 , 'Danuta' , 'Sarna' , 'Rawicz' , '63-900', 'Westerplatte 7/12' , 4100 , 5 ),
                  ( 7 , 'Jolanta' , 'Kwasnicka-Slodka' , 'Wrocław' , '51-200', 'Kwidzynska 54' , 24 , 5 ),
                  ( 8 , 'John' , 'Snow' , 'Brzeg' , '49-300', 'Gorna 39'  , 3500 , 10 ),
                  ( 9 , 'Ace' , 'Ventura' , 'Wroclaw' , '51-215' , 'Trauguta 45/2'  , 2300 , 8 ),
                  ( 10 , 'Bob' , 'Budowniczy' , 'Opole' , '45-020' , 'Winiarska 13'  , 35 , 3 ),
                  ( 11 , 'Maja' , 'Pszczolka' , 'Trzebnica' , '55-100' , 'Wolna 8' , 4200 , 5 ),
                  ( 12 , 'Bogdan' , 'Krzysztof' , 'Wrocław' , '51-200' , 'Krolewska 16' , 3500 , 6 ),
                  ( 13 , 'Dorian' , 'Gray' , 'Wroclaw' , '51-200' , 'Niedzwiedzia 18' , 16 , 8 ),
                  ( 14 , 'Elzbieta' , 'Wozniak' , 'Wroclaw' , '51-200' , 'Barania 83' , 24 , 5 ),
                  ( 15 , 'Olivier' , 'Queen' , 'Wroclaw' , '51-200' , 'Stoczniowa 15' , 20 , 10 ),
                  ( 16 , 'Marcin', 'Krolik', 'Wroclaw', '51-200', 'Urynowa 8', 10000, 1),
                  ( 17 , 'Waclaw', 'Wisniewski', 'Wroclaw', '51-200', 'Bociania 20', 11000, 1),
                  ( 18 , 'Aleksandra', 'Zabkiewicz', 'Wroclaw', '51-200', 'Krucza 13', 6900, 1),
                  ( 19 , 'Olga', 'Radziecka', 'Wroclaw', '51-200', 'Jaskolcza 80', 65, 1),
                  ( 20 , 'Kinga', 'Zajac', 'Wroclaw', '51-200', 'Dabrowskiego 18', 38, 3),
                  ( 21 , 'Pawel', 'Luberda', 'Wroclaw', '51-200', 'Starzynskiego 4', 7000, 3),
                  ( 22 , 'Wojciech', 'Gruca', 'Wroclaw', '51-200', 'Pilsudzkiego 1', 39, 3),
                  ( 23 , 'Jan', 'Szczepaniec', 'Wroclaw', '51-200', 'Wojska Polskiego 1/5', 8500, 3),
                  ( 24 , 'Samanta', 'Samuel', 'Wroclaw', '51-200', 'Sienkiewicza 5', 7400, 3),
                  ( 25 , 'Patryk', 'Pajak', 'Wroclaw', '51-200', 'Krotka 1', 9000, 3),
                  ( 26 , 'Malgorzata', 'Gaska', 'Wroclaw', '51-200', 'Traugutta 4/12', 38, 3)]
    cur.executemany("""INSERT INTO pracownicy(idpracownika, imie, nazwisko, miejscowosc, kod_pocztowy, ulica, pensja, stanowiskanumer)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", pracownicy)
    conn.commit()

def data_entry_lekarze():
    lekarze = [( 1 , 'Ginekolog' , 220621680 , 16),
               ( 2 , 'Neurolog' , 515161355, 17 ),
               ( 3 , 'Chirurg Ogolny' , 321535684 , 18 ),
               ( 4 , 'Chirurg Ogolny' , 326406546 , 20 ),
               ( 5 , 'Pediatra' , 325621352 , 19 ),
               ( 6 , 'Pediatra' , 235162685 , 21 ),
               ( 7 , 'Neurolog' , 621642195 , 22 ),
               ( 8 , 'Ginekolog' , 321649432 , 23 ),
               ( 9 , 'Pediatra', 551436755, 24),
               ( 10, 'Pediatra', 478998166, 25),
               ( 11, 'Pediatra', 765445223, 26)]
    cur.executemany("""INSERT INTO lekarze(idlekarza, specjalizacja, numer_telefonu, pracownicyidpracownika)
                    VALUES(?, ?, ?, ?)""", lekarze)
    conn.commit()

def data_enty_oddzialy_pracownicy():
    oddzialy_pracownicy = [( 1 , 1 , 180 , 'styczen'),
                           ( 1 , 1 , 180 , 'grudzien'),
                           ( 1 , 1 , 80 , 'listopad'),
                           ( 1 , 2 , 180, 'styczen' ),
                           ( 1 , 2 , 100, 'grudzien' ),
                           ( 1 , 2 , 180, 'listopad' ),
                           ( 1 , 2 , 180, 'pazdziernik' ),
                           ( 1 , 2 , 150, 'wrzesien' ),
                           ( 1 , 2 , 80, 'sierpien' ),
                           ( 1 , 2 , 180, 'lipiec' ),
                           ( 1 , 2 , 10, 'czerwiec' ),
                           ( 1 , 3 , 126, 'styczen'),
                           ( 1 , 3 , 60, 'grudzien'),
                           ( 1 , 3 , 110, 'listopad'),
                           ( 1 , 3 , 126, 'pazdziernik'),
                           ( 1 , 3 , 126, 'wrzesien'),
                           ( 1 , 3 , 50, 'sierpien'),
                           ( 1 , 4 , 180 , 'styczen' ),
                           ( 1 , 4 , 180 , 'grudzien' ),
                           ( 1 , 4 , 180 , 'listopad' ),
                           ( 1 , 4 , 180 , 'pazdziernik' ),
                           ( 1 , 4 , 180 , 'wrzesien' ),
                           ( 1 , 4 , 180 , 'sierpien' ),
                           ( 1 , 4 , 180 , 'lipiec' ),
                           ( 1 , 4 , 180 , 'czerwiec' ),
                           ( 2 , 5 , 190, 'styczen'),
                           ( 2 , 5 , 150, 'grudzien'),
                           ( 2 , 5 , 180, 'listopad'),
                           ( 2 , 5 , 190, 'pazdziernik'),
                           ( 2 , 5 , 179, 'wrzesien'),
                           ( 2 , 5 , 100, 'sierpien'),
                           ( 2 , 5 , 190, 'lipiec'),
                           ( 2 , 5 , 190, 'czerwiec'),
                           ( 4 , 6 , 190, 'styczen'),
                           ( 4 , 6 , 150, 'grudzien'),
                           ( 4 , 6 , 180, 'listopad'),
                           ( 4 , 6 , 190, 'pazdziernik'),
                           ( 4 , 6 , 190, 'wrzesien'),
                           ( 4 , 6 , 190, 'sierpien'),
                           ( 4 , 6 , 150, 'lipiec'),
                           ( 4 , 6 , 190, 'czerwiec'),
                           ( 4 , 7 , 190, 'styczen'),
                           ( 4 , 7 , 150, 'grudzien'),
                           ( 4 , 7 , 180, 'listopad'),
                           ( 4 , 7 , 190, 'pazdziernik'),
                           ( 4 , 7 , 80, 'wrzesien'),
                           ( 1 , 8 , 180, 'styczen'),
                           ( 1 , 8 , 150, 'grudzien'),
                           ( 1 , 8 , 180, 'listopad'),
                           ( 1 , 8 , 180, 'pazdziernik'),
                           ( 1 , 8 , 90, 'wrzesien'),
                           ( 1 , 9 , 170, 'styczen'),
                           ( 1 , 9 , 170, 'grudzien'),
                           ( 1 , 9 , 170, 'listopad'),
                           ( 1 , 9 , 150, 'pazdziernik'),
                           ( 1 , 9 , 170, 'wrzesien'),
                           ( 5 , 10 , 140 , 'styczen' ),
                           ( 5 , 10 , 140 , 'grudzien' ),
                           ( 5 , 10 , 100 , 'listopad' ),
                           ( 5 , 10 , 140 , 'padziernik' ),
                           ( 5 , 10 , 140 , 'wrzesien' ),
                           ( 5 , 10 , 50 , 'sierpien' ),
                           ( 4 , 11 , 190, 'styczen' ),
                           ( 4 , 11 , 150, 'grudzien' ),
                           ( 4 , 11 , 180, 'listopad' ),
                           ( 4 , 11 , 190, 'pazdziernik' ),
                           ( 4 , 11 , 190, 'wrzesien' ),
                           ( 4 , 11 , 190, 'sierpien' ),
                           ( 4 , 11 , 150, 'lipiec' ),
                           ( 4 , 11 , 190, 'czerwiec' ),
                           ( 1 , 12, 100, 'listopad' ),
                           ( 1 , 12, 180, 'pazdziernik' ),
                           ( 1 , 12, 180, 'wrzesien' ),
                           ( 1 , 12, 180, 'sierpien' ),
                           ( 1 , 12, 180, 'lipiec' ),
                           ( 1 , 12, 180, 'czerwiec' ),
                           ( 1 , 13, 170, 'styczen' ),
                           ( 1 , 13, 170, 'grudzien' ),
                           ( 1 , 13, 170, 'listopad' ),
                           ( 1 , 13, 170, 'pazdziernik' ),
                           ( 1 , 13, 170, 'wrzesien' ),
                           ( 2 , 14 , 190, 'styczen' ),
                           ( 2 , 14 , 150, 'grudzien' ),
                           ( 2 , 14 , 180, 'listopad' ),
                           ( 2 , 14 , 190, 'pazdziernik' ),
                           ( 2 , 14 , 179, 'wrzesien' ),
                           ( 2 , 14 , 100, 'sierpien' ),
                           ( 2 , 14 , 190, 'lipiec' ),
                           ( 2 , 14 , 190, 'czerwiec' ),
                           ( 1 , 15 , 173 , 'styczen' ),
                           ( 1 , 15 , 180 , 'grudzien' ),
                           ( 1 , 15 , 180 , 'listopad' ),
                           ( 1 , 15 , 180 , 'pazdziernik' ),
                           ( 1 , 15 , 170 , 'wrzesien' ),
                           ( 1 , 15 , 110 , 'sierpien' ),
                           ( 1 , 16 , 140 , 'styczen'),
                           ( 1 , 16 , 100 , 'grudzien'),
                           ( 1 , 16 , 140 , 'listopad'),
                           ( 1 , 16 , 140 , 'pazdziernik'),
                           ( 1 , 16 , 140 , 'wrzesien'),
                           ( 1 , 16 , 140 , 'sierpien'),
                           ( 1 , 16 , 50 , 'lipiec'),
                           ( 2 , 17 , 140 , 'styczen'),
                           ( 2 , 17 , 100 , 'grudzien'),
                           ( 2 , 17 , 140 , 'listopad'),
                           ( 2 , 17 , 140 , 'pazdziernik'),
                           ( 2 , 17 , 140 , 'wrzesien'),
                           ( 2 , 17 , 140 , 'sierpien'),
                           ( 2 , 17 , 50 , 'lipiec'),
                           ( 3 , 18 , 140 , 'styczen'),
                           ( 3 , 18 , 100 , 'grudzien'),
                           ( 3 , 18 , 140 , 'listopad'),
                           ( 3 , 18 , 140 , 'pazdziernik'),
                           ( 3 , 18 , 140 , 'wrzesien'),
                           ( 3 , 18 , 140 , 'sierpien'),
                           ( 3 , 18 , 50 , 'lipiec'),
                           ( 4 , 19 , 140 , 'styczen'),
                           ( 4 , 19 , 100 , 'grudzien'),
                           ( 4 , 19 , 140 , 'listopad'),
                           ( 4 , 19 , 140 , 'pazdziernik'),
                           ( 4 , 19 , 140 , 'wrzesien'),
                           ( 4 , 19 , 140 , 'sierpien'),
                           ( 4 , 19 , 50 , 'lipiec'),
                           ( 4 , 20 , 140 , 'styczen'),
                           ( 4 , 20 , 80 , 'grudzien'),
                           ( 4 , 20 , 140 , 'listopad'),
                           ( 4 , 20 , 140 , 'pazdziernik'),
                           ( 4 , 20 , 140 , 'wrzesien'),
                           ( 4 , 20 , 40 , 'sierpien'),
                           ( 5 , 21 , 140 , 'styczen'),
                           ( 5 , 21 , 80 , 'grudzien'),
                           ( 5 , 21 , 140 , 'listopad'),
                           ( 5 , 21 , 140 , 'pazdziernik'),
                           ( 5 , 21 , 140 , 'wrzesien'),
                           ( 5 , 21 , 40 , 'sierpien'),
                           ( 2 , 22 , 140 , 'styczen'),
                           ( 2 , 22 , 80 , 'grudzien'),
                           ( 2 , 22 , 140 , 'listopad'),
                           ( 2 , 22 , 140 , 'pazdziernik'),
                           ( 2 , 22 , 140 , 'wrzesien'),
                           ( 2 , 22 , 40 , 'sierpien'),
                           ( 4 , 23 , 140 , 'styczen'),
                           ( 4 , 23 , 80 , 'grudzien'),
                           ( 4 , 23 , 140 , 'listopad'),
                           ( 4 , 23 , 140 , 'pazdziernik'),
                           ( 4 , 23 , 140 , 'wrzesien'),
                           ( 4 , 23 , 40 , 'sierpien'),
                           ( 3 , 24 , 140 , 'styczen'),
                           ( 3 , 24 , 80 , 'grudzien'),
                           ( 3 , 24 , 140 , 'listopad'),
                           ( 3 , 24 , 140 , 'pazdziernik'),
                           ( 3 , 24 , 140 , 'wrzesien'),
                           ( 3 , 24 , 40 , 'sierpien'),
                           ( 3 , 25 , 140 , 'styczen'),
                           ( 3 , 25 , 80 , 'grudzien'),
                           ( 3 , 25 , 140 , 'listopad'),
                           ( 3 , 25 , 140 , 'pazdziernik'),
                           ( 3 , 25 , 140 , 'wrzesien'),
                           ( 3 , 25 , 40 , 'sierpien'),
                           ( 1 , 26 , 140 , 'styczen'),
                           ( 1 , 26 , 80 , 'grudzien'),
                           ( 1 , 26 , 140 , 'listopad'),
                           ( 1 , 26 , 140 , 'pazdziernik'),
                           ( 1 , 26 , 140 , 'wrzesien'),
                           ( 1 , 26 , 40 , 'sierpien')]
    cur.executemany("""INSERT INTO oddzialy_pracownicy(oddzialynumer, pracownicyidpracownika, ilosc_godzin, miesiac)
                    VALUES(?, ?, ?, ?)""", oddzialy_pracownicy)
    conn.commit()

def data_entry_testy_medyczne():
    testy_medyczne = [(1, 'morfologia krwi', '2018-04-13', 'norma', 1),
                      (2, 'morfologia krwi', '2018-04-14', 'norma', 12),
                      (3, 'morfologia krwi', '2018-04-15', 'wysokie THS', 1),
                      (4, 'morfologia krwi', '2019-01-04', 'krzywa cukrowa wynik 140', 12),
                      (5, 'morfologia krwi', '2018-04-13', 'norma', 1)]
    cur.executemany("""INSERT INTO testy_medyczne(numer_testu, nazwa, data, wynik_testu, pracownicyidpracownika)
                    VALUES(?, ?, ?, ?, ?)""", testy_medyczne)
    conn.commit()

def data_entry_pacjenci():
    pacjenci = [( 95213846558 , 'Jakub' , ' Poranek' , 'Trzebnica' , '55-100' , 'Irkuca 18' , 'Jadwiga Poranek' , 'szpital'),
                ( 45378354345 , 'Mateusz' , 'Trzcielinski' , 'Wroclaw' , '51-200' , 'Krakowska 51' , 'Wiktor Konieczny' , 'szpital'),
                ( 52486734565 , 'Jakub' , 'Tworczy' , 'Wroclaw' , '51-200' , 'Rynek 3' , 'Sebastian Pstrąg' , 'szpital'),
                ( 53767545478 , 'Janusz' , 'Godny' , 'Wroclaw' , '51-200' , 'Podgorna 3/8' , 'Mikolaj Koszerny' , 'szpital'),
                ( 85128648985 , 'Krzysztof' , 'Dabrowski' , 'Wroclaw' , '51-200' , 'Szpitalna 19' , 'Bogdan Pawlacz' , 'szpital'),
                ( 76121613548 , 'Natalia' , 'Grzeszna' , 'Rawicz' , '63-900' , 'Wroclawska 42' , 'Zdzislaw Dobroduszny' , 'ambulatoryjna'),
                ( 76543867343 , 'Witold' , 'Dobry' , 'Rawicz' , '63-900' , 'Wolnosci 17' , 'Dawid Piekarz' , 'ambulatoryjna'),
                ( 78274538745 , 'Przemyslaw' , 'Przemily' , 'Rawicz' , '63-900' , 'Zmigrodzka 84' , 'Milosz Wierzacy' , 'ambulatoryjna'),
                ( 24080109787 , 'Maria', 'Sokol', 'Wroclaw', '51-200', 'Traugutta 51/2', 'Jan Sokol', 'szpital'),
                ( 94111934221 , 'Witold', 'Saneczko', 'Wroclaw', '51-200', 'Krakowska 12', 'Matylda Saneczko', 'szpital'),
                ( 91010214352 , 'Marta', 'Taneczna', 'Wroclaw', '51-200', 'Stworza 15', 'Mateusz Taneczny', 'szpital'),
                ( 23080134521 , 'Mikolaj', 'Szlachetny', 'Wroclaw', '51-200', 'Stworzona 2/3', 'Anna Szlachetna', 'ambulatoryjna')]
    cur.executemany("""INSERT INTO pacjenci(pesel, imie, nazwisko, miejscowosc, kod_pocztowy, ulica, krewny, forma_opieki)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", pacjenci)
    conn.commit()

def data_entry_oddzialy_pacjenci():
    oddzialy_pacjenci = [( 1 , 95213846558 , 1 , 1 ),
                         ( 2 , 53767545478 , 2 , 6 ),
                         ( 5 , 85128648985 , 14 , 3 ),
                         ( 2 , 45378354345 , 1 , 5),
                         ( 5 , 52486734565 , 13 , 3),
                         ( 3 , 24080109787 , 24 , 1 ),
                         ( 1 , 94111934221, 1 , 2 ),
                         ( 2 , 53767545478 , 5 , 1 ),
                         ( 2 , 91010214352 , 1 , 4),
                         ( 2 , 53767545478 , 5 , 1 ),
                         ( 2 , 53767545478 , 5 , 1 ),
                         ( 1 , 94111934221, 5, 3),
                         ( 1 , 4080109787, 4, 1),
                         ( 1 , 94111934221, 4, 2)]
    cur.executemany("""INSERT INTO oddzialy_pacjenci(oddzialynumer, pacjencipesel, numer_pokoju, numer_lozka)
                    VALUES(?, ?, ?, ?)""", oddzialy_pacjenci)
    conn.commit()

def data_entry_pacjenci_srodki_higieniczne():
    srodki_higieniczne = [( 95213846558 , 4 , '2018-09-5' , '12:45', 6 ),
                          ( 76121613548 , 2 , '2018-12-03' , '11:18' , 2 ),
                          ( 45378354345 , 1 , '2018-11-30' , '9:58' , 5 ),
                          ( 76543867343 , 3 , '2018-12-17' , '23:30' , 15 ),
                          ( 52486734565 , 2 , '2018-12-14' , '14:20' , 4 ),
                          ( 78274538745 , 4 , '2018-10-25' , '17:15' , 16 ),
                          ( 95213846558 , 2 , '2018-09-14' , '6:25' , 18 ),
                          ( 45378354345 , 3 , '2018-11-28' , '7:40' , 20 ),
                          ( 24080109787 , 5 , '2019-01-30' , '17:40', 1),
                          ( 94111934221 , 5 , '2019-01-20' , '9:18', 2),
                          ( 85128648985 , 5 , '2018-12-12' , '10:03', 1),
                          ( 23080134521 , 5 , '2019-01-03' , '10:30', 1),
                          ( 23080134521 , 5 , '2019-02-03' , '15:40', 5)]
    cur.executemany("""INSERT INTO pacjenci_srodki_higieniczne(PACJENCIpesel, srodki_higienicznenumer, data, godzina, ilosc)
                    VALUES(?, ?, ?, ?, ?)""", srodki_higieniczne)
    conn.commit()

def data_entry_wizyty():
    wizyty = [(1,'2018-10-23', 'T', 6, 1),(2,'2017-05-23', 'T', 9, 5),
              (3,'2018-04-13', 'T', 16, 3),(4,'2019-01-03', 'T', 20, 21),
              (13,'2018-12-13', 'T', 13, 22)]
    cur.executemany("""INSERT INTO wizyty(numer_wizyty, data, recepta, chorobyidchoroby, skierowaniaid_skierowania)
                    VALUES(?, ?, ?, ?, ?)""", wizyty)

    wizyty1 = [(5,'2017-05-23', 'N'),(6,'2018-03-25', 'N'),
               (7,'2015-04-10', 'N'),(8,'2015-05-20', 'N'),
               (9,'2015-06-21', 'N'),(10,'2015-04-11', 'N'),
               (11,'2015-01-01', 'N'),(14,'2015-10-17', 'N')]
    cur.executemany("""INSERT INTO wizyty(numer_wizyty, data, recepta)
                    VALUES(?, ?, ?)""", wizyty1)

    wizyty2 = [(12,'2019-02-03', 'T', 20),(15,'2018-12-12', 'T', 20),
               (16,'2018-12-10', 'T', 11),(17,'2018-12-12', 'T', 9),
               (18,'2019-01-30', 'T', 20)]
    cur.executemany("""INSERT INTO wizyty(numer_wizyty, data, recepta, chorobyidchoroby)
                    VALUES(?, ?, ?, ?)""", wizyty2)
    conn.commit()

def data_entry_typy_badan():
    typy_badan = [(1, 1), (2, 2), (3, 3), (4, 4), (26, 5)]
    typy_badan2 = [(5, 1), (6, 2), (7, 3), (8, 4),
                   (9, 5), (10, 6), (11, 7), (12, 8),
                   (13, 9), (14, 10), (15, 11), (16, 12),
                   (17, 13), (21, 14), (22, 15), (23, 16),
                   (24, 17), (25, 18)]
    typy_badan3 = [(18, 1), (19, 2), (20, 3)]
    cur.executemany("""INSERT INTO typy_badan(id_typ_badania, testy_medycznenumer_testu)
                    VALUES(?, ?)""", typy_badan)
    cur.executemany("""INSERT INTO typy_badan(id_typ_badania, wizytynumer_wizyty)
                    VALUES(?, ?)""", typy_badan2)
    cur.executemany("""INSERT INTO typy_badan(id_typ_badania, zabieginumer_zabiegu)
                    VALUES(?, ?)""", typy_badan3)
    conn.commit()

def data_entry_lekarze_pacjenci():
    lekarze_pacjenci = [(5, 76543867343, 1), (6, 45378354345, 2), (5, 78274538745, 3),
                        (1, 52486734565, 5), (2, 53767545478, 6), (7, 45378354345, 7),
                        (8, 76543867343, 15), (5, 85128648985, 9),
                        (3, 95213846558, 10), (4, 53767545478, 11), (3, 85128648985, 12),
                        (3 ,76543867343 , 17), (5, 45378354345, 18), ( 5, 45378354345, 19),
                        (11 ,78274538745 , 13), (9,52486734565 ,14), (10 , 53767545478, 16),
                        (10 ,53767545478 ,20 ), (5, 23080134521, 8), (5, 23080134521, 4),
                        (9, 94111934221, 21), (9, 3080134521, 22), (10, 4080109787, 23),
                        (10, 94111934221, 24), (10, 4080109787, 25)]
    cur.executemany("""INSERT INTO lekarze_pacjenci(lekarzeidlekarza, pacjencipesel, typy_badanid_typ_badania)
                    VALUES(?, ?, ?)""", lekarze_pacjenci)
    conn.commit()

                    
    
create_table()
data_entry_oddzialy()
data_entry_stanowiska()
data_entry_choroby()
data_entry_skierowania()
data_entry_zabiegi()
data_entry_srodki_higieniczne()
data_entry_pracownicy()
data_entry_lekarze()
data_enty_oddzialy_pracownicy()
data_entry_testy_medyczne()
data_entry_pacjenci()
data_entry_oddzialy_pacjenci()
data_entry_pacjenci_srodki_higieniczne()
data_entry_wizyty()
data_entry_typy_badan()
data_entry_lekarze_pacjenci()



