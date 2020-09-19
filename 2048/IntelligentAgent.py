import math
import time
from BaseAI import BaseAI


class IntelligentAgent(BaseAI):

	def getMove(self, grid):
		# Selects a random move and returns it
		self.MAXINT = 1e20
		moveset = grid.getAvailableMoves()
		if moveset:
			# return moveset[0][0]
			time_lim = 0.01 + time.clock()
			finalMove,maxUntility = None,-self.MAXINT
			depth_lim = 1
			while time.clock() <= time_lim:
				move,_,untility = self.Maximize(grid, time_lim, depth_lim, -self.MAXINT, self.MAXINT,0)
				if untility > maxUntility:
					finalMove, maxUntility = move, untility
				depth_lim += 1
			# print(depth_lim-1)
			return finalMove
		else:
			return None


	def Maximize(self, grid, time_lim, depth_lim, alpha, beta, depth):
		if not grid.canMove():
			return (None, grid, self.evalueGrid(grid))
		maxMove, maxGrid, maxUtility = None, grid, -self.MAXINT
		for move in grid.getAvailableMoves():
			# Make move first
			grid_after_move = grid.clone()
			grid_after_move.move(move[0])
			if depth >= depth_lim or time.clock() >= time_lim:
				utility = self.evalueGrid(grid_after_move)
			else:
				utility = self.Chance(grid_after_move, time_lim, depth_lim, alpha, beta, depth+1)
			if utility > maxUtility:
				maxMove, maxGrid, maxUtility = move[0], grid_after_move, utility
			# alpha beta puring
			if maxUtility > beta:
				break
			if maxUtility > alpha:
				alpha = maxUtility
		return (maxMove, maxGrid, maxUtility)


	def Chance(self, grid, time_lim, depth_lim, alpha, beta, depth):
		two_tile = self.Minimize(grid, time_lim, depth_lim, alpha, beta, tile_val=2, depth=depth)
		four_tile = self.Minimize(grid, time_lim, depth_lim, alpha, beta, tile_val=4, depth=depth)
		return .9 * two_tile[2] + .1 * four_tile[2]

	def Minimize(self, grid, time_lim, depth_lim, alpha, beta, tile_val, depth):
		if not grid.canMove():
			return (None, grid, self.evalueGrid(grid))

		minTile, minGrid, minUtility = None, grid, self.MAXINT

		open_tiles = grid.getAvailableCells()
		for tile in open_tiles:
			# insert tile with value in tile_val
			grid_after_tile = grid.clone()
			grid_after_tile.insertTile(tile,tile_val)

			if depth >= depth_lim or time.clock() >= time_lim:
				utility = self.evalueGrid(grid_after_tile)
			else:
				utility = self.Maximize(grid_after_tile, time_lim, depth_lim, alpha, beta,depth+1)[2]
			if utility < minUtility:
				minMove, minGrid, minUtility = tile, grid_after_tile, utility
			# alpha beta puring
			if minUtility < alpha:
				break
			if minUtility < beta:
				beta = minUtility
		return (minTile, minGrid, minUtility)

	def evalueGrid(self,grid):
		w1,w3,w4,w5,w6 = 1,5,10,0.5,3
		score = self.avg_tile_value(grid) * w1 \
				+ self.available_cell_count(grid) * w3 \
				+ self.distance(grid) * w4 \
				+ self.smoothness(grid) * w5 \
				+ self.montonicity(grid) * w6
				# + self.max_tile_in_corner_value(grid) * w2 \
		return score

	def available_cell_count(self,grid):
		return len(grid.getAvailableCells())

	def avg_tile_value(self,grid):
		avg = sum(sum(row) for row in grid.map)/(grid.size * grid.size)
		return math.log2(avg)

	def max_tile_in_corner_value(self,grid):
		corner = grid.size - 1
		tiles_in_corner_value = [grid.getCellValue((0,0)),grid.getCellValue((0,corner)),
								 grid.getCellValue((corner,0)),grid.getCellValue((corner,corner))]
		if max(tiles_in_corner_value) == 0:
			return 0
		else:
			return math.log2(max(tiles_in_corner_value))

	def distance(self,grid):
		dis = None
		max_tile = grid.getMaxTile()
		corner = grid.size - 1
		for x in range(grid.size):
			if dis:
				break
			for y in range(grid.size):
				if max_tile == grid.map[x][y]:
					dis = -min([abs(x - 0) + abs(y - 0),abs(x - 0) + abs(y - corner),
								abs(x - corner) + abs(y - 0),abs(x - corner) + abs(y - corner),])
					break
		return dis

	def smoothness(self,grid):
		smoothness = 0
		for x in range(grid.size):
			for y in range(grid.size):
				s = float('infinity')

				if x > 0:
					s = min(s, abs((grid.map[x][y] or 2) - (grid.map[x - 1][y] or 2)))
				if y > 0:
					s = min(s, abs((grid.map[x][y] or 2) - (grid.map[x][y - 1] or 2)))
				if x < 3:
					s = min(s, abs((grid.map[x][y] or 2) - (grid.map[x + 1][y] or 2)))
				if y < 3:
					s = min(s, abs((grid.map[x][y] or 2) - (grid.map[x][y + 1] or 2)))

				smoothness -= s

		return smoothness

	def montonicity(self,grid):
		totals = [0, 0, 0, 0]

		for x in range(3):

			currentIndex = 0
			nextIndex = currentIndex + 1

			while nextIndex < 4:
				while nextIndex < 4 and grid.map[x][nextIndex] == 0:
					nextIndex += 1

				if nextIndex >= 4:
					nextIndex -= 1

				currentValue = math.log(grid.map[x][currentIndex]) / math.log(2) if grid.map[x][currentIndex] else 0
				nextValue = math.log(grid.map[x][nextIndex]) / math.log(2) if grid.map[x][nextIndex] else 0

				if currentValue > nextValue:
					totals[0] += currentValue + nextValue
				elif nextValue > currentValue:
					totals[1] += currentValue - nextValue

				currentIndex = nextIndex
				nextIndex += 1

		for y in range(3):

			currentIndex = 0
			nextIndex = currentIndex + 1

			while nextIndex < 4:
				while nextIndex < 4 and grid.map[nextIndex][y] == 0:
					nextIndex += 1

				if nextIndex >= 4:
					nextIndex -= 1

				currentValue = math.log(grid.map[currentIndex][y]) / math.log(2) if grid.map[currentIndex][y] else 0
				nextValue = math.log(grid.map[nextIndex][y]) / math.log(2) if grid.map[nextIndex][y] else 0

				if currentValue > nextValue:
					totals[2] += nextValue - currentValue
				elif nextValue > currentValue:
					totals[3] += currentValue - nextValue

				currentIndex = nextIndex
				nextIndex += 1

		return max(totals[0], totals[1]) + max(totals[2], totals[3])
