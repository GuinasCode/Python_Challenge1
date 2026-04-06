from app.database import DatabaseManager


class MenuModel:
    @staticmethod
    def list_all():
        with DatabaseManager() as db:
            rows = db.execute_query("SELECT id, item, valor FROM menu ORDER BY id")
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_ids(ids: list[int]):
        if not ids:
            return []
        placeholders = ",".join(["?"] * len(ids))
        with DatabaseManager() as db:
            rows = db.execute_query(f"SELECT id, item, valor FROM menu WHERE id IN ({placeholders}) ORDER BY id", tuple(ids))
            return [dict(r) for r in rows]

    @staticmethod
    def create(item: str, valor: float):
        with DatabaseManager() as db:
            cur = db.execute_non_query("INSERT INTO menu (item, valor) VALUES (?, ?)", (item, valor))
            new_id = cur.lastrowid
            row = db.execute_query("SELECT id, item, valor FROM menu WHERE id = ?", (new_id,))[0]
            return dict(row)

    @staticmethod
    def update(item_id: int, item: str, valor: float):
        with DatabaseManager() as db:
            cur = db.execute_non_query("UPDATE menu SET item = ?, valor = ? WHERE id = ?", (item, valor, item_id))
            if cur.rowcount == 0:
                return None
            row = db.execute_query("SELECT id, item, valor FROM menu WHERE id = ?", (item_id,))[0]
            return dict(row)

    @staticmethod
    def delete(item_id: int):
        with DatabaseManager() as db:
            cur = db.execute_non_query("DELETE FROM menu WHERE id = ?", (item_id,))
            return cur.rowcount > 0
