class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        x = []
        n = len(nums)
        for i in range(n):
            for j in range(i, n):
                for k in range(j,n):
                    if nums[i] + nums[j] + nums[k] == 0 and i != j and i != k and j != k:
                        x.append(sorted([nums[i], nums[j], nums[k]]))
        print(x)
        x = [list(i) for i in set(tuple(i) for i in x)]
        print(x)

s = Solution()
s.threeSum([-1,0,1,2,-1,-4])