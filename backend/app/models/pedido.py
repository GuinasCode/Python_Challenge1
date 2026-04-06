import json
import re
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
    def _normalize_items(requested_items: list[int] | list[dict]):
        normalized: list[dict] = []
        for item in requested_items:
            if isinstance(item, int):
                normalized.append({"item_id": item, "quantidade": 1})
                continue

            if hasattr(item, "model_dump"):
                item = item.model_dump()

            item_id = item.get("item_id", item.get("id"))
            quantidade = item.get("quantidade", 1)
            try:
                item_id = int(item_id)
                quantidade = int(quantidade)
            except (TypeError, ValueError) as exc:
                raise ValueError("Itens inválidos") from exc

            if item_id <= 0 or quantidade <= 0:
                raise ValueError("Itens inválidos")
            normalized.append({"item_id": item_id, "quantidade": quantidade})

        if not normalized:
            raise ValueError("Selecione ao menos um item")
        return normalized

    @staticmethod
    def _build_item_details(requested_items: list[dict], menu_items: list[dict]):
        menu_by_id = {item["id"]: item for item in menu_items}
        details = []
        total = 0.0

        for entry in requested_items:
            menu_item = menu_by_id[entry["item_id"]]
            quantidade = entry["quantidade"]
            subtotal = round(float(menu_item["valor"]) * quantidade, 2)
            total += subtotal
            details.append(
                {
                    "item_id": menu_item["id"],
                    "nome": menu_item["item"],
                    "quantidade": quantidade,
                    "valor_unitario": float(menu_item["valor"]),
                    "subtotal": subtotal,
                    "categoria_id": menu_item.get("categoria_id"),
                    "categoria_nome": menu_item.get("categoria_nome") or "Sem categoria",
                    "imagem_base64": menu_item.get("imagem_base64") or "",
                }
            )

        return details, round(total, 2)

    @staticmethod
    def _build_items_summary(details: list[dict]):
        return ", ".join(
            f"{item['quantidade']}x {item['nome']} (R$ {item['subtotal']:.2f})" for item in details
        )

    @staticmethod
    def _parse_legacy_details(summary: str):
        details = []
        if not summary:
            return details

        pattern = re.compile(
            r"(?:(?P<quantidade>\d+)x\s+)?(?P<nome>.+?)\s*\(R\$\s*(?P<valor>\d+(?:\.\d{2})?)\)"
        )
        for raw_part in summary.split(","):
            part = raw_part.strip()
            if not part:
                continue
            match = pattern.fullmatch(part)
            if match:
                quantidade = int(match.group("quantidade") or 1)
                subtotal = float(match.group("valor"))
                valor_unitario = round(subtotal / quantidade, 2) if quantidade else subtotal
                details.append(
                    {
                        "item_id": None,
                        "nome": match.group("nome").strip(),
                        "quantidade": quantidade,
                        "valor_unitario": valor_unitario,
                        "subtotal": subtotal,
                        "categoria_id": None,
                        "categoria_nome": "Sem categoria",
                        "imagem_base64": "",
                    }
                )
            else:
                details.append(
                    {
                        "item_id": None,
                        "nome": part,
                        "quantidade": 1,
                        "valor_unitario": 0.0,
                        "subtotal": 0.0,
                        "categoria_id": None,
                        "categoria_nome": "Sem categoria",
                        "imagem_base64": "",
                    }
                )
        return details

    @staticmethod
    def _deserialize_order_items(raw_order_items: str | None, fallback_summary: str | None = None):
        if raw_order_items:
            try:
                parsed = json.loads(raw_order_items)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
        return Order._parse_legacy_details(fallback_summary or "")

    @staticmethod
    def _serialize_order(row):
        data = dict(row)
        data["itens_detalhados"] = Order._deserialize_order_items(data.get("order_items"), data.get("itens"))
        data.pop("order_items", None)
        return data

    @staticmethod
    def create(nome_cliente: str, item_ids: list[int] | list[dict]):
        requested_items = Order._normalize_items(item_ids)
        menu_items = MenuModel.get_by_ids([entry["item_id"] for entry in requested_items])
        found_ids = {row["id"] for row in menu_items}
        missing = [entry["item_id"] for entry in requested_items if entry["item_id"] not in found_ids]
        if missing:
            raise ValueError(f"Itens inválidos: {missing}")

        details, total = Order._build_item_details(requested_items, menu_items)
        itens_str = Order._build_items_summary(details)
        today = datetime.today().strftime("%Y-%m-%d")
        with DatabaseManager() as db:
            cur = db.execute_non_query(
                """
                INSERT INTO orders (data, nome_cliente, itens, order_items, status, valor_total)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (today, nome_cliente, itens_str, json.dumps(details, ensure_ascii=False), status[0], total),
            )
            row = db.execute_query(
                "SELECT id, data, nome_cliente, itens, order_items, status, valor_total FROM orders WHERE id = ?",
                (cur.lastrowid,),
            )[0]
            return Order._serialize_order(row)

    @staticmethod
    def get(order_id: int):
        with DatabaseManager() as db:
            rows = db.execute_query(
                "SELECT id, data, nome_cliente, itens, order_items, status, valor_total FROM orders WHERE id = ?",
                (order_id,),
            )
            return Order._serialize_order(rows[0]) if rows else None

    @staticmethod
    def list_all(data: str | None = None, status_filter: str | None = None):
        query = "SELECT id, data, nome_cliente, itens, order_items, status, valor_total FROM orders WHERE 1=1"
        params = []
        if data:
            query += " AND data = ?"
            params.append(Order._to_date(data))
        if status_filter:
            query += " AND status = ?"
            params.append(status_filter)
        query += " ORDER BY id DESC"
        with DatabaseManager() as db:
            rows = db.execute_query(query, tuple(params) if params else None)
            return [Order._serialize_order(r) for r in rows]

    @staticmethod
    def list_pending():
        with DatabaseManager() as db:
            rows = db.execute_query(
                "SELECT id, data, nome_cliente, itens, order_items, status, valor_total FROM orders WHERE status != 'Entregue' ORDER BY id DESC"
            )
            return [Order._serialize_order(r) for r in rows]

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
            row = db.execute_query(
                "SELECT id, data, nome_cliente, itens, order_items, status, valor_total FROM orders WHERE id = ?",
                (order_id,),
            )[0]
            return Order._serialize_order(row)

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
            rows = db.execute_query(
                "SELECT COALESCE(SUM(valor_total), 0) AS total FROM orders WHERE data BETWEEN ? AND ?",
                (ini_iso, fim_iso),
            )
            return {"total": float(rows[0]["total"]), "inicio": ini_iso, "fim": fim_iso}

    @staticmethod
    def best_sellers(limit: int = 10):
        with DatabaseManager() as db:
            rows = db.execute_query("SELECT itens, order_items FROM orders")
        ranking: dict[str, int] = {}
        for row in rows:
            details = Order._deserialize_order_items(row["order_items"], row["itens"])
            for item in details:
                nome = item.get("nome")
                quantidade = int(item.get("quantidade", 1))
                if nome:
                    ranking[nome] = ranking.get(nome, 0) + quantidade
        data = sorted(ranking.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [{"item": item, "quantidade": qtd} for item, qtd in data]
