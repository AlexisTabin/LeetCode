class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        smallest_price = prices[0]
        max_overall = 0
        for i, price in enumerate(prices):
            diff = price - smallest_price
            max_overall = max(diff, max_overall)
            smallest_price = min(price, smallest_price)
                
            
        return max_overall