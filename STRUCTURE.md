# Filesystem API - Projektstruktur

```
filesystem-api/
├── Dockerfile              # Container Image Definition (Python 3.12-slim)
├── README.md               # Hauptdokumentation & Quick Reference
├── SETUP.md                # Ausführliche Setup & Troubleshooting Guide
├── STRUCTURE.md            # Diese Datei - Projektstruktur
├── LICENSE                 # Lizenzinformation
├── requirements.txt        # Python Abhängigkeiten
├── config.py               # Konfigurationsverwaltung
├── config.toml             # TOML Konfigurationsdatei (Optional)
└── app/
    └── main.py             # FastAPI Application + alle Endpoints
```

## Dateien Beschreibung

### Build & Deployment

| Datei | Zweck | Details |
|-------|-------|---------|
| `Dockerfile` | Container Image | Python 3.12-slim, optimiert für Production |
| `requirements.txt` | Python Dependencies | FastAPI, uvicorn, aiofiles, python-multipart |

### Konfiguration

| Datei | Zweck | Format |
|-------|-------|--------|
| `config.py` | Config-Loader | Lädt aus TOML und Environment Vars |
| `config.toml` | Konfiguration | TOML Format (optional) |

### Code

| Datei | Zweck | Größe |
|-------|-------|-------|
| `app/main.py` | Komplette API | ~800 Zeilen FastAPI Code |

### Dokumentation

| Datei | Zweck | Zielgruppe |
|-------|-------|------------|
| `README.md` | Übersicht | Alle Benutzer |
| `SETUP.md` | Detaillierte Anleitung | DevOps / Administratoren |
| `STRUCTURE.md` | Projektstruktur | Entwickler |
| `LICENSE` | Lizenz | Rechtliche Info |

## Architektur

### Entry Point

```
Dockerfile
  ↓
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
  ↓
app/main.py (FastAPI Application)
```

### Request Flow

```
HTTP Request
  ↓
FastAPI Router
  ↓
API Key Check (Security Middleware)
  ↓
CORS Middleware
  ↓
Endpoint Handler
  ↓
Path Validation (normalize_path)
  ↓
Filesystem Operation (aiofiles)
  ↓
Response JSON
```

### Module/Classes

```
app/main.py
├── Middleware
│   ├── CORS
│   └── API Key Authentication
├── Request Models (Pydantic)
│   ├── ReadFileRequest
│   ├── WriteFileRequest
│   ├── EditFileRequest
│   ├── SearchFilesRequest
│   └── ... (weitere Models)
├── Response Models (Pydantic)
│   ├── DirectoryEntry
│   ├── FileMetadata
│   └── SearchResult
├── Utility Functions
│   └── normalize_path()
│   └── search_files()
│   └── search_content()
└── Endpoints
    ├── POST /read_file
    ├── POST /write_file
    ├── POST /edit_file
    ├── POST /create_directory
    ├── POST /list_directory
    ├── POST /directory_tree
    ├── POST /search_files
    ├── POST /search_content
    ├── POST /move_path
    ├── POST /delete_path
    └── POST /get_metadata
```

## Dependencies

### Python Packages

```
fastapi>=0.109.0      # Web Framework
uvicorn>=0.27.0       # ASGI Server
pydantic>=2.0.0       # Data Validation
python-dotenv>=1.0.0  # Environment Variables
aiofiles>=23.0.0      # Async File I/O
python-multipart      # Multipart Form Data
```

### System Libraries

```
In Dockerfile installiert:
├── curl                  # Health Checks
└── ca-certificates       # HTTPS Support
```

## Konfiguration

### Environment Variables (per Docker Compose)

```yaml
environment:
  - STORAGE_PATH=/storage
  - MAX_FILE_SIZE=10485760
  - ALLOWED_ORIGINS=http://localhost,http://127.0.0.1
  - DOMAIN=filesystem-api
  - FILESYSTEM_API_KEY=X1-8CAl9ZOTZjHzNDg-OXGfjwZCjGWrxjMumSI3dcPZ2lbIZUPpdB2zNjjtramKW
```

### Volumes (Docker)

```yaml
volumes:
  - /home/ki-projekt/datenbank/filesystem_data:/storage
```

Die `/storage` wird als Speicherort für alle Dateien verwendet.

## Port Mapping

| Internal | External (Host) | Service |
|----------|-----------------|---------|
| 8003 | 8003 | Filesystem API |

Via API Gateway:
- `http://localhost:8080/api/filesystem/*` → `http://filesystem-api:8003/*`

## Healthcheck

**Endpoint:** `GET /health` (falls implementiert)

**Alternativer Check:**
```bash
curl -X POST http://localhost:8003/list_directory \
  -H "X-API-Key: key" \
  -H "Content-Type: application/json" \
  -d '{"path": "/storage"}'
```

## Build & Run

### Docker Build

```bash
cd filesystem-api
docker build -t filesystem-api:latest .
```

### Docker Run

```bash
docker run -d \
  --name filesystem-api \
  -p 8003:8003 \
  -v /home/ki-projekt/datenbank/filesystem_data:/storage \
  -e STORAGE_PATH=/storage \
  -e FILESYSTEM_API_KEY=your-key \
  filesystem-api:latest
```

### Docker Compose (empfohlen)

```bash
cd /home/ki-projekt
docker-compose up -d filesystem-api
```

## Entwicklung

### Lokal starten (mit Reload)

```bash
cd filesystem-api
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

### OpenAPI UI

```
Swagger UI: http://localhost:8003/docs
ReDoc: http://localhost:8003/redoc
```

## Performance Charakteristiken

| Operation | Durchschnittliche Latenz | Max Dateigröße |
|-----------|--------------------------|-----------------|
| read_file | < 50ms | 10 MB |
| write_file | < 100ms | 10 MB |
| edit_file | < 200ms | 10 MB |
| list_directory | < 100ms | unlimited |
| search_files | 500ms - 5s | depends |
| search_content | 1s - 30s | depends |

## Security Features

- ✅ API Key Authentication (X-API-Key Header)
- ✅ Allowed Directory Whitelisting
- ✅ Max File Size Limiting
- ✅ CORS Protection
- ✅ Path Normalization (verhindert ../ Attacks)
- ✅ Asynchronous I/O (Safe Concurrency)

## Integration Points

```
Filesystem API (8003)
├── API Gateway (8080/api/filesystem/*)
├── Summarizer API (liest Dateien)
├── Memory API (speichert Dateizustände)
└── Open Terminal API (filesystem.exec)
```

## Logging

Alle Requests werden von FastAPI/Uvicorn geloggt:

```bash
# Docker Logs
docker-compose logs -f filesystem-api

# Suchlogmuster
docker-compose logs filesystem-api | grep -i "error\|warning"
```

## Deployment Checklist

- [ ] `STORAGE_PATH` auf existierendes Verzeichnis setzen
- [ ] `FILESYSTEM_API_KEY` auf sicheres Secret setzen
- [ ] `ALLOWED_DIRECTORIES` auf erlaubte Pfade setzen
- [ ] `MAX_FILE_SIZE` für Umgebung anpassen
- [ ] Storage Volume mit ausreichend Platz konfigurieren
- [ ] CORS Origins für Production anpassen
- [ ] Health Checks in Load Balancer konfigurieren

## Troubleshooting

### API antwortet nicht

```bash
# Container läuft?
docker-compose ps filesystem-api

# Logs überprüfen
docker-compose logs filesystem-api

# Mit curl testen
curl http://localhost:8003/docs
```

### Storage nicht zugänglich

```bash
# Volume gemountet?
docker-compose exec filesystem-api ls -la /storage

# Berechtigungen überprüfen
docker-compose exec filesystem-api stat /storage
```

### API Key Fehler

```bash
# Key im Container prüfen
docker-compose exec filesystem-api env | grep API_KEY

# Header in Request prüfen
curl -v -H "X-API-Key: your-key" http://localhost:8003/...
```

## Links

- [Quellcode](./app/main.py)
- [OpenAPI Dokumentation](/docs)
- [FastAPI Framework](https://fastapi.tiangolo.com/)
- [Async Python](https://docs.python.org/3/library/asyncio.html)
