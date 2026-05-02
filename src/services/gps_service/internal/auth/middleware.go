package auth

import (
	"gps_service/internal/response"
	"net/http"
	"strings"
)

func AuthMiddleware(JWTManager *JWTManager) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			authHeader := r.Header.Get("Authorization")
			if authHeader == "" {
				response.WriteError(w, http.StatusUnauthorized, "invalid authorization header")
				return
			}
			parts := strings.SplitN(authHeader, " ", 2)
			if len(parts) != 2 || strings.ToLower(parts[0]) != "bearer" {
				response.WriteError(w, http.StatusUnauthorized, "invalid authorization header")
				return
			}

			tokenString := parts[1]
			if tokenString == "" {
				response.WriteError(w, http.StatusUnauthorized, "missing token")
				return
			}
			claims, err := JWTManager.VerifyAccessToken(tokenString)
			if err != nil {
				if strings.Contains(err.Error(), "expired") {
					response.WriteError(w, http.StatusUnauthorized, "token expired")
					return
				}
				response.WriteError(w, http.StatusUnauthorized, "invalid token")
				return
			}
			ctx := WithUser(r.Context(), claims)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

func RequireRole(role string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			user, ok := GetUserFromContext(r.Context())
			if !ok {
				response.WriteError(w, http.StatusUnauthorized, "unauthorized")
				return
			}

			if user.Role != role {
				response.WriteError(w, http.StatusForbidden, "forbidden")
				return
			}

			next.ServeHTTP(w, r)
		})
	}
}
