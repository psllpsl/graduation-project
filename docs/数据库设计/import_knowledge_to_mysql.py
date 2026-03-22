"""
将 804 条知识库数据导入 MySQL 数据库
"""
import json
import pymysql
from datetime import datetime

# 数据库配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '267091212',
    'database': 'dental_clinic',
    'charset': 'utf8mb4'
}

# 知识库 JSON 文件路径
json_file_path = r'D:\Project\毕业设计\data\knowledge\knowledge_base_v3.json'

def import_knowledge():
    """导入知识库数据到 MySQL"""
    
    # 读取 JSON 文件
    print(f"正在读取 {json_file_path}...")
    with open(json_file_path, 'r', encoding='utf-8') as f:
        knowledge_list = json.load(f)
    
    print(f"共读取 {len(knowledge_list)} 条知识库数据")
    
    # 连接数据库
    print(f"正在连接数据库...")
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    # 清空现有数据
    print("正在清空现有数据...")
    cursor.execute("DELETE FROM knowledge_base")
    conn.commit()
    
    # 插入数据
    print("正在导入数据...")
    insert_sql = """
    INSERT INTO knowledge_base (category, title, content, keywords, source, is_active)
    VALUES (%s, %s, %s, %s, %s, 1)
    """
    
    success_count = 0
    error_count = 0
    
    for i, item in enumerate(knowledge_list, 1):
        try:
            cursor.execute(insert_sql, (
                item.get('category', ''),
                item.get('title', ''),
                item.get('content', ''),
                item.get('keywords', ''),
                item.get('source', '《口腔修复学》第 8 版')
            ))
            success_count += 1
            
            if i % 100 == 0:
                print(f"已导入 {i} 条...")
                
        except Exception as e:
            print(f"导入第 {i} 条数据失败：{e}")
            error_count += 1
    
    # 提交事务
    conn.commit()
    
    # 验证数据
    print("\n正在验证数据...")
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    total_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT category, COUNT(*) AS count 
        FROM knowledge_base 
        GROUP BY category 
        ORDER BY count DESC
    """)
    category_stats = cursor.fetchall()
    
    print(f"\n✅ 导入完成！")
    print(f"成功导入：{success_count} 条")
    print(f"导入失败：{error_count} 条")
    print(f"数据库中共有：{total_count} 条")
    
    print(f"\n按分类统计:")
    for category, count in category_stats:
        print(f"  {category}: {count} 条")
    
    # 关闭连接
    cursor.close()
    conn.close()
    print("\n数据库连接已关闭")

if __name__ == '__main__':
    import_knowledge()
