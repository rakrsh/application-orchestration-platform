# EU Cybersecurity Resilience Act (CRA) — Quick Start & Checklist

**Purpose:** Fast-track compliance checklist and week-by-week implementation guide  
**Status:** Active Implementation Phase 1  
**Last Updated:** 2026-08-18

---

## 🎯 Executive Checklist (High-Level Milestones)

### Phase 1: Foundation (Weeks 1–6) – *CRITICAL PATH*

**Week 1–2: SSDLC & Threat Model**
- [ ] Create `docs/SECURITY_REQUIREMENTS.md` (SSDLC overview, design principles)
- [ ] Create `docs/architecture/THREAT_MODEL.md` (STRIDE analysis of all components)
- [ ] Implement code review policy (2+ approvers for security-sensitive code)
- [ ] Enable branch protection on `main` (require reviews, status checks)

**Week 2–3: Security Testing**
- [ ] Migrate to pytest with coverage reporting (target ≥80% for critical paths)
- [ ] Add SAST scanning to CI/CD (.github/workflows/sast.yml)
- [ ] Add dependency scanning: pip-audit, npm audit (.github/workflows/deps.yml)
- [ ] Add container scanning: Trivy (.github/workflows/container-scan.yml)

**Week 3–4: SBOM & Dependency Locking**
- [ ] Generate dependency lock files (requirements.lock via pip-tools, package-lock.json)
- [ ] Add SBOM generation (cyclonedx-bom, syft) to release workflow
- [ ] Configure Dependabot for automated dependency PRs
- [ ] Create `docs/SBOM.md` (where to find, interpretation guide)

**Week 4–6: Vulnerability Management**
- [ ] Publish `docs/SECURITY.md` (vulnerability disclosure policy, reporting instructions)
- [ ] Create `.well-known/security.txt` (RFC 9110 compliant security contact)
- [ ] Set up GitHub Security Advisories
- [ ] Create `docs/INCIDENT_RESPONSE.md` (detection, escalation, notification)

---

### Phase 2: Governance & Audit (Weeks 7–10) – *HIGH PRIORITY*

**Week 7–8: Security Documentation**
- [ ] Complete threat model with data flow analysis
- [ ] Create `docs/DATA_PROTECTION.md` (encryption, retention, GDPR compliance)
- [ ] Create `docs/HARDENING.md` (production security checklist)
- [ ] Create `docs/KNOWN_ISSUES.md` (track CVEs, workarounds)

**Week 8–9: Audit Logging & Secrets**
- [ ] Implement structured audit logging (auth, authz, data changes)
- [ ] Add audit endpoints (GET /audit-logs with filtering/search)
- [ ] Remove hardcoded secrets from docker-compose.yml
- [ ] Create .env.example with placeholder values
- [ ] Add secrets scanning to CI/CD (detect-secrets)

**Week 9–10: Access Control & Review**
- [ ] Document RBAC model and OpenFGA policies
- [ ] Implement least privilege review (reduce default permissions)
- [ ] Create access provisioning checklist (onboarding/offboarding)
- [ ] Schedule quarterly access reviews

---

### Phase 3: Operations & Monitoring (Weeks 11+) – *CONTINUOUS*

**Week 11–12: Security Monitoring**
- [ ] Configure alerting for auth failures, policy violations
- [ ] Build security dashboard (real-time event tracking)
- [ ] Document alert thresholds and escalation

**Week 12–13: Patch Management**
- [ ] Automate security patches (Dependabot configured)
- [ ] Create patch testing workflow
- [ ] Document patch release process
- [ ] Set 30-day SLA for security patch deployment

**Week 14–15: Supply Chain & Compliance**
- [ ] Implement container image signing (cosign)
- [ ] Generate SLSA provenance for builds
- [ ] Create compliance matrix (CRA requirements → implemented controls)
- [ ] Schedule third-party security audit

---

## 📋 Detailed Week-by-Week Tasks

### **WEEK 1: SSDLC & Design**

#### Task 1.1: Security Requirements Document
```
File: docs/SECURITY_REQUIREMENTS.md
Owner: [Architecture Lead]
Time: 1 day
Checklist:
  ✓ Define secure coding principles (input validation, error handling, logging)
  ✓ Document code review requirements
  ✓ Define build & release security gates
  ✓ List approved development practices (testing, logging, secrets handling)
  ✓ Define non-functional security requirements (encryption, audit trails)
```

**Template Start:**
```markdown
# Security Requirements

## Development Practices
- All code must pass SAST scanning before merge
- Security-sensitive changes require security review
- All endpoints must validate input via Pydantic models
- No secrets (API keys, passwords) in code or logs
- Audit all auth and policy decisions
- Use parameterized SQL queries

## Code Review Policy
- Require 2+ approvals for code touching auth, storage, or policy
- Security team reviews changes to encryption, secrets, or access control
- Automated checks: SAST, linting, unit tests must pass

## Testing Requirements
- Unit test all API endpoints
- Integration tests for auth flows
- Code coverage ≥80% for critical paths
- Load testing before major releases

## Deployment Requirements
- Container images signed with cosign
- SBOM generated and published
- Security scanning passes before push to registry
- Secrets injected via environment variables, not config files
```

#### Task 1.2: Threat Model (STRIDE)
```
File: docs/architecture/THREAT_MODEL.md
Owner: [Security Lead]
Time: 2 days
Approach: STRIDE analysis per component
  ✓ Spoofing: Can attacker impersonate a user? (mitigation: OAuth2, Keycloak)
  ✓ Tampering: Can attacker modify data in transit/at rest? (mitigation: TLS, auth checks)
  ✓ Repudiation: Can attacker deny actions? (mitigation: audit logging)
  ✓ Info Disclosure: Can attacker access sensitive data? (mitigation: encryption, RBAC)
  ✓ DoS: Can attacker disrupt service? (mitigation: rate limiting, resource limits)
  ✓ Elevation: Can attacker gain higher privileges? (mitigation: least privilege, RBAC)
```

**Threat Model Output Format:**
```
Component: FastAPI Backend
STRIDE Analysis:
  - Spoofing: Backend trusts X-Auth-Request-User header from OAuth2-Proxy
    Threat: Proxy could be misconfigured, header spoofed
    Mitigation: Validate header presence; sign headers with shared secret (TODO)
    Status: OPEN (implement header signing)
    
  - Tampering: API responses sent over HTTP (unencrypted)
    Threat: Man-in-the-middle could intercept and modify data
    Mitigation: Use HTTPS in production; validate TLS certificates
    Status: IMPLEMENTED (HTTPS enforced)

  - Info Disclosure: Unencrypted database connection
    Threat: Credentials could be intercepted over network
    Mitigation: Use encrypted connections (SSL/TLS for PostgreSQL)
    Status: OPEN (add SSL/TLS to connection string)
```

#### Task 1.3: Code Review Policy
```
File: docs/SECURE_CODING.md
Owner: [Backend Lead + Frontend Lead]
Time: 1 day
Checklist:
  ✓ Define code review process (who reviews, when)
  ✓ List security-sensitive code areas (auth, storage, policy, encryption)
  ✓ Define review checklist for security changes
  ✓ Document approval criteria
  ✓ Define escalation path for security issues
```

**Example Review Checklist:**
```markdown
# Security Code Review Checklist

## Before Submitting PR
- [ ] Input validation: All user inputs validated via Pydantic models
- [ ] Output encoding: No raw SQL; use parameterized queries
- [ ] Error handling: No stack traces or secrets in error messages
- [ ] Logging: Security events (auth, authz, data changes) are logged
- [ ] Secrets: No API keys, passwords, or tokens in code
- [ ] Dependencies: No new dependencies added without justification

## Reviewer Checklist
- [ ] Code follows secure coding guidelines
- [ ] Security-sensitive functions have test coverage >80%
- [ ] No new vulnerabilities introduced
- [ ] Changes align with threat model
- [ ] Audit logging added for data modifications

## Approval
- Security-sensitive changes: Require security team approval
- Regular changes: Require 2+ peer reviews
- Urgent patches: Expedited review; documented review waiver
```

#### Task 1.4: GitHub Branch Protection
```bash
# Enable on GitHub via Settings > Branches > main
  ✓ Require pull request reviews (2+ approvers)
  ✓ Dismiss stale PR approvals
  ✓ Require status checks: CI (tests), SAST (Semgrep), Linting
  ✓ Require branches to be up to date before merging
  ✓ Include administrators in restrictions
  ✓ Require signed commits
```

---

### **WEEK 2–3: Security Testing & SAST**

#### Task 2.1: Pytest Migration
```
File: backend/fastapi/tests/
Owner: [Backend Lead]
Time: 2 days
Checklist:
  ✓ Install pytest: pip install pytest pytest-cov pytest-async
  ✓ Convert unittest tests to pytest fixtures
  ✓ Add coverage tracking: pytest --cov=app --cov-report=html
  ✓ Set coverage threshold: 80% for critical paths
  ✓ Add to CI/CD: .github/workflows/test.yml
  ✓ Document testing guide in docs/TESTING.md
```

**pytest Configuration (pyproject.toml or pytest.ini):**
```ini
[tool:pytest]
testpaths = backend/fastapi/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=backend.fastapi.app --cov-report=html --cov-report=term-missing
```

#### Task 2.2: Add SAST Scanning (Semgrep)
```yaml
# File: .github/workflows/sast.yml
name: SAST Scanning

on: [push, pull_request]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          generateSarif: true
          config: p/security-audit p/python p/django
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: semgrep.sarif
  
  bandit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r backend/fastapi/app/ -f json -o bandit-report.json
      - name: Upload Bandit results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: bandit-report.json
```

#### Task 2.3: Dependency Scanning
```yaml
# File: .github/workflows/deps.yml
name: Dependency Scanning

on: [push, pull_request]

jobs:
  pip-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run pip-audit
        run: |
          pip install pip-audit
          pip-audit --desc --skip-editable
        continue-on-error: true  # Log issues but don't fail build initially
  
  npm-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run npm audit
        working-directory: frontend
        run: npm audit --audit-level=moderate
        continue-on-error: true
```

#### Task 2.4: Container Scanning (Trivy)
```yaml
# File: .github/workflows/container-scan.yml
name: Container Image Scanning

on: [push, pull_request]

jobs:
  trivy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t app-backend:test backend/fastapi/
      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: app-backend:test
          format: sarif
          output: trivy-report.sarif
      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: trivy-report.sarif
```

---

### **WEEK 3–4: SBOM & Dependency Locking**

#### Task 3.1: Generate Lock Files
```bash
# Python: Create requirements.lock via pip-tools
pip install pip-tools
cd backend/fastapi/
pip-compile requirements.txt -o requirements.lock

# Commit both:
git add requirements.txt requirements.lock
git commit -m "Lock dependencies for reproducible builds"

# Node/npm: Ensure package-lock.json is tracked
cd frontend
npm ci  # Uses package-lock.json
git add package-lock.json
git commit -m "Lock npm dependencies"
```

#### Task 3.2: SBOM Generation Script
```python
# File: scripts/generate_sbom.py
import subprocess
import json
from pathlib import Path

def generate_sbom():
    """Generate CycloneDX SBOM for Python and Node dependencies."""
    
    # Python SBOM
    subprocess.run([
        "cyclonedx-bom",
        "-o", "sbom-python.json",
        "-format", "json",
        "backend/fastapi/requirements.lock"
    ], check=True)
    
    # Node SBOM
    subprocess.run([
        "cyclonedx-npm",
        "-o", "sbom-node.json",
        "frontend/"
    ], check=True)
    
    # Merge SBOMs (optional)
    with open("sbom-python.json") as f:
        python_sbom = json.load(f)
    with open("sbom-node.json") as f:
        node_sbom = json.load(f)
    
    # Create merged SBOM metadata
    merged = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "version": 1,
        "metadata": {
            "timestamp": "2026-08-18T00:00:00Z",
            "component": {
                "name": "Application Orchestration Platform",
                "version": "1.0.0"
            }
        },
        "components": python_sbom.get("components", []) + node_sbom.get("components", [])
    }
    
    with open("sbom-merged.json", "w") as f:
        json.dump(merged, f, indent=2)
    
    print(f"✓ Generated SBOMs: sbom-python.json, sbom-node.json, sbom-merged.json")

if __name__ == "__main__":
    generate_sbom()
```

#### Task 3.3: SBOM CI/CD Integration
```yaml
# File: .github/workflows/sbom.yml
name: SBOM Generation

on:
  push:
    tags: 'v*'  # Only on version tags

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install SBOM tools
        run: |
          pip install cyclonedx-bom
          npm install -g @cyclonedx/npm
      - name: Generate SBOM
        run: python scripts/generate_sbom.py
      - name: Upload SBOM to Release
        uses: actions/upload-release-asset@v1
        with:
          upload_url: ${{ github.event.release.upload_url }}
          asset_path: ./sbom-merged.json
          asset_name: sbom-${{ github.ref }}.json
          asset_content_type: application/json
```

#### Task 3.4: Documentation
```markdown
# File: docs/SBOM.md

## Software Bill of Materials (SBOM)

### What is an SBOM?
An SBOM is a complete inventory of all software components, dependencies, and libraries in the application.
Format: CycloneDX JSON (industry standard, machine-readable)

### Where to Find
SBOMs are published with each release:
- GitHub Releases: `sbom-v{version}.json`
- Format: CycloneDX 1.4
- Updated: Every release

### How to Use
```bash
# View components
jq '.components[] | {name, version}' sbom-v1.0.0.json

# Check for specific dependency
jq '.components[] | select(.name=="flask")' sbom-v1.0.0.json

# Compare with NIST NVD for vulnerabilities
# See https://nvd.nist.gov/
```

### License Information
All third-party licenses are included in the SBOM.
Review before deploying in regulated environments.

### Updates
SBOM updated with:
- Every security patch
- New dependency additions
- Dependency version upgrades
```

---

### **WEEK 4–6: Vulnerability Management**

#### Task 4.1: Vulnerability Disclosure Policy
```markdown
# File: docs/SECURITY.md

# Security & Vulnerability Disclosure

## Reporting a Vulnerability

If you discover a security vulnerability, please email **security@example.com** with:
- Description of the vulnerability
- Affected component(s) and versions
- Steps to reproduce (if applicable)
- Suggested fix (if known)

**Do not** open a public GitHub issue for security vulnerabilities.

## Coordinated Disclosure Timeline

- **Immediate:** We acknowledge receipt within 24 hours
- **3 days:** Initial assessment and severity rating
- **7 days:** Proposed fix and timeline for patch
- **Critical (CVSS 9–10):** Patch within 7 days; notify users
- **High (CVSS 7–8):** Patch within 30 days; notify users
- **Medium (CVSS 4–6):** Patch within 90 days; include in next release
- **Low (CVSS 0–3):** Patch in next regular release

## Severity Ratings (CVSS)

| Severity | CVSS | Example | Timeline |
|---|---|---|---|
| Critical | 9.0–10.0 | RCE, auth bypass, data breach | 7 days |
| High | 7.0–8.9 | Privilege escalation, DoS | 30 days |
| Medium | 4.0–6.9 | Unauth info disclosure | 90 days |
| Low | 0.0–3.9 | Low-impact bugs | Next release |

## Supported Versions

| Version | Status | Security Support Until |
|---|---|---|
| 1.x | Current | 2027-08-18 |
| 0.x | Deprecated | 2026-08-18 |

We recommend running the latest version.

## Patch Release Process

1. Fix validated by security team
2. Fix reviewed by engineering team
3. Tests added and pass
4. Version bumped (patch: 1.0.0 → 1.0.1)
5. Release published with security advisory
6. Users notified via GitHub Advisories
```

#### Task 4.2: Create security.txt
```text
# File: .well-known/security.txt (RFC 9110)

Contact: security@example.com
Expires: 2027-08-18T00:00:00.000Z
Preferred-Languages: en, de
Canonical: https://example.com/.well-known/security.txt
Policy: https://example.com/docs/SECURITY.md
Acknowledgments: https://example.com/docs/SECURITY.md#acknowledgments

# Reporting Security Issues:
# Email: security@example.com
# Please do not disclose details publicly until we've had time to respond.
```

#### Task 4.3: GitHub Security Advisories Setup
```
Via GitHub UI:
  1. Go to Settings > Security > Security advisories
  2. Enable "Submit advisories"
  3. On next release, create advisory:
     - Title: "Security advisory: {issue}"
     - Description: Impact, affected versions
     - CVSS score (if applicable)
     - Patch release version
  4. Publish advisory
  5. GitHub auto-notifies users of affected repos
```

#### Task 4.4: Incident Response Runbook
```markdown
# File: docs/INCIDENT_RESPONSE.md

# Security Incident Response Plan

## Overview
This document describes the process for detecting, responding to, and reporting security incidents.

## Severity Levels

| Level | Impact | Response Time | Example |
|---|---|---|---|
| **Critical** | Data breach, RCE, service down | 1 hour | Ransomware, active exploit |
| **High** | Privilege escalation, auth bypass | 4 hours | Unauth access to admin panel |
| **Medium** | Data exposure (limited), DoS | 1 day | Info leak, service slow |
| **Low** | Minor security issue | 1 week | Weak crypto, missing log |

## Detection & Triage

**Who detects?**
- Automated alerts: Security monitoring (Prometheus, CloudWatch)
- Manual reports: Users, security researchers (security@example.com)
- Vulnerability scanning: Automated pipeline (SAST, deps)

**Triage checklist:**
- [ ] Is the issue confirmed?
- [ ] What's the impact (confidentiality, integrity, availability)?
- [ ] How many users/systems affected?
- [ ] Is it actively being exploited?
- [ ] Assign severity level (Critical/High/Medium/Low)

## Response Process

### Step 1: Acknowledge (within 1 hour for Critical)
- Email reporter: "We've received your report. We're investigating."
- Internal: Create incident ticket with details

### Step 2: Investigate (within 4 hours for Critical)
- Reproduce the issue
- Determine root cause
- Assess impact scope
- Update severity if needed

### Step 3: Develop Fix (target time by severity)
- Write fix and tests
- Code review (expedited for Critical)
- Deploy to staging
- Validate fix

### Step 4: Release Patch
- Merge fix to main
- Create patch release (e.g., 1.0.1)
- Publish GitHub release and advisory
- Update SBOM and known issues

### Step 5: Communicate & Document
- Notify users of vulnerability and patch
- Provide remediation steps (e.g., "Update to v1.0.1")
- Document root cause and prevention in runbook
- Update threat model if needed

## Escalation

**Report to authorities if:**
- Critical vulnerability affecting multiple users
- Data breach with >100 records exposed
- Active exploitation in the wild
- Incident reported by government agency

**Who to notify:**
- EU-CERT / ENISA (if EU-based product)
- Affected data protection authority (GDPR data breach)
- Customers (within 72 hours per GDPR Article 33)

## Communication Template

**Subject:** [SECURITY] Patch Available: {Vulnerability Description}

```
Dear Users,

We've identified and fixed a security vulnerability in Application Orchestration Platform.

**Vulnerability:** {Description}
**Severity:** {Critical/High/Medium/Low}
**Affected Versions:** {e.g., v1.0.0, v1.0.1}
**Patched Version:** {e.g., v1.0.2}

**What you need to do:**
1. Update to v1.0.2 immediately
2. Review audit logs for suspicious activity
3. Reset any exposed credentials

**For more details:**
- Security Advisory: [link to GitHub advisory]
- SBOM: [link to SBOM]
- Questions: security@example.com

Thank you for using Application Orchestration Platform.
```

## Post-Incident Review

**Within 1 week, conduct postmortem:**
- What went wrong?
- How did we detect it?
- How fast was our response?
- What can we improve?
- Update runbook with lessons learned

---

## Key Contacts

| Role | Name | Email | Phone |
|---|---|---|---|
| Security Lead | [TBD] | security@example.com | [TBD] |
| Engineering Lead | [TBD] | eng-lead@example.com | [TBD] |
| Product Owner | [TBD] | product@example.com | [TBD] |
| On-Call (24/7) | [TBD] | oncall@example.com | [TBD] |

---

## Testing

Test this runbook quarterly:
- [ ] Simulate a vulnerability report
- [ ] Practice patch release process
- [ ] Validate communication templates
- [ ] Measure response time
```

---

## 📋 Compliance Matrix (Quick Reference)

| CRA Requirement | Implementation | Status | Owner | Due |
|---|---|---|---|---|
| **Article 10: Secure Development** | SSDLC, code review, threat model | 🔴 In Progress | Arch Lead | Week 2 |
| **Article 11: Security Testing** | SAST, DAST, coverage >80% | 🔴 In Progress | Backend | Week 3 |
| **Article 12: Vulnerability Mgmt** | Disclosure policy, severity ratings | 🟡 Planned | Security | Week 4 |
| **Article 13: Incident Response** | Runbook, escalation, communication | 🟡 Planned | Security | Week 6 |
| **Article 14: Documentation** | Threat model, data protection, SBOM | 🟡 Planned | All | Week 8 |
| **Article 15: Update Support** | Patch process, 30-day SLA | 🟡 Planned | DevOps | Week 12 |
| **Supply Chain (implicit)** | SBOM, image signing, SLSA | 🟡 Planned | DevOps | Week 14 |

---

## 🚀 How to Use This Guide

1. **Print or bookmark this page** for daily reference
2. **Assign owners** to each task (update names in checklist)
3. **Create GitHub issues** from tasks (link to this guide)
4. **Track progress** weekly: update status (🔴 → 🟡 → 🟢)
5. **Review bi-weekly** with team; adjust timeline if needed

---

## Resources

- [EU Cyber Resilience Act (Official Text)](https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- [NIST SSDF v1.1](https://csrc.nist.gov/publications/detail/sp/800-218/final)
- [CycloneDX SBOM Format](https://cyclonedx.org/)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OpenSSF Best Practices Badge](https://bestpractices.coreinfrastructure.org/)

---

**Questions?** Refer to [docs/COMPLIANCE_CRA_PLAN.md](COMPLIANCE_CRA_PLAN.md) for detailed guidance.

**Status:** Updated 2026-08-18  
**Next Sync:** Weekly (Fridays, 2 PM CET)
