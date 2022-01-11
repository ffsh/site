![Build Gluon](https://github.com/ffsh/site/workflows/Build%20Gluon/badge.svg)

# Freifunk Südholstein Site-Konfiguration

In diesem Repository wird die Gluon Konfiguration für Freifunk Südholstein gepflegt.

Für einen Überblick über die Änderungen kannst du unseren [Blog](https://freifunk-suedholstein.de) besuchen.

| Version  | Minimum Vorraussetzung | Kommentar                  |
|----------|------------------------|----------------------------|
| 2021.1.0 | 2018.2                 | unter 2018.2 -> 2020.2.3.0 |
|          |                        |                            |

## Automation
Public key von actions: c344a75809e3e869667dd1844f8074a2803217c079bcb8dc60e0914a440a7531

## Firmware selber bauen:

Für das bauen der Firmware kannst du das ./actions/run-build-local.sh Script verwenden, wenn du alle Abhängigkeiten installiert hast.
Passe das script an deinen eigenen Bedarf an.

### Mit Docker

Mit Docker brauchst du die Abhängigkeiten nicht selber installieren und der Build wird sich nicht an irgendwelchen Abhängigkeiten aufhängen.

Falls du schon mal in der Vergangenheit einen Build erstellt hast, löscht du am besten einfach das gluon Verzeichniss.
```
rm -rf gluon
```
Und checkst das submodule frisch aus.

```
git submodule update --init
```
Schaue dir vor dem build noch mal `actions/run-build-local.sh` an, ob es deinen Bedürfnissen entspricht.

```
docker build . --tag gluon
docker run --mount type=bind,source=$(pwd),target=/gluon gluon
```