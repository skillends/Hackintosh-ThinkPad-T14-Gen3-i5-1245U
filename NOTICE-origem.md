# Licensing notice

- **This repository is VostroXe, a modified version of
  [Hackintosh-XPS13Plus-IrisXe-Tahoe](https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe)** by
  JulioNectar, forked at commit `6f03560` and adapted to the Dell Vostro 3520. The changes are described in
  [docs/VOSTRO.md](docs/VOSTRO.md) and recorded in the git history.
- **This repository** (the NootedGreen fork in `src/`, the scripts, `macos/`, `tools/` except the libfprint patch noted
  below, and the documentation) is distributed under the **Thou Shalt Not Profit License 1.0** (see [LICENSE](LICENSE)),
  the license of the projects it derives from, [NootedGreen](https://github.com/sgiammori/NootedGreen) by StezzaPilot
  and the project above. Free to use, study, modify and share; not for profit. As section 17 of that license requires,
  VostroXe's author declares that VostroXe is not-for-profit and that he derives no revenue from distributing it or
  from support or services relating to it.
- **`tools/CS8409HDA/`** (the Vostro's audio driver) is this repository's own code, under the same license. Its codec
  programming reproduces the register writes the Linux `cs8409` and `cs42l42` drivers (Cirrus Logic, GPL-2.0) make on
  this laptop, recorded in `tools/CS8409HDA/ref/`.
- **`src/HookCase/`** is HookCase by Steven Michaud, as modified in the NootedGreen project, with two fixes from this
  repository (probePortMode NULL `callback`, strnstr signature). It is under the **MIT License**; see
  [src/LICENSE-HookCase](src/LICENSE-HookCase).
- **`src/MGL/`** is [MGL](https://github.com/openglonmetal/MGL) by Michael Larson and contributors (OpenGL 4.6 on
  Metal), imported at upstream commit `de0ded04` without its Xcode project, golden images and code generators. This
  repository's changes, which make it run on the Vostro's GPU, are listed in [docs/OPENGL.md](docs/OPENGL.md) and
  marked in each changed file. MGL and these changes are under the **Apache License 2.0**
  ([src/MGL/LICENSE](src/MGL/LICENSE)). The GLFW it bundles (`src/MGL/external/glfw/`, modified by the MGL project)
  is under the **zlib/libpng License** ([src/MGL/external/glfw/LICENSE.md](src/MGL/external/glfw/LICENSE.md)). Its
  build dependencies (SPIRV-Cross, SPIRV-Tools, SPIRV-Headers, glslang, OpenGL-Registry, ezxml) are not included:
  `src/MGL/external/clone_external.sh` downloads them.
- **Third-party components in `EFI/`** keep their own licenses: OpenCore, Lilu, WhateverGreen, VirtualSMC, NVMeFix,
  RestrictEvents, BrightnessKeys, CpuTopologyRebuild (acidanthera and contributors); VoodooI2C and VoodooPS2 (their
  authors); USBToolBox (dhinakg); XHCI-unsupported (RehabMan). See each project for its terms.
- **`EFI/OC/Kexts/RealtekRTL8111.kext`** is the unmodified v3.0.0 release of
  [Mieze/RTL8111_driver_for_OS_X](https://github.com/Mieze/RTL8111_driver_for_OS_X) (executable sha256
  `a9a99d10…`), under the **GNU General Public License v2.0 or later**
  ([licenses/GPL-2.0.txt](licenses/GPL-2.0.txt)). Corresponding source: tag `v3.0.0` of that repository.
- **`EFI/OC/Kexts/HoRNDIS.kext`** is the unmodified rel9.2 release of [jwise/HoRNDIS](https://github.com/jwise/HoRNDIS),
  taken from `HoRNDIS-9.2.pkg` (executable sha256 `a6dae833…`), under the **GNU General Public License v3.0**
  ([licenses/GPL-3.0.txt](licenses/GPL-3.0.txt)). Corresponding source: tag `rel9.2` of that repository.
- **`EFI/OC/Kexts/UTBMap.kext`** is the USB port map of the Dell Vostro 3520 for USBToolBox, made for this repository.
- **`EFI/OC/Kexts/NootedGreen.kext`** and **`EFI/OC/Kexts/CS8409HDA.kext`** are built from `src/NootedGreen` and
  `tools/CS8409HDA` of this repository.
- **Intel SOF audio firmware and topology are not included.** The speaker driver (`tools/AudShim`) is built against
  files you download from the official sof-bin release; `tools/AudShim/AudShimData.h`, which would contain the firmware,
  is generated locally and excluded from the repository. The firmware is distributed by Intel under its own licence
  (`LICENCE.Intel` in sof-bin).
- **libfprint, glib, libgusb and libusb are not included.** `tools/fingerprint/build.sh` downloads them from upstream
  (libfprint commit `6f9479c3`, glib 2.84.4, libgusb 0.3.10, libusb 1.0.29) and builds them locally. All four are
  under the **GNU Lesser General Public License v2.1 or later** ([licenses/LGPL-2.1.txt](licenses/LGPL-2.1.txt)).
  `tools/fingerprint/xefp-libfprint-macos.patch` modifies libfprint and is distributed under the same LGPL-2.1-or-later
  terms; the other files in `tools/fingerprint/` (xe-fp, pam_xefp) are this repository's own code and only link
  dynamically against those libraries.
- **Apple software is not included.** The scripts patch your own copy of Apple's GPUDriversIntel 16.0.32 bundles at
  install time. Apple, macOS, Metal and related names are trademarks of Apple Inc.; this project is not affiliated
  with or endorsed by Apple, Intel or Dell.
