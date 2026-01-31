import sys
import datetime

def greet_user(name):
    """
    一个简单的问候函数，展示 Python 的基础语法
    """
    # 获取当前小时数
    current_hour = datetime.datetime.now().hour
    
    if current_hour < 12:
        greeting = "早上好"
    elif 12 <= current_hour < 18:
        greeting = "下午好"
    else:
        greeting = "晚上好"
        
    return f"你好, {name}! {greeting}。欢迎来到 Python 的世界！"

def main():
    try:
        # 1. 打印 Python 解释器路径（帮你确认 VS Code 是否选对了环境）
        print(f"--- 当前使用的 Python 路径 ---")
        print(sys.executable)
        print("-" * 30)

        # 2. 基础交互
        user_name = input("请输入你的名字: ") or "开发者"
        print(greet_user(user_name))

        # 3. 列表推导式示例：生成 1 到 10 的平方
        squares = [x**2 for x in range(1, 11)]
        print(f"\n1到10的平方列表: {squares}")

    except KeyboardInterrupt:
        print("\n程序已被用户停止。")
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main()