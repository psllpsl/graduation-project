#!/bin/bash
# AutoDL 牙科修复 AI 模型 - Transformers 启动脚本
# 使用方法：bash start_tr.sh

echo ""
echo "============================================================"
echo "     牙科修复 AI 模型 - Transformers 启动脚本"
echo "============================================================"
echo ""

# 配置
MODEL_PATH="./models/dental_qwen_merged"
PORT=6008
LOG_FILE="inference.log"

echo "模型路径：$MODEL_PATH"
echo "服务端口：$PORT"
echo ""

# 检查模型
if [ ! -d "$MODEL_PATH" ]; then
    echo "❌ 错误：模型目录不存在！"
    echo "   路径：$MODEL_PATH"
    exit 1
fi

echo "✅ 模型目录存在"

# 停止旧服务
echo ""
echo "检查旧服务..."
OLD_PID=$(ps aux | grep "start_inference.py" | grep -v grep | awk '{print $2}')
if [ -n "$OLD_PID" ]; then
    echo "⚠️  发现运行中的服务 (PID: $OLD_PID)，正在停止..."
    kill $OLD_PID
    sleep 2
    echo "✅ 旧服务已停止"
else
    echo "✅ 没有运行中的服务"
fi

echo ""
echo "启动推理服务..."

# 启动服务
cd /root/autodl-tmp
nohup python start_inference.py --port $PORT --model_path $MODEL_PATH > $LOG_FILE 2>&1 &
PID=$!

echo "✅ 服务已启动 (PID: $PID)"
echo ""

# 等待启动
echo "等待服务启动中..."
for i in {1..20}; do
    if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
        echo "✅ 服务启动成功！"
        break
    fi
    if [ $i -eq 20 ]; then
        echo "❌ 启动失败，请检查日志："
        echo "   tail -f $LOG_FILE"
        exit 1
    fi
    sleep 1
done

echo ""
echo "============================================================"
echo "        🎉 服务启动完成！"
echo "============================================================"
echo ""
echo "📊 服务信息："
echo "   端口：$PORT"
echo "   内网：http://localhost:$PORT"
echo ""
echo "📋 常用命令："
echo "   查看日志：tail -f $LOG_FILE"
echo "   测试：curl http://localhost:$PORT/test"
echo "   停止：kill $PID"
echo ""
