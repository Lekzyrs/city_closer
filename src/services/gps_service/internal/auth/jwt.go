package auth

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"time"

	"errors"

	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
)

type JWTManager struct {
	SecretKey    []byte
	AccessExpiry time.Duration
}

func NewJWTManager(secret string, accessExpiry time.Duration) *JWTManager {
	return &JWTManager{
		SecretKey:    []byte(secret),
		AccessExpiry: accessExpiry,
	}
}

func (jw *JWTManager) GenerateAccessToken(userID, email, role string) (string, error) {
	now := time.Now()
	claim := &Claims{
		UserID: userID,
		Email:  email,
		Role:   role,
		RegisteredClaims: jwt.RegisteredClaims{
			ID:        uuid.NewString(),
			Issuer:    "city_closer",
			Subject:   userID,
			Audience:  []string{"user"},
			IssuedAt:  jwt.NewNumericDate(now),
			ExpiresAt: jwt.NewNumericDate(now.Add(jw.AccessExpiry)),
		},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claim)
	tokenstring, err := token.SignedString(jw.SecretKey)
	if err != nil {
		return "", err
	}
	return tokenstring, nil
}

func (jw *JWTManager) GenerateRefreshToken() (string, string, error) {
	b := make([]byte, 32)

	_, err := rand.Read(b)
	if err != nil {
		return "", "", err
	}

	token := hex.EncodeToString(b)

	hash := sha256.Sum256([]byte(token))

	return token, hex.EncodeToString(hash[:]), nil
}

func (jw *JWTManager) VerifyAccessToken(tokenStr string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(tokenStr, &Claims{}, func(token *jwt.Token) (interface{}, error) {

		if token.Method != jwt.SigningMethodHS256 {
			return nil, fmt.Errorf("unexpected signing method")
		}

		return jw.SecretKey, nil
	})

	if err != nil {
		return nil, err
	}

	claims, ok := token.Claims.(*Claims)
	if !ok || !token.Valid {
		return nil, errors.New("invalid token")
	}
	if claims.Issuer != "city_closer" {
		return nil, fmt.Errorf("invalid issuer")
	}
	if claims.Subject == "" {
		return nil, fmt.Errorf("invalid subject")
	}

	return claims, nil
}

/*
func (jm *JWTManager) GenerateToken(userID, role string) (string, error) {
	now := time.Now()
	claim := &Claims{
		UserID: userID,
		Role:   role,
		RegisteredClaims: jwt.RegisteredClaims{
			IssuedAt:  jwt.NewNumericDate(now),
			ExpiresAt: jwt.NewNumericDate(now.Add(120 * time.Hour)),
		},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claim)
	tokenString, err := token.SignedString([]byte(jm.secretKey))
	if err != nil {
		return "", err
	}
	return tokenString, nil
}

func (jm *JWTManager) ParseToken(tokenString string) (*Claims, error) {
	claims := &Claims{}
	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (any, error) {
		_, ok := token.Method.(*jwt.SigningMethodHMAC)
		if !ok {
			return nil, jwt.ErrSignatureInvalid
		}
		return []byte(jm.secretKey), nil
	})
	if err != nil {
		return nil, err
	}
	if !token.Valid {
		return nil, jwt.ErrSignatureInvalid
	}
	return claims, nil

}
*/
