CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS idx_points_name_trgm
    ON points USING GIN (name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_terminal_points_name_trgm
    ON terminal_points USING GIN (name gin_trgm_ops);