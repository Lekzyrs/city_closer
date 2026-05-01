package router

import (
	"gps_service/internal/auth"
	"gps_service/internal/cache"
	"gps_service/internal/handlers"

	"github.com/go-chi/chi/v5"
	chimw "github.com/go-chi/chi/v5/middleware"
	"github.com/jackc/pgx/v5/pgxpool"
)

func NewRouter(
	jm *auth.JWTManager,
	pool *pgxpool.Pool,
	pointsCache *cache.PointsCache,
	kiosksCache *cache.KioskCache,
) chi.Router {
	r := chi.NewRouter()

	r.Use(chimw.Logger)
	r.Use(chimw.Recoverer)

	r.Route("/api/v1", func(r chi.Router) {
		r.Post("/auth/login", handlers.DummyLoginHandler(jm, pool))

		// public
		r.Get("/points", handlers.GetPointsHandler(pool, pointsCache))
		r.Get("/kiosks", handlers.GetKioskHandler(pool, kiosksCache))
		r.Get("/kiosks/{id}", handlers.GetKioskByIDHandler(pool, kiosksCache))

		// admin only
		r.Group(func(r chi.Router) {
			r.Use(auth.AuthMiddleware(jm))
			r.Use(auth.RequireRole("admin"))

			r.Post("/points", handlers.CreatePointHandler(pool, pointsCache))
			r.Put("/points/{id}", handlers.UpdatePointHandler(pool, pointsCache))
			r.Delete("/points/{id}", handlers.DeletePointHandler(pool, pointsCache))

			r.Post("/kiosks", handlers.CreateKioskHandler(pool, kiosksCache))
			r.Put("/kiosks/{id}", handlers.UpdateKioskHandler(pool, kiosksCache))
			r.Delete("/kiosks/{id}", handlers.DeleteKioskHandler(pool, kiosksCache))
		})
	})

	return r
}
