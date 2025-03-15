class Solution:
    def passThePillow(self, n: int, time: int) -> int:
        # naive implementation would be with a loop over range(time)
        nb_s_per_cycle = n * 2 - 2
        return n - abs(n - 1 - time % (nb_s_per_cycle))
