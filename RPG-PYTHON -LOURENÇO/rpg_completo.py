# ==========================
#     NÍVEL BÁSICO (1–10)
# ==========================

import random

# ---------- Questões 7 e 8 ----------
class Arma:
    def __init__(self, nome, dano):
        self.nome = nome
        self.dano = dano

class Pocao:
    def __init__(self, nome, cura):
        self.nome = nome
        self.cura = cura

# ---------- Questões 11, 12, 13 ----------
class Personagem:
    def __init__(self, nome, vida, força):
        self.nome = nome
        self.__vida = vida
        self.vida_max = vida
        self.força = força
        self.arma = None
        self.inventario = Inventario()
        self.habilidades = []

    # Vida protegida
    def get_vida(self):
        return self.__vida

    def set_vida(self, valor):
        if valor < 0:
            self.__vida = 0
        elif valor > self.vida_max:
            self.__vida = self.vida_max
        else:
            self.__vida = valor

    # Receber dano
    def receber_dano(self, dano):
        self.set_vida(self.get_vida() - dano)

    # Equipar arma
    def equipar_arma(self, arma):
        self.arma = arma

    # Ataque base
    def atacar(self, alvo):
        variacao = random.randint(-2, 2)  # Questão 25
        dano = self.força + variacao
        if self.arma:
            dano += self.arma.dano
        if dano < 0:
            dano = 0
        print(f"{self.nome} atacou {alvo.nome} causando {dano} de dano!")
        alvo.receber_dano(dano)

    # Habilidade
    def usar_habilidade(self, habilidade, alvo):
        habilidade.usar(self, alvo)

    # Vida > 0?
    def esta_vivo(self):
        return self.get_vida() > 0

    # Exibir status (Questão 5)
    def __str__(self):
        arma_nome = self.arma.nome if self.arma else "Nenhuma"
        return f"{self.nome} | Vida: {self.get_vida()}/{self.vida_max} | Arma: {arma_nome}"


# ---------- Questão 15 ----------
class Inventario:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

# ---------- Questão 17 ----------
def usar_pocao(personagem, pocao):
    personagem.set_vida(personagem.get_vida() + pocao.cura)


# ---------- Classes específicas (Questões 1, 2, 3 e 18) ----------

class Guerreiro(Personagem):
    pass

class Mago(Personagem):
    def atacar(self, alvo):
        dano = self.força + 5
        print(f"{self.nome} lançou magia causando {dano} de dano!")
        alvo.receber_dano(dano)

class Arqueiro(Personagem):
    def atacar(self, alvo):
        dano = self.força + 3
        print(f"{self.nome} atirou uma flecha causando {dano} de dano!")
        alvo.receber_dano(dano)


# ---------- Questões 4, 19 e 26 ----------

class Monstro:
    def __init__(self, nome, vida, força):
        self.nome = nome
        self.vida = vida
        self.força = força

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

    def atacar(self, alvo):
        print(f"{self.nome} atacou {alvo.nome} causando {self.força} de dano!")
        alvo.receber_dano(self.força)

    def esta_vivo(self):
        return self.vida > 0

    @staticmethod
    def goblin_padrao():
        return Monstro("Goblin", 30, 5)


class Orc(Monstro):
    def atacar(self, alvo):
        dano = self.força
        if random.randint(1, 5) == 1:  # Crítico 20%
            dano *= 2
            print(f"{self.nome} acertou um GOLPE CRÍTICO!")
        print(f"{self.nome} atacou {alvo.nome} causando {dano} de dano!")
        alvo.receber_dano(dano)


# ==========================
#     NÍVEL AVANÇADO (21–30)
# ==========================

# ---------- Questão 21 ----------
class Habilidade:
    def usar(self, atacante, alvo):
        raise NotImplementedError("Implementar na classe filha!")

# ---------- Questão 22 ----------
class AtaqueForte(Habilidade):
    def usar(self, atacante, alvo):
        dano = atacante.força + 10
        print(f"{atacante.nome} usou ATAQUE FORTE causando {dano}!")
        alvo.receber_dano(dano)

class BolaDeFogo(Habilidade):
    def usar(self, atacante, alvo):
        dano = 20
        print(f"{atacante.nome} lançou BOLA DE FOGO causando {dano}!")
        alvo.receber_dano(dano)

# ---------- Questão 24 ----------
class Dado:
    @staticmethod
    def rolar(lados=6):
        return random.randint(1, lados)

# ---------- Questão 27, 28, 29 ----------
class Batalha:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def iniciar(self):
        turno = 0
        print("\n==== INÍCIO DA BATALHA ====\n")

        while self.a.esta_vivo() and self.b.esta_vivo():
            if turno % 2 == 0:
                self.a.atacar(self.b)
            else:
                self.b.atacar(self.a)
            turno += 1
            print(f"{self.a.nome}: {self.a.get_vida()} | {self.b.nome}: {self.b.vida}")

        print("\n==== FIM DA BATALHA ====\n")
        if self.a.esta_vivo():
            print(f"VENCEDOR: {self.a.nome}")
        else:
            print(f"VENCEDOR: {self.b.nome}")

# ---------- Questão 30 ----------
class BatalhaEquipes:
    def __init__(self, equipe1, equipe2):
        self.e1 = equipe1
        self.e2 = equipe2

    def iniciar(self):
        print("\n==== BATALHA ENTRE EQUIPES ====\n")

        while any(p.esta_vivo() for p in self.e1) and any(p.esta_vivo() for p in self.e2):

            # Turno equipe 1
            atacante = next((p for p in self.e1 if p.esta_vivo()), None)
            alvo = next((p for p in self.e2 if p.esta_vivo()), None)
            atacante.atacar(alvo)

            if not any(p.esta_vivo() for p in self.e2):
                break

            # Turno equipe 2
            atacante = next((p for p in self.e2 if p.esta_vivo()), None)
            alvo = next((p for p in self.e1 if p.esta_vivo()), None)
            atacante.atacar(alvo)

        print("\n==== FIM DA BATALHA EM EQUIPES ====\n")
        if any(p.esta_vivo() for p in self.e1):
            print("Equipe 1 venceu!")
        else:
            print("Equipe 2 venceu!")
