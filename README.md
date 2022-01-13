# MatchSpecIT

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Uruchamianie środowiska

#### Środowisko deweloperskie (instancja aplikacji)

     docker-compose -f docker-compose.dev.yml up
     
#### Testy

    docker-compose -f docker-compose.dev.yml run backend pytest tests/ -s
