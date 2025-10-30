from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
import os, json, pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "futurix.db")
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)

class Record(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_file: Optional[str]
    raw_json: Optional[str]

def init_db():
    SQLModel.metadata.create_all(engine)

def save_record(parsed: dict, source_file: str = None):
    init_db()
    with Session(engine) as s:
        r = Record(source_file=source_file, raw_json=json.dumps(parsed))
        s.add(r)
        s.commit()
        s.refresh(r)
        return r.id

def list_records():
    init_db()
    with Session(engine) as s:
        res = s.exec(select(Record)).all()
        return [{"id": r.id, "source_file": r.source_file, "parsed": json.loads(r.raw_json)} for r in res]

def delete_record(record_id: int):
    init_db()
    with Session(engine) as s:
        record = s.get(Record, record_id)
        if record:
            s.delete(record)
            s.commit()
            return True
        return False

def export_csv(path=None):
    init_db()
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "futurix_export.csv")
    with Session(engine) as s:
        res = s.exec(select(Record)).all()
        rows = []
        for r in res:
            parsed = json.loads(r.raw_json)
            rows.append({
                "id": r.id,
                "vendor_name": parsed.get("vendor_name"),
                "document_number": parsed.get("document_number"),
                "po_number": parsed.get("po_number"),
                "invoice_date": parsed.get("invoice_date"),
                "total_amount": parsed.get("total_amount")
            })
        df = pd.DataFrame(rows)
        df.to_csv(path, index=False)
        return path
