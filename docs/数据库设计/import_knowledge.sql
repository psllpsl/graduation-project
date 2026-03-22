-- ============================================
-- 导入 804 条知识库数据
-- 数据库：dental_clinic
-- 数据来源：data/knowledge/knowledge_base_v3.json
-- ============================================

USE dental_clinic;

-- 先清空现有数据
DELETE FROM knowledge_base;

-- 插入知识库数据（804 条）
-- 由于数据量较大，这里使用 Python 脚本导入
-- 执行：python import_knowledge_to_mysql.py

-- ============================================
-- 验证数据
-- ============================================
SELECT 'knowledge_base' AS table_name, COUNT(*) AS row_count FROM knowledge_base;

-- 按分类统计
SELECT category, COUNT(*) AS count 
FROM knowledge_base 
GROUP BY category 
ORDER BY count DESC;
