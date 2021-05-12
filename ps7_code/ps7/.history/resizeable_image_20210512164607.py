import imagematrix
import sys

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        energy = {}
        for i in range(self.width):
            for j in range(self.height):
                energy[i, j] = self.energy(i, j)
        dp = {}
        for i in range(self.width):
            dp[i, 0] = energy[i, 0]

        backpointer = {}
        for j in range(1, self.height):
            for i in range(self.width):
                dp[i, j] = energy[i, j] + dp[i, j-1]
                backpointer[i, j] = 0
                if i != 0:
                    if dp[i, j] > energy[i, j] + dp[i-1, j-1]:
                        dp[i, j] = energy[i, j] + dp[i-1, j-1]
                        backpointer[i, j] = -1
                if i != self.width - 1:
                    if dp[i, j] > energy[i, j] + dp[i+1, j-1]:
                        dp[i, j] = energy[i, j] + dp[i+1, j-1]
                        backpointer[i, j] = 1
        #bestvalue in bottom row
        best_value = sys.maxint
        index = None
        for i in range(self.width):
            if best_value > dp[i, self.height-1]:
                best_value = dp[i, self.height-1]
                index = i
        #follow backpoints up
        stream = []
        for j in range(self.height-1, 0, -1):
            stream.append((index, j))
            index = index + backpointer[index, j]
        stream.append(index, 0)
        return stream
        

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
