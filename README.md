# Google Takeout Flattener

Organiza y limpia exportaciones de Google Photos Takeout automáticamente.

## Características

- Aplana la estructura de carpetas de Google Takeout
- Orden cronológico real usando metadata JSON
- Elimina duplicados usando URL única de Google Photos
- Renombra automáticamente:

R1_IMG0001.jpg
R1_IMG0002.heic
R1_VID0001.mp4

- El archivo más antiguo recibe el número más pequeño
- Limpia archivos sobrantes
- Elimina carpetas vacías automáticamente

## Estructura del proyecto

src/
├── takeout_flattener.py
├── config.py
└── config.example.py

## Configuración

Copia:

config.example.py

como:

config.py

y modifica:

```python
SOURCE_DIR = Path("/ruta/a/Takeout")
DEST_DIR = Path("/ruta/destino")
BACKUP_PREFIX = "R1"
```

## Ejecutar

```bash
cd src
python3 takeout_flattener.py
```

## Ejemplo de salida

```text
R1_IMG0001.jpg
R1_IMG0002.heic
R1_VID0001.mov
```

## Cómo funciona

Google Takeout exporta archivos JSON con metadata.

El proyecto usa:

- photoTakenTime.timestamp → fecha real
- url → identificador único

Esto evita problemas con EXIF inconsistentes.

## Licencia

MIT