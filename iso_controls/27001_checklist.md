# ISO 27001 — Checklist de controles de seguridad
**HITL Lab · Por notebook**

---

## Controles minimos por cada notebook

### A.8 — Gestion de activos de informacion
- [ ] Datos usados son sinteticos — ningun dato real de clientes
- [ ] El .env con credenciales NO esta en GitHub (.gitignore verificado)
- [ ] Las API keys vienen de variables de entorno, nunca hardcodeadas
- [ ] El audit log no contiene el prompt completo — solo el hash

### A.9 — Control de acceso
- [ ] El Jupyter notebook requiere token para acceder (JUPYTER_TOKEN en .env)
- [ ] Redis no esta expuesto publicamente en produccion
- [ ] Las credenciales de cada nube son de un usuario con permisos minimos

### A.12 — Seguridad en operaciones
- [ ] El contenedor Docker corre con usuario no-root (jovyan)
- [ ] Los logs de auditoria son append-only (nunca se sobreescriben)
- [ ] El fallback ISO 22301 no expone informacion sensible del sistema

### A.14 — Seguridad en desarrollo
- [ ] Ningun notebook usa eval() o exec() con input externo
- [ ] Las queries a bases de datos usan parametros, no concatenacion
- [ ] Las dependencias en requirements.txt tienen versiones fijas

---

## Clasificacion de datos en HITL Lab

| Tipo de dato | Clasificacion | Donde aparece |
|---|---|---|
| API keys | CONFIDENCIAL | Solo en .env — nunca en notebooks |
| Datos sinteticos | PUBLICO | notebooks/, data/synthetic/ |
| Audit log | INTERNO | data/audit.jsonl — no subir a GitHub |
| Prompts versionados | INTERNO | Documentados en cada notebook |

---

## Evidencia requerida para auditoria

1. Captura de .gitignore mostrando que .env esta excluido
2. data/audit.jsonl con entradas que muestren solo hashes, no datos reales
3. Confirmacion de que docker-compose.yml usa variables de entorno

---
*Basado en ISO/IEC 27001:2022 — Seguridad de la informacion*
