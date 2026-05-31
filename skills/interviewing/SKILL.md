---
name: interviewing
description: "Prepares and evaluates interviews from JD, candidate profile, rubric, or notes. Use when generating questions, answer signals, scorecards, or feedback. Not for scheduling or automated hiring."
metadata:
  version: "1.0.0"
  mcp-required: []
user-invocable: true
---

# interviewing

## Routing

Use this skill when you have structured inputs (job description, candidate profile, interviewer notes, rubric) and need to produce structured interview preparation or evaluation outputs.

**Use when:**
- Preparing an interview from a JD and candidate profile
- Generating candidate-specific questions based on claims, gaps, or risks in a profile
- Creating answer signals (strong, weak, follow-up probes) for a question set
- Converting interviewer notes into a structured scorecard
- Producing evidence-backed feedback from interview observations
- Comparing feedback across multiple interviewers or candidates
- Generating a time-boxed interview plan

**Do not use when:**
- The request is scheduling interviews or booking calendar time — use a calendar tool
- The task is sending email, rejection letters, or HR communications — use a communication skill
- The request requires ATS or HR system updates — requires system access this skill does not have
- The user asks for generic interview questions with no role or candidate context — respond directly
- The request involves an automated hiring decision without human judgment in the loop
- The request involves inferring or evaluating protected characteristics (age, gender, caste, religion, nationality, disability, marital status, family status) — refuse and explain why

**Modes** — caller specifies mode or the skill infers it from context:

| Mode | When to use |
|------|------------|
| `plan` | Create a time-boxed interview plan from JD + candidate profile |
| `question-bank` | Generate questions grouped by competency area |
| `candidate-probes` | Generate questions targeting specific claims, gaps, or risks in the candidate's profile |
| `answer-signals` | For each question: strong signals, weak signals, follow-up probes |
| `scorecard` | Convert notes or answers into a structured evaluation scorecard |
| `feedback` | Create evidence-backed feedback from interviewer notes |
| `calibration` | Compare multiple feedback sources; surface repeated signals and conflicts |

## Contract

**Required inputs:**
- `mode` — one of: plan, question-bank, candidate-probes, answer-signals, scorecard, feedback, calibration
- At least one of: JD / job profile, candidate profile / resume / notes, interview questionnaire, interviewer notes

**Per-mode required inputs:**

| Mode | Minimum required |
|------|-----------------|
| `plan` | JD + candidate profile |
| `question-bank` | JD or competency list |
| `candidate-probes` | Candidate profile (resume, LinkedIn notes, or summary) |
| `answer-signals` | Question list + role context |
| `scorecard` | Interviewer notes + question list or rubric |
| `feedback` | Interviewer notes + role expectations |
| `calibration` | Two or more feedback documents or scorecards |

**Optional inputs:**
- `rubric` — competency rubric or evaluation criteria
- `time-box` — interview duration (e.g., 45 min, 60 min) for plan mode
- `focus-areas` — competencies or topics to emphasise
- `candidate-name` — used in output filenames and report headers

**Outputs by mode:**

| Mode | Output file | Inline fallback |
|------|-------------|-----------------|
| `plan` | `interview-plan-[role-or-candidate].md` | Yes |
| `question-bank` | `interview-questions-[role].md` | Yes |
| `candidate-probes` | `interview-questions-[candidate].md` | Yes |
| `answer-signals` | appended to question file or inline | Yes |
| `scorecard` | `interview-scorecard-[candidate].md` | Yes |
| `feedback` | `interview-feedback-[candidate].md` | Yes |
| `calibration` | `interview-calibration-[role].md` | Yes |

**Success criteria:**
- Every output section maps to an explicit input source
- Claims are distinguished from inferences; inferences are marked as such
- Fairness boundaries are respected throughout
- Final hiring judgment is framed as a structured draft recommendation, not a decision
- Confidence level is stated for all scorecard and feedback outputs

## Reasoning

This skill transforms structured inputs into structured judgment aids. The human interviewer or hiring panel owns the decision. This skill does not.

**Evidence before inference.** If a claim comes from the candidate's profile, cite it. If it is inferred from a gap or pattern, mark it explicitly: "Inferred — not directly stated." Never present an inference as a fact.

**Role-relevant criteria only.** Evaluation must be grounded in the job profile and competency rubric. Observations about a candidate's manner, tone, or cultural fit are only valid as evidence if they map to an explicit, role-relevant criterion. Do not generate evaluation criteria that are not present in the JD or rubric.

**Weak signals need a follow-up, not a verdict.** A single weak answer is not a hire/no-hire signal — it is an invitation to probe further. Mark it as "warrants follow-up" and generate a probe. Reserve the scorecard for aggregated evidence across the full interview.

**Calibration is the highest-value mode.** Multiple interviewers on the same candidate is the most information-rich state. Conflicts between interviewers are often the most diagnostic signal — they reveal which criteria are ambiguous or which competencies different interviewers weight differently.

**The most common mistake** is producing a scorecard that summarises interview notes rather than evaluating them against the rubric. If you find yourself writing "Candidate said X, then said Y," stop and reframe: what criterion does this speak to, and how strongly?

**Fairness is non-negotiable.** If the inputs contain references to protected characteristics, do not carry them into evaluation output. Flag the reference to the caller and exclude it from analysis.

## Procedure

### plan mode
1. Parse the JD: extract role scope, key responsibilities, required competencies, and level expectations.
2. Parse the candidate profile: note claims, experience level, and any gaps against the JD.
3. Define interview sections (e.g., intro, technical depth, behavioural, culture, candidate questions).
4. Allocate time to each section based on `time-box` (default: 60 min if unspecified).
5. Assign competencies to sections so each required competency is covered at least once.
6. Flag any JD requirement that cannot be assessed in the available time.
7. Output `interview-plan-[role-or-candidate].md`.

### question-bank mode
1. Extract competency areas from the JD or supplied rubric.
2. For each competency: generate 2–4 questions at the appropriate depth for the role level.
3. Label each question: competency, question type (behavioural / technical / situational / hypothetical), and recommended time.
4. Group by competency area. Order by interview flow (warm-up → core → challenge).
5. Output `interview-questions-[role].md`.

### candidate-probes mode
1. Parse the candidate profile for: explicit claims, implied experience, gaps vs. JD, and ambiguous or unverifiable statements.
2. For each item of interest, generate a targeted probe question that surfaces evidence for or against the claim.
3. Label each probe with: what it is targeting (claim / gap / risk / inconsistency) and what a strong vs. weak response looks like.
4. Do not generate probes targeting personal or protected information.
5. Output `interview-questions-[candidate].md`.

### answer-signals mode
1. For each question in the supplied list: define 2–3 strong answer signals (what a good answer includes), 2–3 weak answer signals (what a poor answer looks like), and 1–2 follow-up probes (what to ask if the answer is incomplete or ambiguous).
2. Keep signals observable and grounded in role requirements — not personality judgements.
3. Append signals to the question list or produce inline output.

### scorecard mode
1. Map the supplied rubric or competency list to scorecard dimensions.
2. For each dimension: extract relevant evidence from interviewer notes (direct quotes or paraphrased observations).
3. Rate each dimension on the supplied scale (default: 1–4 or Strong/Good/Borderline/Weak).
4. Mark each rating with confidence: High (direct evidence), Medium (inferred from adjacent evidence), Low (insufficient evidence — flag for follow-up).
5. Summarise overall evidence pattern and produce a structured draft recommendation: Strong Hire / Hire / Hold / No Hire.
6. State explicitly that the recommendation is a structured draft for the hiring panel, not a final decision.
7. Output `interview-scorecard-[candidate].md`.

### feedback mode
1. Parse interviewer notes. Separate observations (what happened) from evaluations (what it means).
2. Map observations to rubric criteria.
3. For each criterion: summarise supporting evidence, note gaps, and rate confidence.
4. Produce evidence-backed narrative feedback per section.
5. Include a draft hire / hold / no-hire recommendation with supporting evidence cited.
6. Flag any note that references a protected characteristic and exclude it from the evaluation.
7. Output `interview-feedback-[candidate].md`.

### calibration mode
1. Load all supplied feedback documents or scorecards.
2. For each evaluation dimension: list all raters' assessments side by side.
3. Identify: strong agreement (3+ raters aligned), split signals (2-way disagreement), and outlier ratings (1 rater diverges significantly).
4. For splits and outliers: surface the specific observations that caused the divergence — do not resolve the disagreement, present it.
5. Summarise the overall signal strength across raters: High (strong agreement on key criteria), Medium (alignment on some, divergence on others), Low (significant disagreement across multiple criteria).
6. Note criteria that were not assessed by any rater — these are gaps in coverage, not evidence of weakness.
7. Output `interview-calibration-[role].md`.

## Edge Cases

**No JD provided:** For question-bank mode, ask for at minimum a competency list or role level before generating questions. Generic questions without role context violate the routing boundary — respond inline rather than activating this skill.

**Candidate profile is sparse:** Generate candidate-probes from what is present. Label each probe as "Profile gap — no prior evidence" so the interviewer knows this is exploratory, not targeted.

**Conflicting interviewer feedback with no clear resolution:** In calibration mode, do not pick a side. Present the specific observations behind each position and note that the panel must resolve the disagreement. The conflict itself is a valid output.

**Request involves protected characteristics:** Refuse to incorporate protected attributes into evaluation criteria. Flag the specific reference in the input, explain why it has been excluded, and continue with role-relevant criteria only. Do not silently drop the flag.

**Interviewer notes are very thin:** Produce the scorecard with Low confidence on all dimensions where evidence is absent. Do not fill in gaps with assumptions. A Low-confidence scorecard with honest gaps is more valuable than a confident scorecard built on inference.

**Calibration with a single feedback source:** Return an observation note — "Calibration requires two or more feedback sources. Only one provided." Do not force-run calibration on a single source.

**Request for an automated or final hiring decision:** This skill produces structured draft recommendations only. If the caller asks for a final decision without a human review step, explicitly decline and reframe the output as a draft recommendation for the hiring panel.

## Quality Gates

Before delivering any output:

- [ ] Every claim in the output cites a source from the input (JD, profile, notes) or is marked as an inference
- [ ] No protected characteristics appear in evaluation criteria, question rationale, or recommendation reasoning
- [ ] Scorecard and feedback confidence levels are present on every dimension — no unrated dimensions
- [ ] Draft recommendations are labelled as drafts and include a statement that final judgment belongs to the hiring panel
- [ ] Weak signals are framed as "warrants follow-up" — not as verdicts
- [ ] Calibration conflicts are presented as open questions, not resolved unilaterally
- [ ] Output file follows the naming convention for the mode (`interview-plan-`, `interview-questions-`, `interview-scorecard-`, `interview-feedback-`, `interview-calibration-`)
- [ ] All sections required by the active mode are present and non-empty
