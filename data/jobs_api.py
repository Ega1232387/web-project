from flask import jsonify, Blueprint, request

from data import db_session
from data.jobs import Jobs

blueprint = Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify({'jobs': [item.to_dict(
        only=('id', 'job', 'team_leader', 'work_size', 'department',
              'start_date', 'end_date', 'is_finished', 'category')
    )
        for item in jobs]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify({'jobs': jobs.to_dict(
        only=('id', 'job', 'team_leader', 'work_size', 'department',
              'start_date', 'end_date', 'is_finished', 'category')
    )})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'department', 'category']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    jobs = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        department=request.json['department'],
        category=request.json['category'],
        is_finished=request.json['is_finished']
    )
    if db_sess.query(Jobs).filter(Jobs.id == jobs.id).first():
        return jsonify({'error': 'Id already exists'})
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['POST'])
def edit_job(job_id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'department', 'category']):
        return jsonify({'error': 'Bad request'})

    jobs = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        department=request.json['department'],
        category=request.json['category'],
        is_finished=request.json['is_finished']
    )
    job_to_edit = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job_to_edit:
        return jsonify({'error': 'Not found'})
    if job_to_edit:
        job_to_edit.id = jobs.id
        job_to_edit.job = jobs.job
        job_to_edit.team_leader = jobs.team_leader
        job_to_edit.work_size = jobs.work_size
        job_to_edit.department = jobs.department
        job_to_edit.category = jobs.category
        job_to_edit.is_finished = jobs.is_finished
    db_sess.commit()
    return jsonify({'success': 'OK'})
