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

#### Docker installieren
Es gibt verschiedene Möglichkeiten Docker zu installieren.
Vermutlich kannst du es mit deiner Linux distribution einfach über den Paketmanager installieren, such einfach nach "docker".

Unter Linux wird für gewöhnlich eine docker Gruppe angelegt, wenn du deinen user der docker Gruppe hinzufügst brauchst du docker nicht immer mit root-rechten ausführen.

`sudo usermod -aG docker $USER`

Weitere Informationen: https://docs.docker.com/engine/install/

Alternativ auch gut für Windows mit WSL2: https://rancherdesktop.io/

Docker benötigt in neuen versionen zusätzlich buildx um Images zu bauen.
Das muss extra installiert werden.


#### Image bauen und ausführen

Der erste befehl baut das image und vergibt den namen "gluon" das dauert ein bisschen, denn es müssen ein paar Abhängigkeiten installiert werden.

Du musst das image nicht jedes mal neu bauen. Du kannst den ersten Befehl also auch weg lassen wenn dein image nicht zu alt ist und du bereits eins hast.

Mit `docker image ls` kannst du prüfen ob du schon ein gluon image hast und wie alt es ist.

```
docker buildx build . --tag gluon
docker run --mount type=bind,source=$(pwd),target=/gluon gluon
```
