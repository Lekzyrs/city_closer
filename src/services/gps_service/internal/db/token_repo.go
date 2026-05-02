package db

import (
	"context"
	"errors"
	"gps_service/internal/models"
	"time"

	"github.com/jackc/pgx"
	"github.com/jackc/pgx/v5/pgxpool"
)

type PostgresTokenRepo struct {
	pool *pgxpool.Pool
}

func NewPostgresTokenRepo(pool *pgxpool.Pool) *PostgresTokenRepo {
	return &PostgresTokenRepo{pool: pool}
}

func (r *PostgresTokenRepo) Delete(ctx context.Context, tokenHash string) error {
	_, err := r.pool.Exec(ctx, `
		DELETE FROM refresh_tokens
		WHERE token_hash = $1
	`, tokenHash)
	return err
}

func (r *PostgresTokenRepo) Save(ctx context.Context, tokenHash, userID string, expiresAt time.Time) error {
	_, err := r.pool.Exec(ctx, `
		INSERT INTO refresh_tokens (id, token_hash, user_id, expires_at, created_at)
		VALUES (gen_random_uuid(), $1, $2, $3, NOW())
	`, tokenHash, userID, expiresAt)

	return err
}

func (r *PostgresTokenRepo) Get(ctx context.Context, tokenHash string) (*models.RefreshToken, error) {
	token := &models.RefreshToken{}

	err := r.pool.QueryRow(ctx, `
		SELECT token_hash, user_id, expires_at, created_at
		FROM refresh_tokens
		WHERE token_hash = $1
	`, tokenHash).Scan(
		&token.TokenHash,
		&token.UserID,
		&token.ExpiresAt,
		&token.CreatedAt,
	)

	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			return nil, errors.New("not found")
		}
		return nil, err
	}

	return token, nil
}
