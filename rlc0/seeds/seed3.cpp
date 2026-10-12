#include <vector>

class Solution {
public:
    int search(std::vector<int>& nums, int target) {
        if (nums.size() == 1) {
            return nums[0] == target ? 0 : -1;
        }
        return -1;
    }
};
