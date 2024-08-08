# Using multicore to speed up evaluation
from playground_calling import simulate_game
import multiprocessing

def main_loop():
    outputtuple = simulate_game()
    return outputtuple

if __name__ == '__main__':
    epochs = 20
    output_db = multiprocessing.Array('i', epochs)
    cores = 4
    
    segment = epochs // cores

    processes = []

    for i in range(cores):
        start = i * segment
        if i == cores - 1:
            # Set end pt of last core to num of epochs
            end = epochs
        else:
            end = start + segment

        # Creating a process!
        p = multiprocessing.process(target=main_loop, args=())
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(output_db)
