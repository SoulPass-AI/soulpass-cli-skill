# Owner delegation

The SoulPass owner is the wallet's ACE identity on the user's iPhone. An agent acts for that
owner when it holds an ACE `Delegation` credential the owner issued (ace-spec 04): a signed
`{issuer, subject, issuedAt, expiresAt}` with the owner's KEL, attached to the agent's signed
descriptor. It states one relationship and grants no spending, execution or communication
authority. It lives at most 7 days; the owner renews it while paired and revokes it by not
renewing (unpairing also blocks the agent).

## Pairing

```bash
SOULPASS_PAIR_TOKEN="$TOKEN" soulpass contact pair        # or: --token-stdin, --token-file <chmod 600>
soulpass contact owner
```

1. The SoulPass app on the iPhone shows a one-time pairing token (`soulpass:pair?o=<owner>&s=…`,
   10 minutes, single use). The user hands it to the agent over a private channel — never as a
   command-line argument.
2. `contact pair` sends the owner a `urn:soulpass:approval:1` contact request whose note proves the
   token, then waits while the user approves it on the iPhone.
3. The approval carries the credential, which proves the token back. Only then is the owner
   recorded; the agent republishes its descriptor with the credential. `contact owner` shows the
   owner and the credential's expiry.

While an owner is recorded, `contact pair` refuses another token, so an agent cannot be talked
into moving to someone else.

## Approval messages

The SoulPass profile `urn:soulpass:approval:1` carries:

| Type | Direction | Body |
| --- | --- | --- |
| `urn:soulpass:approval:request:1` | agent → owner | `action`, `summary`, optional `amount`, `currency`, `expiresAt` (unix seconds), `details`, `ref` |
| `urn:soulpass:approval:decision:1` | owner → agent | `requestId`, `outcome` (`approve` / `deny`), optional `reason`, `result` |
| `urn:soulpass:approval:report:1` | agent → owner | `action`, `summary`, `outcome` (`ok` / `failed` / `skipped`), optional `requestId`, `ref`, `proof` |
| `urn:soulpass:approval:delegation:1` | owner → agent | `delegation` (`{kel, credential}`) |

Both sides enforce the relationship on send and receive: agent messages are accepted only from
a live delegate of the receiving owner (`not_permitted` otherwise); owner messages only from the
agent's owner, and a decision only for one open request (`bad_reference` otherwise). Even an
approve decision does not authorize a payment; payments use the proposal and exact-grant
protocols in [agent wallet](agent-wallet.md).
