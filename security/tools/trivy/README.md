# Trivy - Container & Dependency Scanning

**Escanea vulnerabilidades en dependencias, imágenes Docker y configuraciones.**

## 📋 Escaneos disponibles

### 1. **Filesystem Scan**
Analiza archivos de dependencias (requirements.txt, package.json, etc.)

```bash
make trivy
```

### 2. **Dockerfile Scan**
Verifica misconfigurations en archivos Docker

```bash
make trivy-dockerfile          # Dockerfile vulnerable
make trivy-dockerfile-secure   # Dockerfile.secure
```

### 3. **Image Scan**
Escanea imágenes Docker construidas

```bash
make trivy-image          # Imagen vulnerable
make trivy-image-secure   # Imagen segura
```

## 🔍 Vulnerabilidades que detecta

### Dependencias
- CVEs (Common Vulnerabilities and Exposures)
- Versiones desactualizadas
- Librerías con vulnerabilidades conocidas

### Dockerfile
- Usuario root
- Permisos inseguros
- Base images con vulnerabilidades

### Imagen Docker
- Capas vulnerables
- Secretos en archivos
- Misconfigurations

## 🚀 Uso

```bash
# Desde security/
make trivy                     # Full filesystem
make trivy-dockerfile          # Config vulnerable
make trivy-dockerfile-secure   # Config segura
```

## 📊 Severidad

Por defecto escanea: **HIGH** y **CRITICAL**

Edita el Makefile para incluir:
- MEDIUM
- LOW

**Documentación:** https://aquasecurity.github.io/trivy/
