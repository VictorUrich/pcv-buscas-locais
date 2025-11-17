import random

def solucaoInicial(n):
    s = list(range(n))
    random.shuffle(s)
    return s


def avalia(n, s, m):
    v = 0
    for i in range(n-1):
        v += m [s[i]] [s[i+1]]
    v += m [s[n-1]] [s[0]]
    return v

def sucessores(atual, va, n, m):
    melhor = atual[:]
    vm = va

    id_cidade = random.randint(0, n-1)

    for i in range(n):
        if i == id_cidade:
            continue

        aux = atual[:]
        aux[id_cidade], aux[i] = aux[i], aux[id_cidade]
        v_aux = avalia(n, aux, m)

        if v_aux < vm:
            vm = v_aux
            melhor = aux
    return melhor, vm

def sucessores_Tempera(atual, n):
    nova_s = atual[:]

    i = random.randint(0, n-1)
    j = random.randint(0, n-1)
    while i == j:
        j = random.randint(0, n-1)

    nova_s[i], nova_s[j] = nova_s[j], nova_s[i]
    return nova_s

