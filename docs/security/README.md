# 🔒 Security Documentation

This folder contains all security-related documentation and best practices for the Recipe Sharing Platform.

## 📖 Available Guides

### [Security Best Practices](SECURITY.md)
Comprehensive guide covering:
- Why environment variables are essential
- How to properly handle secrets
- Generating secure keys
- What should never be committed to Git
- Environment-specific configuration
- What to do if secrets are accidentally exposed

**Read this before:** Configuring your `.env` file or deploying to production.

## 🔑 Key Security Concepts

### Environment Variables
All sensitive configuration should be stored in `.env` files, never in code.

### Secret Management
- Generate unique secrets for each environment
- Never commit `.env` files to Git
- Rotate secrets regularly
- Use different secrets for dev/staging/production

### Git Security
- Always check `git status` before committing
- Ensure `.env` is in `.gitignore`
- Use `env.example` as a template (safe to commit)

## 🚨 Security Checklist

Before deploying or sharing code:

- [ ] No passwords in `config/settings.py`
- [ ] No API keys in source code
- [ ] No secret keys hardcoded
- [ ] `.env` file exists and is configured
- [ ] `.env` is in `.gitignore` (verified)
- [ ] `env.example` exists as a template
- [ ] All secrets are unique per environment
- [ ] Strong passwords are used

## 📚 Related Documentation

- **Setting up environment variables?** → See [Setup Guide](../getting-started/SETUP_GUIDE.md)
- **Need to generate a SECRET_KEY?** → See [Security Best Practices](SECURITY.md)
- **Project overview?** → See [Main README](../../README.md)

---

*Security is everyone's responsibility. When in doubt, ask!*

