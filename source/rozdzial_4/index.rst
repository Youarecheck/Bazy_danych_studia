Rozdział 4: Definiowanie struktury bazy danych i wsadowe wprowadzanie danych
================================================

W rozdziale przedstawiono proces definiowania struktury bazy danych oraz
metody wsadowego importu danych w środowiskach SQLite i PostgreSQL.
Omówiono wykorzystane narzędzia, składnię języka SQL oraz rozwiązania
umożliwiające efektywne i bezpieczne zasilanie bazy danymi testowymi.
Definiowanie struktury bazy danych w SQLite

Definiowanie struktury bazy danych w SQLite
-------------------------------------------

Poniżej przedstawiono wybrane fragmenty kodu definiującego strukturę bazy
danych w systemie SQLite wraz z krótkim omówieniem zastosowanych
mechanizmów integralności danych.


**Przykład 4.1 – Tworzenie tabeli z kluczem głównym i ograniczeniami (SQLite):**

.. code-block:: sql

    -- Tabela KLIENT – przechowuje dane osobowe i firmowe
    CREATE TABLE klient (
        id_klienta INTEGER PRIMARY KEY AUTOINCREMENT,  -- automatycznie inkrementowany identyfikator
        typ_klienta TEXT NOT NULL
            CHECK (typ_klienta IN ('osoba_fizyczna', 'firma')),  -- ograniczenie zbioru wartości
        imie TEXT,
        nazwisko TEXT,
        nazwa_firmy TEXT,
        email TEXT NOT NULL UNIQUE,  -- unikalność adresu e-mail
        telefon TEXT,
        pesel TEXT UNIQUE,  -- unikalny PESEL (tylko dla osób fizycznych)
        nip_firmy TEXT UNIQUE,  -- unikalny NIP (tylko dla firm)
        data_utworzenia DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CHECK (   -- złożone ograniczenie integralności
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

**Przykład 4.2 – Tworzenie tabeli z kluczem obcym (SQLite):**

.. code-block:: sql

    -- Tabela ADRES – powiązana z klientem relacją 1:N
    CREATE TABLE adres (
        id_adresu INTEGER PRIMARY KEY AUTOINCREMENT,
        ulica TEXT NOT NULL,
        numer_domu TEXT NOT NULL,
        numer_mieszkania TEXT,
        miasto TEXT NOT NULL,
        kod_pocztowy TEXT NOT NULL,
        kraj TEXT NOT NULL DEFAULT 'Polska',
        typ_adresu TEXT NOT NULL
            CHECK (typ_adresu IN ('dostawowy', 'fakturowy', 'korespondencyjny')),
        id_klienta INTEGER NOT NULL,
        FOREIGN KEY (id_klienta) REFERENCES klient(id_klienta)
            ON DELETE CASCADE  -- usunięcie klienta usuwa jego adresy
    );

**Przykład 4.3 – Tworzenie indeksu dla wydajności (SQLite):**

.. code-block:: sql

    -- Indeks na kluczu obcym przyspiesza JOIN-y
    CREATE INDEX idx_adres_klient ON adres(id_klienta);

    -- Indeks na kolumnie często używanej w warunku WHERE
    CREATE INDEX idx_zamowienie_status ON zamowienie(status);

Definiowanie struktury bazy danych w PostgreSQL
-----------------------------------------------

System PostgreSQL oferuje szerszy zestaw typów danych oraz natywne
wsparcie dla typów wyliczeniowych (ENUM), co pozwala na bardziej
precyzyjne modelowanie danych i ograniczeń biznesowych.

**Przykład 4.4 – Definicja typu wyliczeniowego (ENUM) i tabeli (PostgreSQL):**

.. code-block:: sql

    -- Typ wyliczeniowy dla statusu zamówienia
    CREATE TYPE status_zamowienia_enum AS ENUM (
        'przyjete', 'oplacone', 'w_realizacji', 'wyslane', 'dostarczone', 'anulowane'
    );

    -- Tabela ZAMOWIENIE z wykorzystaniem ENUM
    CREATE TABLE zamowienie (
        id_zamowienia SERIAL PRIMARY KEY,  -- autoinkrementacja
        data_zlozenia TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- data ze strefą
        data_wysylki TIMESTAMPTZ,
        status status_zamowienia_enum NOT NULL,  -- wykorzystanie ENUM
        metoda_platnosci metoda_platnosci_enum NOT NULL,
        wartosc_calkowita NUMERIC(10,2) NOT NULL CHECK (wartosc_calkowita >= 0),
        id_klienta INTEGER NOT NULL,
        adres_dostawy_id INTEGER NOT NULL,
        FOREIGN KEY (id_klienta) REFERENCES klient(id_klienta)
            ON DELETE RESTRICT,  -- nie pozwala usunąć klienta z zamówieniami
        FOREIGN KEY (adres_dostawy_id) REFERENCES adres(id_adresu)
            ON DELETE RESTRICT,
        CHECK (data_wysylki IS NULL OR data_wysylki >= data_zlozenia)
    );

Wsadowy import danych z plików CSV 
---------------------------------------------------

Do wsadowego importu danych testowych przygotowano dwa skrypty w języku Python – osobno dla SQLite i PostgreSQL. Ich zadaniem jest automatyczne załadowanie całego zestawu danych z plików CSV do odpowiednich tabel bazy danych.

Skrypt dla SQLite – `import_sqlite.py <https://github.com/Youarecheck/Bazy_danych_kody_sql_and_ERD/blob/master/import_sqlite.py>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Skrypt importuje dane do lokalnej bazy SQLite (domyślnie plik ``nautsa.db``). Wykorzystuje mechanizm ``INSERT`` z wielowierszowym wykonywaniem za pomocą ``executemany()``.

**Zasada działania:**

- Nazwa pliku CSV (np. ``klient.csv``) określa nazwę tabeli docelowej.
- Pierwszy wiersz pliku zawiera nagłówki – nazwy kolumn.
- Import wykonywany jest w ściśle określonej kolejności (``IMPORT_ORDER``), aby zachować integralność kluczy obcych.
- Skrypt sprawdza, czy dana tabela istnieje w bazie – jeśli nie, pomija import.
- W przypadku błędów (np. naruszenie unikalności lub klucza obcego) transakcja jest wycofywana.

**Uruchomienie:**

.. code-block:: bash

    python import_sqlite.py
    Podaj katalog z plikami CSV (ENTER = bieżący katalog): dane/

**Wymagania:** brak zależności zewnętrznych – korzysta z wbudowanego modułu ``sqlite3``.

Skrypt dla PostgreSQL – `import_postgresql.py <https://github.com/Youarecheck/Bazy_danych_kody_sql_and_ERD/blob/master/import_postgresql.py>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Skrypt wykorzystuje polecenie ``COPY``, które jest rekomendowanym przez
PostgreSQL sposobem szybkiego ładowania dużych zbiorów danych z plików
tekstowych i CSV. Dane logowania pobierane są z pliku JSON.

**Zasada działania:**

- Dane logowania wczytywane są z pliku ``database_creds.json`` (host, port, baza, użytkownik, hasło).
- Przed importem skrypt może utworzyć schemat bazy na podstawie pliku ``postgreseversion.sql`` (jeśli istnieje).
- Podobnie jak w przypadku SQLite, nazwa pliku CSV określa tabelę, a pierwszy wiersz to nagłówki kolumn.
- Import wykonywany jest w kolejności zgodnej z zależnościami kluczy obcych (``IMPORT_ORDER``).
- Skrypt sprawdza istnienie tabeli w schemacie ``nautsa`` przed rozpoczęciem importu.

**Uruchomienie:**

.. code-block:: bash

    python import_postgresql.py
    Podaj katalog z CSV (ENTER = bieżący katalog): dane/

**Wymagania:** zewnętrzna biblioteka ``psycopg2-binary``.

.. code-block:: bash

    pip install psycopg2-binary

**Przykładowy plik ``database_creds.json``:**

.. code-block:: json

    {
        "host": "localhost",
        "port": 5432,
        "database": "nautsa",
        "user": "postgres",
        "password": "twoje_haslo"
    }

Wspólne cechy skryptów
^^^^^^^^^^^^^^^^^^^^^^

Oba skrypty działają według tego samego wzorca:

#. **Wykrywanie plików** – skanują wskazany katalog w poszukiwaniu plików ``.csv``.
#. **Dopasowanie tabel** – nazwa pliku (bez rozszerzenia) wskazuje tabelę docelową.
#. **Kolejność importu** – gwarantuje, że dane są wstawiane w odpowiedniej kolejności (np. najpierw ``klient``, potem ``adres``, na końcu ``faktura``), co zapobiega błędom związanym z kluczami obcymi.
#. **Obsługa błędów** – w przypadku problemów (np. naruszenie klucza obcego, brak tabeli) skrypt kontynuuje działanie, informując o błędzie, ale nie przerywa całego procesu.
#. **Czytelne komunikaty** – każdy krok jest opisany w konsoli, co ułatwia diagnostykę.

Różnice między implementacjami
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Porównanie skryptów
   :header-rows: 1
   :widths: 20 30 30 20

   * - Cecha
     - SQLite
     - PostgreSQL
     - Uwagi

   * - Mechanizm importu
     - ``INSERT ... executemany()``
     - ``COPY ... FROM STDIN``
     - COPY jest szybszy dla dużych zbiorów

   * - Logowanie
     - Plik ``.db`` (lokalny)
     - Połączenie sieciowe (host/port)
     - PostgreSQL wymaga danych logowania

   * - Schemat
     - Tworzony przed importem (opcjonalnie)
     - Tworzony przed importem (opcjonalnie)
     - Na podstawie plików SQL

   * - Obsługa schematu
     - Brak (baza bez schematów)
     - Tabela w schemacie ``nautsa``
     - PostgreSQL wspiera schematy

Podsumowanie
------------

Dzięki automatycznemu wykrywaniu plików CSV, kontroli istnienia tabel
oraz zachowaniu odpowiedniej kolejności importu proces ładowania danych
został w znacznym stopniu zautomatyzowany. Zastosowane rozwiązania
ograniczają ryzyko wystąpienia błędów związanych z integralnością
referencyjną oraz ułatwiają przygotowanie środowiska testowego.
Wyboru odpowiedniego skryptu należy dokonać na podstawie docelowego środowiska:

- **SQLite** – w przypadku testów lokalnych, prototypowania lub gdy baza działa w środowisku embedded.
- **PostgreSQL** – w środowisku produkcyjnym lub gdy wymagana jest wysoka wydajność przy dużych zbiorach danych.

Wszystkie zasoby: `github <https://github.com/Youarecheck/Bazy_danych_kody_sql_and_ERD.git>`_

.. admonition:: Opracowanie
   :class: note

   **Autor:** Michał Kraus 
   **Przedmiot:** Bazy danych  
   **Data:** czerwiec 2026