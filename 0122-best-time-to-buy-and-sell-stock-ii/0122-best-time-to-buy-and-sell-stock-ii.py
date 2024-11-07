class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if prices is None:
            return 0
        profit = 0
        for i, price in enumerate(prices):
            if i == 0:
                continue
            last_element = prices[i-1]
            if price > last_element:
                profit += price - last_element
            print("Price : ", price)
            print("Last  : ", last_element)
            print("Profit: ", profit)
                
        return profit
                