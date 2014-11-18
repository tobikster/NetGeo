NetGeo
======
Badanie fizycznej odległości pomiędzy węzłami w Internecie

# 1. Podręcznik użytkownika
Program NetGeo jest bardzo intuicyjny w użyciu.
Jedynym wymaganiem jest przygotowanie pliku wejściowego, w postaci adresów IP jakie mają zostać przebadane.
Każdy adres musi być w osobnym wierszu.

Następnie, program uruchamiany jest poprzez wywołanie komendy 
```
NetGeo <ścieżka do pliku wejściowego>
```

Rezultat działania programu domyślnie zapisywany jest w pliku result.csv, w lokalizacji, z jakiej został uruchomiony program.
Lokalizację oraz nazwę pliku wyjściowego można zmienić korzystająć z opcji --output:
```
NetGeo --output <nazwa pliku wyjściowego> <nazwa pliku wejściowego>
```

Możliwa jest również zmiana domyślnego czasu oczekiwania na odpowiedzi podczas badania ping za pomocą parametru --pingTime
```
NetGeo --pingTime <czas oczekiwania w sekundach> <nazwa pliku wejściowego>
```

Opis dodatkowych opcji programu dostępny jest po wykonaniu polecenia.
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
Następnie należy wyprodukować plik wykonywalny za pomocą skryptu *compile*, który znajduje się w głównym katalogu projektu.
```
cd <ścieżka do repozytorium>
./compile
```
Program zostanie zainstalowany w katalogu *bin* znajdującym się w folderze domowym bieżącego użytkownika.
Dzięki temu będzie możliwe używanie go prosto z lini komend (bash)

# 3. Podręcznik programisty
Program napisany jest z w języku **Python**, jako zbiór funkcji.
Główną funkcją jest **main()**, która wykonuje zasadniczy kod programu.

Poszczególne funkcjonalności wykonywane są przez osobne funkcje, każda z nich odpowiada za atamową część programu.

Aby dodać do programu **NetGeo** kolejną funkcjonalność, należy dopisać funkcję, która ją realizuje a następnie uwzględnić ją w funkcji **main()**

**main()** odpowiedzialna jest również za wczytywanie danych z pliku wejściowego oraz zapisywanie wyników do pliku wyjściowego.

Na chwilę obecną nie jest przewidziane wspieranie mechanizmu obsługi wtyczek.