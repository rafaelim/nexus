-- Seed script to create default users
-- Run this after creating the database schema

-- Create default user (you)
INSERT INTO users (id, email, first_name, last_name, created_at, updated_at)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'user@nexus.local',
    'User',
    'Name',
    NOW(),
    NOW()
)
ON CONFLICT (id) DO NOTHING;

-- Create sysadmin user (optional)
INSERT INTO users (id, email, first_name, last_name, created_at, updated_at)
VALUES (
    '00000000-0000-0000-0000-000000000002',
    'sysadmin@nexus.local',
    'System',
    'Administrator',
    NOW(),
    NOW()
)
ON CONFLICT (id) DO NOTHING;

