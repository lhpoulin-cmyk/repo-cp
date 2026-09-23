"""Fixed stderr blockers with an explicit allowlist of public reason codes.

Public codes describe the state of repo-cp's own reviewed files or local
checkout and are independent of stdin payloads, argument text and the
secret-indicator heuristic. Everything else stays internal and yields only the
fixed blocker line. Classification is per code, not per call site: a code
shared by several sites takes the most conservative class of any of them.

Internal by design:
- Render payload and JSON parsing codes (shared with stdin input); README
  documents fixed non-disclosing stderr for invalid input.
- CLI_ARGUMENTS and UNKNOWN_ARGUMENT; accepted tests pin generic stderr for
  argument errors. Promoting them is an acceptance decision.
- SECRET_INDICATOR, shared with render input; it would be a heuristic oracle.
- Peer-evidence codes, which audits convert to findings, and every code of the
  unprivileged publication reference, which no CLI or validation path reaches.

tests/test_diagnostics.py checks that every literal Denied code in src/repocp
and tools is classified exactly once and that no classification is stale.
"""
from .safety import Denied

PUBLIC = frozenset({
    'AGENT_CONTRACT_MISMATCH', 'AGENT_CONTRACT_PIN_INVALID', 'BROKEN_DOCUMENT_LINK',
    'DUPLICATE_REPOSITORY', 'ENROLLMENT_AUTHORITY_CONFLICT', 'ENROLLMENT_NONCONFORMANCE',
    'FILE_INTEGRITY_AUDIT_FAILED', 'FILE_INTEGRITY_NONCONFORMANCE',
    'FOUNDATION_ARTIFACT_MISMATCH', 'FOUNDATION_PIN_INVALID', 'FOUNDATION_REGISTRY_MISMATCH',
    'PUBLIC_FILE_CHANGED', 'PUBLIC_FILE_UNAVAILABLE', 'REPOSITORY_IDENTITY_CONFLICT',
    'REPOSITORY_NOT_SELECTED', 'SINGLE_LINK_REGULAR_REQUIRED', 'UNSAFE_EXCLUSION',
    'UNSAFE_FILE_OR_SIZE', 'UNSAFE_PATH', 'UNSAFE_REGISTRY', 'VALIDATION_COVERAGE_UNAVAILABLE',
    'VERSION_MISMATCH',
})
INTERNAL = frozenset({
    # Input, parsing, arguments and secret heuristic.
    'CLI_ARGUMENTS', 'DUPLICATE_FIELD', 'INPUT_SIZE', 'INVALID_JSON',
    'OPERATOR_ACTION_NONCONFORMANCE', 'SECRET_INDICATOR', 'UNKNOWN_ARGUMENT',
    # Peer evidence and local audit internals, reported as findings instead.
    'AUDIT_DIRECTORY_CHANGED', 'AUTH_REVIEW_UNAVAILABLE', 'INVALID_GIT_EXCLUSION',
    'INVALID_HANDOFF_PIN', 'PUBLIC_REVISION_INVALID', 'PUBLIC_REVISION_UNAVAILABLE',
    'UNSUPPORTED_GIT_LAYOUT',
    # Unprivileged publication reference.
    'ABSOLUTE_UNAMBIGUOUS_PATH_REQUIRED', 'ATOMIC_NOREPLACE_UNAVAILABLE', 'BYTE_COUNT_MISMATCH',
    'CONCURRENCY_CONFLICT', 'COPY_EXPECTATIONS_DIFFER', 'DESTINATION_DIRECTORY_CHANGED',
    'DESTINATION_DIRECTORY_POLICY', 'DIRECTORY_PATH_CHANGED', 'EXISTING_STATE_REQUIRES_RESOLUTION',
    'FILE_CHANGED_DURING_VERIFICATION', 'HASH_OR_BYTE_COUNT_MISMATCH', 'INTENT_MISMATCH',
    'INVALID_EXPECTATION', 'INVALID_OPERATION_ID', 'INVALID_RECOVERY_PLAN', 'METADATA_MISMATCH',
    'PUBLISHED_IDENTITY_CHANGED', 'RECEIPT_CHANGED', 'RECEIPT_MISMATCH', 'RECORD_CHANGED',
    'RECORD_IDENTITY_CHANGED', 'RECORD_METADATA_MISMATCH', 'RECORD_SIZE',
    'REVIEWED_REVISION_REQUIRED', 'SHORT_WRITE', 'SOURCE_CHANGED', 'SOURCE_PATH_CHANGED',
    'TEMP_IDENTITY_CHANGED', 'UNPRIVILEGED_REFERENCE_ONLY',
})
# Emit the module's own constant, never the exception's object.
CANONICAL = {code: code for code in PUBLIC}


def public_reason(error):
    """Return an allowlisted constant, or None. Subclasses and extra args are never trusted."""
    if type(error) is not Denied or len(error.args) != 1 or type(error.args[0]) is not str:
        return None
    return CANONICAL.get(error.args[0])


def blocker(name, error):
    """Fixed blocker line, plus a REASON line only for an exact public Denied code."""
    reason = public_reason(error)
    return 'BLOCKER=' + name + '\n' + ('' if reason is None else 'REASON=' + reason + '\n')
