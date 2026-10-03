# Q-Reihe – Plugins & Mods für Minecraft

Performance ist nicht nur eine Frage der Serverhardware. Die Q-Reihe beschäftigt sich damit, wie Minecraft Arbeit verteilt, priorisiert und unnötige Belastung vermeidet.

Hier findest du die Q-Plugins und -Mods als Downloads. **Die erste Reihe ist für Minecraft 1.21.11 / Java 21**. Weitere Minecraft- und Java-Versionen werden als eigene Dateien aufgeführt, sobald dafür tatsächlich passende Builds vorhanden sind.

**[Downloadseite mit Sprachwahl](https://retrocraft0-hub.github.io/Q-Downloads/) · [Original-JARs auf GitHub](https://github.com/retrocraft0-hub/Q-Downloads/releases) · [Alle Versionen mit Minecraft und Java](VERSIONEN.md) · [Projektgeschichte](HISTORIE.md)**

Auf der Downloadseite werden zuerst **alle vorhandenen JAR-Dateien** angezeigt; beim Scrollen erscheinen weitere Einträge automatisch. Wenn du gezielt suchen oder nach Minecraft, Java, Q-Version und Plattform filtern möchtest, wähle darüber zuerst eines der fünf Q-Projekte aus. Ein zweiter Klick auf das aktive Projekt öffnet wieder die vollständige Downloadübersicht.

> **Hinweis zu -dev:** Diese Versionen befinden sich noch in Entwicklung. Die JARs wurden gebaut und auf ihre grundlegende Struktur geprüft, aber nicht vollständig im Minecraft-Spielbetrieb getestet. Bitte vorerst nur auf einem Testserver bzw. Testclient verwenden und vorher deine Welt sichern.

## Welches Q brauche ich?

| Projekt | Wofür ist es gedacht? | Verfügbare Version beim Start des Archivs |
| --- | --- | --- |
| **Q-System** | Das Gesamtpaket: verbindet die Bereiche Core, Chunky, Entity und Player. | 6.4.2 |
| **Q-Core** | Verwaltet begrenzte Ressourcenbudgets und berücksichtigt, wie viel Spielraum der Server noch hat. | 5.2.5 |
| **Q-Chunky** | Kümmert sich um die Priorisierung und Verarbeitung von Chunks. | 2.1.5 |
| **Q-Entity** | Konzentriert sich auf die Arbeit rund um Entities und deren Beobachter. | 1.1.5 |
| **Q-Player** | Beschäftigt sich mit spielerbezogenen Vorgängen wie Join, Respawn, Tracking und Dimensionswechsel. Noch in einer frühen Entwicklungsphase. | 0.1.0 |

Die einzelnen Projekte und unterstützten Minecraft-/Java-Versionen werden unabhängig weiterentwickelt. Ein Fix für Paper auf Java 17 bedeutet also nicht automatisch ein Update für Java 21, Fabric oder NeoForge. Q-System ist als Gesamtpaket gedacht; die anderen Q-Projekte sind die eigenständigen Teilbereiche. Das Zusammenspiel verschiedener Q-Module ist noch nicht vollständig im Spielbetrieb geprüft.

## Download & Installation

Wähle bei der gewünschten Version einfach die passende Datei aus:

| Datei | Wohin damit? |
| --- | --- |
| `Q-Name_Paper_Vx.x.x-dev.jar` | Paper-Plugin – in den Ordner `plugins/` deines Testservers |
| `Q-Name_Fabric_Vx.x.x-dev.jar` | Fabric-Mod – in `mods/`; passende Fabric-Abhängigkeiten beachten |
| `Q-Name_NeoForge_Vx.x.x-dev.jar` | NeoForge-Mod – in `mods/`; passende NeoForge-Version beachten |

Du brauchst nur die JAR deiner Plattform, nicht alle drei. Weitere Dateien wie `SHA256SUMS` dienen der Prüfung des Downloads.

**Was hat sich geändert?** Die Neuerungen und bekannten Einschränkungen stehen beim jeweiligen Release. In der [Versionsübersicht](VERSIONEN.md) findest du die Downloads nach Datum, Produkt und Plattform sortiert. Ältere Versionen bleiben verfügbar.

## Noch wichtig

- `-dev` steht für eine experimentelle Ausgabe. Es ist **keine** als stabil bestätigte Version.
- Ein erfolgreicher Build ist kein Beweis für weniger Lag oder bessere FPS. Solche Aussagen machen wir erst mit passenden Praxismessungen.
- Die Downloads sind kostenlos nutzbare, **proprietäre JAR-Dateien** – das Projekt ist nicht Open Source. Der Java-Quellcode wird hier nicht veröffentlicht. © RetroCraft0.

## Fehler melden und Wünsche einreichen

Ist dir beim Testen etwas aufgefallen? Du kannst direkt hier ein öffentliches Feedbackformular ausfüllen:

- **[Fehler melden](https://github.com/retrocraft0-hub/Q-Downloads/issues/new?template=bug-report.yml)** – mit Produkt, Plattform, exakter Q-JAR, Minecraft-/Java-Version, Schritten zum Nachstellen und optional gekürztem Log.
- **[Verbesserung vorschlagen](https://github.com/retrocraft0-hub/Q-Downloads/issues/new?template=feature-request.yml)** – für neue Funktionen, ältere/neue Minecraft-Versionen und weitere Plattformen.
- **[Bereits gemeldete Probleme und Kommentare ansehen](https://github.com/retrocraft0-hub/Q-Downloads/issues)** – du kannst dort auch auf eine vorhandene Meldung antworten.

Meldungen werden für die weitere Q-Entwicklung regelmäßig ausgewertet. Bitte keine privaten IP-Adressen, Zugangsdaten, Tokens, Spieler-UUIDs oder ungekürzte persönliche Logs öffentlich posten. Ein Report ist zunächst ein Hinweis und kein bereits bestätigter Fehler.
