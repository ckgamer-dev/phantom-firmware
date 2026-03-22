# PHANTOM Firmware - Ghost in the Machine

Custom Firmware für Flipper Zero — via GitHub Actions gebaut.

## So benutzen:

### Schritt 1 — GitHub Account (kostenlos)
→ https://github.com/signup

### Schritt 2 — Dieses Repo auf GitHub hochladen
1. Auf GitHub: **"New repository"** → Name: `phantom-firmware` → **Public** → Create
2. Diese Dateien hochladen (drag & drop auf GitHub)

### Schritt 3 — Build starten
1. Auf GitHub: Tab **"Actions"** klicken
2. **"Build PHANTOM Firmware"** klicken
3. **"Run workflow"** → **"Run workflow"** klicken
4. Warten (~15 Minuten)

### Schritt 4 — Firmware herunterladen
1. Auf den fertigen Build klicken
2. Unter **"Artifacts"**: **PHANTOM-Firmware-v0.1.0** herunterladen
3. ZIP entpacken → `.tgz` Datei

### Schritt 5 — Flashen
- qFlipper öffnen
- Flipper per USB verbinden  
- **"Install from file"** → `.tgz` auswählen
- Fertig! 🎉

## Was PHANTOM macht:
- 👻 6 animierte Boot-Frames (Ghost erscheint)
- 👻 5 Desktop-Animationen (Idle, Hacker, RF, Reveal, NFC)
- 📋 5 About-Seiten (PHANTOM Branding)
- 📡 17 Sub-GHz Frequenzen 300-928 MHz
- 🔧 3 Custom Presets (AM650, FM95, Pager)
