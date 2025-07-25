from des.core import Simulator
from des.fila import QueueServer
from des.eventos import Arrival
from des.lcg import RandomLCG
import matplotlib.pyplot as plt

# Parâmetros da simulação
lambda1 = 10   # chegada externa em Fila 1
lambda2 = 20   # chegada externa em Fila 4
mu1 = mu2 = mu3 = mu4 = 30  # taxas de serviço
end_time = 10000  # tempo total de simulação (em segundos)

# Instancia o PRNG Linear Congruente
seed = 42
prng = RandomLCG(seed=seed)

# Inicializa simulador, passando o PRNG
sim = Simulator(end_time, prng)

sim.queues = {
    'Q1': QueueServer('Q1', mu1),
    'Q2': QueueServer('Q2', mu2),
    'Q3': QueueServer('Q3', mu3),
    'Q4': QueueServer('Q4', mu4)
}

# Inicializa chegadas externas
sim.schedule(Arrival(0, sim.queues['Q1'], lambda1, externo=True))
sim.schedule(Arrival(0, sim.queues['Q4'], lambda2, externo=True))

# Executa simulação
sim.run()

# --- Coleta os dados em listas para plotar ---
fila_names = list(sim.queues.keys())
utilizacoes = []
tempos_resposta = []
vazoes = []
perdas = []

for qname in fila_names:
    q = sim.queues[qname]
    utilizacao = q.total_busy_time / end_time
    tempo_medio_resposta = q.total_response_time / q.completed if q.completed > 0 else 0
    vazao = q.completed / end_time
    utilizacoes.append(utilizacao)
    tempos_resposta.append(tempo_medio_resposta)
    vazoes.append(vazao)
    perdas.append(q.losses)

print("\n==== Resultados ====\n")
print("Fila | Utilização | Tempo médio resposta | Vazão (clientes/s) | Perdas")
for i in range(len(fila_names)):
    print(f"{fila_names[i]:4} | {utilizacoes[i]:10.3f} | {tempos_resposta[i]:18.4f} | {vazoes[i]:20.4f} | {perdas[i]}")
print("\nVazão nas saídas de Q3 e Q4:")
print(f"Q3: {vazoes[fila_names.index('Q3')]:.4f} clientes/s")
print(f"Q4: {vazoes[fila_names.index('Q4')]:.4f} clientes/s")

# --- Vazão por intervalo ---
intervalo = 100  # segundos
print("\n==== Vazão por tempo (clientes/s) ====")
for qname in fila_names:
    q = sim.queues[qname]
    n_intervals = int(end_time // intervalo) + 1
    throughput_per_interval = [0] * n_intervals
    for t in q.departure_times:
        idx = int(t // intervalo)
        throughput_per_interval[idx] += 1
    print(f"\nFila {qname} - Vazão por intervalo de {intervalo}s:")
    for i, count in enumerate(throughput_per_interval):
        print(f"  Tempo {i*intervalo:>5} - {(i+1)*intervalo:>5} s: {count/intervalo:.4f} clientes/s")

    # --- Gráfico de vazão por tempo ---
    throughput_per_interval = [x/intervalo for x in throughput_per_interval]
    plt.figure(figsize=(8,3))
    plt.step([intervalo*i for i in range(n_intervals)], throughput_per_interval, where='post')
    plt.title(f'Vazão ao longo do tempo - {qname}')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Vazão (clientes/s)')
    plt.tight_layout()
    plt.savefig(f'vazao_tempo_{qname}.png')
    plt.show()

# --- Gráficos já existentes ---
plt.figure(figsize=(6,4))
plt.bar(fila_names, utilizacoes)
plt.title('Utilização de cada Fila')
plt.xlabel('Fila')
plt.ylabel('Utilização (fração)')
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig('utilizacao_filas.png')
plt.show()

plt.figure(figsize=(6,4))
plt.bar(fila_names, tempos_resposta)
plt.title('Tempo médio de resposta de cada Fila')
plt.xlabel('Fila')
plt.ylabel('Tempo médio de resposta (s)')
plt.tight_layout()
plt.savefig('tempo_resposta_filas.png')
plt.show()

plt.figure(figsize=(6,4))
plt.bar(fila_names, vazoes)
plt.title('Vazão de saída de cada Fila')
plt.xlabel('Fila')
plt.ylabel('Vazão (clientes/s)')
plt.tight_layout()
plt.savefig('vazao_filas.png')
plt.show()

plt.figure(figsize=(6,4))
plt.bar(fila_names, perdas)
plt.title('Número de perdas em cada Fila')
plt.xlabel('Fila')
plt.ylabel('Perdas')
plt.tight_layout()
plt.savefig('perdas_filas.png')
plt.show()
