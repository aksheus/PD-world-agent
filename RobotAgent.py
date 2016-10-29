class RobotAgent:
	"""
	   maintains state of pd world  and provides methods to update pd world
	   w.r.t to actions of our robot agent  """
	def __init__(self,robos_position,pickupCells,dropoffCells):
		""" what are the attributes that we need   ??? 
			format of state:
			state = [X_pos_of_robot,Y_pos_of_robot,carry_flag,number_of_stars_first pickup cell,
						number of stars for 2nd pickup cell, number for 3rd,
						number of stars in first drop of cell, 
						number of stars in second dropff cell,
						number of starts in third dropoff cell
						]
			pickupCells and dropofCells are used to know the coordinates of the pickup and dropoff cells repectively
			their format = [(x1,y1), (x2,y2), (x3,y3)]
		"""
		# these variables are just to initialize our state there is no need to update them 
		self.robos_position=robos_position 
		self.pickupCells=pickupCells # should we keep em as list or set  ?? Let's see
		self.dropoffCells=dropoffCells 
		self.carry=0 # 0 if robo carrying nothing 1 if it carries a star
		# this our actual state which needs to be updated its a list update it carefully
		self.state=[self.robos_position[0],self.robos_position[1],0,5,5,5,0,0,0] # since robot always starts at (1,5) and does not carry anything initially
		# this state attribute reperesents current state and must be updated accordingly
		self.adj_move=[(1,0,'d'),(0,1,'r'),(-1,0,'u'),(0,-1,'l')] # this is just to calculate robots neighbouring coordinates
		self.robo_scope=[]
		self.goal_counter=0
	
	def possibleMoves(self):
		""" sees what possible squares the robo can move to legally
		      and updates robo_scope variable"""
		self.robo_scope=[]
		for x,y,z in self.adj_move:
			temp=(self.state[0]+x,self.state[1]+y,z)
			if temp[0]>0 and temp[0]<6: #    1<=x<=5
				if temp[1]>0 and temp[1]<6: # 1<=y<=5
					self.robo_scope.append(temp)

	def doPickup(self,pickup_cell): #provide the pickup cell returns true if we did pick up !!
		if (self.state[0],self.state[1])==pickup_cell: #check wether the agent is on the pickup cell
			if pickup_cell in self.pickupCells and self.state[2]==0: # is the agent is not carrying a star, is the pickup cell indeed a pickupcell
				p=self.state[self.pickupCells.index(pickup_cell)+3]
				if p>0: # the pickup cell must have atleast one star
					self.state[self.pickupCells.index(pickup_cell)+3]-=1
					self.state[2]=1 # updating carry flag
					return True 
		return False

	def doDropoff(self,dropoff_cell): # provide pick up cell as tuple returns true if drop off is successful
		if (self.state[0],self.state[1])==dropoff_cell: # is the robo on the drop off cell
			if dropoff_cell in self.dropoffCells and self.state[2]==1: # is the robo carrying a star , is the cell indeed a dropoff cell
				d=self.state[self.dropoffCells.index(dropoff_cell)+6]
				if d<5: # the drop off cell can't hold more than 5
					self.state[self.dropoffCells.index(dropoff_cell)+6]+=1
					self.state[2]=0 #updating carry flag
					return True
		return False

	def goalStateCheck(self): #returns true if goal state is reached otherwise false
		if (self.state[3],self.state[4],self.state[5])==(0,0,0):
			if (self.state[6],self.state[7],self.state[8])==(5,5,5):
				return True
		return False








	




		












