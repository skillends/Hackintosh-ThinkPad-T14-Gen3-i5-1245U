# Hackintosh ThinkPad T14 Gen 3 i5-1245U (Alder Lake, Iris Xe)

macOS Tahoe 26.7.2 com OpenCore e aceleração gráfica Metal na Intel Iris Xe 46A8, em um Lenovo ThinkPad T14 Gen 3
(21AJ) com i5-1245U. Inclui EFI, HDMI, áudio ALC257, microfone interno, Wi-Fi e Bluetooth AX211.

*English summary:* macOS Tahoe on a Lenovo ThinkPad T14 Gen 3 (Intel Core i5-1245U, Alder Lake) with OpenCore: Iris Xe
Metal acceleration, HDMI with replug, ALC257 audio, internal DMIC microphone, battery and AX211 Wi-Fi and Bluetooth.

> **Projeto experimental, sem garantia.** Mexe em firmware, kexts e limites de energia. Faça backup e mantenha um
> pendrive de boot. Testado em uma única máquina.

## Hardware testado

| Componente | Modelo |
|---|---|
| Notebook | Lenovo 21AJSF7U00 |
| CPU | Intel Core i5-1245U (2P + 8E, 12 threads) |
| GPU | Intel Iris Xe 46A8, 80 EU |
| Áudio | Realtek ALC257, controlador 8086:51C8, subsistema 17AA:22E8 |
| Wi-Fi e Bluetooth | Intel AX211 |
| SMBIOS | MacBookPro16,2 |

## O que funciona

| Item | Situação |
|---|---|
| Aceleração gráfica | ✅ Metal |
| Tela interna | ✅ 1920x1200 |
| HDMI | ✅ Testado a 2560x1080, 60 Hz, inclusive ao reconectar o cabo. Sem áudio HDMI |
| Alto-falantes e fone | ✅ SimpleHDA + AppleALC, layout 11 |
| Microfone interno | ✅ Driver experimental; veja [docs/MICROFONE.md](docs/MICROFONE.md) |
| Câmera | ✅ USB |
| Bateria | ✅ ECEnabler |
| Wi-Fi | ✅ AirportItlwm |
| Bluetooth | ⚠️ Funciona, com falhas ocasionais; o fone pode cair em modo de chamada |
| Trackpad | ⚠️ Polling, com engasgo leve |
| USB-C DP, HDCP e suspensão | ❌ ou não testados |

## Desempenho

Geekbench 7, CPU, na mesma máquina:

| Configuração | Single | Multi |
|---|---|---|
| Windows | 1963 | 7270 |
| macOS, início | 1334 | 3968 |
| **macOS, configuração atual** | **1676** | **5795** |

Geekbench Metal registrado no início do projeto: 1635.

## O que desenvolvemos aqui

- **HDMI ao reconectar:** o driver da Apple tentava HDCP (endereço I2C 0x74) na porta, o GMBUS ficava preso e o monitor
  não voltava. O kext agora responde a isso sem usar o barramento. O vídeo protegido no monitor externo pode ser afetado.
- **Queda de energia:** sem os drivers térmicos do Windows, o limite de energia oscilava. O kext aciona o modo
  desempenho da Lenovo (`DYTC 0x12B001`) e mantém os limites.
- **Plano de frequência:** CPUFriend com o plano do iMac20,1, gerado a partir do próprio sistema.
- **Microfone:** adaptação de um driver SOF para o subsistema do T14, usando `PDM0`.

Detalhes em [docs/DESCOBERTAS.md](docs/DESCOBERTAS.md). As alterações estão em [patches](patches).

## Como usar

1. Instale o macOS Tahoe. O config usa `EnableJumpstart` para o APFS; o driver da Apple não está incluído. O sistema testado é o 26.7.2 (25G332); o projeto de origem foi feito para o 26.7.1 (25G241).
2. Gere um SMBIOS próprio com [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) para `MacBookPro16,2` e preencha
   `SystemSerialNumber`, `MLB`, `ROM` e `SystemUUID` no `EFI/OC/config.plist`. **Nunca reutilize valores de outra pessoa.**
3. Instale os drivers Metal e kexts do sistema com o `install.sh` do
   [projeto base](https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe). Eles usam binários que não são
   distribuídos aqui. Em build diferente de 25G241, ele exige `XE_FORCE=1`, por sua conta e risco.
4. Se precisar instalar o macOS ou usar disco HFS+, adicione `HfsPlus.efi` de
   [OcBinaryData](https://github.com/acidanthera/OcBinaryData) e ative a entrada no config. Ele não é distribuído aqui.
5. Teste primeiro por pendrive, antes de copiar a EFI para o SSD.
6. Veja os cuidados em [docs/CUIDADOS.md](docs/CUIDADOS.md).

Esta EFI é específica do T14 Gen 3: o mapa de USB, ACPI e boot-args podem não servir em outro modelo.

## Créditos

- [JulioNectar](https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe): aceleração da Iris Xe
- [henriquejsza](https://github.com/henriquejsza/VostroXe): HDMI em Alder Lake-U
- [MarkPLacer](https://github.com/MarkPLacer/RazerSSTMicrophone): driver de microfone
- [laobamac](https://github.com/laobamac/SimpleHDA): SimpleHDA e AirportItlwm para Tahoe
- [b00t0x](https://github.com/b00t0x/CpuTopologyRebuild): CpuTopologyRebuild
- [Acidanthera](https://github.com/acidanthera): OpenCore, Lilu, AppleALC, WhateverGreen, VirtualSMC, CPUFriend
- [1Revenger1](https://github.com/1Revenger1/ECEnabler): ECEnabler
- OpenIntelWireless, VoodooI2C e USBToolBox

Desenvolvido por um usuário do T14 com a ajuda do Claude.

## Licença

Cada componente mantém a própria licença. O NootedGreen e as alterações derivadas seguem a **Thou Shalt Not Profit
License 1.0**, sem uso comercial; veja [LICENSE](LICENSE) e [NOTICE.md](NOTICE.md). Não há binários da Apple neste
repositório, nem firmware SOF.
