-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Finance categories table
CREATE TYPE category_type AS ENUM ('income', 'expense');

CREATE TABLE IF NOT EXISTS finance_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type category_type NOT NULL,
    color VARCHAR(7),
    deleted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, name)
);

-- Expenses table
CREATE TYPE expense_type AS ENUM ('ongoing', 'installment');

CREATE TABLE IF NOT EXISTS expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE RESTRICT,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2),
    category_id UUID NOT NULL REFERENCES finance_categories(id) ON DELETE RESTRICT,
    day_of_month INTEGER NOT NULL CHECK (day_of_month >= 1 AND day_of_month <= 31),
    expense_type expense_type NOT NULL,
    start_date DATE NOT NULL,
    total_payments INTEGER,
    payments_completed INTEGER DEFAULT 0 NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    notes TEXT,
    deleted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Finance transactions table
CREATE TABLE IF NOT EXISTS finance_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE RESTRICT,
    date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    category_id UUID NOT NULL REFERENCES finance_categories(id) ON DELETE RESTRICT,
    expense_id UUID REFERENCES expenses(id) ON DELETE SET NULL,
    tags JSONB,
    payment_method VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Properties table (system-wide, not user-scoped)
CREATE TABLE IF NOT EXISTS properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_default BOOLEAN DEFAULT FALSE NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notes table (monthly and yearly)
CREATE TABLE IF NOT EXISTS notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    domain VARCHAR(50) NOT NULL DEFAULT 'finance',
    year INTEGER NOT NULL,
    month INTEGER CHECK (month IS NULL OR (month >= 1 AND month <= 12)),
    notes TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Partial unique indexes for monthly and yearly notes
-- Monthly notes: unique on (user_id, domain, year, month) where month IS NOT NULL
CREATE UNIQUE INDEX IF NOT EXISTS uq_notes_user_domain_year_month 
    ON notes(user_id, domain, year, month) 
    WHERE month IS NOT NULL;

-- Yearly notes: unique on (user_id, domain, year) where month IS NULL
CREATE UNIQUE INDEX IF NOT EXISTS uq_notes_user_domain_year_yearly 
    ON notes(user_id, domain, year) 
    WHERE month IS NULL;

-- Partial unique index for default property (only one can be default system-wide)
CREATE UNIQUE INDEX IF NOT EXISTS uq_properties_is_default 
    ON properties(is_default) 
    WHERE is_default = TRUE AND deleted_at IS NULL;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_finance_transactions_user_id ON finance_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_finance_transactions_date ON finance_transactions(date);
CREATE INDEX IF NOT EXISTS idx_finance_transactions_category_id ON finance_transactions(category_id);
CREATE INDEX IF NOT EXISTS idx_finance_transactions_expense_id ON finance_transactions(expense_id);
CREATE INDEX IF NOT EXISTS idx_finance_transactions_property_id ON finance_transactions(property_id);
CREATE INDEX IF NOT EXISTS idx_finance_categories_user_id ON finance_categories(user_id);
CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id);
CREATE INDEX IF NOT EXISTS idx_expenses_category_id ON expenses(category_id);
CREATE INDEX IF NOT EXISTS idx_expenses_property_id ON expenses(property_id);
CREATE INDEX IF NOT EXISTS idx_notes_user_id ON notes(user_id);
CREATE INDEX IF NOT EXISTS idx_notes_domain_year_month ON notes(domain, year, month);

