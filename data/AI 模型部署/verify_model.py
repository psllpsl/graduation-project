# AutoDL 模型验证脚本
# 使用方法：在 AutoDL JupyterLab 终端执行 python verify_model.py

import os
import torch

print("=" * 60)
print("🔍 AutoDL 模型验证脚本")
print("=" * 60)

# 1. 检查常见模型路径
print("\n📁 检查模型文件位置...\n")

possible_paths = [
    "./dental_qwen_merged",
    "./models/dental_qwen_merged",
    "/root/autodl-tmp/dental_qwen_merged",
    "/root/autodl-tmp/models/dental_qwen_merged",
    "./checkpoints/dental_qwen_lora",
    "/root/autodl-tmp/checkpoints/dental_qwen_lora",
]

found_model_path = None
found_lora_path = None

for path in possible_paths:
    if os.path.exists(path):
        print(f"✅ 找到：{path}")
        
        # 列出文件
        files = os.listdir(path)
        print(f"   文件列表：{files[:10]}{'...' if len(files) > 10 else ''}")
        
        # 判断是完整模型还是 LoRA 权重
        if "model.safetensors" in files or "pytorch_model.bin" in files:
            print(f"   📦 类型：完整模型")
            found_model_path = path
        elif "adapter_model.safetensors" in files or "adapter_config.json" in files:
            print(f"   🔧 类型：LoRA 权重")
            found_lora_path = path
        print()
    else:
        print(f"❌ 不存在：{path}")

# 2. 扫描 autodl-tmp 目录下所有可能的相关文件
print("\n" + "=" * 60)
print("🔍 扫描 /root/autodl-tmp/ 目录...\n")

autodl_tmp = "/root/autodl-tmp"
if os.path.exists(autodl_tmp):
    for root, dirs, files in os.walk(autodl_tmp):
        # 跳过 .git 和其他隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # 检查是否包含模型相关文件
        model_keywords = ["dental", "qwen", "lora", "adapter", "merged", "checkpoint"]
        folder_name = os.path.basename(root).lower()
        
        if any(kw in folder_name for kw in model_keywords):
            print(f"📂 找到相关目录：{root}")
            
            # 列出前 10 个文件
            relevant_files = [f for f in files if f.endswith(('.json', '.bin', '.safetensors'))]
            if relevant_files:
                print(f"   关键文件：{relevant_files[:10]}")
            
            # 估算目录大小
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(root):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
            
            size_gb = total_size / (1024**3)
            print(f"   大小：{size_gb:.2f} GB")
            print()

# 3. 检查 GPU 状态
print("=" * 60)
print("🖥️ GPU 状态检查...\n")

if torch.cuda.is_available():
    print(f"✅ CUDA 可用")
    print(f"   GPU 型号：{torch.cuda.get_device_name(0)}")
    print(f"   显存总量：{torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    print(f"   显存已用：{torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
    print(f"   显存空闲：{torch.cuda.memory_reserved(0) / 1024**3:.2f} GB")
else:
    print("❌ CUDA 不可用")

# 4. 检查依赖
print("\n" + "=" * 60)
print("📦 依赖检查...\n")

dependencies = {
    "torch": "PyTorch",
    "transformers": "Transformers",
    "vllm": "vLLM",
    "peft": "PEFT (LoRA)",
    "accelerate": "Accelerate",
}

for pkg, name in dependencies.items():
    try:
        mod = __import__(pkg)
        version = getattr(mod, "__version__", "unknown")
        print(f"✅ {name}: {version}")
    except ImportError:
        print(f"❌ {name}: 未安装")

# 5. 总结
print("\n" + "=" * 60)
print("📊 验证总结")
print("=" * 60)

if found_model_path:
    print(f"\n✅ 完整模型已找到：{found_model_path}")
    print(f"   可以直接用于部署！")

if found_lora_path:
    print(f"\n✅ LoRA 权重已找到：{found_lora_path}")
    print(f"   需要与基座模型合并后使用")

if found_model_path and found_lora_path:
    print(f"\n💡 建议：使用 LLaMA Factory 合并 LoRA 权重到基座模型")
    print(f"   命令示例:")
    print(f"   llamafactory-cli export \\")
    print(f"       --model_name_or_path Qwen/Qwen2.5-7B-Instruct \\")
    print(f"       --adapter_name_or_path {found_lora_path} \\")
    print(f"       --export_dir ./dental_qwen_merged \\")
    print(f"       --template qwen")
elif not found_model_path and not found_lora_path:
    print(f"\n❌ 未找到模型或 LoRA 权重")
    print(f"   请检查是否已上传到 AutoDL 服务器")
    print(f"   常见位置：/root/autodl-tmp/dental_qwen_merged/")

print("\n" + "=" * 60)
