package handlers

import (
	"gps_service/internal/db"
	"gps_service/internal/response"
	"net/http"

	"github.com/jackc/pgx/v5/pgxpool"
)

func SearchHandler(pool *pgxpool.Pool) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		q := r.URL.Query().Get("q")
		if q == "" {
			response.WriteError(w, http.StatusBadRequest, "missing q parameter")
			return
		}

		results, err := db.Search(r.Context(), pool, q)
		if err != nil {
			response.WriteError(w, http.StatusInternalServerError, "problems with search")
			return
		}

		response.WriteJSON(w, http.StatusOK, results)
	}
}
