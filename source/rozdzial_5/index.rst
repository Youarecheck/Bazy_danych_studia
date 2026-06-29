Rozdział 5: Definiowanie zapytań do bazy danych
===============================================

W niniejszym rozdziale przedstawiono implementację przykładowych
zapytań do bazy danych sklepu internetowego NautSA. Zapytania zostały
zaimplementowane w postaci funkcji języka Python, które komunikują się
z bazami danych SQLite oraz PostgreSQL i zwracają wyniki w postaci
struktur danych języka Python.

Celem przygotowania modułu było zaprezentowanie praktycznego
wykorzystania języka SQL do realizacji typowych operacji analitycznych
i raportowych wykonywanych na danych sklepu internetowego. Funkcje
obejmują zarówno proste operacje selekcji danych, jak również bardziej
zaawansowane mechanizmy, takie jak agregacja, złączenia tabel,
podzapytania oraz operatory zbiorowe.

Moduł z funkcjami
-----------------

Wszystkie funkcje zostały zapisane w osobnym module języka Python:

`db_queries.py <https://github.com/Youarecheck/Bazy_danych_kody_sql_and_ERD/blob/master/db_queries.py>`_

Moduł zawiera zestaw funkcji przeznaczonych do wykonywania zapytań
zarówno dla bazy SQLite, jak i PostgreSQL. Każda funkcja posiada
komentarz w postaci docstringa opisujący jej przeznaczenie, parametry,
wartości zwracane oraz sposób działania.

Dzięki zastosowaniu docstringów możliwe jest automatyczne generowanie
dokumentacji przy użyciu systemu Sphinx bez konieczności powielania
opisów w kodzie oraz dokumentacji projektowej.

Charakterystyka przygotowanych zapytań
--------------------------------------

W przygotowanym module wykorzystano zagadnienia omawiane podczas zajęć
laboratoryjnych:

* selekcję danych (``SELECT``),
* funkcje agregujące (``COUNT()``, ``SUM()``, ``AVG()``, ``MIN()``, ``MAX()``),
* złączenia tabel (``JOIN``),
* podzapytania,
* operatory zbiorowe (``UNION``),
* grupowanie danych (``GROUP BY``),
* sortowanie wyników (``ORDER BY``).

Funkcje dla SQLite
------------------

W pierwszej części modułu zaimplementowano funkcje współpracujące
z bazą danych SQLite.

Funkcja ``sqlite_top_products()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Zwraca listę najczęściej kupowanych produktów wraz z łączną liczbą
sprzedanych sztuk.

W zapytaniu wykorzystano:

* funkcję agregującą ``SUM()``,
* grupowanie danych ``GROUP BY``,
* złączenie tabel ``JOIN``,
* sortowanie malejące ``ORDER BY DESC``.

Przykładowe wywołanie:

.. code-block:: python

    sqlite_top_products()

Funkcja ``sqlite_customer_orders()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Wyświetla historię zamówień klienta wskazanego za pomocą adresu e-mail.

W zapytaniu wykorzystano:

* selekcję danych ``WHERE``,
* złączenie tabel ``JOIN``,
* sortowanie wyników według daty zamówienia.

Przykładowe wywołanie:

.. code-block:: python

    sqlite_customer_orders("jan.kowalski@example.com")

Funkcja ``sqlite_average_order_value()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Oblicza średnią wartość wszystkich zamówień zapisanych w bazie danych.

W zapytaniu wykorzystano funkcję agregującą:

* ``AVG()``.

Przykładowe wywołanie:

.. code-block:: python

    sqlite_average_order_value()

Funkcja ``sqlite_clients_without_orders()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Wyszukuje klientów, którzy nie złożyli żadnego zamówienia.

W zapytaniu wykorzystano:

* podzapytanie,
* operator ``NOT IN``.

Przykładowe wywołanie:

.. code-block:: python

    sqlite_clients_without_orders()

Funkcja ``sqlite_order_summary()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tworzy zestawienie liczby zamówień dla poszczególnych statusów.

W zapytaniu wykorzystano:

* ``COUNT(*)``,
* ``GROUP BY``.

Przykładowe wywołanie:

.. code-block:: python

    sqlite_order_summary()

Funkcje dla PostgreSQL
----------------------

Druga część modułu została przygotowana dla systemu PostgreSQL.

Funkcja ``pg_top_customers()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Zwraca klientów generujących największą wartość sprzedaży.

W zapytaniu wykorzystano:

* ``JOIN``,
* ``SUM()``,
* ``GROUP BY``,
* ``ORDER BY``.

Przykładowe wywołanie:

.. code-block:: python

    pg_top_customers(credentials)

Funkcja ``pg_invoice_report()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generuje raport faktur poprzez połączenie danych z tabel:

* ``klient``,
* ``zamowienie``,
* ``faktura``.

Zapytanie wykorzystuje wielokrotne złączenia tabel.

Przykładowe wywołanie:

.. code-block:: python

    pg_invoice_report(credentials)

Funkcja ``pg_products_never_sold()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Wyszukuje produkty, które nigdy nie zostały sprzedane.

W zapytaniu wykorzystano:

* podzapytanie,
* operator ``NOT IN``.

Przykładowe wywołanie:

.. code-block:: python

    pg_products_never_sold(credentials)

Funkcja ``pg_order_statistics()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tworzy zestaw podstawowych statystyk dotyczących zamówień.

W zapytaniu wykorzystano funkcje agregujące:

* ``COUNT()``,
* ``MIN()``,
* ``MAX()``,
* ``AVG()``.

Przykładowe wywołanie:

.. code-block:: python

    pg_order_statistics(credentials)

Funkcja ``pg_union_contacts()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prezentuje wykorzystanie operatora zbiorowego ``UNION``.

Wynikiem działania funkcji jest połączona lista kontaktów pochodzących
z różnych źródeł danych.

Przykładowe wywołanie:

.. code-block:: python

    pg_union_contacts(credentials)



Podsumowanie
------------

Przygotowany moduł stanowi warstwę dostępu do danych dla opracowanej
bazy danych sklepu internetowego NautSA. Zaimplementowane funkcje
prezentują wykorzystanie najważniejszych mechanizmów języka SQL,
takich jak selekcja danych, funkcje agregujące, złączenia tabel,
podzapytania oraz operatory zbiorowe.



Wszystkie zasoby: `github <https://github.com/Youarecheck/Bazy_danych_kody_sql_and_ERD.git>`_

.. admonition:: Opracowanie
   :class: note

   **Autor:** Michał Kraus
   **Przedmiot:** Bazy danych
   **Data:** czerwiec 2026