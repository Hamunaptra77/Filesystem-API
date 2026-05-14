# Filesystem API - Vollständige Dokumentation

## Überblick

Die Filesystem API ist ein hochperformanter, sicherer REST-Service zur Verwaltung von Dateisystem-Operationen. Sie bietet:

- **Sichere Dateiverwaltung** - Mit Zugriffskontrolle auf erlaubte Verzeichnisse
- **Erweiterte Suche** - Nach Dateinamen und Dateiinhalt
- **Diff-Engine** - Sehen Sie Änderungen vor dem Speichern (Dry-Run Mode)
- **Batch-Operationen** - Mehrere Dateien gleichzeitig verarbeiten
- **Fehlertoleranz** - Umfangreiche Fehlerbehandlung und Validierung

## Architecture

```
Client Requests (HTTP/HTTPS)
    ↓
┌─────────────────────────────────────────┐
│   FastAPI Application (Port 8003)       │
│   + CORS Middleware                     │
│   + API Key Authentication              │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│   Path Normalization & Validation       │
│   (Allowed Directories Check)           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│   File System Operations                │
│   (Async I/O via aiofiles)              │
└─────────────────────────────────────────┘
    ↓
    /storage
    ├── project1/
    ├── project2/
    └── ...
```

## Installation & Setup

### 1. Voraussetzungen

- Docker & Docker Compose (empfohlen)
- Python 3.12+ (direkter Start)
- Speicherverzeichnis mit Schreibzugriff

### 2. Mit Docker starten

```bash
# Services starten
cd /home/ki-projekt
docker-compose up -d filesystem-api

# Logs überprüfen
docker-compose logs -f filesystem-api

# Status prüfen
curl -H "X-API-Key: your-key" http://localhost:8003/health
```

### 3. Direkter Start (Entwicklung)

```bash
cd /home/ki-projekt/filesystem-api

# Abhängigkeiten installieren
pip install -r requirements.txt

# API starten
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003
```

## Konfiguration

### Umgebungsvariablen

```bash
# Speicherverzeichnis (wo die Dateien gespeichert werden)
STORAGE_PATH=/storage

# Erlaubte Verzeichnisse (Komma-getrennt)
ALLOWED_DIRECTORIES=/storage,/home/user/projects

# Maximale Dateigröße in Bytes (Standard: 10MB)
MAX_FILE_SIZE=10485760

# CORS Origins (Komma-getrennt)
ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,https://example.com

# API Key für Authentifizierung
FILESYSTEM_API_KEY=your-secure-api-key

# Domain/Service Name
DOMAIN=filesystem-api
```

### Via TOML Datei

Erstellen Sie `config.toml`:

```toml
[server]
storage_path = "/storage"
max_file_size = 10485760

[security]
api_key = "your-secure-api-key"
allowed_directories = ["/storage", "/home/user/projects"]
allowed_origins = ["http://localhost", "https://example.com"]

[service]
domain = "filesystem-api"
```

## API Endpoints Übersicht

### 1. Datei Lesen

**POST** `/read_file`

```bash
curl -X POST http://localhost:8003/read_file \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/project1/file.txt"}'
```

### 2. Datei Schreiben

**POST** `/write_file`

```bash
curl -X POST http://localhost:8003/write_file \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/project1/file.txt",
    "content": "File content here"
  }'
```

### 3. Datei Bearbeiten (mit Diff)

**POST** `/edit_file`

```bash
curl -X POST http://localhost:8003/edit_file \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/project1/file.txt",
    "edits": [
      {
        "oldText": "old content",
        "newText": "new content"
      }
    ],
    "dryRun": false
  }'
```

### 4. Verzeichnis Erstellen

**POST** `/create_directory`

```bash
curl -X POST http://localhost:8003/create_directory \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/new_project"}'
```

### 5. Verzeichnis Auflisten

**POST** `/list_directory`

```bash
curl -X POST http://localhost:8003/list_directory \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage"}'
```

### 6. Verzeichnis Baum

**POST** `/directory_tree`

```bash
curl -X POST http://localhost:8003/directory_tree \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/project1"}'
```

### 7. Nach Dateinamen Suchen

**POST** `/search_files`

```bash
curl -X POST http://localhost:8003/search_files \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage",
    "pattern": "*.py",
    "excludePatterns": ["__pycache__", ".git"]
  }'
```

### 8. Nach Dateiinhalt Suchen

**POST** `/search_content`

```bash
curl -X POST http://localhost:8003/search_content \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage",
    "search_query": "function_name",
    "recursive": true,
    "file_pattern": "*.py"
  }'
```

### 9. Datei/Verzeichnis Verschieben

**POST** `/move_path`

```bash
curl -X POST http://localhost:8003/move_path \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "source_path": "/storage/old_name.txt",
    "destination_path": "/storage/new_name.txt"
  }'
```

### 10. Datei Löschen (mit Bestätigung)

**POST** `/delete_path`

```bash
# Schritt 1: Löschangebot erhalten
curl -X POST http://localhost:8003/delete_path \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/file.txt"}'

# Antwort: {"confirmation_token": "..."}

# Schritt 2: Mit Token bestätigen
curl -X POST http://localhost:8003/delete_path \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/storage/file.txt",
    "confirmation_token": "..."
  }'
```

### 11. Metadaten Abrufen

**POST** `/get_metadata`

```bash
curl -X POST http://localhost:8003/get_metadata \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage/file.txt"}'
```

## Sicherheit

### API Key Authentifizierung

```bash
# Jeder Request benötigt einen gültigen API Key im Header
curl -H "X-API-Key: your-secure-key" http://localhost:8003/...
```

### Erlaubte Verzeichnisse

```bash
# Nur Verzeichnisse in ALLOWED_DIRECTORIES sind zugänglich
ALLOWED_DIRECTORIES=/storage,/home/user/projects

# Zugriff auf /etc/passwd wird blockiert (403 Forbidden)
```

### Maximale Dateigröße

```bash
# Schutz vor DoS-Angriffen
MAX_FILE_SIZE=10485760  # 10 MB

# Größere Dateien: 413 Payload Too Large
```

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| 401 Unauthorized | API Key überprüfen: `-H "X-API-Key: ..."` |
| 403 Forbidden (Path) | Verzeichnis in ALLOWED_DIRECTORIES eintragen |
| 413 Payload Too Large | Datei ist zu groß (MAX_FILE_SIZE prüfen) |
| 404 Not Found | Pfad überprüfen (absolute Pfade verwenden) |
| Datei ist gesperrt | Andere Prozesse greifen auf Datei zu |

## Performance Tipps

1. **Batch-Operationen verwenden** für mehrere Dateien
2. **Dry-Run vor Bearbeitungen** um Fehler zu vermeiden
3. **Suche mit Patterns** eingrenzen (z.B. `*.py` statt `*`)
4. **Große Verzeichnisse** in mehreren Requests auflisten

## Docker Debugging

```bash
# Container betreten
docker-compose exec filesystem-api /bin/bash

# Logs anschauen
docker-compose logs filesystem-api

# Umgebungsvariablen überprüfen
docker-compose exec filesystem-api env | grep -i storage

# Speicherverzeichnis prüfen
docker-compose exec filesystem-api ls -la /storage
```

## Integration mit anderen APIs

```bash
# Datei aus filesystem-api lesen, mit summarizer-api zusammenfassen
# 1. Datei lesen
curl -X POST http://localhost:8003/read_file \
  -d '{"path": "/storage/document.txt"}'

# 2. Mit Summarizer API zusammenfassen
curl -X POST http://localhost:8004/summarize \
  -d '{"text": "<gelesen>", "max_length": 150}'
```

## Skalierung

- **Single Instance:** Unterstützt 1000+ Files gleichzeitig
- **Load Balancing:** Mehrere Instances hinter nginx Load Balancer
- **File Monitoring:** Mit inotify für Dateiänderungen (erweiterte Config)

## Links

- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [Aiofiles Dokumentation](https://github.com/Tinche/aiofiles)
- [OpenAPI Spec](/docs)
- [Healthcheck](/health)
