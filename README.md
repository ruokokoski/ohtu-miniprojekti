# Ohjelmistotuotanto - Miniprojekti



## Projektin käyttöönotto

### Asentaminen

1. **Kloonaa repositorio**:
   ```bash
   git clone https://github.com/ruokokoski/ohtu-miniprojekti.git
   cd ohtu-miniprojekti
   ```
2. **Asenna riippuvuudet**:
   ```bash
   poetry install
   ```
3. **Luo .env-tiedosto**:
   ```bash
   DATABASE_URL=postgresql://<your_database_service>
   TEST_ENV=true
   SECRET=<your_own_secret>
   ```

### Yhteyden ottaminen tietokantaan

Tietokantaan yhdistäminen suoraan konsolista:
```bash
   psql <DATABASE_URL>
```

### Sovelluksen käynnistäminen

1. **Käynnistä virtuaaliympäristö**:
   ```bash
   poetry shell
   ```
2. **Käynnistä sovellus**:
   ```bash
   python3 src/index.py
   ```
3. **Sovellus käynnistyy osoitteessa**: http://localhost:5001

## Backlogit
* [Product backlog](https://github.com/users/ruokokoski/projects/3)

* [Sprint backlog viikko 1](https://github.com/users/ruokokoski/projects/5)

## Definition of Done:
 - Luokat, metodit ja muuttujat nimetty kuvaavasti englanniksi
 - Koodi täyttää määritellyt PyLint-laatuvaatimukset
 - Robot-testit User Storylle
 - unittest-kattavuus 60% (?)


