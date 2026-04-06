from app.database import DatabaseManager
from app.models.categoria import CategoryModel
from app.utils import build_placeholder_image


class MenuModel:
    SELECT_FIELDS = """
        m.id,
        m.item,
        m.valor,
        m.categoria_id,
        c.nome AS categoria_nome,
        c.ordem AS categoria_ordem,
        COALESCE(m.imagem_base64, '') AS imagem_base64
    """

    @staticmethod
    def _serialize(row):
        return dict(row)

    @staticmethod
    def _resolve_category(category_id: int | None):
        resolved_id = category_id or CategoryModel.get_default_id()
        category = CategoryModel.get(resolved_id)
        if not category:
            raise ValueError("Categoria inválida")
        return category

    @staticmethod
    def list_all():
        with DatabaseManager() as db:
            rows = db.execute_query(
                f"""
                SELECT {MenuModel.SELECT_FIELDS}
                FROM menu m
                LEFT JOIN categories c ON c.id = m.categoria_id
                ORDER BY COALESCE(c.ordem, 999), COALESCE(c.nome, 'Sem categoria'), m.item
                """
            )
            return [MenuModel._serialize(r) for r in rows]

    @staticmethod
    def get(item_id: int):
        with DatabaseManager() as db:
            rows = db.execute_query(
                f"""
                SELECT {MenuModel.SELECT_FIELDS}
                FROM menu m
                LEFT JOIN categories c ON c.id = m.categoria_id
                WHERE m.id = ?
                """,
                (item_id,),
            )
            return MenuModel._serialize(rows[0]) if rows else None

    @staticmethod
    def get_by_ids(ids: list[int]):
        if not ids:
            return []
        placeholders = ",".join(["?"] * len(ids))
        with DatabaseManager() as db:
            rows = db.execute_query(
                f"""
                SELECT {MenuModel.SELECT_FIELDS}
                FROM menu m
                LEFT JOIN categories c ON c.id = m.categoria_id
                WHERE m.id IN ({placeholders})
                ORDER BY m.id
                """,
                tuple(ids),
            )
            return [MenuModel._serialize(r) for r in rows]

    @staticmethod
    def create(item: str, valor: float, categoria_id: int | None = None, imagem_base64: str | None = None):
        category = MenuModel._resolve_category(categoria_id)
        image = imagem_base64 or build_placeholder_image(item, category["nome"])
        with DatabaseManager() as db:
            cur = db.execute_non_query(
                "INSERT INTO menu (item, valor, categoria_id, imagem_base64) VALUES (?, ?, ?, ?)",
                (item, valor, category["id"], image),
            )
            row = db.execute_query(
                f"""
                SELECT {MenuModel.SELECT_FIELDS}
                FROM menu m
                LEFT JOIN categories c ON c.id = m.categoria_id
                WHERE m.id = ?
                """,
                (cur.lastrowid,),
            )[0]
            return MenuModel._serialize(row)

    @staticmethod
    def update(item_id: int, item: str, valor: float, categoria_id: int | None = None, imagem_base64: str | None = None):
        existing = MenuModel.get(item_id)
        if not existing:
            return None

        category = MenuModel._resolve_category(categoria_id or existing.get("categoria_id"))
        image = imagem_base64 or existing.get("imagem_base64") or build_placeholder_image(item, category["nome"])

        with DatabaseManager() as db:
            db.execute_non_query(
                "UPDATE menu SET item = ?, valor = ?, categoria_id = ?, imagem_base64 = ? WHERE id = ?",
                (item, valor, category["id"], image, item_id),
            )
            row = db.execute_query(
                f"""
                SELECT {MenuModel.SELECT_FIELDS}
                FROM menu m
                LEFT JOIN categories c ON c.id = m.categoria_id
                WHERE m.id = ?
                """,
                (item_id,),
            )[0]
            return MenuModel._serialize(row)

    @staticmethod
    def delete(item_id: int):
        with DatabaseManager() as db:
            cur = db.execute_non_query("DELETE FROM menu WHERE id = ?", (item_id,))
            return cur.rowcount > 0
