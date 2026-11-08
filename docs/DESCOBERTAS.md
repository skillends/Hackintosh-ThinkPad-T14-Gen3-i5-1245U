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
- No Windows (HWiNFO), com 1 tarefa, os núcleos P ficam em 4,0–4,4 GHz e os E em 3,3 GHz.
- O XCPM grava em `IA32_HWP_REQUEST` um "desired" escolhido por ele (de 13 a 44 entre os núcleos, ou 1,3 a 4,4 GHz) e
  trocou a razão quase 1 milhão de vezes desde o boot. Zerando o desired (HWP autônomo, `debug.xepm.hwp_auto`), a
  mediana de 1 tarefa foi de 3,0 para 3,95 GHz, e o Geekbench de 1634 / 6597 para 1811 / 7252.
- `ctrsmt=full` sozinho levou de 1676 / 5795 para 1634 / 6597: multi +14%, single igual.
- Com o CpuTopologyRebuild, o trabalho de fundo (WindowServer, kernel) fica na primeira thread dos núcleos P e os E
  quase parados. O kernel_task gasta 15–28% de CPU com a máquina quase parada; a causa não foi investigada.
- A leitura `debug.xepm.gpu` mostrou RP0 1.200 MHz, a GPU a 1.150–1.200 MHz quando trabalha e 81% do tempo em repouso
  (RC6) parada. O piso de frequência (XE-GTFREQ) funciona neste modelo.
- A leitura `debug.xepm.sensors` (usada por `sensores.py`) travou duas vezes num mesmo boot; a causa não foi investigada.

## HDMI

No T14, a porta responde como `ddi = 1`, como no Dell Vostro 3520.

Ao tirar o cabo, o `GMBUS2` ficava preso (`0x8200`, `0x8a00`) e nem STOP nem reset o soltavam: 133 tentativas, 0
sucessos. A última operação registrada era uma escrita do driver da Apple no endereço `0x74` (HDCP). Ao responder a
esse endereço sem tocar no barramento, o `lightups` passou a 2, a imagem voltou e não houve mais recuperações.

### Boot sem cabo

Depois dessa correção, o boot sem cabo travou: o AUX do eDP (`ddi = 0`) deu cerca de 720 timeouts,
`FB0: Failed to read EDID 0xe00002d6`, e a tela interna não acendeu. Com o cabo, nenhum timeout. Boots anteriores, que
parecem ter sido feitos sem cabo, não tinham a falha. O único código novo que dependia do cabo era a resposta imediata
do GMBUS com HPD baixo.

Essa resposta agora só vale depois de um AUX bom no eDP. No boot seguinte sem cabo foram 0 timeouts, e a recuperação de
energia também incluída no kext não precisou agir. A ligação exata entre o GMBUS e o AUX do eDP não foi explicada. Um
travamento geral aos 35 s (`Ticket spinlock`) apareceu em uma das tentativas, sem causa provada.

## Áudio

- Alto-falante baixo era o volume nos Ajustes, diferente da barra de menus.
- Som abafado no fone era o modo de chamada (8 kHz, mono), porque a entrada escolhida era o microfone do fone.
- Preferências de `bluetoothaudiod` foram ajustadas e o som melhorou, mas o codec observado antes do ajuste era SBC e
  o resultado final não foi medido.
- A tabela NHLT confirma microfone digital de 2 canais no DSP. A escolha de `PDM0` veio do `ts_group` e foi validada
  pelo uso real.
