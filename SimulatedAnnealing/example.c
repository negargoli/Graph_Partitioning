#include <stdlib.h>
#include <stdio.h>
#include "graphics.h"
#include <math.h>
#include<time.h>
#define INF 10000
 
static void delay (void);
static void button_press (float x, float y);
static void drawscreen (void);
int number_of_cell;
int number_of_net;
int gridsize_row;
int gridsize_col;

int **cell_to_net_mapping;
int **net_to_cell_mapping;
int *net_size;

struct node{
	int partition;
	int initial_partition;
	float gain;
	int lock;
	int moved_step;
};
struct node *cell;


void unlock(){
	int i;
	for(i=0;i<number_of_cell;i++){
		cell[i].lock=0;		
	}
}

int is_available_unlock_nodes(){
	int i;
	for(i=0;i<number_of_cell;i++){
		if(cell[i].lock==0)
			return 1;
	}
	return 0;
}
void random_partition(){
	int i,count;
	count=0;
	for(i=0;i<number_of_cell;i++){
		cell[i].partition=0;
		cell[i].initial_partition=0;
		cell[i].gain=0;
		cell[i].lock=0;
		cell[i].moved_step=-1;
	}
	while(1){
		i=rand()%number_of_cell;
		if(cell[i].partition!=1){
			cell[i].partition=1;
			cell[i].initial_partition=1;
			count++;
		}
		if(count==((int)number_of_cell/2))
			break;
	}
}

//int given_cell_only_in_the_partition_of_a_given_net(int cell_index){
float cost(int cell_index){
	
	int k,i,net,count,partition;
	float cost1=0;
	float cost2=0;
	for(k=0;k<number_of_net;k++){
		if(cell_to_net_mapping[cell_index][k]==1){
			net=k;
			count=0;
			partition=cell[cell_index].partition;

			for(i=0;i<net_size[net];i++){
				if(cell[net_to_cell_mapping[net][i]].partition==partition)
					count++;	
			}
			if(count==1)
				cost1++;
			
			if(count==net_size[net])
				cost2++;
		}
	}
	return cost1-cost2;
}

void gain_calculation(){
	
	int i;
	for (i=0;i<number_of_cell;i++){
		cell[i].gain=cost(i);	
	}
}
int cut_set_size(){
	int i,net,j,source_partition,cut_size;
	cut_size=0;
	for(net=0;net<number_of_net;net++){
		source_partition=cell[net_to_cell_mapping[net][0]].partition;
		for(j=1;j<net_size[net];j++){
			if(cell[net_to_cell_mapping[net][j]].partition==(!source_partition)){
				cut_size++;
				break;
			}
		}
	}
	return cut_size;
}

int find_maximum(int partition){
	int i;
	int max_index;
	float max_gain;
	max_index=-1;
	max_gain=-INF;
	for(i=0;i<number_of_cell;i++){	
		if(cell[i].partition==partition&&cell[i].lock==0){
			if(max_gain<cell[i].gain){
					max_gain=cell[i].gain;
					max_index=i;
			}
		}
		if(partition==-1){
			if(max_gain<cell[i].gain){
				max_gain=cell[i].gain;
				max_index=i;
			}
		}
	}
	return max_index;
}

// make random number for r 
double random_between_0to1(){
	return (double)rand()/(double)RAND_MAX;
}


int main(int argc, char **argv) {
	clock_t start,end;
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
	int passes;
	srand(time(NULL));
	printf("circuit=%s\n",argv[1]);
	start=clock();
 // reading the file parameters
 	file = fopen(argv[1], "r");
 	fscanf(file,"%d %d %d %d",&number_of_cell,&number_of_net,&gridsize_row,&gridsize_col);
    	
 	cell_to_net_mapping= malloc(sizeof(int *)*number_of_cell);
	for(i=0;i<number_of_cell;i++) 
		*(cell_to_net_mapping+i)=malloc(sizeof(int)*number_of_net);
	
	net_size=malloc(sizeof(int)*number_of_net);
	
 	net_to_cell_mapping= malloc(sizeof(int *)*number_of_net);
	for(i=0;i<number_of_net;i++) 
		*(net_to_cell_mapping+i)=malloc(sizeof(int)*number_of_cell);

	for(i=0;i<number_of_cell;i++){
		for(j=0;j<number_of_net;j++)
			cell_to_net_mapping[i][j]=0;
	}

	for(i=0;i<number_of_net;i++){
		for(j=0;j<number_of_cell;j++)
			net_to_cell_mapping[i][j]=-1;
	}

 	for(i=0;i<number_of_net;i++){
		fscanf(file,"%d ",&temp);
		net_size[i]=temp;
		for(j=0;j<temp;j++){
			fscanf(file,"%d ",&destination);
			net_to_cell_mapping[i][j]=destination;
			cell_to_net_mapping[destination][i]=1;	
		}
	}
  	

	cell=(struct node *) malloc(sizeof(struct node )*number_of_cell);
	random_partition();
	int current_cell_partition,beforeSwapCutsize,afterSwapCutsize;
	int current_cell,swapping_cell;
	int ITTERATION=10*number_of_cell^(4/3); 	
	float T=40;
	float alpha=0.98;
	do{
		for(j=0;j<ITTERATION;j++){	
			current_cell=(int)random()%number_of_cell;	
			current_cell_partition=cell[current_cell].partition;
			do{
				swapping_cell=(int)random()%number_of_cell;
				if(cell[swapping_cell].partition!=current_cell_partition){
					break;	
				}
			}while(1);
			beforeSwapCutsize=cut_set_size();
			//swapping
			cell[current_cell].partition=1-cell[current_cell].partition;
			cell[swapping_cell].partition=1-cell[current_cell].partition;
			afterSwapCutsize=cut_set_size();
			
			if(afterSwapCutsize>beforeSwapCutsize){
      				float r=random_between_0to1();
      				float temp_compare=exp(-((float)((float)afterSwapCutsize-(float)beforeSwapCutsize)/T)); 
				float condition=exp(-((float)(afterSwapCutsize-beforeSwapCutsize)/T));
				if(!((int)(r*10000)<((int)10000*condition))){
					cell[current_cell].partition=1-cell[current_cell].partition;
					cell[swapping_cell].partition=1-cell[current_cell].partition;
				}
			}
		}
    		// update the T        
		T=alpha*T;
	}while(T>.0000025);

	current_cut_size=cut_set_size();

	printf("Final_cut_size=%d\n",current_cut_size);


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


