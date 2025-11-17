from tspUtils import *
import math
import random

def Subida_de_Encosta(n,m, s_inicial=None):
    if s_inicial is None:
        s_inicial = solucaoInicial(n)


    atual = s_inicial[:]
    va = avalia(n, atual, m)

    while True:
       novo, vn = sucessores(atual, va, n, m)

       if vn < va:
           atual = novo
           va = vn
       else:
           return atual, va

def Subida_de_Encosta_Tentativas(n, m, tMax, s_inicial=None):
    if s_inicial is None:
        s_inicial = solucaoInicial(n)

    atual = s_inicial[:]
    va = avalia(n, atual, m)

    t = 0
    while t < tMax:
        novo, vn = sucessores(atual, va, n, m)
        if vn < va:
            atual = novo
            va = vn
            t = 0
        else:
            t += 1
    return atual, va

def Tempera_Simulada(n,m,t_ini, t_fim, fr, s_inicial=None):
    if s_inicial is None:
        s_inicial = solucaoInicial(n)

    atual = s_inicial[:]
    resp = s_inicial[:]

    va = avalia(n, atual, m)
    vr = va

    t = t_ini

    while t >= t_fim:
        novo = sucessores_Tempera(atual,n)
        vn = avalia(n, novo, m)

        deltaE = vn - va

        if deltaE < 0:
            resp = novo[:]
            vr = vn
            atual = novo[:]
            va = vn
        else:
            ale = random.random()
            aux = math.exp(-deltaE/t)
            if ale <= aux:
                atual = novo[:]
                va = vn
        t = t * fr

    return resp, vr
