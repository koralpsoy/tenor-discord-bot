# README.md

## Discord GIF Bot (Tenor v2)

Ein schneller Reaction‑GIF‑Bot für Discord mit echter Zufallsauswahl über die Tenor‑API v2.

---

## 1) Voraussetzungen

* **Discord‑Konto** mit Zugriff auf einen Server (zum Einladen des Bots)
* **Discord Developer Portal** Zugriff (um einen Bot anzulegen)
* **Tenor‑Entwicklerkonto** (für einen Tenor API Key v2)
* **Python ≥ 3.10** auf deinem Rechner/Server

> **Sicherheit:** Veröffentliche **niemals** deinen Bot‑Token oder Tenor‑Key. Drehe (rotieren) die Keys, wenn sie versehentlich geteilt wurden.

---

## 2) Discord Bot – Token & Berechtigungen (Schritt‑für‑Schritt)

1. Öffne das **Discord Developer Portal** und klicke auf **New Application**. Vergib einen Namen und bestätige.
2. Wechsle in der linken Navigation zu **Bot** und klicke **Add Bot**. Bestätige.
3. **Bot‑Token erzeugen/kopieren:** Im Bereich *Token* auf **Reset Token** (falls nötig) und dann **Copy**. Notiere den Token sicher – er kommt später in deine `.env`.
4. **Intents aktivieren:** Unter **Privileged Gateway Intents** aktiviere mindestens **Message Content Intent** (für das Auslesen der Nachrichten‑Inhalte). Optional **Server Members Intent**, falls du Nutzerlisten brauchst.
5. **Einladungs‑Link (OAuth2) erstellen:**

   * Links im Menü **OAuth2 → URL Generator** öffnen.
   * Unter **Scopes** mindestens **bot** anwählen.
   * Unter **Bot Permissions** wähle: **Read Messages/View Channels**, **Send Messages**, **Embed Links**, **Read Message History**. (Optional: **Use Slash Commands**, falls du Slash‑Commands nutzen willst.)
   * Den generierten Link kopieren und im Browser öffnen, um den Bot auf deinen Server einzuladen.

---

## 3) Tenor API Key v2 – erhalten (Schritt‑für‑Schritt)

1. Öffne die **Tenor‑Entwicklerseite** (Tenor API v2 von Google).
2. Melde dich mit deinem Google‑Konto an (falls noch nicht geschehen).
3. **API‑Key anfordern/erstellen:** Folge dem „Request API Key“/„Create Key“‑Prozess. Du gibst i. d. R. App‑Name, Use‑Case und ggf. einen **client\_key** (frei wählbare Kennung, z. B. `discord-reaction-bot`) an.
4. Nach der Bestätigung erhältst du deinen **API Key** (eine Zeichenkette). Bewahre ihn sicher auf – er kommt später in die `.env` unter `TENOR_API_KEY`.
5. (Optional) Prüfe in den Tenor‑Einstellungen, ob **v2** aktiv ist und beachte das Rate‑Limit deiner Nutzung.

> **Beispiel‑Platzhalter** in `.env.example`: `TENOR_EXAMPLE_KEY_1234567890` – **ersetzen** durch deinen echten Key.

---

## 4) Lokale Konfiguration (ohne Code)

1. Erstelle im Projekt eine Datei **`.env`** auf Basis von **`.env.example`**.
2. Trage folgende Werte ein:

   * `DISCORD_TOKEN` → dein eben kopierter Bot‑Token
   * `TENOR_API_KEY` → dein Tenor API Key (v2)
   * `TENOR_CLIENT_KEY` → optional frei wählbar (z. B. `discord-reaction-bot`)
3. Achte darauf, dass **`.env` nicht committet** wird (liegt in `.gitignore`).

---

## 5) Start & Betrieb (ohne Code)

* **Lokal testen:** Virtuelle Umgebung erstellen, Abhängigkeiten installieren, den Bot starten. Beobachte die Konsole auf Fehler (z. B. ungültiger Token).
* **Server‑Betrieb (empfohlen):**

  * *systemd*: Service anlegen, `.env` per `EnvironmentFile` einbinden, Autostart aktivieren, Logs per `journalctl` prüfen.
  * *Docker/Compose*: Image bauen, `.env` via `env_file` einhängen, `restart`‑Policy setzen.
* **Rechte prüfen:** Falls der Bot keine Nachrichten senden darf, überprüfe die Kanal‑ und Rollenrechte auf deinem Server.

---

## 6) Nutzung in Discord

* Präfix ist `?` – Beispiel: `?hug @Name` oder als Reply auf eine Nachricht mit `?hug`.
* `?help` listet alle verfügbaren Kommandos im Bot.

---

## 7) Warum vorher oft dieselben GIFs?

* Ohne Tenor‑Parameter `random=true` kommen häufig dieselben Top‑Ergebnisse.
* Mit größerem `limit` und zusätzlicher Random‑Auswahl steigt die Varianz deutlich.

---

## 8) Sicherheit & Wartung

* Keys niemals im Code committen – nur über `.env`/Server‑Variablen.
* Bei Leaks Token/Key **rotieren**.
* Regelmäßig Abhängigkeiten aktualisieren und Changelog/Änderungen pflegen.

---

## 9) Lizenz & Kontakt

* Lizenz nach Wunsch (z. B. MIT). Kontakt: Maintainer des Repos.

---

# REPO-METADATEN

**Name:** `discord-tenor-gif-bot`

**Beschreibung:** Ein schneller Discord‑Reaction‑Bot mit Tenor v2 (echte Zufallsauswahl), Reply/Mention‑Support und .env‑Konfiguration. Asynchron mit aiohttp.

---

# requirements.txt

discord.py>=2.3
aiohttp>=3.9
python-dotenv>=1.0

---

# .env.example

DISCORD\_TOKEN=PASTE\_YOUR\_DISCORD\_BOT\_TOKEN\_HERE
TENOR\_API\_KEY=TENOR\_EXAMPLE\_KEY\_1234567890
TENOR\_CLIENT\_KEY=discord-reaction-bot

---

# CHANGES.md

### Entfernt / angeglichen

* **Fehlende Kommandos im Mapping**: `oraoraora`, `choke`, `hahagago` wurden entfernt, damit `COMMANDS` und `RESPONSES` konsistent sind.

### Fixes & Verbesserungen

* Tenor‑Zufallsauswahl: `random=true`, höheres `limit` und zusätzliche Random‑Auswahl
* Asynchrones HTTP (keine blockierenden Aufrufe)
* Fallback auf `gif` → `tinygif` → `nanogif`
* Robustere Zielbestimmung: Reply > Mention > Self

---

# bot.py (separat im Repo vorhanden)

*(Der komplette Code liegt als eigene Datei im Repo und ist **nicht** im README enthalten.)*
