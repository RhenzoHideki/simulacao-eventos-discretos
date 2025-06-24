class RandomLCG:
    """
    Gerador Linear Congruente (LCG): zn+1 = (a * zn + c) % m
    """
    def __init__(self, seed=1, a=1103515245, c=12345, m=2**31):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed

    def random(self):
        "Retorna float uniforme em [0,1)"
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m

    def expovariate(self, lambd):
        "Gera variável aleatória exponencial"
        u = self.random()
        # Evitar log(0)
        if u == 0:
            u = 1e-12
        return - (1.0 / lambd) * np.log(u)

# Obs: vamos usar numpy apenas para o log. 
import numpy as np
