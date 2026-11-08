# Cuidados

- **Não atualize o macOS** sem testar por pendrive antes. Desligue as atualizações automáticas.
- **Mantenha um pendrive de boot** e faça backup da EFI antes de qualquer mudança.
- **Calor:** com `ngreenpm=64`, a CPU pode chegar perto de 100 °C em carga pesada. A proteção do kext atua em 98 °C.
  Para menos calor, teste `ngreenpm=28` e `ngreenpmpl2=35`.
- **HWP autônomo (`ngreenpmauto=1`):** o consumo e a temperatura em uso leve não foram medidos e podem subir. Para
  desligar sem reiniciar: `sudo sysctl -w debug.xepm.hwp_auto=0`; de vez, tire `ngreenpmauto=1` dos boot-args.
- **`sensores.py`:** a leitura de temperatura do kext travou duas vezes num mesmo boot. Prefira `cpu-gpu.py`, que não
  depende dela.
- **Não use `powermetrics --samplers gpu_power,cpu_power`:** o sistema travou logo depois desse comando nesta máquina.
  A causa não foi provada.
- **`amfi_get_out_of_my_way` / `ngreenlv`:** apps de terceiros podem não receber o pedido de permissão do microfone.
- **Bluetooth em dual boot:** o mesmo fone pareado em dois sistemas pode exigir novo pareamento ao trocar de sistema.
- **Suspensão:** pouco testada. O autor do driver de microfone relata um congelamento ao acordar.
- **Boot:** sem `-v`, erros não aparecem na tela. Para diagnosticar, adicione `-v` aos boot-args.
- **Windows:** entre pelo Windows Boot Manager, no F12, e não pelo menu do OpenCore.
