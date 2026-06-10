=========================================
Sprawozdanie: Projektowanie bazy danych
=========================================

:Autor: Michał Kraus

Wybór zagadnienia, opis procesów i danych
=========================================

**Wybrane zagadnienie:**  
System obsługi sprzedaży internetowej dla sklepu NautSA specjalizującego się w podzespołach elektronicznych (płyty główne, pamięci RAM, obudowy, procesory, karty graficzne itp.). Projekt obejmuje ewidencjonowanie klientów (zarówno osób fizycznych, jak i firm), katalog produktów, zarządzanie stanami magazynowymi, obsługę zamówień wraz z fakturowaniem oraz śledzenie płatności.

**Opis procesów i więzy integralności:**

Głównym procesem biznesowym jest cykl życia zamówienia.

* **Rejestracja klienta:**  
  Klient zakłada konto, podając dane osobowe (imię, nazwisko, email, telefon) lub dane firmy (nazwa, NIP). Adresy (dostawowy, fakturowy, korespondencyjny) są przypisywane do konta. Więzy integralności: unikalny adres email, a dla osób fizycznych obowiązkowy PESEL, dla firm – NIP i nazwa firmy (wzajemne wykluczanie).

* **Zarządzanie produktami:**  
  Każdy produkt posiada nazwę, producenta, cenę jednostkową, typ (enum: płyta główna, pamięć RAM, procesor, karta graficzna, dysk, obudowa, zasilacz, inne) oraz bieżący stan magazynowy. Stan magazynowy nie może być ujemny.

* **Składanie zamówienia:**  
  Klient tworzy zamówienie, wybierając produkty i ich ilości. Dla każdej pozycji zamówienia zapisywana jest cena z chwili zakupu (cena historyczna), co zabezpiecza przed późniejszymi zmianami cennika. Zamówienie otrzymuje status (przyjęte, opłacone, w realizacji, wysłane, dostarczone, anulowane) oraz metodę płatności (przelew, karta, blik, za pobraniem). Całkowita wartość zamówienia jest obliczana i przechowywana.

* **Płatności i faktury:**  
  Do zamówienia może zostać wystawiona faktura (relacja 1:1). Faktura posiada unikalny numer, datę wystawienia, kwotę brutto oraz ścieżkę do pliku PDF. Płatność jest rejestrowana poprzez metodę płatności i status (brak osobnej tabeli – atrybuty w zamówieniu).

**Wykaz gromadzonych danych:**

* **Klient:** typ (osoba/firma), imię, nazwisko, nazwa firmy, email, telefon, PESEL, NIP, data utworzenia konta.
* **Adres:** ulica, numer domu, numer mieszkania, miasto, kod pocztowy, kraj, typ adresu (dostawowy/fakturowy/korespondencyjny).
* **Produkt:** nazwa, producent, opis, cena jednostkowa, stan magazynowy, typ produktu, data dodania.
* **Zamówienie:** data złożenia, data wysyłki, status, metoda płatności, wartość całkowita.
* **Pozycja zamówienia:** liczba sztuk, cena w momencie zakupu.
* **Faktura:** numer faktury, data wystawienia, kwota brutto, ścieżka pliku.

Prototyp CSV
============

W celu weryfikacji kompletności i spójności danych przygotowano płaski (zdenormalizowany) plik CSV obrazujący pojedyncze zamówienie wraz z danymi klienta, adresem i produktami.

.. code-block:: csv

    typ_klienta,imie,nazwisko,nazwa_firmy,email,telefon,pesel,nip_firmy,ulica,numer_domu,miasto,kod_pocztowy,typ_adresu,nazwa_produktu,producent,cena_jednostkowa,typ_produktu,ilosc,cena_historyczna,data_zlozenia,status_zamowienia,metoda_platnosci,numer_faktury,kwota_brutto
    osoba_fizyczna,Jan,Kowalski,,jan.kow@example.com,501234567,90010112345,,Kwiatowa,15,Warszawa,00-001,dostawowy,Płyta główna B450,ASUS,399.99,plyta_glowna,1,399.99,2024-01-15 10:30:00,dostarczone,przelew,FV/2024/01/0001,399.99
    firma,,,IT-Solutions,biuro@it.pl,503456789,,1234567890,Morska,8,Gdańsk,80-001,dostawowy,Karta graficzna RTX 3060,NVIDIA,1499.99,karta_graficzna,2,1499.99,2024-02-20 14:15:00,wysłane,karta,FV/2024/02/0015,2999.98

Model konceptualny (pojęciowy)
==============================

Na podstawie analizy procesów i przykładowych danych zdefiniowano model pojęciowy w notacji encja-relacja (ER). Poniżej przedstawiono encje, ich atrybuty, związki oraz zidentyfikowane pułapki.

Zidentyfikowane encje
---------------------

* **KLIENT** – podmiot dokonujący zakupów (osoba fizyczna lub firma).
* **ADRES** – miejsce dostawy, fakturowania lub korespondencji.
* **PRODUKT** – towar oferowany w sklepie.
* **ZAMÓWIENIE** – transakcja zakupu zawierająca informacje o dostawie i płatności.
* **POZYCJA ZAMÓWIENIA** – encja słaba rozwijająca relację wiele-do-wielu między Zamówieniem a Produktem.
* **FAKTURA** – dokument rozliczeniowy przypisany do zamówienia.

Atrybuty encji
--------------

**KLIENT**
- `id_klienta` (identyfikator numeryczny, klucz główny)
- `typ_klienta` (wartość: osoba_fizyczna, firma)
- `imię`, `nazwisko` (dla osób fizycznych)
- `nazwa_firmy` (dla firm)
- `email` (unikalny)
- `telefon`
- `PESEL` (unikalny, tylko dla osób fizycznych)
- `NIP` (unikalny, tylko dla firm)
- `data_utworzenia` (data rejestracji)

**ADRES**
- `id_adresu` (klucz główny)
- `ulica`, `numer_domu`, `numer_mieszkania`
- `miasto`, `kod_pocztowy`, `kraj`
- `typ_adresu` (dostawowy, fakturowy, korespondencyjny)

**PRODUKT**
- `id_produktu` (klucz główny)
- `nazwa`, `producent`, `opis`
- `cena_jednostkowa` (kwota)
- `stan_magazynowy` (liczba całkowita)
- `typ_produktu` (kategoria)
- `data_dodania`

**ZAMÓWIENIE**
- `id_zamowienia` (klucz główny)
- `data_zlozenia`, `data_wysylki`
- `status` (przyjęte, opłacone, w realizacji, wysłane, dostarczone, anulowane)
- `metoda_platnosci` (przelew, karta, blik, za pobraniem)
- `wartosc_calkowita` (kwota)

**POZYCJA ZAMÓWIENIA** (encja słaba)
- `liczba_sztuk` (dodatnia liczba całkowita)
- `cena_w_momencie_zakupu` (kwota historyczna)

**FAKTURA**
- `id_faktury` (klucz główny)
- `numer_faktury` (unikalny)
- `data_wystawienia`
- `kwota_brutto` (kwota)
- `sciezka_pliku` (ścieżka do pliku PDF)

Opis związków (kardynalności)
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 20 15 35

   * - Encja 1
     - Relacja
     - Encja 2
     - Kardynalność
     - Uzasadnienie

   * - KLIENT
     - posiada
     - ADRES
     - 1 : N
     - Klient może mieć wiele adresów, każdy adres należy do jednego klienta.

   * - KLIENT
     - składa
     - ZAMÓWIENIE
     - 1 : N
     - Jeden klient może złożyć wiele zamówień; zamówienie przypisane jest do jednego klienta.

   * - ZAMÓWIENIE
     - zawiera
     - POZYCJA ZAMÓWIENIA
     - 1 : N
     - Zamówienie może zawierać wiele pozycji.

   * - PRODUKT
     - występuje w
     - POZYCJA ZAMÓWIENIA
     - 1 : N
     - Produkt może pojawić się w wielu pozycjach różnych zamówień.

   * - ZAMÓWIENIE
     - jest podstawą
     - FAKTURA
     - 1 : 1 (opcjonalnie)
     - Zamówienie może mieć maksymalnie jedną fakturę; faktura dotyczy jednego zamówienia.

Pułapki w projektowaniu (niepoprawne związki)
---------------------------------------------

**Pułapka wiatraka (chasm trap):**  
Gdyby bezpośrednio połączono encje **KLIENT** i **PRODUKT** relacją "kupuje", utracona zostałaby informacja o kontekście transakcji – nie wiadomo, w którym zamówieniu i w jakiej cenie produkt został nabyty. Podobnie, pominięcie encji **POZYCJA ZAMÓWIENIA** i połączenie ZAMÓWIENIE–PRODUKT jako M:N spowodowałoby niemożność przechowania liczby sztuk i ceny historycznej.

**Pułapka rozwidlonej ścieżki (fan trap):**  
Gdyby **ADRES** był połączony bezpośrednio z **ZAMÓWIENIEM** i jednocześnie z **KLIENTEM**, mogłoby to prowadzić do niejednoznaczności – adres dostawy dla zamówienia powinien być wybrany spośród adresów klienta. W modelu rozwiązano to przez przypisanie zamówieniu konkretnego adresu (`adres_dostawy_id`) będącego kluczem obcym do tabeli ADRES, co nie generuje niejednoznaczności.

Encja słaba
-----------

**POZYCJA ZAMÓWIENIA** jest encją słabą, ponieważ nie może istnieć bez zarówno **ZAMÓWIENIA**, jak i **PRODUKTU**. Jej klucz główny `id_pozycji` jest sztuczny, ale encja ta rozwiją relację M:N. Atrybuty `liczba_sztuk` i `cena_w_momencie_zakupu` są bezpośrednio zależne od pary (zamówienie, produkt).

Schemat w notacji Chena
-----------------------

Poniżej zamieszczono diagram związków encji w notacji Chena, obrazujący model konceptualny bazy danych sklepu NautSA.

.. figure:: /_static/diagram_koncepcyjny_model.png
   :align: center
   :alt: Diagram związków encji w notacji Chena

   Rysunek 1: Model konceptualny

Model logiczny i proces normalizacji
====================================

Przekształcono dane z postaci płaskiej (CSV) do postaci znormalizowanej – trzeciej postaci normalnej (3NF).

Etapy normalizacji
------------------

**Pierwsza postać normalna (1NF):**  
Wprowadzono sztuczne identyfikatory `id_zamowienia` i `id_produktu`. Każda komórka zawiera pojedynczą, atomową wartość. Zdefiniowano klucz główny złożony (`id_zamowienia`, `id_produktu`) dla encji Pozycja.

**Druga postać normalna (2NF):**  
Usunięto częściowe zależności funkcyjne od klucza złożonego:
- Atrybuty zależne tylko od `id_produktu` (nazwa, producent, cena, stan, typ) przeniesiono do tabeli **PRODUKT**.
- Atrybuty zależne tylko od `id_zamowienia` (data, status, metoda płatności, wartość całkowita, dane klienta, adres) przeniesiono do tabeli **ZAMÓWIENIE**.
- Atrybuty zależne od całego klucza (liczba sztuk, cena historyczna) pozostały w **POZYCJA ZAMÓWIENIA**.

**Trzecia postać normalna (3NF):**  
Usunięto zależności przechodnie:
- Z **ZAMÓWIENIA** wydzielono dane klienta do tabeli **KLIENT** (w tym dane firm/osób) oraz dane adresowe do tabeli **ADRES**.
- Z **PRODUKTU** nie wydzielano osobnej kategorii – `typ_produktu` jest atrybutem prostym (enum), nie tworzy nowej encji.
- **FAKTURA** została wydzielona jako osobna tabela ze względu na możliwość późniejszego wystawienia (opcjonalność).

Ostateczna struktura tabel (3NF)
--------------------------------

Otrzymano 6 tabel:

1. **klient**
2. **adres**
3. **produkt**
4. **zamowienie**
5. **pozycja_zamowienia** (encja asocjacyjna)
6. **faktura**

Model fizyczny bazy danych
==========================

Model fizyczny uwzględnia specyfikę dwóch docelowych silników: **PostgreSQL** (produkcyjny, zaawansowany) oraz **SQLite** (lekki, do testów lub zastosowań embedded). Różnice dotyczą typów danych, mechanizmów generowania kluczy głównych, obsługi typów wyliczeniowych (ENUM) oraz precyzji finansowej.

Model fizyczny dla PostgreSQL (skrót)
-------------------------------------

PostgreSQL oferuje bogaty zestaw typów danych dostosowanych do potrzeb aplikacji biznesowych:

- `SERIAL` – automatycznie inkrementowany klucz główny.
- `NUMERIC(10,2)` – precyzyjny typ dla kwot pieniężnych.
- `TIMESTAMPTZ` – data i czas wraz ze strefą czasową.
- Typy wyliczeniowe (`CREATE TYPE ... AS ENUM`) – dla pól o ściśle określonym zbiorze wartości.
- Ograniczenia `CHECK` – zapewniające integralność danych.
- Indeksy – zakładane na kluczach obcych i często używanych kolumnach.

Pełny kod definicji schematu `nautsa` dla PostgreSQL znajduje się w załączonym pliku `sqlcodeElectronicshop.sql`.

Model fizyczny dla SQLite
-------------------------

SQLite jest silnikiem lekkim, często stosowanym w aplikacjach mobilnych, embedded oraz w testach jednostkowych. Dla projektu NautSA przygotowano w pełni funkcjonalny skrypt tworzący bazę danych z zachowaniem wszystkich więzów integralności.

**Kluczowe cechy implementacji w SQLite:**

- Włączenie obsługi kluczy obcych na początku skryptu: `PRAGMA foreign_keys = ON;` – bez tego SQLite ignoruje klauzule `FOREIGN KEY`.
- `INTEGER PRIMARY KEY AUTOINCREMENT` – zamiennik dla `SERIAL`; zapewnia automatyczne generowanie unikalnego identyfikatora.
- `NUMERIC` – typ dla kwot pieniężnych (lepszy niż `REAL`, unika błędów zaokrągleń).
- `DATETIME` – dla dat i czasów (akceptuje `CURRENT_TIMESTAMP`).
- `TEXT` – dla napisów oraz dla typów wyliczeniowych (SQLite nie obsługuje natywnie `ENUM` – zastępuje się go ograniczeniem `CHECK` na kolumnie `TEXT`).
- Ograniczenia `CHECK` – szczegółowo zdefiniowane dla każdej tabeli (m.in. wzajemne wykluczanie PESEL/NIP, dodatnia liczba sztuk, nieujemny stan magazynowy, poprawny status zamówienia).
- Indeksy – zakładane na kluczach obcych (`id_klienta`, `id_zamowienia`, `id_produktu`) oraz na często wyszukiwanych kolumnach (`status`, `typ_produktu`).

**Przykładowy fragment kodu dla SQLite (tabela klient):**

```sql
CREATE TABLE klient (
    id_klienta INTEGER PRIMARY KEY AUTOINCREMENT,
    typ_klienta TEXT NOT NULL
        CHECK (typ_klienta IN ('osoba_fizyczna', 'firma')),
    imie TEXT,
    nazwisko TEXT,
    nazwa_firmy TEXT,
    email TEXT NOT NULL UNIQUE,
    telefon TEXT,
    pesel TEXT UNIQUE,
    nip_firmy TEXT UNIQUE,
    data_utworzenia DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (typ_klienta = 'osoba_fizyczna'
            AND imie IS NOT NULL AND nazwisko IS NOT NULL
            AND pesel IS NOT NULL AND nip_firmy IS NULL
            AND nazwa_firmy IS NULL)
        OR
        (typ_klienta = 'firma'
            AND nazwa_firmy IS NOT NULL AND nip_firmy IS NOT NULL
            AND pesel IS NULL)
    )
);