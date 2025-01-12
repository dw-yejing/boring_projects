#include <iostream>
#include <vector>
#include <chrono>
#include <thread>
#include <fstream>
#include <cstdlib>
#include <string>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <sys/wait.h>
#include <sys/types.h>

class ThreadPerformanceTest {
private:
    int physical_cores;
    int logical_cores;
    std::vector<double> performance_results;
    
    void get_cpu_info() {
        logical_cores = sysconf(_SC_NPROCESSORS_ONLN);
        
        int sockets = 0;
        int cores_per_socket = 0;
        
        // 获取CPU插槽数
        FILE* fp = popen("lscpu | grep 'Socket(s)' | awk '{print $2}'", "r");
        if (fp) {
            char buffer[128];
            if (fgets(buffer, sizeof(buffer), fp) != nullptr) {
                sockets = atoi(buffer);
            }
            pclose(fp);
        }
        
        // 获取每个插槽的核心数
        fp = popen("lscpu | grep 'Core(s) per socket' | awk '{print $4}'", "r");
        if (fp) {
            char buffer[128];
            if (fgets(buffer, sizeof(buffer), fp) != nullptr) {
                cores_per_socket = atoi(buffer);
            }
            pclose(fp);
        }
        
        // 计算总物理核心数
        physical_cores = sockets * cores_per_socket;
        
        // 如果获取失败，使用逻辑核心数作为备选
        if (physical_cores == 0) {
            physical_cores = logical_cores;
        }
    }

public:
    // 模拟CPU密集型任务
    static void cpu_intensive_task(int iterations) {
        volatile double result = 0;
        for (int i = 0; i < iterations; ++i) {
            result += sin(i) * cos(i);
        }
    }

private:
    // 使用指定数量的线程运行任务并测量性能
    double run_parallel_task(int num_threads) {
        const int iterations_per_thread = 10000000;
        std::vector<std::thread> threads;
        
        auto start_time = std::chrono::high_resolution_clock::now();
        
        // 创建指定数量的线程
        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back(cpu_intensive_task, iterations_per_thread);
        }
        
        // 等待所有线程完成
        for (auto& thread : threads) {
            thread.join();
        }
        
        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
        
        return static_cast<double>(iterations_per_thread * num_threads) / duration.count();
    }

public:
    ThreadPerformanceTest() {
        get_cpu_info();
    }

    void run_performance_test() {
        std::cout << "Running performance tests with different thread counts...\n";
        
        // 测试从1个线程到逻辑核心数*2的性能
        for (int thread_count = 1; thread_count <= logical_cores * 2; ++thread_count) {
            double performance = run_parallel_task(thread_count);
            performance_results.push_back(performance);
            
            std::cout << "Threads: " << thread_count 
                      << ", Performance: " << performance 
                      << " operations/ms\n";
        }
    }

    void save_results(const std::string& filename) {
        std::ofstream file(filename);
        if (file.is_open()) {
            file << "CPU Information\n";
            file << "Physical Cores," << physical_cores << "\n";
            file << "Logical Cores," << logical_cores << "\n\n";
            file << "Thread Count,Performance\n";
            
            for (size_t i = 0; i < performance_results.size(); ++i) {
                file << (i + 1) << "," << performance_results[i] << "\n";
            }
            file.close();
        }
    }

    void print_cpu_info() {
        std::cout << "CPU Information:\n";
        std::cout << "Physical Cores: " << physical_cores << "\n";
        std::cout << "Logical Cores (with Hyper-Threading): " << logical_cores << "\n";
    }
};

class ProcessPerformanceTest {
private:
    int physical_cores;
    int logical_cores;
    std::vector<double> performance_results;
    
    void get_cpu_info() {
        logical_cores = sysconf(_SC_NPROCESSORS_ONLN);
        
        int sockets = 0;
        int cores_per_socket = 0;
        
        // 获取CPU插槽数
        FILE* fp = popen("lscpu | grep 'Socket(s)' | awk '{print $2}'", "r");
        if (fp) {
            char buffer[128];
            if (fgets(buffer, sizeof(buffer), fp) != nullptr) {
                sockets = atoi(buffer);
            }
            pclose(fp);
        }
        
        // 获取每个插槽的核心数
        fp = popen("lscpu | grep 'Core(s) per socket' | awk '{print $4}'", "r");
        if (fp) {
            char buffer[128];
            if (fgets(buffer, sizeof(buffer), fp) != nullptr) {
                cores_per_socket = atoi(buffer);
            }
            pclose(fp);
        }
        
        // 计算总物理核心数
        physical_cores = sockets * cores_per_socket;
        
        // 如果获取失败，使用逻辑核心数作为备选
        if (physical_cores == 0) {
            physical_cores = logical_cores;
        }
    }

    double run_process_task(int num_processes) {
        const int iterations_per_process = 10000000;
        auto start_time = std::chrono::high_resolution_clock::now();

        std::vector<pid_t> processes;
        char path[1024];
        ssize_t count = readlink("/proc/self/exe", path, sizeof(path) - 1);
        if (count != -1) {
            path[count] = '\0';
            for (int i = 0; i < num_processes; ++i) {
                pid_t pid = fork();
                if (pid == 0) {  // 子进程
                    // 执行相同的程序，但带上参数
                    execl(path, path, "--process-task", 
                          std::to_string(iterations_per_process).c_str(), 
                          (char*)NULL);
                    exit(1);  // 如果execl失败
                } else if (pid > 0) {  // 父进程
                    processes.push_back(pid);
                }
            }

            // 等待所有子进程完成
            for (pid_t pid : processes) {
                int status;
                waitpid(pid, &status, 0);
            }
        }

        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
        
        return static_cast<double>(iterations_per_process * num_processes) / duration.count();
    }

public:
    ProcessPerformanceTest() {
        get_cpu_info();
    }

    void run_performance_test() {
        std::cout << "Running performance tests with different process counts...\n";
        
        // 测试从1个进程到逻辑核心数的性能
        for (int process_count = 1; process_count <= logical_cores*2; ++process_count) {
            double performance = run_process_task(process_count);
            performance_results.push_back(performance);
            
            std::cout << "Processes: " << process_count 
                      << ", Performance: " << performance 
                      << " operations/ms\n";
        }
    }

    void save_results(const std::string& filename) {
        std::ofstream file(filename);
        if (file.is_open()) {
            file << "Process Performance Results\n";
            file << "Physical Cores," << physical_cores << "\n";
            file << "Logical Cores," << logical_cores << "\n\n";
            file << "Process Count,Performance\n";
            
            for (size_t i = 0; i < performance_results.size(); ++i) {
                file << (i + 1) << "," << performance_results[i] << "\n";
            }
            file.close();
        }
    }

    void print_cpu_info() {
        std::cout << "\nProcess Test CPU Information:\n";
        std::cout << "Physical Cores: " << physical_cores << "\n";
        std::cout << "Logical Cores: " << logical_cores << "\n";
    }
};

int main(int argc, char* argv[]) {
    // 检查是否是子进程执行CPU密集型任务
    if (argc > 2 && std::string(argv[1]) == "--process-task") {
        int iterations = std::stoi(argv[2]);
        ThreadPerformanceTest::cpu_intensive_task(iterations);
        return 0;
    }

    // 主程序流程
    std::cout << "=== Thread Performance Test ===\n";
    ThreadPerformanceTest thread_test;
    thread_test.print_cpu_info();
    thread_test.run_performance_test();
    thread_test.save_results("thread_performance.csv");

    std::cout << "\n=== Process Performance Test ===\n";
    ProcessPerformanceTest process_test;
    process_test.print_cpu_info();
    process_test.run_performance_test();
    process_test.save_results("process_performance.csv");

    return 0;
} 