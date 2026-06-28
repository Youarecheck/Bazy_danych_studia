
Rozdział 3: Modelowanie i implementacja bazy danych
===================================================

W niniejszym rozdziale przedstawiono proces projektowania relacyjnej bazy danych dla sklepu internetowego NautSA specjalizującego się w sprzedaży podzespołów komputerowych i elektronicznych.

Omówiono model konceptualny, model logiczny, proces normalizacji oraz implementację fizyczną bazy danych w dwóch systemach zarządzania bazami danych: PostgreSQL oraz SQLite.

Model konceptualny (pojęciowy)
------------------------------

Na podstawie analizy procesów i przykładowych danych zdefiniowano model pojęciowy w notacji encja-relacja (ER). Poniżej przedstawiono encje, ich atrybuty, związki oraz zidentyfikowane pułapki.

Zidentyfikowane encje
~~~~~~~~~~~~~~~~~~~~~

* **KLIENT** – podmiot dokonujący zakupów (osoba fizyczna lub firma).
* **ADRES** – miejsce dostawy, fakturowania lub korespondencji.
* **PRODUKT** – towar oferowany w sklepie.
* **ZAMÓWIENIE** – transakcja zakupu zawierająca informacje o dostawie i płatności.
* **POZYCJA ZAMÓWIENIA** – encja asocjacyjna realizująca relację wiele-do-wielu pomiędzy encjami ZAMÓWIENIE i PRODUKT oraz przechowująca dodatkowe informacje dotyczące transakcji, takie jak liczba sztuk i cena historyczna.
* **FAKTURA** – dokument rozliczeniowy przypisany do zamówienia.

Atrybuty encji
~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


Diagram modelu konceptualnego
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Poniżej zamieszczono diagram związków encji, obrazujący model konceptualny bazy danych sklepu NautSA.

.. figure:: /_static/diagram_koncepcyjny_model.png
   :alt: Diagram związków encji w notacji Chena
   :align: center
   :width: 80%
   :scale: 70%
   

   Rysunek 3.1: Model konceptualny w notacji Chena.






Model logiczny
--------------




Po przeprowadzeniu procesu normalizacji płaskiej struktury danych otrzymano zestaw sześciu tabel spełniających wymagania trzeciej postaci normalnej (3NF). Dla każdej tabeli określono klucz główny, atrybuty oraz relacje z pozostałymi encjami.

Struktura tabel w modelu logicznym
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tabela **klient**
^^^^^^^^^^^^^^^^^

Przechowuje dane osobowe i firmowe klientów sklepu. Obsługuje dwa typy podmiotów – osoby fizyczne oraz firmy, z odpowiednimi ograniczeniami integralności.

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - Nazwa kolumny
     - Typ danych
     - Klucz
     - Opis

   * - id_klienta
     - INTEGER
     - PK
     - Unikalny identyfikator klienta (autoinkrementacja)

   * - typ_klienta
     - TEXT (enum)
     - -
     - Określa typ: 'osoba_fizyczna' lub 'firma'

   * - imie
     - TEXT
     - -
     - Imię klienta (dla firm – NULL)

   * - nazwisko
     - TEXT
     - -
     - Nazwisko klienta (dla firm – NULL)

   * - nazwa_firmy
     - TEXT
     - -
     - Nazwa firmy (dla osób fizycznych – NULL)

   * - email
     - TEXT
     - UNIQUE
     - Adres e-mail (unikalny, wymagany)

   * - telefon
     - TEXT
     - -
     - Numer kontaktowy

   * - pesel
     - TEXT
     - UNIQUE
     - PESEL (tylko dla osób fizycznych, unikalny)

   * - nip_firmy
     - TEXT
     - UNIQUE
     - NIP (tylko dla firm, unikalny)

   * - data_utworzenia
     - DATETIME
     - -
     - Data rejestracji konta (domyślnie bieżąca data)

Ograniczenia:
- Wzajemne wykluczanie PESEL/NIP – klient może mieć wypełniony tylko jeden z tych atrybutów.
- Dla osób fizycznych: `imie`, `nazwisko` i `pesel` wymagane, `nazwa_firmy` i `nip_firmy` – NULL.
- Dla firm: `nazwa_firmy` i `nip_firmy` wymagane, `imie`, `nazwisko` i `pesel` – NULL.

Tabela **adres**
^^^^^^^^^^^^^^^^

Przechowuje adresy przypisane do klientów. Jeden klient może mieć wiele adresów (np. dostawowy, fakturowy, korespondencyjny).

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - Nazwa kolumny
     - Typ danych
     - Klucz
     - Opis

   * - id_adresu
     - INTEGER
     - PK
     - Unikalny identyfikator adresu

   * - ulica
     - TEXT
     - -
     - Nazwa ulicy

   * - numer_domu
     - TEXT
     - -
     - Numer budynku

   * - numer_mieszkania
     - TEXT
     - -
     - Numer mieszkania (opcjonalny)

   * - miasto
     - TEXT
     - -
     - Nazwa miasta

   * - kod_pocztowy
     - TEXT
     - -
     - Kod pocztowy

   * - kraj
     - TEXT
     - -
     - Nazwa kraju (domyślnie 'Polska')

   * - typ_adresu
     - TEXT (enum)
     - -
     - Typ adresu: 'dostawowy', 'fakturowy', 'korespondencyjny'

   * - id_klienta
     - INTEGER
     - FK
     - Identyfikator klienta (klucz obcy do tabeli klient)

Relacje:
- `id_klienta` odnosi się do `klient.id_klienta`.
- Kaskadowe usuwanie (`ON DELETE CASCADE`) – usunięcie klienta usuwa wszystkie jego adresy.

Tabela **produkt**
^^^^^^^^^^^^^^^^^^

Przechowuje dane produktów oferowanych w sklepie, w tym ich stan magazynowy i kategorię.

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - Nazwa kolumny
     - Typ danych
     - Klucz
     - Opis

   * - id_produktu
     - INTEGER
     - PK
     - Unikalny identyfikator produktu

   * - nazwa
     - TEXT
     - -
     - Nazwa produktu (wymagana)

   * - producent
     - TEXT
     - -
     - Nazwa producenta (domyślnie 'Nieznany')

   * - opis
     - TEXT
     - -
     - Dodatkowy opis techniczny (opcjonalny)

   * - cena_jednostkowa
     - NUMERIC
     - -
     - Aktualna cena jednostkowa (>= 0)

   * - stan_magazynowy
     - INTEGER
     - -
     - Liczba dostępnych sztuk (>= 0, domyślnie 0)

   * - typ_produktu
     - TEXT (enum)
     - -
     - Kategoria: 'plyta_glowna', 'pamiec_ram', 'procesor', 'karta_graficzna', 'dysk', 'obudowa', 'zasilacz', 'inne'

   * - data_dodania
     - DATETIME
     - -
     - Data dodania do oferty (domyślnie bieżąca data)

Tabela **zamowienie**
^^^^^^^^^^^^^^^^^^^^^

Przechowuje dane zamówień złożonych przez klientów, w tym status, metodę płatności i całkowitą wartość.

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - Nazwa kolumny
     - Typ danych
     - Klucz
     - Opis

   * - id_zamowienia
     - INTEGER
     - PK
     - Unikalny identyfikator zamówienia

   * - data_zlozenia
     - DATETIME
     - -
     - Data złożenia zamówienia (domyślnie bieżąca data)

   * - data_wysylki
     - DATETIME
     - -
     - Data wysyłki (opcjonalna, wymaga >= data_zlozenia)

   * - status
     - TEXT (enum)
     - -
     - Status: 'przyjete', 'oplacone', 'w_realizacji', 'wyslane', 'dostarczone', 'anulowane'

   * - metoda_platnosci
     - TEXT (enum)
     - -
     - Metoda płatności: 'przelew', 'karta', 'blik', 'za_pobraniem'

   * - wartosc_calkowita
     - NUMERIC
     - -
     - Całkowita wartość zamówienia (>= 0)

   * - id_klienta
     - INTEGER
     - FK
     - Identyfikator klienta składającego zamówienie

   * - adres_dostawy_id
     - INTEGER
     - FK
     - Identyfikator adresu dostawy

Relacje:
- `id_klienta` → `klient.id_klienta` (ograniczenie `RESTRICT` – nie można usunąć klienta z zamówieniami).
- `adres_dostawy_id` → `adres.id_adresu` (ograniczenie `RESTRICT`).
- `data_wysylki` musi być >= `data_zlozenia` (lub NULL).

Tabela **pozycja_zamowienia**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jest to encja asocjacyjna (słaba), która rozwija relację wiele-do-wielu między **Zamówieniem** a **Produktem**. Każdy wiersz odpowiada jednemu produktowi w konkretnym zamówieniu.

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - Nazwa kolumny
     - Typ danych
     - Klucz
     - Opis

   * - id_pozycji
     - INTEGER
     - PK
     - Unikalny identyfikator pozycji

   * - liczba_sztuk
     - INTEGER
     - -
     - Liczba zamówionych sztuk (> 0)

   * - cena_w_momencie_zakupu
     - NUMERIC
     - -
     - Cena jednostkowa z chwili zakupu (historyczna, >= 0)

   * - id_zamowienia
     - INTEGER
     - FK
     - Identyfikator zamówienia

   * - id_produktu
     - INTEGER
     - FK
     - Identyfikator produktu

Relacje:
- `id_zamowienia` → `zamowienie.id_zamowienia` (`ON DELETE CASCADE`).
- `id_produktu` → `produkt.id_produktu` (`ON DELETE RESTRICT`).
- Unikalność pary (`id_zamowienia`, `id_produktu`) – zapobiega duplikowaniu produktu w jednym zamówieniu.

Tabela **faktura**
^^^^^^^^^^^^^^^^^^

Przechowuje dane faktur wystawionych dla zamówień. Relacja 1:1 z zamówieniem – każde zamówienie może mieć maksymalnie jedną fakturę.

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - Nazwa kolumny
     - Typ danych
     - Klucz
     - Opis

   * - id_faktury
     - INTEGER
     - PK
     - Unikalny identyfikator faktury

   * - numer_faktury
     - TEXT
     - UNIQUE
     - Unikalny numer faktury (wymagany)

   * - data_wystawienia
     - DATETIME
     - -
     - Data wystawienia (domyślnie bieżąca data)

   * - kwota_brutto
     - NUMERIC
     - -
     - Kwota brutto faktury (>= 0)

   * - sciezka_pliku
     - TEXT
     - -
     - Ścieżka do pliku PDF faktury (opcjonalna)

   * - id_zamowienia
     - INTEGER
     - FK (UNIQUE)
     - Identyfikator zamówienia (unikalny – 1:1)

Relacje:
- `id_zamowienia` → `zamowienie.id_zamowienia` (`ON DELETE RESTRICT`).
- `UNIQUE` na `id_zamowienia` zapewnia relację 1:1 – do jednego zamówienia można wystawić tylko jedną fakturę.

Diagram modelu logicznego
~~~~~~~~~~~~~~~~~~~~~~~~~

Poniżej zamieszczono diagram modelu logicznego w notacji Barkera, obrazujący strukturę tabel, klucze główne, klucze obce oraz relacje między encjami po procesie normalizacji do 3. postaci normalnej.

.. figure:: /_static/diagram_model_logiczny.png
   :align: center
   :alt: Diagram modelu logicznego ERD w notacji Barkera
   :width: 35%
   :scale: 65%

   Rysunek 3.2: Model logiczny bazy danych NautSA w notacji Barkera.

Model fizyczny
--------------

Model fizyczny uwzględnia specyfikę dwóch docelowych silników: **PostgreSQL** (produkcyjny, zaawansowany) oraz **SQLite** (lekki, do testów lub zastosowań embedded). Różnice dotyczą typów danych, mechanizmów generowania kluczy głównych, obsługi typów wyliczeniowych (ENUM) oraz precyzji finansowej.

Model fizyczny dla PostgreSQL (skrót)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PostgreSQL oferuje bogaty zestaw typów danych dostosowanych do potrzeb aplikacji biznesowych:

- `SERIAL` – automatycznie inkrementowany klucz główny.
- `NUMERIC(10,2)` – precyzyjny typ dla kwot pieniężnych.
- `TIMESTAMPTZ` – data i czas wraz ze strefą czasową.
- Typy wyliczeniowe (`CREATE TYPE ... AS ENUM`) – dla pól o ściśle określonym zbiorze wartości.
- Ograniczenia `CHECK` – zapewniające integralność danych.
- Indeksy – zakładane na kluczach obcych i często używanych kolumnach.


**Przykładowy fragment kodu dla PostgreSQL (tabela klient):**

.. code-block:: sql

   CREATE TABLE IF NOT EXISTS nautsa.klient (
       id_klienta SERIAL PRIMARY KEY,

       typ_klienta nautsa.typ_klienta_enum NOT NULL,

       imie VARCHAR(100),
       nazwisko VARCHAR(100),

       nazwa_firmy VARCHAR(255),

       email VARCHAR(255) NOT NULL UNIQUE,
       telefon VARCHAR(20),

       pesel CHAR(11) UNIQUE,
       nip_firmy VARCHAR(15) UNIQUE,

       data_utworzenia TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
   );


Pełny kod definicji bazy danych `nautsa` dla PostgreSQL znajduje się w repozytorium pod linkiem: `kod PostgreSQL <https://github.com/Youarecheck/Bazy_danych_kody_sql_and_ERD/blob/master/postgreseversion.sql>`_.

Model fizyczny dla SQLite
~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. code-block:: sql

   CREATE TABLE klient (
       id_klienta INTEGER PRIMARY KEY AUTOINCREMENT,
       typ_klienta TEXT NOT NULL
           CHECK (typ_klienta IN ('osoba_fizyczna', 'firma')),
       imie TEXT,
       nazwisko TEXT,
       nazwa_firmy TEXT,
       email TEXT NOT NULL UNIQUE
   );


Pełny kod definicji bazy danych `nautsa` dla SQLite znajduje się w repozytorium pod linkiem: `kod SQLite <https://github.com/Youarecheck/Bazy_danych_kody_sql_and_ERD/blob/master/sqlLiteversion.sql>`_.


.. admonition:: Opracowanie
   :class: note

   **Autor:** Michał Kraus 
   **Przedmiot:** Bazy danych  
   **Data:** czerwiec 2026