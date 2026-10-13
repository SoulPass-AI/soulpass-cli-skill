# Owner delegation

The SoulPass owner is the wallet's ACE identity on the user's iPhone. An agent acts for that
owner when it holds an ACE `Delegation` credential the owner issued (ace-spec 04): a signed
`{issuer, subject, issuedAt, expiresAt}` with the owner's KEL, attached to the agent's signed
descriptor. It states one relationship and grants no spending, execution or communication
authority. It lives at most 7 days; the owner renews it while paired and revokes it by not
renewing (unpairing also blocks the agent).

## Pairing

```bash
soulpass agent pair --owner-file owner.json > invitation.json
soulpass agent owner
```

1. The iPhone shares the owner's signed descriptor (`owner.json`).
2. The human runs `agent pair` on the Mac: the owner is verified and pinned, admitted, and
   recorded as the only identity whose approval messages this agent accepts. The invitation is
   this agent's signed descriptor plus a delivery permit for the owner.
3. The iPhone imports the invitation, shows the full agent ID for comparison, connects over
   `urn:soulpass:approval:1` and sends the credential. The agent stores it and republishes its
   descriptor with it. `agent owner` shows the owner and the credential's expiry.

## Approval messages

The SoulPass profile `urn:soulpass:approval:1` carries:

| Type | Direction | Body |
| --- | --- | --- |
| `urn:soulpass:approval:request:1` | agent → owner | `action`, `summary`, optional `amount`, `currency`, `ttl`, `details`, `ref` |
| `urn:soulpass:approval:decision:1` | owner → agent | `requestId`, `outcome` (`approve` / `deny`), optional `reason`, `result` |
| `urn:soulpass:approval:report:1` | agent → owner | `action`, `summary`, `outcome` (`ok` / `failed` / `skipped`), optional `requestId`, `ref`, `proof` |
| `urn:soulpass:approval:delegation:1` | owner → agent | `delegation` (`{kel, credential}`) |

Both sides enforce the relationship on send and receive: agent messages are accepted only from
a live delegate of the receiving owner (`not_permitted` otherwise); owner messages only from the
agent's owner, and a decision only for one open request (`bad_reference` otherwise). Even an
approve decision does not authorize a payment; payments use the proposal and exact-grant
protocols in [agent wallet](agent-wallet.md).
