#!/usr/bin/python
#from joblib import Parallel,delayed
from math import exp
import timeit
import numpy as np
from graphics import *
from random import randint
from random import shuffle 
import sys
import random
import copy
import math
INFINITY=99999

#This mapping array is numberOfCells x numberOfCells sized.
#It has the mapping of all cell connections i.e. which cell is connected to which other cells.
netToCell	=[]
cellToNet	=[]
netSize		=[]
partition	=[]
minPartition	=[]
gain		=[]
lock		=[]
cellRowPlacement=[]
cellColPlacement=[]
mapping=[]
COL_SIZE_MAX=1000
ROW_SIZE_MAX=600

with open(sys.argv[1]) as f:
#These lines parse the input file and create the mapping array.
	templine=f.readline()
	line1=map(float,templine.split())
	numberOfCells=int (line1[0])
	numberOfNets=int (line1[1])
	numberOfRow=int (line1[2])
	numberOfCol=int (line1[3])
	netToCell= [[0 for x in range(numberOfCells)] for y in range(numberOfNets)] 
	cellToNet= [[0 for x in range(numberOfNets)] for y in range(numberOfCells)] 
	netSize  = [-1 for x in range(numberOfNets)] 
	partition	= [0 for x in range(numberOfCells)] 
	minPartition	= [-1 for x in range(numberOfCells)]
	gain		= [-1 for x in range(numberOfCells)]
	lock		= [ 0 for x in range(numberOfCells)]
	cellRowPlacement= [-1 for x in range(numberOfCells)] 
	cellColPlacement= [-1 for x in range(numberOfCells)]
	mapping= [[0 for x in range(numberOfCells)] for y in range(numberOfCells)] 
	dia= [[0 for x in range(numberOfCells)] for y in range(numberOfCells)] 
	
	for i in range(0,numberOfNets):
		templine=f.readline()
		line=map(float,templine.split())
		netSize[i]=line[0]
		for j in range(1,int(line[0]+1)):
			netToCell[int(i)][int(j-1)]=line[j]
			cellToNet[int(line[j])][int(i)]=1
			if(j>1):
				mapping[int(line[1])][int(line[j])]=1

col_scaling=COL_SIZE_MAX/(2.2*numberOfCol)
row_scaling=ROW_SIZE_MAX/numberOfRow
#This function clear the screen. This is used to clear the old placement from the screen for printing the latest placement
def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

#This function place the cell in random configuration 		
def randomPlacement():
	for i in range(0,numberOfCells):
		while True:
			row=randint(0,numberOfRow-1)
			col=randint(0,numberOfCol-1)
			already_assigned=0	
			#searching for whether the row and col already assigned
			for j in range(0,numberOfCells):
				if ((row==cellRowPlacement[j])and(col==cellColPlacement[j])):
					already_assigned=1
			#already assigned=1 not assigned exit while
			if(already_assigned==0):
				cellRowPlacement[i]=row
				cellColPlacement[i]=col
				break
#This function draw the grid where we have to do the placement	
def drawGrid(win):
	grid=Rectangle(Point(0,0),Point((numberOfCol)*col_scaling,(numberOfRow)*row_scaling));
	grid.setFill(color_rgb(255,229,204))
	grid.draw(win)
	grid=Rectangle(Point(numberOfCol*col_scaling,0),Point((2*numberOfCol)*col_scaling,(numberOfRow)*row_scaling));
	grid.setFill(color_rgb(204,255,209))
	grid.draw(win)
	for i in range(0,numberOfCol):
		grid = Line(Point(i*col_scaling, 0), Point(i*col_scaling, ROW_SIZE_MAX)) # set endpoints
		grid.setWidth(3)
		grid.draw(win)
	for j in range(0,numberOfRow):
		grid = Line(Point(0, j*row_scaling), Point(COL_SIZE_MAX, j*row_scaling)) # set endpoints
		grid.setWidth(3)
		grid.draw(win)
	for i in range(numberOfCol,2*numberOfCol):
		grid = Line(Point(i*col_scaling, 0), Point(i*col_scaling, ROW_SIZE_MAX)) # set endpoints
		grid.setWidth(3)
		grid.draw(win)
	

#This function draw the current placement on the grid
def drawPlacement(win):
	clear(win)
	drawGrid(win)
	for i in range(0,numberOfCells):
		for j in range(0,numberOfCells):
			if(mapping[i][j]==1):
				if(partition[i]==partition[j]):
					if(partition[i]==0):
						grid = Line(Point(cellColPlacement[i]*col_scaling+col_scaling/2,cellRowPlacement[i]*row_scaling+row_scaling/2),Point(cellColPlacement[j]*col_scaling+col_scaling/2,cellRowPlacement[j]*row_scaling+row_scaling/2))
						grid.setFill(color_rgb(0,0,204))
					else:
						grid = Line(Point((cellColPlacement[i]+numberOfCol)*col_scaling+col_scaling/2,cellRowPlacement[i]*row_scaling+row_scaling/2),Point((cellColPlacement[j]+numberOfCol)*col_scaling+col_scaling/2,cellRowPlacement[j]*row_scaling+row_scaling/2))
						grid.setFill(color_rgb(153,76,0))
				else:
					if(partition[i]==0):
						grid = Line(Point(cellColPlacement[i]*col_scaling+col_scaling/2,cellRowPlacement[i]*row_scaling+row_scaling/2),Point((numberOfCol+cellColPlacement[j])*col_scaling+col_scaling/2,cellRowPlacement[j]*row_scaling+row_scaling/2))	
						grid.setFill(color_rgb(255,0,0))
					else:
						grid = Line(Point((cellColPlacement[i]+numberOfCol)*col_scaling+col_scaling/2,cellRowPlacement[i]*row_scaling+row_scaling/2),Point((cellColPlacement[j])*col_scaling+col_scaling/2,cellRowPlacement[j]*row_scaling+row_scaling/2))
						grid.setFill(color_rgb(255,0,0))
				grid.setWidth(5)
				grid.draw(win)

def randomPartition():
	x = [i for i in range(numberOfCells)]
	shuffle(x)
	for i in range(0,int(numberOfCells/2)):
		partition[int(x[i])]=1

def checkAvailableNodes():
	for i in range(0,numberOfCells):
		if(lock[i]==0):
			return 1
	return 0

def gainCalculation():
	for cell in range(0,numberOfCells):
		cost1=0
		cost2=0
		cellPartition=partition[cell]
		for net in range(0,numberOfNets):
			if(cellToNet[cell][net]==1):
				count=0
				for netElement in range(0,int(netSize[net])):
					cellOnNet=netToCell[net][netElement]
					if(partition[int(cellOnNet)]==cellPartition):
						count=count+1
				if(count==1):
					cost1=cost1+1
				if(count==netSize[net]):
					cost2=cost2+1
		gain[cell]=cost1-cost2			
def totalCross():
	num_cross=0	
	for net in range(0,numberOfNets):
		sourcePartition=partition[int(netToCell[net][0])]
		for destination in range(1,int(netSize[net])):
			if(partition[int(netToCell[net][destination])]!=sourcePartition):
				num_cross=num_cross+1	
	return num_cross

def cutSize():
	cutsz=0
	for net in range(0,numberOfNets):
		sourcePartition=partition[int(netToCell[net][0])]
		for destination in range(1,int(netSize[net])):
			if(partition[int(netToCell[net][destination])]!=sourcePartition):
				cutsz=cutsz+1
				break
	return cutsz

def findMaximumGain(currentPartition):
	maxGain=-INFINITY
	maxIndex=0
	for cell in range(0,numberOfCells):
		if((partition[cell]==currentPartition)and(lock[cell]==0)):
			if(maxGain<gain[cell]):
				maxGain=gain[cell]
				maxIndex=cell	
	return maxIndex
	
def main():
	start = timeit.default_timer()
	for i in range(0,numberOfCells):
		for j in range(0,numberOfCells):
			if((mapping[i][j]==1) and (mapping[j][i]!=1)):
				mapping[j][i]=1
			if((mapping[i][j]!=1) and (mapping[j][i]==1)):
				mapping[i][j]=1
	adjacency=np.array(mapping)
	for i in range(0,numberOfCells):
		count=0
		for j in range(0,numberOfCells):
			if(mapping[i][j]==1):
				count=count+1
		dia[i][i]=count
	diagonal=np.array(dia)
	Laplacian=diagonal-adjacency
	eigvals, eigvecs = np.linalg.eig(Laplacian)
	flat_eigvals=eigvals.flatten()
	secondmaxvalue=np.partition(flat_eigvals,1)[1]
	loc=np.where(eigvals==secondmaxvalue)[0]
	maxindex=loc[0]
	vect=eigvecs[:,maxindex]
	temp_vect=copy.deepcopy(vect)
	temp_vect.flatten()
	temp_vect.sort()
	mid_val=temp_vect[int(numberOfCells/2)]
	for i in range(0,numberOfCells):
		if(vect[i]<mid_val):
			partition[i]=0		
		else:
			partition[i]=1
	#Local Improvement using FM
	minCutSize=INFINITY
	currentPartition=0
	while(checkAvailableNodes()):
		gainCalculation()
		cl=findMaximumGain(currentPartition)
		partition[cl]=1-currentPartition
		lock[cl]=1
		currentCutSize=cutSize()
		currentWireCross=totalCross()
		if(currentCutSize<minCutSize):
			minCutSize=currentCutSize
			for i in range(0,numberOfCells):
				minPartition[i]=partition[i]		
		currentPartition=1-currentPartition
	stop = timeit.default_timer()
        print " The best partition"
	for i in range(0,numberOfCells):
		partition[i]=minPartition[i]
                print(partition[i]),		
	print("\n")
        currentCutSize=cutSize()
	currentWireCross=totalCross()
	print "minimumCutSize=%d" %(currentCutSize)
	print "Time taken for the placement =%f" %(stop-start)
        
	win = GraphWin("Partition", col_scaling*2*numberOfCol, row_scaling*numberOfRow)
	randomPlacement()
	drawPlacement(win)
	win.getMouse() # pause for click in window
	win.close()
main()
