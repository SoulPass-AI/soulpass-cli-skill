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
3. The approval delivers an `ace:delegation:1` credential signed by the owner the token names. Only
   then is the owner recorded; the agent republishes its descriptor with the credential in
   `ext["ace:delegation:1"]`. `contact owner` shows the
   owner and the credential's expiry.

While the owner's credential is live, `contact pair` refuses another token, so an agent cannot be
talked into moving to someone else. To move it, the user unpairs it in the app; once the credential
has lapsed (at most 7 days) a new token pairs.

## Approval messages

The SoulPass profile `urn:soulpass:approval:1` carries:

| Type | Direction | Body |
| --- | --- | --- |
| `urn:soulpass:approval:request:1` | agent → owner | `action`, `summary`, optional `amount`, `currency`, `expiresAt` (unix seconds), `details`, `ref` |
| `urn:soulpass:approval:decision:1` | owner → agent | `requestId`, `outcome` (`approve` / `deny`), optional `reason`, `result` |
| `urn:soulpass:approval:report:1` | agent → owner | `action`, `summary`, `outcome` (`ok` / `failed` / `skipped`), optional `requestId`, `ref`, `proof` |

The owner delivers and renews the agent's credential with ACE's own `ace:delegation:1` message
(`{credential}`: `issuer`, `subject`, `issuedAt`, `expiresAt`, `signature`; at most 7 days).

### Asking your owner: consent requests and the approval card

Any `action` you name is yours to define (`restaurant.book`, `email.send`, `x402.pay` paid from
your own funds, ...). On the iPhone a request whose action is not a payment word is a **consent
request**: the owner sees it, approves with one passkey presence or denies, and you receive a
`decision`. Approving moves nothing from the owner's wallet and runs nothing on the phone — it is
the owner saying yes; you do the work, then send a `report`. The payment words `pay` and
`urn:soulpass:pay:1` are reserved: a payment from the owner's wallet is only ever a
`urn:soulpass:payment:proposal:1` (see [agent wallet](agent-wallet.md)); a plain request using
one of those words can only be denied.

Describe what the owner is agreeing to in `details.display` (a SoulPass convention inside the
free `details` object; the rest of `details` stays yours):

```json
{"action": "restaurant.book", "summary": "book dinner friday", "expiresAt": 1800000000,
 "details": {"venueId": "nopa",
   "display": {"title": "Book dinner Friday",
     "facts": [{"label": "where", "value": "Nopa, 560 Divisadero"},
               {"label": "when", "value": "Fri 7:30pm, 6 people"},
               {"label": "deposit", "value": "$40 on the agent's card"}]}}}
```

- `title` optional, 1–80 characters; `facts` 1–8 rows, `label` 1–32, `value` 1–160; no other members.
- Plain text only: no control, format (bidi, zero-width), line/paragraph separator or private-use
  characters. A display that breaks any rule is dropped whole (the request still shows, with its
  `summary`); the phone never draws part of a card.
- The card is labeled as written by you: it is your description, not a fact SoulPass checked.
  Do not put anything in it you would not stand behind in a `report`.
- `expiresAt` is absolute unix seconds; at or after it the owner can no longer decide.

Both sides enforce the relationship on send and receive: agent messages are accepted only from
a live delegate of the receiving owner (`not_permitted` otherwise); owner messages only from the
agent's owner, and a decision only for one open request (`bad_reference` otherwise). Even an
approve decision does not authorize a payment; payments use the proposal and exact-grant
protocols in [agent wallet](agent-wallet.md).
