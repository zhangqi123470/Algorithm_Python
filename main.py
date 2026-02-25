import heapq
import math
from typing import List
from heapq import *
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        heap_q=[] #the max_heap is also an Array
        # declare the heap
        heap_q=[(-nums[i],i) for i in range(k)] # initialized the heap_q,now the heap_q 
        # is just an Array
        # using the build-in method 
        heapq.heapify(heap_q)
        ans =[]
        # push the elements to the heap
        for i in range(k-1,len(nums)):
            # the heapq should pop the top of the heap
            # push the element into heap
            heapq.heappush(heap_q,(-nums[i],i))
            # pop the heap_top which not longer in the sliding windows 
            while heap_q[0][1]<=i-k:
                heapq.heappop(heap_q)# if now the sliding windows is 3,-1,-3
            current_element=-heap_q[0][0]
            ans.append(current_element)# the max number of the heap

        return ans  

if __name__ == '__main__':
    # Create an instance of the Solution class
    sol = Solution()
    
    # Test with sample input
    test_nums = [1, 3, -1, -3, 5, 3, 6, 7]
    test_k = 3
    
    # Call the method and get result
    result = sol.maxSlidingWindow(test_nums, test_k)
    
    # Print the result
    print(f"Input array: {test_nums}")
    print(f"Window size: {test_k}")
    print(f"Max sliding window result: {result}")