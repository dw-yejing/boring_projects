import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置样式
plt.style.use('seaborn')
sns.set_palette("husl")

# 创建图表
plt.figure(figsize=(12, 8))

# 读取线程性能数据
thread_df = pd.read_csv('thread_performance.csv', skiprows=3)  # 跳过CPU信息部分
with open('thread_performance.csv', 'r') as f:
    lines = f.readlines()
    physical_cores = int(lines[1].split(',')[1])
    logical_cores = int(lines[2].split(',')[1])

# 读取进程性能数据
process_df = pd.read_csv('process_performance.csv', skiprows=3)  # 跳过CPU信息部分

# 绘制性能曲线
plt.plot(thread_df['Thread Count'], thread_df['Performance'], 
         marker='o', label='Thread Performance', color='blue')
plt.plot(process_df['Process Count'], process_df['Performance'], 
         marker='s', label='Process Performance', color='orange')

# 添加垂直线标记物理核心数和逻辑核心数
plt.axvline(x=physical_cores, color='r', linestyle='--', 
            label=f'Physical Cores ({physical_cores})')
plt.axvline(x=logical_cores, color='g', linestyle='--', 
            label=f'Logical Cores ({logical_cores})')

# 设置图表属性
plt.title('Thread vs Process Performance Comparison')
plt.xlabel('Number of Threads/Processes')
plt.ylabel('Performance (operations/ms)')
plt.grid(True)
plt.legend()

# 保存图表
plt.savefig('performance_comparison.png')
plt.show() 