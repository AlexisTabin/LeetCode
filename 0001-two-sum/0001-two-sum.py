class Solution:
    def twoSumFirstTry(self, nums: List[int], target: int) -> List[int]:
        for index_out, num_out in enumerate(nums):
            print(f"Trying with : {num_out}\n")
            for index_in, num_in in enumerate(nums):
                print(f"And with : {num_in}\n")
                addup = num_out + num_in
                if addup == target:
                    if index_out != index_in:
                        print(f"Addup correct ! : {addup}")
                        return [index_out, index_in]

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)

        hashmap = {}
        for i in range(n):
            hashmap[nums[i]] = i

        for i in range(n):
            second_nb = target - nums[i]
            if second_nb in hashmap and hashmap[second_nb] != i :
                return [i, hashmap[second_nb]]

        return []   