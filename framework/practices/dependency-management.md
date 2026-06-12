# Dependency Management

> Best practices for managing packages.

---

## Python

```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

## Node.js

```bash
# Install package
npm install package-name

# Install dev dependency
npm install -D package-name
```

## General Rules

- Pin versions in production (use exact versions or lockfiles)
- Audit dependencies regularly (`npm audit`, `pip audit`)
- Minimize dependencies — each one is a maintenance cost
- Use CDN imports in artifacts when possible instead of npm packages
- Classify audit findings: runtime vs build-time vs dev-only vs false-positive
