# Graph_Partitioning

In this project we have surveyed and implemented some of the most commonly used graph partitioning algorithm. It has an important application in the layout of digital circuits component in VLSI i.e. partitioning a circuit/system into smaller subsystems called block for proper layout of the component. The partitioning speeds up the design process and blocks can be design independently and simultaneously speeding up the overall design process. It is a combinatorial problem i.e. given a graph G with costs on its edges, partition the nodes of G into subsets no longer than a given maximum size, so as to minimize the total cost of the edges cut. Since graph partitioning methods is NP-hard problems, there are many heuristic and approximate algorithms presents in the literature for graph partitioning and can be broadly classified into three categories 
	Local Method
	Global Method
Some of the well-known local methods are the Kernighan–Lin algorithm, and Fiduccia-Mattheyses algorithms, an effective 2-way cuts by local search strategies. Their major drawback is the arbitrary initial partitioning can affect the final solution quality and therefore its generally recommended to run these local search algorithms many times with arbitrary partition initialization and select the best results. Global approaches rely on properties of the entire graph and do not rely on an arbitrary initial partition. The most common example is spectral partitioning, where a partition is derived from the spectrum of the adjacency matrix.
In this project we have tried to cover the entire spectrum of graph partitioning methods and have implemented the following algorithms:
	Tabu Search
	Genetic Algorithm
	Hybrid Genetic Algorithm
	Simulated Annealing
	Spectral Partitioning
	Modified Spectral Partitioning
	Multi-Level Partitioning
we presented the design of our functional unit for adding precision control capability to GPUs. 





Section 1:  ALGORITHM DETAILS:
TABU SEARCH
Tabu search is a meta-level heuristic proposed by Glover for finding good solutions to combinatorial optimization problems. It is capable of obtaining a good solution of competitive quality in high speed when compared to simulated annealing and the KLFM algorithm. The algorithm is as follow[1]:
	Initialization
		Set i=0
		Generate an initial solution 
		Initialize tabu list(s) T and aspiration function A
		Set best=x_i , bestcost=f(best) and besti=i
	Body
		While(i-besti<max){
			i=i+1
locate the best x_i  in N(x_(i-1 )) where x_i  doesnot satisfy tabu conditions or if aspiration function overrules tabu conditions;
			if(f(x_i)<bestcost){
				best=x_i
bestcost=f(best),
besti=i;
			}
			Update tabu list(s) T;
			Update aspiration function A;
}

At each iteration of this algorithm selects the best neighborhood solution and thus unlike hill climbing this algorithm can move down a hill however it can get stuck in a cycle and to get out of it, it uses aspiration function and tabu lists. It keeps track of the past good moves in order to constrain and diversify the search for good solutions.  The main purpose of the tabu list is to constrain the direction of search and prevents the algorithm from going back to a state which was reached previously. Thus, it prevents us from being trapped in any local optimum. In addition to tabu list, the aspiration functions has the ability to overrule the tabu conditions and serves as a mechanism to diversify the search and encourage exploration of new regions in the search space.




GENETIC ALGORITHM
A genetic algorithm is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms. It is commonly used to generate high-quality solutions to optimization and search problems by relying on the bio-inspired operators such as mutation, crossover and selection. The algorithm is as follow[2]:	
generate initial population of fixed size(50)
	do{
		compute fitnesss.
		select two parents from the population
		child=offspring(parent1, parent2)
		mutateChild(child)
		localImprovement(child)
		replace(population,child)
	}(!stopCondition)
	PopulationGeneration:
	randomPartition with node on left 0 and right 1(chromosome)
	Fitness:
	Fitness of member i =(C_w-C_i)+(C_w-C_b)/3 , where C_b,C_w,C_i is the cutsize corresponding to best worst and current member
	Parents Selection:
	Directly proportional to Fitness Value. Thus, changes of selecting the best member if 4 times more than selecting the worst member.
	Offspring Generation:
	Randomly selecting cut point and transferring part of chromosome from each member. 
	Mutation:
	Balancing the chromosome by flipping the partition of random member.
	Replace:
	Selecting the worst member in the population 
	Stopping Condition:
	80% of population have same fitness value
HYBRID GENETIC ALGORITHM
Applied Kernighan and Lin, Fiduccia and Mattheyses algorithm as a part of local improvement.The algorithm is as follow[2]:
minCutSize=Infinite
minPartitionMapping 
for 1:NUM_OF_ITTERATION:
   		cell=findCellWithMaximumGainInGivenPartition()
   		swap(cell)   
   		lock(cell)
   		currentCutsize=cutSize()
   	if(currentCutSize<minCutSize):
		minCutSize=currentCutSize    		
          		minPartitionMapping=CurrentPartition
SIMULATED ANNEALING
It’s a probabilistic technique for approximating the global optimum of a given function. It is a meta heuristic to approximate the global optimization in a large search space. The algorithm is as follow [3,4]:

Random partition
Compute initial cost
Do {
		For ITTERATION:
			select two randomCells
			gain=costOfSwitchingPartitionOfSelectedCells 
			 if(gain>0):
				switch partition of selected cell
			else: 
		                             r= randomNumber
		                             if ( r < exp(gain/T) )
					don’t switch partition of selected cells
				else
					switch partition of selected cells
		endFor
		Update T
} while(cost<CONDITION)

ITERATION, CONDITION and T update rule is the annealing schedule. The best annealing schedule found after trying lots of combination
T: The initial value of T =40, this was the optimal initial value for T.
CONDITION:(cost<.0000025)
ITTERATION: Number of ITTERATION = 10*numberOfCells^(4/3) ,the number of iteration should depends on the number of cells to be partitioned since using constant number of iteration would either takes lots of time even for smaller circuit, if the number of iteration is tuned for best performance on larger circuit or it does not produce optimum partition for larger circuit, if its tuned for smaller circuit. Using this number of iteration I was able to get the optimum partition within a reasonable time.
RUNTIME OPTIMIZATION: Since simulated annealing is a slow method so to make the algorithm run fast we have done some optimization like enabled the compiler O3 optimization and approximated the computation of exp(-A/T) by 1 - A/T since exp(-A/T) is computed many times and considerable savings in computation times (as much as 30%) are made without noticeable degradation of the quality of solutions

