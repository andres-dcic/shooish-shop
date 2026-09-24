# Gitleaks - Secret Scanning

**Busca secretos expuestos en el código y el historio de Git.**

## 📋 Configuración

- **Archivo de configuración:** `config.toml`

## 🔐 Secretos que detecta

- API Keys
- AWS Credentials
- Private Keys (RSA, DSA, etc.)
- Database Passwords
- OAuth Tokens
- JWT Tokens
- Slack/Discord Webhooks
- GitHub Tokens

## 🚀 Uso

```bash
# Desde security/
make gitleaks          # Escanea todo el repo
```

## 🛠️ Configuración personalizada

Edita `config.toml` para:
- Agregar patrones personalizados
- Excluir archivos/directorios
- Configurar reglas específicas

**Documentación:** https://github.com/gitleaks/gitleaks
