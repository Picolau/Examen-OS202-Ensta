import numpy as np
import time
import matplotlib.pyplot as plt
import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD

mrank = comm.Get_rank()
nranks = comm.Get_size()

nombre_cas   : int = 256
nb_cellules  : int = 360  # Cellules fantomes
nb_iterations: int = 360

compute_time = 0.
display_time = 0.

def save_as_md(cells, symbols='⬜⬛'):
    res = np.empty(shape=cells.shape, dtype='<U')
    res[cells==0] = symbols[0]
    res[cells==1] = symbols[1]
    np.savetxt(f'resultat_{num_config:03d}.md', res, fmt='%s', delimiter='', header=f'Config #{num_config}', encoding='utf-8')

def save_as_png(cells):
    fig = plt.figure(figsize=(nb_iterations/10., nb_cellules/10.))
    ax = plt.axes()
    ax.set_axis_off()
    ax.imshow(cells[:, 1:-1], interpolation='none', cmap='RdPu')
    plt.savefig(f"resultat_{num_config:03d}.png", dpi=100, bbox_inches='tight')
    plt.close()

# La façon dont j'ai pensé pour faire la parallelisation en utilisant MPI est la suivante:
# Chaque processus est résponsable pour paralleliser le "outter" boucle
# Le num_config varie de la manière suivant (Ex.: n = 3):
# Processus 0: Responsable pour les num_configs: 0, 3, 6, 9, ...
# Processus 1: Responsable pour les num_configs: 1, 4, 7, 10, ...
# Processus 2: Responsable pour les num_configs: 2, 5, 8, 11, ...
# La parallélisation est donc statique et chaque processus 
# va avoir une charge de travail d'environ nombre_cas / nranks
# La parallisation a été faite en utilisant MPI et la communication entre processus n'était pas nécessaire
for num_config in range(mrank, nombre_cas, nranks):
    t1 = time.time()
    cells = np.zeros((nb_iterations, nb_cellules+2), dtype=np.int16)
    cells[0, (nb_cellules+2)//2] = 1
    for iter in range(1, nb_iterations):
        vals = np.left_shift(1, 4*cells[iter-1, 0:-2]
                             + 2*cells[iter-1, 1:-1]
                             + cells[iter-1, 2:])
        cells[iter, 1:-1] = np.logical_and(np.bitwise_and(vals, num_config), 1)
    t2 = time.time()
    compute_time += t2 - t1

    t1 = time.time()
    save_as_md(cells)
#    save_as_png(cells)
    t2 = time.time()
    display_time += t2 - t1

# Seulement le root processus est responsable pour afficher les résultats de calcul
# Ce qui va être pareil aux résultat de tous les autres processus, vu qu'ils on un charge de travail à peu près pareil
if (mrank == 0):
    print(f"Temps calcul des generations de cellules : {compute_time:.6g}")
    print(f"Temps d'affichage des resultats : {display_time:.6g}")
