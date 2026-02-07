## 盛水最多的容器
# 遍历
# 双指针
# 缩小检索范围
# 设当前的短板为x，长板为y，如果当前容器的容积不是最大的，则更大的容器只可能是：x右移后的板与y构成的容器
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        # 双指针，left:0,right:len(int),
        ## python 语法：集合内置方法:指针
        left=0
        right=len(height)-1
        maxVolume=0
        while left!=right:
            ##  记录当前容器可以存储水的容积
            # 记录当前的short和long木板，迭代short
            short_height=min(height[left],height[right])
            ## 更新maxVolume
            currentVolume=short_height*(right-left)
            if currentVolume>maxVolume:
                maxVolume=currentVolume
        #更新left和right
            if short_height==height[left]:
                left+=1
            else :right-=1
        return maxVolume

if __name__=="__main__":
    nums=[1,3,5,6,3,3]
    # nums=example_string
    solution=Solution()
    print(solution.maxArea(nums))