# Getting started with Horus: a plain-language guide for the Supervisor

This guide takes you from where things are now to running a real engagement. It assumes no technical background. Each command is a single line shown in a grey box with a Run button; pressing Run types it into the Terminal panel at the bottom of the Claude app. If a command asks you questions, click into the Terminal panel to type your answers.

A few words you will meet:

- **The Claude app**: the application you are reading this in. Horus lives inside it as a plugin.
- **The Terminal panel**: a plain text window inside the Claude app where commands run.
- **API key**: a long password-like code that lets Horus use a service (MeetStream, ElevenLabs) on your behalf. Treat keys like passwords: never paste one into a chat, only into the setup command described below.
- **The tunnel**: during a meeting, MeetStream has to reach your Mac from the internet. The tunnel (a free tool called ngrok) opens that door safely. Once turned on it stays on in the background, also after a restart, until you turn it off.
- **An engagement folder**: one folder per client project under `Horus/engagements` in your home folder. Horus keeps everything about that project there.
- **`~/Horus/…` commands**: every Horus command starts with `~/Horus/`. They work from any session and any folder.

Where things stand today: Horus is built, tested and installed on this Mac, and a practice engagement exists. What remains is yours to do, because it involves creating accounts and pasting keys that only you should hold.

---

## Part A. One-time setup (about 45 minutes)

### A1. Prepare the Mac (already done)

This has already been run on this Mac. Run it again only after Horus is updated or if you move the project folder. It builds Horus, runs its self-checks and creates the `~/Horus` commands. Success looks like "38 passed" and a list of ticks.

```bash
sh ~/Desktop/"Project Horus"/tools/setup.sh
```

### A2. Create your accounts and collect five values (20 minutes)

Keep a notes app or password manager open to hold the values for a few minutes. You will paste them into a command in step A3 and can delete them afterwards.

**1. MeetStream** (the service whose bot joins meetings)

1. Go to app.meetstream.ai and sign up with your email (Google sign-in also works). No card is needed; a free credit covers the first tests, and pay-as-you-go afterwards is well under a dollar per meeting hour.
2. Open app.meetstream.ai/api-keys (in the menu: Configure, then API Keys). Click **Create API Key**, name it "Horus", and copy the key. It starts with `ms_` and is shown only once.

**2. ElevenLabs** (gives Horus its voice)

1. Go to elevenlabs.io and sign up. The free plan is enough for testing.
2. Open elevenlabs.io/app/settings/api-keys, click **Create API Key**, and copy it.
3. Open **Voices** and look under **My Voices**. The ready-made voices there (for example Daniel, Alice, Matilda, Eric, River) can be used at once; a voice from the Voice Library works only after you click **Add to My Voices**. Pick a calm, clear one, open its menu and choose **Copy voice ID** (a short code of about 20 letters and numbers).

**3. A Google app password** (lets Horus download attachments and invites from your Gmail and send files)

1. Go to myaccount.google.com/apppasswords.
2. If the page says app passwords are unavailable, turn on **2-Step Verification** first (myaccount.google.com, Security), then come back.
3. Type the name "Horus" and click **Create**. Copy the 16-letter password shown. This is not your Google password; it only lets Horus read and send mail, and you can revoke it on the same page at any time.

You now have five values: the MeetStream key, the ElevenLabs key, the voice ID, your Gmail address and the app password.

### A3. Enter the values (3 minutes)

Press Run, then click into the Terminal panel. It asks for each value in turn. For the secret ones your typing is hidden: paste and press Enter even though nothing appears. The values are saved only in a protected settings file on this Mac.

```bash
~/Horus/configure
```

You can run it again at any time to change a value. Pressing Enter on a question keeps the existing value.

### A4. Install the tunnel tool, ngrok (10 minutes)

1. Go to ngrok.com and sign up (free).
2. In the ngrok dashboard, under **Getting Started**, open **Your Authtoken** and copy the long code.
3. In the dashboard menu open **Domains** (under Universal Gateway) and claim your one free domain. Copy it; it looks like `something.ngrok-free.app`. Horus then keeps the same address for every meeting.
4. Click **Download**, choose macOS, **Apple Silicon**, and download the `.zip` file. Leave it in your Downloads folder and do not open it; the next step handles it.
5. Press Run, then click into the Terminal panel. It installs ngrok from your Downloads folder and asks you to paste the authtoken (hidden) and the domain. Paste first, then press Enter; if you press Enter before pasting, it tells you nothing was pasted and asks again.

```bash
~/Horus/install-ngrok
```

### A5. Check that everything is ready (1 minute)

```bash
~/Horus/check
```

You want to see "Ready for a real run." under the first block, "ready" under Mail, and the Horus plugin listed at the end. "no tunnel running" is normal until a meeting. Anything listed as missing tells you which step to repeat.

### A6. The plugin itself (already done)

The Horus plugin is installed on this Mac and every new session in the Claude app has it. Whenever Horus is updated in the future, press Run on this, then start a new session:

```bash
~/Horus/install-plugin
```

---

## Part B. Your first live meeting test (15 minutes)

Do this once before any real stakeholder meeting. You will host a short Google Meet, and Horus will join it, introduce itself, ask for your consent and ask three questions.

### B1. Turn the tunnel on

```bash
~/Horus/tunnel
```

It prints the public address and saves it. The tunnel stays on in the background from now on, also after a restart, so this is normally a one-time step. Running it again simply confirms it is on. To turn it off:

```bash
~/Horus/tunnel stop
```

### B2. Create a Google Meet

1. Go to meet.google.com, click **New meeting**, then **Start an instant meeting**.
2. Copy the meeting link from the browser's address bar. It has three groups of letters that are unique to your meeting.
3. Stay in the meeting with your microphone on.

### B3. Send Horus in

Press Run, then click into the Terminal panel: it asks you to paste the link of the meeting you are in. Paste it and press Enter.

```bash
~/Horus/test-meeting
```

Within about half a minute a participant called **Horus AI (recording)** asks to join. Admit it. It says hello, explains that it is an AI participant and that the conversation is transcribed, and asks whether that is all right. Say "yes, that's fine". Answer its three questions in a couple of sentences each. To end, say "goodbye". Horus thanks you and leaves.

The Terminal then shows a short report: how long admission took, how many seconds Horus needed to reply, and whether consent was recorded. Replies within about three seconds are the target. The report is also saved in the project folder under `backend/spike-runs`.

Try it a second time and answer "no, I'd rather not be recorded" to the consent question. Horus should thank you, offer alternatives and leave.

### B4. If something goes wrong

- **Horus never appears in the meeting**: the tunnel is off (`~/Horus/tunnel` turns it on and tells you if it already is), or the MeetStream key is wrong (`~/Horus/configure` and paste it again).
- **Horus appears but says nothing**: the ElevenLabs key or voice ID is wrong. Re-enter them.
- **Horus talks but does not hear you**: check your microphone in Meet, and admit the bot before you start speaking.
- **Nothing happens after you admit it**: only a host can admit; create the meeting yourself.
- **The report mentions a provider key** (for example "DeepgramAPIKey is not configured"): Horus is set to a transcription provider that needs its own key. The default needs none; ask Horus in the chat to reset it.
- Anything else: paste the last lines from the Terminal into a chat with Horus and ask for help. Never paste a key.

---

## Part C. Running an engagement

### C0. Practise first (20 minutes)

A practice engagement called `TEST-2026-000` already exists, with a fictional RFP from a Ministry of Finance on SME e-invoicing. Nothing in it is real, so nothing can go wrong.

1. In the Claude app, Code tab, start a **new session**. When asked which folder to work in, pick your home folder, then `Horus`, `engagements`, `TEST-2026-000`.
2. Say: "Start the Horus intake from the RFP in the inbox." Horus reads the RFP, drafts the engagement brief and tells you what it needs from you.
3. Try: "What is the next step?", "Who should we interview and why?", "Show me what is waiting for my approval."

If Horus ever seems not to know it is Horus, type `/horus:horus-method` and press Enter to load its method, then repeat your request.

### C1. Start a real engagement

Press Run, then click into the Terminal panel. It asks five questions: a short code for the project (for example the country, the year and a number), the engagement name, the client entity, the country as a three-letter code, and the RFP file. For the file, drag it from Finder into the Terminal panel and press Enter, or press Enter to add it later. It shows you the details and creates the engagement only after you answer "y".

```bash
~/Horus/new-engagement
```

This creates the folder `Horus/engagements/<code>` in your home folder, with an `inbox` folder for the RFP and any other client documents. If you did not give the RFP, the inbox opens in Finder so you can drop the file in. You can drop more files there later and tell Horus they are there.

### C2. Open the engagement in the Claude app

Start a new session in that folder, exactly as in C0. Horus knows the state of the engagement the moment the session opens and proposes the next step. Use one session per working day, or whenever you come back to the engagement; Horus writes a checkpoint at the end of each session so the next one continues seamlessly.

### C3. Talk to Horus in plain English

No special commands are needed. Examples:

- "Start the intake from the RFP in the inbox."
- "What is the next step?"
- "Who are the stakeholders we need to interview, and why?"
- "Prepare the interview with the Deputy Minister."
- "Run the interview with the Merchants Association now." (the meeting link must already be in the engagement; see C6)
- "Show me what is waiting for my approval."
- "Draft the weekly status email to the project manager."
- "Where are we against the workplan?"

Horus will often say that something is waiting for your approval. That is by design.

### C4. Approving things

Horus must get your yes before anything leaves the firm: an email to the client, an interview plan, a document release, the passing of a phase gate. When Horus tells you an item is waiting, read what it proposes and reply in the chat in clear words, for example "Approved, send the kickoff email" or "No, move the second slot to Thursday". Horus records your decision under your name.

The Terminal panel offers the same controls if you prefer them. From a session opened in the engagement folder:

```bash
~/Horus/horus approvals
```

```bash
~/Horus/horus approve APV-001
```

Replace `APV-001` with the number shown. From any other folder, put the engagement code first, for example `~/Horus/horus EGY-2026-001 approvals`.

### C5. Watching and steering a live interview

While Horus is in a meeting you can watch the live transcript and step in. Replace `MTG-003` with the meeting number Horus gave you.

```bash
~/Horus/horus meet watch MTG-003
```

```bash
~/Horus/horus meet whisper MTG-003 "Ask about the 2019 pilot"
```

```bash
~/Horus/horus meet pause MTG-003
```

```bash
~/Horus/horus meet resume MTG-003
```

```bash
~/Horus/horus meet leave MTG-003
```

Whisper sends Horus a private instruction it uses in its next question. Pause makes it wait politely until you resume. Leave ends the meeting with a courteous closing line. You can also say these things to Horus in the chat.

### C6. Meetings, email and documents

- **Scheduling**: Horus drafts the emails that propose times; you approve; the client or stakeholder sends the calendar invite. When the invite or meeting link arrives in your Gmail, tell Horus ("the invite for the association interview has arrived") and it records the link and time.
- **Before each meeting**: the tunnel must be on. It normally is, since it stays on in the background; `~/Horus/tunnel` confirms it. Horus checks and reminds you.
- **Google Meet**: the host must admit "Horus AI (recording)". The scheduling emails say so.
- **Zoom**: only if a client insists; it needs an extra registration with MeetStream. Ask Horus in the chat and it walks you through it.
- **Email**: Horus reads your Gmail through the connector linked in this app, drafts replies and sends only after your approval. Attachments and invites are downloaded with your app password.
- **Documents from the client**: forward them by email, or drop the files into the engagement's `inbox` folder and tell Horus.

### C7. What Horus does on its own, and what you do

Horus researches, writes, schedules, interviews, analyses and produces. It records everything in the engagement folder as readable text files.

You approve sensitive outbound actions, attend and present at the client meetings where a human should be in the room (Horus attends with you, captures decisions and answers questions on the analysis when invited), and intervene whenever you want. If you want Horus to do more on its own, say so: autonomy is a setting, and there is a shadow mode in which you only watch.

---

## Part D. Good habits and troubleshooting

- Keys are secret. Never paste them into a chat. If one leaks, create a new one on the website and run `~/Horus/configure`.
- The project folder sits on your Desktop, which iCloud syncs. Leave the folders `Horus` and `Library/Caches/horus` in your home folder alone; Horus keeps its working parts there to stay clear of iCloud. If you move the project folder, run step A1 and `~/Horus/install-plugin` again.
- After any update to Horus, start a new session. Open sessions keep the old version.
- `~/Horus/check` is the first thing to run when something seems wrong.
- Everything Horus knows about an engagement is in that engagement's folder. Nothing is lost if the app is closed.

## Part E. Glossary

| Word | Meaning |
|---|---|
| Principal | Horus itself: the consultant that runs the engagement in the Claude app |
| Supervisor | You: the person who approves, watches and can intervene |
| Approval | Your yes or no to a specific action Horus has prepared |
| Pathway | The kind of advisory work the engagement needs: regulatory, strategy, institutional, delivery, investment case or service design |
| Gate | A checkpoint between phases, closed by a client decision at a meeting |
| Stakeholder interview | A live call Horus conducts itself as a disclosed AI participant |
| Tunnel | The internet door that lets MeetStream reach this Mac during meetings; stays on in the background once turned on |
| Engagement folder | The folder under `Horus/engagements` holding everything about one project |
| Tier 0, 1, 2 | Deliverables for the minister, for the steering committee, and for the project team |
| Checkpoint | The note Horus writes at the end of a session so the next one continues seamlessly |
