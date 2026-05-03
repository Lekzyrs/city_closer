package auth

import (
	"encoding/json"
	"gps_service/internal/response"
	"mime"
	"net/http"
	"time"
)

type LoginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type LoginResponse struct {
	AccessToken string `json:"access_token"`
}

func RefreshHandler(authService *AuthService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {

		cookie, err := r.Cookie("refresh_token")
		if err != nil {
			response.WriteError(w, http.StatusUnauthorized, "missing refresh token")
			return
		}

		accessToken, newRefreshToken, err := authService.RefreshToken(r.Context(), cookie.Value)
		if err != nil {
			response.WriteError(w, http.StatusUnauthorized, "invalid refresh token")
			return
		}

		http.SetCookie(w, &http.Cookie{
			Name:     "refresh_token",
			Value:    newRefreshToken,
			HttpOnly: true,
			Secure:   true,
			SameSite: http.SameSiteStrictMode,
			Path:     "/api/v1/auth/refresh",
			Expires:  time.Now().Add(7 * 24 * time.Hour),
		})

		json.NewEncoder(w).Encode(map[string]string{
			"access_token": accessToken,
		})
	}
}

func LoginHandler(authService *AuthService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req LoginRequest

		mediaType, _, _ := mime.ParseMediaType(r.Header.Get("Content-Type"))
		if mediaType != "application/json" {
			response.WriteError(w, http.StatusUnsupportedMediaType, "content type must be application/json")
			return
		}
		err := json.NewDecoder(r.Body).Decode(&req)
		if err != nil {
			response.WriteError(w, http.StatusBadRequest, "invalid request body")
			return
		}
		if req.Email == "" || req.Password == "" {
			response.WriteError(w, http.StatusBadRequest, "email and password required")
			return
		}

		accessToken, refreshToken, err := authService.Login(r.Context(), req.Email, req.Password)
		if err != nil {
			response.WriteError(w, http.StatusUnauthorized, "invalid credentials")
			return
		}

		http.SetCookie(w, &http.Cookie{
			Name:     "refresh_token",
			Value:    refreshToken,
			HttpOnly: true,
			Secure:   true,
			SameSite: http.SameSiteStrictMode,
			Path:     "/api/v1/auth/refresh",
			Expires:  time.Now().Add(7 * 24 * time.Hour),
		})
		w.Header().Set("Content-Type", "application/json")

		json.NewEncoder(w).Encode(LoginResponse{
			AccessToken: accessToken,
		})

	}
}

type RegisterRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

func RegisterHandler(authService *AuthService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		mediaType, _, _ := mime.ParseMediaType(r.Header.Get("Content-Type"))
		if mediaType != "application/json" {
			response.WriteError(w, http.StatusUnsupportedMediaType, "content type must be application/json")
			return
		}

		var req RegisterRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			response.WriteError(w, http.StatusBadRequest, "invalid request body")
			return
		}
		if req.Email == "" || req.Password == "" {
			response.WriteError(w, http.StatusBadRequest, "email and password required")
			return
		}
		if len(req.Password) < 6 {
			response.WriteError(w, http.StatusBadRequest, "password must be at least 6 characters")
			return
		}

		user, accessToken, refreshToken, err := authService.Register(r.Context(), req.Email, req.Password)
		if err != nil {
			if err.Error() == "user already exists" {
				response.WriteError(w, http.StatusConflict, "user already exists")
				return
			}
			response.WriteError(w, http.StatusInternalServerError, "registration failed")
			return
		}

		http.SetCookie(w, &http.Cookie{
			Name:     "refresh_token",
			Value:    refreshToken,
			HttpOnly: true,
			Secure:   true,
			SameSite: http.SameSiteStrictMode,
			Path:     "/api/v1/auth/refresh",
			Expires:  time.Now().Add(7 * 24 * time.Hour),
		})

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(map[string]interface{}{
			"user":         user,
			"access_token": accessToken,
		})
	}
}
