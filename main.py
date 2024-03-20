import pandas as pd 
import matplotlib.pyplot as plt
import datetime as dt

def EMA(okres, dane, aktualna):
    alfa = 2 / (okres + 1)
    baza = 1 - alfa
    licznik = dane[aktualna]
    mianownik = 1.0

    for i in range(1, okres + 1):
        licznik+=baza ** i * dane[aktualna + i]
        mianownik+=baza ** i
    return licznik / mianownik
    

def MACD(dane,aktualna):
    EMA12 = EMA(12, dane, aktualna)
    EMA26 = EMA(26, dane, aktualna)
    return EMA12 - EMA26

def SIGNAL(MACD_series, index):
	return EMA(9, MACD_series, index)

plik = "WIG20"
N = 1000
ramka = pd.read_csv(plik + ".csv")  #zczytywanie danych z pliku
df = ramka.tail(N) 
dane = df["Zamkniecie"].tolist()
daty = df["Data"].tolist()
dane.reverse()
MACD_w = []
for i in range(0,N - 26):   
    MACD_w.append(MACD(dane, i))

SIGNAL_w = []

for i in range(0,N - 26 - 9):   
    SIGNAL_w.append(SIGNAL(MACD_w, i))

for i in range(0, 9):       #pozbywanie się danych, których nie wykorzysta się na wykresach
    MACD_w.pop()

for i in range(0, 35):
    daty.pop()

for i in range(0, 35):
    dane.pop()

MACD_w.reverse()
SIGNAL_w.reverse()
dane.reverse()

x = []
for i in range(0, 965):
    x.append(i)

x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in daty]   #tworzenie i wyświetlanie wykresów
fig = plt.figure()
fig.canvas.set_window_title('Cena zamknięcia') 
plt.plot(x,dane, "k")
plt.xticks(rotation = 15)
plt.ylabel("Cena zamknięcia") 
plt.title(plik)


fig2, ax = plt.subplots()
fig2.canvas.set_window_title('MACD/SIGNAL') 
plt.ylabel("Wartość") 
ax.plot(x, MACD_w,"b", label="MACD")
ax.plot(x, SIGNAL_w,"r", label="SIGNAL")
plt.xticks(rotation = 15)
plt.title(plik)
leg = fig2.legend();
plt.show()


srodki = 1000   #algorytm kupna/sprzedaży
print("Kapitał początkowy:",srodki)
transakcje = []

if MACD_w[0] > SIGNAL_w[0]:
    poczatek = 0 
    flaga = 0
else:
    poczatek = 1 
    flaga = 1

i = 1
while i != N - 36:
    tmp = flaga
    if MACD_w[i] >= SIGNAL_w[i]:
        flaga = 0
    else:
        flaga = 1

    if flaga != tmp:
        transakcje.append(dane[i])
    i+=1

if poczatek == 0:
    for i in range(0,len(transakcje) - 1):
        if(i % 2 == 1):
            srodki = srodki * transakcje[i + 1] / transakcje[i]
    
else:
    for i in range(0,len(transakcje) - 1):
        if(i % 2 == 0):
          srodki = srodki * transakcje[i + 1] / transakcje[i]
             
print("Kapitał końcowy:", srodki)