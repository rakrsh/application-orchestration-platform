# EU Cybersecurity Resilience Act (CRA) Compliance Plan

**Status:** Draft - Initial Assessment & Planning  
**Last Updated:** 2026-08-18  
**Platform:** Application Orchestration Platform  

---

## Executive Summary

This document outlines the Application Orchestration Platform's roadmap to achieve compliance with the **EU Cybersecurity Resilience Act (Cyber Resilience Act)**, which establishes security and resilience requirements for software products placed on the EU market.

### Current State
- ✅ **Implemented:** Authentication (Keycloak, OAuth2-Proxy), authorization (OpenFGA), basic input validation, OpenTelemetry observability
- ❌ **Missing:** Formal SSDLC, security testing, SBOM, vulnerability management, incident response procedures, audit logging, dependency scanning

### Compliance Scope
This plan addresses the CRA's core security obligations across 8 key areas with phased implementation (Phase 1–3).

---

## Part A: CRA Core Requirements Overview

The EU Cyber Resilience Act mandates that software manufacturers must:

| Requirement | Description | Priority |
|---|---|---|
| **Secure Software Development** | Establish and maintain SSDLC with documented design, testing, and vulnerability management | **P1** |
| **Security Testing & Validation** | Perform security testing, code review, vulnerability scanning, and penetration testing before release | **P1** |
| **Software Bill of Materials (SBOM)** | Generate and maintain SBOM in CycloneDX/SPDX format; track all dependencies | **P1** |
| **Vulnerability Management** | Establish vulnerability disclosure, assessment, and coordinated disclosure procedures | **P1** |
| **Security Update Support** | Provide security updates for known vulnerabilities; maintain product support timeline | **P2** |
| **Incident Response** | Document incident response plan; report critical vulnerabilities to authorities if needed | **P2** |
| **Security Documentation** | Publish security documentation, threat model, and known limitations | **P2** |
| **Supply Chain Security** | Validate dependencies; implement secure build and release processes | **P3** |

---

## Part B: Gap Analysis & Implementation Plan

### Phase 1: Foundation (Weeks 1–6) – Core Security Practices

#### 1.1 Secure Software Development Lifecycle (SSDLC)

**Current State:**
- Ad-hoc development with basic CI/CD (linting, tests)
- No formal security requirements, threat modeling, or design review process

**CRA Requirement:**
- Document security design and threat model
- Implement secure coding practices and code review process
- Establish secure build and release pipeline

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **1.1.1** Create Security Requirements Document | docs/SECURITY_REQUIREMENTS.md with SSDLC overview | Architecture | 1 day | Not Started |
| **1.1.2** Document Threat Model (C4-based) | docs/architecture/THREAT_MODEL.md (data flows, threats, controls) | Architecture | 2 days | Not Started |
| **1.1.3** Establish Secure Code Review Policy | docs/SECURE_CODING.md with guidelines for Python/TypeScript/SQL | Backend Lead | 1 day | Not Started |
| **1.1.4** Implement Code Review Workflow | GitHub branch protection rules, mandatory PR review | DevOps | 0.5 day | Not Started |
| **1.1.5** Document Build & Release Process | docs/BUILD_RELEASE_PROCESS.md with security checks | DevOps | 1 day | Not Started |

**Success Criteria:**
- [ ] Security design document published and reviewed
- [ ] All code PRs require peer review before merge
- [ ] Build pipeline includes security gates (no unsigned commits, version tags)

---

#### 1.2 Security Testing & Validation

**Current State:**
- Basic unit tests (unittest); no coverage tracking
- No security testing, SAST, dependency scanning, or DAST

**CRA Requirement:**
- Perform static analysis (SAST), dynamic analysis (DAST), and dependency scanning
- Achieve code coverage >80% for critical paths
- Validate security controls before release

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **1.2.1** Migrate to pytest with coverage reporting | backend/fastapi/tests/ uses pytest; coverage target 80%+ | Backend | 2 days | Not Started |
| **1.2.2** Integrate SAST (Semgrep or Snyk Code) | .github/workflows/sast.yml runs on all PRs | Security | 1 day | Not Started |
| **1.2.3** Integrate dependency scanning | .github/workflows/deps.yml runs pip-audit, npm audit | Security | 1 day | Not Started |
| **1.2.4** Add container image scanning | .github/workflows/container-scan.yml (Trivy/Snyk) | Security | 1 day | Not Started |
| **1.2.5** Create security testing checklist | docs/SECURITY_TESTING_CHECKLIST.md before each release | QA | 0.5 day | Not Started |
| **1.2.6** Establish integration tests | backend/fastapi/tests/test_integration.py (auth, API, policy flows) | Backend | 3 days | Not Started |

**Success Criteria:**
- [ ] All CI/CD pipelines include SAST and dependency scanning
- [ ] Code coverage ≥80% for critical paths (auth, storage, validation)
- [ ] No high/critical vulnerabilities in dependencies
- [ ] Integration tests pass for all critical user flows

**Tools to Add:**
```yaml
# Python SAST & Dependency Scanning
semgrep
bandit
pip-audit

# Node/npm scanning
npm audit (built-in)

# Container scanning
trivy
```

---

#### 1.3 Software Bill of Materials (SBOM) Generation

**Current State:**
- No SBOM generated or tracked
- No formal dependency inventory

**CRA Requirement:**
- Generate SBOM in CycloneDX or SPDX format
- Include all direct and transitive dependencies
- Update SBOM with each release
- Make SBOM publicly available (in release artifacts)

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **1.3.1** Add SBOM generation tool (cyclonedx-bom or syft) | Generate SBOM on release (Python + Node) | DevOps | 1 day | Not Started |
| **1.3.2** Configure SBOM artifact creation | .github/workflows/release.yml generates sbom.json | DevOps | 1 day | Not Started |
| **1.3.3** Create SBOM documentation | docs/SBOM.md (where to find, how to use) | Documentation | 0.5 day | Not Started |
| **1.3.4** Add dependency lock files | Commit requirements.lock (pip-tools) and package-lock.json | Backend/Frontend | 1 day | Not Started |

**Success Criteria:**
- [ ] SBOM generated in CycloneDX format on each release
- [ ] All direct and transitive dependencies included
- [ ] SBOM published in GitHub Releases
- [ ] Lock files tracked in version control

**SBOM Generation Command Example:**
```bash
# Python SBOM (using cyclonedx-bom)
cyclonedx-bom -o sbom-python.json -format json backend/fastapi/requirements.lock

# Node SBOM
cyclonedx-npm -o sbom-node.json frontend/
```

---

#### 1.4 Vulnerability Management & Coordinated Disclosure

**Current State:**
- No formal vulnerability management process
- No security contact or disclosure policy

**CRA Requirement:**
- Establish vulnerability disclosure procedure
- Coordinate with discoverers on remediation timeline
- Document and report handling of critical vulnerabilities
- Provide vulnerability management contact (security.txt)

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **1.4.1** Create vulnerability disclosure policy | docs/SECURITY.md (reporting, embargo, remediation timeline) | Security | 1 day | Not Started |
| **1.4.2** Create security contact | .well-known/security.txt (RFC 9110 compliant) | Security | 0.5 day | Not Started |
| **1.4.3** Document vulnerability assessment procedure | docs/VULNERABILITY_ASSESSMENT.md (severity levels, CVSS) | Security | 1 day | Not Started |
| **1.4.4** Set up security mailing list or triage | security@[domain] or GitHub security advisories | DevOps | 0.5 day | Not Started |
| **1.4.5** Create incident response runbook | docs/INCIDENT_RESPONSE.md (detection, escalation, notification) | Security | 2 days | Not Started |

**Success Criteria:**
- [ ] docs/SECURITY.md published with vulnerability disclosure instructions
- [ ] .well-known/security.txt available at platform domain
- [ ] Response timeline: critical (24h), high (7d), medium (30d)
- [ ] GitHub Security Advisory feature enabled

**Example security.txt:**
```
Contact: security@example.com
Expires: 2027-08-18T00:00:00.000Z
Preferred-Languages: en
Canonical: https://example.com/.well-known/security.txt
```

---

### Phase 2: Governance & Documentation (Weeks 7–10) – Policies & Audit

#### 2.1 Security Documentation & Threat Model

**Current State:**
- Architecture documented (C4 model)
- No published threat model, data protection, or security properties

**CRA Requirement:**
- Publish threat model and security assumptions
- Document known limitations and recommendations
- Describe data handling and privacy measures
- Create security hardening guide

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **2.1.1** Create detailed threat model | docs/architecture/THREAT_MODEL.md (STRIDE analysis) | Security | 3 days | Not Started |
| **2.1.2** Document data protection & privacy | docs/DATA_PROTECTION.md (encryption, retention, GDPR) | Security/Privacy | 2 days | Not Started |
| **2.1.3** Create security hardening guide | docs/HARDENING.md (production deployment, secrets, TLS) | DevOps | 2 days | Not Started |
| **2.1.4** Document known limitations & CVEs | docs/KNOWN_ISSUES.md (CVEs in dependencies, workarounds) | Security | 1 day | Not Started |
| **2.1.5** Create API security guide | docs/API_SECURITY.md (authentication, rate limiting, CORS) | Backend | 1 day | Not Started |

**Success Criteria:**
- [ ] Threat model published and includes STRIDE analysis
- [ ] Data protection doc covers encryption, PII handling, retention
- [ ] Hardening guide covers TLS, secrets management, logging
- [ ] Known issues tracked and communicated

---

#### 2.2 Audit Logging & Event Tracking

**Current State:**
- OpenTelemetry traces for performance
- No structured audit logs for security events (auth, policy decisions, data changes)

**CRA Requirement:**
- Log security-relevant events (login, authorization decisions, data modifications)
- Ensure logs are tamper-proof and retained
- Include user identity, timestamp, action, result, IP address

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **2.2.1** Implement structured audit logging | backend/fastapi/app/audit.py (auth, policy, CRUD events) | Backend | 2 days | Not Started |
| **2.2.2** Add audit log endpoints | GET /audit-logs (with filtering, pagination) | Backend | 1 day | Not Started |
| **2.2.3** Configure log retention & rotation | Docker volume or cloud storage; 90-day retention | DevOps | 1 day | Not Started |
| **2.2.4** Create audit log viewer/dashboard | Frontend audit log panel or export | Frontend | 2 days | Not Started |

**Example Audit Log Events:**
```python
{
  "timestamp": "2026-08-18T10:30:00Z",
  "event_type": "auth.login_success",
  "user_id": "user123",
  "ip_address": "192.0.2.1",
  "user_agent": "Mozilla/5.0...",
  "result": "success"
}

{
  "timestamp": "2026-08-18T10:31:00Z",
  "event_type": "authorization.policy_check",
  "user_id": "user123",
  "resource": "app:my-app",
  "action": "scale",
  "result": "denied",
  "reason": "no_permission"
}

{
  "timestamp": "2026-08-18T10:32:00Z",
  "event_type": "data.app_created",
  "user_id": "user123",
  "app_id": "app456",
  "changes": {"name": "new-app", "replicas": 3}
}
```

**Success Criteria:**
- [ ] All auth, authorization, and data-change events logged
- [ ] Logs include user, timestamp, action, result, and IP
- [ ] Logs retained for ≥90 days
- [ ] Logs exportable and searchable

---

#### 2.3 Secrets Management & Rotation

**Current State:**
- Hardcoded credentials in docker-compose.yml (Keycloak admin/admin)
- No secrets rotation policy

**CRA Requirement:**
- Use secure secrets storage (not hardcoded)
- Implement secrets rotation procedure
- Minimize secrets exposure in logs and version control

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **2.3.1** Remove hardcoded secrets from repo | Update docker-compose.yml, .env.example | DevOps | 0.5 day | Not Started |
| **2.3.2** Document secrets management | docs/SECRETS_MANAGEMENT.md (local dev, production) | DevOps | 1 day | Not Started |
| **2.3.3** Add secrets scanning to CI/CD | .github/workflows/secrets.yml (detect-secrets or Truffleloaf) | Security | 0.5 day | Not Started |
| **2.3.4** Create secrets rotation runbook | docs/SECRETS_ROTATION.md (Keycloak, DB, API keys) | DevOps | 1 day | Not Started |

**Success Criteria:**
- [ ] No hardcoded secrets in version control
- [ ] Secrets scanning enabled in CI/CD
- [ ] .env.example file documents required secrets
- [ ] Rotation procedure documented and tested

---

#### 2.4 Access Control & Least Privilege

**Current State:**
- Role-based access control (RBAC) via Keycloak
- Fine-grained authorization via OpenFGA
- No documented principle of least privilege

**CRA Requirement:**
- Document access control model
- Implement least privilege principle
- Log all access decisions
- Review and update permissions regularly

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **2.4.1** Document RBAC & authorization model | docs/ACCESS_CONTROL.md (roles, permissions, policies) | Security | 2 days | Not Started |
| **2.4.2** Implement least privilege defaults | Review Keycloak/OpenFGA roles; restrict by default | Security | 1 day | Not Started |
| **2.4.3** Add access review workflow | Periodic role/permission audit (quarterly) | Security | 0.5 day | Not Started |
| **2.4.4** Create access provisioning checklist | docs/PROVISIONING.md (onboarding, offboarding) | Security | 1 day | Not Started |

**Success Criteria:**
- [ ] Access control model documented
- [ ] Least privilege principle applied to all roles
- [ ] Quarterly access review process documented
- [ ] Audit logs show access decisions

---

### Phase 3: Continuous Improvement & Operations (Weeks 11+) – Monitoring & Maturity

#### 3.1 Security Monitoring & Alerting

**Current State:**
- OpenTelemetry tracing for observability
- No alerting for security events (repeated auth failures, policy violations)

**CRA Requirement:**
- Monitor for and alert on suspicious activities
- Detect and respond to security events
- Track security metrics and KPIs

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **3.1.1** Add security event detection | Grafana/Prometheus alerts for auth failures, policy denials | DevOps | 2 days | Not Started |
| **3.1.2** Create security dashboard | Real-time view of auth events, access patterns, vulnerabilities | DevOps | 2 days | Not Started |
| **3.1.3** Document alerting thresholds | docs/ALERTING.md (trigger conditions, escalation) | DevOps | 1 day | Not Started |
| **3.1.4** Set up incident notifications | Slack, email, or on-call alerts for critical events | DevOps | 1 day | Not Started |

**Success Criteria:**
- [ ] Alerts configured for high-priority security events
- [ ] Dashboard shows security metrics in real-time
- [ ] Alert thresholds documented and tested

---

#### 3.2 Patch Management & Dependency Updates

**Current State:**
- Manual dependency updates
- No automated patch testing or staged rollouts

**CRA Requirement:**
- Regularly assess and apply security patches
- Test patches before production deployment
- Communicate patch availability to users

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **3.2.1** Automate dependency updates (Dependabot) | .github/dependabot.yml for Python & npm | DevOps | 0.5 day | Not Started |
| **3.2.2** Create patch testing workflow | .github/workflows/patch-test.yml (apply patches, run tests) | QA | 1 day | Not Started |
| **3.2.3** Document patch release process | docs/PATCH_RELEASE.md (testing, staging, production) | DevOps | 1 day | Not Started |
| **3.2.4** Create security advisory template | .github/SECURITY_ADVISORY.md for releases | Security | 0.5 day | Not Started |

**Success Criteria:**
- [ ] Dependabot enabled for automated PRs
- [ ] Security patches applied within 30 days of release
- [ ] Patch notes published in GitHub releases
- [ ] Users can subscribe to security advisories

---

#### 3.3 Compliance Audits & Attestation

**Current State:**
- No third-party security audits or certifications

**CRA Requirement:**
- Support third-party security audits
- Maintain compliance documentation
- Provide attestations of security controls

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **3.3.1** Prepare audit documentation | docs/AUDIT_PREP.md (controls, evidence, evidence locations) | Security | 2 days | Not Started |
| **3.3.2** Create compliance matrix | docs/COMPLIANCE_MATRIX.md (CRA requirements → controls) | Security | 1 day | Not Started |
| **3.3.3** Schedule security audit | Engage third-party auditor (external security firm) | Security | Ongoing | Not Started |
| **3.3.4** Create attestation statement | docs/SECURITY_ATTESTATION.md (sign-off on controls) | Leadership | 0.5 day | Not Started |

**Success Criteria:**
- [ ] Compliance matrix created and maintained
- [ ] Third-party audit scheduled (annual)
- [ ] Audit findings tracked and remediated
- [ ] Attestation published

---

#### 3.4 Supply Chain Security

**Current State:**
- Build artifacts (Docker images) not signed
- No provenance tracking

**CRA Requirement:**
- Verify integrity of build artifacts
- Track dependency provenance
- Implement secure supply chain practices

**Implementation Tasks:**

| Task | Deliverable | Owner | Effort | Status |
|---|---|---|---|---|
| **3.4.1** Implement container image signing | Sign Docker images with cosign on release | DevOps | 1 day | Not Started |
| **3.4.2** Add provenance attestation | Generate SLSA provenance; publish with image | DevOps | 1 day | Not Started |
| **3.4.3** Verify image signatures at deployment | Include signature verification in deployment | DevOps | 1 day | Not Started |
| **3.4.4** Document supply chain process | docs/SUPPLY_CHAIN_SECURITY.md (build, sign, verify) | DevOps | 1 day | Not Started |

**Success Criteria:**
- [ ] Docker images signed and verifiable
- [ ] SLSA provenance generated for releases
- [ ] Deployment process verifies image signatures
- [ ] Supply chain documented and auditable

---

## Part C: Phased Rollout & Timeline

### Phase 1 Timeline (Weeks 1–6) — Estimated Effort: 20 days

**Priority:** P1 (blocking compliance)

| Week | Milestone | Deliverables |
|---|---|---|
| 1–2 | SSDLC & Threat Model | docs/SECURITY_REQUIREMENTS.md, docs/architecture/THREAT_MODEL.md, Secure Code Review Policy |
| 2–3 | Security Testing Infrastructure | pytest migration, SAST/dependency scanning, coverage tracking |
| 3–4 | SBOM & Dependency Locking | SBOM generation, lock files, CycloneDX artifacts |
| 4–6 | Vulnerability Management | Disclosure policy, security.txt, incident response plan, GitHub security advisories |

### Phase 2 Timeline (Weeks 7–10) — Estimated Effort: 15 days

**Priority:** P2 (governance & audit trails)

| Week | Milestone | Deliverables |
|---|---|---|
| 7–8 | Security Documentation | Threat model (detailed), data protection, hardening guide, known issues |
| 8–9 | Audit Logging | Structured audit logs, audit endpoints, retention policy, log viewer |
| 9 | Secrets Management | Remove hardcoded secrets, secrets scanning, rotation runbook |
| 10 | Access Control | Access control documentation, least privilege review, provisioning checklist |

### Phase 3 Timeline (Weeks 11+) — Estimated Effort: 10 days

**Priority:** P3 (continuous improvement)

| Milestone | Deliverables | Timeline |
|---|---|---|
| Security Monitoring | Alerting, security dashboard, incident notifications | Weeks 11–12 |
| Patch Management | Dependabot, patch testing, advisory process | Weeks 12–13 |
| Compliance Audit Prep | Audit documentation, compliance matrix | Weeks 13–14 |
| Supply Chain Security | Image signing, SLSA provenance, deployment verification | Weeks 14–15 |

**Total Estimated Effort:** ~45 development days over 15 weeks (phased implementation)

---

## Part D: Success Metrics & KPIs

### Security Quality Metrics

| Metric | Target | Current | Status |
|---|---|---|---|
| **Code Coverage** | ≥80% for critical paths | <30% | 🔴 To Do |
| **Vulnerability Count** | 0 High/Critical in dependencies | Unknown | 🔴 To Do |
| **Audit Log Completeness** | 100% of auth/authz/data events logged | 0% | 🔴 To Do |
| **SBOM Coverage** | 100% of dependencies included | 0% | 🔴 To Do |
| **SAST Issues Fixed** | 100% of High/Critical | N/A | 🔴 To Do |
| **Patch Time to Deploy** | ≤30 days for security patches | Untracked | 🔴 To Do |
| **Policy Review Frequency** | Quarterly access reviews | None | 🔴 To Do |

### Compliance Metrics

| Artifact | Status | Owner | Due |
|---|---|---|---|
| Security Requirements Document | Not Started | Architecture | Week 1 |
| Threat Model (STRIDE) | Not Started | Security | Week 3 |
| SBOM (CycloneDX) | Not Started | DevOps | Week 4 |
| Vulnerability Disclosure Policy | Not Started | Security | Week 4 |
| security.txt (RFC 9110) | Not Started | Security | Week 4 |
| Data Protection Policy | Not Started | Security/Privacy | Week 8 |
| Audit Logging System | Not Started | Backend | Week 9 |
| Access Control Documentation | Not Started | Security | Week 10 |
| Compliance Matrix (CRA) | Not Started | Security | Week 13 |

---

## Part E: Tools & Dependencies to Add

### Security Scanning

```bash
# Python static analysis & dependency scanning
pip install semgrep bandit pip-audit

# SBOM generation
pip install cyclonedx-bom

# Secrets detection
pip install detect-secrets
```

### CI/CD Workflow Additions

```yaml
# .github/workflows/sast.yml
- Static analysis (Semgrep, Bandit)
- Dependency scanning (pip-audit, npm audit)
- Secrets scanning (detect-secrets)
- Container image scanning (Trivy)

# .github/workflows/sbom.yml
- Generate SBOM on release
- Publish to GitHub Releases

# .github/workflows/release.yml
- Sign container images (cosign)
- Generate SLSA provenance
- Publish security advisories
```

### Documentation Files to Create

```
docs/
├── SECURITY.md (vulnerability disclosure)
├── SECURITY_REQUIREMENTS.md (SSDLC overview)
├── SECURE_CODING.md (guidelines)
├── architecture/THREAT_MODEL.md (STRIDE analysis)
├── DATA_PROTECTION.md (GDPR, encryption)
├── HARDENING.md (production deployment)
├── KNOWN_ISSUES.md (CVEs, workarounds)
├── API_SECURITY.md (auth, rate limiting)
├── AUDIT_LOGGING.md (audit log spec)
├── ACCESS_CONTROL.md (RBAC/FGA model)
├── SECRETS_MANAGEMENT.md (secrets handling)
├── PATCH_RELEASE.md (patch process)
├── SUPPLY_CHAIN_SECURITY.md (signing, provenance)
├── INCIDENT_RESPONSE.md (detection, escalation)
├── COMPLIANCE_MATRIX.md (CRA → controls)
└── SBOM.md (where to find, how to use)
```

### Code Changes Required

**Backend (FastAPI):**
- [ ] Audit logging module (app/audit.py)
- [ ] Audit log endpoints (GET /audit-logs with filtering)
- [ ] Input validation enhancements (env var parsing, SQL injection tests)
- [ ] Error handling improvements (no stack trace leaks)
- [ ] Non-root Docker user

**Frontend (Angular):**
- [ ] Audit log viewer component
- [ ] Security dashboard
- [ ] OWASP top 10 validation (CSP headers, XSS protection)

**Infrastructure:**
- [ ] Docker Compose: Remove hardcoded secrets, use .env
- [ ] GitHub Actions: Add SAST, dependency scanning, secrets detection, SBOM, signing
- [ ] Security logging (syslog, structured logs)
- [ ] Dependabot configuration

---

## Part F: References & Regulatory Framework

### EU Cyber Resilience Act (CRA)
- **Regulation (EU) 2024/2847**
- **Effective Date:** 12 September 2025 (security requirements phase)
- **Key Sections:**
  - Article 10: Secure software development
  - Article 11: Security testing
  - Article 12: Vulnerability management
  - Article 13: Incident response
  - Article 14: Documentation & transparency

### Related Standards
- **NIST Secure Software Development Framework (SSDF):** v1.1
- **SLSA Framework:** Software artifact provenance and integrity
- **CycloneDX / SPDX:** Software Bill of Materials formats
- **OWASP Top 10:** Web application security risks
- **OpenSSF Best Practices:** Badge criteria

### Compliance Checklists
- [OpenSSF Badge](https://bestpractices.coreinfrastructure.org/) — Passing badge recommended
- [NIST SSDF Practices](https://csrc.nist.gov/publications/detail/sp/800-218/final)
- [CRA Annex I Requirements](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) — Official regulation text

---

## Part G: Risk Mitigation & Dependencies

### Critical Path Items (Must Complete)
1. ✅ Phase 1 (Weeks 1–6) — SSDLC, security testing, SBOM, vulnerability management
2. ✅ Phase 2 Part 1 (Weeks 7–8) — Security documentation & threat model
3. ✅ Phase 2 Part 2 (Weeks 8–9) — Audit logging & secrets management

### Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Resource constraints | Delayed compliance | Prioritize Phase 1; defer Phase 3 (monitoring) |
| Lack of security expertise | Inadequate controls | Hire security consultant for threat modeling & audit |
| Third-party dependency vulnerabilities | Supply chain risk | Automate scanning; track and patch regularly |
| Audit logging performance | Production impact | Use async logging, separate log storage |
| Secrets exposure in logs | Data breach | Implement log filtering, sanitization; rotate immediately |

---

## Approval & Sign-Off

| Role | Name | Date | Status |
|---|---|---|---|
| **Security Lead** | TBD | — | 🔴 Pending |
| **Engineering Lead** | TBD | — | 🔴 Pending |
| **Product Owner** | TBD | — | 🔴 Pending |
| **Legal/Compliance** | TBD | — | 🔴 Pending |

---

## Next Steps

1. **Week 1 Kickoff:** Review this plan with stakeholders; assign owners
2. **Resource Allocation:** Allocate 2–3 engineers for Phase 1
3. **Tool Setup:** Install SAST, dependency scanning, SBOM tools
4. **Documentation:** Start with SECURITY_REQUIREMENTS.md and THREAT_MODEL.md
5. **Automation:** Configure GitHub Actions workflows for continuous scanning
6. **Review Cycle:** Bi-weekly sync on progress; adjust timeline as needed

---

**Document Version:** 1.0 (Initial Assessment)  
**Last Reviewed:** 2026-08-18  
**Next Review:** Weekly during Phase 1 implementation
