import sqlite3
from tkinter import *
import tkinter as tk


db=sqlite3.connect('baza.db')
cur = db.cursor()

def Zapytania(numzap):
    print(numzap)
    if (numzap==0):
        cur.execute("""select nazwisko, pesel from pacjenci
                join pacjenci_srodki_higieniczne as psh on pesel=psh.PACJENCIpesel
                join srodki_higieniczne on SRODKI_HIGIENICZNEnumer=numer
                join lekarze_pacjenci as lp on pesel=lp.pacjencipesel
                join typy_badan on typy_badanid_typ_badania=id_typ_badania
                join wizyty on wizytynumer_wizyty= numer_wizyty
                join choroby as ch on chorobyidchoroby=ch.id_choroby
                join lekarze on lp.lekarzeidlekarza=idlekarza
                where ch.nazwa='Cukrzyca' and 
                lekarze.specjalizacja='Pediatra' and
                srodki_higieniczne.nazwa = 'cetol-2' """)

    elif (numzap==1):
        cur.execute("""select distinct pacjenci.nazwisko as pacjenci from pacjenci
                join lekarze_pacjenci as lp on pesel=lp.pacjencipesel
                join lekarze on lekarzeidlekarza=idlekarza
                join pracownicy as p on pracownicyidpracownika=p.idpracownika
                where p.nazwisko in ('Samuel', 'Pajak', 'Gaska')
                order by pacjenci.nazwisko """)

    elif (numzap==2):
        cur.execute("""select distinct nazwisko, count(pacjenci.nazwisko) as count from pacjenci
                join oddzialy_pacjenci as op on pesel=op.pacjencipesel
                where op.oddzialynumer = 1 and
                pacjenci.nazwisko like 'S%'
                group by pacjenci.nazwisko
                having count(pacjenci.nazwisko)>2 """)

    elif (numzap==3):
        cur.execute("""select nazwisko, imie, count(numer_wizyty) as count from pracownicy
                join lekarze on idpracownika=pracownicyidpracownika
                join lekarze_pacjenci on idlekarza=lekarzeidlekarza
                join typy_badan on TYPY_BADANid_typ_badania= id_typ_badania
                join wizyty on wizytynumer_wizyty=numer_wizyty
                where strftime('%Y', data)>'2014' and strftime('%Y', data)<'2016'
                group by imie
                order by count(numer_wizyty)""")

    elif (numzap==4):
        cur.execute("""select nazwisko, round(pensja * 1.15,0) as pensja from pracownicy """)

    elif (numzap==5):
        cur.execute("""select imie, nazwisko, pensja, nazwa_stanowiska from pracownicy
                join stanowiska as s on stanowiskanumer=s.numer
                where pensja > 40 and stanowiskanumer != 1""")

    elif (numzap==6):
        cur.execute("""select nazwa, count(*) as count from pracownicy
                join oddzialy_pracownicy as op on idpracownika=op.pracownicyidpracownika
                join oddzialy on op.oddzialynumer=numer
                where miesiac='styczen'
                group by nazwa
                order by nazwa""")

    elif (numzap==7):
        cur.execute("""select distinct p.nazwisko as nazwisko, nazwa_stanowiska from pracownicy as p
                join stanowiska as s on p.stanowiskanumer=s.numer
                join pracownicy as r on p.pensja < r.pensja*0.5 where r.stanowiskanumer == 1""")
        
    elif (numzap==8):
         cur.execute("""select o.nazwa as nazwa, count(p.pesel) as count from oddzialy as o
                join oddzialy_pacjenci as op on o.numer=op.oddzialynumer
                join pacjenci as p on op.pacjencipesel=p.pesel
                join pacjenci as r on op.pacjencipesel=r.pesel
                group by nazwa
                having count(p.pesel) > ( count(r.pesel) / count(o.numer) ) """)

    elif (numzap==9):
        cur.execute("""select nazwa, sum(pensja) as sum from oddzialy
                join oddzialy_pracownicy as op on numer=op.oddzialynumer
                join pracownicy on op.pracownicyidpracownika=idpracownika
                where miesiac='styczen'
                order by pensja""")


    Zapytanie = cur.fetchall()
    return Zapytanie


class Widget(tk.Frame):
    def __init__(self, root = None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.init_Widget()
        self.frame = tk.Frame(root)
        self.frame.grid()
      

        self.bottomF = tk.Frame(root)
        self.bottomF.grid(sticky='S')
        self.resultF = tk.Frame(root)
        self.resultF.grid()

    def init_Widget(self):
        self.root.title("Selly Oak Clinic")
        self.grid()
        
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        #ZAPYTANIA PROJEKTOWE
        View = tk.Menu(menu)
        menu.add_cascade(label="Zapytania Projektowe", menu = View)
        View.add_command(label="Zapytania",
                         command=self.PROZAP)

        #Zamknięcie
        Close = tk.Menu(menu)
        menu.add_cascade(label= "Zamykanie", menu = Close)
        Close.add_command(label= "Zamknij",
                         command= root.destroy)



    def clear_all(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        for widget in self.bottomF.winfo_children():
            widget.destroy()
        for widget in self.resultF.winfo_children():
            widget.destroy()


    def PROZAP(self):
        self.clear_all()
        self.zap = ['1) Nazwiska i daty urodzeń pacjentów, którym przepisano lek "Cetol-2", '
                        'cierpiących na cukrzycę, którzy odbyli jedną lub więcej wizyt u lekarza '
                        'pracującego na oddziale pediatrycznym.',
                        '2) Lista pacjentów, którzy odwiedzili jednego lub więcej lekarzy ogólnych: "Dr Pająk "'
                        ',"Dr. Samuel "i" Dr. Gąska ". (Wymień tylko nazwiska pacjentów posortowane'
                        'alfabetycznie - nie są wymagane żadne inne szczegóły)',
                        '3) Łączna liczba pacjentów, których nazwisko zaczyna się na literę "S", '
                        'i którzy złożyli więcej niż 2 wizyty u lekarza ogólnego.',
                        '4) Nazwisko imię lekarza, który miał najmniej wizyt pacjentów w 2015 roku.',
                        '5) Wyświetl nazwiska i stawki godzinowe powiększone o 15% dla wszystkich '
                        'pracowników z pensją naliczaną godzinowo i zaokrąglone do liczb całkowitych.',
                        '6) Dla każdego pracownika na zatrudnionego na stałym etacie wyświetl wartość jego'
                        'płacy podstawowej, ale ukryj wartość płacy jeśli etat pracownika to ordynator.',
                        '7) Dla każdego oddziału wyświetl liczbę zatrudnionych w nim pracowników.',
                        '8) Wyświetl nazwiska i etaty pracowników których rzeczywiste zarobki nie przekraczają '
                        '50% zarobków ich szefów.',
                        '9) Podaj nazwę oddziału oraz liczbę pacjentów, w których ilość pacjentów przekracza '
                        'średnią ilość pacjentów na oddział w szpitalu.',
                        '10) Wyświetl nazwę oddziału wypłacającego miesięcznie swoim pracownikom ze stałą'
                        'pensją najwięcej pieniędzy.'
                        ]
        for i in range(len(self.zap)):
            
            label_1 = tk.Label(self.frame,text=self.zap[i]).grid(column=0,row=1+i)
            button_1 = tk.Button(self.frame,text = ("Zapytanie", i+1), command = lambda i=i: self.which_zap(i)).grid(row=1+i, column = 1)

    def Wynik(self,results,mheight=10):
        
        result = tk.Listbox(self.resultF)
        result.grid(row = 2,column = 0)

        listbox_scroll = tk.Scrollbar(self.resultF, orient="vertical", command=result).grid(row=2, column=1)
        
        
        for x in results:
            result.insert(END, x)            
           


    def which_zap(self,i):
        self.clear_all()
        label_1 = tk.Label(self.frame,text=self.zap[i]).grid(column=0, row=1)

        results = Zapytania(i)
        self.Wynik(results)


    def COMBO(self,txt,res,mrow=0):
        label_1= tk.Label(self.frame, text=txt).grid(column = 0, row = 0 + mrow)

        box = ttk.Combobox(self.frame, values=res, width = 100).grid(column = 0, row = 1 + mrow)
        box.bind('<<COMBOBOXSELECTED>>', self.wybrany)
        self.all_comboboxes.append(box)

    def wybrany(self,event= None):
        print('_________________________')
        if event:
            print("event.widget:", event.widget.get())  

        
##########################################################################################
root = tk.Tk()
root.geometry("1400x500")

apli = Widget(root)

root.mainloop()

db.close()
        
