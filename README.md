
# 4D5NW Dorker v2.0

Der **4D5NW Dorker** ist ein leichtgewichtiges OSINT-Tool mit grafischer Oberfläche zur automatisierten Dork-Suche und gezielten Extraktion von E-Mail-Adressen bestimmter Domains.

Das Tool nutzt die Suchmaschine **DuckDuckGo**, um Webseiten zu finden, auf denen z. B. `@icloud.com`, `@wunschdomain.de` oder andere Domains auftauchen.

Anschließend werden diese Seiten aufgerufen und konkrete E-Mail-Adressen extrahiert.

---

## ✨ Features

- 🔍 Automatisierte Dork-Suche via DuckDuckGo
- 📧 E-Mail-Extraktion für beliebige Domains (`@gmail.com`, `@wunschdomain.de`, ...)
- 🌓 Darkmode-Umschaltung
- 🕒 Konfigurierbare Verzögerung (1–20 Sekunden) zur Vermeidung von Rate-Limits
- 📊 Fortschrittsbalken für beide Modi
- 📁 Speicherfunktion für Ergebnisse
- 📘 Hilfe-Dialog mit Bedienhinweisen

---

## 🖥️ Screenshot

![4D5NW Dorker GUI](https://i.imgur.com/pFPKNbz.png))

---

## ⚙️ Installation

### 🔗 Voraussetzungen

- Python 3.8+
- Installation der Module:

```bash
pip install duckduckgo-search requests
```

> Falls `tkinter` fehlt (z. B. unter Linux):
> ```bash
> sudo apt install python3-tk
> ```

---

## 🚀 Start

```bash
python dorkscanner.py
```

---

## 🧪 Beispiel-Dorkliste (`dorks.txt`)

```txt
intext:"@wunschdomain.de"
filetype:pdf "@wunschdomain.de"
site:linkedin.com "@wunschdomain.de"
```

---

## 🧰 Bedienung

1. Dork-Liste (.txt) laden  
2. Domains eingeben (z. B. `wunschdomain.de, gmail.com`)  
3. Verzögerung einstellen (15–20 Sekunden empfohlen)  
4. Entweder:
   - Normale Suche → zeigt URLs
   - E-Mail-Extraktion → durchsucht Seiten nach E-Mails  
5. Darkmode aktivieren (optional)  
6. Ergebnisse speichern  
7. Hilfe anzeigen bei Fragen

---

## ⚠️ Hinweise

- DuckDuckGo limitiert schnelle Anfragen → daher Delay nutzen
- Nur öffentlich zugängliche Seiten werden durchsucht
- Bitte **nur für ethische, legale Zwecke** einsetzen

---

## 🧠 Changelog v2.0

- Fortschrittsbalken hinzugefügt
- Darkmode per Checkbox
- GUI-Hilfe integriert
- Toolname auf **4D5NW Dorker** umbenannt

---

## 👨‍💻 Entwickler

> Erstellt von **4D5NW (PBE)**

---

## 📄 Lizenz

Dieses Tool dient zu Ausbildungs- und Testzwecken. Keine kommerzielle Nutzung ohne Genehmigung.
