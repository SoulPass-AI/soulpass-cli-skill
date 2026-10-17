# SoulPass — Hardware-Secured Solana Trading Terminal for AI Agents

[![ClawHub](https://img.shields.io/badge/ClawHub-soulpass-blue)](https://clawhub.ai/skills/soulpass)
[![Solana](https://img.shields.io/badge/Solana-Mainnet-purple)](https://solana.com)

AI agent skill for **Solana trading, DeFi, and agent-to-agent infrastructure** with hardware-secured wallet. Built for Claude Code, Codex, Gemini CLI, and OpenClaw.

## What it does

### Trading & DeFi
- **Spot trading** — buy/sell any Solana token against USDC; routes (Jupiter, launchpad bonding curves) come from SoulPass's execution planner and every leg is checked on-device before signing
- **Meme coin trading** — pre-trade token risk checks (Jupiter verified flag, liquidity, mint/freeze authority; for launchpad coins LP lock, holder concentration, deployer and first buyers via `market launch`)
- **Copy trading** — follow a book from soulpass.ai; this device re-derives and verifies every rebalance before signing (Solana legs, each book under its own session)
- **DeFi yield** — earn interest on idle funds via Jupiter Lend (Solana) or Aave V3 (EVM)
- **Trading bots** — JSON-RPC daemon for low-latency automated strategies

### Agent Identity & Communication (ACE)
- **ACE identity** — a verifiable agent identity (`ace:sha256:…`) on the ACE relay, with an optional on-chain identity NFT (Metaplex Agent Registry, ERC-8004-format registration file)
- **Private agent-to-agent messaging** — post-quantum: every packet ML-DSA-signed and encrypted to the recipient's rotating X-Wing prekey, deliverable while the peer is offline; peers are admitted explicitly by the human
- **Service discovery** — find public agents by the profiles they support
- **Agent commerce** — sell services to other agents over ACE (Agent Commerce Engine, an open protocol); verify every payment on chain before delivering
- **Agent wallet** — the user's coding and personal agents can request payments; the user pairs them in SoulPass and confirms each payment on iPhone, and the agent gets a digest-bound payment receipt

SoulPass is an ordinary ACE agent: it has no built-in authority over other agents. Agents that want to message or request payments from SoulPass use the [ACE skill](https://github.com/aceprotocol/ace-skill).

### Security
- **Hardware-rooted keys** — the wallet's keys are generated in the Apple Secure Enclave and cannot be exported; chain keys derive from a hybrid post-quantum device root (P-256 ECDH ‖ ML-KEM-768); no seed phrase, no `.env` key file
- **Guardrails outside the prompt** — CLI spend policy (per-transaction caps, recipient allowlist) is enforced before signing; admission, payment authority and owner-key ceremonies are human-only

## Quick start

```bash
# Install
brew tap SoulPass-AI/soulpass && brew install soulpass

# Initialize wallet (brand-new account; if you already have one, run `soulpass link` instead)
soulpass init --new

# Start trading
soulpass spot --sell USDC --buy SOL --amount 100
```

## Why hardware security matters

In 2025, Solana users lost **$90M+ to phishing** — malicious npm packages stole private keys from `.env` files. SoulPass has no key file to steal: its root key is born in the Secure Enclave and cannot be exported.

| Approach | Security | Can run autonomously? |
|----------|----------|-----------------------|
| `.env` private key | None — plaintext | Yes |
| Browser wallet | Software encryption | No — human approves |
| MPC wallet | Provider holds shard | Yes — centralized trust |
| **SoulPass** | **Hardware-rooted key (Secure Enclave)** | **Yes — within a human-set spend policy** |

## Install as an agent skill

```bash
npx skills add SoulPass-AI/soulpass-cli-skill
```

Or clone https://github.com/SoulPass-AI/soulpass-cli-skill into your agent's skills directory (e.g. `~/.claude/skills/soulpass`).

## Links

- [SoulPass website](https://soulpass.ai)
- [ClawHub listing](https://clawhub.ai/skills/soulpass)
- [CLI releases](https://github.com/SoulPass-AI/soulpass)
- [ACE protocol](https://aceprotocol.org)
