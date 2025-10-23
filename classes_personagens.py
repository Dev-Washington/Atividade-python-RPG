import random
from abc import ABC, abstractmethod

# === UTILIDADES ===

# 24. Classe Dado para gerar valores aleatórios
class Dado:
    @staticmethod
    def rolar(lados=6):
        """Rola um dado com número especificado de lados"""
        return random.randint(1, lados)
    
    @staticmethod
    def rolar_variacao(base, variacao):
        """Adiciona uma variação aleatória a um valor base"""
        return base + random.randint(-variacao, variacao)


# === HABILIDADES ===

# 21. Molde/Contrato para Habilidades (classe abstrata)
class Habilidade(ABC):
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
    
    @abstractmethod
    def usar(self, usuario, alvo):
        """Método abstrato que obriga toda habilidade a implementar uso"""
        pass
    
    def __str__(self):
        return f"{self.nome}: {self.descricao}"


# 22. Implementando habilidades concretas
class AtaqueForte(Habilidade):
    def __init__(self):
        super().__init__("Ataque Forte", "Um golpe devastador com dano aumentado")
    
    def usar(self, usuario, alvo):
        # Dano base * 1.5 + variação de dado
        dano_base = usuario.calcular_dano()
        dano = int(dano_base * 1.5) + Dado.rolar(6)
        print(f"\n💥 {usuario.nome} usa {self.nome}!")
        print(f"⚔️  Um golpe devastador causa {dano} de dano em {alvo.nome}!")
        alvo.receber_dano(dano)


class BolaDeFogo(Habilidade):
    def __init__(self):
        super().__init__("Bola de Fogo", "Lança uma esfera flamejante de magia pura")
    
    def usar(self, usuario, alvo):
        # Dano fixo alto + variação de dado
        dano = 25 + Dado.rolar(10)
        print(f"\n🔥 {usuario.nome} conjura {self.nome}!")
        print(f"✨ Uma explosão flamejante causa {dano} de dano mágico em {alvo.nome}!")
        alvo.receber_dano(dano)


class FlechaPerfurante(Habilidade):
    def __init__(self):
        super().__init__("Flecha Perfurante", "Uma flecha que ignora parte da defesa")
    
    def usar(self, usuario, alvo):
        dano = usuario.calcular_dano() + 10 + Dado.rolar(8)
        print(f"\n🎯 {usuario.nome} dispara {self.nome}!")
        print(f"🏹 A flecha perfura causando {dano} de dano em {alvo.nome}!")
        alvo.receber_dano(dano)


# === CLASSE BASE ===

class Personagem:
    def __init__(self, nome, vida, forca):
        self.nome = nome
        self._vida = vida
        self._vida_maxima = vida
        self.forca = forca
        self.arma = None
        self.inventario = Inventario()
        self.habilidades = []  # 23. Lista de habilidades
    
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        if valor < 0:
            self._vida = 0
        elif valor > self._vida_maxima:
            self._vida = self._vida_maxima
        else:
            self._vida = valor
    
    @property
    def vida_maxima(self):
        return self._vida_maxima
    
    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0
    
    def esta_vivo(self):
        return self.vida > 0
    
    def usar_pocao(self):
        pocao = self.inventario.buscar_pocao()
        if pocao:
            cura_real = min(pocao.cura, self.vida_maxima - self.vida)
            self.vida += cura_real
            self.inventario.remover_item(pocao)
            print(f"\n💚 {self.nome} usou {pocao.nome} e recuperou {cura_real} pontos de vida!")
            return True
        else:
            print(f"\n❌ {self.nome} não tem poções no inventário!")
            return False
    
    # 25. Combate imprevisível - ataque com variação de dado
    def atacar(self, alvo):
        dano_base = self.calcular_dano()
        variacao = Dado.rolar(4) - 2  # Variação de -2 a +2
        dano = max(1, dano_base + variacao)
        print(f"\n⚔️  {self.nome} ataca {alvo.nome} causando {dano} de dano!")
        alvo.receber_dano(dano)
    
    def calcular_dano(self):
        dano = self.forca
        if self.arma:
            dano += self.arma.dano
        return dano
    
    # 23. Sistema para usar habilidades
    def adicionar_habilidade(self, habilidade):
        self.habilidades.append(habilidade)
    
    def listar_habilidades(self):
        if not self.habilidades:
            print(f"{self.nome} não possui habilidades!")
        else:
            print(f"\n🌟 Habilidades de {self.nome}:")
            for i, hab in enumerate(self.habilidades, 1):
                print(f"  {i}. {hab}")
    
    def usar_habilidade(self, indice, alvo):
        if 0 <= indice < len(self.habilidades):
            self.habilidades[indice].usar(self, alvo)
            return True
        return False


# === CLASSES DE HERÓIS ===

class Guerreiro(Personagem):
    def __init__(self, nome, vida, forca):
        super().__init__(nome, vida, forca)
        self.adicionar_habilidade(AtaqueForte())  # Habilidade especial
    
    def __str__(self):
        arma_info = f", Arma: {self.arma.nome}" if self.arma else ""
        return f"⚔️  Guerreiro: {self.nome} | Vida: {self.vida}/{self.vida_maxima} | Força: {self.forca}{arma_info}"
    
    def atacar(self, alvo):
        dano_base = self.calcular_dano()
        variacao = Dado.rolar(4) - 2
        dano = max(1, dano_base + variacao)
        print(f"\n⚔️  {self.nome} desfere um golpe poderoso em {alvo.nome} causando {dano} de dano!")
        alvo.receber_dano(dano)


class Mago(Personagem):
    def __init__(self, nome, vida, forca, poder_magico):
        super().__init__(nome, vida, forca)
        self.poder_magico = poder_magico
        self.adicionar_habilidade(BolaDeFogo())
    
    def __str__(self):
        arma_info = f", Arma: {self.arma.nome}" if self.arma else ""
        return f"✨ Mago: {self.nome} | Vida: {self.vida}/{self.vida_maxima} | Força: {self.forca} | Poder: {self.poder_magico}{arma_info}"
    
    def calcular_dano(self):
        dano = self.forca + self.poder_magico
        if self.arma:
            dano += self.arma.dano
        return dano
    
    def atacar(self, alvo):
        dano_base = self.calcular_dano()
        variacao = Dado.rolar(4) - 2
        dano = max(1, dano_base + variacao)
        print(f"\n✨ {self.nome} conjura um feitiço arcano em {alvo.nome} causando {dano} de dano mágico!")
        alvo.receber_dano(dano)


class Arqueiro(Personagem):
    def __init__(self, nome, vida, forca, precisao):
        super().__init__(nome, vida, forca)
        self.precisao = precisao
        self.adicionar_habilidade(FlechaPerfurante())
    
    def __str__(self):
        arma_info = f", Arma: {self.arma.nome}" if self.arma else ""
        return f"🏹 Arqueiro: {self.nome} | Vida: {self.vida}/{self.vida_maxima} | Força: {self.forca} | Precisão: {self.precisao}{arma_info}"
    
    def calcular_dano(self):
        dano = self.forca + self.precisao
        if self.arma:
            dano += self.arma.dano
        return dano
    
    def atacar(self, alvo):
        dano_base = self.calcular_dano()
        variacao = Dado.rolar(4) - 2
        dano = max(1, dano_base + variacao)
        print(f"\n🏹 {self.nome} dispara uma flecha certeira em {alvo.nome} causando {dano} de dano!")
        alvo.receber_dano(dano)


# === CLASSES DE INIMIGOS ===

class Monstro(Personagem):
    def __init__(self, nome, vida, forca):
        super().__init__(nome, vida, forca)
    
    def __str__(self):
        return f"👹 {self.nome} | Vida: {self.vida}/{self.vida_maxima} | Força: {self.forca}"
    
    def atacar(self, alvo):
        dano_base = self.calcular_dano()
        variacao = Dado.rolar(4) - 2
        dano = max(1, dano_base + variacao)
        print(f"\n👹 {self.nome} ataca ferozmente {alvo.nome} causando {dano} de dano!")
        alvo.receber_dano(dano)
    
    @staticmethod
    def criar_goblin():
        return Monstro("Goblin", 50, 8)
    
    @staticmethod
    def criar_dragao():
        return Monstro("Dragão", 150, 20)


# 26. Orc com golpe crítico
class Orc(Monstro):
    def __init__(self):
        super().__init__("Orc", 80, 12)
        self.chance_critico = 30  # 30% de chance
    
    def __str__(self):
        return f"💀 {self.nome} Selvagem | Vida: {self.vida}/{self.vida_maxima} | Força: {self.forca}"
    
    def atacar(self, alvo):
        dano_base = self.calcular_dano()
        
        # Verificar se é crítico
        if Dado.rolar(100) <= self.chance_critico:
            dano = dano_base * 2
            print(f"\n💥 GOLPE CRÍTICO! {self.nome} desfere um ataque brutal em {alvo.nome}!")
            print(f"💀 Dano DOBRADO: {dano}!")
        else:
            variacao = Dado.rolar(4) - 2
            dano = max(1, dano_base + variacao)
            print(f"\n💀 {self.nome} ataca {alvo.nome} causando {dano} de dano!")
        
        alvo.receber_dano(dano)


# === ITENS ===

class Arma:
    def __init__(self, nome, dano):
        self.nome = nome
        self.dano = dano
    
    def __str__(self):
        return f"⚔️  {self.nome} | Dano: +{self.dano}"


class Pocao:
    def __init__(self, nome, cura):
        self.nome = nome
        self.cura = cura
    
    def __str__(self):
        return f"💊 {self.nome} | Cura: {self.cura}"


class Inventario:
    def __init__(self):
        self.itens = []
    
    def adicionar_item(self, item):
        self.itens.append(item)
    
    def remover_item(self, item):
        if item in self.itens:
            self.itens.remove(item)
            return True
        return False
    
    def listar_itens(self):
        if not self.itens:
            print("📦 Inventário vazio!")
        else:
            print("\n📦 INVENTÁRIO:")
            for i, item in enumerate(self.itens, 1):
                print(f"  {i}. {item}")
    
    def buscar_pocao(self):
        for item in self.itens:
            if isinstance(item, Pocao):
                return item
        return None
    
    def contar_pocoes(self):
        return sum(1 for item in self.itens if isinstance(item, Pocao))


# === SISTEMA DE BATALHA ===

# 27, 28, 29. Gerenciador de Batalha com sistema de turnos
class Batalha:
    def __init__(self, lado1, lado2):
        self.lado1 = lado1 if isinstance(lado1, list) else [lado1]
        self.lado2 = lado2 if isinstance(lado2, list) else [lado2]
        self.turno = 1
    
    def combatentes_vivos(self, lado):
        return [c for c in lado if c.esta_vivo()]
    
    def lado_vivo(self, lado):
        return any(c.esta_vivo() for c in lado)
    
    # 28. Sistema de turnos
    def executar_turno(self, atacante, defensores):
        if not atacante.esta_vivo():
            return
        
        # Escolher alvo aleatório entre os vivos
        alvos_vivos = self.combatentes_vivos(defensores)
        if not alvos_vivos:
            return
        
        alvo = random.choice(alvos_vivos)
        atacante.atacar(alvo)
        
        if not alvo.esta_vivo():
            print(f"💀 {alvo.nome} foi derrotado!")
    
    def executar_turno_jogador(self, jogador, inimigos):
        if not jogador.esta_vivo():
            return
        
        alvos_vivos = self.combatentes_vivos(inimigos)
        if not alvos_vivos:
            return
        
        print(f"\n⚔️  Turno de {jogador.nome}")
        print("1 - Ataque Normal")
        print("2 - Usar Habilidade")
        print("3 - Usar Poção")
        
        escolha = input("Escolha: ").strip()
        
        if escolha == "1":
            if len(alvos_vivos) > 1:
                print("\nEscolha o alvo:")
                for i, alvo in enumerate(alvos_vivos, 1):
                    print(f"{i}. {alvo.nome} (Vida: {alvo.vida}/{alvo.vida_maxima})")
                alvo_idx = int(input("Alvo: ").strip()) - 1
                alvo = alvos_vivos[alvo_idx]
            else:
                alvo = alvos_vivos[0]
            
            jogador.atacar(alvo)
            
            if not alvo.esta_vivo():
                print(f"💀 {alvo.nome} foi derrotado!")
        
        elif escolha == "2":
            jogador.listar_habilidades()
            hab_idx = int(input("Escolha a habilidade: ").strip()) - 1
            
            if len(alvos_vivos) > 1:
                print("\nEscolha o alvo:")
                for i, alvo in enumerate(alvos_vivos, 1):
                    print(f"{i}. {alvo.nome} (Vida: {alvo.vida}/{alvo.vida_maxima})")
                alvo_idx = int(input("Alvo: ").strip()) - 1
                alvo = alvos_vivos[alvo_idx]
            else:
                alvo = alvos_vivos[0]
            
            jogador.usar_habilidade(hab_idx, alvo)
            
            if not alvo.esta_vivo():
                print(f"💀 {alvo.nome} foi derrotado!")
        
        elif escolha == "3":
            jogador.usar_pocao()
    
    # 30. Batalha em equipe
    def iniciar(self, jogador_controlado=None):
        print("\n" + "="*60)
        print("⚔️  BATALHA INICIADA! ⚔️")
        print("="*60)
        
        while self.lado_vivo(self.lado1) and self.lado_vivo(self.lado2):
            print(f"\n{'='*60}")
            print(f"TURNO {self.turno}")
            print(f"{'='*60}")
            
            # Mostrar status
            print("\n🛡️  SEUS HERÓIS:")
            for heroi in self.combatentes_vivos(self.lado1):
                print(f"  {heroi}")
            
            print("\n👹 INIMIGOS:")
            for inimigo in self.combatentes_vivos(self.lado2):
                print(f"  {inimigo}")
            
            # Turno do lado 1 (heróis)
            for combatente in self.lado1:
                if combatente.esta_vivo():
                    if jogador_controlado and combatente == jogador_controlado:
                        self.executar_turno_jogador(combatente, self.lado2)
                    else:
                        self.executar_turno(combatente, self.lado2)
                    
                    if not self.lado_vivo(self.lado2):
                        break
            
            if not self.lado_vivo(self.lado2):
                break
            
            input("\n[Pressione ENTER para turno dos inimigos]")
            
            # Turno do lado 2 (inimigos)
            for combatente in self.lado2:
                if combatente.esta_vivo():
                    self.executar_turno(combatente, self.lado1)
                    
                    if not self.lado_vivo(self.lado1):
                        break
            
            self.turno += 1
        
        # 29. Anunciar vencedor
        self.anunciar_vencedor()
    
    def anunciar_vencedor(self):
        print("\n" + "="*60)
        print("⚔️  FIM DA BATALHA! ⚔️")
        print("="*60)
        
        if self.lado_vivo(self.lado1):
            print("\n🎉 VITÓRIA! Seus heróis venceram! 🎉")
            print("\n🏆 Heróis sobreviventes:")
            for heroi in self.combatentes_vivos(self.lado1):
                print(f"  {heroi}")
        else:
            print("\n💀 DERROTA... Seus heróis foram derrotados... 💀")


# === JOGO ===

def criar_heroi():
    print("\n" + "="*50)
    print("🎮 BEM-VINDO AO RPG! 🎮")
    print("="*50)
    print("\nEscolha seu herói:")
    print("1 - Guerreiro (Vida: 100, Força: 15)")
    print("2 - Mago (Vida: 80, Poder Total: 25)")
    print("3 - Arqueiro (Vida: 90, Precisão Total: 22)")
    
    escolha = input("\nSua escolha: ").strip()
    nome = input("Digite o nome do seu herói: ").strip()
    
    if escolha == "1":
        heroi = Guerreiro(nome if nome else "Thorin", 100, 15)
        arma = Arma("Espada Longa", 10)
    elif escolha == "2":
        heroi = Mago(nome if nome else "Gandalf", 80, 5, 20)
        arma = Arma("Cajado Mágico", 8)
    elif escolha == "3":
        heroi = Arqueiro(nome if nome else "Legolas", 90, 10, 12)
        arma = Arma("Arco Élfico", 9)
    else:
        heroi = Guerreiro("Thorin", 100, 15)
        arma = Arma("Espada Longa", 10)
    
    heroi.arma = arma
    heroi.inventario.adicionar_item(Pocao("Poção de Vida", 30))
    heroi.inventario.adicionar_item(Pocao("Poção de Vida", 30))
    heroi.inventario.adicionar_item(Pocao("Poção Grande", 50))
    
    return heroi

def iniciar_jogo():
    jogador = criar_heroi()
    
    # Criar aliados
    aliado1 = Mago("Merlin", 70, 5, 18)
    aliado1.arma = Arma("Varinha Antiga", 6)
    
    # 30. Batalha em equipe - 2 heróis vs 3 inimigos
    print("\n" + "="*60)
    print("🌲 Vocês encontram um grupo de inimigos! 🌲")
    print("="*60)
    
    goblin1 = Monstro.criar_goblin()
    goblin2 = Monstro.criar_goblin()
    orc = Orc()
    
    equipe_herois = [jogador, aliado1]
    equipe_inimigos = [goblin1, goblin2, orc]
    
    input("\n[Pressione ENTER para iniciar]")
    
    batalha = Batalha(equipe_herois, equipe_inimigos)
    batalha.iniciar(jogador_controlado=jogador)
    
    print("\n\n🎮 FIM DO JOGO 🎮\n")

if __name__ == "__main__":
    iniciar_jogo()