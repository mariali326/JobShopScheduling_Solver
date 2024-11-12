# Job Shop Scheduling Solver
Questo progetto fornisce un solver per il problema di Job-Shop Scheduling in Python. Il solver trova una soluzione a costo minimo per un insieme di 15 task, soggetti a vincoli di precedenza e un vincolo disgiuntivo. L'obiettivo del solver è minimizzare il tempo di completamento dei task, ovvero trovare la soluzione con il tempo di completamento minimo in base ai parametri forniti dall'utente.

## File Sorgente
* jss_solver.py: Questo è il file principale del solver.
   - Contiene i dati predefiniti sui task, come la durata di ciascun task e le informazioni sui vincoli di precedenza e disgiuntivi tra i task.
   - Contiene l'implementazione dell'algoritmo di risoluzione per il problema di Job Shop Scheduling, che utilizza il backtracking e il MAC (Maintaining Arc Consistency) per ottimizzare la ricerca della soluzione. È possibile passare i parametri desiderati tramite il terminale per personalizzare l'istanza del problema.

## Come Eseguire il Solver
Per eseguire il solver, apri il terminale e utilizza il comando seguente per modificare i valori dei vari parametri:
```bash
python jss_solver.py --duration_Axle <value> --duration_Wheel <value> --duration_Nuts <value> --duration_Cap <value> --duration_Inspect <value> --max_time <value>
```
### Parametri
Tutti i valori devono essere espressi come numeri interi, rappresentanti i minuti.
* --duration_Axle: Durata del task "Axle"
* --duration_Wheel: Durata del task "Wheel"
* --duration_Nuts: Durata del task "Nuts"
* --duration_Cap: Durata del task "Cap"
* --duration_Inspect: Durata del task "Inspect"
* --max_time: Tempo massimo di completamento per la soluzione

## Istruzioni per Riprodurre i Risultati
1. Istanza 1: Per riprodurre i risultati dell'istanza 1, cliccare su Run o eseguire il comando:
   ```bash
   python jss_solver.py
   ```
2. Istanza 2: Per riprodurre i risultati dell'istanza 2, impostare la durata di "Axle" a 11:
   ```bash
   python jss_solver.py --duration_Axle 11
   ```
3. Istanza 3: Per riprodurre i risultati dell'istanza 3, impostare la durata di "Wheel" a 2 e la durata di "Inspect" a 4:
   ```bash
   python jss_solver.py --duration_Wheel 2 --duration_Inspect 4
   ```
4. Istanza 4: Per riprodurre l'istanza 4, aumentare tutti i valori di durata di 1. Questo dovrebbe portare a un'istanza in cui non esiste una soluzione valida:
   ```bash
   python jss_solver.py --duration_Axle 11 --duration_Wheel 2 --duration_Nuts 3 --duration_Cap 2 --duration_Inspect 4 --max_time 31
   ```

## Note Importanti
Si consiglia di evitare valori troppo grandi per i parametri, in particolare per il tempo di completamento. Poiché l'algoritmo implementato potrebbe richiedere molto tempo per eseguire calcoli complessi su valori elevati, è preferibile utilizzare valori moderati per ottenere tempi di esecuzione ragionevoli. In caso di parametri con valori molto alti, l'algoritmo può comunque fornire un risultato, ma potrebbe richiedere un tempo significativamente lungo. 
  

