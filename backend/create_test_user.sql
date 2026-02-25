-- ============================================
-- 创建测试用户
-- ============================================

USE dental_clinic;

-- 创建管理员用户（密码：admin123）
-- 使用 bcrypt 加密
DELETE FROM users WHERE username IN ('admin', 'test');

INSERT INTO `users` (`username`, `password_hash`, `real_name`, `role`, `phone`) VALUES
('admin', '$2b$12$KIXjFq3lqQM4xQz7Z8Z9ZuTqVqJqJqJqJqJqJqJqJqJqJqJqJqJqJ', '系统管理员', 'admin', '13800138000'),
('test', '$2b$12$KIXjFq3lqQM4xQz7Z8Z9ZuTqVqJqJqJqJqJqJqJqJqJqJqJqJqJqJ', '测试用户', 'doctor', '13800138001');

-- 验证用户是否创建成功
SELECT id, username, real_name, role FROM users;
