---
title: Vulnerable & Outdated Libraries
id: SCWE-089
alias: vulnerable-outdated-libraries
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [1104]
status: new
---

## Relationships
- CWE-1104: Use of Unmaintained Third Party Components  
  [CWE-1104 Link](https://cwe.mitre.org/data/definitions/1104.html)

## Description  
Smart contracts that depend on outdated or vulnerable third‑party libraries inherit their security flaws. Attackers can exploit known issues in widely used libraries (e.g., reentrancy, integer overflow, or access control bypasses), especially if the library is no longer maintained or patched.  
Common risks include:  
- Exploitation of known vulnerabilities in older OpenZeppelin versions or other dependencies.  
- Inheriting insecure logic or deprecated patterns from unmaintained libraries.  
- Increased attack surface due to indirect dependencies.  

## Remediation  
- **Version pinning:** Always specify exact, up‑to‑date versions of dependencies in `package.json`, `foundry.toml`, or `hardhat.config.js`.  
- **Regular audits:** Periodically review library versions for known vulnerabilities and upgrade accordingly.  
- **Vendor management:** Rely on reputable, actively maintained libraries (e.g., OpenZeppelin). Avoid custom forks unless fully audited.  
- **Automated scanning:** Use dependency scanners (e.g., `npm audit`, `snyk`, `slither-check-oz`) to detect outdated or vulnerable libraries.  

## Examples  
- **Outdated Dependency Example (`package.json`)**  
    ```json
    {
      "dependencies": {
        "@openzeppelin/contracts": "^2.3.0",
        "truffle": "^5.0.0"
      },
      "notes": "Insecure: OpenZeppelin v2.3.0 contains outdated ERC777 and SafeMath implementations."
    }
    ```

- **Updated Dependency Example (`package.json`)**  
    ```json
    {
      "dependencies": {
        "@openzeppelin/contracts": "^5.0.0",
        "hardhat": "^2.22.0"
      },
      "notes": "Secure: Latest OpenZeppelin release with modern ERC20, patched ERC777, and Solidity 0.8+ overflow checks."
    }
    ```
