![Build Gluon](https://github.com/ffsh/site/workflows/Build%20Gluon/badge.svg)

# Freifunk Südholstein Site-Konfiguration

In diesem Repository wird die Gluon Konfiguration für Freifunk Südholstein gepflegt.

Für einen Überblick über die Änderungen kannst du unseren [Blog](https://freifunk-suedholstein.de) besuchen.

| Version    | Minimum Vorraussetzung | Kommentar                  |
|------------|------------------------|----------------------------|
| 2021.1.0.0 | 2018.2                 | unter 2018.2 -> 2020.2.3.0 |
| 2022.1.0.0 | 2020.1                 |                            |
| 2023.1.0.0 | 2021.1.2.2             |                            |

https://archiv.firmware.freifunk-suedholstein.de/

## Automation
Public key von actions: 7af457e2719e7a6c0882acc7ff4f7613af0baaa7fd5aab9728a443a1fd07418e

## Firmware selber bauen:

Für das Bauen der Firmware kannst du das ./actions/run-build-local.sh Script verwenden, wenn du alle Abhängigkeiten installiert hast.
Passe das Script an deinen eigenen Bedarf an.

### Mit Docker

Mit Docker brauchst du die Abhängigkeiten nicht selber installieren und der Build wird sich nicht an irgendwelchen fehlenden Abhängigkeiten aufhängen.

Falls du schon mal in der Vergangenheit einen Build erstellt hast, löscht du am besten einfach das gluon Verzeichnis.
```
rm -rf gluon
```
Und checkst das submodule frisch aus.

```
git submodule update --init
```
Schaue dir vor dem build noch mal `actions/run-build-local.sh` an, ob es deinen Bedürfnissen entspricht.
Dann baust du den Container neu und startest den build von gluon.

```
docker build . --tag gluon
docker run --mount type=bind,source=$(pwd),target=/gluon gluon
```
