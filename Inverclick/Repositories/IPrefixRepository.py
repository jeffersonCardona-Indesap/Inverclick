# pyrefly: ignore [missing-import]
from sqlalchemy import select
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from Models.prefix import Prefix

class IPrefixRepository:
    def get_by_id(self, prefix_id: int) -> Prefix | None:
        statement = select(Prefix).where(Prefix.id == prefix_id)
        return statement.scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        statement = select(Prefix).offset(skip).limit(limit)
        return statement.scalars().all()

    def get_by_code(self, code : str) -> Prefix | None:
        statement = select(Prefix).where(Prefix.country_phone_code == code)
        return statement.scalar_one_or_none()