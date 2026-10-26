
# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy

The TakeMeter classifier must achieve **at least 80% overall accuracy** on the held-out test set.

**Why this target:**

I want the classifier to correctly identify most r/technology posts while recognizing that factual reports and opinions can sometimes overlap. I chose 80% as a challenging but useful target for a two-label classifier.

---

## 2. Per-label performance

Both `factual_report` and `opinion` must individually achieve an **F1-score of at least 0.70** on the held-out test set.

**Why this target:**

I want TakeMeter to classify both factual reports and opinions reliably instead of performing well on only the most common type of post. This matters because many r/technology submissions are news reports.

---

## 3. Class balance

In `labels.csv`, **neither label may exceed 60%** of the labeled examples.

**Why this target:**

I want both `factual_report` and `opinion` to have enough training examples so the model does not become biased toward the more common category. With 200 posts, this means 80–120 examples per label.

---

## 4. Labeling consistency

Two people independently applying our `factual_report` and `opinion` definitions to the **same 30 r/technology posts** must agree on **at least 24 of the 30 posts (80%)**.

**Why this target:**

I want my label definitions to be clear enough that another person can classify the same technology posts consistently, especially when a news report contains someone else’s opinion. This requires a separate independent labeling check under our taxonomy; the Unit 6 staff-taxonomy agreement task does not measure this criterion.

---

## 5. High-confidence accuracy

Among held-out test predictions where the model’s top predicted class has a confidence score of **at least 0.80**, **at least 85% must be correct**, with **at least 10 such predictions**. If fewer than 10 qualify, the criterion is not met.

**Why this target:**

I want TakeMeter’s high-confidence predictions to be reliable so users can trust classifications when the model is confident about its decision. The evaluation must extract prediction confidence values from model outputs if the notebook does not already report this measure.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
