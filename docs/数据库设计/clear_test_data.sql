-- ============================================
-- 清空测试数据脚本
-- 用途：清空患者、复诊、对话数据，重新开始测试
-- 执行日期：2026-03-11
-- ============================================

USE dental_clinic;

-- ============================================
-- 1. 清空数据
-- ============================================

-- 清空对话记录
DELETE FROM dialogues;

-- 清空复诊计划
DELETE FROM appointments;

-- 清空患者数据
DELETE FROM patients;

-- ============================================
-- 2. 重置自增 ID（可选，让 ID 从 1 开始）
-- ============================================

ALTER TABLE dialogues AUTO_INCREMENT = 1;
ALTER TABLE appointments AUTO_INCREMENT = 1;
ALTER TABLE patients AUTO_INCREMENT = 1;

-- ============================================
-- 3. 验证清空结果
-- ============================================

SELECT 'patients' AS table_name, COUNT(*) AS row_count FROM patients
UNION ALL
SELECT 'appointments', COUNT(*) FROM appointments
UNION ALL
SELECT 'dialogues', COUNT(*) FROM dialogues;

-- 预期结果：全部为 0
