from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments submitted to teacher"""
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)

@teacher_assignments_resources.route('assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""    
    submit_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.updateGrade(
        _id=submit_assignment_payload.id,
        grade=submit_assignment_payload.grade, 
        principal=p)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)