#!/usr/bin/env python3
"""Academia: an offline, course-based retrieval practice CLI (Python standard library)."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import random
import sqlite3
import sys
import time

ROOT = Path(__file__).resolve().parent


def connect(path):
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    db.executescript('''
        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS questions (
            course TEXT NOT NULL REFERENCES courses(id), id TEXT NOT NULL,
            topic TEXT NOT NULL, question TEXT NOT NULL, answer TEXT NOT NULL,
            source TEXT NOT NULL, origin TEXT NOT NULL,
            kind TEXT NOT NULL, hints TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending', reviewed_at TEXT,
            PRIMARY KEY(course, id));
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY, course TEXT NOT NULL, question_id TEXT NOT NULL,
            attempted_at TEXT NOT NULL, response TEXT NOT NULL,
            confidence INTEGER NOT NULL, correct INTEGER NOT NULL,
            hints_used INTEGER NOT NULL, seconds REAL NOT NULL,
            difficulty TEXT NOT NULL, method TEXT NOT NULL,
            question_snapshot TEXT NOT NULL,
            FOREIGN KEY(course, question_id) REFERENCES questions(course, id));
    ''')
    return db


def now():
    return datetime.now(timezone.utc).isoformat()


def require_course(db, course):
    if not db.execute('SELECT 1 FROM courses WHERE id=?', (course,)).fetchone():
        raise ValueError(f'Unknown course {course!r}. Create it with: course add {course} "Course name"')


def nonempty(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{field} must be a nonempty string')
    return value.strip()


def import_questions(db, course, rows, origin):
    """Validate the complete batch before inserting; imported trust flags are ignored."""
    require_course(db, course)
    if not isinstance(rows, list) or not rows:
        raise ValueError('Import must be a nonempty JSON array')
    records = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Every question must be a JSON object')
        fields = {key: nonempty(row.get(key), key)
                  for key in ('id', 'topic', 'question', 'answer', 'source')}
        if fields['id'] in seen:
            raise ValueError(f"Duplicate question id: {fields['id']}")
        seen.add(fields['id'])
        hints = row.get('hints', [])
        if not isinstance(hints, list) or any(not isinstance(h, str) or not h.strip() for h in hints):
            raise ValueError('hints must be an array of nonempty strings')
        kind = nonempty(row.get('kind', 'recall'), 'kind')
        records.append((course, fields['id'], fields['topic'], fields['question'],
                        fields['answer'], fields['source'], origin, kind, json.dumps(hints)))
    with db:
        db.executemany('''INSERT INTO questions
            (course,id,topic,question,answer,source,origin,kind,hints)
            VALUES (?,?,?,?,?,?,?,?,?)''', records)
    return len(records)


def prompt_choice(prompt, choices):
    while True:
        value = input(prompt).strip().lower()
        if value in choices:
            return value
        print('Choose: ' + ', '.join(choices))


def confidence_prompt():
    while True:
        try:
            confidence = int(input('Before seeing the answer, confidence in correctness (0–100): '))
            if 0 <= confidence <= 100:
                return confidence
        except ValueError:
            pass
        print('Enter an integer from 0 to 100.')


def review(db, course, question_id):
    require_course(db, course)
    query = "SELECT * FROM questions WHERE course=? AND status='pending'"
    params = [course]
    if question_id:
        query += ' AND id=?'
        params.append(question_id)
    rows = db.execute(query + ' ORDER BY id', params).fetchall()
    if not rows:
        print('No matching pending questions.')
    for row in rows:
        print(f"\n[{row['id']}] {row['topic']} | {row['origin']} | {row['kind']}")
        print(f"Source: {row['source']}\nQuestion: {row['question']}\nAnswer: {row['answer']}")
        print('Hints: ' + json.dumps(json.loads(row['hints']), ensure_ascii=False))
        print('Check correctness, source, wording, and hints before approving.')
        choice = prompt_choice('[a]pprove / [r]eject / [s]kip / [q]uit: ', ('a', 'r', 's', 'q'))
        if choice == 'q':
            break
        if choice in ('a', 'r'):
            with db:
                db.execute('UPDATE questions SET status=?, reviewed_at=? WHERE course=? AND id=?',
                           ('trusted' if choice == 'a' else 'rejected', now(), course, row['id']))


def study(db, course, topic=None, count=10, shuffle=False):
    require_course(db, course)
    query = "SELECT * FROM questions WHERE course=? AND status='trusted'"
    params = [course]
    if topic:
        query += ' AND topic=?'
        params.append(topic)
    rows = db.execute(query + ' ORDER BY id', params).fetchall()
    if shuffle:
        random.shuffle(rows)
    rows = rows[:count]
    if not rows:
        print('No trusted questions match. Import or add questions, then run review.')
        return
    completed = 0
    for row in rows:
        print(f"\n[{row['id']}] {row['topic']} | {row['kind']}\n{row['question']}")
        print('Type your attempt (one line; use /hint for help or /quit to stop).')
        started = time.monotonic()
        timestamp = now()
        hints = json.loads(row['hints'])
        used = 0
        while True:
            response = input('Your attempt: ').strip()
            if response == '/quit':
                print(f'{completed} attempts saved.')
                return
            if response == '/hint':
                if used < len(hints):
                    print(hints[used])
                    used += 1
                else:
                    print('No more hints available.')
                continue
            if response:
                break
            print('Make an attempt first, or enter "I don’t know".')
        confidence = confidence_prompt()
        seconds = time.monotonic() - started
        print(f"\nANSWER\n{row['answer']}\nSource: {row['source']}")
        correct = prompt_choice('Was your attempt correct? [y/n]: ', ('y', 'n')) == 'y'
        difficulty = prompt_choice('Difficulty [easy/good/hard]: ', ('easy', 'good', 'hard'))
        with db:
            db.execute('''INSERT INTO attempts
                (course,question_id,attempted_at,response,confidence,correct,hints_used,
                 seconds,difficulty,method,question_snapshot) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                (course, row['id'], timestamp, response, confidence, int(correct), used,
                 seconds, difficulty, 'retrieval', json.dumps(dict(row))))
        completed += 1
    print(f'\n{completed} attempts saved. Results are self-assessed.')


def seed_legacy(db):
    course = 'cs205'
    with db:
        db.execute('INSERT OR IGNORE INTO courses VALUES (?,?)', (course, 'CS205 — Discrete Mathematics'))
    rows = []
    for filename in ('decks.json', 'homework.json'):
        for card in json.loads((ROOT / filename).read_text()):
            base = dict(id=card['id'], topic=card['topic'], question=card['question'],
                        answer=card['answer'], source=card.get('source', f"Midterm review p.{card['page']}"))
            rows.append(base)
            if 'practice_question' in card:
                rows.append(dict(id=card['id'] + ' practice', topic=card['topic'],
                                 question=card['practice_question'], answer=card['practice_answer'],
                                 source='Original paired practice from legacy decks.json', kind='transfer'))
    existing = {r[0] for r in db.execute('SELECT id FROM questions WHERE course=?', (course,))}
    rows = [r for r in rows if r['id'] not in existing]
    count = import_questions(db, course, rows, 'legacy') if rows else 0
    print(f'Imported {count} legacy questions into cs205 as pending. Run: review cs205')


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError('must be at least 1')
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default=os.environ.get('ACADEMIA_DB', str(ROOT / 'data' / 'academia.sqlite3')),
                        help='Local database path (or set ACADEMIA_DB)')
    commands = parser.add_subparsers(dest='command', required=True)
    course = commands.add_parser('course', help='Organize independent classes').add_subparsers(dest='action', required=True)
    add_course = course.add_parser('add')
    add_course.add_argument('id')
    add_course.add_argument('name')
    course.add_parser('list')
    commands.add_parser('init', help='Import existing Discrete Math cards into the pending queue')
    imp = commands.add_parser('import', help='Import manual or externally AI-generated JSON into review')
    imp.add_argument('course')
    imp.add_argument('file', type=Path)
    imp.add_argument('--origin', choices=('manual', 'ai'), required=True)
    add = commands.add_parser('add', help='Write a question manually (pending until reviewed)')
    add.add_argument('course')
    add.add_argument('id')
    for name in ('topic', 'question', 'answer', 'source'):
        add.add_argument('--' + name, required=True)
    add.add_argument('--kind', default='recall')
    add.add_argument('--hint', action='append', default=[])
    rev = commands.add_parser('review', help='Inspect and approve or reject pending questions')
    rev.add_argument('course')
    rev.add_argument('--id')
    listing = commands.add_parser('questions', help='List question metadata without answers')
    listing.add_argument('course')
    listing.add_argument('--status', choices=('pending', 'trusted', 'rejected'))
    session = commands.add_parser('study', help='Attempt trusted questions before revealing answers')
    session.add_argument('course')
    session.add_argument('--topic')
    session.add_argument('--count', type=positive, default=10)
    session.add_argument('--shuffle', action='store_true')
    for name in ('history', 'stats', 'export'):
        sub = commands.add_parser(name)
        sub.add_argument('course')
    args = parser.parse_args(argv)
    db = connect(args.db)
    try:
        if args.command == 'course':
            if args.action == 'add':
                with db:
                    db.execute('INSERT INTO courses VALUES (?,?)',
                               (nonempty(args.id, 'id'), nonempty(args.name, 'name')))
                print(f'Created course {args.id}.')
            else:
                for row in db.execute('SELECT * FROM courses ORDER BY id'):
                    print(f"{row['id']}\t{row['name']}")
        elif args.command == 'init':
            seed_legacy(db)
        elif args.command == 'import':
            count = import_questions(db, args.course, json.loads(args.file.read_text()), args.origin)
            print(f'Imported {count} pending questions. Run: review {args.course}')
        elif args.command == 'add':
            row = {k: getattr(args, k) for k in ('id', 'topic', 'question', 'answer', 'source', 'kind')}
            row['hints'] = args.hint
            import_questions(db, args.course, [row], 'manual')
            print(f'Added pending question. Run: review {args.course} --id {args.id}')
        elif args.command == 'review':
            review(db, args.course, args.id)
        elif args.command == 'study':
            study(db, args.course, args.topic, args.count, args.shuffle)
        else:
            require_course(db, args.course)
            if args.command == 'questions':
                for row in db.execute('SELECT * FROM questions WHERE course=? ORDER BY topic,id', (args.course,)):
                    if args.status is None or args.status == row['status']:
                        print(f"{row['id']}\t{row['topic']}\t{row['status']}\t{row['origin']}")
            else:
                rows = db.execute('SELECT * FROM attempts WHERE course=? ORDER BY id', (args.course,)).fetchall()
                if args.command == 'export':
                    print(json.dumps([dict(r) for r in rows], indent=2, ensure_ascii=False))
                elif args.command == 'history':
                    for row in rows:
                        print(f"{row['attempted_at']}\t{row['question_id']}\tcorrect={row['correct']}"
                              f"\tconfidence={row['confidence']}%\thints={row['hints_used']}\t{row['difficulty']}")
                elif not rows:
                    print('No attempts yet.')
                else:
                    n = len(rows)
                    accuracy = sum(r['correct'] for r in rows) / n
                    confidence = sum(r['confidence'] for r in rows) / n / 100
                    brier = sum((r['confidence']/100-r['correct'])**2 for r in rows) / n
                    assisted = sum(r['hints_used'] > 0 for r in rows) / n
                    print(f'Attempts: {n} (self-assessed; includes repeated questions)\n'
                          f'Accuracy: {accuracy:.1%}\nMean confidence: {confidence:.1%}\n'
                          f'Confidence minus accuracy: {confidence-accuracy:+.1%}\n'
                          f'Brier score: {brier:.3f} (lower is better)\nHint-assisted attempts: {assisted:.1%}')
    finally:
        db.close()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nSession stopped; completed attempts are saved.')
    except (ValueError, OSError, sqlite3.Error) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)
