from datetime import datetime
from app.database import DatabaseManager
from app.models.menu import MenuModel
from app.utils import status


class Order:
    @staticmethod
    def _to_date(date_str: str | None):
        if not date_str:
            return datetime.today().strftime("%Y-%m-%d")
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")

    @staticmethod
    def create(nome_cliente: str, item_ids: list[int]):
        menu_items = MenuModel.get_by_ids(item_ids)
        found_ids = {row["id"] for row in menu_items}
        missing = [i for i in item_ids if i not in found_ids]
        if missing:
            raise ValueError(f"Itens inválidos: {missing}")

        total = sum(float(row["valor"]) for row in menu_items)
        itens_str = ", ".join([f"{row['item']} (R$ {row['valor']:.2f})" for row in menu_items])
        today = datetime.today().strftime("%Y-%m-%d")
        with DatabaseManager() as db:
            cur = db.execute_non_query(
                """
                INSERT INTO orders (data, nome_cliente, itens, status, valor_total)
                VALUES (?, ?, ?, ?, ?)
                """,
                (today, nome_cliente, itens_str, status[0], total),
            )
            order_id = cur.lastrowid
            row = db.execute_query(
                "SELECT id, data, nome_cliente, itens, status, valor_total FROM orders WHERE id = ?", (order_id,)
            )[0]
            return dict(row)

    @staticmethod
    def get(order_id: int):
        with DatabaseManager() as db:
            rows = db.execute_query(
                "SELECT id, data, nome_cliente, itens, status, valor_total FROM orders WHERE id = ?", (order_id,)
            )
            return dict(rows[0]) if rows else None

    @staticmethod
    def list_all(data: str | None = None, status_filter: str | None = None):
        query = "SELECT id, data, nome_cliente, itens, status, valor_total FROM orders WHERE 1=1"
        params = []
        if data:
            query += " AND data = ?"
            params.append(Order._to_date(data))
        if status_filter:
            query += " AND status = ?"
            params.append(status_filter)
        query += " ORDER BY id"
        with DatabaseManager() as db:
            rows = db.execute_query(query, tuple(params) if params else None)
            return [dict(r) for r in rows]

    @staticmethod
    def list_pending():
        with DatabaseManager() as db:
            rows = db.execute_query(
                "SELECT id, data, nome_cliente, itens, status, valor_total FROM orders WHERE status != 'Entregue' ORDER BY id"
            )
            return [dict(r) for r in rows]

    @staticmethod
    def advance_status(order_id: int):
        with DatabaseManager() as db:
            rows = db.execute_query("SELECT status FROM orders WHERE id = ?", (order_id,))
            if not rows:
                raise LookupError("Pedido não encontrado")
            current = rows[0]["status"]
            idx = status.index(current)
            if idx == len(status) - 1:
                raise ValueError("Pedido já está Entregue")
            nxt = status[idx + 1]
            db.execute_non_query("UPDATE orders SET status = ? WHERE id = ?", (nxt, order_id))
            row = db.execute_query("SELECT id, data, nome_cliente, itens, status, valor_total FROM orders WHERE id = ?", (order_id,))[0]
            return dict(row)

    @staticmethod
    def delete(order_id: int):
        with DatabaseManager() as db:
            rows = db.execute_query("SELECT status FROM orders WHERE id = ?", (order_id,))
            if not rows:
                raise LookupError("Pedido não encontrado")
            if rows[0]["status"] != "Pendente":
                raise ValueError("Apenas pedidos pendentes podem ser cancelados")
            db.execute_non_query("DELETE FROM orders WHERE id = ?", (order_id,))

    @staticmethod
    def revenue(inicio: str | None = None, fim: str | None = None):
        if not inicio:
            inicio = datetime.today().strftime("%d/%m/%Y")
        if not fim:
            fim = inicio
        ini_iso = datetime.strptime(inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
        fim_iso = datetime.strptime(fim, "%d/%m/%Y").strftime("%Y-%m-%d")
        with DatabaseManager() as db:
            rows = db.execute_query("SELECT COALESCE(SUM(valor_total), 0) AS total FROM orders WHERE data BETWEEN ? AND ?", (ini_iso, fim_iso))
            return {"total": float(rows[0]["total"]), "inicio": ini_iso, "fim": fim_iso}

    @staticmethod
    def best_sellers(limit: int = 10):
        with DatabaseManager() as db:
            rows = db.execute_query("SELECT itens FROM orders")
        ranking: dict[str, int] = {}
        for row in rows:
            parts = [p.strip() for p in row["itens"].split(",")]
            for p in parts:
                nome = p.split(" (R$")[0].strip()
                if nome:
                    ranking[nome] = ranking.get(nome, 0) + 1
        data = sorted(ranking.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [{"item": item, "quantidade": qtd} for item, qtd in data]
