# Bot Learning - Trading Bot from Scratch

## Objetivo
Aprender a construir un bot de trading funcional desde cero, entendiendo cada línea de código.

## Archivos

### `simple_database.py`
Gestión de base de datos SQLite con operaciones CRUD:
- `create_trades_table()` - Crear tabla
- `insert_trade()` - Abrir trade y retornar ID
- `update_trade()` - Cerrar trade y calcular PnL
- `get_trade_by_id()` - Consultar trade específico
- `get_all_trades()` - Ver todos los trades

Funciones de formateo:
- `format_datetime()` - Limpiar fechas
- `format_price()` - Redondear precios a 2 decimales
- `format_size()` - Redondear tamaño a 4 decimales

### `simple_bot.py`
Bot simple que:
1. Descarga datos de AAPL (1 mes, 4h)
2. Calcula volatilidad
3. Si volatilidad > threshold: abre trade
4. Simula cierre (precio +5%)
5. Guarda en BD con PnL calculado

## Conceptos Aprendidos

- SQLite y operaciones CRUD
- Tuplas en Python
- Context managers (`with`)
- Manejo de excepciones
- Formatos de datos
- Análisis técnico básico (volatilidad)
- Ciclo completo de trading: abrir → cerrar → reportar

## Ejecución

```bash
python simple_bot.py
```

## Próximos Pasos
- Agregar scheduler para ejecutar cada hora
- Agregar más estrategias
- Mejorar análisis técnico
- Crear dashboard de resultados