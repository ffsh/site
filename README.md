[![Build Status](http://jenkins.grotax.de/buildStatus/icon?job=FFSH-Firmware)](http://jenkins.grotax.de/job/FFSH-Firmware/)

# Freifunk Südholstein Site-Konfiguration

In diesem Repository wird die Gluon Konfiguration für Freifunk Südholstein gepflegt.


## Branch Struktur

dev ist der aktive entwicklungs branch hier werden neue gluon versionen vor der veröfentlichung getestet. Aktuell wird als gluon branch next verwendet
testing ist der nächst stabilere branch
rc basiert auf testing
stable basiert auf rc und ist der stablie empfohlene branch

## Neuen Dinge hinzufügen

Wenn du etwas Neues zur Konfiguration hinzufügen willst, wie zum Beispiel einen Schlüssel, dann benutze dafür bitte den Master Branch.

## Eine Version hat einen Fehler

Dann behebe den Fehler in dem entsprechenden Branch, ob die Änderungen in Master übernommen werden, prüfen wir später.



## Firmware selber bauen:

Für das bauen der Firmware haben wir ein pyhton script. Dadurch können wir die firmware automatisch bauen. Es kann jedoch auch

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
