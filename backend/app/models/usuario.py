from app.database import DatabaseManager


class UserModel:
    @staticmethod
    def get_by_login(login: str):
        with DatabaseManager() as db:
            rows = db.execute_query(
                "SELECT id, login, nome, email, senha_hash, perfil, ativo, criado_em FROM users WHERE login = ?",
                (login,),
            )
            return dict(rows[0]) if rows else None
