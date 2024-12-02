import os
import numpy as np
import time
from collections import deque

# Configurações principais
MAX_ITERATIONS = 1000 # Máximo de iterações
TABU_TENURE = 1860       # Comprimento da lista Tabu
NUM_REPLICATES = 10     # Número de replicações por instância
INSTANCE_DIR = "./bancos-dados/"  # Diretório das instâncias
OUTPUT_FILE = "./outputs/output.txt"     # Arquivo de saída


def read_instance(file_path):
    #print(f"Lendo instância do arquivo: {file_path}")
    with open(file_path, "r") as file:
        lines = file.readlines()
    num_elements, num_combinations = map(int, lines[0].split())
    interactions = []
    for line in lines[1:]:
        a, b, benefit = map(float, line.split())
        interactions.append((int(a) - 1, int(b) - 1, benefit))
    #print(f"Instância lida: {num_elements} elementos, {len(interactions)} interações")
    return num_elements, interactions


#Calcula o benefício de uma solução
def evaluate_solution(solution, interactions):
    score = 0
    for a, b, benefit in interactions:
        if solution[a] and solution[b]:
            score += benefit
    return score


#Executa a busca Tabu com técnica de aspiração
def tabu_search(num_elements, interactions, max_iterations=MAX_ITERATIONS, tabu_tenure=TABU_TENURE):
    #print(f"Iniciando busca Tabu: {num_elements} elementos, {len(interactions)} interações")
    current_solution = np.random.randint(2, size=num_elements)  # Solução inicial aleatória
    best_solution = current_solution.copy()
    best_score = evaluate_solution(best_solution, interactions)
    tabu_list = deque(maxlen=tabu_tenure)  # Lista Tabu

    for iteration in range(max_iterations):
        #print(f"Iniciando iteração {iteration+1}")
        # Geração de vizinhos
        neighbors = []
        for i in range(num_elements):
            neighbor = current_solution.copy()
            neighbor[i] = 1 - neighbor[i]  # Alterna entre 0 e 1
            if tuple(neighbor) not in tabu_list:
                neighbors.append((neighbor, evaluate_solution(neighbor, interactions)))

        if not neighbors:
            #print("Sem vizinhos válidos. Encerrando busca.")
            break

        # Seleção do melhor vizinho com aspiração
        neighbors.sort(key=lambda x: x[1], reverse=True)
        best_neighbor, best_neighbor_score = neighbors[0]

        # Se o movimento tabu levar a uma solução melhor do que a melhor encontrada, aspiração é permitida
        if best_neighbor_score > best_score or tuple(best_neighbor) not in tabu_list:
            # Atualização de tabu e solução atual
            tabu_list.append(tuple(best_neighbor))
            current_solution = best_neighbor
            
            # Atualização do melhor resultado
            if best_neighbor_score > best_score:
                best_solution = best_neighbor
                best_score = best_neighbor_score

        #print(f"Melhor solução da iteração {iteration+1}: Score = {best_neighbor_score}")
    
    #print(f"Busca Tabu finalizada. Melhor score: {best_score}")
    return best_solution, best_score


def run_replicates(file_path, num_replicates=NUM_REPLICATES, max_iterations=MAX_ITERATIONS):
    #print(f"Executando {num_replicates} replicações para o arquivo {file_path}")
    num_elements, interactions = read_instance(file_path)
    best_scores = []
    execution_times = []

    for replicate in range(num_replicates):
        #print(f"Iniciando replicação {replicate+1}")
        start_time = time.time()
        _, best_score = tabu_search(num_elements, interactions, max_iterations)
        execution_time = time.time() - start_time
        best_scores.append(best_score)
        execution_times.append(execution_time)
        #print(f"Replicação {replicate+1} concluída. Tempo: {execution_time:.4f}s, Melhor Score: {best_score}")

    aggregated_results = {
        "best_score": max(best_scores),
        "mean_score": np.mean(best_scores),
        "mean_time": np.mean(execution_times)
    }
    #print(f"Resultados agregados: {aggregated_results}")
    return aggregated_results


def main():
    instance_files = [f for f in os.listdir(INSTANCE_DIR) if f.endswith(".sparse")]
    results = []

    for instance_file in instance_files:
        file_path = os.path.join(INSTANCE_DIR, instance_file)
        #print(f"=======================================================================================================================")
        #print(f"Iniciando processamento da instância: {instance_file}")
        result = run_replicates(file_path)
        #print(f"Finalizado processamento da instância: {instance_file}. Resultados: {result}")
        results.append((instance_file, result))

    # output
    with open(OUTPUT_FILE, "w") as output_file:
        output_file.write("Instance\tBest_Score\tMean_Score\tMean_Time\n")
        for instance_file, result in results:
            output_file.write(f"{instance_file}\t{result['best_score']:.2f}\t{result['mean_score']:.2f}\t{result['mean_time']:.4f}\n")
    #print("Processamento concluído. Resultados salvos em", OUTPUT_FILE)


if __name__ == "__main__":
    main()
