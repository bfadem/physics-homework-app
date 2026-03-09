import csv
import io

from flask import (
    Blueprint,
    Response,
    current_app,
    render_template,
    request,
)

from .models import Problem, Submission, User, db

bp = Blueprint("main", __name__)


# ---------------------------------------------------------------------------
# Public placeholders — grading logic not yet implemented
# ---------------------------------------------------------------------------


@bp.get("/")
def index():
    return render_template("coming_soon.html")


# ---------------------------------------------------------------------------
# Admin export
# ---------------------------------------------------------------------------


@bp.get("/admin/export.csv")
def export_csv():
    token = request.args.get("token", "")
    if not current_app.config.get("ADMIN_TOKEN") or token != current_app.config["ADMIN_TOKEN"]:
        return Response("Unauthorized", status=401)

    rows = (
        db.session.query(Submission, User, Problem)
        .join(User, Submission.user_id == User.id)
        .join(Problem, Submission.problem_id == Problem.id)
        .order_by(Submission.submitted_at.asc())
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "submission_id",
            "submitted_at",
            "user_id",
            "username",
            "problem_id",
            "problem_title",
            "problem_type",
            "student_answer",
            "score",
            "feedback",
        ]
    )

    for sub, user, problem in rows:
        writer.writerow(
            [
                sub.id,
                sub.submitted_at.isoformat(),
                user.id,
                user.username,
                problem.id,
                problem.title,
                problem.problem_type,
                sub.student_answer,
                sub.score,
                sub.feedback,
            ]
        )

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=submissions.csv"},
    )
