-- ============================================
-- 初始化测试数据
-- 数据库：dental_clinic
-- 执行日期：2026-02-22
-- 版本：v1.3（修复 bcrypt 密码哈希）
-- ============================================

USE dental_clinic;

-- ============================================
-- 1. 插入用户数据（医护人员）
-- 密码均为：admin123
-- ============================================
DELETE FROM users WHERE username IN ('admin', 'doctor_zhang', 'doctor_li');

INSERT INTO users (username, password_hash, real_name, role, phone) VALUES
('admin', '$2b$12$rSU6DROyKvuBIs0v3RmUU.rtAsCOsyjUef1WnvmOrgdZu74JAVF9y', '系统管理员', 'admin', '13800138000'),
('doctor_zhang', '$2b$12$rSU6DROyKvuBIs0v3RmUU.rtAsCOsyjUef1WnvmOrgdZu74JAVF9y', '张医生', 'doctor', '13800138001'),
('doctor_li', '$2b$12$rSU6DROyKvuBIs0v3RmUU.rtAsCOsyjUef1WnvmOrgdZu74JAVF9y', '李医生', 'doctor', '13800138002');

-- ============================================
-- 2. 插入患者数据
-- ============================================
DELETE FROM patients;

INSERT INTO patients (openid, name, gender, age, phone, medical_history, allergy_history) VALUES
('oAbCdEfGhIjKlMnOpQrStUvWx', '张三', '男', 45, '13900139001', '高血压', '无'),
('oAbCdEfGhIjKlMnOpQrStUvWy', '李四', '女', 38, '13900139002', '无', '青霉素过敏'),
('oAbCdEfGhIjKlMnOpQrStUvWz', '王五', '男', 52, '13900139003', '糖尿病', '无'),
('oAbCdEfGhIjKlMnOpQrStUvW0', '赵六', '女', 29, '13900139004', '无', '无'),
('oAbCdEfGhIjKlMnOpQrStUvW1', '孙七', '男', 61, '13900139005', '高血压、冠心病', '磺胺类过敏');

-- ============================================
-- 3. 插入治疗记录数据
-- ============================================
DELETE FROM treatment_records;

INSERT INTO treatment_records (patient_id, treatment_type, treatment_date, tooth_position, material, dentist_id, notes) VALUES
(1, '固定义齿修复', '2026-01-15', '左上 6', '全瓷牙', 2, '患者恢复良好'),
(1, '种植牙手术', '2026-02-10', '右下 6', 'ITI 种植体', 2, '手术顺利'),
(2, '活动义齿修复', '2026-01-20', '上颌', '钴铬合金', 3, '初戴适应中'),
(3, '固定义齿修复', '2026-02-05', '左下 6、7', '烤瓷牙', 2, '已完成'),
(4, '种植牙手术', '2026-02-18', '左上 4', '奥齿泰种植体', 3, '术后恢复中'),
(5, '活动义齿修复', '2026-01-10', '下颌', '纯钛支架', 2, '定期复查');

-- ============================================
-- 4. 插入复诊计划数据
-- ============================================
DELETE FROM appointments;

INSERT INTO appointments (patient_id, appointment_date, appointment_type, status, notes) VALUES
(1, '2026-03-15 09:00:00', '种植牙复查', 'pending', '检查骨结合情况'),
(1, '2026-05-15 09:00:00', '固定义齿复查', 'pending', '戴牙后复查'),
(2, '2026-03-01 14:00:00', '活动义齿调整', 'pending', '初戴后调整'),
(3, '2026-03-10 10:00:00', '固定义齿复查', 'pending', '戴牙后复查'),
(4, '2026-03-20 09:00:00', '种植牙二期', 'pending', '安装愈合基台'),
(5, '2026-02-28 15:00:00', '活动义齿复查', 'pending', '适应性检查');

-- ============================================
-- 5. 插入对话记录数据（示例）
-- ============================================
DELETE FROM dialogues;

INSERT INTO dialogues (patient_id, session_id, user_message, ai_response, message_type) VALUES
(1, 'sess_001', '医生，我种植牙多久能正常吃饭？', '一般种植牙术后 2-3 个月可以正常咀嚼食物。但具体情况因人而异，建议您术后 1 周内吃软食，1 个月内避免用手术侧咀嚼硬物。请按时复诊，医生会根据您的恢复情况给出具体建议。', 'consultation'),
(2, 'sess_002', '活动义齿刚戴上很不舒服，正常吗？', '活动义齿初戴时有轻微不适是正常的，一般需要 1-2 周适应期。如果出现明显疼痛、溃疡或无法咀嚼，请及时复诊调整。建议您先吃软食，逐渐适应后再恢复正常饮食。', 'consultation'),
(3, 'sess_003', '烤瓷牙能用多久？', '烤瓷牙的使用寿命一般为 10-15 年，良好的口腔卫生和定期复查可以延长使用寿命。建议您每天认真刷牙、使用牙线，每半年到一年复查一次。', 'consultation');

-- ============================================
-- 6. 插入知识库数据（示例）
-- ============================================
DELETE FROM knowledge_base;

INSERT INTO knowledge_base (category, title, content, keywords, source) VALUES
('术后护理', '种植牙术后注意事项', '1. 术后 24 小时内不要刷牙，可用漱口水漱口\n2. 术后 1-2 天内避免剧烈运动\n3. 术后 1 周内避免用手术侧咀嚼食物\n4. 按医嘱服用抗生素和止痛药\n5. 如有持续出血、剧烈疼痛或发热，请及时就医\n6. 按时复诊，一般术后 7 天拆线，3-6 个月进行二期手术', '种植牙，术后护理，注意事项', '口腔修复学第 8 版'),
('术后护理', '固定义齿佩戴注意事项', '1. 初戴固定义齿时，如有轻微不适属正常现象\n2. 避免咬硬物，如冰块、坚果壳等\n3. 保持良好的口腔卫生，每天刷牙 2 次\n4. 使用牙线清洁义齿与真牙之间的缝隙\n5. 定期复查，一般每 6-12 个月复查一次\n6. 如出现松动、疼痛或破损，请及时就医', '固定义齿，注意事项，护理', '口腔修复学第 8 版'),
('术后护理', '活动义齿使用指南', '1. 初戴活动义齿时，可能有异物感，一般 1-2 周可适应\n2. 饭后应取下义齿清洗，并漱口\n3. 睡前取下义齿，浸泡在清水中\n4. 避免用热水清洗义齿，以免变形\n5. 定期复查，一般每 6 个月复查一次\n6. 如义齿破损或不适，请及时就医调整', '活动义齿，使用指南，护理', '口腔修复学第 8 版'),
('常见问题', '种植牙的寿命有多长？', '种植牙的平均寿命为 10-20 年，甚至更长。影响种植牙寿命的因素包括：\n1. 患者的口腔卫生习惯\n2. 定期复查和维护\n3. 吸烟、饮酒等不良习惯\n4. 全身健康状况（如糖尿病等）\n5. 种植体的品牌和质量', '种植牙，寿命，使用年限', '临床指南'),
('常见问题', '什么情况下需要做牙冠修复？', '以下情况建议做牙冠修复：\n1. 牙齿大面积缺损，无法用充填材料修复\n2. 根管治疗后的牙齿，需要保护\n3. 牙齿颜色或形态异常，影响美观\n4. 作为固定义齿的基牙\n5. 种植牙上部修复', '牙冠，适应症，修复', '口腔修复学第 8 版');

-- ============================================
-- 7. 插入系统配置数据
-- ============================================
DELETE FROM system_config;

INSERT INTO system_config (config_key, config_value, description) VALUES
('reminder_time', '09:00', '每日复诊提醒发送时间'),
('reminder_advance_hours', '24', '提前多少小时发送提醒'),
('ai_max_tokens', '512', 'AI 回复最大 token 数'),
('ai_temperature', '0.7', 'AI 生成温度参数'),
('session_timeout_minutes', '30', '会话超时时间（分钟）');

-- ============================================
-- 验证数据
-- ============================================
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM users
UNION ALL
SELECT 'patients', COUNT(*) FROM patients
UNION ALL
SELECT 'treatment_records', COUNT(*) FROM treatment_records
UNION ALL
SELECT 'appointments', COUNT(*) FROM appointments
UNION ALL
SELECT 'dialogues', COUNT(*) FROM dialogues
UNION ALL
SELECT 'knowledge_base', COUNT(*) FROM knowledge_base
UNION ALL
SELECT 'system_config', COUNT(*) FROM system_config;
