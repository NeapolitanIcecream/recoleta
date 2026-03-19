---
source: hn
url: https://github.com/nix-windows/nix-windows-demo
published_at: '2026-03-12T23:58:52'
authors:
- Ericson2314
topics:
- nix
- windows
- cross-compilation
- deterministic-builds
- virtual-machine
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: Nix on Windows –- proof-of-concept demo

## Summary
This is a proof of concept for offline building and booting a Windows ValidationOS virtual machine with Nix preinstalled on Linux. It demonstrates that Nix can run in a Windows environment deterministically without requiring a Windows license or Windows toolchain.

## Problem
- The problem this work addresses is how to bring Nix to Windows and get a minimally usable workflow running **without relying on a native Windows installation, license, or build tools**.
- This matters because Nix's value for cross-platform reproducible builds is high, but Windows environments are usually harder to automate, harder to customize offline, and more dependent on proprietary installation workflows.
- An additional obstacle is that ValidationOS lacks `shell32.dll`, while Nix depends on `SHGetKnownFolderPath` in it to locate directories such as `AppData` and `ProgramData`.

## Approach
- The core method is simple: **cross-compile** Nix for Windows on Linux, then **inject it directly** into a free, lightweight Windows ValidationOS disk image and boot it with QEMU.
- The build process is **deterministic**: no VM is started during the build phase; instead, `guestfish` directly modifies the contents of the VHDX/disk image.
- Offline image customization includes injecting a startup script, disabling the firewall, configuring SSH keys, and modifying the Winlogon registry so that `cmd.exe` starts in `C:\nix\bin`.
- To work around the missing `shell32.dll`, the project provides a minimal **stub DLL** that implements only the `SHGetKnownFolderPath` needed by Nix, returning directory paths by reading environment variables; this DLL is placed alongside `nix.exe` to take advantage of the Windows DLL search order.
- Both Nix and the stub DLL are cross-compiled on Linux using MinGW (`pkgsCross.mingwW64`), and the entire image preparation process requires no Windows tools.

## Results
- Successfully builds and boots a Windows ValidationOS image of about **~1GB**, which the text says can **boot within seconds**.
- Successfully logs in over SSH and runs Nix on Windows: the example command `C:\nix\bin\nix-build C:\demo.nix` executes `echo Hello` and writes the result into the Nix store.
- Claims that the entire workflow **requires no Windows license or installation**, and is **completed entirely on Linux**, including cross-compilation and disk image preparation.
- Claims the build is **deterministic** because no VM is started during the build; files are injected offline into the disk image instead.
- Does not provide standard academic benchmarks, error rates, throughput, or quantitative comparisons with other Windows Nix approaches.

## Link
- [https://github.com/nix-windows/nix-windows-demo](https://github.com/nix-windows/nix-windows-demo)
