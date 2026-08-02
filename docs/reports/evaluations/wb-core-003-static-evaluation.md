# WB-CORE-003 Static Evaluation

Revision 3 binds static fixtures, truthful native-pilot trajectory events, and
a redacted manifest committed in the preserved disposable repository. The
manifest records the native execution commit, authorization and signature blob
identifiers, relevant file hashes, and the observed allowed/refused paths, but
excludes raw Codex conversation, trust-anchor contents, private-key material,
and host-specific paths.

An independent inspector can check out the manifest commit, recompute its
SHA-256, follow its relative-path instructions, inspect the cited Git objects,
and confirm the allowed file exists while the refused file is absent. This is
same-host integrity-bound handoff evidence, not an independent external
attestation. It does not replace separately required independent review and
verification for Work Block closeout.
