import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description="Input durations for components and maximum time.")
    parser.add_argument('--duration_Axle', type=int, default=10, help="Durata di Axle (>=1)")
    parser.add_argument('--duration_Wheel', type=int, default=1, help="Durata di Wheel (>=1)")
    parser.add_argument('--duration_Nuts', type=int, default=2, help="Durata di Nuts (>=1)")
    parser.add_argument('--duration_Cap', type=int, default=1, help="Durata di Cap (>=1)")
    parser.add_argument('--duration_Inspect', type=int, default=3, help="Durata di Inspect (>=1)")
    parser.add_argument('--max_time', type=int, default=30, help="Tempo massimo (>=1)")

    return parser.parse_args()

args = get_arguments()
duration_Axle = args.duration_Axle
duration_Wheel = args.duration_Wheel
duration_Nuts = args.duration_Nuts
duration_Cap = args.duration_Cap
duration_Inspect = args.duration_Inspect
max_time = args.max_time

# Tempo massimo di inizio per ogni task
max_start_time = max_time - 3

# Dizionario delle durate per ciascun task
durations = {
    'AxleF': duration_Axle,
    'AxleB': duration_Axle,
    'WheelRF': duration_Wheel,
    'WheelLF': duration_Wheel,
    'WheelRB': duration_Wheel,
    'WheelLB': duration_Wheel,
    'NutsRF': duration_Nuts,
    'NutsLF': duration_Nuts,
    'NutsRB': duration_Nuts,
    'NutsLB': duration_Nuts,
    'CapRF': duration_Cap,
    'CapLF': duration_Cap,
    'CapRB': duration_Cap,
    'CapLB': duration_Cap,
    'Inspect': duration_Inspect
}

# Variabili di inizio (rappresentano i tempi di inizio dei task)
tasks = {task: 0 for task in durations}

# Inizializzazione dei domini per ogni task
task_domains = {task: set(range(1, max_start_time + 1)) for task in tasks}

# Vincoli di precedenza tra i task
precedence_constraints = {
    'AxleF': ['WheelRF', 'WheelLF'],
    'AxleB': ['WheelRB', 'WheelLB'],
    'WheelRF': ['NutsRF'],
    'WheelLF': ['NutsLF'],
    'WheelRB': ['NutsRB'],
    'WheelLB': ['NutsLB'],
    'NutsRF': ['CapRF'],
    'NutsLF': ['CapLF'],
    'NutsRB': ['CapRB'],
    'NutsLB': ['CapLB'],
    'CapRF': ['Inspect'], 'CapLF': ['Inspect'],
    'CapRB': ['Inspect'], 'CapLB': ['Inspect']
}

# Vincolo disgiuntivo per AxleF e AxleB (non possono sovrapporsi)
def disjunctive_constraint():
    return (
        (tasks['AxleF'] + duration_Axle <= tasks['AxleB']) or (tasks['AxleB'] + duration_Axle <= tasks['AxleF'])
    )

def check_precedence_constraints():
    for task, dependents in precedence_constraints.items():
        if tasks[task] > 0:  # Solo se il task è stato assegnato
            for dependent in dependents:
                if tasks[dependent] > 0:  # Solo se il task successore è stato assegnato
                    if tasks[task] + durations[task] > tasks[dependent]:
                        return False

    if tasks['Inspect'] > 0:
        for task in tasks:
            if task != 'Inspect' and tasks[task] + durations[task] > tasks['Inspect']:
                return False  # "Inspect" deve essere eseguito dopo gli altri task

    return True

# Funzione per controllare e applicare i vincoli di precedenza in MAC
def apply_precedence_mac(task, start_time):
    for successor in precedence_constraints.get(task, []):
        min_start_time = start_time + durations[task]
        # Se il task successore ha valori che violano la precedenza, devono essere rimossi dal dominio
        task_domains[successor] = {t for t in task_domains[successor] if t >= min_start_time}

        if not task_domains[successor]:  # Se il dominio diventa vuoto
            return False
    return True

# Funzione di backtracking con MAC applicato a ogni passo
def backtrack_mac(assigned_tasks, valid_solutions):
    if len(assigned_tasks) == len(tasks) - 1:  # Caso base: tutti i task tranne Inspect sono assegnati
        # "Inspect" viene assegnato come l'ultimo task
        tasks['Inspect'] = max([tasks[task] + durations[task] for task in tasks if task != 'Inspect'])

        if check_precedence_constraints() and disjunctive_constraint():
            completion_time = max(tasks[task] + durations[task] for task in tasks)
            if completion_time <= max_time:
                # Aggiunta della soluzione corrente alla lista delle soluzioni
                valid_solution = [(task, tasks[task], tasks[task] + durations[task]) for task in tasks]
                valid_solutions.append((valid_solution, completion_time))
        return

    unassigned_tasks = [task for task in tasks if tasks[task] == 0]

    # Si deve assicurare che "Inspect" non venga scelto prima di completare gli altri task
    if 'Inspect' in unassigned_tasks:
        unassigned_tasks.remove('Inspect')

    # Scelta della variabile con il dominio più piccolo (escluso Inspect)
    task_to_assign = min(unassigned_tasks, key=lambda t: len(task_domains[t]))

    for start_time in sorted(task_domains[task_to_assign]):
        # Backup del dominio originale per ripristino in caso di backtrack
        original_domains = {t: set(task_domains[t]) for t in task_domains}

        tasks[task_to_assign] = start_time

        if task_to_assign in ['AxleF', 'AxleB']:
            if not disjunctive_constraint():  # Se il vincolo non è rispettato
                continue  # Proseguire con un altro tentativo

        # Applicazione di MAC, i domini vengono ristretti in base a questo assegnamento
        if check_precedence_constraints() and apply_precedence_mac(task_to_assign, start_time):
            backtrack_mac(assigned_tasks + [task_to_assign], valid_solutions)

        # Ripristino dei domini in caso di fallimento
        tasks[task_to_assign] = 0
        task_domains.update(original_domains)


if __name__ == "__main__":
    all_solutions = []
    backtrack_mac([], all_solutions)

    if all_solutions:
        for solution, total_duration in all_solutions:
            print(f"Soluzione valida: {solution}, Tempo totale: {total_duration}")

        # Ricerca della soluzione ottimale con costo minimo (minimo tempo totale)
        optimal_solution = min(all_solutions, key=lambda s: s[1])
        print(f"Soluzione ottimale trovata: {optimal_solution}")
    else:
        print("=====UNSATISFIABLE=====\nNessuna soluzione valida trovata.")