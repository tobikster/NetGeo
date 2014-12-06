NetGeo
======
Badanie fizycznej odległości pomiędzy węzłami w Internecie

# 1. Podręcznik użytkownika
Program NetGeo jest narzędziem służącym do badania zależności pomiędzy fizyczną odległością węzłów w Internecie, a innymi wielkościami, takimi jak średni czas RTT oraz czas ściągania pliku z serwera.
Program posiada jednynie interfejs konsolowy.

Danymi wejściowymi programu jest plik tekstowy zawierający badane adresy IP - każdy adres w nowym wierszu.
Wyniki eksperymentu zapisywane są w formacie CSV - wartości oddzielone średnikami.
W kolejnych kolumnach pliku zapisane są:
- adres IP badanego węzła
- jego fizyczna lokalizacja (podana w radianach)
- odległość od hosta do wyznaczonego położenia komputera, na którym zostało uruchomione narzędzie NetGeo
- średni czas RTT
- czas pobierania domyślnego pliku z serwera (podzielony przez jego długość w celu normalizacji)

Opis opcji, z jakimi może zostać uruchomione narzędzie jest dostępny po wydaniu polecenia

```
NetGeo --help
```

Program wymaga jednego argumentu - ścieżki do pliku z adresami IP.
Uruchomienie następuje po wydaniu polecenia

```
NetGeo <ścieżka do pliku>
```

Rezultat działania programu zapisywany jest w pliku *result.csv*, w lokalizacji, z jakiej został uruchomiony program.

## Opcje dodatkowe
Wywołując program z dodatkowymi opcjami można zmienić domyślne wartości parametrów:
- Lokalizację oraz pliku wynikowego można zmienić korzystająć z opcji --output:

```
NetGeo --output <nazwa pliku wyjściowego> <nazwa pliku wejściowego>
```

- Czas badania narzędziem PING można zmienić z domyślnej wartości 5 s za pomocą opcji --pingTime

```
NetGeo --pingTime <czas w sekundach> <ścieżka do pliku>
```

Opis wszystkich opcji programu dostępny jest po wykonaniu polecenia.

```
NetGeo --help
```

# 2. Podręcznik administratora
NetGeo dostępny jest jedynie na platformę Linux, jednak ewentualne portowanie na inne platformy nie powinno przysparzać problemów.
Szczegóły opisane są w podręczniku programisty.

Aby zainstalować narzędzie, wystarczy pobrać kod źródłowy, np. za pomocą polecenia
 
```
git clone https://github.com/tobikster/NetGeo.git
```

Instalacja narzędzia wykonywana jest za pomocą dołączonego do projektu skryptu **install**, który należy wywołać poleceniem

```
cd <ścieżka do repozytorium>
./install.sh
```

Program zostanie zainstalowany w katalogu *~/bin*.
Dzięki temu będzie możliwe używanie go prosto z lini komend (bash) - jeżeli katalog ten jest uwzględniony w zmiennej środowiskowej PATH.
Jeśli tak nie jest, należy dodać katalog ~/bin do zmiennej PATH, np. dodając do pliku ~/.profile linię

```
export PATH="$HOME/bin:$PATH"
```

Do działania programu wymagane jest narzędzie PING (dostępne domyślnie na większości systemów Linux).
Aby skrypt instalacyjny zadziałał poprawnie, wymagany jest program zip.

# 3. Podręcznik programisty
Program napisany jest z w języku **Python**, jako zbiór funkcji.
Główną funkcją jest **main()**, która wykonuje zasadniczy kod programu.

Poszczególne funkcjonalności wykonywane są przez osobne funkcje, każda z nich odpowiada za atamową część programu.

Aby dodać do programu **NetGeo** kolejną funkcjonalność, należy dopisać funkcję, która ją realizuje a następnie uwzględnić ją w funkcji **main()**

**main()** odpowiedzialna jest również za wczytywanie danych z pliku wejściowego oraz zapisywanie wyników do pliku wyjściowego.

Na chwilę obecną nie jest przewidziane wspieranie mechanizmu obsługi wtyczek.
