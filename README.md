# MatchSpecIT

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Uruchamianie środowiska

#### Środowisko 

    język programowania: python 3.9.9
    baza danych: postgres 12.0

#### Środowisko deweloperskie (instancja aplikacji)

     docker-compose -f docker-compose.dev.yml up
     
#### Testy

    docker-compose -f docker-compose.dev.yml run backend pytest tests/ -s


####  Konsola dockerowa (bash)

    docker-compose -f docker-compose.dev.yml exec backend bash

## Tworzenie diagramu bazy danych

#### Instalacja

    https://django-extensions.readthedocs.io/en/latest/installation_instructions.html
    https://pygraphviz.github.io/documentation/stable/install.html
    

#### Generowanie

    ./manage.py graph_models -a --arrow-shape normal -o diagram.png

    lub inne w linku https://django-extensions.readthedocs.io/en/latest/graph_models.html