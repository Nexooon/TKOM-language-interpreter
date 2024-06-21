### Hubert Brzóskniewicz

Bingo - a programming language with special type for currencies and a dictionary to store them.

<br>

# <p style="text-align: center;">TKOM Dokumentacja projektu</p>


## <p style="text-align: center;"> Temat: Bingo - język walutowy</p>


# 1. Opis zakładanej funcjonalności

W Bingo oprócz podstawowych typów danych i operacji mamy również typ walutowy. Możemy przechowywać w nim ilość oraz rodzaj waluty (np. 20 PLN). Istnieje zarówno możliwość transferu środków pomiędzy zmiennymi typu walutowego jak i zmiana wartości konkretnej zmiennej. Do powyższych operacji możemy użyć dowolnych kombinacji walut, wartości będą przeliczane do jednej waluty tak, aby wszystko było spójne (dokładne sposoby przeliczania podane są w przykładach kodu związanych z walutami).

Nasze waluty można przechowywać w portfelu (słownik) na różnych kontach. Dostęp do takich kont jest możliwy poprzez wskazanie nazwy konta lub typu waluty, która nas interesuje. W przypadku podania typu, zwracany jest słownik zawierający tylko interesujące nas konta.

Przeliczniki walut niezbędne do przeprowadzania operacji na typach walutowych znajdują się w specjalnym pliku konfiguracyjnym, który pobiera interpreter. Rodzaje dostępnych walut również są pobierane z tego pliku i przekazywane do leksera. Przykładowa struktura pliku znajduje się w domyślnym pliku kofiguracyjnym ('eurofxref.csv'). Pierwsza waluta z kursem 1.0 jest walutą główną. Kursy pozostałych walut to przelicznik z waluty głównej na daną walutę.

W programie musi znajdować się funkcja main typu void. To ona będzie wykonywana w czasie działania programu.

# 2. Dostępne konstrukcje językowe

### Typy zmiennych:

+ int
+ float
+ str
+ cur (typ walutowy)
+ curtype (rodzaj waluty)
+ dict (słownik)
+ bool (true/false)

### Operatory

+ \+
+ \-
+ \*
+ /
+ ( )
+ <, <=, >, >=, ==, !=
+ &&, ||
+ !, - (negacja)
+ +=, -=, =
+ -> (transfer pomiędzy typami cur)

| Operator    | Dopuszczalne pary typów | Typ wynikowy |
| ------------| ----------------------- | ------------ |
| + | int-int, float-float, str-str, cur-cur | int, float, str, cur |
| - | int-int, float-float, cur-cur | int, float, cur |
| * | int-int, float-float, str-int, int-str, cur-int, int-cur, cur-float, float-cur | int, float, str, str, cur, cur, cur, cur |
| / | float-float, cur-int, cur-float | float, cur, cur |
| >, >=, <, <= | int-int, float-float, int-float, float-int | bool |
| ==, != | int-int, float-float, int-float, float-int, curtype-curtype, string-string, bool-bool | bool |
| && | bool-bool | bool |
| \|\| | bool-bool | bool |
| ! | bool | bool |
| - (negacja) | int, float | int, float |
| += | int-int, float-float, str-str |
| -= | int-int, float-float |
| -> | cur-cur-cur |


| Operator  | Priorytet | Asocjacyjność |
| --------- | --------- | ------------- |
| - (negacja) | 7 | Brak |
| * | 6 | Lewostronna |
| / | 6 | Lewostronna |
| + | 5 | Lewostronna |
| - (odejmowanie) | 5 | Lewostronna |
| > | 4 | Brak |
| >= | 4 | Brak |
| < | 4 | Brak |
| <= | 4 | Brak |
| == | 4 | Brak |
| != | 4 | Brak |
| ! | 3 | Brak |
| && | 2 | Lewostronna |
| \|\| | 1 | Lewostronna |


### Komentarze:

`# to jest komentarz jednolinijkowy`

### Tworzenie zmiennych:

```
int a = 2;
float b = 2.12;
str napis = "abc";
cur pieniadze = 40 PLN;
curtype rodzaj = EUR;
dict słownik = {};
bool passed = true;
```
- typowanie statyczne, silne
- zmienne tworzone wewnątrz funkcji są widoczne tylko w jej obrębie, tak samo w blokach instrukcyjnych (zasięg ograniczony przez `{}`) - możliwe jest przysłanianie zmiennych
- deklaracja zmiennych możliwa jedynie wewnątrz bloku `{}`

### Instrukcja warunkowa:

```
if warunek {
    # do sth
}
elif warunek {
    # do sth
}
else {
    # do sth else
}
```

### Pętla:

```
while warunek {
    # do sth
}

# iterowanie po słowniku
dict wallet = {};
for account in wallet {
    # do sth
}
```

### Funkcje:

```
typ nazwa(argumenty) {
    # do sth
    return val;
}
```
- przekazywanie argumentów do funkcji przez referencję
- przeciążanie funkcji nie jest dozwolone
- możliwość wywoływania rekursywnego

### Funkcje wbudowane

- print();
- input();

+ konwersja typów
    + to_int(float/str)
    + to_float(int/str)
    + to_str(int/float/cur/curtype)


# 3. Notacja EBNF

Dla przejrzystości pominięto znaki spacji.

Poziom składni

``` ebnf
program             = { function_definition };

function_definition = function_type , identifier , "(" , parameters , ")" , block;
parameters          = [ parameter , { "," , parameter } ];
parameter           = type , identifier;
block               = "{" , { statement } , "}";

statement           = declaration
                    | assignment_or_function_call
                    | conditional
                    | loop
                    | return_statement
                    | currency_transfer;

declaration         = type , identifier , [ "=" , expression ] , ";";
assignment_or_function_call = object_access , [ ( "=" | "+=" | "-=" ) , expression ] , ";";

conditional         = "if" , expression , block ,
                    { "elif" , expression , block } ,
                    [ "else" , block ];

loop                = "while" , expression , block
                    | "for" , identifier , "in" , identifier , block;

return_statement    = "return" , [ expression ] , ";";

currency_transfer   = "from" , expression , "->" , expression , [ "->" , expression ] , ";";

expression          = conjunction , { "||" , conjunction };
conjunction         = negation , { "&&" , negation };
negation            = [ "!" ] , relation_term;
relation_term       = additive_term , [ relation_operator , additive_term ];
relation_operator   = "<" | "<=" | ">" | ">=" | "==" | "!=";
additive_term       = multiplicative_term , { ( "+" | "-" ) , multiplicative_term };
multiplicative_term = unary_application , { ( "*" | "/" ) , unary_application };
unary_application   = [ "-" ] , term;
term                = literal | object_access | "(" , expression , ")";
object_access       = identifier_or_call , { "." , identifier_or_call };
identifier_or_call  = identifier , [ "(" , arguments , ")" ];
arguments           = [ expression , { "," , expression } ];
```

Poziom leksyki
``` ebnf
type            = "int" | "float" | "str" | "cur" | "curtype" | "bool" | "dict";
function_type   = type | "void";

literal         = number , [currency_type] | string | boolean | currency_type | dict;
number          = integer , [ "." , digit , { digit } ];
integer         = "0" | digit_positive , { digit };
string          = '"' , { unicode_symbol } , '"';
(* unicode_symbol ommited *)
boolean         = "true" | "false";
currency_type   = { letter }; (* specified in special file *)
dict            = "{" , [ pair , { "," , pair } ] , "}";
pair            = string , ":" , number, currency_type;

identifier      = letter , { letter | digit | "_" };
digit_positive  = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
digit           = digit_positive | "0";
(* letter ommited *)
```

# 4. Przykłady kodu

#### tworzenie zmiennych
```
void main() {
    int a = 220;
    a = 110;

    float b = 2.2;
    b = 3.132;

    str c = "abc";
    c = "def";

    cur d = 100 PLN;
    d = 10.23 USD;

    # typ cur może przyjąć więcej niż 2 cyfry po przecinku, jednak w ramach wyświetlania jego wartości zawsze pokazane zostanie zaokrąglenie do 2 miejsc po przecinku.
    # Dzięki temu nie tracimy dokładności obliczeń na walutach
    d = 12.454 JPY;
    print(d); # 12.45 JPY
}
```

#### operacje na zmiennych
```
void main() {
    int a = 2;
    int b = 4;
    int suma = a + b;
    int roznica = a - b;
    int iloczyn = a * b;
    a += 5;
    a -= 3;

    float a_2 = 2.5;
    float b_2 = 4.3;
    float suma_2 = a_2 + b_2;
    float roznica_2 = a_2 - b_2;
    float iloczyn_2 = a_2 * b_2;
    float iloraz_2 = a_2 / b_2;
    a_2 += 5.51;
    a_2 -= 3.12;

    str c = "tekst tekst";
    str d = " wiecej tekstu";
    str konkatenacja = c + d;
}
```

#### priorytety operacji
```
void main() {
    int wynik = 2 + 2 * 2; # 6
    print(wynik);
    wynik = (2 + 2) * 2; # 8
    print(wynik);

    float wynik_float = 4.0 + 4.0 / 2.0; # 6.0
    print(wynik_float);
    wynik_float = (4.0 + 4.0) / 2.0; # 4.0
    print(wynik_float);

    wynik_float = 10.0 - 2.0 * 4.0 + 8.0 / 4.0; # 4.0
    print(wynik_float);
    wynik = 3 - 2 - 1; # 0
    print(wynik);
}
```

#### instrukcja warunkowa
```
void main() {
    if (10 <= 2 || 20.2 > 10) {
        print("dobrze");
    }
    else {
        print("źle");
    }

    if (10 > 2 && 102.22 < 234.121) {
        print("dobrze");
    }
    elif return_true() {
        print("dobrze");
    }
    else {
        print("źle");
    }
}

bool return_true() {
    return true;
}
```

#### Pętla
```
void main() {
    int a = 0;
    int i = 0;

    while i<5 {
        a += 2;
        i += 1;
        print(i);
    }

    print(a); # 10
}
```

#### Wejście/wyjście
```
void main() {
    str wejscie = input("wprowadz liczbe: ");
    print("wprowadzono: " + wejscie);
}
```

#### Konwersja typów
W nawiasach podano dopuszczalne typy argumentów
+ to_int(float/str)
+ to_float(int/str)
+ to_str(int/float/cur/curtype)
```
void main() {
    int number_int = 24;
    float number_float = 9.87;
    str string_int = "215";
    str string_float = "1.22";
    cur currency = 10 EUR;
    curtype currency_type = USD;


    int a = to_int(number_float); # a==9
    int b = to_int(string_int); # b==215

    float c = to_float(number_int); # c==24.0
    float d = to_float(string_float); # d==1.22

    str napis = to_str(number_int); # napis=="24"
    str napis_float = to_str(number_float); # napis_float=="9.87"
    str napis_cur = to_str(currency); # napis_cur=="10 EUR"
    str napis_curtype = to_str(currency_type); # napis_curtype=="USD"
}
```

#### Inne konstrukcje oraz przykładowe błędy
```
void main() {
    float a = 50.0;
    float b = 100.0;

    float wynik = iloraz(a, b);
    print(wynik); # wynik==0.5

    wynik = iloraz(20.0, 10.0);
    print(wynik); # wynik==2

    int wynik2 = iloraz(a, b);
    ### SemanticError : Ln 11 Col 5 : Type mismatch.
}

float iloraz(float x, float y) {
    return x/y;
}
```

+ przekazywanie argumentów do funkcji przez referencje
```
void przekazywanie_przez_referencje(float a, str b, cur c, dict d) {
    a += 7.21;
    b = "zmiana";
    c = c + 10 USD;
    d.add("konto", 10 PLN);
}

void main() {
    float x = 12.91;
    str y = "tekst";
    cur z = 30 USD;
    dict zz = {};

    print(x);
    print(y); # x=12.91; y="tekst"
    print(z);
    print(zz); # z=30.00 USD, zz={}

    przekazywanie_przez_referencje(x, y, z, zz);

    print(x);
    print(y); # x=20.12; y="zmiana"
    print(z);
    print(zz); # z=40.00 USD, zz={"konto": 10 PLN}
}
```

+ utworzenie zmiennej w bloku if
```
void main() {
    int a = 7;
    int b = 10;
    if (a < 10) {
        a = 5;
        int b = 20;
        int c = 10;
    }
    print(a); # 5
    print(b); # 10
    print(c);
    ### SemanticError : Ln 11 Col 11 : 'c' was not declared in this scope
}
```

+ rekursja
```
int factorial(int n) {
    if (n==0 || n==1) {
        return 1;
    }
    else {
        return n * factorial(n-1);
    }
}

void main() {
    str num = input("Wprowadź liczbę: ");

    int fact = factorial(to_int(num));
    print("Silnia liczby " + num + " wynosi: " + to_str(fact));
}
```


```
void wypisz() {
    print("hej, tutaj funkcja");
    return;
}

int dodaj_wieksze(int a, int b, int c) {
    if (a > b) {
        return a + c;
    }
    else {
        return b + c;
    }
}

void main(){
    int zmienna = 10;
    int zmienna2 = 20;

    int i = 0;
    while i < 3 {
        wypisz();
        int wynik = dodaj_wieksze(zmienna, zmienna2, i);
        print(wynik);
        i += 1;
    }
}
```

#### stworzenie zmiennej wewnątrz funkcji
```
void funkcja() {
    float a = 2.2;
}

void main() {
    funkcja();
    print(a);
    ### SemanticError : Ln 7 Col 11 : 'a' was not declared in this scope
}
```

#### przeciążenie funkcji
```
void funkcja(int a) {
    a += 2;
}

void funkcja(int a, str b) {
    a += 2;
    print(b);
}
### ParserError: Ln 5 Col 1 : Redefinition of a function from line 1
```


### Przykłady działań z typem walutowym
```
void main() {
    cur a = 100 PLN;
    cur b = 10.5 EUR;
    cur c = 82.12 JPY;

    # typ cur posiada pola type (rodzaj waluty - curtype) oraz value (ilość pieniędzy - float)
    curtype d = a.type; # d==PLN
    float e = a.value; # e==100.0

    # można zmienić wartość value
    c.set_value(90.77); # c==90.77 JPY


    cur sum = a + b; # waluta wynikowa zawsze taka sama jak pierwszy element operacji
    cur minus = a - b;


    a = a + 50 USD; # a dalej w PLN
    b = b - 1 EUR; # b dalej w EUR
    print("po operacjach:");
    print(a);
    print(b);

    # porównywanie walut
    # a > b
    # gdy typy porównywanych walut nie są jednakowe, na potrzeby porównania waluty sprowadzane są do waluty głównej, zdefiniowanej w pliku konfiguracyjnym z kursami


    # transfer środków
    # pomiędzy zmiennymi przelewana jest równowartość wyrażenia znajdującego się pomiędzy znakami "->"
    # zmienna po lewej jest pomniejszana o tą wartość, a zmienna po prawej jest o nią powiększana
    from a -> 10 PLN -> b;
    from a -> 5 EUR -> b;
    from a -> 0.1*a + 2.24 JPY -> b;

    cur x = 100 PLN;
    cur y = 200 PLN;
    from x -> 10 PLN -> y;
    print(x);
    print(y);

    # można też pominąć zmienną po jednej stronie:
    from a -> 10 PLN; # pomniejszenie a o 10 PLN
    from 10 PLN -> b; # zwiększenie b o 10 PLN

    cur z = 30 PLN;
    from z -> 10 PLN;
    print(z);
    from 20 PLN -> z;
    print(z);


    if (a > b) {
        print(a);
    }
}
```

#### słownik (portfel)
- w słowniku klucze mogą być jedynie typu str (nazwa konta), a wartości jedynie typu cur
```
void main() {
    dict wallet = {};
    dict wallet2 = {
        "oszczędności": 2000 PLN,
        "inwestycje USD": 100 USD
    };

    cur a = wallet2.get("oszczędności");
    print(a);

    dict dolary = wallet2.get(USD); # zwraca słownik zawierający wszystkie konta w dolarach (filtrowanie)
    print("filtered:");
    for account in dolary {
        print(account.name);
        print(account.value);
    }

    wallet2.add("konto EUR", 20.12 EUR);

    #wallet.add(12, 23);
    ### TypeError : line 13 : Dictionary accepts only str and cur

    print("wallet2:");
    for account in wallet2 {
        print(account.name);
        print(account.value);           # cały typ cur
        print(account.value.value);     # float
        print(account.value.type);      # curtype
        print("----");
    }

    # do słownika można też dodać referencję do waluty
    cur waluta_do_konta = 40 EUR;
    wallet.add("konto", waluta_do_konta);

    for account in wallet {
        if (account.value.type == "EUR") {
            account.value.set_value(10);
        }
    }
    print(wallet);
    print(waluta_do_konta);
}
```

# 5. Sposób realizacji
Projekt składa się z 3 głównych modułów - lekser, parser oraz interpreter. Lekser posiada publiczną metodę get_next_token(). Inicjalizując parser podajemy mu instancję leksera. Parser posiada publiczną metodę parse(), która zwraca drzewo obiektów dokumentu. Drzewo to jest następnie odwiedzane przez interpreter (wzorzec wizytatora). Interpreter dodatkowo odpowiednio zarządza kontekstami i obliczeniami (wykorzystuje do tego osobne moduły). Do specjalnych typów obiektów (cur, curtype, dict) utworzono specjalne klasy w module Currency.

Rodzaje rozróżnianych tokenów:
- PLUS              (+)
- MINUS             (-)
- MUL               (*)
- DIV               (/)
- LESS              (<)
- LESS_EQUAL        (<=)
- GREATER           (>)
- GREATER_EQUAL     (>=)
- EQUAL             (==)
- NOT_EQUAL         (!=)
- AND               (&&)
- OR                (||)
- NOT               (!)
- ASSIGN            (=)
- ADD_AND_ASSIGN    (+=)
- SUB_AND_ASSIGN    (-=)
- CUR_TRANSFER      (->)

- INT
- FLOAT
- STR
- CUR
- CURTYPE
- DICT
- BOOL
- VOID

- BOOL_VALUE_TRUE   (true)
- BOOL_VALUE_FALSE  (false)

- STR_CONST
- IDENTIFIER
- INT_CONST
- FLOAT_CONST
- CURTYPE_CONST

- LEFT_BRACKET      (()
- RIGHT_BRACKET     ())
- DOT               (.)
- COMMA             (,)
- LEFT_CURLY_BRACKET({)
- RIGHT_CURLY_BRACKET(})
- SEMICOLON         (;)
- COLON             (:)

- IF
- ELIF
- ELSE
- WHILE
- FOR
- IN
- RETURN
- FROM

- END_OF_FILE       (EOF)
- COMMENT


# 6. Sposób testowania
Projekt był testowany za pomocą testów jednostkowych, testów integracyjnych oraz testów akceptacyjnych.<br>
Testy jednostkowe przeprowadzono dla leksera oraz interpretera. Testy integracyjne dla leksera oraz interpretera.<br>
Na końcu przeprowadzono testy akceptacyjne, sprawdzając projekt jako całość - podając przykładowe pliki do wykonania.<br>

# 7. Opis użytkowy
Aby skorzystać z interpretera, należy uruchomić plik main.py. Przyjmuje on 2 argumenty, przy czym drugi jest opcjonalny:

1. ścieżka do pliku do interpretacji
2. ścieżka do pliku konfiguracyjnego (z kursami walut) - argument opcjonalny, domyślnie przyjmuje plik `eurofxref.csv`

`python3 main.py path_to_file [path_to_exchange_rate_file]`

W razie wystąpienia błędu podczas analizy pliku wejściowego, zostaniemy poinformowani stosownym komunikatem.
