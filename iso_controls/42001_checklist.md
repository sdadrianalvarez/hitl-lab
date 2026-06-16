# ISO 42001 — Checklist de controles AI
**HITL Lab · Por notebook**

---

## Controles mínimos por cada notebook

- [ ] El prompt está documentado con número de versión (`PROMPT_VERSION`)
- [ ] El sistema prompt define claramente el rol del modelo
- [ ] El output del modelo pasa por revisión humana antes de usarse
- [ ] Se registra en audit log: timestamp, modelo, proveedor, latencia
- [ ] Los supuestos del modelo están declarados explícitamente en el notebook
- [ ] Existe un mecanismo de fallback si el modelo no responde
- [ ] El notebook incluye una celda de reflexión sobre limitaciones del modelo

## Evidencia requerida para auditoría

1. Captura de pantalla del output del modelo
2. Entrada en `data/audit.jsonl` con timestamp y modelo usado
3. Decisión del revisor humano documentada
4. Versión del prompt usada

---
*Basado en ISO/IEC 42001:2023 — Artificial Intelligence Management Systems*
