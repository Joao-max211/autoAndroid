# autoAndroid
O autoAndroid é um projeto feito totalmente em python criado com o objetivo de criar automações simples para o Android

## 🛠️ Tecnologias
- Python 3.10+
- ADB (Android Debug Bridge)
- Bibliotecas Python: subprocess, os, time
## 📋 Requisitos
- ADB
- Python 3.10+
### 🔧 Instalação do ADB
https://developer.android.com/tools/releases/platform-tools
### ADB documentação
https://developer.android.com/tools/adb?hl=pt-br
## 🎮 Modo de uso
- AVISO: Certifique se o adb esta conectado ao aparelho:
  ```bash
   adb devices
- Importe o modulo autoAndroid e crie um objeto da classe AutoAndroid()
  ```python
  import autoAndroid
  
  bot = autoAndroid.AutoAndroid() # <- Objeto resposavel por executar os comandos
- Simulando toques na tela
  ```python
  #Usando posições obsolutas
  x_abs = 500
  y_abs = 650
  bot.tap(x_abs, y_abs)
  #Usando posições relativas
  lag_tela, alt_tela = bot.width, bot.height
  x_rel = x_abs / lag_tela
  y_rel = y_abs / alt_tela
  bot.tap(x_rel, y_rel)
- Simulanto a digitação de texto
  ```python
  msg = 'Ola' # <- É importante que a mensagem não tenham espaços
  bot.text(msg)
- Pegando coordenadas de toques
  ```python
  #Toques unicos
  x, y =  bot.getXY() # <- Aguarda o usuario da um clique unico para retornar as coordenadas
  print(x, y)
  #Toques dublos
  x, y = bot.getXY(DoubleClick=True) # <- Aguarda o usuario da dois cliques para retornar as coordenadas
  print(x, y)
