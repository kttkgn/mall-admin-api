-- 删除已存在的管理员用户
DELETE FROM users WHERE username = 'admin';

-- 创建管理员用户
INSERT INTO users (
    username,
    email,
    hashed_password,
    full_name,
    role,
    status,
    is_active,
    is_superuser,
    created_at,
    updated_at
) VALUES (
    'admin',
    'admin@example.com',
    '$2b$12$u/diFzjg8kUYNR4KlDidzOfN3BGViFfVS1bz.nxysY8kOCMn6jvpG',
    'Administrator',
    'admin',
    1,
    1,
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
); 