#include <stdlib.h>
#include <stdio.h>
#include "graphics.h"
#include <math.h>
#include<time.h>
#include <stdbool.h>
#define INF 1000000
#define NUMBER_OF_POPULATION 100 
#define NUM_CUTPOINT  5 
static void delay (void);
static void button_press (float x, float y);
static void drawscreen (void);
int number_of_cell;
int number_of_net;
int gridsize_row;
int gridsize_col;
int best;

int **cell_to_net_mapping;
int **net_to_cell_mapping;
int **connected_matrix;
int *net_size;

float fitness_score[NUMBER_OF_POPULATION];

int cutsize[NUMBER_OF_POPULATION];
int cutsize_temp[NUMBER_OF_POPULATION];
int min_cutsize_ptr;
int max_cutsize_ptr;

struct node{
  int row; 
  int col; 
  int partition[NUMBER_OF_POPULATION]; // we have two partition 
  int offspring_partition; 
  int best_partition; 
  float gain;
  int lock;  // if a node is locked we can not move it anymore
  //int moved_step;  // in which movement this node goes from one partition to the other partition
};
struct node *cell;

// Merges two subarrays of arr[].
// First subarray is arr[l..m]
// Second subarray is arr[m+1..r]
void merge(int arr[], int l, int m, int r)
{
    int i, j, k;
    int n1 = m - l + 1;
    int n2 =  r - m;
 
    /* create temp arrays */
    int L[n1], R[n2];
 
    /* Copy data to temp arrays L[] and R[] */
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1+ j];
 
    /* Merge the temp arrays back into arr[l..r]*/
    i = 0; // Initial index of first subarray
    j = 0; // Initial index of second subarray
    k = l; // Initial index of merged subarray
    while (i < n1 && j < n2)
    {
        if (L[i] <= R[j])
        {
            arr[k] = L[i];
            i++;
        }
        else
        {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    /* Copy the remaining elements of L[], if there
       are any */
    while (i < n1)
    {
        arr[k] = L[i];
        i++;
        k++;
    }
 
    /* Copy the remaining elements of R[], if there
       are any */
    while (j < n2)
    {
        arr[k] = R[j];
        j++;
        k++;
    }
}
 
/* l is for left index and r is right index of the
   sub-array of arr to be sorted */
void mergeSort(int arr[], int l, int r)
{
    if (l < r)
    {
        // Same as (l+r)/2, but avoids overflow for
        // large l and h
        int m = l+(r-l)/2;
 
        // Sort first and second halves
        mergeSort(arr, l, m);
        mergeSort(arr, m+1, r);
 
        merge(arr, l, m, r);
    }
}



int if_already_assigned(int row,int col){
	int i,j;
	for(i=0;i<number_of_cell;i++){
		if((row==cell[i].row)&&(col==cell[i].col)){
			return 1;
		}
	}
	return 0;	
}

void unlock(){
	int i;
	for(i=0;i<number_of_cell;i++){
		cell[i].lock=0;		
	}
}
// find out is there any node available anymore which can be moved
int is_available_unlock_nodes(){
	int i;
	for(i=0;i<number_of_cell;i++){
		if(cell[i].lock==0)
			return 1;
	}
	return 0;
}
//Random Generating the population pool
void random_partition(){
	int i,count,j;
	for(i=0;i<number_of_cell;i++){
		for(j=0;j<NUMBER_OF_POPULATION;j++)
			cell[i].partition[j]=0;
		cell[i].gain=0;
		cell[i].lock=0;
		cell[i].offspring_partition=0;
	}
	for(j=0;j<NUMBER_OF_POPULATION;j++){
		count=0;
		while(1){
			i=rand()%number_of_cell; // find random cell and assign it to one of the partitions ( partition 1)
			if(cell[i].partition[j]!=1){
				cell[i].partition[j]=1;
				count++;
			}
			if(count==((int)number_of_cell/2)) // half of the nodes are in one partition and the other half in another partition
				break;
		}
	}
}

// find cost 
float cost(int cell_index){
	
	int k,i,net,count,partition;
	float cost1=0;
	float cost2=0;
	for(k=0;k<number_of_net;k++){
		if(cell_to_net_mapping[cell_index][k]==1){
			net=k;
			count=0;
			partition=cell[cell_index].offspring_partition;

			for(i=0;i<net_size[net];i++){
				if(cell[net_to_cell_mapping[net][i]].offspring_partition==partition)
					count++;	
			}
			if(count==1)
				cost1++; // is it is the only node of the net which is in the opposite partition 
		
			if(count==net_size[net])
				cost2++; // if all the nodes of the net are in the same partition 
	
		}
	}
	return cost1-cost2;  // the total cost of a node 
}
// gain for each node is the cost of moving it to the other partition 
void gain_calculation(){
	int i;
	for (i=0;i<number_of_cell;i++){
		cell[i].gain=cost(i);	
	}
}
//population_member=-1 for child population
// find the cut size 
int cut_set_size(int population_member){
	int i,net,j,source_partition,cut_size;
	cut_size=0;
	if(population_member!=-1){
		  // go through all nets 
			for(net=0;net<number_of_net;net++){
		   // find the partition of the source node 
				source_partition=cell[net_to_cell_mapping[net][0]].partition[population_member];
				for(j=1;j<net_size[net];j++){
		      // if the sink node partition is different from the source partition the cutsize will increment 
					if(cell[net_to_cell_mapping[net][j]].partition[population_member]==(!source_partition)){
						cut_size++;
						break;
					}
				}
			}
	}
	else{
		  // go through all nets 
			for(net=0;net<number_of_net;net++){
		   // find the partition of the source node 
				source_partition=cell[net_to_cell_mapping[net][0]].offspring_partition;
				for(j=1;j<net_size[net];j++){
		      // if the sink node partition is different from the source partition the cutsize will increment 
					if(cell[net_to_cell_mapping[net][j]].offspring_partition==(!source_partition)){
						cut_size++;
						break;
					}
				}
			}
	}
	return cut_size;
}
// find the cutsize for all the members in the population
void population_cutsize(){
	int i;
	for(i=0;i<NUMBER_OF_POPULATION;i++){
		cutsize[i]=cut_set_size(i);
	}
}
// according to the paper's formula find the fitness score for each member of the population
void population_fitness(){
	int i;
	int min_cut_size=INF;
	int max_cut_size=-INF;
        // find the min and max cut_size in the population 
	for(i=0;i<NUMBER_OF_POPULATION;i++){
		if(min_cut_size>cutsize[i]){
			min_cut_size=cutsize[i];
			min_cutsize_ptr=i;
		}
		if(max_cut_size<cutsize[i]){
			max_cut_size=cutsize[i];
			max_cutsize_ptr=i;
		}
	}
	
	for(i=0;i<NUMBER_OF_POPULATION;i++){
		fitness_score[i]=cutsize[max_cutsize_ptr]-cutsize[i]+(cutsize[max_cutsize_ptr]-cutsize[min_cutsize_ptr])/3.0;
	}
}
// select the two parents which want to produce the offspring according to their fitness
// The ones with higher fitness have higher chance to be chosen 
void parents_selection(int * parent1,int * parent2){
	int sum_of_weight,i;
	sum_of_weight=0;
	for( i=0;i<NUMBER_OF_POPULATION;i++){
		sum_of_weight+=(int)(3.0*fitness_score[i]);	
	}	
	int rnd =rand()%sum_of_weight;
	for(i=0;i<NUMBER_OF_POPULATION;i++){
		if(rnd<((int)(3.0*fitness_score[i]))){
			*parent1=i;
			break;
		}
		rnd-=(int)(3.0*fitness_score[i]);
	}
        // search for paret two 
        sum_of_weight=0;
	for( i=0;i<NUMBER_OF_POPULATION;i++){
		if(i!= (*parent1))
			sum_of_weight+=(int)(3.0*fitness_score[i]);	
	}
	int rnd2 =rand()%sum_of_weight;
	for(i=0;i<NUMBER_OF_POPULATION;i++){
		if(i!=(*parent1)){
			if(rnd2<((int)(3.0*fitness_score[i]))){
				*parent2=i;
				break;
			}
			rnd2-=(int)(3.0*fitness_score[i]);
		}
	}
}
// creat offspring by 
void crossover(int parent1,int parent2){
 
        /************************ Use Bernulie distribution ***************************/
        int i;
        bool randbool;
        for( i=0 ; i<number_of_cell ; i++)
        {
            
            randbool = rand() & 1;
            if(randbool==0)
             	cell[i].offspring_partition=cell[i].partition[parent1];
            else
		cell[i].offspring_partition=cell[i].partition[parent2];

        }


       /*************************** End ***************************************/
}
// make the offspring balanced by randomly change the number of ones and zeros  
void mutation(){
	int number_of_zeros,number_of_ones,diff,odd;
	int i,pos;
	number_of_zeros=number_of_ones=0;
	for(i=0;i<number_of_cell;i++){
		if(cell[i].offspring_partition==0)
			number_of_zeros++;
		else
			number_of_ones++;
	}
	diff=number_of_zeros-number_of_ones;
	odd=number_of_cell%2;	
	if(abs(diff)!=odd){
		do{
			do{
			 	pos=rand()%number_of_cell;
				if((diff>0)&(cell[pos].offspring_partition==0))
					break;
				if((diff<0)&(cell[pos].offspring_partition==1))
					break;

			}while(1);
			cell[pos].offspring_partition=!(cell[pos].offspring_partition);
			if(diff>0)
				diff=diff-2;
			else
				diff=diff+2;
		
		}while(abs(diff)!=odd);
	}
}
// replace the offspring with the largest hamming distance wih offspring and worst fitness score 
void replacement(int parent1,int parent2){	
	int i,j,hamming_distance[NUMBER_OF_POPULATION],max_distance,max_distance_min_fitness_index,temp_fit;
	int cutsize_offspring,randsel;
	for(i=0;i<NUMBER_OF_POPULATION;i++){
		hamming_distance[i]=0;
		for(j=0;j<number_of_cell;j++){
			if(cell[j].partition[i]!=cell[j].offspring_partition)
				hamming_distance[i]=hamming_distance[i]+1;
		}
	}
	max_distance=-INF;
	for(i=0;i<NUMBER_OF_POPULATION;i++){
		if(max_distance<hamming_distance[i]){
			max_distance=hamming_distance[i];
		}
	}
	temp_fit=INF;
        // find the one in the population which has the max hamming distance and the worst fitness score
	for(i=0;i<NUMBER_OF_POPULATION;i++){
		if(hamming_distance[i]==max_distance){
			if(temp_fit>((int)(3.0*fitness_score[i]))){	
				temp_fit=(int)(3.0*fitness_score[i]);
				max_distance_min_fitness_index=i;
			}
		}
	}
	cutsize_offspring=cut_set_size(-1);//-1 correspond to cutsize of offspring	
	for(i=0;i<number_of_cell;i++){
			cell[i].partition[max_distance_min_fitness_index]=cell[i].offspring_partition;	
			cutsize[max_distance_min_fitness_index]=cutsize_offspring;
	}
}

int stop_condition_met(){
	int i,count=0,diversity=0;
	int max,val,stop_condition;
	for(i=0;i<NUMBER_OF_POPULATION;i++){
		cutsize_temp[i]=cutsize[i];		
	}
	mergeSort(cutsize_temp, 0, NUMBER_OF_POPULATION- 1);	
	val=cutsize_temp[0];
	max=1;
	count=diversity=1;
        
	for(i=1;i<NUMBER_OF_POPULATION;i++){
		if(cutsize_temp[i]!=val){
			val=cutsize_temp[i];
			if(max<count)
				max=count;
			count=0;
			diversity++;	
		}	
		else{
			count++;
		}
	}
	stop_condition=((int) (10*NUMBER_OF_POPULATION/100));
	printf("diversity=%d stop_condition=%d\n",diversity,stop_condition);	
	if(diversity<=stop_condition)
		return 1;
	else
		return 0;
}

//// find the node which has the max gain in the given partition 
int find_maximum(int partition){
	int i;
	int max_index;
	float max_gain;
	max_index=-1;
	max_gain=-INF;
	for(i=0;i<number_of_cell;i++){	
		if(cell[i].offspring_partition==partition&&cell[i].lock==0){
			if(max_gain<cell[i].gain){
					max_gain=cell[i].gain;
					max_index=i;
			}
		}
     // the first time we should find the max gain through all the nodes in both partitions 
		if(partition==-1){
			if(max_gain<cell[i].gain){
				max_gain=cell[i].gain;
				max_index=i;
			}
		}
	}
	return max_index;
}

int main(int argc, char **argv) {
 	int i,j,temp;
 	FILE *file;
	int destination;
	int k;
	int step;
	int cell_index_of_max_gain;
	int current_partition;
	int step_min_cut;
	int min_cut_val;
	int current_cut_size;
	clock_t start, end; 
        int passes,diversity;
	int parent1,parent2;
	srand(time(NULL));
	start=clock();
 // reading the file parameters
 	printf("circuit=%s\n",argv[1]);
	file = fopen(argv[1], "r");
 	fscanf(file,"%d %d %d %d",&number_of_cell,&number_of_net,&gridsize_row,&gridsize_col);
    	
 	cell_to_net_mapping= malloc(sizeof(int *)*number_of_cell);
	for(i=0;i<number_of_cell;i++) 
		*(cell_to_net_mapping+i)=malloc(sizeof(int)*number_of_net);
	
	net_size=malloc(sizeof(int)*number_of_net);
	
 	net_to_cell_mapping= malloc(sizeof(int *)*number_of_net);
	for(i=0;i<number_of_net;i++) 
		*(net_to_cell_mapping+i)=malloc(sizeof(int)*number_of_cell);
 	
  connected_matrix= malloc(sizeof(int *)*number_of_cell);
	for(i=0;i<number_of_cell;i++) 
		*(connected_matrix+i)=malloc(sizeof(int)*number_of_cell);
	for(i=0;i<number_of_cell;i++){
		for(j=0;j<number_of_cell;j++)
  connected_matrix[i][j]=0;
  }
   
	for(i=0;i<number_of_cell;i++){
		for(j=0;j<number_of_net;j++)
			cell_to_net_mapping[i][j]=0;
	}

	for(i=0;i<number_of_net;i++){
		for(j=0;j<number_of_cell;j++)
			net_to_cell_mapping[i][j]=-1;
	}
   int source;
   //creat two array to save the which cell is in which net and visa versa
 	for(i=0;i<number_of_net;i++){
		fscanf(file,"%d ",&temp);
		net_size[i]=temp;
		for(j=0;j<temp;j++){
			fscanf(file,"%d ",&destination);
      if(j==0)
         source=destination; 
      else
        connected_matrix[source][destination]=1;
        
			net_to_cell_mapping[i][j]=destination;
			cell_to_net_mapping[destination][i]=1;	
		}
	}

  cell=(struct node *) malloc(sizeof(struct node )*number_of_cell);
  // do the random population generation 
  random_partition();
  population_cutsize();
  passes=0; 
  int mm=1000;
  do{
	 population_fitness();
 	 parents_selection(&parent1,&parent2);
	 crossover(parent1,parent2);
 	 mutation();
/**************************************** FM ************************************/ 
	 int pass;
         for ( pass=0 ; pass<1 ; pass++)
         {
         gain_calculation();
  	 current_cut_size=cut_set_size(-1);
	 min_cut_val=current_cut_size;
	 for(i=0;i<number_of_cell;i++)
		cell[i].best_partition=cell[i].offspring_partition;

	 if(number_of_cell%2==0)
		temp=find_maximum(-1);
	 else{
		temp=find_maximum(0);//0 partition will be having more elements
	 }
      	 current_partition=cell[temp].offspring_partition;
	 do{
	 	gain_calculation();
  	 	cell_index_of_max_gain=find_maximum(current_partition);
	 	cell[cell_index_of_max_gain].offspring_partition= (!current_partition);
         	cell[cell_index_of_max_gain].lock=1;
  	 	current_cut_size=cut_set_size(-1);
	 	if(current_cut_size<min_cut_val){
	 	       min_cut_val=current_cut_size;
	 		for(i=0;i<number_of_cell;i++)
	 	       	cell[i].best_partition=cell[i].offspring_partition;
	 	}
	 	current_partition=!current_partition; 
	 	mm--;
  	 }while(is_available_unlock_nodes()); 
	 for(i=0;i<number_of_cell;i++)
  	 	cell[i].lock=0;
	 for(i=0;i<number_of_cell;i++)
		cell[i].offspring_partition=cell[i].best_partition;
         }
	 /**********************************************end of FM **************************************/
         replacement(parent1,parent2);
	passes++;
 }while(!stop_condition_met());

	for(i=0;i<NUMBER_OF_POPULATION;i++){
		printf("%f ",fitness_score[i]);
	}
	printf("\n");
	current_cut_size=INF;
	mergeSort(cutsize, 0, NUMBER_OF_POPULATION- 1);	
	for(i=0;i<NUMBER_OF_POPULATION;i++){
       		if(current_cut_size>cutsize[i])
		     {	
                       current_cut_size=cutsize[i];
                       best=i;
                      }
		printf("%d ",cutsize[i]);
	 }
	printf("\nFinal_cut_size=%d\n",current_cut_size);
	end=clock(); 
        printf("time in milliseond=%ld\n",(end-start)*1000/CLOCKS_PER_SEC);
        printf("the final partitioing\n");
        for(i=0;i< number_of_cell;i++)
        {
          printf(" %d ", cell[i].partition[best]);
        }  
        printf("\n");
// This part is for graphic 

// /* initialize display */

 init_graphics("Some Example Graphics");
 init_world (0.,0.,2*gridsize_col,gridsize_row);
  int temp_row; 
  int temp_col; 
  for(i=0;i<number_of_cell;i++){
		do{
			temp_row=(int) random()%gridsize_row;
			temp_col=(int) random()%(gridsize_col); 
		}while(if_already_assigned(temp_row,temp_col));		
		cell[i].row=temp_row;
		cell[i].col=temp_col;
  }
 while(1)
{
  setcolor (BLACK);
  setlinewidth(5);
  setlinestyle (SOLID);
  drawline (gridsize_col,0.,gridsize_col,gridsize_row);
 // draw initial placement 
  setlinewidth(0.2);
  for(i=0;i<number_of_cell;i++){
  if( cell[i].partition[best]== 0 )
   fillrect( cell[i].col , cell[i].row , cell[i].col+0.2 , cell[i].row +0.2); 
  else 
   fillrect( cell[i].col+gridsize_col , cell[i].row , cell[i].col+gridsize_col+0.2 , cell[i].row +0.2); 
  } 

	for ( i=0 ; i<number_of_cell ; i++)
	{  
		for ( j=0 ; j<number_of_cell ; j++)
    		     if(connected_matrix[i][j]==1)
    		     {
    			if(cell[i].partition[best] ==0 && cell[j].partition[best] ==0)
			{
      				setcolor(BLUE);
				drawline(cell[i].col+0.1 , cell[i].row + 0.1 ,cell[j].col+0.1 , cell[j].row+0.1);
  			}
    			if(cell[i].partition[best] ==0 && cell[j].partition[best] ==1)
			{
      				setcolor(GREEN);
				drawline(cell[i].col+0.1 , cell[i].row+0.1,cell[j].col+gridsize_col+0.1 , cell[j].row+0.1);
  			}
     			if(cell[i].partition[best] ==1 && cell[j].partition[best]==1)
			{
      				setcolor(RED);
				drawline(cell[i].col+gridsize_col+0.1 , cell[i].row +0.1,cell[j].col+gridsize_col+0.1 , cell[j].row+0.1);
  			}
   
   	             }
   
   
	}

}

 return (0);
}

static void delay (void) {

/* A simple delay routine for animation. */

 int i, j, k, sum;

 sum = 0;
 for (i=0;i<1000;i++) 
    for (j=0;j<i;j++)
       for (k=0;k<30;k++) 
          sum = sum + i+j-k; 
}

static void button_press (float x, float y) {

/* Called whenever event_loop gets a button press in the graphics *
 * area.  Allows the user to do whatever he/she wants with button *
 * clicks.                                                        */

 printf("User clicked a button at coordinates (%f, %f)\n", x, y);
}


