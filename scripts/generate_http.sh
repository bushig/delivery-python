#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "🔧 Генерация HTTP-роутеров и моделей из OpenAPI контракта..."

BACKUP_MAIN="src/adapters/in_/http/main.py"
BACKUP_INIT="src/adapters/in_/http/routers/__init__.py"

if [ -f "$BACKUP_MAIN" ]; then
  cp "$BACKUP_MAIN" "${BACKUP_MAIN}.bak"
fi

if [ -f "$BACKUP_INIT" ]; then
  cp "$BACKUP_INIT" "${BACKUP_INIT}.bak"
fi

uv run fastapi-codegen \
  --input openapi_contract.yaml \
  --output src/adapters/in_/http \
  --output-model-type pydantic_v2.BaseModel \
  --model-file models \
  --python-version 3.12 \
  --disable-timestamp

if [ -f "${BACKUP_MAIN}.bak" ]; then
  mv "${BACKUP_MAIN}.bak" "$BACKUP_MAIN"
fi

if [ -f "${BACKUP_INIT}.bak" ]; then
  mv "${BACKUP_INIT}.bak" "$BACKUP_INIT"
fi

echo "✅ Генерация завершена!"
echo ""
echo "📁 Сгенерированные файлы:"
echo "   - src/adapters/in_/http/models.py (Pydantic модели)"
echo ""
echo "⚠️  Роутеры и main.py теперь пишутся вручную и не перезаписываются"
