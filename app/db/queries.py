from sqlalchemy.orm import Session

def get_full_wanted_data(db: Session) :
    return db.query