import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

collaborators = sqlalchemy.Table('collaborators', SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('jobs', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('jobs.id'))
)

class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader_id = sqlalchemy.Column(sqlalchemy.Integer,
                                      sqlalchemy.ForeignKey("users.id"))
    team_leader = orm.relation('User')
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = orm.relation("User", secondary="collaborators", backref='user')
    # collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
