# Q-Downloads – verifizierbare Veröffentlichung und November-Bereitschaft

**Gültigkeit:** 2026-11-01 · öffentliche Downloadbibliothek, keine privaten Q-Quellen.

Dieses Repository enthält ausschließlich öffentlich freigegebene Binär-Artefakte, öffentliche Prüf-/Nutzungsinformationen und die Download-Website. Es ist **kein Java-Quellarchiv und kein Build-Worker**.

## Was weiterhin streng getrennt bleibt
- Jede Q-Version wird als echte **Q-Produkt × Q-Version × Minecraft Java Release × Plattform/Loader × Java-Ziel**-Kombination geführt.
- `-dev.jar` ist eine **Testversion**. Erfolgreiche CI, JAR-Descriptor-Prüfung und originale SHA sind keine bestätigten Minecraft-Start-/Lasttests.
- Private Java-Dateien, Source-ZIPs, private Manifeste, PATs, Provider-Schlüssel und Zugangsdaten gehören **niemals** in Q-Downloads, seine GitHub Pages oder öffentliche Releases.
- Die öffentliche Website listet nur tatsächlich veröffentlichte GitHub-Release-Links. Bloße Vorhaben und geplante Quoten führen zu keinem neuen Download.
- Die Kennzeichnung als stabile/CurseForge-freigegebene Version erfolgt nur nach persönlicher Freigabe des Inhabers; keine automatische Umbenennung ohne bestätigten Nachweis.

## Technische Aufnahmeprüfung
1. Ein echter Loader-Build wird aus einer eindeutig zugeordneten privaten Quelle kompiliert und die Plattform-/Minecraft-/Java-Metadaten werden am JAR überprüft.
2. Der private Release-Archivar behält Originalbinary, Original-SHA, Prüfergebnis und privaten Source-Snapshot.
3. Die öffentliche Freigabe erhält **dieselben binären Bytes** (SHA-256 identisch), ohne private Source-Snapshots.
4. Der vorhandene Katalog wird erst dann mit der neuen realen Release-Datei aktualisiert, wenn deren tatsächliche GitHub-Release-URL feststeht.
5. `python3 tools/check-release-catalog.py` kontrolliert lokal ohne Netzwerk die fünf Achsen, eindeutige Ziele/Dateinamen, Release-Links, Status und Shard-Zählwerte. Der GitHub-Workflow `Q Downloads site checks` führt diese Prüfung für Änderungen am Webauftritt/Katalog aus.
6. Der Offline-Check **lädt keine JARs herunter** und beweist daher nicht allein das tatsächliche Vorhandensein eines Release-Assets oder dessen SHA. Dafür sind private exakt-HEAD-gesteuerte Publisher- und Release-Prüfungen notwendig.

## Aktueller Stand, noch nicht als Neurelease interpretieren
Die öffentliche Katalogdatei weist am 1. November 2026 weiterhin **16 eigenständige Download-Einträge** aus. Der jüngste verzeichnete Eintrag ist vom **2. Oktober 2026**. Aus der Wiederverfügbarkeit von GitHub-Minuten entsteht kein neuer Release automatisch.

## Bei neuen Anbietern
Neue Build-Dienste werden erst nach Prüfung von legalem Free-Kontingent, hartem 0-€-Kostenstopp, Source-Vertraulichkeit, eingeschränkter API-Berechtigung, nativer Toolchain und reproduzierbaren Build-Checks als nutzbar betrachtet. Die öffentliche Bibliothek erhält keine Zugangsdaten oder direkten Zugriffe auf solche Anbieter. Release und CurseForge bleiben voneinander getrennt.

© RetroCraft0 · Proprietäre JAR-Downloads · Kein öffentlicher Quellcode.
