import subprocess
from time import time


class AutoAndroid:
    def __init__(self):
        self.width, self.height = self.getWindowSize()
        self.max_x, self.max_y = self.getMaxXY()

    #Toca na tela nas cordenadas absolutas/relativas x e y
    def tap(self, X:int | float, Y:int | float) -> None:
        if isinstance(X, float) and isinstance(Y, float):
            x, y  = self.width * X, self.height * Y
        else:
             x, y = X, Y 
        subprocess.run(['adb', 'shell', 'input', 'tap', f'{x}', f'{y}'])

    #Digite uma mensagem
    def text(self, msg:str) -> None:
        subprocess.run(['adb', 'shell', 'input', 'text', msg])

    #Pega as cordenadas de onde o usuario clicou uma ou duas vezes
    def getXY(self, DoubleClick:bool=False) -> list[int]:
        x = y = last_click = 0
        try:
            proc = subprocess.Popen(['adb', 'shell', 'getevent', '-l'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            for line in proc.stdout:
                if 'ABS_MT_POSITION_X' in line:
                    x = int(line.split(' ')[12], 16)
                if 'ABS_MT_POSITION_Y' in line:
                    y = int(line.split(' ')[12], 16)
                if DoubleClick:
                    if 'BTN_TOUCH' in line and 'DOWN' in line:
                        current_click = time()
                        if current_click - last_click < 0.5:
                            print('DoubleCLick')
                            break
                        last_click = current_click
                else:
                    if x > 0 and y > 0:
                        break
            #Verifica se a coordenadas estao dentro da limite da tela
            if x > self.width and y > self.height:
                x, y =  map(int, [x / self.max_x * self.width, y / self.max_y * self.height])
            return [x, y]
        except Exception as err:
            raise RuntimeError(f'Falha ao pegar as coodernadas do clique: {err}')
        finally:
            proc.terminate()
            proc.wait()

    #Pegar tamanho da tela
    def getWindowSize(self) -> list[int]:
        try:
            size = subprocess.check_output(['adb', 'shell', 'wm', 'size'], text=True)
            size = size.split(' ')[-1]
            size = size.replace('\n', '')
            size = size.split('x')
            return map(int, size)
        except Exception as err:
            raise RuntimeError(f'Falha ao pegar tamanho da tela: {err}')

    #Pegar larguara e altura maxima da tela
    def getMaxXY(self) -> list[int]:
        x_max = y_max = 0
        try:
            proc = subprocess.Popen(['adb', 'shell', 'getevent', '-lp'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            for line in proc.stdout:
                if 'ABS_MT_POSITION_X' in line:
                    x_max = line.split(',')[2].split(' ')[-1]
                if 'ABS_MT_POSITION_Y' in line:
                    y_max = line.split(',')[2].split(' ')[-1]
                    return map(int, [x_max, y_max])
        except Exception as err:
            raise RuntimeError(f'Falha ao pegar altura e largura maxima do aparelho: {err}')
        finally:
            proc.terminate()
            proc.wait()

