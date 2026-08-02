# WB-CORE-003 Coder Self-Check

Implementation stayed inside the approved write-set. A high authority-binding
finding was remediated by deriving READY state only from a committed,
role-separated authorization record and detached signature, independently
binding and verifying both in lifecycle and the hook against an external Owner
trust anchor. Offline generated-key fixtures cover positive verification plus
missing environment, modified JSON/signature, wrong signer, forged local
record, expiry, and stale-base cases. Independent review remains pending; a
Reviewer READY is advisory only.

Repeat-review remediation adds explicit hook regressions for forged and widened
READY gates plus dirty and changed authorization bindings. It also routes paired
`.agent` authority paths to the Codex CI suite and removes the duplicate active
Work Block projection from Planned.

Renewal now independently revalidates the authorization JSON and detached
signature blob bindings plus every signed gate field before updating expiry.
Offline adversarial fixtures assert that blob, write-set, specification, digest,
Critic, and Work Block tampering is rejected with the forged state unchanged.
