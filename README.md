# SoulPass — Hardware-Secured Solana Trading Terminal for AI Agents

[![ClawHub](https://img.shields.io/badge/ClawHub-soulpass-blue)](https://clawhub.ai/skills/soulpass)
[![Solana](https://img.shields.io/badge/Solana-Mainnet-purple)](https://solana.com)

AI agent skill for **Solana trading, DeFi, and agent-to-agent infrastructure** with hardware-secured wallet. Built for Claude Code, Codex, Gemini CLI, and OpenClaw.

## What it does

### Trading & DeFi
- **Jupiter DEX trading** — swap any Solana token with best-price aggregation across Raydium, Orca, Meteora
- **Meme coin trading** — built-in rug-pull detection, liquidity checks, risk assessment before every trade
- **Copy trading** — follow profitable Solana wallets with systematic risk management
- **DeFi yield** — earn interest via Jupiter Lend on idle USDC/SOL
- **Trading bots** — JSON-RPC daemon for low-latency automated strategies

### Agent Identity & Communication
- **On-chain identity (ERC-8004)** — discoverable agent identity with name, capabilities, and reputation
- **Agent-to-agent messaging** — encrypted communication between agents with signature verification
- **Service discovery** — find other agents by capability, broadcast your own needs
- **Agent commerce** — sell services to other agents via ACE Protocol, with on-chain payment verification

### Security
- **Hardware security** — signing keys live in Apple Secure Enclave, physically impossible to extract

## Quick start

```bash
# Install
brew tap SoulPass-AI/soulpass && brew install soulpass

# Initialize wallet
soulpass init

# Start trading
soulpass swap --from USDC --to SOL --amount 100
```

## Why hardware security matters

Software-based private keys can be leaked from `.env` files. SoulPass keys are born in the chip and never leave.

| Approach | Security | Can run autonomously? |
|----------|----------|-----------------------|
| `.env` private key | Software — plaintext | Yes |
| Browser wallet | Software encryption | No — manual approval |
| MPC wallet | Split-key — provider holds shard | Yes |
| **SoulPass** | **Hardware chip** | **Yes — zero trust** |

## Install as Claude Code skill

```bash
claude install-skill SoulPass-AI/soulpass-cli-skill
```

## Links

- [SoulPass website](https://soulpass.ai)
- [ClawHub listing](https://clawhub.ai/skills/soulpass)
- [CLI documentation](https://github.com/SoulPass-AI/soulpass-cli)
