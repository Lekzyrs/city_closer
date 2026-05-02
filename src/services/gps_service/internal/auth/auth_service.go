package auth

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"gps_service/internal/models"
	"time"

	"golang.org/x/crypto/bcrypt"
)

type TokenRepository interface {
	Save(ctx context.Context, tokenHash, userID string, expiresAt time.Time) error
	Get(ctx context.Context, tokenHash string) (*models.RefreshToken, error)
	Delete(ctx context.Context, tokenHash string) error
}

type UserRepository interface {
	GetByEmail(ctx context.Context, email string) (*models.User, error)
	GetByID(ctx context.Context, id string) (*models.User, error)
	Create(ctx context.Context, email, passwordHash, role string) (*models.User, error)
}

type AuthService struct {
	jwtManager *JWTManager
	userRepo   UserRepository
	tokenRepo  TokenRepository
}

func NewAuthService(jwt *JWTManager, userRepo UserRepository, tokenRepo TokenRepository) *AuthService {
	return &AuthService{
		jwtManager: jwt,
		userRepo:   userRepo,
		tokenRepo:  tokenRepo,
	}
}

func (s *AuthService) RefreshToken(ctx context.Context, refreshToken string) (string, string, error) {

	hashBytes := sha256.Sum256([]byte(refreshToken))
	hash := hex.EncodeToString(hashBytes[:])

	token, err := s.tokenRepo.Get(ctx, hash)
	if err != nil {
		return "", "", errors.New("invalid token")
	}

	if token.ExpiresAt.Before(time.Now()) {
		return "", "", errors.New("expired token")
	}

	user, err := s.userRepo.GetByID(ctx, token.UserID)
	if err != nil {
		return "", "", errors.New("invalid token")
	}

	accessToken, err := s.jwtManager.GenerateAccessToken(user.ID, user.Email, user.Role)
	if err != nil {
		return "", "", err
	}

	newRefreshToken, newHash, err := s.jwtManager.GenerateRefreshToken()
	if err != nil {
		return "", "", err
	}

	if err := s.tokenRepo.Delete(ctx, hash); err != nil {
		return "", "", err
	}

	if err := s.tokenRepo.Save(ctx, newHash, user.ID, time.Now().Add(7*24*time.Hour)); err != nil {
		return "", "", err
	}

	return accessToken, newRefreshToken, nil
}

func (s *AuthService) Login(ctx context.Context, email, password string) (string, string, error) {
	user, err := s.userRepo.GetByEmail(ctx, email)
	if err != nil {
		return "", "", errors.New("invalid credentials")
	}

	err = bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(password))
	if err != nil {
		return "", "", errors.New("invalid credentials")
	}

	accessToken, err := s.jwtManager.GenerateAccessToken(user.ID, user.Email, user.Role)
	if err != nil {
		return "", "", err
	}

	refreshToken, refreshHash, err := s.jwtManager.GenerateRefreshToken()
	if err != nil {
		return "", "", err
	}
	err = s.tokenRepo.Save(ctx, refreshHash, user.ID, time.Now().Add(7*24*time.Hour))
	if err != nil {
		return "", "", err
	}
	return accessToken, refreshToken, nil
}

func (s *AuthService) Register(ctx context.Context, email, password string) (*models.User, string, string, error) {
	existing, _ := s.userRepo.GetByEmail(ctx, email)
	if existing != nil {
		return nil, "", "", errors.New("user already exists")
	}

	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, "", "", err
	}

	user, err := s.userRepo.Create(ctx, email, string(hash), "user")
	if err != nil {
		return nil, "", "", err
	}

	accessToken, err := s.jwtManager.GenerateAccessToken(user.ID, user.Email, user.Role)
	if err != nil {
		return nil, "", "", err
	}

	refreshToken, refreshHash, err := s.jwtManager.GenerateRefreshToken()
	if err != nil {
		return nil, "", "", err
	}

	err = s.tokenRepo.Save(ctx, refreshHash, user.ID, time.Now().Add(7*24*time.Hour))
	if err != nil {
		return nil, "", "", err
	}

	return user, accessToken, refreshToken, nil
}
