from fastapi import FastAPI, HTTPException
from database import get_connection

app = FastAPI(title="API GET de Catálogo de Videojuegos")


@app.get("/")
def root():
    return {
        "mensaje": "API GET de Catálogo de Videojuegos activa",
        "endpoints": [
            "/games",
            "/games/{id}",
            "/games/genre/{genre}",
            "/developers",
            "/developers/{id}",
        ],
    }


@app.get("/games")
def get_games():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT g.id, g.title, g.genre, g.price::float AS price,
                       g.release_year, g.developer_id, d.name AS developer_name
                FROM games g
                INNER JOIN developers d ON g.developer_id = d.id
                ORDER BY g.id ASC;
            """)
            return cur.fetchall()
    finally:
        conn.close()


@app.get("/games/genre/{genre}")
def get_games_by_genre(genre: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT g.id, g.title, g.genre, g.price::float AS price,
                       g.release_year, g.developer_id, d.name AS developer_name
                FROM games g
                INNER JOIN developers d ON g.developer_id = d.id
                WHERE g.genre ILIKE %s
                ORDER BY g.id ASC;
            """, (genre,))
            rows = cur.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail=f"No hay juegos del género '{genre}'.")
            return rows
    finally:
        conn.close()


@app.get("/games/{game_id}")
def get_game_by_id(game_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT g.id, g.title, g.genre, g.price::float AS price,
                       g.release_year, g.developer_id, d.name AS developer_name
                FROM games g
                INNER JOIN developers d ON g.developer_id = d.id
                WHERE g.id = %s;
            """, (game_id,))
            game = cur.fetchone()
            if not game:
                raise HTTPException(status_code=404, detail="Videojuego no encontrado.")
            return game
    finally:
        conn.close()


@app.get("/developers")
def get_developers():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, country, foundation_year FROM developers ORDER BY id ASC;")
            return cur.fetchall()
    finally:
        conn.close()


@app.get("/developers/{developer_id}")
def get_developer_by_id(developer_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, country, foundation_year FROM developers WHERE id = %s;", (developer_id,))
            dev = cur.fetchone()
            if not dev:
                raise HTTPException(status_code=404, detail="Desarrollador no encontrado.")
            return dev
    finally:
        conn.close()