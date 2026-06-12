# Production Maintainability Standard

> Mandatory acceptance rule for all production code changes.

---

## The Rule

Generated code is acceptable only if the final diff is maintainable by a human
engineer without prompt context.

## Production Code Must:

- Follow existing project patterns and naming
- Keep abstractions small and justified by current complexity
- Expose side effects, data flow, failure modes, and ownership boundaries clearly
- Avoid prompt-shaped, generic, over-broad, or speculative helper code
- Avoid duplicated generated boilerplate that will drift during maintenance
- Include targeted checks that prove the changed contract, not just a green build
- Be explainable in the closeout without relying on hidden prompt history

## Reviewer/Verifier Must Block If:

- The diff looks correct only because of the prompt context
- The code is hard to modify safely
- The code would be costly for a future maintainer to own
- Abstractions exist "just in case" without current need
- The change duplicates patterns instead of reusing existing ones

## Why This Matters

AI agents can generate code that looks correct but is unmaintainable. The
Production Maintainability Standard ensures the human engineer who inherits
this code 6 months from now can understand and modify it without needing the
original prompt conversation.
