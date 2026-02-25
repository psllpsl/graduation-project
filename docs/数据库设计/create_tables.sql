-- ============================================
-- 数据库：dental_clinic
-- 描述：基于 AI 智能客服的牙科修复复诊提醒与管理系统
-- 创建日期：2026-02-22
-- 版本：v1.3
-- ============================================

-- ============================================
-- 创建数据库
-- ============================================
DROP DATABASE IF EXISTS `dental_clinic`;
CREATE DATABASE IF NOT EXISTS `dental_clinic`
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE dental_clinic;

-- ============================================
-- 表 1：用户表（users）- 医护人员账号
-- ============================================
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '加密密码',
    `real_name` VARCHAR(50) NOT NULL COMMENT '真实姓名',
    `role` VARCHAR(20) NOT NULL DEFAULT 'doctor' COMMENT '角色：admin/doctor',
    `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ============================================
-- 表 2：患者表（patients）
-- ============================================
DROP TABLE IF EXISTS `patients`;
CREATE TABLE `patients` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `openid` VARCHAR(64) NOT NULL COMMENT '微信用户标识',
    `name` VARCHAR(50) NOT NULL COMMENT '姓名',
    `gender` VARCHAR(10) DEFAULT NULL COMMENT '性别',
    `age` INT DEFAULT NULL COMMENT '年龄',
    `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
    `id_card` VARCHAR(18) DEFAULT NULL COMMENT '身份证号',
    `medical_history` TEXT COMMENT '既往病史',
    `allergy_history` TEXT COMMENT '过敏史',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_openid` (`openid`),
    KEY `idx_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='患者表';

-- ============================================
-- 表 3：治疗记录表（treatment_records）
-- ============================================
DROP TABLE IF EXISTS `treatment_records`;
CREATE TABLE `treatment_records` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `patient_id` INT NOT NULL COMMENT '患者 ID',
    `treatment_type` VARCHAR(50) NOT NULL COMMENT '治疗类型',
    `treatment_date` DATE NOT NULL COMMENT '治疗日期',
    `tooth_position` VARCHAR(50) DEFAULT NULL COMMENT '牙位',
    `material` VARCHAR(100) DEFAULT NULL COMMENT '修复材料',
    `dentist_id` INT DEFAULT NULL COMMENT '医生 ID',
    `notes` TEXT COMMENT '治疗备注',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_patient_id` (`patient_id`),
    KEY `idx_dentist_id` (`dentist_id`),
    KEY `idx_treatment_date` (`treatment_date`),
    CONSTRAINT `fk_tr_patient` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_tr_dentist` FOREIGN KEY (`dentist_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='治疗记录表';

-- ============================================
-- 表 4：复诊计划表（appointments）
-- ============================================
DROP TABLE IF EXISTS `appointments`;
CREATE TABLE `appointments` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `patient_id` INT NOT NULL COMMENT '患者 ID',
    `appointment_date` DATETIME NOT NULL COMMENT '复诊日期',
    `appointment_type` VARCHAR(50) NOT NULL COMMENT '复诊类型',
    `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态：pending/completed/cancelled',
    `reminder_sent` TINYINT NOT NULL DEFAULT 0 COMMENT '是否已发送提醒：0/1',
    `reminder_time` DATETIME DEFAULT NULL COMMENT '提醒发送时间',
    `notes` TEXT COMMENT '复诊备注',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_patient_id` (`patient_id`),
    KEY `idx_appointment_date` (`appointment_date`),
    KEY `idx_status` (`status`),
    CONSTRAINT `fk_app_patient` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='复诊计划表';

-- ============================================
-- 表 5：对话记录表（dialogues）
-- ============================================
DROP TABLE IF EXISTS `dialogues`;
CREATE TABLE `dialogues` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `patient_id` INT NOT NULL COMMENT '患者 ID',
    `session_id` VARCHAR(64) NOT NULL COMMENT '会话 ID',
    `user_message` TEXT NOT NULL COMMENT '用户消息',
    `ai_response` TEXT NOT NULL COMMENT 'AI 回复',
    `message_type` VARCHAR(20) NOT NULL DEFAULT 'consultation' COMMENT '消息类型',
    `is_handover` TINYINT NOT NULL DEFAULT 0 COMMENT '是否人工接管：0/1',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '对话时间',
    PRIMARY KEY (`id`),
    KEY `idx_patient_id` (`patient_id`),
    KEY `idx_session_id` (`session_id`),
    KEY `idx_created_at` (`created_at`),
    CONSTRAINT `fk_dia_patient` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='对话记录表';

-- ============================================
-- 表 6：知识库表（knowledge_base）
-- ============================================
DROP TABLE IF EXISTS `knowledge_base`;
CREATE TABLE `knowledge_base` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `category` VARCHAR(50) NOT NULL COMMENT '知识分类',
    `title` VARCHAR(200) NOT NULL COMMENT '知识标题',
    `content` TEXT NOT NULL COMMENT '知识内容',
    `keywords` VARCHAR(255) DEFAULT NULL COMMENT '关键词',
    `source` VARCHAR(200) DEFAULT NULL COMMENT '来源',
    `is_active` TINYINT NOT NULL DEFAULT 1 COMMENT '是否启用：0/1',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_category` (`category`),
    KEY `idx_keywords` (`keywords`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识库表';

-- ============================================
-- 表 7：系统配置表（system_config）
-- ============================================
DROP TABLE IF EXISTS `system_config`;
CREATE TABLE `system_config` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `config_key` VARCHAR(100) NOT NULL COMMENT '配置键',
    `config_value` TEXT NOT NULL COMMENT '配置值',
    `description` VARCHAR(255) DEFAULT NULL COMMENT '配置说明',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';
