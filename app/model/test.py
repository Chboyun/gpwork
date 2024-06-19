from typing import List, Optional

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, Integer, String, text
from sqlalchemy.dialects.mysql import TEXT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Label(Base):
    __tablename__ = 'label'

    label_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label_name: Mapped[str] = mapped_column(VARCHAR(255))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    description: Mapped[str] = mapped_column(String(255), server_default=text("'没有描述'"))

    kl_label: Mapped[List['KlLabel']] = relationship('KlLabel', back_populates='label')


class Library(Base):
    __tablename__ = 'library'

    library_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    library_name: Mapped[str] = mapped_column(VARCHAR(255))
    description: Mapped[str] = mapped_column(VARCHAR(255), server_default=text("'没有描述'"), comment='对知识库的简要描述')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    kl_library: Mapped[List['KlLibrary']] = relationship('KlLibrary', back_populates='library')


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(255))
    password: Mapped[str] = mapped_column(VARCHAR(255))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    knowledge: Mapped[List['Knowledge']] = relationship('Knowledge', back_populates='user')
    collect: Mapped[List['Collect']] = relationship('Collect', back_populates='user')
    comment: Mapped[List['Comment']] = relationship('Comment', back_populates='user')


class Knowledge(Base):
    __tablename__ = 'knowledge'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.user_id'], name='user_id'),
        Index('user_id', 'user_id')
    )

    kl_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, comment='创建人')
    kl_title: Mapped[str] = mapped_column(VARCHAR(255), server_default=text("'空'"), comment='标题')
    kl_like: Mapped[int] = mapped_column(Integer, server_default=text("'0'"), comment='点赞数量')
    kl_dislike: Mapped[int] = mapped_column(Integer, server_default=text("'0'"), comment='点踩数量')
    kl_hot: Mapped[int] = mapped_column(Integer, server_default=text("'0'"), comment='热度')
    kl_state: Mapped[int] = mapped_column(Integer, server_default=text("'0'"), comment='状态 ： \r\n0 ， 未审核\r\n1，  审核未通过\r\n2， 审核通过，上线状态\r\n3， 下线状态')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    kl_content: Mapped[Optional[str]] = mapped_column(TEXT, comment='富文本内容，html')

    user: Mapped['User'] = relationship('User', back_populates='knowledge')
    annex: Mapped[List['Annex']] = relationship('Annex', back_populates='kl')
    collect: Mapped[List['Collect']] = relationship('Collect', back_populates='kl')
    comment: Mapped[List['Comment']] = relationship('Comment', back_populates='kl')
    kl_label: Mapped[List['KlLabel']] = relationship('KlLabel', back_populates='kl')
    kl_library: Mapped[List['KlLibrary']] = relationship('KlLibrary', back_populates='kl')


class Annex(Base):
    __tablename__ = 'annex'
    __table_args__ = (
        ForeignKeyConstraint(['kl_id'], ['knowledge.kl_id'], name='annex_ibfk_1'),
        Index('kl_id', 'kl_id')
    )

    annex_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    annex_url: Mapped[str] = mapped_column(VARCHAR(255))
    kl_id: Mapped[int] = mapped_column(Integer)
    annex_name: Mapped[str] = mapped_column(VARCHAR(255), server_default=text("'未命名'"))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    kl: Mapped['Knowledge'] = relationship('Knowledge', back_populates='annex')


class Collect(Base):
    __tablename__ = 'collect'
    __table_args__ = (
        ForeignKeyConstraint(['kl_id'], ['knowledge.kl_id'], name='collect_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['user.user_id'], name='collect_ibfk_2'),
        Index('kl_id', 'kl_id'),
        Index('user_id', 'user_id')
    )

    collect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kl_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    kl: Mapped['Knowledge'] = relationship('Knowledge', back_populates='collect')
    user: Mapped['User'] = relationship('User', back_populates='collect')


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = (
        ForeignKeyConstraint(['kl_id'], ['knowledge.kl_id'], name='comment_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['user.user_id'], name='comment_ibfk_2'),
        Index('kl_id', 'kl_id'),
        Index('user_id', 'user_id')
    )

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kl_id: Mapped[int] = mapped_column(Integer, comment='对应的知识 id')
    comment_content: Mapped[str] = mapped_column(TEXT, comment='评论内容')
    user_id: Mapped[int] = mapped_column(Integer)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    kl: Mapped['Knowledge'] = relationship('Knowledge', back_populates='comment')
    user: Mapped['User'] = relationship('User', back_populates='comment')


class KlLabel(Base):
    __tablename__ = 'kl_label'
    __table_args__ = (
        ForeignKeyConstraint(['kl_id'], ['knowledge.kl_id'], name='kl_label_ibfk_1'),
        ForeignKeyConstraint(['label_id'], ['label.label_id'], ondelete='RESTRICT', onupdate='RESTRICT', name='kl_label_ibfk_2'),
        Index('kl_id', 'kl_id'),
        Index('label_id', 'label_id')
    )

    kl_label_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kl_id: Mapped[int] = mapped_column(Integer)
    label_id: Mapped[int] = mapped_column(Integer)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    kl: Mapped['Knowledge'] = relationship('Knowledge', back_populates='kl_label')
    label: Mapped['Label'] = relationship('Label', back_populates='kl_label')


class KlLibrary(Base):
    __tablename__ = 'kl_library'
    __table_args__ = (
        ForeignKeyConstraint(['kl_id'], ['knowledge.kl_id'], ondelete='RESTRICT', onupdate='RESTRICT', name='kl_library_ibfk_1'),
        ForeignKeyConstraint(['library_id'], ['library.library_id'], ondelete='RESTRICT', onupdate='RESTRICT', name='kl_library_ibfk_2'),
        Index('kl_id', 'kl_id'),
        Index('library_id', 'library_id')
    )

    kl_library_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    library_id: Mapped[int] = mapped_column(Integer)
    kl_id: Mapped[int] = mapped_column(Integer)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    kl: Mapped['Knowledge'] = relationship('Knowledge', back_populates='kl_library')
    library: Mapped['Library'] = relationship('Library', back_populates='kl_library')
