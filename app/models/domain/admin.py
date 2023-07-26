from typing import List

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from Backend.app.db.orm import CriminalData

'''
# 범죄자 1명 검색
def search_criminal_data(session: Session, criminal_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))
'''

def create_criminal_data(session: Session, criminal_data: CriminalData) -> CriminalData:
    session.add(instance=criminal_data)
    session.commit()
    session.refresh(instance=criminal_data)
    return criminal_data


def update_criminal_data(session: Session, criminal_data: CriminalData) -> CriminalData:
    session.add(instance=criminal_data)
    session.commit()
    session.refresh(instance=criminal_data)
    return criminal_data


def delete_criminal_data(session: Session, criminal_id: int) -> None:
    session.execute(delete(CriminalData).where(CriminalData.id == criminal_id))
    session.commit()
