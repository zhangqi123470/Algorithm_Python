import java.util.Arrays;
import java.util.List;

public class demo {
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }
}

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
       // 先对数组进行排序
       Arrays.sort(strs);
       // Java 中需要创建实例或使用静态方法
    String[] chars = strs[0].chars()
    .mapToObj(c -> String.valueOf((char) c))
    .toArray(String[]::new);
Arrays.sort(chars);
String key = String.join("", chars);  // 需要静态方法
        return null;

    }
}

