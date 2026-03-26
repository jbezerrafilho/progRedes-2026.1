def hanoi(n_discos, origem, destino, auxiliar):
	if n_discos == 1:
		print(f"Mover disco 1 de {origem} para {destino}")
		return
	else:
		hanoi(n_discos -1, origem, auxiliar, destino)
		print(f"Mover disco {n_discos} de {origem} para {destino}")
		hanoi(n_discos -1, auxiliar, destino, origem)

	

n_discos = 3
hanoi(n_discos, 'A', 'C', 'B')