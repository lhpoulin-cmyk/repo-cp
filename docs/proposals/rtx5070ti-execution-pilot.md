# RTX 5070 Ti bounded execution pilot packet

Status: prepared for review; execution unauthorized and not performed.

## Fixed objective

Prove one actual CUDA kernel executes on the intended RTX 5070 Ti inside VM 320,
without invoking a model or changing runtime configuration. The existing
gpu-compute smoke implementation is reused verbatim.

| Field | Fixed value |
| --- | --- |
| Physical host | `hv-katra` |
| Execution target | VM 320, `cuda-compute-katra` |
| Accelerator | NVIDIA GeForce RTX 5070 Ti, PCI ID `10de:2c05`, guest PCI `0000:01:00.0` |
| Implementation source | `gpu-compute` commit `c1d001a8f19ff4108d303f4529dde276e39f8253` |
| Script | `/srv/gpu-compute/tests/smoke/cuda-nvidia` |
| Reviewed script SHA-256 | `dfd7865e6f030a087633d89aca0e89bfc5086326eefb2bd03b9ff232ac3453f8` |
| Fallback profile SHA-256 | `d7ab8ef9d30e2edc505e5f58088f9dff4571c4b7a698892520599554bddd75f7` |
| Command block SHA-256 | `257e4b204ae81abd3a1e3dc6980aed6ca80f81293af9d18adba1bfacb38be259` (UTF-8 fenced contents with final newline) |
| Invocation count | exactly one |
| Wall limit | 120 seconds, then TERM; KILL after a 10-second grace; no automatic retry |
| Model/tool/network use | no model; no model-facing tools; no network operation by the workload |

The script checks GPU identity, capability 12.0, device nodes, CUDA 13.3,
minimum driver, Vulkan, libcuda and llama.cpp device visibility. It then compiles
one kernel, allocates four device bytes, writes integer `42` with one thread,
copies it back, verifies the value and reports the runtime device identity.

## Admission sequence

1. Recheck the exact repo-cp Work Entry 009 record and canonical revisions.
2. Obtain a new operator authorization naming this packet, the operator-managed
   guest session, actual executor/principal, target VM and evidence destination.
3. Use gpu-cp's accepted hardware/runtime boundary and gpu-compute's script
   identity as the qualified target evidence. Do not apply Work Entry 005's
   text-generation-only schema to this CUDA workload.
4. Run the read-only identity/resource preflight. Any mismatch is a terminal
   refusal; it is not authorization to repair or reconfigure the appliance.
5. Execute exactly one bounded smoke invocation. There is no retry or fallback.

## Exact commands after authorization

Session establishment is deliberately not invented here. The authorization must
identify an existing operator-managed normal-user guest session to
`cuda-compute-katra`; the Ollama-forward and telemetry-only identities are not
shells. Once inside the verified guest, run this exact command block:

```bash
set -Eeuo pipefail
test "$(hostname -s)" = "cuda-compute-katra"
test -d /srv/gpu-compute/.git
cd /srv/gpu-compute

test "$(sha256sum tests/smoke/cuda-nvidia | awk '{print $1}')" = \
  "dfd7865e6f030a087633d89aca0e89bfc5086326eefb2bd03b9ff232ac3453f8"
test "$(sha256sum config/profiles/nvidia-rtx5070ti/profile.yaml | awk '{print $1}')" = \
  "d7ab8ef9d30e2edc505e5f58088f9dff4571c4b7a698892520599554bddd75f7"

hostname -s
nproc
lscpu
free -b
swapon --show --bytes
findmnt --target /
findmnt --target /tmp
findmnt --target /mnt/models
df -B1 / /tmp /mnt/models
nvidia-smi --query-gpu=name,pci.bus_id,driver_version,memory.total,compute_cap,temperature.gpu,power.draw --format=csv,noheader
for field in current_link_speed current_link_width max_link_speed max_link_width; do
  printf '%s=' "$field"
  cat "/sys/bus/pci/devices/0000:01:00.0/$field"
done

pilot_tmp=$(mktemp -d /tmp/helix-work-entry-009.XXXXXX)
cleanup() { rm -rf -- "$pilot_tmp"; }
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
if TMPDIR="$pilot_tmp" timeout --signal=TERM --kill-after=10s 120s tests/smoke/cuda-nvidia; then
  smoke_status=0
else
  smoke_status=$?
fi
printf 'smoke_exit=%s\n' "$smoke_status"
nvidia-smi --query-gpu=name,pci.bus_id,driver_version,memory.total,memory.used,compute_cap,temperature.gpu,power.draw --format=csv,noheader
cleanup
test ! -e "$pilot_tmp"
trap - EXIT HUP INT TERM
printf 'cleanup=PASS\n'
exit "$smoke_status"
```

The outer task-owned temporary directory makes cleanup independent of the smoke
script's inner `mktemp`. A timeout, forced termination, signal, nonzero status,
identity mismatch, missing metric or cleanup failure is a failed pilot. Do not
retry, install,
change a profile, enable CPU fallback or switch devices.

## Evidence return

Return a sanitized receipt containing:

- Work Entry `009`, packet revision and authorization reference;
- actual executor, acting principal and session mechanism, never inferred from
  Git headers or the machine hostname;
- start/end UTC timestamps, target hostname and command block SHA-256;
- preflight and postflight output hashes, exit status and timeout status;
- runtime-reported GPU name/capability and kernel value `42` verification from
  the fixed script identity plus its compiled-kernel `PASS` result;
- observed CPU/RAM/swap/storage/PCIe/driver/runtime fields for Work Entry 010;
- cleanup result and confirmation that no model, install, service or config
  action occurred.

Success requires exact target identity, all smoke checks `PASS`, kernel value
`42`, capability `12.0`, status zero within 120 seconds, and verified cleanup.
Any other outcome is failure or `UNKNOWN`; metadata-only checks never become
execution proof.

## Anticipated effects and authorization needed

Anticipated live effects are one CUDA compilation and kernel invocation, transient
files only under a task-owned `/tmp` directory, brief GPU compute/VRAM/power use,
and read-only system queries. No model, network call, service change, persistent
runtime state or repository write is intended.

Required authority is a separate explicit live-run authorization for exactly this
target, command block, executor/session and evidence path. This preparation record
does not supply it.

Live effects during preparation: NONE.
