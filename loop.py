import pygame
from obj import *
import conf
import sys
import time
import draw_rede

class Loop:
    def __init__(self, surface):
        self.draw_rede = draw_rede.DrawRede(425, 200)
        self.best_agente = None
        self.quant_agentes = 500
        self.qt_loop_epoca = 3_000
        self.qt_iter = 0
        self.surface = surface
        self.parede = Parede(surface)
        self.sensor = Sensor(surface)
        self.agentes = []
        ag = self.load_net()
        self.agentes.append(ag)
        #for i in range(0, self.quant_agentes):
        #    self.agentes.append(Agente(surface, self.parede))
    def loop(self):
        if pygame.mouse.get_pressed() == (True, False, False):
            agent = Agente(self.surface, self.parede)
            pos_m = pygame.mouse.get_pos()
            agent.x = pos_m[0]
            agent.y = pos_m[1]
            self.agentes.append(agent)
        if pygame.mouse.get_pressed() == (False, False, True):
            pos_m = pygame.mouse.get_pos()
            agent.x = pos_m[0]
            agent.y = pos_m[1]
        self.parede.loop()
        self.sensor.loop()
        for ag in self.agentes:
            ag.loop()
        for rect in self.parede.rects:
            for ag in self.agentes:
                collision = rect.colliderect((ag.pos_rect[0] -5, ag.pos_rect[1] - 5, ag.pos_rect[2], ag.pos_rect[3]))
                if collision:
                    ag.score += 1
                    #self.agentes.remove(ag)
        self.qt_iter += 1
        if self.qt_iter >= self.qt_loop_epoca:
            self.qt_iter = 0
            sys.stdout.write("\n=======================Fim de epoca========================\n")
            agentes_remover = []
            for ag in self.agentes:
                sys.stdout.write(str(ag.score) + "\n")
                if ag.score == 0:
                    agentes_remover.append(ag)
                max_score = self.ordenarLista(self.agentes)
                for ag in self.agentes:
                    if ag.score == max_score:
                        self.best_agente = ag
                        break
            self.save_net(self.best_agente)
            for ag in agentes_remover:
                self.agentes.remove(ag)
        self.draw_rede.draw(self.surface, self.agentes[0])

    def save_net(self, ag):
        arq = open('pesos.txt', 'w')
        arq.write(str(ag.score)+' ')
        for layer in ag.rede.rede:
            for perc in layer.perceptrons:
                arq.write(str(perc.bias)+' ')
                for peso in perc.pesos:
                    arq.write(str(peso)+' ')
        arq.close()

    def load_net(self):
        ag = Agente(self.surface, self.parede)
        arq = open('pesos.txt', 'r')
        pesos = arq.readline().split(' ')
        print(pesos)
        i = 1
        for layer in ag.rede.rede:
            for perc in layer.perceptrons:
                perc.bias = int(pesos[i])
                i += 1
                j = 0
                for j in range(0, len(perc.pesos)):
                    perc.pesos[j] = int(pesos[i])
                    i += 1
        arq.close()
        return ag

    def ordenarLista(self, list_agente: list):
        val = []
        for ag in list_agente:
            val.append(ag.score)
        val.sort()
        val_min = val[-1]
        return val_min