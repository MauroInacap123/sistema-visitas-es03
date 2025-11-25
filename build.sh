#!/usr/bin/env bash
# Build script para Render.com
set -o errexit

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

echo "👤 Creando superusuario..."
python manage.py createsu

echo "✅ Build completado exitosamente!"
```

### PASO 3: Guardar el archivo

⚠️ **IMPORTANTE:** Asegúrate de que se guarde como `build.sh` (sin extensión `.txt`)

---

## 📁 VERIFICAR UBICACIÓN:

Tu estructura debe verse así:
```
proyecto/
├── SistemaRegistros/
│   ├── management/
│   │   ├── __init__.py          ← Vacío
│   │   └── commands/
│   │       ├── __init__.py      ← Vacío
│   │       └── createsu.py      ← Con código
│   └── ...
├── build.sh                     ← NUEVO ⭐
├── manage.py
├── README.md
└── requirements.txt