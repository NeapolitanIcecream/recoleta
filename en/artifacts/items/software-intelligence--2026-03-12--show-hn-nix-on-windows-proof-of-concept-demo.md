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
- reproducible-builds
- vm-image
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# Show HN: Nix on Windows –- proof-of-concept demo

## Summary
This is a proof of concept for bringing the **Nix package manager to Windows**: it offline-builds a bootable Windows ValidationOS image on Linux with a working Nix preinstalled. Its significance is that it shows Windows can be provided with a Nix environment in a fairly deterministic way, without a Windows installation workflow or Windows toolchain.

## Problem
- Target problem: how to **run Nix on Windows** while avoiding dependence on a full Windows installation, licensing, manual configuration, or native Windows build tools.
- This matters because Nix emphasizes reproducible, declarative software builds; if it can cover Windows, it can extend to cross-platform development, testing, and automated delivery scenarios.
- The specific obstacle is that ValidationOS lacks `shell32.dll`'s `SHGetKnownFolderPath`, which Nix requires, so Nix cannot run directly.

## Approach
- **Cross-compile** `nix.exe` and its dependencies on Linux using `pkgsCross.mingwW64`, with no Windows toolchain required at all.
- Based on Microsoft's free, lightweight **ValidationOS**, extract a VHDX from the ISO, then use `guestfish` and `chntpw` to **inject files and registry changes offline**, rather than starting a virtual machine during the build.
- Inject a startup script to disable the firewall, configure SSH keys, and modify Winlogon so `cmd.exe` starts in `C:\nix\bin` by default.
- To work around the missing `shell32.dll`, the author does not modify Nix itself, but instead provides a **minimal stub DLL** that implements only `SHGetKnownFolderPath`, returning paths by reading environment variables such as `LOCALAPPDATA`, `APPDATA`, and `ProgramData`.
- Place this stub DLL next to `nix.exe`, taking advantage of Windows DLL search order so it is loaded first, allowing Nix to work in this minimal Windows environment.

## Results
- Successfully builds and boots a ValidationOS Windows image of about **~1GB**, and the image **boots within seconds**; the article does not provide a stricter startup-time benchmark comparison.
- The entire image build process is claimed to be **deterministic**: the build **does not start a VM**, but instead modifies the disk image directly offline; however, the article does not provide reproducibility test figures or hash comparison results.
- In the demo, you can log into the Windows VM via **SSH** and run `C:\nix\bin\nix-build C:\demo.nix`, showing that the preinstalled Nix can actually run.
- The example derivation executes `echo Hello` via `cmd.exe` and writes the result into the **Nix store** as an end-to-end functional validation.
- No standard datasets, performance metrics, throughput, success rates, or quantitative comparisons against existing Windows Nix approaches are provided; the strongest concrete conclusion is: **Linux can offline-generate and boot a minimal Windows VM with Nix installed, and can execute Nix builds remotely.**

## Link
- [https://github.com/nix-windows/nix-windows-demo](https://github.com/nix-windows/nix-windows-demo)
