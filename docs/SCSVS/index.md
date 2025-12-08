---
hide:
  - toc
search:
  exclude: true
---

# OWASP SCSVS

<img src="../assets/scsvs_cover.png" align="right" style="border-radius: 3px; margin: 3em; box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;" width="350px" >

<a href="https://github.com/OWASP/www-project-smart-contract-security-verification-standard/">:material-github: GitHub Repo</a>

<a href="https://owasp.org/www-project-smart-contract-security-verification-standard">:material-web: OWASP Project Page</a>

The **Smart Contract Security Verification Standard (SCSVS)** is a list of specific security requirements or tests for smart contracts, primarily written in Solidity and deployed on EVM-based blockchains. These requirements are intended to be used by architects, developers, testers, security professionals, tool vendors, and consumers to define, build, test, and verify secure smart contracts, decentralized applications (dApps) and blockchain protocols. The standard promotes best practices for ensuring the security and integrity of smart contracts and decentralized finance (DeFi) systems.

To complement the SCSVS, the OWASP SCS project also provides the [OWASP Smart Contract Security Testing Guide (SCSTG)](https://scs.owasp.org/SCSTG), the [OWASP Smart Contract Weakness Enumeration (SCWE)](https://scs.owasp.org/SCWE) and the [OWASP SCS Checklist](../checklists/index.md) which together are the perfect companion for verifying the controls listed in the OWASP SCSVS and demonstrate compliance.

<br>

<button class="scs-button" onclick="window.location.href='https://github.com/OWASP/www-project-smart-contract-security-verification-standard/releases/download/v0.0.1/OWASP_Smart_Contract_Security_Verification_Standard-0.0.1_en.pdf';"> Download the SCSVS</button>

<br>

## The SCSVS Control Groups

The standard is divided into various groups of controls, labeled **SCSVS-XXXXX**, that represent the most critical areas of the smart contract attack surface:

- **SCSVS-ARCH**: Secure architecture, design principles, and threat modeling practices for blockchain systems.  
- **SCSVS-CODE**: Policies and procedures for secure development, testing, and deployment of smart contracts.  
- **SCSVS-GOV**: Security of business logic and economic mechanisms to prevent manipulation or exploitation.  
- **SCSVS-AUTH**: Robust access control and authentication measures for blockchain-based applications.  
- **SCSVS-COMM**: Secure communication and interaction between contracts, users, and external systems.  
- **SCSVS-CRYPTO**: Best practices for cryptographic implementation in blockchain applications.  
- **SCSVS-ORACLE**: Ensures arithmetic and logical operations are safe and resistant to attacks.  
- **SCSVS-BLOCK**: Mitigation against denial of service (DoS) attacks and resource exhaustion risks.  
- **SCSVS-BRIDGE**: Efficient data and state management practices to maintain blockchain integrity.  
- **SCSVS-DEFI**: Optimization and monitoring of gas usage to avoid inefficiencies and constraints.  
- **SCSVS-COMP**: Component-specific security guidelines tailored to blockchain applications.  


!!! warning "SCS Testing Profiles"

    **The SCS project has traditionally provided three verification levels (L1, L2 and L3), which were revisited during the SCSVS refactoring in 2024, and have been reworked as ["SCS Testing Profiles"]().
    <br><br>
    While we move things around and as a temporary measure, the [OWASP SCS Checklist](../checklists/index.md) will still contain the verification levels, associated with the current SCSTG v0.0.1 tests.

<br><br>
