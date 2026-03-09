from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(64), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(db.String(256), nullable=False)
    is_admin: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=False)

    submissions: Mapped[list["Submission"]] = db.relationship(
        "Submission", back_populates="user", lazy="dynamic"
    )


class Problem(db.Model):
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(256), nullable=False)
    question_text: Mapped[str] = mapped_column(db.Text, nullable=False)
    # "symbolic" or "written"
    problem_type: Mapped[str] = mapped_column(db.String(32), nullable=False)
    answer_key: Mapped[str] = mapped_column(db.Text, nullable=False)
    rubric: Mapped[str] = mapped_column(db.Text, nullable=True)

    submissions: Mapped[list["Submission"]] = db.relationship(
        "Submission", back_populates="problem", lazy="dynamic"
    )


class Submission(db.Model):
    __tablename__ = "submissions"
    __table_args__ = (
        Index("ix_submissions_user_id", "user_id"),
        Index("ix_submissions_problem_id", "problem_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    problem_id: Mapped[int] = mapped_column(db.ForeignKey("problems.id"), nullable=False)
    student_answer: Mapped[str] = mapped_column(db.Text, nullable=False)
    score: Mapped[float] = mapped_column(db.Float, nullable=True)
    feedback: Mapped[str] = mapped_column(db.Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = db.relationship("User", back_populates="submissions")
    problem: Mapped["Problem"] = db.relationship("Problem", back_populates="submissions")
