# Work Entry 009 — bounded RTX 5070 Ti execution pilot preparation

Status: `COMPLETE` — preparation published; live execution unperformed

Priority: `GREEN` (normal attention)

Operator health: `BLUE` — newly scoped; readiness unverified. Health is kept
separate because the canonical work protocol does not define `BLUE` as a
priority value.

## Objective and authority

Prepare the first small, observable execution against the existing RTX 5070 Ti
appliance. This entry is separate from Work Entries 005 and 007 and from their
branch-to-main reconciliation. Preparation may inspect public repository evidence
and author repo-cp records. It may not invoke a model or GPU workload, install or
deploy software, use or alter credentials, or mutate a host, VM, service, device,
adapter or runtime.

The machine-readable entry is [WORK_ENTRY_009.json](WORK_ENTRY_009.json). The
reviewable run packet is
[rtx5070ti-execution-pilot.md](../proposals/rtx5070ti-execution-pilot.md).
The JSON is the immutable START record and therefore retains its then-current
`ACTIVE` state; this handoff and the canonical topology carry the later closure.

## Finding

The historical `ws-code-agent → cuda-compute → RTX 5070 Ti` label is not the
current execution topology. Current committed evidence identifies:

- accelerator/runtime policy owner: `gpu-cp` at
  `e64e39c029616d69ec4523500facd20e7a75c9f2`;
- appliance implementation: `gpu-compute` at
  `c1d001a8f19ff4108d303f4529dde276e39f8253`;
- guest compute/access owner: `compute-cp` at
  `a615f8db86a52abb9612f083695f0185301aa991`;
- workstation transport evidence: `ws-cp` at
  `2fda2ffc4f230f690523beaf17d76186ddc7d0e5`;
- physical host `hv-katra`, Proxmox VM 320 `cuda-compute-katra`, and direct
  passthrough of NVIDIA device `10de:2c05` to the guest.

`ws-code-agent` is a bounded validation surface recorded inside ws-cp, not a
current independent repository or a general GPU command adapter. The existing
Ollama tunnel and NVIDIA telemetry identities are finite and do not provide an
administrative shell. The run packet therefore uses an explicitly authorized
operator guest session and the existing gpu-compute smoke script; it does not
invent a dispatcher or broaden a forced-command identity.

## Dependency disposition

Work Entry 005 review commit
`3073fd4e4c552a692d506489597faaf3f5e1038a` defines
`helix-offload.execution-request/v1` only for `TEXT_GENERATION_UTF8`, with model
network and tools denied. Its admission result always says
`execution_occurred: false` and `adapter_invoked: false`. It is therefore not an
admission contract for this CUDA-kernel smoke and is not a runtime prerequisite.
Before any later text-generation pilot, recheck that contract on canonical main.

The preserved Work Entry 007 contribution-attribution proposal describes Git
commit and work contribution claims. It explicitly says role `execute` is
development activity, not live execution. It is not a runtime prerequisite and
must not be used to infer the GPU executor. If a later commit records this
pilot, 007 may attribute that commit separately from the runtime receipt.

Applicable admission for this pilot is instead a later exact operator decision
under `HELIX_REPOSITORY_WORK_PROTOCOL_V1`, the gpu-cp runtime boundary and the
gpu-compute guest boundary. The decision must name the target guest, reviewed
script identity, executor/session, one invocation, timeout and evidence return.

## Preparation result

The selected workload is the existing `tests/smoke/cuda-nvidia` compiled-kernel
probe. It has fixed source, allocates one integer on the device, launches one
thread, requires `sm_120`, verifies the returned value `42`, and cleans its
temporary compilation directory through an exit trap. It performs no model
call, model pull, service change or peer mutation.

Current readiness remains `UNKNOWN`: repository evidence is strong but dated,
and no live telemetry, host probe or CUDA command was run during preparation.
The smallest next action is review and exact authorization of the packet. A
later run must stop before execution if the guest identity, script hash, profile
hash, device identity, storage reserve or live authority differs.

Preparation, review-branch delivery, ordinary publication and independent
canonical verification completed in repo-cp commit
`37a84624c029fba101f9899affab714e4b31b49f`. The preparation entry is therefore
complete and scheduling-ineligible. The packet remains an unperformed proposal;
its exact live authority must come from a separate later decision.

Live effects: NONE.
