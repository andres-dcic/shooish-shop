# Semgrep - SAST (Static Application Security Testing)

**Detecta vulnerabilidades en el código fuente.**

## 📋 Configuración

- **Archivo de reglas:** `rules.yml`
- **Lenguajes soportados:** Python, JavaScript, Java, Go, etc.

## 🔍 Vulnerabilidades que detecta

- SQL Injection
- Cross-Site Scripting (XSS)
- Broken Object Level Authorization (IDOR/BOLA)
- Hardcoded secrets
- Insecure patterns

## 🚀 Uso

```bash
# Desde security/
make semgrep           # Full repo
make semgrep-app       # Solo app/ (vulnerable)
make semgrep-app-secure # Solo app_secure/ (segura)
```

## 📖 Reglas personalizadas

Edita `rules.yml` para agregar nuevas reglas de detección específicas para tu proyecto.

**Documentación:** https://semgrep.dev/docs/
