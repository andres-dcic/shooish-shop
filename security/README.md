# Security Tools Configuration

Este directorio contiene la configuración para las 3 herramientas de análisis de seguridad.

## 📁 Estructura

```
security/
├── tools/
│   ├── semgrep/          # SAST - Static Application Security Testing
│   │   └── rules.yml     # Reglas personalizadas para detectar vulnerabilidades
│   │
│   ├── gitleaks/         # Secret Scanning
│   │   └── config.toml   # Configuración para detectar secretos expuestos
│   │
│   └── trivy/            # Container & Dependency Scanning
│       └── README.md     # Documentación de Trivy
│
└── shoosh-shop-v1/       # Referencia - versión anterior
```

---

## 🔧 Herramientas

### 1. **Semgrep** (SAST)
**Ubicación:** `tools/semgrep/rules.yml`

Detecta vulnerabilidades de código como:
- SQL Injection
- XSS (Cross-Site Scripting)
- IDOR/BOLA (Broken Object Level Authorization)

**Uso:**
```bash
make semgrep-app           # Analiza app/ (vulnerable)
make semgrep-app-secure    # Analiza app_secure/ (segura)
```

---

### 2. **Gitleaks** (Secret Scanning)
**Ubicación:** `tools/gitleaks/config.toml`

Busca secretos expuestos en el código:
- API Keys
- Contraseñas
- Tokens
- Credenciales AWS

**Uso:**
```bash
make gitleaks              # Escanea todo el repositorio
```

---

### 3. **Trivy** (Container & Dependency Scanning)
**Ubicación:** `tools/trivy/`

Escanea en múltiples niveles:
- **Filesystem:** Vulnerabilidades en dependencias (requirements.txt, etc.)
- **Dockerfile:** Misconfigurations en archivos Docker
- **Image:** Vulnerabilidades en la imagen construida

**Uso:**
```bash
make trivy                 # Filesystem scan completo
make trivy-dockerfile      # Escanea Dockerfile vulnerable
make trivy-dockerfile-secure # Escanea Dockerfile.secure
make trivy-image           # Escanea imagen construida vulnerable
make trivy-image-secure    # Escanea imagen construida segura
```

---

## 🚀 Ejecutar todos los escaneos

```bash
# Todos los escaneos
make security

# O por herramienta
make semgrep
make gitleaks
make trivy

# Comparar vulnerable vs seguro
make scan-app
make scan-app-secure
```

---

## 📊 Flujo típico de uso

1. **Desarrollo** → Código nuevo en `app/`
2. **Semgrep** → Detecta vulnerabilidades de código
3. **Gitleaks** → Verifica que no haya secretos expuestos
4. **Build Docker** → `make build`
5. **Trivy** → Escanea imagen y dependencias
6. **Fix** → Corregir vulnerabilidades
7. **Verificar** → Repetir escaneos hasta estar limpio

---

## 🛡️ Referencias

- [Semgrep Docs](https://semgrep.dev/docs/)
- [Gitleaks Docs](https://github.com/gitleaks/gitleaks)
- [Trivy Docs](https://aquasecurity.github.io/trivy/)
