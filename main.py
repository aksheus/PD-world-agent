from RobotAgent import RobotAgent
from random import choice,random,seed
from operator import itemgetter
import sys
from MainMenu import Mainmenu
from collections import deque
#this code just initializes the global q matrix btw we are going with state space representation 2  50x4 in size
# gonna use a dictionary for efficiency  .... key's are (i,j,x) tuples where i,j,x are the values in the problem speification ppt
# i is x-coordinate of robot,  j is y-cordinate of robot, x is 1 if its holding a star or it is zero otherwise
#  each key has a value of the type list  , [up,left,right,down,pickup,dropoff] the four actions , 0 is up ,1 is left ,2 is right ,3 is down
# 4 is pick up 5 is drop off 
l=[(x,y) for x in range(1,6) for y in range(1,6)]
m=[(x,y,0) for x,y in l]+[(x,y,1) for x,y in l]  #just initialization stuff
Q={ (x,y,z): [0,0,0,0,0,0] for x,y,z in m } # Q is our Q matrix
ulrd={ 0 :'u', 1 :'l' , 2 :'r' , 3:'d'}
counters=[0 for _ in range(6)]
get_seed= lambda x: 316+(100*x) # result should be different for different runs of the same experiment, but sequence of results should be same
bank_account=0
bank_account_forty=deque([],maxlen=40)

def R(did_we_pickup,did_we_drop): #reward function
	global bank_account,bank_account_forty
	if did_we_pickup or did_we_drop:
		bank_account+=13
		bank_account_forty.append(13)
		return 13
	else:
		bank_account+=-1
		bank_account_forty.append(-1)
		return -1

def weighted_choice(weights):
	"""  send weights in descending order returns index
		 according to weighted distribution"""
	rnd=random()*sum(weights)
	for i,w in enumerate(weights):
		rnd-=w
		if rnd<0:
			return i

def clear_Q():
	global m
	global Q
	for x,y,z in m:
		Q[(x,y,z)]=[0,0,0,0,0,0]

def Q_learning(robo,alpha=0.5,iterations=10000,policy='PRandom',special=False):  # implements q - learning algorithm
	"""
		Q(a,s) <-- (1-alpha)*Q(a,s)+ alpha*[R(s',a,s)+ gamma*max(Q(a',s'))] """
	global Q
	global ulrd
	gamma=0.3
	if policy=='PRandom':
		for _ in range(iterations):
			if robo.goalStateCheck():
				print('hey we got here')
				robo.goal_counter+=1
				if robo.goal_counter==4:
					print('hey we got here 4 times')
					return
				robo.state=[robo.robos_position[0],robo.robos_position[1],0,5,5,5,0,0,0]
				robo.robo_scope=[]
			robo.possibleMoves()
			s=(robo.state[0],robo.state[1],robo.state[2])
			move=choice(robo.robo_scope)
			did_we_pickup=robo.doPickup((s[0],s[1]))
			did_we_drop=robo.doDropoff((s[0],s[1]))
			if did_we_pickup==False and did_we_drop==False: # one operator at a time fellows , can't pick up and run immediately
				robo.state[0],robo.state[1]=move[0],move[1]
			ns=(robo.state[0],robo.state[1],robo.state[2]) # next state
			if did_we_pickup:
				Q[s][4]= (1-alpha)*Q[s][4] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
				continue
			if did_we_drop:
				Q[s][5]= (1-alpha)*Q[s][5] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
				continue			
			if move[2]=='u':
				Q[s][0]= (1-alpha)*Q[s][0] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			elif move[2]=='l':
				Q[s][1]= (1-alpha)*Q[s][1] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			elif move[2]=='r':
				Q[s][2]= (1-alpha)*Q[s][2] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			elif move[2]=='d':
				Q[s][3]= (1-alpha)*Q[s][3] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			print(s)
			print(Q[s])
			print('\n')
	elif policy=='PExploit1':
		for _ in range(iterations):
			if robo.goalStateCheck():
				robo.goal_counter+=1
				print('hey we got here')
				if special and robo.goal_counter==2:
					print('hey we got here 2 times')
					robo.pickupCells=[(2,2),(4,4),(1,5)] # set this .word document
				if robo.goal_counter==4:
					print('hey we got here 4 times')
					return
				robo.state=[robo.robos_position[0],robo.robos_position[1],0,5,5,5,0,0,0]
				robo.robo_scope=[] 
			robo.possibleMoves()
			s=(robo.state[0],robo.state[1],robo.state[2])
			# calculating max q value for possible operator with dice roll for ties
			qvalues=[(x,y) for x,y in enumerate(Q[s][:4])]
			possible_dirs=set([z for x,y,z in robo.robo_scope])
			qvalues=[(x,y) for x,y in qvalues if ulrd[x] in possible_dirs] # prune away non-applicable directions
			maximal_val=max(qvalues,key=itemgetter(1))
			maximal_values=[(x,y) for x,y in qvalues if y==maximal_val[1]]
			maximal_val=maximal_values[weighted_choice([1/len(maximal_values) for _ in range(len(maximal_values))])] #dice roll
			exploit_move=[(x,y,z) for x,y,z in robo.robo_scope if z==ulrd[maximal_val[0]]][0]
			# hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
			moves=[exploit_move,choice(robo.robo_scope)] # index 0 with probability 0.65 , index 1 with probbaility 0.35
			move=moves[weighted_choice([0.65,0.35])]
			did_we_pickup=robo.doPickup((s[0],s[1]))
			did_we_drop=robo.doDropoff((s[0],s[1]))
			if did_we_pickup==False and did_we_drop==False: # one operator at a time fellows , can't pick up and run immediately
				robo.state[0],robo.state[1]=move[0],move[1]
			ns=(robo.state[0],robo.state[1],robo.state[2]) # next state
			if did_we_pickup:
				Q[s][4]= (1-alpha)*Q[s][4] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
				continue
			if did_we_drop:
				Q[s][5]= (1-alpha)*Q[s][5] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
				continue	 
			if move[2]=='u':
				Q[s][0]= (1-alpha)*Q[s][0] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			elif move[2]=='l':
				Q[s][1]= (1-alpha)*Q[s][1] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			elif move[2]=='r':
				Q[s][2]= (1-alpha)*Q[s][2] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			elif move[2]=='d':
				Q[s][3]= (1-alpha)*Q[s][3] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			print(s)
			print(Q[s])
			print('\n')
	elif policy=='PExploit2':
		for _ in range(iterations):
			if robo.goalStateCheck():
				robo.goal_counter+=1
				print('hey we got here')
				if special and robo.goal_counter==2:
					print('hey we got here 2 times')
					robo.pickupCells,robo.dropoffCells=robo.dropoffCells,robo.pickupCells #swap _ em
				if robo.goal_counter==4:
					print('hey we got here 4 times')
					return
				robo.state=[robo.robos_position[0],robo.robos_position[1],0,5,5,5,0,0,0]
				robo.robo_scope=[]
			robo.possibleMoves()
			s=(robo.state[0],robo.state[1],robo.state[2])
			# calculating max q value for possible operator with dice roll for ties
			qvalues=[(x,y) for x,y in enumerate(Q[s][:4])]
			possible_dirs=set([z for x,y,z in robo.robo_scope])
			qvalues=[(x,y) for x,y in qvalues if ulrd[x] in possible_dirs] # prune away non-applicable directions
			maximal_val=max(qvalues,key=itemgetter(1))
			maximal_values=[(x,y) for x,y in qvalues if y==maximal_val[1]]
			maximal_val=maximal_values[weighted_choice([1/len(maximal_values) for _ in range(len(maximal_values))])] #dice roll
			exploit_move=[(x,y,z) for x,y,z in robo.robo_scope if z==ulrd[maximal_val[0]]][0]
			# hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
			moves=[exploit_move,choice(robo.robo_scope)] # index 0 with probability 0.9 , index 1 with probbaility 0.1
			move=moves[weighted_choice([0.9,0.1])]
			did_we_pickup=robo.doPickup((s[0],s[1]))
			did_we_drop=robo.doDropoff((s[0],s[1]))
			if did_we_pickup==False and did_we_drop==False: # one operator at a time fellows , can't pick up and run immediately
				robo.state[0],robo.state[1]=move[0],move[1]
			ns=(robo.state[0],robo.state[1],robo.state[2]) # next state
			if did_we_pickup:
				Q[s][4]= (1-alpha)*Q[s][4] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
				continue
			if did_we_drop:
				Q[s][5]= (1-alpha)*Q[s][5] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
				continue	 
			if move[2]=='u':
				Q[s][0]= (1-alpha)*Q[s][0] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			elif move[2]=='l':
				Q[s][1]= (1-alpha)*Q[s][1] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			elif move[2]=='r':
				Q[s][2]= (1-alpha)*Q[s][2] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			elif move[2]=='d':
				Q[s][3]= (1-alpha)*Q[s][3] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(6))))
			print(s)
			print(Q[s])
			print('\n')
	return

def visualize(which_button):
	global Q,counters,get_seed,bank_account,bank_account_forty
	if which_button==1:
		r=RobotAgent((1,5),[(1,1),(3,3),(5,5)],[(5,1),(5,3),(2,5)])
		seed(get_seed(counters[0]))
		bank_account=0
		bank_account_forty=deque([],maxlen=40)
		Q_learning(r,0.3,10000,'PRandom')
		#print(bank_account)
		#print(sum(elem for elem in bank_account_forty))
		print(r.blocks_delivered)
		print(sum(e for e in r.blocks_delivered_forty))
		counters[0]+=1
		clear_Q()
		print('how many times we scored goals : {}'.format(r.goal_counter))
		del r
	elif which_button==2:
		r=RobotAgent((1,5),[(1,1),(3,3),(5,5)],[(5,1),(5,3),(2,5)])
		seed(get_seed(counters[1]))
		bank_account=0
		bank_account_forty=deque([],maxlen=40)
		Q_learning(r,0.3,100,'PRandom')
		Q_learning(r,0.3,9900,'PExploit1')
		#print(bank_account)
		#print(sum(elem for elem in bank_account_forty))
		print(r.blocks_delivered)
		print(sum(e for e in r.blocks_delivered_forty))		
		counters[1]+=1
		clear_Q()
		print('how many times we scored goals : {}'.format(r.goal_counter))
		del r
	elif which_button==3:
		r=RobotAgent((1,5),[(1,1),(3,3),(5,5)],[(5,1),(5,3),(2,5)])
		seed(get_seed(counters[2]))
		bank_account=0
		bank_account_forty=deque([],maxlen=40)
		Q_learning(r,0.3,100,'PRandom')
		Q_learning(r,0.3,9900,'PExploit2')
		#print(bank_account)
		#print(sum(elem for elem in bank_account_forty))
		print(r.blocks_delivered)
		print(sum(e for e in r.blocks_delivered_forty))		
		counters[2]+=1
		clear_Q()
		print('how many times we scored goals : {}'.format(r.goal_counter))
		del r
	elif which_button==4:
		r=RobotAgent((1,5),[(1,1),(3,3),(5,5)],[(5,1),(5,3),(2,5)])
		seed(get_seed(counters[3]))
		bank_account=0
		bank_account_forty=deque([],maxlen=40)
		Q_learning(r,0.5,100,'PRandom')
		Q_learning(r,0.5,9900,'PExploit2')
		#print(bank_account)
		#print(sum(elem for elem in bank_account_forty))
		print(r.blocks_delivered)
		print(sum(e for e in r.blocks_delivered_forty))		
		counters[3]+=1
		clear_Q()
		print('how many times we scored goals : {}'.format(r.goal_counter))
		del r
	elif which_button==5:
		r=RobotAgent((1,5),[(1,1),(3,3),(5,5)],[(5,1),(5,3),(2,5)])
		seed(get_seed(counters[4]))
		bank_account=0
		bank_account_forty=deque([],maxlen=40)
		Q_learning(r,0.5,100,'PRandom') # need not worry,impossible to reach terminal state twice need minimum of 124 iterations best case
		Q_learning(r,0.5,9900,'PExploit2',True)
		#print(bank_account)
		#print(sum(elem for elem in bank_account_forty))
		print(r.blocks_delivered)
		print(sum(e for e in r.blocks_delivered_forty))		
		counters[4]+=1
		clear_Q()
		print('how many times we scored goals : {}'.format(r.goal_counter))
		del r
	elif which_button==6:
		r=RobotAgent((1,5),[(1,1),(3,3),(5,5)],[(5,1),(5,3),(2,5)])
		seed(get_seed(counters[5]))
		bank_account=0
		bank_account_forty=deque([],maxlen=40)
		Q_learning(r,0.5,100,'PRandom')
		Q_learning(r,0.5,9900,'PExploit1',True)
		#print(bank_account)
		#print(sum(elem for elem in bank_account_forty))
		print(r.blocks_delivered)
		print(sum(e for e in r.blocks_delivered_forty))		
		counters[5]+=1
		clear_Q()
		print('how many times we scored goals : {}'.format(r.goal_counter))
		del r
	print('#######################################')
	return

if __name__=='__main__':
	mm=Mainmenu('PD-World Agent','600x600')
	mm.addButton('Visualize experiment 1',lambda: visualize(1))
	mm.addButton('Visualize experiment 2',lambda: visualize(2))
	mm.addButton('Visualize experiment 3',lambda: visualize(3))
	mm.addButton('Visualize experiment 4',lambda: visualize(4))
	mm.addButton('Visualize experiment 5',lambda: visualize(5))
	mm.addButton('Visualize experiment 6',lambda: visualize(6))
	mm.game_board.mainloop()
