# RTX 5070 Ti execution-host capacity assessment

Status: preparation complete; current live capacity not measured.

This assessment coordinates with Work Entry 009. It uses accepted repository
evidence and delegates its one required current measurement to the 009 packet;
it does not define or request a second GPU run.

## Evidence boundary

The reviewed source revisions were gpu-cp
`e64e39c029616d69ec4523500facd20e7a75c9f2`, gpu-compute
`c1d001a8f19ff4108d303f4529dde276e39f8253`, and compute-cp
`a615f8db86a52abb9612f083695f0185301aa991`. Measurements below are historical
unless marked as a demand or unknown. No live host, guest, GPU, model or network
query was made during this assessment.

The principal reviewed records were:

- `gpu-compute:CURRENT_STATE.md` and
  `gpu-compute:config/model-runtime-profiles.tsv` at the revision above;
- `gpu-cp:docs/acceptance/rtx5070ti-runtime-20260810.md`, the Qwen2.5-Coder
  14B/32B and Devstral runtime acceptances, and the Katra profile README at the
  revision above;
- `compute-cp:contracts/guest-compute-appliance.md` and
  `compute-cp:evidence/2026-08-14-open-the-forge.md` at the revision above.

The physical host is `hv-katra`. The workload target is Proxmox VM 320,
`cuda-compute-katra`, with direct VFIO/PCIe passthrough of NVIDIA device
`10de:2c05` as guest device `0000:01:00.0`. This is a VM with direct device
assignment, not bare-metal execution, a container, or a virtual GPU allocation.

## Intended workload envelopes

| Workload | Size and context | Concurrency | Latency evidence or target | Expected use |
| --- | --- | --- | --- | --- |
| Work Entry 009 CUDA smoke | No model or context; one four-byte allocation and one-thread kernel | Exactly one invocation | Hard timeout at 120 seconds, then a 10-second termination grace; no performance SLO | One-time execution-path proof and current resource snapshot |
| Qwen2.5-Coder 14B Q4 | 14.8B parameters; accepted context 4096 | One request was exercised; keep proposed use at one | Observed 4.705 s cold and 0.284–0.297 s warm for the fixed six-token probe; no production latency target exists | Preferred conservative model for a separately authorized later local-agent pilot |
| Devstral 24B Q4 | 24.0B parameters; accepted context 4096 | Single-request evidence only | Observed 31.15 s cold and 0.91–0.92 s warm for its fixed probe; no production latency target exists | Exact-profile comparison option, not the first pilot |
| Qwen3-Coder 30B Q4 | 30.5B parameters; accepted partial-offload profile | Single-request evidence only | One neutral controlled run; no accepted latency target | Exact-profile option, not spare capacity |
| Qwen2.5-Coder 32B Q4 | 32.8B parameters; accepted context 4096 | One request at a time was exercised | Observed 51.547 s cold and 4.049–4.238 s warm for the fixed six-token probe; no production latency target exists | Same-family scale control, not the first pilot |
| Qwen3.5 9B QLoRA proposal | 9B-class training proposal; fit parameters remain in compute-cp | No batch ran | No latency or throughput evidence; stopped before training | Deferred until CPU/software compatibility is resolved |

No reviewed requirement establishes multi-request concurrency or a context above
4096. Observed probe times are not service-level objectives and should not be
extrapolated to arbitrary prompts.

## Capacity table

| Resource | Available capacity | Workload demand | Evidence | Gap |
| --- | --- | --- | --- | --- |
| GPU compute | RTX 5070 Ti, capability 12.0; direct passthrough | 009: one `sm_120` kernel, one thread, one launch | gpu-cp runtime acceptance records this exact kernel class passing | Current device identity and health must be rechecked |
| GPU memory | 16,303 MiB reported | 009: four device bytes plus compiler/runtime overhead; 14B: 9,304 MiB peak; 24B: 14,648 MiB; 30B: 14,890 MiB; 32B: 14,634 MiB | Accepted gpu-cp profiles, each single-request | 009 and 14B have strong historical margin; larger models leave only 1,413–1,669 MiB reported headroom; concurrency and larger contexts are unmeasured |
| Hypervisor CPU/RAM | Physical totals and current contention not stated in reviewed records | VM 320 requires its configured 8 vCPU and 16,384 MiB allocation | Physical host identity is accepted; capacity details are absent | Current host capacity, contention and exact VM allocation must be captured read-only |
| Guest CPU | 8 vCPU allocation; VM reported `Common KVM processor` without x86-v2/AVX in the training probe | 009: compile a tiny CUDA source and supervise one process; partial-offload profiles use 12–29% CPU placement; QLoRA stack requires a compatible CPU/software baseline | gpu-compute current state; compute-cp training evidence | Adequate historically for smoke/inference; training blocked before fit by CPU exposure/software compatibility |
| Guest RAM | 16,384 MiB VM allocation; accepted model runs retained at least 13,849,677,824 bytes available for 14B and 14,011,752,448 bytes for 32B | 009: small compile/process overhead; model demand already observed within allocation | gpu-compute and gpu-cp accepted runtime evidence | Current free/available memory unknown; no concurrency evidence |
| Swap | None during accepted model runs | 009 does not require swap; accepted profiles did not require it | gpu-cp acceptance | No gap for 009; adding swap would not cure the training CPU compatibility issue |
| Root storage | 64 GiB virtual disk; 43 GiB free after growth (historical) | 009: transient CUDA source/binary in task-owned `/tmp`; no persistent artifact | gpu-compute current state | Current free bytes and temporary-directory filesystem unknown |
| Model storage | 160 GiB virtual disk; 70,559,580,160 bytes free after 32B acceptance | No model use in 009; accepted 14B and 32B blobs are 8,988,110,784 and 19,851,336,384 bytes | gpu-compute state and gpu-cp acceptance | Current free bytes unknown; no new model acquisition is authorized |
| Storage performance | No throughput or latency measurement was found | 009 writes only a tiny transient source and binary; no storage SLO exists | No relevant benchmark evidence | Not needed for 009; define a workload SLO before authorizing any storage benchmark |
| PCIe | Direct passthrough of compute function `10de:2c05` | 009 has negligible transfer volume; model profiles already ran on this path | gpu-cp reconciliation and gpu-compute deployment evidence | Negotiated current/max link speed and width were not retained in reviewed evidence |
| Driver/toolkit | Historical driver 610.57.04; CUDA toolkit 13.3.73; `sm_120` compilation passed | 009 requires the reviewed profile minimums and exact script checks | gpu-cp runtime acceptance | Current loaded driver/toolkit and script/profile hashes must be verified |
| Model runtime | Patched Ollama 0.32.0 and llama.cpp b10173 historically accepted | Irrelevant to 009; exact accepted runtime required for later model work | gpu-compute state and gpu-cp profiles | Current service/version state unknown; it must not be changed for 009 |
| Concurrency | Only one request at a time was evidenced by the reviewed profiles | 009: exactly one invocation; intended model concurrency is one unless separately accepted | Acceptance records and 009 packet | More than one model request is unsupported, not merely unmeasured capacity |

VRAM headroom figures are arithmetic differences from the reported 16,303 MiB
total, not new measurements. Idle utilization is intentionally not used as a
capacity claim.

## Scoped conclusion

- **Work Entry 009:** sufficient on the historically accepted configuration;
  current readiness is not yet measurable until its identity/resource preflight.
- **Single Qwen2.5-Coder 14B Q4 at context 4096:** historically sufficient with
  6,999 MiB reported VRAM headroom and no CPU offload.
- **Single accepted 24B/30B/32B profiles at context 4096:** historically workable
  only in their exact partial-offload envelopes; near-VRAM-limit behavior is not
  evidence for higher concurrency or larger context.
- **Qwen3.5 9B QLoRA:** not yet measurable. The prior attempt stopped at the
  exposed CPU/software compatibility boundary before any batch, overfit or GPU
  fit measurement.

## Prioritized recommendations

1. **Authorize one 009 run, not a separate resource benchmark.** Its preflight
   collects current CPU, RAM, swap, filesystem, GPU, driver and PCIe-link facts,
   and its postflight confirms the tiny kernel completed and cleaned up.
   Expected benefit: closes current-readiness unknowns at negligible workload
   scale. Incremental cost: none.
2. **Keep inference concurrency at one and prefer the accepted 14B/4096 profile
   for a later model pilot.** Expected benefit: uses owned equipment with the
   largest evidenced VRAM margin and avoids an unsupported orchestration change.
   Incremental cost: none.
3. **Treat 24B/30B/32B as exact-profile partial-offload options, not spare
   capacity.** Do not raise context or concurrency without a separately admitted
   measurement because their reported VRAM headroom is only 1,413–1,669 MiB.
4. **Resolve the VM CPU exposure/software compatibility contract before another
   QLoRA fit probe.** First determine whether an already supported CPU model or
   compatible software stack exists; do not add RAM, swap or a GPU on speculation.

No hardware purchase or recurring service is recommended. Consequently, no
price lookup is relevant at this stage. Resource reallocation is also
unjustified before the coordinated measurement identifies a real bottleneck.

## Coordinated measurement packet

The concrete packet is
[rtx5070ti-execution-pilot.md](rtx5070ti-execution-pilot.md). After separate
live authorization, first run the following read-only block through an existing
operator-managed Proxmox session to `hv-katra`. The authorization must name the
session and acting principal; this record does not create host access.

```bash
set -Eeuo pipefail
test "$(hostname -s)" = "hv-katra"
pveversion --verbose
lscpu
free -b
swapon --show --bytes
pvesm status
vm_status=$(qm status 320)
printf '%s\n' "$vm_status"
test "$vm_status" = "status: running"
vm_safe=$(qm config 320 | awk -F ': ' '$1 ~ /^(name|cores|memory|balloon|cpu|hostpci0|scsi0|scsi1|ostype)$/{print}')
printf '%s\n' "$vm_safe"
grep -Fxq 'name: cuda-compute-katra' <<<"$vm_safe"
grep -Fxq 'cores: 8' <<<"$vm_safe"
grep -Fxq 'memory: 16384' <<<"$vm_safe"
grep -Eq '^hostpci0: .*01:00\.0' <<<"$vm_safe"
grep -Eq '^scsi0: ' <<<"$vm_safe"
grep -Eq '^scsi1: ' <<<"$vm_safe"
pci_state=$(lspci -nnk -s 01:00.0)
printf '%s\n' "$pci_state"
grep -Fq '10de:2c05' <<<"$pci_state"
grep -Fq 'Kernel driver in use: vfio-pci' <<<"$pci_state"
```

Host preflight block SHA-256:
`3ea2dab2d641394a635ec39cdc21e22528fdd313d1d1384ac404c0aba9a83a0d`
for the UTF-8 fenced contents including the final newline. A target mismatch,
missing VM,
non-running VM, missing passthrough mapping, or allocation other than the
accepted 8 vCPU/16,384 MiB stops the packet before guest execution. Do not
change the VM or host in response.

Then run the linked 009 guest block once in the named normal-user guest session.
The limits are one kernel launch, TERM at 120 seconds, KILL after a 10-second
grace, no retry, no model, no installation, no network operation by the
workload, and transient files only under its task-owned `/tmp` directory. These
two preflight/execution phases are one measurement packet and one GPU workload.

Capture these 010 fields from the same receipt:

- hypervisor CPU/RAM/swap, storage-pool status, safe VM allocation fields and
  passthrough binding;
- guest hostname, `nproc`, CPU model/flags and virtualization presentation;
- total/available RAM and swap;
- filesystem identity, total and free bytes for `/`, `/tmp` and `/mnt/models`;
- GPU name, PCI bus ID, total/used VRAM, compute capability, driver, temperature
  and power before and after;
- current/max PCIe link speed and width;
- exact script/profile hashes, elapsed time, timeout/exit state, returned value
  and cleanup result.

Stop before the kernel if identity, hashes, storage reserve, metric availability
or authority differs. During execution, TERM at 120 seconds; do not retry. The
packet's exit trap removes its task-owned temporary directory on success,
failure or signal. A nonzero status, timeout, cleanup failure, XID/CUDA error,
unexpected resource pressure or missing postflight is a failed measurement and
does not authorize repair or reconfiguration.

Live effects during assessment: NONE.
