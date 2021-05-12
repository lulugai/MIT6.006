import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        energy = {}
        for i in range(self.width):
            for j in range(self.height):
                energy[i, j] = self.energy(i, j)
        dp = {}
        for i in range(self.width):
            dp[i, 0] = energy[i, 0]

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
