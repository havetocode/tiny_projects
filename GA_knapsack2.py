import numpy as np


np.random.seed(111)

w0 = 450
no_obj = 30

objects = np.ndarray((no_obj,3))
for i in range(no_obj):
	objects[i,0] = i 
	objects[i,1] = np.random.randint(1,20) 
	objects[i,2] = np.random.randint(1,20) 

print objects

pop_size = 100
no_genes = no_obj
population = np.ndarray((no_genes,pop_size))
for i in range(no_genes):
	for j in range(pop_size):
		population[i,j] = np.random.randint(0,5)


##variation parameters
selection_param = int(pop_size/3)
mutation_rate = 0.3
discard_no = int(pop_size/6)

def fitness(generation,population,objects):

	indv_fitness = np.ndarray((pop_size), dtype=np.float64)
	total_weight = np.ndarray((pop_size))
	total_value = np.ndarray((pop_size))

	for i in range(pop_size):
		total_weight[i] = np.sum(population[:,i]*objects[:,1])
		total_value[i] = np.sum(population[:,i]*objects[:,2])

	for i in range(pop_size):
		
		if np.any(population[:,i] < 0) or total_weight[i] >= w0:
			indv_fitness[i] = 0
		else:
			indv_fitness[i] = total_value[i]/(1+total_weight[i])
	
	if generation%20==0:

		print "Generation:"
		print generation
		print "Mean fitness:"
		print np.mean(indv_fitness)
		print "Total weight:"
		print total_weight
		print "Total value:"
		print total_value
		
	return indv_fitness

def selection(indv_fitness):
	
	fitness_order = np.argsort(indv_fitness)[::-1]
	parent_ind = fitness_order[:selection_param]
	parent2_ind = fitness_order[selection_param:-selection_param]
	infertile_ind =  fitness_order[-selection_param:]

	return parent_ind, parent2_ind, infertile_ind

def breeding(population,parent_ind,parent2_ind):
	
	parent1 = np.ndarray((no_obj,len(parent_ind)))
	parent2 = np.ndarray((no_obj,len(parent2_ind)))
	np.random.shuffle(parent2_ind)

	for i in range(len(parent_ind)):
		parent1[:,i] = population[:,parent_ind[i]]
	
	for i in range(len(parent2_ind)):
		parent2[:,i] = population[:,parent2_ind[i]]

	for i in range(len(parent_ind)):
		
		rand_gene_int = np.random.randint(0,no_obj,int(no_obj/3))

		for j in range(len(rand_gene_int)):
			temp = parent1[rand_gene_int[j],i]
			parent1[rand_gene_int[j],i] = parent2[rand_gene_int[j],i]
			parent2[rand_gene_int[j],i] = temp
	
	pop_sans_weak = np.hstack((parent1,parent2))

	return pop_sans_weak

def mutation(pop_sans_weak,population,infertile_ind):

	weaklings = np.ndarray((no_obj,len(infertile_ind)))
	weakling_weights = np.ndarray((len(infertile_ind))) 
	weakling_values = np.ndarray((len(infertile_ind)))

	for i in range(len(infertile_ind)):
		weaklings[:,i] = population[:,infertile_ind[i]]
	
	for i in range(len(infertile_ind)):
		weakling_weights[i] = np.sum(weaklings[:,i]*objects[:,1])

	muta_genes = np.random.randint(0,no_obj,int(mutation_rate*no_obj))

	for i in range(len(muta_genes)):
		for j in range(len(infertile_ind)):

			if weakling_weights[j]>w0:
				weaklings[muta_genes[i],j] -= np.random.randint(2)
			else:
				weaklings[muta_genes[i],j] += np.random.randint(2)
	
	population = np.hstack((pop_sans_weak,weaklings))

	return population

def discard_weak(population,indv_fitness):

	fitness_order = np.argsort(indv_fitness)[::-1]
	
	for i in range(discard_no):
		population[:,fitness_order[len(fitness_order)-i-1]] = population[:,fitness_order[i]]

	return population

def main(population,objects):

	j=1
	generation = 1

	indv_fitness = np.ndarray((pop_size))
	indv_fitness = fitness(generation,population,objects)	
	
	while generation<10001:
		
		temp = indv_fitness
		parent_ind, parent2_ind, infertile_ind = selection(indv_fitness)
		pop_sans_weak = breeding(population,parent_ind,parent2_ind)
		population = mutation(pop_sans_weak,population,infertile_ind)
		indv_fitness = fitness(generation,population,objects)
		population = discard_weak(population,indv_fitness)
		
		##Need something to stop the algorithm
		"""
		if j>50:
			break

		if np.all(temp == indv_fitness) and np.any(indv_fitness != 0):
			j+=1
			print "Convergence param:"
			print j
		else:
			j=1
		"""
		generation+=1

	return population,indv_fitness

solution,fin_fitness = main(population,objects)
print solution
print fin_fitness
print "Mean fitness:"
print np.mean(fin_fitness)
