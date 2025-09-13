import os
import time
import subprocess
import shutil
import glob
from pathlib import Path

class XDABenchmark:
    def __init__(self, base_dir="/pro/decom/third-test"):
        self.base_dir = Path(base_dir)
        self.bytecode1_dir = self.base_dir / "bytecode1"
        self.bytecode2_dir = self.base_dir / "bytecode2"
        self.temp_bytecode_dir = self.base_dir / "bytecode"
        
    def cleanup_intermediate_files(self):
        """清理中间生成的文件和目录，但保留重要的目录结构"""
        print("Cleaning up intermediate files...")
        
        # 清理目录列表 - 清空内容但保留目录结构  
        cleanup_dirs_empty = [
            ".temp",
            "all_contract_tac",
            "predict",
            "detect-library", 
            "rate",
            "count",
            "vul",
            "preprocess"
        ]
        
        # 清理文件列表
        cleanup_files = [
            "results.json",
            "count.csv", 
            "rate.csv",
            "exp3.csv"
        ]
        
        # 清空目录但保留目录结构
        for dir_path in cleanup_dirs_empty:
            full_path = self.base_dir / dir_path
            if full_path.exists() and full_path.is_dir():
                for item in full_path.iterdir():
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                #print(f"  Cleaned directory: {dir_path}")
            else:
                # 如果目录不存在则创建
                full_path.mkdir(parents=True, exist_ok=True)
                #print(f"  Created directory: {dir_path}")
        
        # 删除文件
        for file_path in cleanup_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                full_path.unlink()
                print(f"  Removed file: {file_path}")
        
        # 清理gigahorse可能生成的临时文件
        """pattern_files = [
            "*.facts",
            "*.out"
        ]
        
        for pattern in pattern_files:
            for file_path in self.base_dir.glob(pattern):
                if file_path.is_file():
                    try:
                        file_path.unlink()
                        print(f"  Removed pattern file: {file_path.relative_to(self.base_dir)}")
                    except:
                        pass"""
    
    def setup_temp_directory(self):
        """创建临时bytecode目录"""
        if self.temp_bytecode_dir.exists():
            shutil.rmtree(self.temp_bytecode_dir)
        self.temp_bytecode_dir.mkdir()
        
        # 确保.temp目录存在（decompile.py需要）
        temp_dir = self.base_dir / ".temp"
        if not temp_dir.exists():
            temp_dir.mkdir()
            print("Created .temp directory for decompile.py")
        
        # 确保其他必要的目录存在
        required_dirs = [
            "preprocess",
            "preprocess/dasm",
            "preprocess/new_dasm", 
            "preprocess/data",
            "preprocess/true_data",
            "preprocess/true_label",
            "preprocess/no_log_dasm",
            "preprocess/new_bytecode",
            "all_contract_tac",
            "predict",
            "detect-library",
            "rate",
            "count",
            "vul"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.base_dir / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True)
                print(f"Created directory: {dir_name}")
    
    def cleanup_temp_directory(self):
        """清理临时目录"""
        if self.temp_bytecode_dir.exists():
            shutil.rmtree(self.temp_bytecode_dir)
    
    def copy_contract_to_temp(self, contract_path):
        """将单个合约复制到临时目录"""
        dest_path = self.temp_bytecode_dir / contract_path.name
        shutil.copy2(contract_path, dest_path)
        return dest_path
    
    def run_step_with_timing(self, script_name, step_name):
        """运行单个步骤并测量时间"""
        print(f"Running {step_name}...")
        start_time = time.time()
        
        # 对不同步骤设置不同的超时时间
        timeout_map = {
            "1. Decompilation": 1200000,  # 反编译步骤1分钟超时
            "2. Data Preprocessing": 30,
            "3. Function Boundary Recovery": 300,
            "4. Library Detection": 30,
            "5. Taint Analysis": 3000
        }
        timeout = timeout_map.get(step_name, 60)
        
        try:
            result = subprocess.run(
                ["python3", script_name],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            if result.returncode == 0:
                print(f"✓ {step_name} completed in {execution_time:.2f} seconds")
                return execution_time, True
            else:
                print(f"✗ {step_name} failed:")
                print(f"  Return code: {result.returncode}")
                if result.stderr.strip():
                    print(f"  Error: {result.stderr.strip()[:500]}")
                if result.stdout.strip():
                    print(f"  Output: {result.stdout.strip()[:500]}")
                return execution_time, False
                
        except subprocess.TimeoutExpired:
            print(f"✗ {step_name} timed out after {timeout} seconds")
            # 尝试杀死相关进程
            subprocess.run(["pkill", "-f", script_name], capture_output=True)
            subprocess.run(["pkill", "-f", "gigahorse"], capture_output=True)
            return timeout, False
        except Exception as e:
            print(f"✗ {step_name} error: {str(e)}")
            return 0, False
    
    def test_decompilation_only(self, contract_path):
        """只测试反编译步骤"""
        print(f"\n{'='*50}")
        print(f"Testing decompilation only: {contract_path.name}")
        print(f"{'='*50}")
        
        # 设置临时目录
        self.setup_temp_directory()
        self.copy_contract_to_temp(contract_path)
        
        # 只运行反编译步骤
        execution_time, success = self.run_step_with_timing("decompile.py", "1. Decompilation")
        
        # 清理临时目录
        self.cleanup_temp_directory()
        
        return execution_time, success
    
    def run_complete_pipeline(self, contract_path):
        """运行完整的工具链并记录每步时间"""
        print(f"\n{'='*50}")
        print(f"Testing contract: {contract_path.name}")
        print(f"{'='*50}")
        
        # 清理之前的中间文件
        self.cleanup_intermediate_files()
        
        # 设置临时目录
        self.setup_temp_directory()
        self.copy_contract_to_temp(contract_path)
        
        steps = [
            ("decompile.py", "1. Decompilation"),
            ("preprocess.py", "2. Data Preprocessing"),
            ("predict.py", "3. Function Boundary Recovery"),
            ("validate.py", "4. Library Detection"),
            ("vul-detectionviataintanalysis.py", "5. Taint Analysis")
        ]
        
        step_times = {}
        total_time = 0
        successful_steps = 0
        
        for script, step_name in steps:
            execution_time, success = self.run_step_with_timing(script, step_name)
            step_times[step_name] = execution_time
            total_time += execution_time
            
            if success:
                successful_steps += 1
            else:
                print(f"Pipeline stopped at {step_name}")
                break
        
        # 清理临时目录
        self.cleanup_temp_directory()
        
        return step_times, total_time, successful_steps == len(steps)
    
    def test_single_contract(self, dataset_name, dataset_dir):
        """测试单个合约"""
        contracts = list(dataset_dir.glob("*.hex"))
        if not contracts:
            print(f"No .hex files found in {dataset_dir}")
            return None
        
        # 选择最小的合约进行测试
        contracts_with_size = []
        for contract in contracts:
            """ size = contract.stat().st_size
            contracts_with_size.append((contract, size))
        
            # 按文件大小排序，选择最小的
            contracts_with_size.sort(key=lambda x: x[1])
            test_contract = contracts_with_size[0][0]
            file_size = contracts_with_size[0][1]
            
            print(f"\nTesting {dataset_name} with smallest contract: {test_contract.name} (Size: {file_size} bytes)")"""

            step_times, total_time, success = self.run_complete_pipeline(contract)
        
        if success:
            print(f"\n✓ Complete pipeline successful for {dataset_name}")
            print(f"Total time: {total_time:.2f} seconds")
            print("\nStep breakdown:")
            for step, time_taken in step_times.items():
                print(f"  {step}: {time_taken:.2f}s")
        else:
            print(f"\n✗ Pipeline failed for {dataset_name}")
        
        return step_times, total_time, success
    
    def run_benchmark(self):
        """运行基准测试"""
        print("XDA Tool Benchmark - Single Contract Test")
        print("=" * 60)
        
        results = {}
        
        # 测试 bytecode1 数据集
        if self.bytecode1_dir.exists():
            results['bytecode1'] = self.test_single_contract("Bytecode1", self.bytecode1_dir)
        else:
            print(f"Bytecode1 directory not found: {self.bytecode1_dir}")
        
        # 测试 bytecode2 数据集
        if self.bytecode2_dir.exists():
            results['bytecode2'] = self.test_single_contract("Bytecode2", self.bytecode2_dir)
        else:
            print(f"Bytecode2 directory not found: {self.bytecode2_dir}")
        
        # 输出汇总结果
        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)
        
        for dataset_name, result in results.items():
            if result and result[2]:  # 如果测试成功
                step_times, total_time, success = result
                print(f"\n{dataset_name.upper()} Results:")
                print(f"  Total Pipeline Time: {total_time:.2f} seconds")
                for step, time_taken in step_times.items():
                    print(f"  {step}: {time_taken:.2f}s")
            else:
                print(f"\n{dataset_name.upper()}: Test failed or not run")

if __name__ == "__main__":
    benchmark = XDABenchmark(os.getcwd())
    benchmark.run_benchmark()
