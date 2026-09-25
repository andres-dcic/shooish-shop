# GitHub Actions Workflows - Security Lab

Tres workflows de CI/CD que demuestran diferentes enfoques: básico, inseguro y seguro.

## 📋 Workflows Disponibles

### 1. **basic-workflow.template.yml** - Workflow Básico (Template)
**Trigger:** Push a `main`

**¿Qué hace?**
- ⬇️ Descarga el código
- 🏗️ Ejecuta un build simple
- 📦 Ejecuta un publish simple
- 🚀 Ejecuta un deploy simple

**Características:**
- Workflow básico sin validación de seguridad
- Jobs secuenciales: `build` → `publish` → `deploy`
- Ideal para entender la estructura de GitHub Actions
- Sin escaneos de seguridad

**Resultado esperado:**
```
✅ Build completado
✅ Publish completado
✅ Deploy completado
(sin validación de seguridad)
```

---

### 2. **deploy-insecure.yml** - Deployment Permisivo (Vulnerable)
**Trigger:** Push a `main` o `develop`

**¿Qué hace?**
- ✅ Ejecuta Semgrep (reporta, no bloquea)
- ✅ Ejecuta Gitleaks (reporta, no bloquea)
- ✅ Ejecuta Trivy (reporta, no bloquea)
- 🚀 **DEPLOYA IGUAL** aunque encuentre vulnerabilidades

**Características:**
- `continue-on-error: true` en cada step
- Los escaneos generan reportes (SARIF)
- El deployment **nunca se detiene**
- Ideal para ver cómo se ve un deployment riesgoso

**Resultado esperado:**
```
⚠️  Escaneos reportan vulnerabilidades
🚀 Pero deployment se completa igual
❌ Imagen contiene:
   - SQL Injection
   - XSS
   - IDOR
```

---

### 3. **deploy-secure.yml** - Deployment Seguro
**Trigger:** Push a `production` o `secure`

**¿Qué hace?**
- 🔴 Ejecuta Semgrep (bloquea si encuentra vulnerabilidades)
- 🔴 Ejecuta Gitleaks (bloquea si encuentra secretos)
- 🔴 Ejecuta Trivy FS (bloquea si encuentra vulnerabilidades)
- 🔴 Ejecuta Trivy Image (bloquea si imagen es vulnerable)
- ✅ Despliega **SOLO SI** todas las validaciones pasan

**Características:**
- `exit-code: '1'` en cada step (bloquea en error)
- Sin `continue-on-error`
- Los escaneos son **obligatorios**
- Usa `Dockerfile.secure` (versión corregida)
- Incluye job de tests post-deployment

**Resultado esperado:**
```
✅ Semgrep: Sin vulnerabilidades
✅ Gitleaks: Sin secretos
✅ Trivy: Sin vulnerabilidades
✅ Deploy completado SEGURO
```

---

## 🚀 Cómo Usar

### Workflow Insecuro
```bash
# Push a main o develop
git push origin main

# O disparar manualmente
# En GitHub UI > Actions > Deploy Insecure > Run workflow
```

**Verás:**
- 🟡 Escaneos reportan hallazgos
- 🚀 Deployment continúa de todas formas
- ⚠️ Warnings sobre vulnerabilidades

---

### Workflow Seguro
```bash
# Push a production o secure
git push origin production

# O disparar manualmente
# En GitHub UI > Actions > Deploy Secure > Run workflow
```

**Verás:**
- 🟢 Si hay vulnerabilidades → ❌ BLOQUEADO
- 🟢 Si todo está limpio → ✅ DEPLOYMENT

---

## 📊 Comparación

| Aspecto | Basic | Insecure | Secure |
|---------|-------|----------|--------|
| **Semgrep** | ❌ | Reporta | Bloquea |
| **Gitleaks** | ❌ | Reporta | Bloquea |
| **Trivy** | ❌ | Reporta | Bloquea |
| **Seguridad** | Ninguna | Reporta solo | Valida |
| **Deployment** | Siempre | Siempre | Si pasa validación |
| **Imagen** | N/A | `app/` | `app_secure/` |
| **Rama** | main | main/develop | production/secure |
| **Ideal para** | Aprender Actions | Ver qué NO hacer | Producción |

---

## 🎓 Lecciones

### 📚 Workflow BÁSICO:
- Demuestra estructura fundamental de GitHub Actions
- Build → Publish → Deploy secuencial
- Sin protecciones de seguridad

### ✅ Lo que hace el workflow SEGURO:
1. Bloquea deployments inseguros
2. Fuerza corrección de vulnerabilidades
3. Genera reportes auditables
4. Usa imagen verificada (`app_secure/`)

### ❌ Lo que permite el workflow INSECURO:
1. Deploya código vulnerable
2. Solo genera reportes (no bloquea)
3. Riesgoso para producción
4. Útil para demos de "qué NO hacer"

### 📈 Progresión Recomendada:
1. **Basic** → Entender GitHub Actions
2. **Insecure** → Ver vulnerabilidades ignoradas
3. **Secure** → Ver protecciones en acción

---

## 🔧 Personalización

### Para bloquear más estrictamente:
```yaml
severity: MEDIUM,HIGH,CRITICAL
exit-code: '1'
```

### Para ser más permisivo:
```yaml
severity: CRITICAL
continue-on-error: true
```

### Para agregar más herramientas:
- OWASP Dependency Check
- Snyk
- SonarQube
- Twistlock

---

## 📖 Referencias

- [Semgrep GitHub Action](https://github.com/semgrep/semgrep-action)
- [Gitleaks GitHub Action](https://github.com/gitleaks/gitleaks-action)
- [Trivy GitHub Action](https://github.com/aquasecurity/trivy-action)
- [GitHub Code Scanning](https://docs.github.com/en/code-security/code-scanning)
