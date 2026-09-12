# Foundation compatibility requests

These requests neither extend V1 nor reopen its missing-contract blocker.

## FCR001: structured action guarantees

REQUESTED / NOT IMPLEMENTED. Ask Foundation to consider an additive companion
contract or future version for unique gate identity, operation class,
referenced-artifact checksums, authentication method, secret-handling declarations,
and expiration/invalidation conditions. Foundation must define V1 binding,
representation, validation, compatibility, authority and fail-closed rules with
reference tests and migration guidance. No local substitute schema is proposed.

V1 has no structured fields for these properties. Existing domain artifacts
retain those guarantees where applicable; free-text preconditions are not machine
enforcement. Action-artifact checksums differ from repo-cp's accepted Foundation
implementation digests. Secret-indicator heuristics do not establish universal
secret policy or prove absence of secrets. V1 also does not prove command safety,
capability, provenance authenticity or authorization. Unsupported guarantees
never become PASS and do not prevent safe supported V1 rendering.

## FCR002: target-facet authority

HELIX_TARGET_FACET_CONTRACT_V1 is UNRESOLVED / NOT SUPPLIED by Foundation
999fcf6a4bf181bdba201e9ca0c2f2bc4e7e2af5. Louis's separate target-facet request
remains the input for Foundation-owned vocabulary, schema, invariants,
compatibility and conflicts. No facet contract, ownership matrix or enrollment
of peer facet declarations is supplied here. No virtualization-cp is created.
Hosting, OS type, observation and automation confer no target authority.

B70 remains NOT_ADMITTED; 192.168.10.91 is observed evidence only;
DESIRED_NETWORK_STATE=UNRESOLVED; LIVE_MUTATION=NONE. Guest-platform and
application-workload owner selection remains Louis's unresolved decision after
reviewing domain missions. No arm-cp/gpu-cp selection is guessed.
