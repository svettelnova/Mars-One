import flask
from data import db_session
from data.jobs import Jobs
from flask import jsonify, request
import datetime

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify({'jobs': list(map(Jobs.to_dict, jobs))})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_jobs(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': job.to_dict()
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader_id', 'description', 'work_size', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if request.json['id']:
        job = session.query(Jobs).get(request.json['id'])
        if not job:
            return jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        team_leader_id=request.json['team_leader_id'],
        description=request.json['description'],
        work_size=request.json['work_size'],
        start_date=datetime.datetime.now(),
        is_finished=request.json['is_finished']
    )
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_news(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})
