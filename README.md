# Filesystem API

Eine sichere, hochperformante REST API zur Verwaltung von Dateien und Verzeichnissen mit erweiterten Funktionen für das Lesen, Bearbeiten, Schreiben, Suchen und Löschen von Dateien.

**Version:** 2.0.0  
**Framework:** FastAPI + Uvicorn  
**Python:** 3.12+

## Features

✅ **Dateioperationen** - Lesen, Schreiben, Bearbeiten, Verschieben, Löschen  
✅ **Verzeichnisverwaltung** - Erstellen, Auflisten, Baumstruktur  
✅ **Suchfunktionen** - Nach Dateinamen und Dateiinhalt  
✅ **Metadaten** - Größe, Änderungszeit, Dateityp  
✅ **Sicherheit** - API Key, CORS, Allowed Directories  
✅ **Diff-Engine** - Sehen Sie Änderungen vor dem Speichern (Dry-Run)  
✅ **Two-Step Deletion** - Schützen Sie vor versehentlichem Löschen  
✅ **Async/Await** - High-Performance Non-Blocking I/O  
✅ **Fehlerbehandlung** - Umfangreiche, informative Fehlermeldungen

## Installation & Setup

### 1. Docker (Empfohlen)

```bash
# Services starten
cd /home/ki-projekt
docker-compose up -d filesystem-api

# Logs anschauen
docker-compose logs -f filesystem-api
```

### 2. Direkter Start

```bash
cd /home/ki-projekt/filesystem-api

# Abhängigkeiten installieren
pip install -r requirements.txt

# API starten
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003
```

### 3. Umgebungsvariablen

```bash
# Speicherverzeichnis (Standard: /storage)
STORAGE_PATH=/storage

# Erlaubte Verzeichnisse (komma-separiert)
ALLOWED_DIRECTORIES=/storage,/home/user/documents

# API Key (optional)
FILESYSTEM_API_KEY=your-secret-key-here

# CORS Allowed Origins
ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,http://localhost:3000
```

## API-Referenz

### Basis-URL

```
http://localhost:8003
```

### Authentifizierung

Wenn `FILESYSTEM_API_KEY` gesetzt ist, müssen alle Requests diesen Header enthalten:

```
X-API-Key: your-secret-key-here
```

---

## Endpunkte

### 1. Datei lesen

**POST** `/read_file`

Liest den vollständigen Inhalt einer Datei.

**Request:**
```json
{
  "path": "/storage/example.txt"
}
```

**Response (200 OK):**
```json
{
  "content": "Dateiinhalt hier..."
}
```

**Fehler:**
- `404` - Datei nicht gefunden
- `403` - Zugriff verweigert (Pfad nicht erlaubt)
- `500` - Lesefehler

**Beispiel:**
```bash
curl -X POST http://localhost:8003/read_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/config.json"}'
```

---

### 2. Datei schreiben

**POST** `/write_file`

Schreibt Inhalt in eine Datei (überschreibt, wenn bereits vorhanden).

**Request:**
```json
{
  "path": "/storage/new-file.txt",
  "content": "Neuer Dateiinhalt"
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully wrote to /storage/new-file.txt"
}
```

**Fehler:**
- `403` - Schreibzugriff verweigert
- `500` - Schreibfehler

**Beispiel:**
```bash
curl -X POST http://localhost:8003/write_file \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/hello.txt",
    "content": "Hallo Welt!"
  }'
```

---

### 3. Datei bearbeiten (mit Diff)

**POST** `/edit_file`

Wendet mehrere Ersetzungen auf eine Datei an. Nutzen Sie `dryRun: true` um Änderungen zu previwen.

**Request:**
```json
{
  "path": "/storage/config.json",
  "edits": [
    {
      "oldText": "\"debug\": false",
      "newText": "\"debug\": true"
    },
    {
      "oldText": "\"timeout\": 30",
      "newText": "\"timeout\": 60"
    }
  ],
  "dryRun": false
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully edited file /storage/config.json"
}
```

**Response mit Dry-Run (200 OK):**
```json
{
  "diff": "--- a/storage/config.json\n+++ b/storage/config.json\n@@ -1,3 +1,3 @@\n \"debug\": false\n-\"debug\": false\n+\"debug\": true\n"
}
```

**Fehler:**
- `400` - Text nicht gefunden
- `404` - Datei nicht gefunden
- `403` - Zugriff verweigert
- `500` - Bearbeitungsfehler

**Beispiele:**

```bash
# Preview der Änderungen (Dry-Run)
curl -X POST http://localhost:8003/edit_file \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/file.txt",
    "edits": [{"oldText": "alt", "newText": "neu"}],
    "dryRun": true
  }'

# Änderungen anwenden
curl -X POST http://localhost:8003/edit_file \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/file.txt",
    "edits": [{"oldText": "alt", "newText": "neu"}],
    "dryRun": false
  }'
```

---

### 4. Verzeichnis erstellen

**POST** `/create_directory`

Erstellt ein Verzeichnis (mit allen Zwischenverzeichnissen).

**Request:**
```json
{
  "path": "/storage/new/deep/directory/structure"
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully created directory /storage/new/deep/directory/structure"
}
```

**Fehler:**
- `403` - Erstellungsrechte verweigert
- `500` - Erstellungsfehler

**Beispiel:**
```bash
curl -X POST http://localhost:8003/create_directory \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/projects/2024/mai"}'
```

---

### 5. Verzeichnis auflisten

**POST** `/list_directory`

Listet die Inhalte eines Verzeichnisses auf.

**Request:**
```json
{
  "path": "/storage"
}
```

**Response (200 OK):**
```json
{
  "entries": [
    {"name": "file1.txt", "type": "file"},
    {"name": "file2.json", "type": "file"},
    {"name": "subdir", "type": "directory"},
    {"name": ".config", "type": "directory"}
  ]
}
```

**Fehler:**
- `400` - Pfad ist keine Verzeichnis
- `403` - Lesezugriff verweigert
- `500` - Auflistungsfehler

**Beispiel:**
```bash
curl -X POST http://localhost:8003/list_directory \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage"}'
```

---

### 6. Verzeichnis-Baumstruktur

**POST** `/directory_tree`

Gibt eine rekursive Baumstruktur eines Verzeichnisses zurück.

**Request:**
```json
{
  "path": "/storage/projects"
}
```

**Response (200 OK):**
```json
{
  "tree": [
    {
      "name": "2024",
      "type": "directory",
      "children": [
        {
          "name": "mai",
          "type": "directory",
          "children": [
            {"name": "notes.txt", "type": "file", "children": null},
            {"name": "data.json", "type": "file", "children": null}
          ]
        }
      ]
    },
    {
      "name": "archive.zip",
      "type": "file",
      "children": null
    }
  ]
}
```

**Fehler:**
- `400` - Pfad ist nicht vorhanden
- `403` - Lesezugriff verweigert

**Beispiel:**
```bash
curl -X POST http://localhost:8003/directory_tree \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage"}'
```

---

### 7. Dateien suchen

**POST** `/search_files`

Sucht Dateien nach Name/Pattern (Case-Insensitive Substring Match).

**Request:**
```json
{
  "path": "/storage",
  "pattern": "*.json",
  "excludePatterns": ["node_modules", ".git"]
}
```

**Response (200 OK):**
```json
{
  "matches": [
    {"path": "/storage/config.json"},
    {"path": "/storage/data.json"},
    {"path": "/storage/project/settings.json"}
  ]
}
```

**Parameter:**
- `path` (string) - Startverzeichnis
- `pattern` (string) - Suchpattern (Case-insensitive Substring)
- `excludePatterns` (array, optional) - Ausschlussmuster

**Fehler:**
- `400` - Pfad ist nicht vorhanden
- `403` - Lesezugriff verweigert

**Beispiele:**
```bash
# Alle JSON Dateien finden
curl -X POST http://localhost:8003/search_files \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage",
    "pattern": ".json"
  }'

# Mit Ausschlüssen
curl -X POST http://localhost:8003/search_files \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage",
    "pattern": ".py",
    "excludePatterns": ["__pycache__", ".venv"]
  }'
```

---

### 8. Inhalt durchsuchen

**POST** `/search_content`

Sucht nach Text-Inhalten in Dateien.

**Request:**
```json
{
  "path": "/storage",
  "search_query": "TODO",
  "recursive": true,
  "file_pattern": "*.txt"
}
```

**Response (200 OK):**
```json
{
  "matches": [
    {
      "file_path": "/storage/readme.txt",
      "line_number": 5,
      "line_content": "TODO: Update documentation"
    },
    {
      "file_path": "/storage/notes.txt",
      "line_number": 12,
      "line_content": "TODO: Fix the bug"
    }
  ]
}
```

**Parameter:**
- `path` (string) - Startverzeichnis
- `search_query` (string) - Suchtext
- `recursive` (boolean) - Rekursive Suche (default: true)
- `file_pattern` (string) - Dateimuster (default: "*")

**Fehler:**
- `400` - Pfad ist nicht vorhanden
- `403` - Lesezugriff verweigert

**Beispiele:**
```bash
# Einfache Textsuche
curl -X POST http://localhost:8003/search_content \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage",
    "search_query": "error"
  }'

# Python Dateien durchsuchen
curl -X POST http://localhost:8003/search_content \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/code",
    "search_query": "import",
    "file_pattern": "*.py",
    "recursive": true
  }'
```

---

### 9. Metadaten abrufen

**POST** `/get_metadata`

Gibt Metadaten über eine Datei oder ein Verzeichnis zurück.

**Request:**
```json
{
  "path": "/storage/document.pdf"
}
```

**Response (200 OK):**
```json
{
  "path": "/storage/document.pdf",
  "type": "file",
  "size_bytes": 2048576,
  "modification_time_utc": "2024-05-10T14:30:45+00:00",
  "creation_time_utc": "2024-05-01T10:15:20+00:00",
  "last_metadata_change_time_utc": "2024-05-10T14:30:45+00:00"
}
```

**Fehler:**
- `404` - Pfad nicht gefunden
- `403` - Zugriff verweigert

**Beispiel:**
```bash
curl -X POST http://localhost:8003/get_metadata \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/data.json"}'
```

---

### 10. Datei/Verzeichnis verschieben

**POST** `/move_path`

Verschiebt oder benennt eine Datei oder ein Verzeichnis um.

**Request:**
```json
{
  "source_path": "/storage/old-name.txt",
  "destination_path": "/storage/new-name.txt"
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully moved '/storage/old-name.txt' to '/storage/new-name.txt'"
}
```

**Fehler:**
- `404` - Quelldatei nicht gefunden
- `403` - Zugriff verweigert
- `500` - Verschiebungsfehler

**Beispiele:**
```bash
# Datei umbenennen
curl -X POST http://localhost:8003/move_path \
  -H "Content-Type: application/json" \
  -d '{
    "source_path": "/storage/temp.txt",
    "destination_path": "/storage/final.txt"
  }'

# Datei verschieben
curl -X POST http://localhost:8003/move_path \
  -H "Content-Type: application/json" \
  -d '{
    "source_path": "/storage/file.txt",
    "destination_path": "/storage/archive/file.txt"
  }'
```

---

### 11. Datei/Verzeichnis löschen (Two-Step)

**POST** `/delete_path`

Löscht eine Datei oder ein Verzeichnis mit obligatorischer zwei-Stufen-Bestätigung.

#### Step 1: Bestätigungstoken anfordern

**Request:**
```json
{
  "path": "/storage/important-file.txt",
  "recursive": false
}
```

**Response (200 OK):**
```json
{
  "message": "`Confirm deletion of file: /storage/important-file.txt with token abc12`",
  "confirmation_token": "abc12",
  "expires_at": "2024-05-10T14:35:45+00:00"
}
```

#### Step 2: Mit Token löschen

**Request:**
```json
{
  "path": "/storage/important-file.txt",
  "recursive": false,
  "confirmation_token": "abc12"
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully deleted file: /storage/important-file.txt"
}
```

**Fehler:**
- `400` - Token invalid/abgelaufen oder Parameter mismatch
- `404` - Datei nicht gefunden
- `403` - Zugriff verweigert

**Wichtig:**
- Token läuft nach 60 Sekunden ab
- Für nicht-leere Verzeichnisse: `recursive=true` erforderlich
- Path und recursive-Flag müssen in beide Requests gleich sein

**Beispiele:**

```bash
# Step 1: Token anfordern
TOKEN=$(curl -s -X POST http://localhost:8003/delete_path \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/file.txt",
    "recursive": false
  }' | jq -r '.confirmation_token')

echo "Token: $TOKEN"

# Step 2: Mit Token löschen
curl -X POST http://localhost:8003/delete_path \
  -H "Content-Type: application/json" \
  -d "{
    \"path\": \"/storage/file.txt\",
    \"recursive\": false,
    \"confirmation_token\": \"$TOKEN\"
  }"
```

---

## Docker Integration

### Mit API Gateway

Das Filesystem API ist in das API Gateway integriert:

```
http://localhost:8080/api/filesystem/
```

### Docker Compose

```yaml
filesystem-api:
  build:
    context: ./filesystem-api
  container_name: filesystem-api
  working_dir: /app
  ports:
    - "8003:8003"
  volumes:
    - /home/ki-projekt/datenbank/filesystem_data:/storage
  environment:
    - STORAGE_PATH=/storage
    - MAX_FILE_SIZE=10485760
    - ALLOWED_ORIGINS=http://localhost,http://127.0.0.1
  restart: unless-stopped
  networks:
    - ai-net
```

### Container starten

```bash
# Mit Docker Compose
docker-compose up -d filesystem-api

# Logs anschauen
docker-compose logs -f filesystem-api

# In den Container gehen
docker exec -it filesystem-api bash

# Container neu starten
docker-compose restart filesystem-api
```

---

## Sicherheit

### Allowed Directories

Die API kann nur auf Dateien in konfigurierten Verzeichnissen zugreifen:

```bash
ALLOWED_DIRECTORIES=/storage,/home/user/documents,/var/www
```

Versuche, außerhalb dieser Verzeichnisse zuzugreifen, führen zu HTTP 403 Fehlern.

### API Key

Optional API Key für Authentifizierung:

```bash
FILESYSTEM_API_KEY=super-secret-key-12345

# Mit curl verwenden:
curl -H "X-API-Key: super-secret-key-12345" http://localhost:8003/...
```

### CORS

```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,https://example.com
```

---

## Fehlerbehandlung

### Häufige Fehler

| Status | Bedeutung | Lösung |
|--------|-----------|--------|
| 400 | Bad Request | Überprüfen Sie Request-Format und Parameter |
| 403 | Forbidden | Pfad ist nicht in ALLOWED_DIRECTORIES |
| 404 | Not Found | Datei/Verzeichnis existiert nicht |
| 401 | Unauthorized | API Key fehlt oder ist ungültig |
| 500 | Server Error | Systemfehler - siehe Logs |

### Error-Response Format

```json
{
  "detail": "Ausführliche Fehlerbeschreibung"
}
```

---

## Performance-Tipps

1. **Batch-Operationen** - Kombinieren Sie mehrere Edits in einem Request
2. **Dry-Run vor Edit** - Überprüfen Sie Änderungen mit `dryRun: true`
3. **Dateigröße** - API ist optimiert für Textdateien bis zu mehreren MB
4. **Search-Pattern** - Verwenden Sie spezifische Patterns für schnellere Suche
5. **Recursive-Flag** - Setzen Sie auf `false` wenn möglich

---

## Beispiel-Workflows

### Konfigurationsdatei aktualisieren

```bash
# 1. Datei lesen
curl -X POST http://localhost:8003/read_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/config.json"}' | jq .

# 2. Änderungen mit Dry-Run vorschauen
curl -X POST http://localhost:8003/edit_file \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/config.json",
    "edits": [{"oldText": "debug: false", "newText": "debug: true"}],
    "dryRun": true
  }' | jq .

# 3. Änderungen anwenden
curl -X POST http://localhost:8003/edit_file \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/config.json",
    "edits": [{"oldText": "debug: false", "newText": "debug: true"}],
    "dryRun": false
  }' | jq .
```

### Projektstruktur durchsuchen

```bash
# Alle Python-Dateien finden
curl -X POST http://localhost:8003/search_files \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/project",
    "pattern": ".py",
    "excludePatterns": ["__pycache__", ".venv"]
  }' | jq .

# Nach 'import' suchen in Python-Dateien
curl -X POST http://localhost:8003/search_content \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/project",
    "search_query": "import",
    "file_pattern": "*.py"
  }' | jq .
```

### Verzeichnis sicher löschen

```bash
# Step 1: Token anfordern
RESPONSE=$(curl -s -X POST http://localhost:8003/delete_path \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/temp", "recursive": true}')

TOKEN=$(echo $RESPONSE | jq -r '.confirmation_token')
echo "Löschung verlangt Bestätigung. Token: $TOKEN"

# Step 2: Mit Token löschen
curl -X POST http://localhost:8003/delete_path \
  -H "Content-Type: application/json" \
  -d "{
    \"path\": \"/storage/temp\",
    \"recursive\": true,
    \"confirmation_token\": \"$TOKEN\"
  }"
```

---

## Troubleshooting

### API antwortet nicht

```bash
# Container-Status überprüfen
docker-compose ps filesystem-api

# Logs anschauen
docker-compose logs filesystem-api

# Container neu starten
docker-compose restart filesystem-api
```

### Permission Denied Fehler

```bash
# Verzeichnis-Berechtigungen überprüfen
ls -la /home/ki-projekt/datenbank/filesystem_data

# Berechtigungen korrigieren
chmod 755 /home/ki-projekt/datenbank/filesystem_data
```

### ALLOWED_DIRECTORIES Error

Stellen Sie sicher, dass alle konfigurierten Verzeichnisse existieren:

```bash
mkdir -p /storage
mkdir -p /home/user/documents

# Docker Container starten
docker-compose restart filesystem-api
```

---

## API-Dokumentation (Swagger/OpenAPI)

Interaktive API-Dokumentation verfügbar unter:

```
http://localhost:8003/docs
```

---

## Umgebungsvariablen-Referenz

| Variable | Standard | Beschreibung |
|----------|----------|-------------|
| `STORAGE_PATH` | `/storage` | Standard-Speicherverzeichnis |
| `ALLOWED_DIRECTORIES` | `$STORAGE_PATH` | Erlaubte Verzeichnisse (komma-separiert) |
| `FILESYSTEM_API_KEY` | - | Optional API Key für Authentifizierung |
| `ALLOWED_ORIGINS` | `localhost` | CORS Allowed Origins (komma-separiert) |
| `PORT` | `8003` | Port für die API |

---

## Lizenz

Siehe LICENSE im Projekt-Root.

---

## Support

Für Probleme oder Fragen:

1. Logs überprüfen: `docker-compose logs filesystem-api`
2. API-Dokumentation: `http://localhost:8003/docs`
3. Mit API Gateway: `http://localhost:8080/api/filesystem/docs`
