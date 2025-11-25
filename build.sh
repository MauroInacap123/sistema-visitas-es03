#!/usr/bin/env bash
# Build script para Render.com
set -o errexit

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input --clear

echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

echo "👤 Creando superusuario..."
python manage.py createsu || echo "⚠️ Superusuario ya existe o error al crear"

echo "✅ Build completado exitosamente!"