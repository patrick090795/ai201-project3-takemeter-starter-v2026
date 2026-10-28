# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does


TakeMeter is a text classifier being developed from public discussions in Reddit's r/ItsAllAboutGames community. The intended labels are `analysis` (a supported gaming argument), `hot_take` (a confident unsupported gaming claim), and `reaction` (an immediate response or feeling without a developed argument). For community exploration, I examined 35 comments across two public discussion threads and identified examples and difficult boundaries for these three categories. The next steps are to finalize the unit of analysis, collect and label real examples, and train the classifier.

## Label Taxonomy

I explored 35 comments from two public r/ItsAllAboutGames discussion threads. The three labels below describe **how the writer communicates**, rather than whether I agree with the gaming opinion. These are proposed rules for labeling a consistent unit of text; the exploration used _comments_, while the assignment refers to _posts_. I will confirm that comments are permitted before using them as dataset rows.

### `analysis`

**Definition:** A comment that makes a gaming claim or argument supported by at least one specific, relevant, identifiable fact, gameplay mechanic, example, or comparison that a reader could examine.

**Example 1 (paraphrased from a real discussion):** A player argues that consoles are easier to use than PCs, citing setup and hardware requirements and game compatibility.

**Example 2 (paraphrased from a real discussion):** A player proposes alternative Smash Bros. tournament formats using adjustable stages and items, comparing them with formats in Magic: The Gathering.

### `hot_take`

**Definition:** A comment that makes a confident judgment or general claim about gaming without giving a specific supporting example or piece of evidence.

**Example 1 (short real comment):** "Bethesda titles age like milk. Especially Skyrim."

**Example 2 (paraphrased from a real discussion):** A commenter claims that open-world games waste at least half of players' time without identifying supporting examples.

### `reaction`

**Definition:** A comment whose main purpose is to express an immediate feeling, agreement, disagreement, surprise, or personal response rather than develop an independent gaming argument.

**Example 1 (short real comment):** "That's unpopular... take my upvote."

**Example 2 (short real comment):** "I love this take."

### The hardest boundary

**Which two labels:** `analysis` and `hot_take`.

**Decision rule:** If a writer supports a gaming claim with a _specific, relevant, identifiable_ fact, gameplay mechanic, example, or comparison, use `analysis`, even if the tone is emotional. A confident judgment without that kind of support is `hot_take`. Merely writing "because" or offering another broad assertion does not count as evidence. If the text primarily responds with emotion, agreement, or surprise without developing its own argument, use `reaction`.

**Borderline examples to revisit during labeling:** A player says Skyrim combat feels worse after Dark Souls (`analysis` or `reaction`); a player claims competitive balancing reduces fun (`analysis` or `hot_take`); a player explains leaving Pokemon because of competitive systems (`analysis` or `reaction`).

**Boundary stress test:** I used AI to generate eight synthetic gaming comments designed to challenge the definitions and completed the interactive classification exercise. These synthetic comments are not part of the real-post dataset. I will record any disputed classifications and the resulting clarifications before labeling the 200 examples; I have not included an agreement score because it has not been saved here.

**Community discussion sources:**

- https://www.reddit.com/r/ItsAllAboutGames/comments/1h8m09j/
- https://www.reddit.com/r/ItsAllAboutGames/comments/1h693y2/

## _The examples above are exploratory. Before submission, check the exact comment wording and source links, and confirm with the course that comments qualify as examples when the instructions say posts._

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

**Counts per label:**

| Label     | Count | Share |
| --------- | ----- | ----- |
|           |       |       |
|           |       |       |
|           |       |       |
| **Total** |       | 100%  |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**

> _The post:_
>
> _Could have been:_
>
> _I chose, because:_

**2.**

> _The post:_
>
> _Could have been:_
>
> _I chose, because:_

**3.**

> _The post:_
>
> _Could have been:_
>
> _I chose, because:_

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- _What I asked for:_ I shared r/technology post titles and asked AI to help identify repeated patterns and possible labels for TakeMeter.
- _What came back:_ It suggested categories such as factual reporting, opinion, reaction, and analysis, and compared several borderline headlines.
- _What I changed:_ I settled on two labels (`factual_report` and `opinion`) because the original posts in this community are mostly news submissions and the other categories were difficult to apply consistently.

**Moment 2**

- _What I asked for:_ I asked AI to create eight difficult examples to test the boundary between my labels.
- _What came back:_ Eight fictional headlines and suggested classifications. I initially matched five out of eight.
- _What I changed:_ I clarified my decision rule to distinguish a post reporting another person's opinion from a post advancing the author's own opinion.

**Pre-labelling disclosure:** No real posts have been AI-pre-labeled for `labels.csv` yet. I will disclose any AI-assisted pre-labeling and my manual corrections when collecting the full dataset in Milestone 4.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure          | Baseline | Trained | Difference |
| ---------------- | -------- | ------- | ---------- |
| Overall accuracy |          |         |            |
| Macro F1         |          |         |            |
| F1 — `label_one` |          |         |            |
| F1 — `label_two` |          |         |            |

**What I predicted before I looked:**

<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**

<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |     |     |     |
| ---------------- | --- | --- | --- |
| \*\*\*\*         |     |     |     |
| \*\*\*\*         |     |     |     |
| \*\*\*\*         |     |     |     |

**My biggest off-diagonal number, and what it means:**

<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| #   | Criterion | Target | Verdict | How I decided |
| --- | --------- | ------ | ------- | ------------- |
| 1   |           |        |         |               |
| 2   |           |        |         |               |
| 3   |           |        |         |               |
| 4   |           |        |         |               |
| 5   |           |        |         |               |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** **_ / 30 = _**%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**

> _The post:_
>
> _Staff said / I said:_
>
> _My call, and why:_
>
> _Which pile:_

**2.**

> _The post:_
>
> _Staff said / I said:_
>
> _My call, and why:_
>
> _Which pile:_

**What the pattern in my disagreements tells me:**

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**The gap between what I meant my labels to capture and what the model
learned:**

<!-- Two sentences. Your confusion matrix is the evidence. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
