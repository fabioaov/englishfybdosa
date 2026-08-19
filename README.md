# Englishfy BDO SA

Simples script para alterar o idioma do client do Black Desert SA para inglês.

Credits to [Shad0wtrance](https://www.reddit.com/r/blackdesertonline/comments/p8vjss/guide_all_your_bdo_language_file_needs/).

## Como usar

1. Faça o download do arquivo [Englishfy_BDO_SA.exe](https://github.com/fabioaov/englishfybdosa/releases)
2. Execute-o
3. Escolha a ação desejada:
   - **Aplicar Inglês**: Escolha o idioma (PT ou ES), selecione a pasta raiz do Black Desert (ex.: `C:\BlackDesert`) e aguarde a conclusão.
   - **Restaurar Idioma Original**: Selecione a pasta raiz do jogo para restaurar o backup original.

**Repita os passos após a manutenção semanal.**

## Rodar pelo código-fonte

Caso não queira usar o `.exe`, rode direto pelo Python (3.8+):

```bash
pip install -r requirements.txt
python app.py
```

O aplicativo exibirá uma interface para aplicar o idioma inglês ou restaurar o idioma original a partir do backup (`backup_languagedata_*.loc`).

