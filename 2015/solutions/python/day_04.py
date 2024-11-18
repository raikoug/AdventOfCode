from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

import concurrent.futures
import os
import time
import multiprocessing
from hashlib import md5

def worker_task(args):
    # args è una tupla (process_id, stop_event)
    offset, salt, stop_event = args
    # Simula il lavoro del processo
    i = 0+offset
    progress = 40000
    while True:
        if stop_event.is_set():
            # Un altro processo ha trovato la soluzione, esce
            return None
        # calcola md5sum di {salt}+i con i a salti di offset
        if md5(f'{salt}{i}'.encode("UTF-8")).hexdigest()[0:5] == "00000":
            return i
        if i > progress:
            print(f"Worker {offset} calculated {i} MD5s")
            progress += 40000
        i += 32
    return None

def worker_task2(args):
    # args è una tupla (process_id, stop_event)
    offset, salt, stop_event = args
    # Simula il lavoro del processo
    i = 0+offset
    progress = 40000
    while True:
        if stop_event.is_set():
            # Un altro processo ha trovato la soluzione, esce
            return None
        # calcola md5sum di {salt}+i con i a salti di offset
        if md5(f'{salt}{i}'.encode("UTF-8")).hexdigest()[0:6] == "000000":
            return i
        if i > progress:
            print(f"Worker {offset} calculated {i} MD5s")
            progress += 40000
        i += 32
    return None


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    num_processes = os.cpu_count()  # Ottiene il numero di CPU
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Crea un evento per comunicare tra i processi
        manager = multiprocessing.Manager()
        stop_event = manager.Event()
        # Invia i task ai processi
        futures = [executor.submit(worker_task, (i, inputs_1, stop_event)) for i in range(num_processes)]
        # Attende che il primo futuro sia completato
        done, not_done = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
        # Ottiene il risultato dal futuro completato
        for future in done:
            result = future.result()
            if result is not None:
                print(result)
                # Imposta l'evento per segnalare agli altri processi di fermarsi
                stop_event.set()
                break
        # Interrompe gli altri processi
        executor.shutdown(wait=False, cancel_futures=True)
    
    return result


    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    num_processes = os.cpu_count()  # Ottiene il numero di CPU
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Crea un evento per comunicare tra i processi
        manager = multiprocessing.Manager()
        stop_event = manager.Event()
        # Invia i task ai processi
        futures = [executor.submit(worker_task2, (i, inputs_1, stop_event)) for i in range(num_processes)]
        # Attende che il primo futuro sia completato
        done, not_done = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
        # Ottiene il risultato dal futuro completato
        for future in done:
            result = future.result()
            if result is not None:
                print(result)
                # Imposta l'evento per segnalare agli altri processi di fermarsi
                stop_event.set()
                break
        # Interrompe gli altri processi
        executor.shutdown(wait=False, cancel_futures=True)
    
    return result


if __name__ == "__main__":
    print(solve_2())