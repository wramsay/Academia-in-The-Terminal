# Academia in the Terminal

An offline retrieval practice CLI for multiple classes. Write questions yourself or import externally AI-generated drafts, review them, then practice recalling answers before revealing them. Python 3.9+; no dependencies, accounts, network access, or paid APIs.

## Get started

```sh
./run.sh init
./run.sh review cs205
./run.sh study cs205 --count 5 --shuffle
```

`init` copies the existing Discrete Math review, paired practice, and homework cards into a **pending** queue without modifying the original files. It is safe to repeat: existing IDs are skipped. Review questions individually against your materials before approving them. Use `q` to leave review whenever you want; you can study the questions already approved.

## Add another class

```sh
./run.sh course add math101 "Calculus I"
./run.sh import math101 examples/questions.json --origin manual
./run.sh review math101
./run.sh study math101 --topic Derivatives
./run.sh course list
```

Use any course ID and topic name. Question IDs are unique within a course, so separate classes can reuse the same IDs.

```sh
./run.sh add cs205 implication-01 --topic Logic \
  --question "When is p implies q false?" \
  --answer "Exactly when p is true and q is false." \
  --source "Lecture on implication" --hint "Consider a broken promise."
./run.sh review cs205 --id implication-01
```

## Hybrid question bank

[Example import format](examples/questions.json): a JSON array with required nonempty `id`, `topic`, `question`, `answer`, and `source` strings; optional `kind` and `hints` (an array of strings).

For AI drafts prepared outside the app:

```sh
./run.sh import math101 /path/to/drafts.json --origin ai
./run.sh questions math101 --status pending
./run.sh review math101
```

Every import and manual addition is pending. Imported approval flags are ignored. Review shows the complete question, answer, source, origin, and hints, then offers approve, reject, skip, or quit. Only approved questions enter study. The app does not check a source's accuracy for you. Fix a rejected draft in your JSON and import it with a new ID; existing IDs are never overwritten. Duplicate IDs or invalid rows reject the entire batch.

## Practice and measure

Study prompts for a written attempt, then confidence from 0–100 **before** showing the answer. Use `/hint` or `/quit`; “I don’t know” is a valid attempt. After reveal, assess correctness and difficulty. Completed attempts are saved immediately; interrupted, unfinished attempts are not recorded. Long proofs can be worked on paper and summarized in the one-line response.

```sh
./run.sh history cs205
./run.sh stats cs205
./run.sh export cs205 > cs205-attempts.json
```

History records responses, UTC timestamps, confidence, correctness, hint use, response time, difficulty, study method, and question snapshots. Stats report self-assessed accuracy, confidence gap, Brier score, and hint use. Repeated and assisted attempts are included; these are descriptive summaries, not proof of retention or learning gains.

Data stays in `data/academia.sqlite3`, ignored by Git. Back up that file while the app is closed; exports contain attempt history, not a complete question-bank backup. Override the location with `ACADEMIA_DB` or `./run.sh --db /path/to/study.sqlite3 ...`. Use one interactive process per database at a time.

The original viewer remains available with `python3 flashcards.py` (including its old flags). It shows answers immediately and does not record attempts; the new default `run.sh` uses the retrieval engine. Original PDFs, JSON files, and builder scripts remain unchanged.

See the [MVP specification and roadmap](docs/MVP.md).

## Tests

```sh
python3 -m unittest discover -s tests -v
```
