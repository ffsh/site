[![Build Status](https://jenkins.grotax.de/buildStatus/icon?job=FFSH-Firmware)](https://jenkins.grotax.de/job/FFSH-Firmware/)

# Freifunk Südholstein Site-Konfiguration

In diesem Repository wird die Gluon Konfiguration für Freifunk Südholstein gepflegt.

Für einen Überblick über die Änderungen kannst du unseren [Blog](https://freifunk-suedholstein.de) besuchen.

## Branch Struktur

| branch  | gluon-branch    | Kommentar                                          |
|---------|-----------------|----------------------------------------------------|
| dev     | mater           | Nur für Entwickler enthält experimentelle Software |
| testing | v2019.1.x       | Zum testen einer neuen Version für interessierte.  |
| rc      | v2019.1         | Zum erneuten testen (in einer größeren Gruppe)     |
| stable  | v2019.1         | Für alle anderen, **empfohlene** Version           |


## Jenkins

Den aktuellen build Status siehst du oben in dieser README oder du gehst auf [jenkins.grotax.de](https://jenkins.grotax.de). Wenn der Build erfolgreich war, werden die images auf [firmware.grotax.de](https://firmware.grotax.de) veröffentlicht. Diese sind jedoch nicht für das automatische Update freigegeben.

## Firmware selber bauen:

Für das bauen der Firmware haben wir ein Python Script. Dadurch können wir die Firmware automatisch bauen.
Das script kann aber auch zum manuellen bauen genutzt werden. Ein Beispiel findet sich weiter unten.

### build.py Argumente:

| command | value    | make "equivalent" | Kommentar                                       |
|---------|----------|-------------------|-------------------------------------------------|
| -c      | update   | make update       | lädt opwenwrt und wendet gluon patches an       |
| -c      | build    | make build        | baut die firmware                               |
| -c      | clean    | make clean        | löscht alle packages des targets                |
| -c      | dirclean | make dirclean     | löscht alle targets und die toolchain (kaputt!) |
| -c      | sign     | n/a               | signiert die firmware                           |

Weitere Argumente für das Script:

| command | value | default | name | pflicht | Kommentar |
|---|---|---|---|---|----|
| -b | dev or testing or rc or stable | dev | Branch | ja | der Firmware branch |
| -w | site | n/a | Workspace | ja | Pfad zum site Repository |
| -n | 42 | n/a | Build Number | ja | build Nummer wird von jenkins automatisch hochgezählt wird im firmware Namen verwendet |
| -t | ar71xx-generic or ... | all targets | Target | nein | ohne Angabe werden alle Targets gebaut, mit angabe nur der angegebene Target |
| -s | <pfad zu secret> | n/a | Secret | nein | wird nur beim signieren benötigt |
| -d | <pfad zu public directory> | n/a | Directory | nein | wird nur bei -publish benötigt |
| --commit | der verwendete commit | n/a | Commit | ja | commit sha, dient als Refferenz im build.json |
| --cores | 1 bis N | 1 | Cores | nein | Anzahl der zu verwenden Threads, Empfehlung: CPU-Kerne+1 |
| --log | w or s | s | Log | nein | Log level w: nur warnungen/Fehler, s: alles |

Beispiel:
```
./build.py -c update -b dev -n 42 -w $(pwd) --commit $(git rev-parse HEAD)
./build.py -c build -t "ar71xx-tiny" -b dev -n 42 -w $(pwd) --commit $(git rev-parse HEAD)
```
