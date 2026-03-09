<!-- markdownlint-disable MD032 -->
<!-- markdownlint-disable MD022 -->

# Player Insights en Jugadores

## Context
- La vista pública `player_detail_view` ya muestra tabla de posiciones por scope y listado de partidos del jugador.
- Falta una capa intermedia de insights para entender tendencia reciente, compañero recurrente y rivales frecuentes.
- El modelo `Match` no maneja estado adicional de finalización; el conjunto actual de partidos representa partidos jugados.
- Existe helper reutilizable `build_player_matches_queryset(player)` que centraliza el filtro de partidos del jugador.

## Objectives
- Añadir una sección **Player Insights** entre la tabla de posiciones y “Partidos jugados” en la página de detalle de jugador.
- Calcular en backend (sin lógica de negocio en template) tres bloques: Tendencia, Compañero más habitual y Rivales más habituales.
- Mantener consistencia visual con tablas/iconos existentes del ranking (Bootstrap 5 + Bootstrap Icons/patrones actuales).
- Cubrir casos borde y desempates estables mediante tests.
- Compactar verticalmente `player_detail.html`, homogeneizar espaciados entre secciones y unificar formato visual de nombres clicables con `hall_of_fame.html`.
- En `player_detail.html`, mostrar el nombre del jugador en el encabezado principal del detalle (manteniendo “Jugadores” como encabezado solo en `/players/`).

## Scope
### In
- Modificar `player_detail_view` (o helper/service frontend asociado) para calcular insights on-the-fly.
- Reusar `build_player_matches_queryset` y evitar N+1 con `select_related` adecuado.
- Actualizar `frontend/player_detail.html` para renderizar mini-tablas de insights.
- Hacer nombres clicables con patrón existente hacia `player_detail`.
- Reordenar bloques para reducir scroll y mantener separación consistente entre tablas.
- Ajustar tablas de "Compañero habitual" y "Rivales habituales" al mismo orden de columnas que "Tendencia":
  - etiqueta/nombre(s), `🏆-🌴`, `🏓`, `🎯`.
- Agregar/actualizar tests de frontend para validar cálculo, desempates, estado vacío y render.
- Actualizar `CHANGELOG.md` bajo `## [Unreleased]`.

### Out
- Refactors amplios no solicitados.
- Cambios globales de CSS/JS.
- Migraciones de base de datos.
- Cambios fuera de archivos permitidos.

## Risks
- Desempates mal aplicados en compañero/rivales.
  - Mitigación: tests específicos para empate por conteo, win-rate, fecha y id.
- Duplicación de lógica entre vista y template.
  - Mitigación: entregar estructura `player_insights` ya calculada desde backend.
- Regresiones de rendimiento por múltiples queries.
  - Mitigación: una sola carga de partidos del jugador y agregaciones en memoria.
- Inconsistencia visual respecto a tablas existentes.
  - Mitigación: reusar clases Bootstrap y patrón de tabla/clickable-row existente.

## Plan Steps
- [ ] Crear helper backend para construir `player_insights` desde partidos del jugador.
- [ ] Integrar `player_insights` en el contexto de `player_detail_view`.
- [ ] Insertar sección “Player Insights” en `player_detail.html` entre ranking y partidos.
- [ ] Implementar “Tendencia” (últimos 5, últimos 10, total) con `%` entero y `W-L`.
- [ ] Implementar “Compañero más habitual” (top 1) con desempates estables:
  - count desc, win-rate desc, most recent desc, partner id asc.
- [ ] Implementar “Rivales más habituales” (top 3) agrupando pareja rival como tupla ordenada por id y desempates estables:
  - encounters desc, win-rate desc, most recent desc, tuple ids asc.
- [ ] Añadir/actualizar tests en `paddle/frontend/tests/test_players_pages.py` (y/o archivo frontend acotado) cubriendo:
  - 0 partidos, menos de N partidos, más de N partidos.
  - desempates de compañero y rivales.
  - canonicalización de pareja rival.
  - render de links/números esperados.
- [ ] Ejecutar pytest de alcance mínimo relevante y revisar resultados.
- [ ] Actualizar `CHANGELOG.md` en `Unreleased`.
- [ ] Verificar que el diff quede limitado al alcance solicitado.
- [ ] Ajustar `player_detail.html` para:
  - título principal con nombre de jugador en detalle,
  - layout de insights más compacto y espaciado uniforme,
  - links de nombres con estilo visual neutro (sin color de enlace por defecto).
- [ ] Alinear columnas de "Compañero habitual" y "Rivales habituales" con "Tendencia" (nombre(s), rate `🏆-🌴`, partidos, `%`).

## Acceptance Criteria
- `/players/<id>/` muestra sección de insights entre tabla de posiciones y sección de partidos.
- Tendencia contiene 3 filas (5, 10, total) con:
  - porcentaje entero,
  - W-L,
  - número de partidos de la ventana (usando disponibles si son menos),
  - 0% y 0-0 si no hay partidos.
- Compañero más habitual devuelve top 1 correcto con:
  - partidos juntos,
  - win-rate juntos,
  - desempates estables especificados.
- Rivales más habituales devuelve top 3 correcto con:
  - encuentros por pareja rival canonicalizada,
  - win-rate vs pareja,
  - desempates estables especificados.
- Nombres de jugador en insights son clicables al detalle del jugador.
- No hay lógica de negocio en templates.
- Tests relevantes pasan y CHANGELOG se actualiza.

## Validation Commands
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `pytest paddle/frontend/tests/test_players_pages.py paddle/frontend/tests/test_views.py -q`

## Execution Log
- 2026-03-01 - Plan created.
- 2026-03-01 - Scope refined with layout compaction and column-order alignment for insights tables.

## Post-Mortem / Improvements
- Pendiente tras implementación.
- Validar si conviene extraer helper a `frontend/services/` si crece la lógica de insights en futuras iteraciones.
