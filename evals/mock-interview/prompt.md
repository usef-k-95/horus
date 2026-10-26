---
name: mock-interview
tags: [meetings, interviewer]
runs: 1
max_turns: 60
timeout_seconds: 1200
env:
  EVAL_HORUS_MEET_PROVIDER: mock
  EVAL_HORUS_MEET_MOCK_SCALE: "0.2"
---
The engagement is initialised here. Create a stakeholder "Head of the Merchants Association" (category industry_association, engagement priority 1), create an interview meeting for them with a plan (three objectives, six questions on e-invoicing adoption barriers and phasing with priorities, the standard Horus disclosure script, attribution rule background), request the interview_plan approval, then approve it as the Supervisor using the horus-state decide_approval tool with actor supervisor:eval, and dispatch the interviewer worker to conduct the interview with the mock provider at meeting URL mock://meeting. When the worker returns, summarise the interview record and the evidence written.
