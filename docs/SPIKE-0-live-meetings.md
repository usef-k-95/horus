# Live meetings runbook (MeetStream) — build step 0

| | |
|---|---|
| **Goal** | Horus joins a Google Meet (and, when the client hosts, a Zoom) meeting from a link as a disclosed AI participant, discloses itself, confirms consent, conducts the interview from an approved plan, obeys Supervisor controls, leaves, and writes the meeting facts, evidence and debrief into the engagement state |
| **Provider** | MeetStream (decision 12, revised 26 October 2026). The MeetStream Claude plugin `meetstream-ai-meeting-bot-api` is installed at user scope as the provider's live-tested documentation; its skills are available in any session |
| **Code** | `backend/src/horus_meet/` (adapters `meetstream`, `elevenlabs`, `mock`, `recall`; `audio.py`, `turns.py`, `session.py`, `bridge.py`, `server.py`, `spike.py`, `cli.py`), `plugin/agents/interviewer.md`, `plugin/skills/horus-method/references/live-meetings.md` |
| **Status** | Built and verified against a fake MeetStream that answers the REST calls, opens the control websocket and posts transcript webhooks (`backend/tests/test_meetstream_adapter.py`), plus the mock provider for dry runs. Real runs need the Supervisor's accounts and a tunnel (section 3). |

## 1. What the spike measures

Per reply: `turn_detection_ms` (end of speech to the turn being declared complete), `transcript_lag_ms` (end of speech to the final transcript sentence), `synth_ms` (text to PCM), `playback_start_ms` (first `sendaudio` chunk), `pipeline_ms` (end of speech to first Horus audio, excluding the model). Target: median `pipeline_ms` under 1,500 ms, leaving room for the model inside the 3-second target. Also: admission time, disclosure spoken and posted, consent verdict and words, controls received, state transitions, errors. Each run writes `report.md`, `report.json`, `transcript.jsonl`, `events.jsonl` and `provider-events.jsonl` into `backend/spike-runs/<run>/` (or `meetings/<MTG>/live/` when driven from an engagement).

## 2. Commands (from `backend/`)

```bash
./uvw sync --extra dev
```

```bash
./uvw run pytest
```

```bash
./uvw run horus-meet mock-run --fast
```

```bash
./uvw run horus-meet check-env
```

Real runs:

```bash
./uvw run horus-meet spike "https://meet.google.com/xxx-xxxx-xxx" --platform meet --turns 3
```

```bash
./uvw run horus-meet spike "https://zoom.us/j/…?pwd=…" --platform zoom --turns 3
```

Supervisor controls while a run is live, from a second terminal (the run folder is printed when the spike starts):

```bash
./uvw run horus-meet control backend/spike-runs/<run-folder> whisper "Ask about the 2019 pilot."
```

```bash
./uvw run horus-meet control backend/spike-runs/<run-folder> leave
```

Inside an engagement the same controls are `./uvw run horus meet whisper MTG-007 "…"`, `pause`, `resume`, `takeover`, `leave`, and `./uvw run horus meet watch MTG-007` tails the live transcript.

## 3. What the Supervisor must do

Horus cannot create accounts or enter credentials. These steps are yours; values go only into `backend/.env` (ignored by git). Facts below were verified against MeetStream's documentation and OpenAPI contract on 26 October 2026.

1. **MeetStream account.** Sign up at app.meetstream.ai (self-serve, no card; a small free credit covers the spike; pay-as-you-go is about $0.35 per bot-hour plus $0.10 per hour of transcription). In Configure › API Keys create a key (shown once, starts with `ms_`) and put it in `.env` as `MEETSTREAM_API_KEY`.
2. **Tunnel.** MeetStream must reach this machine: it posts live transcripts and status changes and opens the control websocket. Install ngrok or cloudflared, run `ngrok http 8765` (or `cloudflared tunnel --url http://localhost:8765`), and put the public `https://…` URL in `.env` as `HORUS_MEET_PUBLIC_URL`. Keep it running during meetings. A fixed domain avoids re-editing `.env` each time.
3. **Google Meet.** No setup. The bot asks to join and a host or co-host must admit it, so host test meetings yourself; for client interviews the scheduling email tells the host to expect "Horus AI (recording)". If a workspace blocks anonymous guests, MeetStream's signed-in bots need a Google Workspace account registered in the dashboard (Phase 2).
4. **Zoom (only when the client hosts on Zoom).** Create a Zoom General app with the Meeting SDK enabled in the Zoom App Marketplace and save its Client ID and Secret under MeetStream Integrations › Zoom. Development credentials join only meetings hosted by your own Zoom account; meetings hosted by others require Zoom app review and a ZAK or OBF token endpoint. For the spike, host the Zoom test meeting yourself.
5. **Text-to-speech.** Create an ElevenLabs account and API key, pick a voice and put `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID` in `.env`. Leave `ELEVENLABS_OUTPUT_FORMAT=pcm_24000`; the runtime resamples to the 48 kHz PCM that MeetStream expects.
6. **Mail (for attachments and invites).** In your Google account enable two-step verification and create an app password; put `HORUS_MAIL_USER` and `HORUS_MAIL_APP_PASSWORD` in `.env`. Check with `./uvw run horus-mail check`.
7. **Optional: MeetStream hosted MCP and calendar.** `claude mcp add --transport http meetstream https://mcp.meetstream.ai/mcp --header "Authorization: Bearer $MEETSTREAM_API_KEY"` adds MeetStream's own tools to Claude Code; connecting a Google Calendar in the MeetStream dashboard enables auto-join of invited meetings. Neither is needed for the spike.
8. **Run the protocol.** `./uvw run horus-meet check-env` must say ready. Create a test Meet, join with a microphone, start the spike with the link, admit the bot. When it has spoken its disclosure, answer the consent question out loud; answer each question in two or three sentences; try a `whisper`; end one run with `leave` and another by saying "goodbye". Run once declining consent. Keep the `report.md` files.

## 4. Reading the results

Pass: `success` on Meet (and Zoom if tested), median `pipeline_ms` under 1,500 ms, disclosure spoken and posted, consent recorded, controls honoured, decline handled politely. If `transcript_lag_ms` dominates, the provider's end-of-turn is slow: try `--transcript meetstream_sentence` or `assemblyai_sentence`. If `playback_start_ms` or audio quality is the problem, lower `CHUNK_SECONDS` in the adapter or move to MeetStream's hosted agents (MIA) for the live loop while keeping plan, approval and debrief in Horus. If the bot is not admitted or is blocked, check the Meet host settings and the bot name.

## 5. Running an interview from an engagement

1. Create the `meetings` record with participants, purpose and `plan` (question guide, disclosure script, attribution rule), and `request_approval` with class `interview_plan`; the Supervisor approves with `./uvw run horus approve APV-…`.
2. When the invite arrives, set `join_url` and `scheduled_at` (the scheduling protocol in `plugin/skills/horus-method/references/scheduling-and-email.md`).
3. `/horus:horus-method interview MTG-…` dispatches the `interviewer` worker, which calls `join`, `disclose`, `consent`, the `listen` and `say` loop, `mark` and `leave` on the `horus-meet` server. The runtime refuses to join without the approved plan and refuses to interview before consent is recorded.
4. After the call the interviewer writes evidence, the interview record, open questions, actions and the debrief; the Principal confirms the proposed updates and drafts the follow-up email for approval.

## 6. Provider facts the runtime relies on (verified 26 October 2026)

| Topic | Fact |
|---|---|
| Base URL and auth | `https://api.meetstream.ai/api/v1`; header `Authorization: Token <key>`; a missing key returns 403 |
| Create bot | `POST /bots/create_bot` with `meeting_link`, `bot_name`, `video_required: false`, `audio_required`, `bot_message` (chat text on join), `callback_url`, `live_transcription_required.webhook_url`, `socket_connection_url.websocket_url`, `recording_config.transcript.provider` (one streaming provider: `deepgram_streaming`, `meetstream_streaming`, `assemblyai_streaming`, `meeting_captions`), `recording_config.retention`, `automatic_leave` (waiting room 60 to 600 s on Meet), `custom_attributes`, `Idempotency-Key` header; response `{bot_id, transcript_id, status}` |
| Live transcript | HTTP POST to our webhook, sentence mode: `{bot_id, speakerName, speakerId, timestamp, transcript, words[], end_of_turn, …}`; about one to two seconds after speech; unsigned, not retried |
| Speaking | Over the control websocket MeetStream opens to us: `{"command": "sendaudio", "audiochunk": <base64 PCM16 LE 48 kHz mono>, "sample_rate": 48000, "encoding": "pcm16", "channels": 1, "endianness": "little"}` in 0.5 to 2 s chunks; `interrupt {action: clear_audio_queue}`; `sendmsg`; audio before `bot.inmeeting` is dropped |
| Status | `GET /bots/{id}/status`; callback events `bot.joining`, `bot.in_waiting_room`, `bot.inmeeting`, `bot.recording`, `bot.leaving`, `bot.stopped`, `bot.kicked`, `bot.denied`, `bot.notallowed`, `bot.failed`, `bot.done`; compare case-insensitively |
| Chat | `POST /bots/{id}/send_message {"message"}` (30 per minute per bot); post-call `GET /bots/{id}/get_chats` |
| Leave and data | `POST /bots/{id}/remove_bot`, `GET /bots/{id}/stop_status`; `GET /transcript/{transcript_id}/get_transcript`; `DELETE /bots/{id}/delete` for erasure; retention set per bot |
| Calendar | Join-only: connect Google or Outlook calendars with your own OAuth client, list events, schedule or auto-schedule bots; MeetStream cannot create meetings or links |
| Zoom | Firm's own Zoom General app with Meeting SDK registered in MeetStream; external hosts need Zoom review and ZAK or OBF tokens; the host must allow recording or the bot leaves |
| Google Meet | Anonymous bot asks to join; a host admits; signed-in bots via registered Workspace accounts |
| Alternatives kept | Recall.ai adapter (`HORUS_MEET_PROVIDER=recall`); MeetStream MIA hosted agents for a lower-latency live loop |
