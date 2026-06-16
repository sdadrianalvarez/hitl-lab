# ISO 22301 — Checklist de continuidad del negocio / DRP
**HITL Lab · Por notebook**

---

## Controles minimos

### Fallback de modelos AI
- [ ] El AIAdapter tiene FALLBACK_RESPONSE definido
- [ ] Si el proveedor activo falla, el fallback responde en < 1 segundo
- [ ] El fallback incluye: mensaje claro + RTO estimado + contacto soporte
- [ ] El is_fallback queda registrado en audit log para analisis posterior

### Disponibilidad del ambiente
- [ ] docker-compose tiene restart: unless-stopped en todos los servicios
- [ ] Redis funciona como cache — si el modelo falla, respuesta en cache
- [ ] El notebook puede correr en modo offline con datos pre-generados

### RTO y RPO definidos

| Componente | RTO | RPO | Estrategia |
|---|---|---|---|
| Modelo AI principal | 30 seg | N/A | Fallback automatico al siguiente proveedor |
| Jupyter Lab | 2 min | N/A | docker-compose restart |
| Redis cache | 1 min | 1 hora | Volumen persistente |
| Audit log | 0 | 1 hora | Append a archivo local |

### Proveedores de respaldo (orden de prioridad)
1. claude — proveedor principal
2. gemini — primer respaldo (latencia baja)
3. openai — segundo respaldo
4. watsonx — respaldo enterprise
5. FALLBACK_RESPONSE — respuesta estatica garantizada

---

## Prueba de continuidad requerida

Ejecuta esto para verificar que el fallback funciona:

`python
# Simula falla del proveedor
import os
os.environ['PROVIDER'] = 'proveedor_inexistente'
from adapters import AIAdapter
adapter = AIAdapter()
respuesta = adapter.complete('test')
assert '[HITL-DRP]' in respuesta
print('Fallback ISO 22301: OK')
`

---

## Evidencia requerida para auditoria

1. Captura del fallback funcionando con proveedor inexistente
2. Entrada en audit log con is_fallback: true
3. docker-compose.yml con restart: unless-stopped documentado

---
*Basado en ISO 22301:2019 — Continuidad del negocio*
