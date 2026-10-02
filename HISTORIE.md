# Q – Entwicklungsgeschichte von QDB bis zur heutigen Q-Familie

> **Historischer Überblick, keine Open-Source-Freigabe.** Die Q-Produkte werden proprietär als binäre Minecraft-Plugins und Mods bereitgestellt. Alte Entwicklungsstände sind **HISTORISCH / UNGETESTET**, nicht automatisch mit aktuellen Minecraft-, Paper-, Fabric- oder NeoForge-Versionen kompatibel. Vor Experimenten Backups anlegen und nur einen isolierten Testserver/Testclient nutzen.

## Wie Q begann

Die frühe Entwicklung begann als **QDB**: zunächst ein kompakter Mechanismus für Zustands-/Interessenänderungen, dann ein eigenständiger Runtime-Ansatz mit Backpressure, Sichtbarkeit, Session-/Epoch-Schutz und schließlich einem versionierten API-/Capability-Vertrag. Die dokumentierten Phasen waren **QDB 0.1, 0.2 und 0.3**. Es ist derzeit **kein zugehöriges originales QDB-JAR** in den wiedergefundenen physischen Altarchiven bestätigt. Hier wird deshalb auch keines als Download angeboten.

Daraus wuchs **Q-Core** als kleine modulare Grundlage, später **Q-System** als komplette adaptive Performance-Architektur. **Q-Chunky** wurde als eigenständiger Chunk-Spezialist ausgegliedert; anschließend entstanden die Standalone-Bereiche Q-Entity und Q-Player. Die ursprüngliche Idee bleibt: unnötige Arbeit möglichst vermeiden, endliche Budgets/Headroom respektieren, bei Fehlern sicher zurückfallen und keine unbelegten Performanceversprechen machen.

## Nachgewiesene historische Originalversionen im Eigentümerarchiv

Am 02.10.2026 wurde ein physisches älteres Q-Archiv auf Original-JARs, SHA-256, vorhandene Java-Klassen und Paper/Fabric/NeoForge-Metadatendateien untersucht. Der Fund enthält **41 unterschiedliche originale JAR-Binärdateien** in 59 Ablagepfaden. Für eine öffentliche kanonische Auswahl kommen **39 Dateien** infrage (bei je einer älteren Paper-Version von System und Core existierten zwei unterschiedliche Originalvarianten; die Zweitvarianten sollen privat aufbewahrt werden).

| Produkt | Tatsächlich aufgefundene ursprüngliche Versionsnummern | Gefundene Loader je Version |
|:--|:--|:--|
| **Q-System** | 2.0.0, 2.1.0, 2.2.0, 3.0.0, 4.0.0, 4.1.0, 4.1.1, 4.1.2, 4.1.3, 5.0.0, 5.1.0, 5.2.0 | Ältere Versionen teils nur Paper; v5.0.0, 5.1.0, 5.2.0: Paper/Fabric/NeoForge |
| **Q-Core** | 1.0.0, 1.1.0, 1.2.0, 3.0.0, 4.0.0, 4.1.0, 4.1.1, 4.1.2, 4.1.3, 5.0.0, 5.1.0 | Ältere Versionen teils nur Paper; v5.0.0 Fabric/NeoForge und Paper; v5.1.0 alle drei |
| **Q-Chunky** | 1.0.0, 2.0.0 | Jeweils Paper/Fabric/NeoForge |
| **Q-Entity** | Eigenständige spätere Entwicklung | Kein eigenständiger alter JAR im geprüften Altarchiv |
| **Q-Player** | Sehr frühes eigenständiges Q-Produkt | Kein eigenständiger alter JAR im geprüften Altarchiv |

**Wichtig:** Diese Tabelle dokumentiert die physisch wiedergefundenen Dateien; sie ist noch keine Behauptung, dass all diese älteren JARs hier bereits als eigene GitHub Releases hochgeladen wurden. Original-Binärarchive sollen nach abgeschlossener Import- und Sicherheitsprüfung mit echten Prüfsummen in das dauerhafte öffentliche Versionsarchiv aufgenommen werden. Es werden keine aktuellen JARs umbenannt, um fehlende alte Versionsnummern vorzutäuschen. Für Q-System 4.2.1 lag ausdrücklich nur ein fehlender/fehlerhafter Artefaktmarker vor; Q-System 6.1.0 ist als genanntes Entwicklungsthema kein bestätigter vorhandener Original-JAR-Download.

## Die moderne Entwicklungsfamilie

| Q-Produkt | Aktueller nachgewiesener öffentlicher Entwicklungsstand (02.10.2026) | Zweck |
|:--|:--|:--|
| Q-System | v6.4.2 | Vollständige Q-Architektur / Koordination der Funktionsbereiche |
| Q-Core | v5.2.5 | Gemeinsame schlanke Grundlagen, Budget/Headroom |
| Q-Chunky | v2.1.5 | Chunk-Verwaltung, begrenzte intelligente Arbeitslast |
| Q-Entity | v1.1.5 | Entity/AI-Arbeit und sichere Interessenverwaltung |
| Q-Player | v0.1.0 | Frühe Spieler-/Lifecycle-/optionale Client-Komponenten |

Die aktuellen fünf **UNGETESTET / DEVELOPMENT**-Prereleases enthalten je eine tatsächlich gebaute Paper-, Fabric- und NeoForge-JAR plus SHA256 und öffentlichen Entwicklungs-Audit.

## So bleibt das Archiv ab jetzt nachvollziehbar

- Eine neue Dev-Version erscheint erst nach einer substantiell abgeschlossenen Änderung und erfolgreicher technischer Build-/Metadatenprüfung. **Das beweist keine Minecraft-Lauffähigkeit.**
- Experimentelle zukünftige Downloadnamen erhalten sichtbar `-dev`, ein eigenes öffentliches Audit und Hinweise auf tatsächlich belegte Fixes, mögliche Risiken und noch fehlende Tests.
- Alte tatsächlich veröffentlichte Versionen **werden nicht gelöscht**, wenn eine neue Ausgabe erscheint.
- Erst wenn RetroCraft0 eine konkrete Version und Plattform persönlich freigegeben und nachweislich auf CurseForge veröffentlicht hat, wird eine separate Ausgabe ohne `-dev` angezeigt. Historische Dev-Originale bleiben erhalten.

**[Öffentliche Q-Projektbeschreibung](README.md)** · **[Tatsächlich verfügbare Downloads](https://github.com/retrocraft0-hub/Q-Downloads/releases)** · **[Chronologischer Versionsindex](VERSIONEN.md)**

© RetroCraft0. Öffentlich bereitgestellte Binärdateien sind keine Veröffentlichung des privaten Java-Quellcode-Repositories.