"""
生成微信小程序占位图标脚本
运行此脚本生成所有需要的 PNG 图标文件
"""

import base64
import os

# 简单的 1x1 像素 PNG（灰色）
GRAY_PNG = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz'
    'AAALEwAACxMBAJqcGAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAABSSURB'
    'VDiN7c0xAQAgDASh+jf9a4wJJDJnZu4BvLN3AwAA8I8IAAAgQgQAAIgQAQAAIkgAAIAIEQAAIEIE'
    'AAAIEAEAACJEAACACBEAACBCBAAAiBABAAAiRAAAgAgRAAAgQgQAAPgxAwAADqPhXAAAAABJRU5E'
    'RK5CYII='
)

# 简单的 1x1 像素 PNG（蓝色）
BLUE_PNG = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz'
    'AAALEwAACxMBAJqcGAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAABpSURB'
    'VDiN7c0xAQAgDASh+jf9a4wJJDJnZu4BvLN3AwAA8I8IAAAgQgQAAIgQAQAAIkgAAIAIEQAAIE'
    'IEAAAIEAEAACJEAACACBEAACBCBAAAiBABAAAiRAAAgAgRAAAgQgQAAPgxAwAADqPhXAAAAABJRU5E'
    'RK5CYII='
)

def create_placeholder_png(filename, color='gray'):
    """创建占位 PNG 文件"""
    content = BLUE_PNG if color == 'blue' else GRAY_PNG
    with open(filename, 'wb') as f:
        f.write(content)
    print("[OK] 已创建：" + filename)

# 创建所有图标文件
icons = [
    # TabBar 图标（灰色 - 未选中）
    ('chat.png', 'gray'),
    ('appointment.png', 'gray'),
    ('knowledge.png', 'gray'),
    ('profile.png', 'gray'),
    # TabBar 图标（蓝色 - 选中）
    ('chat-active.png', 'blue'),
    ('appointment-active.png', 'blue'),
    ('knowledge-active.png', 'blue'),
    ('profile-active.png', 'blue'),
    # 头像图标
    ('ai-avatar.png', 'blue'),
    ('user-avatar.png', 'gray'),
]

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

print("开始生成占位图标...")
print("=" * 40)

for icon_name, color in icons:
    icon_path = os.path.join(script_dir, icon_name)
    create_placeholder_png(icon_path, color)

print("=" * 40)
print("[OK] 所有图标已生成完成！")
print("")
print("注意：这些是 1x1 像素的占位图标")
print("请替换为实际的 81x81 像素图标文件")
