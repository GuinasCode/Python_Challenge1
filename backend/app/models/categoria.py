import sqlite3

from app.database import DatabaseManager
from app.utils import CATEGORY_PRESETS, category_order


class CategoryModel:
    @staticmethod
    def list_all():
        with DatabaseManager() as db:
            rows = db.execute_query(
                """
                SELECT c.id, c.nome, c.ordem, COUNT(m.id) AS total_itens
                FROM categories c
                LEFT JOIN menu m ON m.categoria_id = c.id
                GROUP BY c.id, c.nome, c.ordem
                ORDER BY c.ordem, c.nome
                """
            )
            return [dict(row) for row in rows]

    @staticmethod
    def get(category_id: int):
        with DatabaseManager() as db:
            rows = db.execute_query(
                "SELECT id, nome, ordem FROM categories WHERE id = ?",
                (category_id,),
            )
            return dict(rows[0]) if rows else None

    @staticmethod
    def get_by_name(nome: str):
        with DatabaseManager() as db:
            rows = db.execute_query(
                "SELECT id, nome, ordem FROM categories WHERE nome = ?",
                (nome,),
            )
            return dict(rows[0]) if rows else None

    @staticmethod
    def ensure_defaults():
        with DatabaseManager() as db:
            for nome, preset in CATEGORY_PRESETS.items():
                db.execute_non_query(
                    "INSERT OR IGNORE INTO categories (nome, ordem) VALUES (?, ?)",
                    (nome, preset["order"]),
                )
                db.execute_non_query(
                    "UPDATE categories SET ordem = ? WHERE nome = ? AND (ordem IS NULL OR ordem = 0)",
                    (preset["order"], nome),
                )

    @staticmethod
    def get_default_id():
        CategoryModel.ensure_defaults()
        default = CategoryModel.get_by_name("Sem categoria")
        if default:
            return default["id"]
        created = CategoryModel.create("Sem categoria", category_order("Sem categoria"))
        return created["id"]

    @staticmethod
    def create(nome: str, ordem: int = 0):
        try:
            with DatabaseManager() as db:
                cur = db.execute_non_query(
                    "INSERT INTO categories (nome, ordem) VALUES (?, ?)",
                    (nome, ordem),
                )
                row = db.execute_query(
                    "SELECT id, nome, ordem FROM categories WHERE id = ?",
                    (cur.lastrowid,),
                )[0]
                data = dict(row)
                data["total_itens"] = 0
                return data
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe uma categoria com esse nome") from exc

    @staticmethod
    def update(category_id: int, nome: str, ordem: int = 0):
        try:
            with DatabaseManager() as db:
                cur = db.execute_non_query(
                    "UPDATE categories SET nome = ?, ordem = ? WHERE id = ?",
                    (nome, ordem, category_id),
                )
                if cur.rowcount == 0:
                    return None
                row = db.execute_query(
                    """
                    SELECT c.id, c.nome, c.ordem, COUNT(m.id) AS total_itens
                    FROM categories c
                    LEFT JOIN menu m ON m.categoria_id = c.id
                    WHERE c.id = ?
                    GROUP BY c.id, c.nome, c.ordem
                    """,
                    (category_id,),
                )[0]
                return dict(row)
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe uma categoria com esse nome") from exc

    @staticmethod
    def delete(category_id: int):
        protected = CategoryModel.get_by_name("Sem categoria")
        if protected and protected["id"] == category_id:
            raise ValueError("A categoria padrão não pode ser removida")

        with DatabaseManager() as db:
            item_count = db.execute_query(
                "SELECT COUNT(1) AS total FROM menu WHERE categoria_id = ?",
                (category_id,),
            )[0]["total"]
            if item_count:
                raise ValueError("Remova ou recategorize os itens antes de excluir a categoria")
            cur = db.execute_non_query(
                "DELETE FROM categories WHERE id = ?",
                (category_id,),
            )
            return cur.rowcount > 0
