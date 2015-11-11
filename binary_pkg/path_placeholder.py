

LENGTH = 100
RANDOM = 'jc4b6yulaujayb9sr94ia88eourzeqip0oidmas391yaj24ng0bmdur5g21g2k6kobby09vj5ereo9mivqyqzrfbalp9z0uj4v7kiqehtyvpfjoa6dgc6b9fgzjrvm3bpi6ee7f8sqwnqwd0dh1nvkq2pwvwpmvganamqy4mb1ybcvvq4kdx56txwrkify0l3hcvt4o4cg641ko3qc6wwrlu728r7bmq12mu1uunnouxgzkqemzokce7tibqr8pu'


import os

def make_path(*dirnames):
    prefix = os.path.join(*dirnames)
    end = LENGTH - len(prefix) - len(os.path.pathsep)
    if not end > 20:
        raise RuntimeError('base path is too long, please build in a shorter directory')
    return os.path.join(prefix, RANDOM[:end])


