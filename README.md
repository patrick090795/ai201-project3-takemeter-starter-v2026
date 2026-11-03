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

TakeMeter is a text classifier for public gaming discussions collected from Reddit's r/ItsAllAboutGames community. It assigns each example one of three labels: `analysis` (a gaming argument supported by identifiable details), `hot_take` (a confident unsupported gaming claim), or `reaction` (a personal or conversational response). I explored 35 comments from two discussion threads before defining the labels. My dataset now contains 201 unique labeled examples, which I will use to fine-tune and evaluate a small text classifier.

---

## Label Taxonomy

I explored 35 comments from two public r/ItsAllAboutGames discussion threads. The three labels below describe **how the writer communicates**, rather than whether I agree with the gaming opinion. The dataset includes public submissions.

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

**Boundary stress test:** I used AI to generate eight synthetic gaming comments designed to challenge the definitions and completed the interactive classification exercise. These synthetic comments were not used as training examples. I have not reported a score because the exercise results were not saved in the repository.

**Community discussion sources:**

- https://www.reddit.com/r/ItsAllAboutGames/comments/1h8m09j/
- https://www.reddit.com/r/ItsAllAboutGames/comments/1h693y2/

_The taxonomy examples are drawn from exploratory discussions. Some are paraphrases rather than exact comment text; source wording should be checked before the final submission._

## The Dataset

**Where the posts came from:** I gathered 201 unique public submissions from discussions in r/ItsAllAboutGames. I kept the collected texts in one unsplit `labels.csv` file, using exactly the columns `text`, `label`, and `note`.

**How I labelled them:** I assigned 20 labels independently, without AI suggestions, and marked those entries `cold` in the note column. AI helped propose labels for the remaining 180 examples. I personally reviewed and approved all AI-assisted classifications. Those entries are documented as AI-assisted and human-reviewed in the notes.

**Counts per label:**

| Label      |   Count |    Share |
| ---------- | ------: | -------: |
| `analysis` |      81 |    40.3% |
| `hot_take` |      47 |    23.4% |
| `reaction` |      73 |    36.3% |
| **Total**  | **201** | **100%** |

No label exceeds the 60% maximum specified in my acceptance criteria.

**Three hard cases**

**1. Ambiguous game endings (row 20)**

> A game's ending doesn't have to explain everything to be good. Sometimes leaving players with questions makes the story more memorable than tying every detail into a neat conclusion.

**Could have been:** `analysis` or `hot_take`.

**I chose:** `hot_take`. The text offers a reason for the preference but does not identify a concrete example or independently checkable game feature to support the generalization.

**2. Gaming announcement (row 33)**

> You don't need to be EA to hold a lightsaber: Lucasfilm Games opens the Star Wars vault to indie studios!

**Could have been:** `analysis` or `hot_take`.

**I chose:** `hot_take` in the approved dataset. This is a limitation of my taxonomy: the text is primarily an announcement, so neither label fits cleanly. I retained the reviewed classification but would reconsider the taxonomy or collection criteria in a future iteration.

**3. Question inviting a reaction (row 51)**

> Which game made you feel genuinely stupid and did it feel good or terrible?

**Could have been:** `reaction` or `hot_take`.

**I chose:** `reaction` in the approved dataset because the question invites a personal emotional response rather than making an unsupported gaming claim. It is borderline because it asks for a reaction instead of expressing one.

---

## The Training Run

**Base model:** `distilbert-base-uncased` (DistilBERT with a newly initialized three-class sequence-classification head).

**Training environment:** Google Colab running Linux, NVIDIA Tesla T4 GPU (`cuda`), PyTorch `2.11.0+cu130`. I used Colab because Windows Application Control blocked PyTorch and scikit-learn native libraries on my computer. Colab's managed Python environment did not pass the starter script's virtual-environment check, but the training dependencies loaded and the notebook ran successfully.

**Settings:** 3 epochs, learning rate `2e-5`, batch size 16, maximum sequence length 128 tokens, and random seed 42. The model was fine-tuned using the supplied notebook.

**Anything I changed from the defaults, and why:** I kept the default training hyperparameters. I configured the three labels (`analysis`, `hot_take`, `reaction`) and corrected the evaluation confusion-matrix label lookup, which otherwise caused `KeyError: 0` with the name-to-ID mapping. This corrected metric counting; it did not retrain or change the model predictions.

**Split sizes:** 139 training, 31 validation, and 31 held-out test examples (approximately 70/15/15).

| Label      | Training | Validation |   Test |
| ---------- | -------: | ---------: | -----: |
| `analysis` |       55 |         13 |     13 |
| `hot_take` |       33 |          7 |      7 |
| `reaction` |       51 |         11 |     11 |
| **Total**  |  **139** |     **31** | **31** |

**Training and validation:** The model completed all three epochs. The final validation accuracy was 48.39% and macro F1 was approximately 0.309 (final validation loss 1.015374).

**Held-out test results:** Accuracy 48.4%; macro F1 0.309. Per-label F1: `analysis` 0.619, `hot_take` 0.000, `reaction` 0.308. The most-confident third of predictions was 60% accurate, compared with 30% for the least-confident third. These summary confidence figures do not independently establish whether the confidence acceptance criterion was met.

**Observation:** The `hot_take` category had only seven test examples, so its measured F1 may be unstable across seeds. Its F1 of zero and the weaker `reaction` result show areas to diagnose in Unit 6. The original acceptance criteria have not been changed after training. The notebook reported writing `results.json` and `test_split.csv`; both still need to be checked in the GitHub repository before submission.

---

## How I Used AI

**Moment 1 — Taxonomy design**

- **What I asked for:** I asked AI to compare public gaming communities and help identify observable distinctions in r/ItsAllAboutGames discussions.
- **What came back:** Candidate patterns including supported arguments, unsupported judgments, and conversational reactions, followed by eight synthetic boundary-test comments.
- **What I changed:** I chose the three labels `analysis`, `hot_take`, and `reaction`, and clarified that merely using the word “because” does not make a claim supported analysis. The synthetic examples were not added to the dataset.

**Moment 2 — Assisted labeling**

- **What I asked for:** I asked AI to propose labels for the examples I had not labeled independently, using my written definitions.
- **What came back:** Suggested labels and notes flagging ambiguous examples, particularly questions and announcements that do not fit the taxonomy neatly.
- **What I changed:** I personally reviewed and approved the AI-assisted classifications. I preserved the independent labels and documented questionable boundary cases in the Dataset section.

**Pre-labeling disclosure:** Of the 201 examples, 16 were labeled independently (`cold`); 185 were AI-assisted and then human-reviewed and approved. Four of the initial 20 examples were AI-assisted. No synthetic stress-test comments were used as training examples.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.452 | 0.484 | +0.032 |
| Macro F1 | 0.326 | 0.309 | -0.017 |
| F1 — `analysis` | 0.556 | 0.619 | +0.063 |
| F1 — `hot_take` | 0.000 | 0.000 | +0.000 |
| F1 — `reaction` | 0.421 | 0.308 | -0.113 |


**What I predicted before I looked:**

I predicted the general zero-shot baseline would have higher accuracy than my trained model.

**What the gap actually means:**

My prediction was not supported. The trained model had slightly higher accuracy, by about 3.2 percentage points. However, the baseline had higher macro F1 and performed better on reaction. Both models had zero F1 on hot_take, so fine-tuning did not solve that category.

---

## Run Log — Before

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥80% | 48.39% | 48.39% | 54.84% | MISSED |
| 2. Every label F1 | ≥0.70 | Minimum: 0.000 | Minimum: 0.000 | Minimum: 0.000 | MISSED |
| 3. Largest label share | ≤60% | 40.3%* | 40.3%* | 40.3%* | MET* |
| 4. Independent labeling agreement | ≥24/30 | Not measured | Not measured | Not measured | Pending |
| 5. High-confidence accuracy | ≥85% accuracy at confidence ≥0.80, with ≥10 predictions | 0 qualifying; accuracy N/A | 0 qualifying; accuracy N/A | 0 qualifying; accuracy N/A | MISSED |

### Confusion matrix


| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 13 | 0 | 0 |
| **hot_take** | 7 | 0 | 0 |
| **reaction** | 9 | 0 | 2 |

**My biggest off-diagonal number, and what it means:**

The largest confusion was 9 reaction posts classified as analysis, while no analysis posts were classified as reaction. This shows the model favored analysis on this split. 

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

**Agreement rate:** 25 / 30 = **83.33%**

I labeled all 30 posts using the staff taxonomy before comparing my answers with the staff labels. All 30 texts matched. There were five disagreements, reviewed below. My original labels remain unchanged to preserve the comparison.

### 1. Carbon plates and training mileage

**The post:**

> Carbon plates aren't the whole story. My times dropped 2% in the shoes and another 2% the following year in the same pair, when the only thing that changed was going from 35 to 50 miles a week.

**Staff said:** `analysis`  
**I said:** `hot_take`

**My call, and why:** I agree with `analysis`. The writer compares two 2% improvements and an increase from 35 to 50 miles per week to support the argument that shoes alone do not explain the improvement. Under rule 1, these details carry the argument rather than decorate it.

**Which pile:** (a) The rule covered it, but I applied it loosely.

### 2. Marathon non-starters

**The post:**

> Went back through the club results going back to 2012. Every single year the number of people who enter the spring marathon and don't start it sits between 18 and 23 percent. It's not a bad-luck year, it's the base rate.

**Staff said:** `analysis`  
**I said:** `hot_take`

**My call, and why:** I agree with `analysis`. The results since 2012 show a repeated non-start rate of 18–23%. This pattern supports the conclusion that it is normal rather than one unlucky year. Under rule 1, the figures support the reasoning.

**Which pile:** (a) The rule covered it, but I applied it loosely.

### 3. Energy gels before 90 minutes

**The post:**

> If you need a gel before 90 minutes you have a fuelling problem, not an energy problem.

**Staff said:** `hot_take`  
**I said:** `analysis`

**My call, and why:** I agree with `hot_take`. The writer provides no evidence that needing a gel before 90 minutes indicates a fuelling problem. The number is part of the claim, not evidence supporting it. Under rule 1, a number alone does not make a post analysis.

**Which pile:** (a) The rule covered it, but I applied it loosely.

### 4. Enjoying long runs

**The post:**

> Nobody actually enjoys the long run. They enjoy having done it, which is a completely different thing, and the sport would be more honest if it said so.

**Staff said:** `hot_take`  
**I said:** `reaction`

**My call, and why:** I agree with `hot_take`. I initially focused on the feeling of enjoyment, but “Nobody actually enjoys” makes an unsupported claim about all runners. Under rule 2, this is a general claim rather than the writer's immediate personal reaction.

**Which pile:** (a) The rule covered it, but I applied it loosely.

### 5. Repeated injury threads

**The post:**

> Every injury thread on this forum is the same injury and the same three replies.

**Staff said:** `hot_take`  
**I said:** `reaction`

**My call, and why:** I agree with `hot_take`. The writer generalizes about every injury thread without providing examples or evidence. Under rule 2, this is a claim about the forum rather than an immediate personal experience.

**Which pile:** (a) The rule covered it, but I applied it loosely.

### What the pattern in my disagreements tells me

Three disagreements involved the boundary between `analysis` and `hot_take`. I overlooked supporting evidence in two posts and treated an unsupported numerical threshold as evidence in another. The other two disagreements came from confusing general claims with personal reactions.

After reviewing the rules, I placed all five disagreements in pile (a). This suggests I need to apply the evidence and personal-response rules more carefully. It gives me a reason to review similar boundaries in my gaming dataset, but it does not prove that labeling caused the model's errors.

This staff-taxonomy check is separate from acceptance criterion 4, which requires two people to label 30 gaming comments using my own taxonomy.

---

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

       [x] criteria.md has five numbered criteria, each naming a NUMBER
       [x] Each has a reason underneath tied to your data or taxonomy
       [x] labels.csv: 201 rows, text/label/note, ONE file not split
       [x] No label above 70%
       [x] All five unit 5 sections have real content
       [x] Label Taxonomy includes the decision rule for your hardest boundary
       [x] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (generated in Colab; Git commit not yet verified)
       [ ] At least four new commits (verify Git history)
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
