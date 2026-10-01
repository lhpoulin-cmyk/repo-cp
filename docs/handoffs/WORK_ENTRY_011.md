# Work Entry 011 — RTX 5070 Ti execution-host capacity assessment

Status: `COMPLETE` — assessment and measurement plan published; measurement unperformed

Priority: `GREEN` (normal attention)

Operator health: `BLUE` — requirements and current capacity are not yet fully
verified. Health is recorded separately because `BLUE` is not a priority value
in the canonical work protocol.

## Objective and authority

Assess whether the existing RTX 5070 Ti appliance can support the bounded Work
Entry 009 kernel pilot and the already documented model workloads. This entry
may read existing repository evidence and prepare records. It may not run a GPU
workload or benchmark, install software, reallocate resources, change the VM or
host, or purchase hardware.

The machine-readable entry is [WORK_ENTRY_011.json](WORK_ENTRY_011.json). The
capacity decision and coordinated measurement plan are
[work-entry-011-rtx5070ti-capacity-assessment.md](../proposals/work-entry-011-rtx5070ti-capacity-assessment.md).
The JSON is the immutable START record and therefore retains its then-current
`ACTIVE` state; this handoff and the canonical topology carry the later closure.

This assessment was initially recorded as Work Entry 010 in local commit
`1df7226210012096dde02b84593b4c29351ee14f`. Louis's follow-up reserved 010 for
DERP, so the capacity assessment is now 011. The original commit remains
immutable historical evidence; the mapping is recorded in
[WORK_ENTRY_010_011_RENUMBER.md](WORK_ENTRY_010_011_RENUMBER.md).

## Verified execution topology

The accelerator is not bare metal from the workload's perspective. The physical
host is Proxmox hypervisor `hv-katra`; execution occurs in VM 320,
`cuda-compute-katra`, with the NVIDIA compute function `10de:2c05` passed
through directly by VFIO as guest PCI device `0000:01:00.0`. The accepted VM
allocation is 8 vCPU and 16,384 MiB RAM. This naming and ownership split is
defined by compute-cp; gpu-cp accepts accelerator/runtime facts and gpu-compute
owns the appliance implementation.

The reviewed records do not state the hypervisor's physical CPU/RAM totals,
current contention, or current VM 320 configuration. Those facts remain
`UNKNOWN`; the coordinated measurement packet includes a bounded read-only host
preflight rather than mistaking guest allocation for physical-host capacity.

Historical accepted evidence records an NVIDIA GeForce RTX 5070 Ti with 16,303
MiB VRAM, compute capability 12.0, driver 610.57.04 and CUDA 13.3.73. It also
records a 64 GiB root disk with 43 GiB free after growth, a 160 GiB model disk,
and no swap during accepted model runs. These are evidence of the accepted
configuration, not a current live inventory. Negotiated PCIe speed and width
were not recorded in the reviewed evidence.

## Workload requirements

Work Entry 009 is the only new workload in this scope: one compilation and one
launch of a one-thread `sm_120` CUDA kernel that allocates four device bytes and
returns integer `42`, with a 120-second TERM deadline, 10-second kill grace and
no retry. It has no model, context, concurrency or persistent-storage demand.

Existing project requirements also include exact, accepted single-request
profiles at context 4096. Qwen2.5-Coder 14B Q4 is the conservative useful model
baseline: 100% GPU placement and 9,304 MiB observed peak VRAM. Larger accepted
profiles use partial CPU offload and approximately 14.6–14.9 GiB of reported
VRAM. Nothing reviewed accepts concurrent model requests or a larger runtime
context. Qwen3.5 9B QLoRA remains a proposed training workload, not a capacity
result: its fit probe stopped before training because the VM exposed a
`Common KVM processor` without the x86-v2/AVX baseline required by the tested
Python stack.

## Decision

The accepted historical configuration is **sufficient for the bounded Work
Entry 009 kernel pilot**, subject to the packet's current identity and resource
preflight. It was also sufficient for one Qwen2.5-Coder 14B Q4 request at
context 4096. Present-day readiness remains `UNKNOWN` until the one coordinated
009 preflight/run captures current capacity.

The evidence does not support a general conclusion for concurrent inference,
larger contexts, or QLoRA training. It also does not justify an upgrade. The
smallest next action is to execute the already prepared 009 packet only after
separate live authorization; its preflight and postflight measurements satisfy
011 without a duplicate benchmark.

Assessment, measurement-plan preparation, review-branch delivery, ordinary
publication and independent canonical verification completed in repo-cp commit
`37a84624c029fba101f9899affab714e4b31b49f`. Work Entry 011 is therefore
complete and scheduling-ineligible. The later 009 measurement is a coordinated
evidence source, not a blocking topology dependency and not execution authority.

Live effects: NONE.
