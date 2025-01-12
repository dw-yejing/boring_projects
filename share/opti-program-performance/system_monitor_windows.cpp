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
#include <windows.h>
#include <comdef.h>
#include <Wbemidl.h>
#pragma comment(lib, "wbemuuid.lib")


class ThreadPerformanceTest {
private:
    int physical_cores;
    int logical_cores;
    std::vector<double> performance_results;
    
    void get_cpu_info() {
        SYSTEM_INFO sysInfo;
        GetSystemInfo(&sysInfo);
        logical_cores = sysInfo.dwNumberOfProcessors;

        // 使用GetLogicalProcessorInformation获取物理核心数
        DWORD length = 0;
        GetLogicalProcessorInformation(nullptr, &length);
        if (length > 0) {
            std::vector<SYSTEM_LOGICAL_PROCESSOR_INFORMATION> buffer(length / sizeof(SYSTEM_LOGICAL_PROCESSOR_INFORMATION));
            if (GetLogicalProcessorInformation(buffer.data(), &length)) {
                physical_cores = 0;
                for (const auto& info : buffer) {
                    if (info.Relationship == RelationProcessorCore) {
                        physical_cores++;
                    }
                }
            }
        }
        
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
        SYSTEM_INFO sysInfo;
        GetSystemInfo(&sysInfo);
        logical_cores = sysInfo.dwNumberOfProcessors;

        // 使用GetLogicalProcessorInformation获取物理核心数
        DWORD length = 0;
        GetLogicalProcessorInformation(nullptr, &length);
        if (length > 0) {
            std::vector<SYSTEM_LOGICAL_PROCESSOR_INFORMATION> buffer(length / sizeof(SYSTEM_LOGICAL_PROCESSOR_INFORMATION));
            if (GetLogicalProcessorInformation(buffer.data(), &length)) {
                physical_cores = 0;
                for (const auto& info : buffer) {
                    if (info.Relationship == RelationProcessorCore) {
                        physical_cores++;
                    }
                }
            }
        }
        
        if (physical_cores == 0) {
            physical_cores = logical_cores;
        }
    }

    double run_process_task(int num_processes) {
        const int iterations_per_process = 10000000;
        auto start_time = std::chrono::high_resolution_clock::now();

        std::vector<HANDLE> processes;
        for (int i = 0; i < num_processes; ++i) {
            STARTUPINFOA si;
            PROCESS_INFORMATION pi;
            ZeroMemory(&si, sizeof(si));
            si.cb = sizeof(si);
            ZeroMemory(&pi, sizeof(pi));

            // 获取当前程序的路径
            char buffer[MAX_PATH];
            GetModuleFileNameA(NULL, buffer, MAX_PATH);
            std::string command = std::string(buffer) + " --process-task " + 
                                std::to_string(iterations_per_process);

            // 创建新进程
            if (CreateProcessA(NULL, const_cast<LPSTR>(command.c_str()),
                NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
                processes.push_back(pi.hProcess);
                CloseHandle(pi.hThread);
            }
        }

        // 等待所有进程完成
        WaitForMultipleObjects(static_cast<DWORD>(processes.size()), 
                             processes.data(), TRUE, INFINITE);

        // 清理进程句柄
        for (HANDLE h : processes) {
            CloseHandle(h);
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