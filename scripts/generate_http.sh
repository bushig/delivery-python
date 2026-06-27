#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "🔧 Генерация HTTP-роутеров и моделей из OpenAPI контракта..."

uv run fastapi-codegen \
  --input openapi_contract.yaml \
  --output src/adapters/in_/http \
  --output-model-type pydantic_v2.BaseModel \
  --model-file models \
  --generate-routers \
  --template-dir templates \
  --python-version 3.12 \
  --disable-timestamp

echo "✅ Генерация завершена!"
echo ""
echo "📁 Сгенерированные файлы:"
echo "   - src/adapters/in_/http/models.py (Pydantic модели)"
echo "   - src/adapters/in_/http/routers/*.py (роутеры по тегам)"
echo "   - src/adapters/in_/http/main.py (агрегатор роутеров)"
echo ""
echo "⚠️  Не забудьте подключить роутеры в src/main.py:"
echo "   from src.adapters.in_.http.main import router as http_router"
echo "   app.include_router(http_router, prefix='/api/v1')"
