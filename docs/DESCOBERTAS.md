# Descobertas

Medições feitas em uma única máquina. Elas podem não valer para outras.

## Energia

Com 12 threads, o consumo subia a 36-45 W e caía para cerca de 15 W a 60 °C. A CPU informou `PL1` como motivo
(`MSR 0x64F`), mesmo com `MSR 0x610` em 64 W e PSys em 100 W. Lendo o MCHBAR ao vivo, o limite aparecia em 32/35 W,
20/20 W e, às vezes, 12 W.

Depois de `DYTC(0x12B001)` (modo desempenho, valor do `thinkpad_acpi` do Linux), o limite ficou estável nas leituras
seguintes, e 12 threads sustentaram cerca de 35 W por 30 s. A causa exata dos valores externos não foi provada; a
hipótese é o firmware da Lenovo sem os drivers térmicos do Windows.

## CPU

- `ctrsmt=off` deu 809 / 4823: o multi subiu, mas o single caiu muito.
- `cpus=4`, só com os núcleos de desempenho, ainda mostrou clock oscilando. Os núcleos de eficiência não explicam tudo.
- CPUFriend com o plano do iMac20,1 eliminou as quedas perto de 1 GHz na medição e levou a 1676 / 5795.
- Com 64 W, o limite no multi passou a ser térmico, chegando a 98 °C. O Windows também chegou a 100 °C.

## HDMI

No T14, a porta responde como `ddi = 1`, como no Dell Vostro 3520.

Ao tirar o cabo, o `GMBUS2` ficava preso (`0x8200`, `0x8a00`) e nem STOP nem reset o soltavam: 133 tentativas, 0
sucessos. A última operação registrada era uma escrita do driver da Apple no endereço `0x74` (HDCP). Ao responder a
esse endereço sem tocar no barramento, o `lightups` passou a 2, a imagem voltou e não houve mais recuperações.

## Áudio

- Alto-falante baixo era o volume nos Ajustes, diferente da barra de menus.
- Som abafado no fone era o modo de chamada (8 kHz, mono), porque a entrada escolhida era o microfone do fone.
- Preferências de `bluetoothaudiod` foram ajustadas e o som melhorou, mas o codec observado antes do ajuste era SBC e
  o resultado final não foi medido.
- A tabela NHLT confirma microfone digital de 2 canais no DSP. A escolha de `PDM0` veio do `ts_group` e foi validada
  pelo uso real.
