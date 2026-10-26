# PDIA problem deconstruction

Problem-Driven Iterative Adaptation (PDIA) treats capability building as solving locally nominated problems through rapid iteration with broad local authorisation. Horus uses its deconstruction tools and its change-space test rather than its full multi-year programme logic.

When Horus uses this: P1 to P2 on the institutional and operating-model pathway, and whenever a brief asks for a "best practice" solution in a context where previous reforms stalled.

## What it is

Developed by Matt Andrews, Lant Pritchett and Michael Woolcock at Harvard's Center for International Development, PDIA responds to the finding that many public-sector reforms produce "isomorphic mimicry": institutions that look like best practice but do not function. PDIA's four principles are local problem nomination, authorising positive deviance and experimentation, tight feedback loops, and engaging a broad set of agents so the reform is politically viable. Its working tools are the problem construction and deconstruction (a fishbone diagram with repeated "why" questions until causes become entry points), the "triple-A" change space (authority, acceptance, ability), and the crawl of small iterations recorded and reviewed.

## When Horus uses it

- Institutional and operating-model pathway anchor framework: before proposing a target model, the Principal deconstructs why the current institution underperforms and tests where change space exists.
- Transformation and delivery pathway: when the implementation gap is a capability problem rather than a design problem.
- Any pathway when the RFP asks Horus to import a model from another jurisdiction. PDIA is the counterweight to international benchmarking.
- Interview design: the "why" ladder produces interview questions that surface causes rather than complaints.

## Steps

1. **Construct the problem.** State it so that it matters locally and can be measured: what the failure costs, to whom, and what "solved" would look like in observable terms.
2. **Deconstruct.** Build a fishbone: the problem at the head, major cause categories as bones, and under each the specific causes found by asking "why" repeatedly. Stop when a cause is actionable by someone identifiable.
3. **Sequence entry points.** For each actionable cause, assess the change space: authority (who can sanction action), acceptance (who must accept it and will they), ability (people, money, time). Large change space on all three is a quick win; small on all three is parked.
4. **Design iterations.** For the chosen entry points, define a small action, who acts, and what will be learned by when. Weeks, not quarters.
5. **Run and reflect.** After each iteration, record what happened, what was learned, and whether the next step is to continue, adapt or stop.
6. **Expand the coalition.** Use results to enlarge authorisation and acceptance; recruit the agents whose ability is needed next.
7. **Feed the design.** In a Horus engagement the deconstruction and change-space findings feed the operating-model options and the transition plan, which is written as a sequence of iterations rather than a big-bang.

## Outputs → state records

- The fishbone and "why" ladder: an `analyses` record of kind `institutional_diagnostic` or `diagnostic`, with `findings[]` tied to `evidence`.
- Causes as testable statements: `hypotheses` of kind `diagnostic` and `causal`, with `parent` links reflecting the fishbone.
- Change-space assessments: fields on `stakeholders` (`decision_role`, `stance`, `red_lines`) and on `appraisals.feasibility` (`administrative`, `legal`, `political`); the authority dimension maps to RAPID roles.
- Entry points and iterations: `options` of kind `operating_model` or `delivery_intervention` with `variants[]`, and the `analyses` record of kind `implementation_plan` with `sequencing[]` written as iterations.
- Capability findings: `implementation_plan.content.capacity_needs[]`.

## Pitfalls

- Deconstructing to causes outside anyone's reach ("political will"), which produces no entry point. Keep asking why until an actor appears.
- Mistaking the client's preferred solution for the problem; PDIA's first step exists to prevent solution-driven reform.
- Treating the change-space test as a one-off; it shifts after every interview and gate.
- Importing the full PDIA programme logic into a short engagement. Horus uses the tools; the client runs the iterations.
- Using PDIA as a reason to avoid recommending anything specific. The output is still a target model and a sequenced transition, written to allow adaptation.

## Source

Matt Andrews, Lant Pritchett and Michael Woolcock, Building State Capability: Evidence, Analysis, Action, Oxford University Press, 2017; the PDIA Toolkit, Harvard Center for International Development, 2018; the original article "Escaping Capability Traps through Problem Driven Iterative Adaptation", World Development, 2013.
