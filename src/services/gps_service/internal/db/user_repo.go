package db

import (
	"context"
	"errors"
	"gps_service/internal/models"

	"github.com/jackc/pgx"
	"github.com/jackc/pgx/v5/pgxpool"
)

/*
CREATE TABLE users (

	user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	email VARCHAR(255) NOT NULL UNIQUE,
	password_hash TEXT NOT NULL,
	role VARCHAR(50) NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'user')),
	created_at TIMESTAMPTZ NOT NULL DEFAULT now()

);
*/

type PostgresUserRepo struct {
	pool *pgxpool.Pool
}

func NewPostgresUserRepo(pool *pgxpool.Pool) *PostgresUserRepo {
	return &PostgresUserRepo{pool: pool}
}

func (r *PostgresUserRepo) GetByEmail(ctx context.Context, email string) (*models.User, error) {
	user := &models.User{}

	err := r.pool.QueryRow(ctx, `
		SELECT user_id, email, password_hash, role, created_at
		FROM users
		WHERE email = $1
	`, email).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.Role,
		&user.CreatedAt,
	)

	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			return nil, errors.New("user not found")
		}
		return nil, err
	}

	return user, nil
}

func (r *PostgresUserRepo) GetByID(ctx context.Context, id string) (*models.User, error) {
	user := &models.User{}

	err := r.pool.QueryRow(ctx, `
		SELECT user_id, email, password_hash, role, created_at
		FROM users
		WHERE user_id = $1
	`, id).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.Role,
		&user.CreatedAt,
	)

	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			return nil, errors.New("user not found")
		}
		return nil, err
	}

	return user, nil
}

func (r *PostgresUserRepo) Create(ctx context.Context, email, passwordHash, role string) (*models.User, error) {
	user := &models.User{}
	err := r.pool.QueryRow(ctx, `
		INSERT INTO users (email, password_hash, role)
		VALUES ($1, $2, $3)
		RETURNING user_id, email, password_hash, role, created_at
	`, email, passwordHash, role).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.Role,
		&user.CreatedAt,
	)
	if err != nil {
		return nil, err
	}
	return user, nil
}
