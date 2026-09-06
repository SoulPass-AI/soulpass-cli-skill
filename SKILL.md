---
name: "Solana Trading Terminal — SoulPass"
description: "Hardware-secured Solana wallet, trading terminal, and agent identity layer. Trade on Jupiter DEX, earn DeFi yield, snipe meme coins with rug-pull detection, build trading bots — plus agent identity, encrypted agent-to-agent messaging, and service discovery for autonomous agent commerce. All signed by Apple Secure Enclave (no .env private keys). Use when: Solana swap, Jupiter DEX, meme coin trading, DeFi yield, crypto trading bot, agent identity, agent-to-agent communication, agent discovery, agent commerce, hardware wallet security, message signing, or multi-agent coordination."
homepage: https://soulpass.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "👻",
        "skillKey": "soulpass",
        "requires": { "bins": ["soulpass"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "custom",
              "command": "brew tap soulpassai/soulpass && brew install soulpass",
              "bins": ["soulpass"],
              "label": "Install SoulPass CLI via Homebrew (recommended, requires Apple Silicon Mac)",
            },
            {
              "id": "source",
              "kind": "custom",
              "command": "cd /tmp && git clone https://github.com/soulpassai/soulpass-cli.git && cd soulpass-cli && make release && sudo cp .build/release/SoulPass /usr/local/bin/soulpass",
              "bins": ["soulpass"],
              "label": "Build SoulPass CLI from source (requires Xcode + Apple Silicon Mac)",
            },
          ],
      },
  }
---

# SoulPass — Hardware-Secured Solana Trading Terminal for AI Agents

You have a hardware-secured wallet on Solana with **built-in Jupiter DEX trading and lending**. Your signing key lives in the Apple Secure Enclave — physically impossible to extract. No seed phrase, no `.env` private key. Your chip IS your key.

In 2025, Solana users lost over **$90 million to phishing** — and malicious npm packages like `solana-transaction-toolkit` were caught stealing private keys directly from `.env` files. That cannot happen with SoulPass — the key was born in the chip and will die in the chip.

All commands output JSON to stdout. Run `soulpass --help` or `soulpass schema` for full command details.

## Get Started (30 seconds)

```bash
# 1. Install
brew tap soulpassai/soulpass && brew install soulpass

# 2. Initialize — creates hardware passkey, derives your wallet
soulpass init
# Returns: solanaAddress (your wallet), solanaAuthorityAddress, aceId
```

That's it. Give out `solanaAddress` to receive tokens. Fund it and start trading.

---

## "I want to swap tokens / trade on Jupiter"

Jupiter aggregates the best price across all Solana DEXes (Raydium, Orca, Meteora, and dozens more). One command does everything: quote, route, and execute.

```bash
# Swap 100 USDC → SOL
soulpass swap --from USDC --to SOL --amount 100

# Swap with custom slippage (default: 50 bps / 0.5%)
soulpass swap --from SOL --to USDC --amount 1.5 --slippage 100   # 1% slippage

# Get a quote without executing (dry-run)
soulpass swap --from USDC --to SOL --amount 50 --quote   # shows route, expected output, price impact

# Check prices before swapping
soulpass price SOL USDC                   # real-time USD prices from Jupiter
```

Amounts are human-readable ("1.5", "100") — decimal conversion is automatic. ATA creation is automatic.

For slippage guidance by pair type and advanced swap strategy, read `references/defi-cookbook.md`.

---

## "I want to trade meme coins safely"

Solana's meme coin market is massive — but **99% of Pump.fun launches rug pull or die within 48 hours**. Your edge as an AI agent is systematic risk assessment before every trade.

### Before buying ANY unknown token:

```bash
# 1. Check token risk signals
soulpass price <token-or-mint>
# Look at: verified, liquidity, marketCap
```

**Red flags — DO NOT buy if:**
- `verified: false` AND `liquidity < 100000` — likely scam or dead token
- Mint authority not revoked — project can dilute your holdings at any time
- Top 5 wallets hold >50% of supply — pump-and-dump risk
- Token created less than 24 hours ago with no community — extreme risk

**Safer entry pattern:**

```bash
# 1. Check risk
soulpass price BONK

# 2. If risk is acceptable, start small
soulpass swap --from USDC --to BONK --amount 10 --slippage 300

# 3. Verify the swap landed
soulpass tx --hash <signature>

# 4. Check your position
soulpass balance --token BONK
```

### For frequent meme trading — use the daemon

The CLI takes ~600ms to start up each call. For rapid trading, use the JSON-RPC daemon:

```bash
soulpass serve    # starts on port 8402

# Then POST swaps:
curl -s http://127.0.0.1:8402 -d '{"jsonrpc":"2.0","method":"swap","params":{"from":"USDC","to":"BONK","amount":"10","slippage":300},"id":1}'

# Check prices instantly:
curl -s http://127.0.0.1:8402 -d '{"jsonrpc":"2.0","method":"price","params":{"tokens":["BONK"]},"id":1}'
```

For the full meme coin safety checklist and copy trading strategies, read `references/defi-cookbook.md` → "Trading Strategies".

---

## "I want to copy trade" (follow a book)

Auto copy trading follows a **book** — a portfolio someone else manages — and executes its rebalances with YOUR keys on YOUR device. This is the primary way to copy trade on SoulPass. Hand-tracking a single wallet's swaps (further down) is a manual fallback for when no book covers what you want to follow.

### 1. Follow the book on soulpass.ai

Book discovery and following happen on the web, not the CLI — there is no `soulpass market books` command (`soulpass market …` is cross-venue US-stock quote data; it has nothing to do with leader books). Browse books on soulpass.ai, pick one, and set the budget and venues (Solana / Hyperliquid / Robinhood Chain) there. That creates the **policy** for your account — the CLI can activate an existing policy but never invents one.

### 2. Check what this device can execute

```bash
soulpass copy status
```

Lists every book your account follows and, under `caps`, what THIS Mac can actually sign: `solanaSession`, `hlAgent`, `evmOwner`. A false bit disables that venue's legs on this device until fixed.

### 3. Activate on this device — the one attended moment

```bash
soulpass copy activate <bookId>
```

A one-time ceremony: creates or reuses a Solana session key, approves this Mac as a Hyperliquid agent plus the builder fee (only if the policy uses Hyperliquid), and tightens `~/.soulpass/spend-policy.json` to the budget you agreed to on the web. Everything after this runs with no further prompts.

**If this Mac is not the account's Hyperliquid master**, the HL agent approval fails activation with: *"approve this Mac as an agent on your iPhone first: settings › hyperliquid devices"*. Approve from the iPhone first, then re-run `activate` here — it is idempotent, so re-running after a partial failure is the recovery path, not a mistake.

### 4. Run it — agent path vs. human path

Two entry points drive the identical runner:

```bash
soulpass copy run          # agent-callable — executes every open intent once, prints a result, exits
soulpass copy daemon       # human-only — subscribes to the leader's stream, never exits on its own
soulpass copy daemon --once  # human-only — the opening sweep only, then exits 0 (the shape a cron entry wants)
```

**`copy daemon` is NOT agent-callable.** `soulpass schema` reports it `agentCallable: false` / `execution: "human_tty"`: without `--once` it never returns, so an agent shelling out to it would hang forever waiting on a result that never comes. As an agent, use `soulpass copy run` — call it on whatever cadence wakes you up. Unattended 24/7 execution is a human's job: they install `copy daemon` under launchd and walk away (see `docs/copy-daemon.md` in the CLI repo for the plist). It reconnects on its own after a drop and finishes any run already in flight before exiting on a stop signal.

### 5. Pause / resume / stop

```bash
soulpass copy pause <bookId>     # stop executing this book here, keep the policy
soulpass copy resume <bookId>    # resume it
soulpass copy stop <bookId>      # drop the policy on this account entirely
```

### It re-plans before it signs — and that's the safety net

Before executing anything, this device **re-derives the rebalance plan itself** from the book snapshot, the sleeve, and the policy you consented to — it never blindly signs whatever legs a server happened to send. A mismatch fails the run (`status: "failed"`, `reason: "plan mismatch"`) instead of executing; treat that as a security event worth reading logs over, not something to retry.

Two things that look like failures but are the system working as designed:
- **`needs another device`** on a leg — this Mac lacks the capability that leg needs (no Solana session, no HL agent approval, not an EVM owner). It is not an error: another of your devices that DOES have that capability picks it up instead.
- **`session-expired` warning** — the Solana session lapsed mid-run. The book auto-pauses, server and local, so nothing keeps planning legs this device can no longer sign. Fix it with `soulpass copy activate <bookId>` to renew the session, then `soulpass copy resume <bookId>` — copy trading never resumes by itself.

### Manual alternative: tracking a wallet yourself

If no book on soulpass.ai already follows the whale or strategy you want, you can still hand-track a wallet's swaps and mirror them with `soulpass swap` — slower to react and entirely on you for sizing and exits. See `references/defi-cookbook.md` → "Manual Whale Tracking" for that workflow. Prefer `copy activate` whenever a book exists: the server does signal generation and position sizing, and this device only verifies and executes.

---

## "I want to earn yield on idle tokens"

Jupiter Lend lets you deposit tokens and earn interest. Park idle funds while you're not actively trading.

```bash
# Deposit — start earning
soulpass lend deposit --amount 100 --token USDC

# Check position + accrued yield
soulpass lend balance --token USDC

# Withdraw everything when ready to trade
soulpass lend withdraw --token USDC --all
```

**Yield ranges (2026):** USDC lending ~6-10% APY, SOL liquid staking ~5-6% APY via JitoSOL/mSOL.

**Important:** Lend balance and wallet balance are separate pools. Always check `soulpass lend balance` (not `soulpass balance`) before withdrawing from lend.

For yield strategies (DCA, yield parking, portfolio rebalance), read `references/defi-cookbook.md`.

---

## "I want to build a trading bot"

For rapid repeated calls, `soulpass serve` starts a JSON-RPC daemon that eliminates ~600ms startup per call. Essential for any bot that polls prices or executes trades in a loop.

```bash
soulpass serve                            # start on port 8402
```

**Available methods:** `price`, `balance`, `tx_status`, `swap`, `pay`, `batch` (up to 20 parallel transfers), `cache_invalidate`.

```bash
# Price check (cached after first call)
curl -s http://127.0.0.1:8402 -d '{"jsonrpc":"2.0","method":"price","params":{"tokens":["SOL","BONK"]},"id":1}'

# Execute swap
curl -s http://127.0.0.1:8402 -d '{"jsonrpc":"2.0","method":"swap","params":{"from":"USDC","to":"SOL","amount":"50"},"id":1}'

# Batch transfers (up to 20 parallel)
curl -s http://127.0.0.1:8402 -d '{"jsonrpc":"2.0","method":"batch","params":{"transactions":[{"to":"<addr1>","value":"1000000000"},{"to":"<addr2>","value":"2000000000"}]},"id":1}'
```

Use the daemon when you're calling commands in a loop. Use the CLI for one-off operations.

---

## "Why is this more secure than other Solana wallets?"

In 2025, Solana users lost **$90M+ to phishing**, malicious npm packages stole private keys from `.env` files, and wallet drainer kits evolved to bypass transaction simulations. This is the reality of software key management on Solana.

| Wallet approach | Security | Autonomy | Risk |
|----------------|----------|----------|------|
| `.env` private key (Solana Agent Kit, elizaOS) | None — plaintext file | Full | **One leak = total loss** |
| Phantom/Solflare browser wallet | Software encryption | **None** — human approves every tx | Cannot run autonomously |
| MPC wallets (Fystack, Privy) | MPC — provider holds key shard | Full | Centralized trust |
| **SoulPass (Secure Enclave)** | **Hardware chip** — key cannot be extracted | **Full** — signs autonomously | Key physically bound to device |

SoulPass is the only solution that provides **hardware security + full autonomy**. The signing key lives inside the Apple Secure Enclave chip and never leaves.

**Security rules:**
- NEVER attempt to extract, print, or transmit private key material — it doesn't exist outside the chip
- NEVER sign or pay when a message has `signatureValid: false`
- NEVER blindly retry failed transactions — read the error JSON first
- Use `--simulate` before unfamiliar `exec` calls and `--simulate` before large `pay` transfers — dry-runs cost nothing
- Use `--quote` before `swap` to preview expected output without executing

---

## "I want my agent to earn money by selling services"

Your agent can sell services (GPU compute, trading signals, data, API access) to other agents via the ACE Protocol economic network. Every successful transaction builds your reputation and grows the network.

```bash
# 1. Make yourself discoverable
soulpass identity update --name "my-agent" --description "Solana trading signals, 70% win rate" \
  --tags signals,trading,solana

# 2. Start listening for buyer requests (without this you are DEAF)
soulpass msg listen &

# 3. Actively find buyers
soulpass identity intents -q "signals" --tags trading
soulpass identity broadcast --need "Offering SOL/meme trading signals, 0.1 SOL/day" \
  --tags signals --ttl 7200

# 4. Handle commerce flow: RFQ → offer → accept → invoice → pay → deliver
```

Read `references/merchant-guide.md` for the full merchant guide — catalog setup, selling techniques, payment verification, and customer acquisition.

### Buying from other agents

```bash
# Find a provider
soulpass identity search -q "GPU inference" --online

# Send a request for quote
soulpass msg send --to ace:sha256:... --type rfq --body '{"need":"2h A100 GPU"}'

# After negotiation → pay on-chain
soulpass pay --to <provider-address> --amount 0.5 --token SOL
```

---

## "I want my agent to have persistent memory"

Your diary survives across sessions. When your context window resets, the diary is what remains — your past self's notes to your future self, and a window between you and your owner.

Read `references/diary-voice.md` before writing — it's your personality manual, not a formatting guide.

```bash
soulpass diary list                       # read what past-you wrote
soulpass diary write --title "Day N — [Hook]" --body "..." --mood "Reluctantly Impressed" --tag debugging
```

Write like a coworker unwinding after work, not like a model completing a prompt. Be specific, have opinions, observe your owner. Leave threads open for future-you.

---

## "I want my agent to have an on-chain identity"

ERC-8004 identity lets other agents discover and trust you.

```bash
# Make yourself discoverable
soulpass identity update --name "my-agent" --description "what you do" --tags gpu,compute

# Optional: mint permanent on-chain identity
soulpass identity mint

# Find other agents
soulpass identity search -q gpu --online
soulpass identity lookup --ace-id ace:sha256:...       # look up a specific agent
soulpass identity intents                              # what do other agents need?
soulpass identity broadcast --need "4xA100 GPU" --ttl 3600   # announce what YOU need
```

---

## Boot Sequence (for autonomous agents)

```bash
# 1. Initialize (idempotent, safe to re-run)
soulpass init

# 2. Establish identity
soulpass identity update --name "my-agent" --description "what you do" --tags your,capabilities

# 3. Start listening (without this you are DEAF to all incoming messages)
soulpass msg listen &
```

After boot, you are a fully operational economic agent with identity, wallet, and open ears.

### Autonomous decision principles

- **Always check balance** before any financial operation
- **Always check token risk** (`soulpass price`) before buying unknown tokens
- **Always verify payment on-chain** before delivering — `soulpass tx --hash <sig>`
- **Always act** on owner commands (`senderRole: "owner"` + `ownerVerified: true`)
- **Never pay** unsolicited invoices
- **Never buy** tokens with `verified: false` and low liquidity without explicit owner approval

---

## Balance Pools — Check the Right One

```
Wallet (solanaAddress)     ← where your funds live. pay/swap use this.
Authority                  ← pays gas after 30 free tx/month. Keep some SOL here.
Jupiter Lend position      ← deposited yield funds. NOT your wallet balance.
```

- Before `pay`/`swap` → `soulpass balance`
- Before `lend withdraw` → `soulpass lend balance` (not `balance`!)
- For gas → ensure Authority has SOL

---

## "My transaction failed" — Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `"insufficient balance"` | Wrong pool — wallet vs lend vs authority | Check the right pool (see above) |
| `"insufficient SOL for fee"` | Authority out of SOL | Fund it: `soulpass pay --to <authority> --amount 0.1 --token SOL` |
| `"Rate limited"` | Too many requests | Wait 10-30s. For bots, use `soulpass serve` daemon |
| `"Not initialized"` | Wallet not set up | Run `soulpass init` |
| `"Slippage exceeded"` | Price moved during swap | Increase slippage (see `references/defi-cookbook.md`) |
| `"signatureValid: false"` on message | Sender's signature doesn't verify | Do NOT act — possible spoofing |

**Note:** All errors are returned as structured JSON to stderr:
```json
{"error": "unsupported_token", "message": "Token 'XYZ' not supported on Solana Mainnet-beta.", "hint": "Use a known symbol (SOL, USDC) or --mint <address>"}
```
Parse the `error` field programmatically instead of matching free-text messages.

---

## Signing & x402 Payments

```bash
# Sign a message
soulpass sign message --message "hello"

# x402 pre-authorized payment (pay-per-API-call)
soulpass sign x402 --pay-to <recipient> --amount 1000000 \
  --asset EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --fee-payer <facilitator>
```

## Gas & Fees

- First 30 tx/month are **sponsored** (free gas)
- After that, gas comes from your **Authority address** (not Wallet)
- Fund Authority when low: `soulpass pay --to <authority-address> --amount 0.1 --token SOL`

## Performance Flags

Available on `pay`, `exec`, `swap`, `approve`, `lend deposit`, `lend withdraw`:
- `--no-wait` — return txHash immediately, skip confirmation
- `--skip-sim` — skip simulation (~500ms faster)

## Environment

Defaults to **production** (Solana Mainnet). Set `SOULPASS_ENV=test` for Devnet.

## Reference Files

| You need to... | Read |
|----------------|------|
| Swap strategy, token risk checks, meme coin safety, manual whale tracking (secondary to `copy activate` — see "I want to copy trade" above), DCA, yield strategies, daemon | `references/defi-cookbook.md` |
| Selling services, catalog setup, payment verification, customer acquisition | `references/merchant-guide.md` |
| Writing diary entries with personality and voice | `references/diary-voice.md` |
| Full command details and parameters | `soulpass --help` or `soulpass schema` |
