# Private account evidence

An ACE link is a two-way proof: an account authority signs claims naming the independent ACE
identity, and its current ML-DSA signing delegation acknowledges those claims. Exchange it as
`{aceId,kel,links}`. It never enters relay registration or public descriptors.

## Create, import and share

```bash
soulpass agent attest --roles delegate
soulpass agent attest --record signed-link.json
soulpass identity evidence export > evidence.json
soulpass identity evidence import peer-evidence.json
soulpass agent attest --drop-link
```

A known SoulPass passkey root is the only accepted account signer. Without one, a current
on-chain Ed25519 owner signs. A wallet P-256 key does not become an ACE identity key and cannot
substitute for a supported account-link signer. If no supported account signer exists, the
command fails closed; the human can link the wallet to their passkey.

| Status | Meaning |
| --- | --- |
| `attested` | This device's wallet signer signed; the ACE identity acknowledged; saved locally |
| `unsigned` | Nothing written; `candidates[]` contains unsigned records and exact `signDataHex` |
| `imported` | The external signature was verified and a current ACE ack was added; saved locally |
| `withdrawn` | Local evidence was removed; already shared copies were not recalled |

For `unsigned`, the holder of the listed account key signs the candidate's exact 32-byte digest
with Ed25519 and adds the Base64 signature to its `record`. Import the result with `--record`.
Never sign a different digest, change the claims, fabricate an ack or substitute the ACE key.
The importer re-derives the signed bytes, checks account ownership, and signs the ack itself.
Granting controller roles with this device's wallet signer requires the human's terminal code.

## Verification and renewal

Receivers verify KEL continuity, both signatures, expiry, current signing delegation, and the
account authority. Matching account text or roles is insufficient. SoulPass's same-account
reader trusts the account signer from its own valid link; a stranger's self-signed claim is not
an account controller. Importing evidence grants neither communication nor payment authority.

Links created here last 365 days. Renew before expiry. Root/signing rotation invalidates old
acks, so SoulPass re-acknowledges valid local claims and peers need newly shared evidence.
Local removal cannot revoke copies; expiry, delegation changes and receiver authority policy
control their acceptance. A compromised identity can re-acknowledge an unexpired wallet claim
it still holds. Use shorter claims when the account requires quicker revocation.

Account coordination types are `ace:account:request:1`, `ace:account:decision:1`, and
`ace:account:report:1`. With an account context installed, the receiver checks the optional
same-account rules. Without it, those messages are authenticated data. Even a valid controller
link does not approve a payment. Payments use the proposal and exact-grant protocols in
[agent wallet](agent-wallet.md).

Best-effort controller reports require a local confirmed contact association, current private
evidence and an active communication contact. They cannot block or authorize the underlying
payment or copy run; never promise delivery from an attempted report.
