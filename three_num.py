from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        ## 返回不相同的三元组
        ## 双指针,pointer1:  
        # pointer2 
        # 一次遍历
            # 双指针 :先进行排序，限制指针移动的方向
            nums.sort()
            res=[]
            for i in range(0,len(nums)-1):
                left=i+1
                right=len(nums)-1
                # 与target进行比较
                while left<len(nums) and right<len(nums) and left<right:
                    sum=nums[right]+nums[left]+nums[i]
                    if sum==0:
                        res.append([nums[i],nums[left],nums[right]])
                    
                    left+=1
                    right-=1
            return res

if __name__ =="__main__":
    example_list=[-1,0,1,2,-1,-4]
    solution =Solution()
    print(solution.threeSum(example_list))

                
                    
