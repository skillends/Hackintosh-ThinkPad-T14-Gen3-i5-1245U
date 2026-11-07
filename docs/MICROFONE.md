# Microfone interno

O microfone é digital e fica no DSP da Intel, por isso o AppleALC não o alcança. A solução adapta o
[RazerSSTMicrophone](https://github.com/MarkPLacer/RazerSSTMicrophone), que usa o mesmo controlador `8086:51C8`.

**Experimental.** É um driver de kernel. O autor original relata um congelamento ao acordar da suspensão, sem causa
definida.

## Instalação

```sh
git clone https://github.com/MarkPLacer/RazerSSTMicrophone.git
cd RazerSSTMicrophone
git checkout 17cff4e
git apply /caminho/para/patches/razer-sst-t14-gen3.diff
python3 tools/fetch-dependencies.py
./Test.command
./Build.command
```

O `fetch-dependencies.py` baixa e confere o firmware da Intel. Ele não é distribuído aqui.

Depois, instale `build/RazerSSTMicrophone.kext` em `/Library/Extensions`, ajuste o dono para `root:wheel`, registre o kext
com `kmutil load -z` junto com os outros kexts auxiliares e reinicie. Leia antes o `docs/INSTALL.md` do projeto original.

## Uso

O driver fica parado até ser publicado:

```sh
sudo build/publish
```

Publique alguns minutos depois do boot. O nome pode aparecer como `Razer PDM1 internal microphone capture`.

Com `amfi_get_out_of_my_way`, pode ser necessário registrar a permissão de microfone manualmente em cada app.

## Se ficar mudo

Troque `physical_pdm_controller` para `1` em `hardware/thinkpad-t14-gen3.json`, recompile e instale de novo. A BIOS do
T14 ativa as duas linhas, e aqui funcionou com `0`.
