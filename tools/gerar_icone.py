"""Desenha o icone do Cabo de Guerra e os tamanhos que o iPhone precisa.

A divisa entre as duas metades e serrilhada de proposito: duas metades lisas
divididas no meio sao a cara de logo de pizzaria/refrigerante, e a serrilha da
a ideia de duas forcas presas uma na outra, que e o que o jogo e.

Sao gerados tres arquivos:
  src/assets/icon.png   1024  — e daqui que o Flet tira o icone do app
  arte/icone_120.png     120  — AppIcon60x60@2x
  arte/icone_180.png     180  — AppIcon60x60@3x, que o Flet NAO gera sozinho

Sem o @3x o iPhone estica o de 120 para 180 e o icone sai borrado. O ios.yml
copia esses dois para dentro do .app na hora de empacotar.

Aqui a arte e geometria chapada, entao cada tamanho e desenhado direto no seu
proprio tamanho — nao ha pixel art para preservar, como no Vale do Girassol.

Rodar (na pasta do projeto):  python tools/gerar_icone.py
                              (precisa do pygame: pip install pygame)
"""
import os

import pygame

VERMELHO = (211, 47, 47)
AZUL = (25, 118, 210)
BRANCO = (255, 255, 255)
DENTES = 4          # quantas pontas tem a serrilha
AMP = 0.085         # altura da serrilha, em fracao do lado
BARRA = 0.40        # comprimento dos sinais, em fracao do lado
ESPESSURA = 0.055   # espessura dos sinais, em fracao do lado


def desenhar(lado):
    s = pygame.Surface((lado, lado))     # sem alpha: o iOS exige opaco
    s.fill(VERMELHO)

    meio, amp = lado // 2, lado * AMP
    serra = [(i * lado / DENTES, meio + (amp if i % 2 else -amp))
             for i in range(DENTES + 1)]
    # canto inferior esquerdo, canto inferior direito, e volta pela serrilha da
    # direita para a esquerda. Na ordem trocada o poligono se cruza e vira laco.
    pygame.draw.polygon(s, AZUL, [(0, lado), (lado, lado)] + serra[::-1])

    esp, barra = max(2, round(lado * ESPESSURA)), round(lado * BARRA)
    ym, ya = meio // 2, meio + meio // 2
    pygame.draw.rect(s, BRANCO, (lado//2 - barra//2, ym - esp//2, barra, esp))
    pygame.draw.rect(s, BRANCO, (lado//2 - barra//2, ya - esp//2, barra, esp))
    pygame.draw.rect(s, BRANCO, (lado//2 - esp//2, ya - barra//2, esp, barra))
    return s


def main():
    pygame.init()
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    saidas = (
        (os.path.join(raiz, "src", "assets", "icon.png"), 1024),
        (os.path.join(raiz, "arte", "icone_120.png"), 120),
        (os.path.join(raiz, "arte", "icone_180.png"), 180),
    )
    for caminho, lado in saidas:
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        pygame.image.save(desenhar(lado), caminho)
        print(f"{os.path.relpath(caminho, raiz)}: {lado}x{lado}")
    pygame.quit()


if __name__ == "__main__":
    main()
