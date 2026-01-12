#!/bin/bash

# Database initialization script
# This script creates the database schema and seeds default users

set -e

DB_HOST="${DB_HOST:-localhost}"
DB_USER="${DB_USER:-postgres}"
DB_NAME="${DB_NAME:-nexus}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"

echo "Initializing database: $DB_NAME"

# Set password for psql
export PGPASSWORD=$DB_PASSWORD

# Create schema
echo "Creating database schema..."
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f db/schema.sql

# Seed default users
echo "Seeding default users..."
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f db/seed.sql

echo "Database initialization complete!"
echo ""
echo "Default user ID: 00000000-0000-0000-0000-000000000001"
echo "Make sure your .env file has:"
echo "DEFAULT_USER_ID=00000000-0000-0000-0000-000000000001"

