import contextlib
import io
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import academia as app


class AcademiaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'study.db'
        self.db = app.connect(self.path)
        with self.db:
            self.db.executemany('INSERT INTO courses VALUES (?,?)', [('math', 'Math'), ('cs', 'CS')])
        self.row = dict(id='q1', topic='Topic', question='Question?', answer='Answer', source='Lecture 1', hints=['Hint'])

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def run_quiet(self, function, *args, inputs=()):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', side_effect=inputs):
            function(*args)
        return output.getvalue()

    def test_trust_cannot_be_imported_and_pending_cannot_be_studied(self):
        app.import_questions(self.db, 'math', [dict(self.row, status='trusted', reviewed_at='today')], 'ai')
        output = self.run_quiet(app.study, self.db, 'math')
        self.assertIn('No trusted questions', output)
        row = self.db.execute('SELECT * FROM questions').fetchone()
        self.assertEqual(row['status'], 'pending')
        self.assertIsNone(row['reviewed_at'])

    def test_course_isolation_and_persistent_attempt(self):
        for course in ('math', 'cs'):
            app.import_questions(self.db, course, [self.row], 'manual')
        self.run_quiet(app.review, self.db, 'math', None, inputs=['a'])
        self.assertIn('No trusted questions', self.run_quiet(app.study, self.db, 'cs'))
        self.run_quiet(app.study, self.db, 'math', inputs=['/hint', 'my answer', '80', 'y', 'hard'])
        reopened = app.connect(self.path)
        try:
            rows = reopened.execute('SELECT * FROM attempts').fetchall()
            self.assertEqual(len(rows), 1)
            self.assertEqual((rows[0]['course'], rows[0]['confidence'], rows[0]['hints_used']), ('math', 80, 1))
            self.assertEqual(rows[0]['response'], 'my answer')
        finally:
            reopened.close()

    def test_answer_is_hidden_until_attempt_and_confidence(self):
        app.import_questions(self.db, 'math', [self.row], 'manual')
        self.run_quiet(app.review, self.db, 'math', None, inputs=['a'])
        output = io.StringIO()
        responses = iter(['', 'attempt', '101', '80', 'n', 'hard'])
        def answer(prompt):
            if prompt.startswith(('Your attempt', 'Before seeing')):
                self.assertNotIn('ANSWER', output.getvalue())
            return next(responses)
        with contextlib.redirect_stdout(output), patch('builtins.input', side_effect=answer):
            app.study(self.db, 'math')
        self.assertIn('ANSWER', output.getvalue())

    def test_import_validation_and_collision_are_atomic(self):
        with self.assertRaises(ValueError):
            app.import_questions(self.db, 'math', [self.row, dict(self.row, id='q2', answer='')], 'ai')
        self.assertEqual(self.db.execute('SELECT count(*) FROM questions').fetchone()[0], 0)
        app.import_questions(self.db, 'math', [self.row], 'manual')
        with self.assertRaises(sqlite3.IntegrityError):
            app.import_questions(self.db, 'math', [dict(self.row, id='q2'), self.row], 'ai')
        self.assertEqual(self.db.execute('SELECT count(*) FROM questions').fetchone()[0], 1)

    def test_rejected_and_skipped_questions_remain_unavailable(self):
        app.import_questions(self.db, 'math', [self.row, dict(self.row, id='q2')], 'ai')
        self.run_quiet(app.review, self.db, 'math', None, inputs=['r', 's'])
        self.assertIn('No trusted questions', self.run_quiet(app.study, self.db, 'math'))

    def test_legacy_init_is_repeatable(self):
        self.run_quiet(app.seed_legacy, self.db)
        count = self.db.execute('SELECT count(*) FROM questions').fetchone()[0]
        self.assertGreater(count, 100)
        self.run_quiet(app.seed_legacy, self.db)
        self.assertEqual(self.db.execute('SELECT count(*) FROM questions').fetchone()[0], count)
        self.assertEqual(self.db.execute("SELECT count(*) FROM questions WHERE status='trusted'").fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
