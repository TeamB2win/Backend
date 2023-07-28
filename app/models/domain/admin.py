from typing import List

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from db.orm import CriminalData

# 범죄자 전체 조회
def search_criminals_data(session: Session) -> CriminalData:
    #return session.scalars(select(CriminalData)).all()
    return session.execute(select(CriminalData)).scalars().all()

# 범죄자 1명 조회
def search_criminal_data(session: Session, criminal_id: int) -> CriminalData | None:
    return session.scalar(select(CriminalData).where(CriminalData.id == criminal_id))

# 범죄자 데이터 추가
def create_criminal_data(session: Session, criminal_data: CriminalData) -> CriminalData:
    session.add(instance=criminal_data) # session object에 저장
    session.commit() # 데이터베이스에 저장
    session.refresh(instance=criminal_data) # 데이터베이스에서 다시 읽기
    return criminal_data

# 범죄자 데이터 수정
def update_criminal_data(session: Session, criminal_data: CriminalData) -> CriminalData:
    session.add(instance=criminal_data)
    session.commit()
    session.refresh(instance=criminal_data)
    return criminal_data

# 범죄자 데이터 삭제
def delete_criminal_data(session: Session, criminal_id: int) -> None:
    session.execute(delete(CriminalData).where(CriminalData.id == criminal_id))
    session.commit()
