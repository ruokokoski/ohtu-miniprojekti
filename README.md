# Ohjelmistotuotanto - Miniprojekti

[![GHA_workflow_badge](https://github.com/ruokokoski/ohtu-miniprojekti/workflows/CI/badge.svg)](https://github.com/ruokokoski/ohtu-miniprojekti/actions)

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
4. **Tietokannan alustus**:
   ```bash
   poetry run python3 src/db_helper.py
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

### Yhteyden ottaminen tietokantaan

Tietokantaan yhdistäminen suoraan konsolista (lähinnä testausta varten):
```bash
   psql <DATABASE_URL>
```

## Dokumentit
* [Product backlog](https://github.com/users/ruokokoski/projects/3)

* [Sprint backlog viikko 1](https://github.com/users/ruokokoski/projects/5)

* [Burndown ja Daily Scrum-muistiinpanot](https://docs.google.com/spreadsheets/d/1luvy2gwmod2LeKPFvA8zie4YPotvT7EOjNS1cLOUY30/edit?gid=1923908994#gid=1923908994)

## Sovelluksen testaus

### Koodin laatutarkasten suoritus
```bash
   poetry run pylint src
```

### Yksikkötestien suoritus
```bash
   poetry run pytest
```

### Testikattavuus html-tiedostoksi
```bash
   poetry shell
   coverage run --branch -m pytest
   coverage html
```

### Robot-testien suoritus
```bash
   bash run_robot_tests.sh
```

## Definition of Done:
 - Toteutus täyttää user storyn vaatimukset
 - Luokat, metodit ja muuttujat nimetty kuvaavasti englanniksi
 - Koodi täyttää määritellyt PyLint-laatuvaatimukset
 - Robot-testit User Storylle
 - unittest-kattavuus >75%

## Current sprint burndown chart
![Alt text](https://docs.google.com/spreadsheets/d/e/2PACX-1vSgmI9CcnHExwW76f3Iid2vBFtww8dJj3gGbKORF8bFOcxoj4qKHqvyHGiRsX7gq379fEPJEW54qcTe/pubchart?oid=1546569514&format=image)
