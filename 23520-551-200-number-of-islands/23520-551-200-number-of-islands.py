class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        nb_islands = 0    
        if not grid:
            return 0

        def bfs(grid, row, col):
            if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]) or grid[row][col] != "1":
                return
            grid[row][col] = "@"
            bfs(grid, row+1, col)
            bfs(grid, row-1, col)
            bfs(grid, row, col+1)
            bfs(grid, row, col-1)

        
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == "1":
                    bfs(grid, row, col)
                    nb_islands += 1
        return nb_islands

