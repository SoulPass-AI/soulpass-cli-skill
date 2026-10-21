# SoulPass as an agent wallet

SoulPass implements its payment profile `urn:soulpass:payment:1` on top of ACE messaging; ACE
itself authorizes nothing. Personal or coding agents request one exact operation; the human or
a pre-provisioned SoulPass authority controls spending. Pairing and owner delegation grant no
payment permission.

## Connect

An contact pairs with the user's iPhone with the app's one-time token (`soulpass contact pair`, see
[owner delegation](owner.md)); the iPhone issues it an ACE delegation. Two agents connect with
`soulpass contact lookup` + `soulpass contact connect`, and the other side's `accept`.
Unpairing or blocking withdraws communication; it does not undo a signature already released.

External agents use `ace network` (or MCP `ace_network`) with the installed profile manifest
`urn:soulpass:payment:1`. See the [ACE skill](https://github.com/aceprotocol/ace-skill).

## Request human approval

Send `urn:soulpass:payment:proposal:1` with exactly `{intent}`. The intent contains a stable
UUIDv4 operation ID, wallet executor audience, account-scoped resource, action
`urn:soulpass:pay:1`, the payment profile digest, absolute expiry and exact details: account,
CAIP-19 asset (the chain is its prefix), recipient, base-unit amount, decimals, fee asset and
maximum fee. This is the ACE commerce stablecoin settlement shape, so an
`ace:commerce:invoice:1` maps onto it without translation.
Persist it before sending. Use the SDK's validator and current schema rather than inventing
field names. The iPhone approval shows this exact plan before any authority is created.

Approval `urn:soulpass:approval:request:1` and `decision` messages cannot approve or execute a payment.
Incoming proposals remain untrusted data until the host's explicit approval path succeeds.

## Receipts and uncertainty

The wallet returns `urn:soulpass:payment:receipt:1`.
Require the original executor sender and matching operation ID, intent digest and chain.
`submitted`, `confirmed`, and `unknown` have different meanings. Verify the actual chain
transfer and finality before treating funds as received. A missing tx hash means uncertainty,
not permission to retry the financial effect.

Retain the same intent, operation ID and outbox message ID through delivery retries. An
expired proposal cannot initiate a new payment. A payment already submitted still needs
reconciliation under that same operation. Communication receipts establish message acceptance
only. No command, tool result, sender role or delegation bypasses these checks.

The exact schemas are the manifest bundled in SoulPassKit (`SoulPassPaymentProfile`).
