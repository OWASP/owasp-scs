---
title: Alternate Top 15 — Web3 Attack Vectors (Beyond Smart Contracts)
hide:
  - toc
---

# Alternate Top 15: Web3 Attack Vectors (Beyond Smart Contracts)

This list **complements** the **OWASP Smart Contract Top 10 : 2026** by cataloguing significant **non-smart-contract** attack vectors in the Web3 space. These threats target infrastructure, custody, social layers, and operational security rather than on-chain logic.

> **Scope & Purpose:** This is an **awareness list** for protocols, Web3 users, stakeholders, and the CXO suite to look out for. It is **not ranked** by losses, frequency, or any statistics—ordering does not imply relative severity or prevalence. Use it alongside the OWASP Smart Contract Top 10 for a broader view of Web3 security risks.


??? info "Future Development"
    This list will be **developed**, **ranked**, and **maintained** in the near future. Methodology, data sources, and update cycles will be established as the OWASP Smart Contract Top 10 project evolves. Stakeholder feedback and incident data will inform future iterations.



![OWASP Web3 Alternate Top 15 — List View](../assets/waTop15List.png)


## WA01 — Multisig Hijacking

**Description:** Attackers manipulate the signing interface or approval flow so that signers approve transactions without clearly seeing what they authorise. Blind signing, UI spoofing, and malicious JavaScript injected into wallet frontends allow attackers to trick multisig operators into executing delegatecalls or upgrades that hand over control.

**2025 Example:** Malicious code was injected into Safe{Wallet}'s signing interface (app.safe.global), attributed to a [breached Safe{Wallet} developer machine](https://www.bleepingcomputer.com/news/security/lazarus-hacked-bybit-via-a-breached-safe-wallet-developer-machine/). Signers saw one transaction but executed another—a delegatecall to an attacker-controlled contract. Hardware wallets typically lack the ability to parse complex Safe transactions, enabling blind signing. Similar techniques target DAO treasuries and custody setups.

**Case Study: Bybit $1.5B — Largest Crypto Heist in History (Feb 2025)**  

The Bybit hack remains the **largest crypto heist by amount stolen in 2025** and in recorded history (~$1.5B, ~401,000 ETH). The [FBI](https://www.bleepingcomputer.com/news/security/fbi-confirms-lazarus-hackers-were-behind-15b-bybit-crypto-heist/) attributes operation "TraderTraitor" to North Korea's Lazarus group. Bybit used Safe{Wallet} for its Ethereum multisig cold wallet. Attackers compromised Safe{Wallet}'s developer infrastructure (via a breached developer machine; AWS S3/CloudFront credentials likely exposed) and injected malicious JavaScript into app.safe.global. When Bybit's signers approved a cold-to-warm transfer, the compromised UI presented a legitimate-looking transaction but executed a delegatecall to an attacker-controlled contract instead. Funds were drained; at least $300M had been laundered by March 2025. Third-party audits (Sygnia, Verichains) confirmed the root cause was malicious code from Safe{Wallet}'s infrastructure—not Bybit's own systems. This incident illustrates how multisig hijacking can target high-value CEX custody; see also [WA07](#wa07--centralised-exchange--web225-infrastructure-breaches).

**References:**

- [BlockSec — Bybit $1.5B Hack: In-Depth Analysis of the Malicious Safe Wallet Upgrade Attack](https://blocksecteam.medium.com/bybit-1-5b-hack-in-depth-analysis-of-the-malicious-safe-wallet-upgrade-attack-2b82e37d4d28)
- [BleepingComputer — Lazarus hacked Bybit via breached Safe{Wallet} developer machine](https://www.bleepingcomputer.com/news/security/lazarus-hacked-bybit-via-a-breached-safe-wallet-developer-machine/)
- [Trail of Bits — Maturing your smart contracts beyond private key risk](https://blog.trailofbits.com/2025/06/25/maturing-your-smart-contracts-beyond-private-key-risk/) (Radiant, WazirX, Bybit case studies)

**Key lessons:** Never trust signing UIs blindly; verify transaction calldata independently; use hardware signing with display verification; audit frontend and CDN integrity.

---

## WA02 — Supply Chain Attacks (npm, PyPI, OSS)

**Description:** Attackers compromise open-source package registries (npm, PyPI) to distribute crypto-draining malware, credential stealers, clipboard hijackers, or cryptominers. Malicious code executes in the same context as browser wallets or CI pipelines, enabling theft of keys, keystores, and on-chain authorisations.

**Examples:** (1) **Sept 2025 — chalk/npm:** A [phishing campaign](https://www.sygnia.co/threat-reports-and-advisories/npm-supply-chain-attack-september-2025/) (npmjs[.]help) targeting the `chalk` maintainer led to malware in 18 packages (>2B weekly downloads). The payload hooked `fetch`, `XMLHttpRequest`, and `window.ethereum` to intercept wallet transactions across multiple chains. (2) **Dec 2023 — Ledger Connect Kit:** [Compromised npm package](https://socket.dev/blog/ledger-connect-kit-supply-chain-attack-wallet-drainer) (versions 1.1.5–1.1.7) injected wallet-draining code; a phished former Ledger employee's npm access was the initial vector. Affected 100+ dApps including SushiSwap, Revoke.cash; ~$600K lost. Approximately [75% of blockchain-related malicious packages](https://socket.dev/blog/2025-blockchain-and-cryptocurrency-threat-report) tracked by Socket in 2025 were on npm.

**References:**

- [Sygnia — 16 Minutes to Impact: npm Supply Chain Abuse Deploys crypto-draining malware](https://www.sygnia.co/threat-reports-and-advisories/npm-supply-chain-attack-september-2025/)
- [Socket.dev — Ledger Connect Kit Supply Chain Attack](https://socket.dev/blog/ledger-connect-kit-supply-chain-attack-wallet-drainer)
- [Socket.dev — 2025 Blockchain and Cryptocurrency Threat Report](https://socket.dev/blog/2025-blockchain-and-cryptocurrency-threat-report)

**Key lessons:** Lock dependencies; use lockfiles and reproducible builds; verify package integrity; monitor for typosquatting and dependency confusion.

---

## WA03 — Private Key Compromise (PKC)

**Description:** Private keys or seed phrases are stolen or leaked through phishing, malware, weak entropy, ECDSA nonce reuse, or implementation bugs. [Chainalysis reports](https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2025) that PKC was responsible for **43.8%** of funds stolen via hacks in 2024—more than any other single vector. [CertiK](https://www.certik.com/resources/blog/private-key-compromises) documented ~$239M in PKC losses in 2024 (1,160% YoY increase).

**2024 Examples:** [Ripple co-founder Chris Larsen](https://www.certik.com/resources/blog/private-key-compromises) lost ~$112M (Jan 2024) after private keys were compromised. PlayDapp (~$32.3M), FixedFloat (~$26M), and nine incidents in March 2024 alone (>$22M combined) further illustrate the scale.

**References:**

- [Chainalysis — Crypto Hacking and Stolen Funds 2025](https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2025)
- [CertiK — Major Private Key Compromises](https://www.certik.com/resources/blog/private-key-compromises)
- [Trail of Bits — Maturing your smart contracts beyond private key risk](https://blog.trailofbits.com/2025/06/25/maturing-your-smart-contracts-beyond-private-key-risk/)

**Key lessons:** Use HSMs and secure key storage; avoid key reuse; implement MPC or multisig for high-value ops; rotate keys; audit cryptographic implementations.

---

## WA04 — Drainer Malware & Drainer-as-a-Service (DaaS)

**Description:** Crypto drainers are *toolkits or services* that deploy phishing sites and fake dApps to trick users into granting malicious contracts permission to transfer assets (`approve`, `setApprovalForAll`, `permit`). No private key theft required—social engineering plus on-chain permission abuse. Distinct from general approval phishing (WA06): drainers are packaged, sold as kits or DaaS subscriptions ($500–$10K) on Telegram and darknet forums.

**2025 Stats:** [Scam Sniffer's 2024 report](https://drops.scamsniffer.io/scam-sniffer-2024-web3-phishing-attacks-wallet-drainers-drain-494-million/) states wallet drainers stole **$494 million** (67% YoY increase), affecting 332,000+ wallet addresses. Largest single theft: $55.4 million; 30 incidents exceeded $1M each. [Research using SilentPush](https://decodecybercrime.com/crypto-drainers-of-2025-the-rising-web-of-wallet-theft/) identified 122 drainer domains Jan–Jul 2025, 54 active. Notable kits: Inferno ($81M), MS Drainer ($59M), Venom ($27M). Targets: MetaMask, Phantom, Solflare, WalletConnect, Ledger, Coinbase Wallet.

**References:**

- [Scam Sniffer — 2024 Web3 Phishing Attacks & Wallet Drainers](https://drops.scamsniffer.io/scam-sniffer-2024-web3-phishing-attacks-wallet-drainers-drain-494-million/)
- [BleepingComputer — Cryptocurrency wallet drainers stole $494 million in 2024](https://www.bleepingcomputer.com/news/security/cryptocurrency-wallet-drainers-stole-494-million-in-2024/)
- [Decode Cybercrime — Crypto Drainers of 2025: The Rising Web of Wallet Theft](https://decodecybercrime.com/crypto-drainers-of-2025-the-rising-web-of-wallet-theft/)

**Key lessons:** Scrutinise all approval requests; avoid unlimited approvals; use revoke.cash–style tools; blocklist known drainer domains and contracts.

---

## WA05 — Fake Interview & Video Call Social Engineering

**Description:** Attackers pose as employers or journalists, invite targets to fake interviews (Zoom, custom meeting apps), and abuse remote-control features to install malware or gain system access. Once in control, they steal wallets, credentials, and initiate unauthorised crypto transactions.

**2025 Examples:**
- **GrassCall:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/grasscall-malware-campaign-drains-crypto-wallets-via-fake-job-interviews/) reports Russian-speaking group "Crazy Evil" posted fake jobs for "ChainSeeker.io" on CryptoJobsList and WellFound. Applicants downloaded malicious "GrassCall" meeting software that installed info-stealing malware (Rhadamanthys on Windows, AMOS Stealer on macOS); hundreds reported drained wallets. Recorded Future attributes $5M+ stolen through similar scams since 2021.
- **ELUSIVE COMET:** [Trail of Bits](https://blog.trailofbits.com/2025/04/17/mitigating-elusive-comet-zoom-remote-control-attacks/) and [Malwarebytes](https://www.malwarebytes.com/blog/news/2025/04/zoom-attack-tricks-victims-into-allowing-remote-access-to-install-malware-and-steal-money) document fake "Bloomberg Crypto" interviews via X and Calendly (bloombergconferences@gmail.com). Attackers used Zoom's remote control feature, renaming themselves to "Zoom" so the permission prompt appeared legitimate, granting full system access for malware deployment and credential theft.

**References:**

- [BleepingComputer — GrassCall malware campaign drains crypto wallets via fake job interviews](https://www.bleepingcomputer.com/news/security/grasscall-malware-campaign-drains-crypto-wallets-via-fake-job-interviews/)
- [Trail of Bits — Mitigating ELUSIVE COMET Zoom remote control attacks](https://blog.trailofbits.com/2025/04/17/mitigating-elusive-comet-zoom-remote-control-attacks/)
- [Malwarebytes — Zoom attack tricks victims into allowing remote access](https://www.malwarebytes.com/blog/news/2025/04/zoom-attack-tricks-victims-into-allowing-remote-access-to-install-malware-and-steal-money)
- [SEAL — Advisory on ELUSIVE COMET](https://www.securityalliance.org/news/2025-03-elusive-comet)

**Key lessons:** Verify interviewer identity through official channels; avoid downloading custom meeting software; treat remote-control requests with extreme suspicion.

---

## WA06 — UI/UX Spoofing & Approval Phishing

**Description:** Attackers create spoofed or cloned sites (e.g., OpenSea, Uniswap) or misleading prompts that trick users into signing transactions granting malicious contracts spending authority (`approve`, `setApprovalForAll`, `permit`, or Permit2). Users believe they are claiming an airdrop, minting an NFT, or swapping—they instead grant unlimited token/NFT transfer rights. [Chainalysis](https://www.chainalysis.com/blog/approval-phishing-cryptocurrency-scams-2023/) estimated at least $374M stolen via approval phishing in 2023. Emerging vector: [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) `SetCode` delegation scams, where users are tricked into "upgrading" their wallet but grant full control to a malicious contract.

**References:**

- [Chainalysis — Approval Phishing Scams 2023](https://www.chainalysis.com/blog/approval-phishing-cryptocurrency-scams-2023/)
- [Security Alliance — Using EIP-7702 (Wallet Security)](https://frameworks.securityalliance.org/wallet-security/verifying-7702/)
- [Gate.io — Permit, Uniswap Permit2, and Signature Phishing](https://www.gate.io/learn/articles/is-your-wallet-safe-how-hackers-exploit-permit-uniswap-permit2-and-signatures-for-phishing/4197)
- [MetaMask — Signature Phishing](https://support.metamask.io/privacy-and-security/staying-safe-in-web3/signature-phishing/)

**Key lessons:** Verify URLs; use bookmark preferred sites; avoid unlimited approvals; carefully review signing content; watch for high-risk signature popups.

---

## WA07 — Centralised Exchange & Web2/2.5 Infrastructure Breaches

**Description:** Custody, exchange infrastructure, and operational security failures—not smart contract bugs—cause the largest single losses. Cold/warm wallet procedures, internal tooling, and human error are exploited. Web2.5 (hybrid centralised–decentralised) systems inherit both on-chain and off-chain risks.

**2025 Example:** **Bybit $1.5B** (February 2025)—[largest crypto heist in history](https://www.bbc.com/news/articles/c2kgndwwd7lo). [FBI attributes](https://www.bleepingcomputer.com/news/security/fbi-confirms-lazarus-hackers-were-behind-15b-bybit-crypto-heist/) the operation "TraderTraitor" to North Korean Lazarus group. Attackers compromised Safe{Wallet} infrastructure (via breached developer machine) and injected malicious code into app.safe.global; Bybit signers using Safe unknowingly approved a wallet upgrade transaction. ~401,000 ETH stolen; funds drained within 13 blocks. At least $300M had been laundered by March 2025. [IC3 PSA 2025](https://ic3.gov/psa/2025/psa250226).

**References:**

- [BBC — North Korean hackers cash out hundreds of millions from $1.5bn ByBit hack](https://www.bbc.com/news/articles/c2kgndwwd7lo)
- [BleepingComputer — FBI confirms Lazarus hackers were behind $1.5B Bybit crypto heist](https://www.bleepingcomputer.com/news/security/fbi-confirms-lazarus-hackers-were-behind-15b-bybit-crypto-heist/)
- [IC3 — North Korea Responsible for $1.5 Billion Bybit Hack](https://ic3.gov/psa/2025/psa250226)
- [BlockSec — Bybit $1.5B Hack: In-Depth Analysis](https://blocksecteam.medium.com/bybit-1-5b-hack-in-depth-analysis-of-the-malicious-safe-wallet-upgrade-attack-2b82e37d4d28)

**Key lessons:** Segregate custody; use specialised security tooling; enforce M-of-N signing with independent verification; audit infra and processes.

---

## WA08 — Phishing & General Social Engineering

**Description:** Phishing emails, fake support sites, and impersonation trick users into revealing seed phrases, recovery phrases, or passwords. Unlike approval phishing (WA06) or drainer sites (WA04), these attacks aim to steal credentials directly—once obtained, attackers have full control. AI has increased scale and sophistication in 2024–2025.

**2024 Example:** [Fake Ledger data-breach emails](https://www.bleepingcomputer.com/news/security/new-fake-ledger-data-breach-emails-try-to-steal-crypto-wallets/) (Dec 2024) impersonating "support@ledger.com" claimed recovery phrases were exposed and directed users to a fake Ledger site to "verify" their 24-word phrase. Credential phishing targets seed phrases, not on-chain approvals.

**References:**

- [BleepingComputer — Fake Ledger data breach emails try to steal crypto wallets](https://www.bleepingcomputer.com/news/security/new-fake-ledger-data-breach-emails-try-to-steal-crypto-wallets/)
- [Elliptic — The State of Crypto Scams 2025](https://www.elliptic.co/blog/the-state-of-crypto-scams-2025-keeping-our-industry-safe-with-blockchain-analytics)
- [Ledger Support — Beware of phishing attempts](https://support.ledger.com/hc/en-us/articles/360035343054-Beware-of-phishing-attempts)

**Key lessons:** Never share seed phrases or private keys; Ledger/support will never ask for recovery phrases; verify official channels; use hardware wallets; enable 2FA; avoid clicking links in unsolicited messages.

---

## WA09 — Romance, Investment, Impersonation, Recovery & Pig Butchering Scams

**Description:** Social-engineering scams that exploit trust, urgency, or authority to trick victims into sending crypto. Multiple techniques overlap:

- **Romance & pig butchering:** Long-term romance or friendship scams where attackers build trust over weeks or months, then direct victims to fake investment platforms. A [February 2024 study](https://time.com/6836703/pig-butchering-scam-victim-loss-money-study-crypto/) (Griffin & Mei, University of Texas) estimated **more than $75 billion** stolen worldwide (Jan 2020–Feb 2024). Often involves call centers and [human trafficking victims](https://www.reuters.com/investigates/special-report/fintech-crypto-fraud-thailand/) forced to operate scams. [Chainalysis](https://www.chainalysis.com/blog/2024-pig-butchering-scam-revenue-grows-yoy/) reports pig butchering accounted for 33.2% of crypto scam revenue in 2024, ~40% YoY growth.
- **Investment scams:** Fake trading platforms, Ponzi schemes, and “guaranteed returns” that lure victims to deposit crypto. Investment fraud accounted for ~71% of crypto-related losses in 2023 per some estimates.
- **Impersonation scams:** Fraudsters pose as exchange support, government officials, influencers, or law enforcement. [FBI warnings](https://www.ic3.gov/PSA/2024/PSA240801) cite exchange impersonators requesting credentials via unsolicited calls; fake law firms and government impersonators pressure victims to pay “fees” or “back taxes.”
- **Recovery scams:** Scammers target victims who were already drained, posing as law firms or “recovery services” to extract more. [IC3](https://www.ic3.gov/PSA/2024/PSA240624) reported recovery scams exceeding $9.9M (Feb 2023–Feb 2024).
- **Giveaway scams:** “Send 1 ETH, get 2 back”–style offers via spoofed influencer accounts or livestreams.

**References:**

- [TIME — Pig-Butchering Scam $75 Billion](https://time.com/6836703/pig-butchering-scam-victim-loss-money-study-crypto/)
- [Chainalysis — Pig Butchering Scam Revenue 2024](https://www.chainalysis.com/blog/2024-pig-butchering-scam-revenue-grows-yoy/)
- [IC3 — Fictitious Law Firms Targeting Crypto Scam Victims](https://www.ic3.gov/PSA/2024/PSA240624)
- [IC3 — Scammers Impersonating Cryptocurrency Exchanges](https://www.ic3.gov/PSA/2024/PSA240801)
- [Elliptic — The State of Crypto Scams 2025](https://www.elliptic.co/blog/the-state-of-crypto-scams-2025-keeping-our-industry-safe-with-blockchain-analytics)

**Key lessons:** Be wary of unsolicited investment advice; avoid sending crypto to unknown platforms; never pay upfront “recovery” fees; verify identity through official channels (call back via published numbers); ignore giveaway offers from social media or livestreams.

---

## WA10 — Rug Pulls, Fake Airdrops & Token Impersonation

**Description:** Fraudulent token launches, fake airdrops, and token impersonation (same name/logo as legitimate projects) lure users into buying or claiming. Rug pulls remove liquidity or dump; fake airdrop claim pages often drain via malicious approvals (overlaps with WA04/WA06). Token impersonators create fake versions of trending or legitimate tokens.

**2023-2024 Examples:** [Omni Network](https://cointelegraph.com/news/omni-token-dumps-after-airdrop-as-scammers-rug-fake-token) (Apr 2024)—legitimate OMNI airdrop coincided with scammers launching a fake OMNI token that rugged 100%. [Blockfence research](https://blockfence.io/security/32m-stolen-over-1300-fake-tokens-rugged/) identified 1,300+ fake token rug pulls on Ethereum stealing >$32M from ~42,000 victims, impersonating projects (e.g., Blockfence, Wisealth) and memecoins (Pepe variants).

**References:**

- [CoinTelegraph — Omni token dumps after airdrop as scammers rug fake token](https://cointelegraph.com/news/omni-token-dumps-after-airdrop-as-scammers-rug-fake-token)
- [Blockfence — $32M Stolen: Over 1,300 Fake Tokens Rugged](https://blockfence.io/security/32m-stolen-over-1300-fake-tokens-rugged/)
- [MetaMask — Rug pulls and airdrop scams](https://support.metamask.io/privacy-and-security/staying-safe-in-web3/scammers-and-phishers-rugpulls-and-airdrop-scams/)

**Key lessons:** Verify contract addresses and official links; avoid FOMO-driven connects; use blocklists for known scam tokens and domains.

---

## WA11 — Wrench Attacks & Physical Coercion

**Description:** Attackers bypass technical controls entirely by threatening, kidnapping, or physically coercing key individuals (founders, operators, whales) to authorise transfers, reveal seed phrases, or sign governance actions. Traditional “$5 wrench attacks” have Web3-specific variants, including in-person extortion and forced travel to jurisdictions with weaker protections.

**2020–2024 Examples:** Academic research from UCL’s AFT 2024 paper “Investigating Wrench Attacks” catalogues dozens of physical attacks against cryptocurrency holders, including home invasions, kidnappings, and extortion cases across Europe and Asia, many of which remain under-reported. AP reporting and industry commentary highlight Ledger co-founder kidnapping attempts and rising “wrench attack” risk during bull markets.

**References:**

- [UCL / AFT 2024 — Investigating Wrench Attacks: Physical Attacks Targeting Cryptocurrency Users](https://discovery.ucl.ac.uk/id/eprint/10195033/1/wrench_attack-3.pdf)
- [AP News — Why ‘wrench attacks’ on wealthy crypto holders are on the rise](https://apnews.com/article/crypto-bitcoin-kidnapping-wrench-attack-ddc7263c25ba590f85648e1682576971)
- [Cointelegraph — Can panic wallets stop a wrench?](https://cointelegraph.com/news/panic-wallets-crypto-physical-security)

**Key lessons:** Treat high-value keys like physical cash; minimise human single points of failure; use time-locked withdrawals, duress-wallet patterns, spend limits, and geography-aware controls; train staff on physical security and incident response.

---

## WA12 — Insider Threats & Collusive Abuse

**Description:** Employees, contractors, or trusted partners abuse legitimate access to wallets, admin panels, RPC infrastructure, or deployment pipelines to steal funds or exfiltrate secrets. Collusion with external attackers can turn otherwise “secure” controls (multisig, approval workflows) into rubber stamps if signers or approvers are compromised or bribed.

**Examples:** An insider at Solana’s Cypher Protocol admitted to stealing ~$300K in 2024 by abusing privileged access to protocol keys and treasury flows. A former employee of New Zealand exchange Cryptopia kept customer data after being laid off and later stole ~NZD 245,000 in crypto from user accounts, demonstrating how departed staff can remain a live threat without rigorous offboarding.

**References:**

- [CoinDesk — Insider at Solana’s Cypher Protocol Admits to Stealing $300K](https://www.coindesk.com/business/2024/05/14/insider-at-solanas-cypher-protocol-admits-to-stealing-300k)
- [The Block — Ex-employee pleads guilty to stealing over $170,000 from Cryptopia](https://www.theblock.co/post/110495/ex-employee-pleads-guilty-to-stealing-over-170000-from-cryptopia)

**Key lessons:** Apply least-privilege and segregation of duties; require independent verification for large movements; log and monitor administrative actions; rotate roles and access; run background checks and enforce strong offboarding procedures.

---

## WA13 — DNS, Domain & Routing Infrastructure Hijacking

**Description:** Compromise of DNS providers, domain registrar accounts, BGP routes, or CDN configurations lets attackers silently redirect traffic from legitimate dApps, wallets, bridges, and exchanges to cloned phishing sites. Even technically sophisticated users can be tricked when real domains temporarily resolve to malicious infrastructure.

**Examples:** In 2022, attackers gained access to Namecheap DNS settings for DeFi projects including Convex, Ribbon, and DeFiSaver, injecting malicious code that prompted users for unlimited approvals and stole >$500K. In May 2024, Curve Finance reported repeated DNS hijacks of `curve.fi`, where users were redirected to wallet-draining phishing pages despite the underlying smart contracts remaining uncompromised.

**References:**

- [Revoke.cash — Namecheap DNS Hijack Exploit Breakdown](https://revoke.cash/es/exploits/namecheap?chainId=1)
- [Cointelegraph / TradingView — Curve Finance warns its DNS has been hijacked again](https://es.tradingview.com/news/cointelegraph:80ae03cf709cd:0/)

**Key lessons:** Lock registrar accounts (2FA, hardware keys, registry locks); monitor DNS and TLS certificate changes; use multi-region, multi-provider DNS; deploy phishing-resistant browser protections and content-security policies.

---

## WA14 — Wallet Software, Extension & App Compromises

**Description:** Exploiting bugs or supply-chain weaknesses in wallet desktop apps, mobile apps, and browser extensions enables attackers to bypass UI safeguards, inject malicious signing prompts, or silently approve transactions. Malicious updates, compromised signing keys, or 0-days in wallet code can instantly endanger all users who install the affected version.

**2025 Example:** In late 2025, attackers abused stolen Chrome Web Store API credentials from Trust Wallet’s infrastructure (“Shai-Hulud” supply-chain attack) to publish a malicious 2.68 version of the Trust Wallet browser extension, which exfiltrated seed phrases disguised as analytics traffic and drained an estimated $7–8.5M from thousands of users. Related campaigns in the same window compromised additional Chrome extensions, illustrating the systemic risk of extension-store access keys.

**References:**

- [Trust Wallet — Browser Extension v2.68 Incident: Community Update](https://trustwallet.com/blog/announcements/trust-wallet-browser-extension-v268-incident-community-update)
- [Rescana — Trust Wallet Chrome Extension Supply Chain Attack](https://www.rescana.com/post/trust-wallet-chrome-extension-supply-chain-attack-7-million-cryptocurrency-theft-via-compromised-v)
- [SecurityWeek — Several Chrome Extensions Compromised in Supply Chain Attack](https://www.securityweek.com/several-chrome-extensions-compromised-in-supply-chain-attack/)

**Key lessons:** Prefer audited, open-source wallets with secure release processes; verify app publishers; enable automatic revocation or rollback mechanisms; monitor wallet security advisories and rotate devices when compromise is suspected.

---

## WA15 — Nation-State Infiltration via Fake Hiring & Malicious OSS Contributions

**Description:** State-backed groups infiltrate crypto and Web3 ecosystems by posing as legitimate developers or employers, using fake job interviews, recruiter personas, and seemingly benign open source contributions or npm packages to compromise developer machines, CI pipelines, and production infrastructure. Once inside, they steal keys, cloud credentials, and source code, or poison software supply chains to facilitate large-scale exchange and protocol heists.

**2022–2025 Examples:** North Korea–linked Lazarus subgroup “TraderTraitor” has repeatedly targeted blockchain and crypto firms with fake hiring campaigns and DeFi-themed open source projects, seeding malicious npm packages that delivered infostealers (e.g., BeaverTail / InvisibleFerret) to developer laptops. U.S. DOJ actions in 2025 highlighted at least **136 victim companies** and **$2.2M+ in illicit wages** funneled to Pyongyang, with over **$15M in crypto seized** across related cases; among them, an Atlanta blockchain R&D company that unknowingly hired four DPRK developers who then stole **>$900K** in cryptocurrency. The same cluster of activity has been tied to multi-hundred-million-dollar thefts including the DMM Bitcoin hack (~$308M, May 2024) and the Bybit $1.5B incident, where compromised developer infrastructure and poisoned software supply chains played a central role.

**References:**

- [Wiz — TraderTraitor: Deep Dive into North Korea’s $1.5B Crypto Heists](https://wiz.io/blog/north-korean-tradertraitor-crypto-heist)
- [Stacklok — Dependency Hijacking: North Korea’s New Wave of DeFi-Themed Open Source Attacks](https://stacklok.com/blog/dependency-hijacking-dissecting-north-koreas-new-wave-of-defi-themed-open-source-attacks-targeting-developers)
- [lazarusholic — Inside the GitHub Infrastructure Powering North Korea’s “Contagious Interview” npm Attacks](https://lazarus.day/reports/post/inside-the-github-infrastructure-powering-north-koreas-contagious-interview-npm-attacks-mWBsT)
- [U.S. DOJ — Major Enforcement Actions Targeting North Korean Remote IT Worker Schemes](https://www.justice.gov/opa/pr/justice-department-announces-actions-disrupt-north-korean-it-worker-scheme)
- [Reuters — North Koreans Use Fake Names, Scripts to Land Remote IT Work](https://www.reuters.com/technology/north-koreans-use-fake-names-scripts-land-remote-it-work-cash-2023-11-21/)
- [CoinDesk — How North Korea Infiltrated the Crypto Industry](https://www.coindesk.com/policy/2022/04/29/how-north-korea-infiltrated-the-crypto-industry/)
- [Chainalysis / Google Threat Intelligence / Mandiant — DPRK IT Worker Schemes (joint reporting and advisories)](https://www.chainalysis.com/blog/north-korean-it-workers-crypto-sanctions-evasion/)

**Key lessons:** Treat unsolicited hiring outreach and “contribution offers” with suspicion; isolate development and CI environments; enforce strict review and provenance checks on new dependencies and OSS contributions; monitor for anomalous developer activity and outbound traffic; plan for nation-state–class adversaries in threat models for high-value protocols and exchanges.

---

## Summary Table

| ID   | Attack Vector                                  | Primary Target                | Example                                      |
|------|------------------------------------------------|-------------------------------|----------------------------------------------|
| WA01 | Multisig Hijacking                             | Custody, multisig operators   | Safe{Wallet} signing UI compromise            |
| WA02 | Supply Chain (npm, PyPI)                       | Developers, wallet users      | chalk/npm Sept 2025, Ledger Connect Kit 2023  |
| WA03 | Private Key Compromise                         | Key holders, infra            | Chris Larsen $112M, PlayDapp, FixedFloat      |
| WA04 | Drainer Malware / DaaS                         | End users, retail             | $494M (2024), Inferno $81M, MS Drainer $59M   |
| WA05 | Fake Interview / Video Call Social Eng.        | Job seekers, executives       | GrassCall, ELUSIVE COMET                      |
| WA06 | Deceptive dApp Interfaces & Approval Phishing  | End users                     | Spoofed OpenSea/Uniswap, Permit2, EIP-7702    |
| WA07 | CEX & Web2/2.5 Infrastructure                  | Exchanges, custodians         | Bybit $1.5B (largest heist)                   |
| WA08 |  Phishing & General Social Engineering      | Broad                         | Fake Ledger support emails (Dec 2024)         |
| WA09 | Romance, Investment, Impersonation, Recovery & Pig Butchering Scams | Retail, vulnerable users | Pig butchering ~$75B, recovery scams $9.9M+   |
| WA10 | Rug Pulls, Fake Airdrops & Token Impersonation | Retail, degens                | Omni fake token, 1,300 fake tokens $32M       |
| WA11 | Wrench Attacks & Physical Coercion             | Key individuals, executives   | Kidnapping, extortion for seed phrases        |
| WA12 | Insider Threats & Collusive Abuse              | Teams, custodians, DAOs       | Rogue employee drains treasury                 |
| WA13 | DNS, Domain & Routing Hijacking                | dApps, exchanges, wallets     | DNS hijack redirects to phishing frontends    |
| WA14 | Wallet Software & Extension Compromise         | Wallet users                  | Malicious wallet update injects drain prompts |
| WA15 | Nation-State Infiltration via Fake Hiring & Malicious OSS Contributions | Devs, infra, protocols | DPRK “TraderTraitor” fake hiring & npm attacks |
