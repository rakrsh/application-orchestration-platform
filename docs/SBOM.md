# Software Bill of Materials (SBOM)

## Overview
As part of our commitment to the EU Cyber Resilience Act (CRA) and supply chain security, the Application Orchestration Platform generates a Software Bill of Materials (SBOM) for every release.

## Format
The SBOMs are generated in the standard **CycloneDX** JSON format.

## Availability
- **Releases:** The SBOM for each version is attached as a build artifact to the corresponding GitHub Release.
- **Python Backend:** Included as `sbom-python.json`.
- **Node.js Frontend:** (Future Phase) Will be included as `sbom-node.json`.

## Usage
Users and auditors can consume the SBOM using any CycloneDX compatible tool to verify the provenance and security posture of our dependencies.
