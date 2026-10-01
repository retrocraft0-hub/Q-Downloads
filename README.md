# Q-Reihe – Experimentelle Downloads | RetroCraft0

> ⚠️ **ACHTUNG – UNGETESTETE DEVELOPMENT-VERSIONEN**
>
> Diese Downloads werden aus der laufenden Q-Entwicklung erzeugt. Ein grüner automatischer Java-/JAR-Build bedeutet **nicht**, dass ein Plugin/Mod auf einem echten Minecraft-Server oder -Client stabil funktioniert. Fehler, Datenverlust, Inkompatibilitäten und schlechtere Performance sind möglich. **Nur auf einem Testserver bzw. Testclient verwenden. Vorher Backups machen.** Die ausdrücklich geprüften Vollversionen erscheinen getrennt auf CurseForge.

## Was ist Q?

**Q** ist RetroCraft0s modular entwickelte Minecraft-Performance-Familie für **Minecraft Java 1.21.11 / Java 21**. Die Ausgaben werden unabhängig für **Paper (Server-Plugin)**, **Fabric (Mod)** und **NeoForge (Mod)** gebaut. Das technische Ziel ist nicht, wahllos mehr Aufgaben asynchron auszuführen, sondern unnötige Arbeit zu vermeiden, Tick-Headroom und Ressourcen mit begrenzten Budgets zu verwalten und bei Fehlern möglichst auf das sichere Standardverhalten zurückzufallen (**bounded / fail-open**). Behauptungen über tatsächliche Leistungssteigerungen brauchen reale Messungen; die automatischen Builds allein beweisen sie nicht.

### Die fünf eigenständigen Produkte

| Q-Produkt | Zweck / Entwicklungsziel | Reifestand der hier gelisteten Ausgangsversion |
| --- | --- | --- |
| **Q-System** | Vollständige Q-Performance-Architektur, inklusive der Funktionsbereiche der eigenständigen Q-Produkte; soll gemeinsame Zuständigkeiten ohne Doppelarbeit koordinieren. | Entwicklung / nicht vollumfänglich spielgetestet |
| **Q-Core** | Gemeinsame Performance-Grundlagen, begrenzte Budgets, Headroom und optionale Q-Familienkoordination. | Entwicklung / nicht vollumfänglich spielgetestet |
| **Q-Chunky** | Chunk-bezogene Arbeit, Priorisierung und ressourcenbewusste Chunk-Verarbeitung. | Entwicklung / nicht vollumfänglich spielgetestet |
| **Q-Entity** | Entity-bezogene Optimierung und abgestimmte Beobachter-/Interessenverwaltung. | Entwicklung / nicht vollumfänglich spielgetestet |
| **Q-Player** | Spieler-Lifecycle, Join/Respawn/Dimensionswechsel, Tracking, Chunk-Interessen und optionale Client-Komponenten. **Noch sehr frühe Entwicklungsphase.** | Besonders experimentell |

**LEGO-Prinzip als Entwicklungsziel:** Die Standalone-Produkte sollen unabhängig funktionieren, optionale Q-Nachbarn erkennen und Überschneidungen sicher koordinieren; Q-System soll als Gesamtsystem mit ihnen zusammenarbeiten. Die vollständige plattformübergreifende Umsetzung und Mischinstallation sind **noch kein bestätigtes Releaseversprechen**.

## Plugins und Mods herunterladen

➡️ **[Alle chronologisch geordneten Development-Versionen auf GitHub Releases](https://github.com/retrocraft0-hub/Q-Downloads/releases)**

**[Zur chronologischen Versionsübersicht mit Archiv- und Downloadhinweisen](VERSIONEN.md)**

Die neueste Ausgabe steht oben; ältere Ausgaben bleiben separat abrufbar. Jeder Produkteintrag erhält, sofern erfolgreich gebaut:

| Download in jedem einzelnen Versions-Eintrag | Installationsart |
| --- | --- |
| `Q-PRODUKT-vVERSION.jar` | **Paper: Plugin**, in den Plugin-Ordner des kompatiblen Testservers |
| `Q-PRODUKT-Fabric-vVERSION.jar` | **Fabric: Mod**; jeweils erforderliche Loader-/API-Abhängigkeiten beachten |
| `Q-PRODUKT-NeoForge-vVERSION.jar` | **NeoForge: Mod**, passende Loader-Version beachten |
| `SHA256SUMS` | Prüfsummen aller drei JAR-Dateien |
| `PUBLIC-AUDIT.md` | Öffentlicher Stand: was verifiziert wurde, was noch ungetestet ist und mögliche Risiken |

**Nicht jede Stunde bedeutet eine neue Version.** Nur bei relevanter Änderung am jeweiligen Produkt und erfolgreichen Build-Prüfungen entsteht eine neue experimentelle Ausgabe. Wird nur Q-Player verändert, bleiben die anderen Produktversionen unverändert.

## Chronologisches Versionsregister – bestätigter Ausgangsbestand

Im privaten Entwicklungs-Repository lagen zum Einrichtungszeitpunkt **diese fünf Quellversionen** vor, daraus ergeben sich jeweils drei Loader-Artefakte (15 Ausgaben, nicht 15 unterschiedliche Produktversionsnummern). Ein Eintrag ist erst dann **öffentlich verfügbar**, wenn unter [Releases](https://github.com/retrocraft0-hub/Q-Downloads/releases) die betreffenden JARs wirklich angehängt wurden.

| Produkt | Nachgewiesene Ausgangsversion | Paper / Fabric / NeoForge | Öffentlicher Downloadstatus |
| --- | --- | --- | --- |
| Q-System | **v6.4.2** | je eine JAR vorgesehen | Über Releases prüfen |
| Q-Core | **v5.2.5** | je eine JAR vorgesehen | Über Releases prüfen |
| Q-Chunky | **v2.1.5** | je eine JAR vorgesehen | Über Releases prüfen |
| Q-Entity | **v1.1.5** | je eine JAR vorgesehen | Über Releases prüfen |
| Q-Player | **v0.1.0** | je eine JAR vorgesehen | Über Releases prüfen |

**Ältere Versionen:** Frühere Versionsstände werden ebenfalls aufgenommen, sobald die **tatsächlichen ursprünglichen JAR-Dateien** verfügbar und überprüft sind. Eine bloße Erwähnung einer alten Versionsnummer ist kein Download und wird nicht als vorhandener Release ausgegeben. Neue Builds bekommen pro Produkt einen eigenen datierten GitHub-Prerelease; die Releases-Seite bildet den chronologischen Verlauf.

### Wie lese ich die Versionsberichte?

Jeder neue Download erhält einen öffentlichen Audit, der die Version, Artefakt-Prüfsummen, erfolgreich absolvierte automatisierte Buildprüfungen, nicht ausgeführte Minecraft-Start-/Stress-/Kompatibilitätstests und produktspezifische Risiken enthält. **Bekannte, anhand von Logs oder reproduzierbaren Tests bestätigte Fehler** werden als solche ausgewiesen. Hypothetische Fehler und ungetestete Komponenten werden nicht fälschlich zu bestätigten Bugs erklärt. Im Zweifel lieber einen Build als experimentell/gesperrt ausweisen als ihn als stabil zu verkaufen.

## Stable / Vollversionen

Die geprüften und von RetroCraft0 freigegebenen Versionen werden später als Updates innerhalb der **bestehenden CurseForge-Projekte** veröffentlicht. Ein neuer GitHub-Development-Prerelease ist keine automatische CurseForge-Freigabe. **CurseForge-Links werden erst nach bestätigter Projektzuordnung eingefügt.**

## Download- und Nutzungsrechte

**Kostenlos öffentlich herunterladbare Binaries; KEINE Open-Source-Veröffentlichung.** Es werden keine privaten Java-Quellen, Git-Historien, internen Entwicklungsprotokolle, API-Tokens oder Uploadberechtigungen bereitgestellt. Die JARs dürfen zum persönlichen Ausprobieren und Testen genutzt werden; alle weiteren nicht ausdrücklich gewährten Rechte bleiben bei © RetroCraft0, soweit gesetzlich zulässig. Öffentliche JARs enthalten Bytecode, der technisch dekompiliert werden kann; die Downloadseite ist kein absoluter technischer Kopierschutz.

Besucher dürfen alle öffentlichen Versionen herunterladen, aber ohne ausdrücklich erteilten Schreibzugriff **nicht die Dateien, Versionshinweise oder Veröffentlichungen in diesem Originalrepository ändern**. Der eigentliche Q-Autopilot, die private Quellcodeentwicklung und das CurseForge-Freigabefenster liegen in einem **separaten privaten GitHub-Repository**.
