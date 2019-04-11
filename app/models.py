#!/usr/bin/env python3


from .appsql import db
from sqlalchemy.sql import func

class Bgvisit(db.Model):

    __tablename__ = 'bg_visit'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    visit_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    visit_name = db.Column(db.String(255), nullable=False)
    visit_ip = db.Column(db.String(255), nullable=True)

    created_at =  db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())
