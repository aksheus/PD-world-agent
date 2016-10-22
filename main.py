from RobotAgent import RobotAgent
from random import choice
#this code just initializes the global q matrix btw we are going with state space representation 2  50x4 in size
# gonna use a dictionary for efficiency  .... key's are (i,j,x) tuples where i,j,x are the values in the problem speification ppt
# i is x-coordinate of robot,  j is y-cordinate of robot, x is 1 if its holding a star or it is zero otherwise
#  each key has a value of the type list  , [up,left,right,down] the four actions , 0 is up ,1 is left ,2 is right ,3 is down
l=[(x,y) for x in range(1,6) for y in range(1,6)]
m=[(x,y,0) for x,y in l]+[(x,y,1) for x,y in l]  #just initialization stuff
Q={ (x,y,z): [0,0,0,0] for x,y,z in m } # Q is our Q matrix
smthn='nothing happened'

def R(did_we_pickup,did_we_drop): #reward function
	global smthn
	if did_we_pickup or did_we_drop:
		return 13
	else:
		return -1

def Q_learning(robo,alpha=0.5,iterations=10000,policy='PRandom'):  # implements q - learning algorithm
	"""
		Q(a,s) <-- (1-alpha)*Q(a,s)+ alpha*[R(s',a,s)+ gamma*max(Q(a',s'))]
	"""
	gamma=0.3
	if policy=='PRandom':
		for _ in range(iterations):
			robo.possibleMoves()
			s=(robo.state[0],robo.state[1],robo.state[2])  
			move=choice(robo.robo_scope)
			did_we_pickup=robo.doPickup((s[0],s[1]))
			did_we_drop=robo.doDropoff((s[0],s[1]))
			robo.state[0],robo.state[1]=move[0],move[1]
			ns=(robo.state[0],robo.state[1],robo.state[2]) # next state 
			if move[2]=='u':
				Q[s][0]= (1-alpha)*Q[s][0] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(4))))
			elif move[2]=='l':
				Q[s][1]= (1-alpha)*Q[s][1] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(4))))
			elif move[2]=='r':
				Q[s][2]= (1-alpha)*Q[s][2] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(4))))
			elif move[2]=='d':
				Q[s][3]= (1-alpha)*Q[s][3] + alpha*(R(did_we_pickup,did_we_drop)+gamma*(max(Q[(ns)][x] for x in range(4))))
			print(s)
			print(Q[s])
			print('\n')
	elif policy=='PExploit1':
		pass
		# next time  



	return

if __name__=='__main__':
	r=RobotAgent((1,5),[(1,5),(3,3),(5,5)],[(1,4),(5,3),(2,5)])
	Q_learning(r,0.5,10000)
	print(smthn)
