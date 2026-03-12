-- ============================================
-- 删除 treatment_records 和 system_config 表
-- 执行日期：2026-03-11
-- ============================================

USE dental_clinic;

-- 删除治疗记录表
DROP TABLE IF EXISTS `treatment_records`;

-- 删除系统配置表
DROP TABLE IF EXISTS `system_config`;

-- 验证删除成功（应该剩 5 张表）
SHOW TABLES;
