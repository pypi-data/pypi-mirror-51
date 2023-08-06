from contextlib import closing
import traceback
import datetime
import os
import sqlite3
import time
import abc

import uuid
from enum import Enum
from pailab.ml_repo.repo_objects import repo_object_init, RawData, RepoInfoKey  # pylint: disable=E0401
from pailab.ml_repo.repo import MLObjectType  # pylint: disable=E0401

import logging
logger = logging.getLogger(__name__)
logger_sql = logging.getLogger(__name__ + '_SQLITE')


class JobState(Enum):
    """Job states
    """
    SUBMITTED = 'submitted'
    WAITING_PRED = 'waiting_for_predecessor'
    WAITING = 'waiting'
    RUNNING = 'running'
    SUCCESSFULLY_FINISHED = 'successfully_finished'
    FAILED = 'failed'


class JobInfo:
    def __init__(self, user):
        self.user = user
        self.state = JobState.SUBMITTED.value
        self.submission_time = None
        self.error_message = None
        self.trace_back = None
        self.start_time = None
        self.end_time = None

    def set_state(self, state):
        self.state = state.value

    def set_start_time(self):
        self.start_time = datetime.datetime.now()

    def set_end_time(self):
        self.end_time = datetime.datetime.now()

    def __str__(self):
        result = self.user + ', ' + self.state + ', started ' + \
            str(self.start_time) + ', finished ' + str(self.end_time)
        if self.error_message is not None:
            result = result + ',  error_message: ' + self.error_message
        return result


class JobRunnerBase(abc.ABC):
    """Baseclass for all job runners so that they can be used together with the MLRepo
    """

    @abc.abstractmethod
    def add(self, job_name, job_version, user):  # pragma: no cover
        """[summary]
        """
        pass

    @abc.abstractmethod
    def get_info(self, job_name, job_version):  # pragma: no cover
        """[summary]
        """
        pass


class SimpleJobRunner(JobRunnerBase):
    def __init__(self, repo, throw_job_error = False):
        """Constructor
        
        Args:
            :param: repo (MLRepo): repository 
            throw_job_error (bool, optional): Defaults to False. If True, all errors from job will be rethrown. Otherwise, 
                error and traceback are stored in job only and no error will be thrown.
        """

        self._repo = repo
        self._job_info = {}
        self._throw_job_error = throw_job_error

    def set_repo(self, repo):
        self._repo = repo

    def get_info(self, job_name, job_version):
        jobid = job_name + ':' + str(job_version)
        return self._job_info[jobid]

    def add(self, job_name, job_version, user):
        job_id = job_name + ':' + str(job_version)
        job_info = JobInfo(user)
        job_info.set_state(JobState.RUNNING)
        job_info.start_time = datetime.datetime.now()
        self._job_info[job_id] = job_info
        job = self._repo.get(job_name, version=job_version)
        try:
            job.run(self._repo, job_id)
            job_info.end_time = datetime.datetime.now()
            job_info.set_state(JobState.SUCCESSFULLY_FINISHED)
        except Exception as e:
            logger.error(str(e) + ': ' + str(traceback.format_exc()))
            job_info.end_time = datetime.datetime.now()
            job_info.set_state(JobState.FAILED)
            job_info.error_message = str(e)
            job_info.trace_back = traceback.format_exc()
            if self._throw_job_error:
                raise e

        return job_id

    def get_waiting_jobs(self):
        """Return list of open jobs

        Returns:
            empty list because by construction, this JobRunner can only return something if the jobs have been finished
        """
        return []


class SQLiteJobRunner(JobRunnerBase):
    # region private
    def _create_new_db(self):
        logger.info('Creating new database for job runner.')
        self._conn = sqlite3.connect(self._sqlite_db_name)
        with closing(self._conn.cursor()) as cursor:
            cursor.execute('''CREATE TABLE predecessors (job_name TEXT NOT NULL, job_version TEXT NOT NULL, predecessor_name TEXT NOT NULL, predecessor_version TEXT NOT NULL, PRIMARY KEY(job_name, job_version))''')
            cursor.execute(
                '''CREATE TABLE jobs (job_name TEXT NOT NULL, job_version TEXT NOT NULL, job_state TEXT NOT NULL, start_time TIMESTAMP,
                                            end_time TIMESTAMP, error_message TEXT, stack_trace TEXT, insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                                            unfinished_pred_jobs INTEGER, user TEXT NOT NULL, PRIMARY KEY(job_name, job_version))''')
            self._conn.commit()
        
    def _setup_new(self):
        if not os.path.exists(self._sqlite_db_name):
            self._create_new_db()
        else:
            self._conn = sqlite3.connect(self._sqlite_db_name)

    @staticmethod
    def sqlite_name(name):
        return "'" + name + "'"

    def _set_finished(self, job_name, job_version, error_message='', stack_trace=''):
        '''Set the job finished

            It sets the job to finished and removes predecessor conditions respectively
        Args:
            job_name (str): name of job
            job_version (str): version of job
            error_message (str, optional): Defaults to ''. Error message if job raised an error
            stack_trace (str, optional): Defaults to ''. Stack trace of error.
        '''
        successfull = True
        if error_message != '' or stack_trace != '':
            successfull = False
        # first update jobs waiting for the job to be finished
        with closing(self._conn.cursor()) as cursor:
            if successfull:
                candidates = []
                for row in cursor.execute("select job_name, job_version from predecessors where predecessor_name = '"
                                        + job_name + "'" + " and predecessor_version = '" + job_version + "'"):
                    candidates.append((row[0], row[1]))
                cursor.execute( "delete from predecessors where predecessor_name = '"
                            + job_name + "'" + " and predecessor_version = '" + job_version + "'")
                self._conn.commit()
                for c in candidates:
                    cursor.execute("update jobs SET unfinished_pred_jobs=unfinished_pred_jobs-1  where job_name='" +
                                c[0] + "' and job_version='" + c[1] + "'")
                    self._conn.commit()
                    cursor.execute("update jobs SET job_state='" + JobState.WAITING.value + "' where job_name='" +
                                c[0] + "' and job_version='" + c[1] + "' and unfinished_pred_jobs <= 0")
                    self._conn.commit()
                cursor.execute("update jobs SET job_state='" + JobState.SUCCESSFULLY_FINISHED.value + "', end_time='" + str(datetime.datetime.now())
                            + "' where job_name = '" + job_name + "' and job_version = '" + job_version + "'")
                self._conn.commit()
            else:
                cursor.execute("update jobs SET job_state='" + JobState.FAILED.value + "', error_message='" + error_message.replace("'", "") + "', stack_trace='" + stack_trace.replace("'", "") + "', end_time='"
                            + str(datetime.datetime.now()) + "' where job_name = '" +
                            job_name + "' and job_version = '" + str(job_version) + "'")
                self._conn.commit()
        

    def _run_job(self, job_name, job_version):
        job = self._repo.get(job_name, version=job_version)
        try:
            job.run(self._repo, 0)
        except Exception as e:
            logger.error(str(e) + ': ' + str(traceback.format_exc()))
            return str(e), traceback.format_exc()
        return '', ''

    # endregion

    def __init__(self, sqlite_db_name, repo, sleep = 1, steps_to_heartbeat = 30):
        '''Contructor

        Args:
            sqlite_db_name (str): filename of sqlite database used
        '''
        self._sqlite_db_name = sqlite_db_name
        self._setup_new()
        self._sleep = sleep  # time to wait in sec before new request for open jobs to db
        self._steps_to_heartbeat = steps_to_heartbeat
        self._repo = repo
        self._id = str(uuid.uuid1())
        self._conn.set_trace_callback(logger_sql.info)

    def set_repo(self, repo):
        self._repo = repo

    def add(self, job_name, job_version, user):
        with closing(self._conn.cursor()) as cursor:
            job = self._repo.get(job_name, version=job_version)
            predecessors = job.get_predecessor_jobs()
            for predecessor in predecessors:
                cursor.execute("insert into predecessors (job_name, job_version, predecessor_name, predecessor_version) VALUES ("
                            + SQLiteJobRunner.sqlite_name(job_name) +
                            ", "
                            + SQLiteJobRunner.sqlite_name(str(job_version)) +
                            ","
                            + SQLiteJobRunner.sqlite_name(predecessor[0]) +
                            ","
                            + SQLiteJobRunner.sqlite_name(str(predecessor[1])) +
                            ")")
                self._conn.commit()
            job_state = JobState.WAITING.value
            if len(predecessors) > 0:
                job_state = JobState.WAITING_PRED.value
            cursor.execute("insert into jobs ( job_name, job_version, job_state,  unfinished_pred_jobs, user ) VALUES ("
                        + SQLiteJobRunner.sqlite_name(job.repo_info[RepoInfoKey.NAME]) +
                        ", "
                        + SQLiteJobRunner.sqlite_name(str(job.repo_info[RepoInfoKey.VERSION])) +
                        ",'"
                        + job_state +
                        "',"
                        + str(len(predecessors)) +
                        ", '" + user + "')")
            self._conn.commit()

    def run(self, max_steps=None):
        wait = self._sleep
        step = 0
        with closing(self._conn.cursor()) as cursor: 
            while True:
                if max_steps is not None:
                    step += 1
                    if step > max_steps:
                        return
                if wait > self._steps_to_heartbeat:
                    logger.info('heartbeat')
                    wait = 0
                row = None
                with self._conn:
                    cursor.execute("select job_name, job_version from jobs where job_state = '"
                                        + JobState.WAITING.value + "' order by insert_time desc")
                    row = cursor.fetchone()
                    if row is not None:
                        cursor.execute("update jobs SET start_time = '" + str(
                            datetime.datetime.now()) + "', job_state='" + JobState.RUNNING.value + "' where job_name = '"
                            + row[0] + "' and job_version='" + row[1] + "'")
                        self._conn.commit()
                    
                #logger.error('len(rows): ' + str(len(rows)))
                if row is not None:
                    logger.info('Start running job ' +
                                row[0] + ', version ' + row[1])
                    error, stack_trace = self._run_job(row[0], row[1])
                    self._set_finished(row[0], row[1], error, stack_trace)
                    if error == '' and stack_trace == '':
                        logger.info('Finished running job ' +
                                    row[0] + ', version ' + row[1] + ' successfully.')
                    else:
                        logger.error('Finished running job ' + row[0] + ', version ' +
                                    row[1] + ' with errors: ' + error + '   stacktrace: ' + stack_trace)
                    wait = 0
                else:
                    time.sleep(self._sleep)
                    wait += self._sleep
        
    def get_info(self, job_name, job_version):
        result = {}
        with closing(self._conn.cursor()) as cursor:
            rows = cursor.execute("select * from jobs where job_name='" +
                                job_name + "' and job_version = '" + str(job_version) + "'")
            column_names = [x[0] for x in rows.description]
            for row in rows:
                for i in range(len(row)):
                    result[column_names[i]] = row[i]
                cursor.close()
                return result
        return {'message': 'no info available for ' + job_name + ', version ' + str(job_version)}

    def get_waiting_jobs(self):
        """Return list of open jobs

        Returns:
            list of tuples: list containing tuples of job names and versions of the jobs currently waiting
        """
        open_jobs = []
        with closing(self._conn.cursor()) as cursor:
            for row in cursor.execute( "select job_name, job_version from jobs where job_state in ('"
                                    + JobState.WAITING.value + "','" + JobState.WAITING_PRED.value + "','" + JobState.RUNNING.value +"')"):
                open_jobs.append((row[0], row[1]))
        return open_jobs

    def close_connection(self):
        """Closes the database connection
        """
        self._conn.close()
