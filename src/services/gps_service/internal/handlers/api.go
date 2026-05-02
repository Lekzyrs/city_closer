package handlers

import (
	"encoding/json"
	"gps_service/internal/auth"
	"gps_service/internal/cache"
	"gps_service/internal/db"
	"gps_service/internal/response"

	"net/http"
	"strings"

	"github.com/go-chi/chi/v5"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/rs/zerolog/log"
)

type LoginRequest struct {
	Role string `json:"role"`
}

type TokenResponse struct {
	Token string `json:"token"`
}

type CreateKioskRequest struct {
	Name        string  `json:"name"`
	Description string  `json:"description"`
	Latitude    float64 `json:"latitude"`
	Longitude   float64 `json:"longitude"`
}

type UpdateKioskRequest struct {
	Name        string  `json:"name"`
	Description string  `json:"description"`
	Latitude    float64 `json:"latitude"`
	Longitude   float64 `json:"longitude"`
}

func GetKioskByIDHandler(pool *pgxpool.Pool, kiosksCache *cache.KioskCache) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		id := chi.URLParam(r, "id")
		if strings.TrimSpace(id) == "" {
			response.WriteError(w, http.StatusBadRequest, "id is required")
			return
		}

		kiosk, err := db.GetKioskByID(r.Context(), pool, id)
		if err != nil {
			if err.Error() == "kiosk is not found" {
				response.WriteError(w, http.StatusNotFound, "kiosk not found")
				return
			}
			response.WriteError(w, http.StatusInternalServerError, "failed to get kiosk")
			return
		}

		response.WriteJSON(w, http.StatusOK, map[string]any{
			"kiosk": kiosk,
		})
	}
}

func GetKioskHandler(pool *pgxpool.Pool, kiosksCache *cache.KioskCache) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		ctx := r.Context()

		cached, err := kiosksCache.GetAll(ctx)
		if err == nil {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			_, _ = w.Write([]byte(cached))
			return
		}

		kiosks, err := db.GetKiosks(ctx, pool)
		if err != nil {
			response.WriteError(w, http.StatusInternalServerError, "failed to get kiosks")
			return
		}

		resp := map[string]any{
			"kiosks": kiosks,
		}

		data, err := json.Marshal(resp)
		if err == nil {
			_ = kiosksCache.SetAll(ctx, data)
		}

		response.WriteJSON(w, http.StatusOK, resp)
	}
}

func CreateKioskHandler(pool *pgxpool.Pool, kiosksCache *cache.KioskCache) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		defer r.Body.Close()

		var req CreateKioskRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			response.WriteError(w, http.StatusBadRequest, "invalid request body")
			return
		}

		if strings.TrimSpace(req.Name) == "" {
			response.WriteError(w, http.StatusBadRequest, "name is required")
			return
		}

		k := db.Kiosk{
			Name:        req.Name,
			Description: req.Description,
			Latitude:    req.Latitude,
			Longitude:   req.Longitude,
		}

		created, err := db.CreateKiosk(r.Context(), pool, k)
		if err != nil {
			log.Error().Err(err).Msg("failed to create kiosk")
			response.WriteError(w, http.StatusInternalServerError, "failed to create kiosk")
			return
		}

		_ = kiosksCache.InvalidateAll(r.Context())

		response.WriteJSON(w, http.StatusCreated, map[string]any{
			"kiosk": created,
		})
	}
}

func UpdateKioskHandler(pool *pgxpool.Pool, kiosksCache *cache.KioskCache) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		defer r.Body.Close()

		id := chi.URLParam(r, "id")
		if strings.TrimSpace(id) == "" {
			response.WriteError(w, http.StatusBadRequest, "id is required")
			return
		}

		var req UpdateKioskRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			response.WriteError(w, http.StatusBadRequest, "invalid request body")
			return
		}

		if strings.TrimSpace(req.Name) == "" {
			response.WriteError(w, http.StatusBadRequest, "name is required")
			return
		}

		k := db.Kiosk{
			ID:          id,
			Name:        req.Name,
			Description: req.Description,
			Latitude:    req.Latitude,
			Longitude:   req.Longitude,
		}

		err := db.UpdateKiosk(r.Context(), pool, k)
		if err != nil {
			log.Error().Err(err).Msg("failed to update kiosk")
			response.WriteError(w, http.StatusInternalServerError, "failed to update kiosk")
			return
		}

		_ = kiosksCache.InvalidateAll(r.Context())

		response.WriteJSON(w, http.StatusOK, map[string]any{
			"kiosk": "updated",
		})
	}
}

func DeleteKioskHandler(pool *pgxpool.Pool, kiosksCache *cache.KioskCache) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		id := chi.URLParam(r, "id")
		if strings.TrimSpace(id) == "" {
			response.WriteError(w, http.StatusBadRequest, "id is required")
			return
		}

		if err := db.DeleteKiosk(r.Context(), pool, id); err != nil {
			if err.Error() == "kiosk is not found" {
				response.WriteError(w, http.StatusNotFound, "kiosk not found")
				return
			}
			response.WriteError(w, http.StatusInternalServerError, "failed to delete kiosk")
			return
		}

		_ = kiosksCache.InvalidateAll(r.Context())

		response.WriteJSON(w, http.StatusOK, map[string]any{
			"message": "deleted",
		})
	}
}

func DummyLoginHandler(jwtManager *auth.JWTManager, pool *pgxpool.Pool) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req LoginRequest
		err := json.NewDecoder(r.Body).Decode(&req)
		if err != nil {
			response.WriteError(w, http.StatusBadRequest, "invalid request body")
			return
		}

		var userID string
		var email string

		switch req.Role {
		case "admin":
			userID = "11111111-1111-1111-1111-111111111111"
			email = "admin@dummy.local"
		case "user":
			userID = "22222222-2222-2222-2222-222222222222"
			email = "user@dummy.local"
		default:
			response.WriteError(w, http.StatusBadRequest, "invalid role")
			return
		}

		err = db.EnsureUserExists(r.Context(), userID, email, req.Role, pool)
		if err != nil {
			response.WriteError(w, http.StatusInternalServerError, "failed to ensure dummy user")
			return
		}

		token, err := jwtManager.GenerateAccessToken(userID, email, req.Role)
		if err != nil {
			response.WriteError(w, http.StatusInternalServerError, "failed to generate token")
			return
		}

		response.WriteJSON(w, http.StatusOK, TokenResponse{
			Token: token,
		})
	}
}

func PingDbHandler(pool *pgxpool.Pool) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		err := pool.Ping(r.Context())
		if err != nil {
			log.Error().Err(err).Msg("problems with pinging")
			response.WriteError(w, http.StatusInternalServerError, "database ping failed")
			return
		}
		response.WriteJSON(w, http.StatusOK, map[string]string{"status": "ok"})
	}

}
