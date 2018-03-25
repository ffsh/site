[![Build Status](https://jenkins.grotax.de/buildStatus/icon?job=FFSH-Firmware)](https://jenkins.grotax.de/job/FFSH-Firmware/)

# Freifunk Südholstein Site-Konfiguration

In diesem Repository wird die Gluon Konfiguration für Freifunk Südholstein gepflegt.


## Branch Struktur

| branch  | gluon-branch | Kommentar                                          |
|---------|--------------|----------------------------------------------------|
| dev     | next         | Nur für Entwickler enthält experimentelle Software |
| testing | n/a          | Zum testen einer neuen Version für interessierte.  |
| rc      | n/a          | Zum erneuten testen (in einer größeren Gruppe)     |
| stable  | n/a          | Für alle anderen, empfohlene Version               |


## Firmware selber bauen:

Für das bauen der Firmware haben wir ein Python script. Dadurch können wir die Firmware automatisch bauen. Es kann jedoch auch

### build.py Argumente:

Optionen für -c (command - Befehl):
- build.py -c update ruft make update auf.
    - Muss vor dem bauen ausgeführt werden, aktuallisiert die Abhängigkeiten
- build.py -c build ruft make all auf.
    - Baut die Firmware und erstellt ein manfiest
- build.py -c clean ruft make clean auf.
    - Löscht daten des targets also pakete etc. sollte man nur im Fehlerfall nutzen
- build.py -c sign ruft das sign script auf.
    - Signiert das manifest
- build.py -c publish
    - kopiert die images an einen beliebigen anderen ort (wichtig für jenkins)

Weitere Optionen:
- -b branch, der aktuelle Branch (Pflicht)
- -n Build nummer (jenkins führt diese Nummer, ist beliebig) (Pflicht)
- -w Workspace, das site Verzeichnis (Pflicht)
- --commit, der aktuelle commit (Pflicht)



```
./build.py -c update -b dev -n 42 -w $(pwd) --commit $(git rev-parse HEAD)
./build.py -c build -t "ar71xx-tiny" -b dev -n 42 -w $(pwd) --commit $(git rev-parse HEAD)
```
