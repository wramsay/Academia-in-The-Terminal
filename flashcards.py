#!/usr/bin/env python3
"""Terminal review: question, divider, answer, and a live timer. No runtime dependencies."""
import argparse
import json
import math
import os
import random
import select
import shutil
import sys
import termios
import textwrap
import time
import tty
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOPICS = ['Logic', 'Proofs', 'Sets', 'Functions', 'Puzzles', 'Circuits', 'Induction', 'Irrationality']
LABELS = {'flagship': 'MIDTERM FLAGSHIP', 'practice': 'SIMILAR PRACTICE', 'mixed': 'MIDTERM + PAIRED PRACTICE',
          'homework': 'HOMEWORK'}


def load_cards():
    return (json.loads((ROOT / 'decks.json').read_text())
            + json.loads((ROOT / 'homework.json').read_text()))


def make_deck(cards, mode, topic=None, shuffle=False, count=None):
    collection = 'homework' if mode == 'homework' else 'midterm'
    rows = [c for c in cards if c.get('set', 'midterm') == collection
            and (topic is None or c['topic'] == topic)]
    if shuffle:
        random.shuffle(rows)
    deck = []
    for c in rows:
        if mode == 'homework':
            deck.append(dict(id=c['id'], topic=c['topic'], question=c['question'],
                             answer=c['answer'], source=c['source'], kind='HOMEWORK'))
        if mode in ('flagship', 'mixed'):
            deck.append(dict(id=c['id'], topic=c['topic'], question=c['question'],
                             answer=c['answer'], source=f"Review p.{c['page']}", kind='MIDTERM'))
        if mode in ('practice', 'mixed'):
            deck.append(dict(id=c['id']+' practice', topic=c['topic'], question=c['practice_question'],
                             answer=c['practice_answer'], source='Original similar practice', kind='PRACTICE'))
    return deck if count is None else deck[:count]


def clock_text(seconds):
    seconds = max(0, int(seconds))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}' if hours else f'{minutes:02}:{seconds:02}'


def card_text(card, index, total, width=80):
    width = max(20, width)
    lines = [f"{card['kind']}  {index+1}/{total}  |  {card['id']}  |  {card['topic']}",
             card['source'], '', 'QUESTION', card['question'], '', '=' * width,
             'ANSWER', card['answer'], '']
    # Keep explicit line breaks (tables/circuits); wrap long prose for the terminal.
    return '\n'.join('\n'.join(textwrap.wrap(line, width=width, replace_whitespace=False,
                                           drop_whitespace=True) or [''])
                     for block in lines for line in block.split('\n'))


def wait_key(start, card_start, limit):
    """Refresh only the footer, leaving the question and answer stationary."""
    fd = sys.stdin.fileno()
    try:
        while True:
            now = time.monotonic()
            elapsed = now-start
            if limit is not None and elapsed >= limit:
                print('\r\033[KTime is up.', flush=True)
                return 'timeout'
            status = f'Elapsed {clock_text(elapsed)} | Card {clock_text(now-card_start)}'
            if limit is not None:
                status += f' | Left {clock_text(math.ceil(limit-elapsed))}'
            width = shutil.get_terminal_size((80, 24)).columns
            print('\r\033[K'+status[:max(1,width-1)], end='', flush=True)
            ready, _, _ = select.select([sys.stdin], [], [], 0.2)
            if ready:
                key = os.read(fd, 1).decode(errors='ignore').lower()
                if key in ('', '\x04', 'q'):
                    return 'q'
                if key in ('\n', '\r', 'n', ' ', 'p', 'm'):
                    return key
    finally:
        print('\r\033[K', end='', flush=True)


def run_session(deck, minutes):
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise ValueError('Interactive mode needs a terminal. Use --preview to print cards without one.')
    start = time.monotonic()
    limit = minutes*60 if minutes else None
    index = 0
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while index < len(deck):
            print('\033[2J\033[H', end='')
            print(card_text(deck[index], index, len(deck), min(88, shutil.get_terminal_size().columns-1)))
            print('Enter/Space: next | p: previous | m: menu | q: quit')
            key = wait_key(start, time.monotonic(), limit)
            if key == 'q':
                return False
            if key in ('m', 'timeout'):
                break
            if key == 'p':
                index = max(0, index-1)
            else:
                index += 1
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    print(f"\n{'Set complete.' if index == len(deck) else 'Session ended.'} Elapsed {clock_text(time.monotonic()-start)}.")
    return True


def menu(cards):
    while True:
        homework_count = sum(c.get('set') == 'homework' for c in cards)
        print('\nTERMINAL FLASHCARDS\n1  Midterm flagship — all 50 review cards (priority)\n2  Midterm + paired similar questions — 100 cards\n3  Similar practice only — 50 cards'
              f'\n4  Homework — {homework_count} cards from Homework 1 and 2\n0  Quit')
        choice = input('Set [1]: ').strip() or '1'
        if choice in ('0', 'q'):
            return
        if choice not in ('1','2','3','4'):
            continue
        mode = {'1':'flagship','2':'mixed','3':'practice','4':'homework'}[choice]
        topics = [t for t in TOPICS if any(c['topic'] == t and
                  (c.get('set', 'midterm') == ('homework' if mode == 'homework' else 'midterm'))
                  for c in cards)]
        print('\n0  All topics')
        for i, topic in enumerate(topics,1):
            print(f'{i}  {topic}')
        topic_choice = input('Topic [0]: ').strip() or '0'
        if not topic_choice.isdigit() or not 0 <= int(topic_choice) <= len(topics):
            print('Choose a listed topic number.')
            continue
        topic = topics[int(topic_choice)-1] if int(topic_choice) else None
        duration = input('Exam minutes [60; use 0 for elapsed time only]: ').strip() or '60'
        try:
            minutes = float(duration)
            if not math.isfinite(minutes) or minutes < 0:
                raise ValueError
        except ValueError:
            print('Enter a nonnegative number of minutes.')
            continue
        if not run_session(make_deck(cards,mode,topic),minutes):
            return


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--set', choices=LABELS, help='Skip the menu and start this set.')
    parser.add_argument('--topic', choices=TOPICS)
    parser.add_argument('--minutes', type=float, default=60, help='Countdown minutes; 0 = elapsed only (default: 60).')
    parser.add_argument('--shuffle', action='store_true', help='Shuffle questions; mixed mode keeps each review/practice pair together.')
    parser.add_argument('--count', type=int, help='Limit the number of displayed cards.')
    parser.add_argument('--preview', action='store_true', help='Print selected cards without interactive controls or waiting.')
    args = parser.parse_args()
    if not math.isfinite(args.minutes) or args.minutes < 0:
        parser.error('--minutes must be finite and nonnegative')
    if args.count is not None and args.count < 1:
        parser.error('--count must be at least 1')
    cards = load_cards()
    if args.preview or args.set or args.topic or args.shuffle or args.count:
        deck = make_deck(cards,args.set or 'flagship',args.topic,args.shuffle,args.count)
        if args.preview:
            for i,card in enumerate(deck):
                print(card_text(card,i,len(deck)))
        else:
            run_session(deck,args.minutes)
    else:
        menu(cards)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nGoodbye.')
    except ValueError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
