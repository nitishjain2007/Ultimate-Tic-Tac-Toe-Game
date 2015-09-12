import random
import sys
import signal
import copy

class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()

class Player28:
	
	def __init__(self):
		pass

	def move(self,temp_board,temp_block,old_move,flag):
#		while(1):
#			pass
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = self.get_empty_out_of(temp_board, blocks_allowed, temp_block)
		if(len(cells) == 81):
			return cells[40]
		hutility = []
		for i in range(0,len(cells)):
			hutility.append(0)
		endlist = self.heuristic(cells, blocks_allowed, temp_board, temp_block,0,flag)
		#position = endlist.index(max(endlist))
		occurrences = lambda s, lst: (i for i,e in enumerate(lst) if e == s)
		good_positions = list(occurrences(max(endlist), endlist))
		position = good_positions[random.randrange(len(good_positions))]
		return cells[position]



	def copyboard(self,board):
		local_board = [] 
		for i in range(9): 
			row = ['-']*9 
			local_board.append(row) 
		for k in range(9): 
			for l in range(9): 
				local_board[k][l] = board[k][l]
		return local_board

	def copyblock(self,block):
		local_temp_block = ['-']*9 
		for k in range(9): 
			local_temp_block[i] = block[i]
		return local_temp_block


	def check_empty(self,block_no, game_board):
		for i in range(0,3):
			for j in range(0,3):
				row = i + 3*(block_no/3)
				col = j + 3*(block_no%3)
				if game_board[row][col] == 'x' or game_board[row][col] == 'o':
					return False
		return True

	def check_count(self,block_no, game_board):
		count_x = 0
		count_o = 0
		for i in range(0,3):
			for j in range(0,3):
				row = i + 3*(block_no/3)
				col = j + 3*(block_no%3)
				if game_board[row][col] == 'x':
					count_x += 1
				elif game_board[row][col] == 'o':
					count_o += 1
					
		return [count_x, count_o]

	def get_empty_out_of(self, gameb, blal,block_stat):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			for i in range(9):
				for j in range(9):
	                                no = (i/3)*3
	                                no += (j/3)
					if gameb[i][j] == '-' and block_stat[no] == '-':
						cells.append((i,j))	
		return cells










	def check_horizontal(self,list1, list2, block_no, find_bit, flag):
		x_line = 0
		o_line = 0
		true_bit = 0
		ans_list = []
		for i in range(0,3):
			count_x = 0
			ans_list = []
			for j in list1:
				if j/3 == i:
					count_x += 1
					ans_list.append(j)
			count_h = 0
			if count_x == 2:
				for k in list2:
					if k/3 == i:
						count_h = 1
				if count_h == 0:
					x_line += 1
					if flag and find_bit=='x' and block_no/3==i:
						check = 1
						for item in ans_list:
							if block_no == item:
								check = 0
								break
						if check:
							return True
			
			count_o = 0
			ans_list = []
			for m in list2:
				if m/3 == i:
					count_o += 1
					ans_list.append(m)
			count_h = 0
			if count_o == 2:
				for l in list1:
					if l/3 == i:
						count_h = 1
				if count_h == 0:
					o_line += 1
					if flag and find_bit=='o' and block_no/3==i:
						check = 1
						for item in ans_list:
							if block_no == item:
								check = 0
								break
						if check:
							return True

		if flag:
			return False
		return [x_line, o_line]						



	def check_vertical(self, list1, list2, block_no, find_bit, flag):
		x_line = 0
		o_line = 0
		for i in range(0,3):
			count_x = 0
			ans_list = []
			for j in list1:
				if j%3 == i:
					count_x += 1
					ans_list.append(j)
			count_h = 0
			if count_x == 2:
				for k in list2:
					if k%3 == i:
						count_h = 1
				if count_h == 0:
					x_line += 1
					if flag and find_bit=='x' and (block_no%3)==i:
						check = 1
						for item in ans_list:
							if block_no == item:
								check = 0
								break
						if check:
							return True
			count_o = 0
			ans_list = []
			for m in list2:
				if m%3 == i:
					count_o += 1
					ans_list.append(m)
			count_h = 0
			if count_o == 2:
				for l in list1:
					if l%3 == i:
						count_h = 1
				if count_h == 0:
					o_line += 1
					if flag and find_bit=='o' and (block_no%3)==i:
						check = 1
						for item in ans_list:
							if block_no == item:
								check = 0
								break
						if check:
							return True
		if flag:
			return False
		return [x_line, o_line]						

	def check_diagonal(self, list1, list2, block_no, find_bit, flag):
		x_line = 0
		o_line = 0
		for i in range(0,3):
			count_x1 = 0
			ans_list1 = []
			ans_list2 = []
			count_x2 = 0
			for j in list1:
				if j%3 == j/3:
					count_x1 += 1
					ans_list1.append(j)
				if j%3 + j/3 == 2:
					count_x2 += 1
					ans_list2.append(j)
			count_h1 = 0
			count_h2 = 0
			if count_x1 == 2:
				for k in list2:
					if k%3 == k/3:
						count_h1 = 1
				if count_h1 == 0:
					x_line += 1
					if flag and find_bit=='x' and block_no%3==block_no/3:
						check = 1
						for item in ans_list1:
							if block_no == item:
								check = 0
								break
						if check:
							return True

			if count_x2 == 2:
				for k in list2:
					if k%3 + k/3 == 2:
						count_h2 = 1
				if count_h2 == 0:
					x_line += 1
					if flag and find_bit=='x' and (block_no%3 + block_no/3) == 2:
						check = 1
						for item in ans_list2:
							if block_no == item:
								check = 0
								break
						if check:
							return True
			
			count_o1 = 0
			ans_list1 = []
			count_o2 = 0
			ans_list2 = []
			for l in list2:
				if l%3 == l/3:
					count_o1 += 1
					ans_list1.append(l)
				if l%3 + l/3 == 2:
					count_o2 += 1
					ans_list2.append(l)
			count_h1 = 0
			count_h2 = 0
			if count_o1 == 2:
				for k in list1:
					if k%3 == k/3:
						count_h1 = 1
				if count_h1 == 0:
					o_line += 1
					if flag and find_bit=='o' and (block_no%3)==(block_no/3):
						check = 1
						for item in ans_list1:
							if block_no == item:
								check = 0
								break
						if check:
							return True

			if count_o2 == 2:
				for m in list1:
					if m%3 + m/3 == 2:
						count_h2 = 1
				if count_h2 == 0:
					o_line += 1
					if flag and find_bit=='o' and (block_no%3 + block_no/3) == 2:
						check = 1
						for item in ans_list2:
							if block_no == item:
								check = 0
								break
						if check:
							return True
		if flag:
			return False
		return [x_line, o_line]


	def check_state(self, game_board, block):
		#print_lists1(game_board)
		x_list = []
		o_list = []
		count_x = 0
		count_o = 0
		for i in range(0,3):
			for j in range(0,3):
				row = i + 3*(block/3)
				col = j + 3*(block%3)
				if game_board[row][col] == 'x':
					x_list.append(3*i + j)
				elif game_board[row][col] == 'o':
					o_list.append(3*i + j)	
		H = self.check_horizontal(x_list, o_list, 0, 'x', 0)  
		V = self.check_vertical(x_list, o_list, 0, 'x', 0) 
		D = self.check_diagonal(x_list, o_list, 0, 'x', 0)
		
		count_x = H[0] + V[0] + D[0]
		count_o = H[1] + V[1] + D[1]
		
		return [count_x, count_o]

	def check_block_line(self, game_board, block_stat, block_no, find_bit):
		x_list = []
		o_list = []
		count_x = 0
		count_o = 0
		for i in range(0,3):
			for j in range(0,3):
				row = 3*i
				if game_board[row+j] == 'x':
					x_list.append(3*i + j)
				elif game_board[row+j] == 'o':
					o_list.append(3*i + j)
		H = self.check_horizontal(x_list, o_list, block_no, find_bit, 1)  
		V = self.check_vertical(x_list, o_list, block_no, find_bit, 1) 
		D = self.check_diagonal(x_list, o_list, block_no, find_bit, 1)
		if H==1 or V==1 or D==1:
			return True

		return False




	def check_block(self, game_board, block_no, cell, find_bit):
		x_list = []
		o_list = []
		if find_bit == 'x':
			toggle = 'o'
		else:
			toggle = 'x'
		k=0	
		listf = []
		for i in range(0,3):
			liste = []
			for j in range(0,3):
				liste.append(k)
				k+=1
			listf.append(liste)
		cell_value = listf[cell[0]%3][cell[1]%3]
		#print "the cell value is ", cell_value
		count_x = 0
		count_o = 0
		for i in range(0,3):
			for j in range(0,3):
				row = i + 3*(block_no/3)
				col = j + 3*(block_no%3)
				if game_board[row][col] == 'x':
					x_list.append(3*i + j)
				elif game_board[row][col] == 'o':
					o_list.append(3*i + j)	
		all_list = x_list + o_list
		H = self.check_horizontal(x_list, o_list, cell_value, find_bit, 1)  
		V = self.check_vertical(x_list, o_list, cell_value, find_bit, 1) 
		D = self.check_diagonal(x_list, o_list, cell_value, find_bit, 1)
		
		Hk = self.check_horizontal(x_list, o_list, cell_value, toggle, 1)  
		Vk = self.check_vertical(x_list, o_list, cell_value, toggle, 1) 
		Dk = self.check_diagonal(x_list, o_list, cell_value, toggle, 1)

		make = block = 0
		if H or V or D:
			make = 1
		if Hk or Vk or Dk:
			block = 2
		return make + block

	def check_probable_block(self, block_list, block_stat, flag):
		if flag == 'x':
			toggle = 'o'
		else:
			toggle = 'x'
		prob = -1
		count_list = []		
		for blocks in block_list:
			count = 0
			for block in blocks:
				if block_stat[block] == flag:
					count += 1
				elif block_stat[block] == toggle:
					count = -1
					break
			count_list.append(count)
			if count > prob:
				prob = count
		bcount = 0
		for index in count_list:
			if index <= 0:
				bcount += 1
		if bcount == 3:
			prob = 0
		return	prob*50	





	def check(self, temp_board,cells,temp_block):
		temp_board1 = temp_board
		#temp_board1[cells[0]][cells[1]] = flag
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed1  = []

		if cells[0] in for_corner and cells[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if cells[0] % 3 == 0 and cells[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed1 = [0, 1, 3]
			elif cells[0] % 3 == 0 and cells[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed1 = [1,2,5]
			elif cells[0] in [2,5, 8] and cells[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed1  = [3,6,7]
			elif cells[0] in [2,5,8] and cells[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed1 = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if cells[0] % 3 == 0 and cells[1] in [1,4,7]:
				## upper-center block
				blocks_allowed1 = [1]

			elif cells[0] in [1,4,7] and cells[1] % 3 == 0:
				## middle-left block
				blocks_allowed1 = [3]
		
			elif cells[0] in [2,5,8] and cells[1] in [1,4,7]:
				## lower-center block
				blocks_allowed1 = [7]

			elif cells[0] in [1,4,7] and cells[1] in [2,5,8]:
				## middle-right block
				blocks_allowed1 = [5]
			elif cells[0] in [1,4,7] and cells[1] in [1,4,7]:
				blocks_allowed1 = [4]
		cells1 = self.get_empty_out_of(temp_board1, blocks_allowed1,temp_block)
		returnlist = []
		returnlist.append(blocks_allowed1)
		returnlist.append(cells1)
		return returnlist







	def utilityvaluepersonal(self, temp_board,temp_board2,cell,temp_block,flag,tempflag,depth):
		block = 3*(cell[0]/3)+(cell[1]/3)
		list3 = [[[0,1,3],[1],[1,2,5]],[[3],[4],[5]],[[3,6,7],[7],[5,7,8]]]
		if(flag == 'x'):
			case = 0
		else:
			case = 1
		utilityvalue1 = 0
		flagarr = ['x', 'o']
		getnumberlist = self.check_state(temp_board, block)
		a = self.check_block(temp_board,block,cell,flag)
		if(getnumberlist[case] > 0 or getnumberlist[case ^ 1] > 0):
			if cell[0]==4 and cell[1]==4:
				a = self.check_block(temp_board,block,cell,flag)
			if(a == 3):
				if(self.check_block_line(temp_board, temp_block, block, flagarr[case])):
					utilityvalue1 += 600
					if block == 4:
						utilityvalue1 += 100
				else:
					utilityvalue1 += 400
					if block == 4:
						utilityvalue1 += 100
			elif(a == 2):
				if(self.check_block_line(temp_board, temp_block, block, flagarr[case ^ 1])):
					utilityvalue1 += 600
					if block == 4:
						utilityvalue1 += 100
				else:
					utilityvalue1 += 350
					if block == 4:
						utilityvalue1 += 100
			elif(a == 1):
				if(self.check_block_line(temp_board, temp_block, block, flagarr[case])):
					utilityvalue1 += 600
					if block == 4:
						utilityvalue1 += 100
				else:
					utilityvalue1 += 300
					if block == 4:
						utilityvalue1 += 100
			else:  
				list4 = [[[1,2], [3,6], [4,8]], [[0,2],[4,7]], [[0,1], [4,6], [5,8]], [[0,6], [4,5]], [[0,8], [1,7], [2,6], [3,5]], [[2,8], [3,4]], [[0,3], [2,4], [7,8]], [[1,4], [6,8]],[[0,4], [2,5], [6,7]]]
				utilityvalue1 += self.check_probable_block(list4[block], temp_block, flagarr[case])
		if((cell[0]%3 == 0 or cell[0]%3 == 2) and (cell[1]%3 == 0 or cell[1]%3 == 2)):
			utilityvalue1 -= 50
		temp1 = 1
		#print "the list of blocks for" ,cell , "are ", list3[cell[0]%3][cell[1]%3]
		for i in range(0,len(list3[cell[0]%3][cell[1]%3])):
			if(list3[cell[0]%3][cell[1]%3][i] == '-'):
				temp1 = 0
				break
		if(temp1 == 1):
			utilityvalue1 -= 150

		blocks_allowed1 = list3[cell[0]%3][cell[1]%3]

		if tempflag:
			if len(blocks_allowed1) == 1:
				if(temp_block[blocks_allowed1[0]] != '-'):
					utilityvalue1 -= 100
				else:
					temp = self.check_count(blocks_allowed1[0], temp_board)
					if((temp[0] == 0 and temp[1] == 0) or (temp[case] == 1 and temp[case ^ 1] == 0)):
						utilityvalue1 += 100
					elif(temp[case] == 1 and temp[case^ 1] == 1):
						utilityvalue1 += 80
					elif(temp[case] == 0 and temp[case^1] == 1):
						utilityvalue1 -= 10
					elif(temp[case] >= 2 and temp[case^1] >= 2):
						getnumberlist = self.check_state(temp_board2, blocks_allowed1[0])
						if(getnumberlist[case] > 0):
							if(temp_block[blocks_allowed1[0]] == '-'):
								if(self.check_block_line(temp_board2, temp_block, blocks_allowed1[0], flag)):
									utilityvalue1 -= 500
									if(temp_block == 4):
										utilityvalue1 -= 50
								else:
									utilityvalue1 -= 100
							else:
								utilityvalue1 -= 200
						if(getnumberlist[case ^ 1] > 0):
							if(temp_block[blocks_allowed1[0]] == '-'):
								if(self.check_block_line(temp_board2, temp_block, blocks_allowed1[0], flagarr[case ^ 1])):
									utilityvalue1 -= 500
									if(temp_block == 4):
										utilityvalue1 -= 50
								else:
									utilityvalue1 -= 250
							else:
								utilityvalue1 -= 200
						if(getnumberlist[case] == 0 and getnumberlist[case ^ 1] == 0):
							utilityvalue1 += 50

					else:
						getnumberlist = self.check_state(temp_board2, blocks_allowed1[0])
						#print "the getnumberlist for cell ", cell, "is ",getnumberlist
						#print temp_board[cell[0]][cell[1]]
						if(temp[case] >= 2):
							if(getnumberlist[case] > 0):
								if(self.check_block_line(temp_board, temp_block, blocks_allowed1[0], flagarr[case])):
									utilityvalue1 -= 300
								else:
									utilityvalue1 -= 150
							else:
								utilityvalue1 += 50;
						elif(temp[case ^ 1] >= 2):
							if(getnumberlist[case ^ 1] > 0):
								if(self.check_block_line(temp_board, temp_block, blocks_allowed1[0], flagarr[case ^ 1])):
									utilityvalue1 -= 500
								else:
									utilityvalue1 -= 250
							else:
								utilityvalue1 -= 50;
					
			else:
				utilityvalue2 = [0, 0, 0]
				count_temp=0
				for i in range(0,len(blocks_allowed1)):
					if(temp_block[blocks_allowed1[i]] != '-'):
						utilityvalue2[i] = 0
						count_temp += 1
					else:
						temp = self.check_count(blocks_allowed1[i],temp_board)
						if((temp[0] == 0 and temp[1] == 0) or (temp[case] == 1 and temp[case ^ 1] == 0)):
							utilityvalue2[i] += 50
						elif(temp[case] == 1 and temp[case^ 1] == 1):
							utilityvalue2[i] += 80
						elif(temp[case] == 0 and temp[case^1] == 1):
							utilityvalue2[i] -= 10
						elif(temp[case] >= 2 and temp[case^1] >= 2):
							getnumberlist = self.check_state(temp_board2, blocks_allowed1[i])
							if(getnumberlist[case] > 0):
								if(temp_block[blocks_allowed1[i]] == '-'):
									utilityvalue2[i] -= 50
								else:
									utilityvalue2[i] -= 100
							if(getnumberlist[case ^ 1] > 0):
								if(temp_block[blocks_allowed1[i]] == '-'):
									utilityvalue2[i] -= 125
								else:
									utilityvalue2[i] -= 100
							if(getnumberlist[case] == 0 and getnumberlist[case ^ 1] == 0):
								utilityvalue1 += 25

						else:
							getnumberlist = self.check_state(temp_board2, blocks_allowed1[i])
							if(temp[case] >= 2):
								if(getnumberlist[case] > 0):
									utilityvalue2[i] -= 75;
								else:
									utilityvalue2[i] += 25;
							elif(temp[case ^ 1] >= 2):
								if(getnumberlist[case ^ 1] > 0):
									utilityvalue2[i] -= 125;
								else:
									utilityvalue2[i] -= 25;

				if(count_temp == 3):
					utilityvalue1 -= 100
				else:
					utilityvalue1 += min(utilityvalue2)



		if(depth):
			utilityvalue1 *= -1
			


		#print "the utilityvaluepersonal for cell ", cell, "is ",utilityvalue1
		return utilityvalue1

	def utilityvalue(self, temp_board,cell,temp_block,flag):
		list1 = self.check(temp_board,cell,temp_block)
		blocks_allowed1 = list1[0]
		temp_board2 = self.copyboard(temp_board)
		temp_board2[cell[0]][cell[1]] = flag
		utilityvalue1 = 0
		if flag == 'x':
			case = 0
		else:
			case = 1
		flagarr = ['x', 'o']
		if len(blocks_allowed1) == 1:
			if(temp_block[blocks_allowed1[0]] != '-'):
				utilityvalue1 -= 300
			else:
				temp = self.check_count(blocks_allowed1[0],temp_board)
				if((temp[0] == 0 and temp[1] == 0) or (temp[case] == 1 and temp[case ^ 1] == 0)):
					utilityvalue1 += 100
				elif(temp[case] == 1 and temp[case^ 1] == 1):
					utilityvalue1 += 80
				elif(temp[case] == 0 and temp[case^1] == 1):
					utilityvalue1 -= 10
				elif(temp[case] >= 2 and temp[case^1] >= 2):
					getnumberlist = self.check_state(temp_board2, blocks_allowed1[0])
					if(getnumberlist[case] > 0):
						if(temp_block[blocks_allowed1[0]] == '-'):
							if(self.check_block_line(temp_board2, temp_block, blocks_allowed1[0], flag)):
								utilityvalue1 -= 500
								if(temp_block == 4):
									utilityvalue1 -= 50
							else:
								utilityvalue1 -= 100
						else:
							utilityvalue1 -= 200
					if(getnumberlist[case ^ 1] > 0):
						if(temp_block[blocks_allowed1[0]] == '-'):
							if(self.check_block_line(temp_board2, temp_block, blocks_allowed1[0], flagarr[case ^ 1])):
								utilityvalue1 -= 500
								if(temp_block == 4):
									utilityvalue1 -= 50
							else:
								utilityvalue1 -= 250
						else:
							utilityvalue1 -= 200
					if(getnumberlist[case] == 0 and getnumberlist[case ^ 1] == 0):
						utilityvalue1 += 50

				else:
					getnumberlist = self.check_state(temp_board2, blocks_allowed1[0])
					#print "the getnumberlist for cell ", cell, "is ",getnumberlist
					#print temp_board[cell[0]][cell[1]]
					if(temp[case] >= 2):
						if(getnumberlist[case] > 0):
							if(self.check_block_line(temp_board, temp_block, blocks_allowed1[0], flagarr[case])):
								utilityvalue1 -= 500
								if(temp_block == 4):
									utilityvalue1 -= 50
							else:
								utilityvalue1 -= 150
						else:
							utilityvalue1 += 50;
					elif(temp[case ^ 1] >= 2):
						if(getnumberlist[case ^ 1] > 0):
							if(self.check_block_line(temp_board, temp_block, blocks_allowed1[0], flagarr[case ^ 1])):
								utilityvalue1 -= 300
								if(temp_block == 4):
									utilityvalue1 -= 50
							else:
								utilityvalue1 -= 250
						else:
							utilityvalue1 -= 50;

		else:
			utilityvalue2 = [0, 0, 0]
			count_temp=0
			for i in range(0,len(blocks_allowed1)):
				if(temp_block[blocks_allowed1[i]] != '-'):
					utilityvalue2[i] = 0
					count_temp += 1
				else:
					temp = self.check_count(blocks_allowed1[i],temp_board)
					if((temp[0] == 0 and temp[1] == 0) or (temp[case] == 1 and temp[case ^ 1] == 0)):
						utilityvalue2[i] += 50
					elif(temp[case] == 1 and temp[case^ 1] == 1):
						utilityvalue2[i] += 80
					elif(temp[case] == 0 and temp[case^1] == 1):
						utilityvalue2[i] -= 10
					elif(temp[case] >= 2 and temp[case^1] >= 2):
						getnumberlist = self.check_state(temp_board2, blocks_allowed1[i])
						if(getnumberlist[case] > 0):
							if(temp_block[blocks_allowed1[i]] == '-'):
								utilityvalue2[i] -= 100
							else:
								utilityvalue2[i] -= 200
						if(getnumberlist[case ^ 1] > 0):
							if(temp_block[blocks_allowed1[i]] == '-'):
								utilityvalue2[i] -= 250
							else:
								utilityvalue2[i] -= 200
						if(getnumberlist[case] == 0 and getnumberlist[case ^ 1] == 0):
							utilityvalue1 += 50

					else:
						getnumberlist = self.check_state(temp_board2, blocks_allowed1[i])
						if(temp[case] >= 2):
							if(getnumberlist[case] > 0):
								utilityvalue2[i] -= 150;
							else:
								utilityvalue2[i] += 50;
						elif(temp[case ^ 1] >= 2):
							if(getnumberlist[case ^ 1] > 0):
								utilityvalue2[i] -= 250;
							else:
								utilityvalue2[i] -= 50;
			if(count_temp == 3):
				utilityvalue1 = -300;
			else:
				utilityvalue1 = min(utilityvalue2)
				#print "array is ", utilityvalue2 ,"             min is ", utilityvalue1
		#print "utility for ", cell , "is ", utilityvalue1
		return utilityvalue1








	def maxindexof(self, cells,blocks_allowed,temp_board,temp_block,hcount,flag):
		#print "maxindex called"
		hutility1 = []
		for i in range(0,len(cells)):
			temp_board1 = self.copyboard(temp_board)
			temp_board1[cells[i][0]][cells[i][1]] = flag
			for_corner = [0,2,3,5,6,8]

			#List of permitted blocks, based on old move.
			blocks_allowed1  = []

			if cells[i][0] in for_corner and cells[i][1] in for_corner:
				## we will have 3 representative blocks, to choose from

				if cells[i][0] % 3 == 0 and cells[i][1] % 3 == 0:
					## top left 3 blocks are allowed
					blocks_allowed1 = [0, 1, 3]
				elif cells[i][0] % 3 == 0 and cells[i][1] in [2, 5, 8]:
					## top right 3 blocks are allowed
					blocks_allowed1 = [1,2,5]
				elif cells[i][0] in [2,5, 8] and cells[i][1] % 3 == 0:
					## bottom left 3 blocks are allowed
					blocks_allowed1  = [3,6,7]
				elif cells[i][0] in [2,5,8] and cells[i][1] in [2,5,8]:
					### bottom right 3 blocks are allowed
					blocks_allowed1 = [5,7,8]
				else:
					print "SOMETHING REALLY WEIRD HAPPENED!"
					sys.exit(1)
			else:
			#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
				if cells[i][0] % 3 == 0 and cells[i][1] in [1,4,7]:
					## upper-center block
					blocks_allowed1 = [1]
		
				elif cells[i][0] in [1,4,7] and cells[i][1] % 3 == 0:
					## middle-left block
					blocks_allowed1 = [3]
			
				elif cells[i][0] in [2,5,8] and cells[i][1] in [1,4,7]:
					## lower-center block
					blocks_allowed1 = [7]

				elif cells[i][0] in [1,4,7] and cells[i][1] in [2,5,8]:
					## middle-right block
					blocks_allowed1 = [5]
				elif cells[i][0] in [1,4,7] and cells[i][1] in [1,4,7]:
					blocks_allowed1 = [4]

		# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
			cells1 = self.get_empty_out_of(temp_board1, blocks_allowed1, temp_block)
			#print "cells possible to move at level " , hcount -1 , "are " , cells1
			
			list1 = self.heuristic(cells1,blocks_allowed1,temp_board1,temp_block,hcount,flag)
			#print "the maximum endlist for ", cells[i] , "is ", list1
			b = self.utilityvaluepersonal(temp_board,temp_board1,cells[i],temp_block,flag,1,(hcount-1)%2)
			#print "Personalutilityvalue of ", cells[i] , " is ", b
	#		print "list at ", cells[i] , "is ", list1
			if(len(list1) != 0):
				hutility1.append(max(list1) + b)
			else:
				hutility1.append(b)
		#print "Heuristic at level " , hcount-1 , " is" , hutility1
		#print hutility1
		return hutility1


	def minindexof(self, cells,blocks_allowed,temp_board,temp_block,hcount,flag):
		#print "minindex called"
		hutility1 = []
		for i in range(0,len(cells)):
			temp_board1 = self.copyboard(temp_board)
			temp_board1[cells[i][0]][cells[i][1]] = flag
			for_corner = [0,2,3,5,6,8]

			#List of permitted blocks, based on old move.
			blocks_allowed1  = []

			if cells[i][0] in for_corner and cells[i][1] in for_corner:
				## we will have 3 representative blocks, to choose from

				if cells[i][0] % 3 == 0 and cells[i][1] % 3 == 0:
					## top left 3 blocks are allowed
					blocks_allowed1 = [0, 1, 3]
				elif cells[i][0] % 3 == 0 and cells[i][1] in [2, 5, 8]:
					## top right 3 blocks are allowed
					blocks_allowed1 = [1,2,5]
				elif cells[i][0] in [2,5, 8] and cells[i][1] % 3 == 0:
					## bottom left 3 blocks are allowed
					blocks_allowed1  = [3,6,7]
				elif cells[i][0] in [2,5,8] and cells[i][1] in [2,5,8]:
					### bottom right 3 blocks are allowed
					blocks_allowed1 = [5,7,8]
				else:
					print "SOMETHING REALLY WEIRD HAPPENED!"
					sys.exit(1)
			else:
			#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
				if cells[i][0] % 3 == 0 and cells[i][1] in [1,4,7]:
					## upper-center block
					blocks_allowed1 = [1]
		
				elif cells[i][0] in [1,4,7] and cells[i][1] % 3 == 0:
					## middle-left block
					blocks_allowed1 = [3]
			
				elif cells[i][0] in [2,5,8] and cells[i][1] in [1,4,7]:
					## lower-center block
					blocks_allowed1 = [7]

				elif cells[i][0] in [1,4,7] and cells[i][1] in [2,5,8]:
					## middle-right block
					blocks_allowed1 = [5]
				elif cells[i][0] in [1,4,7] and cells[i][1] in [1,4,7]:
					blocks_allowed1 = [4]

		# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
			cells1 = self.get_empty_out_of(temp_board1, blocks_allowed1, temp_block)
			#print "cells possible to move at level " , hcount -1 , "are " , cells1
			
			list1 = self.heuristic(cells1,blocks_allowed1,temp_board1,temp_block,hcount,flag)
			b = self.utilityvaluepersonal(temp_board,temp_board1,cells[i],temp_block,flag,1,(hcount-1)%2)
			#print "Personalutilityvalue of ", cells[i] , " is ", b
			#print "list at ", cells[i] , "is ", list1
			#print "the minimum endlist for ", cells[i] , "is ", list1
			if(len(list1)!=0):
				hutility1.append(min(list1) + b)
			else:
				hutility1.append(b)
		#print "Heuristic at level " , hcount-1 , " is" , hutility1
		return hutility1








	def heuristic(self, cells,blocks_allowed,temp_board,temp_block,hcount,flag):
		if(hcount%2 == 0):
			hstate = 'max'
		else:
			hstate = 'min'
		if(hcount < 2):
			hcount += 1
			if(hstate == 'max'):
				return self.maxindexof(cells,blocks_allowed,temp_board,temp_block,hcount,flag)
			else:
				return self.minindexof(cells,blocks_allowed,temp_board,temp_block,hcount,flag)


		else:
			hutility = []
			if(hcount != 2):
				print "something bad happened"
			else:
				for i in range(0,len(cells)):
					g = self.utilityvalue(temp_board,cells[i],temp_block,flag)
					h = self.utilityvaluepersonal(temp_board,temp_board,cells[i],temp_block,flag,0,0)
					hutility.append(g+h);
			#print "Heuristic at level " , hcount , " is" , hutility
			return hutility;

class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))
		

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		for i in range(9):
			for j in range(9):
				if gameb[i][j] == '-':
					cells.append((i,j))	
		
	return cells
		
# Note that even if someone has won a block, it is not abandoned. But then, there's no point winning it again!
# Returns True if move is valid
def check_valid_move(game_board, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True


	for_corner = [0,2,3,5,6,8]

	#List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		## we will have 3 representative blocks, to choose from

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			## top left 3 blocks are allowed
			blocks_allowed = [0, 1, 3]
		elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
			## top right 3 blocks are allowed
			blocks_allowed = [1,2,5]
		elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
			## bottom left 3 blocks are allowed
			blocks_allowed  = [3,6,7]
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
			### bottom right 3 blocks are allowed
			blocks_allowed = [5,7,8]

		else:
			print "SOMETHING REALLY WEIRD HAPPENED!"
			sys.exit(1)

	else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			## upper-center block
			blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			## middle-left block
			blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			## lower-center block
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			## middle-right block
			blocks_allowed = [5]

		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]


	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
	cells = get_empty_out_of(game_board, blocks_allowed)

	#Checks if you made a valid move. 
	if current_move in cells:
		return True
	else:
		return False

def update_lists(game_board, block_stat, move_ret, fl):
	#move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl


	#print "@@@@@@@@@@@@@@@@@"
	#print block_stat

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3	
	id1 = block_no/3
	id2 = block_no%3
	mg = 0
	mflg = 0
	if block_stat[block_no] == '-':

		### now for diagonals
		## D1
		# ^
		#   ^
		#     ^
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
			mg=1
			#print "SEG: D1 found"

		## D2
		#     ^
		#   ^
		# ^
		############ MODIFICATION HERE, in second condition -> gb[id1*3][id2*3+2]
		# if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3] and game_board[id1*3+1][id2*3+1] != '-':
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
			mg=1
			#print "SEG: D2 found"

		### col-wise
		if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        #### MODIFICATION HERE, [i] was missing previously
                        # if game_board[id1*3]==game_board[id1*3+1] and game_board[id1*3+1] == game_board[id1*3+2] and game_board[id1*3] != '-':
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
				#print "SEG: Col found"
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        ### MODIFICATION HERE, [i] was missing previously
                        #if game_board[id2*3]==game_board[id2*3+1] and game_board[id2*3+1] == game_board[id2*3+2] and game_board[id2*3] != '-':
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
				#print "SEG: Row found"
                                break

	
	if mflg == 1:
		block_stat[block_no] = fl

	#print 
	#print block_stat
	#print "@@@@@@@@@@@@@@@@@@@@@@@"	
	return mg

#Check win
def terminal_state_reached(game_board, block_stat,point1,point2):
	### we are now concerned only with block_stat
	bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-') or (bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		print block_stat
		return True, 'W'
	## Col win
	elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		print block_stat
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-'):
		print block_stat
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-':
					smfl = 1
					break
		if smfl == 1:
			return False, 'Continue'
		
		else:
			##### check of number of DIAGONALs


			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
				return True, 'D'	


def decide_winner_and_get_message(player,status, message):
	if status == 'P1':
		return ('P1', 'MORE DIAGONALS')
	elif status == 'P2':
		return ('P2', 'MORE DIAGONALS')
	elif player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# game board is a 9x9 list, block_stat is a 1D list of 9 elements
	game_board, block_stat = get_init_board_and_blockstatus()

	#########
	# deciding player1 / player2 after a coin toss
	pl1 = obj1 
	pl2 = obj2

	### basically, player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) ### for the first move

	WINNER = ''
	MESSAGE = ''
	TIMEALLOWED = 60


	### These points will not keep track of the total points of both the players.
	### Instead, these variables will keep track of only the blocks won by DIAGONALS, and these points will be used only in cases of DRAW....
	p1_pts=0
	p2_pts=0

	#### printing
	print_lists(game_board, block_stat)

	while(1):
		###################################### 
		########### firstly pl1 will move
		###################################### 
		
		## just for checking that the player1 does not modify the contents of the 2 lists
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player1 to complete in TIMEALLOWED secs. 
		try:
			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			break
			### MODIFICATION!!
		signal.alarm(0)
	
		#### check if both lists are the same!!
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			##player1 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		### now check if the returned move is valid
		if not check_valid_move(game_board, ret_move_pl1, old_move):
			## player1 loses - he made the wrong move.
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break
			

		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl
		######## So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
		p1_pts += update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		### now check if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)
		############################################
		### Now player2 plays
		###########################################
		
                ## just for checking that the player2 does not modify the contents of the 2 lists
                temp_board_state = game_board[:]
                temp_block_stat = block_stat[:]


		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player2 to complete in TIMEALLOWED secs. 
		try:
                	ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                #### check if both lists are the same!!
                if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
                        ##player2 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			

                ### now check if the returned move is valid
                if not check_valid_move(game_board, ret_move_pl2, old_move):
                        ## player2 loses - he made the wrong move...
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
                ######## So if the move is valid, we update the 'game_board' and 'block_stat' lists with the move of P2
                p2_pts += update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

                ### now check if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
                if gamestatus == True:
			print_lists(game_board, block_stat)
                        WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
                        break
		### otherwise CONTINUE	
		old_move = ret_move_pl2
		print_lists(game_board, block_stat)

	######### THESE ARE NOT THE TOTAL points, these are just the diagonal points, (refer to the part before the while(1) loop
	####### These will be used only in cases of DRAW
	print p1_pts
	print p2_pts

	
	print WINNER
	print MESSAGE
#	return WINNER, MESSAGE, p1_pt2, p2_pt2

if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Human vs. Human'
		print '                2 => Human vs. Bot'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Manual_player()
		obj2 = Manual_player()

	elif option == '2':
		obj1 = Player28()
		obj2 = Manual_player()


        #########
        # deciding player1 / player2 after a coin toss
        num = random.uniform(0,1)
	interchange = 0
        if num > 0.5:
		interchange = 1
		simulate(obj2, obj1)
	else:
		simulate(obj1, obj2)
