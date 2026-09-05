# Group 1 video plan — "We Are Group 1"

Format: Nabil records a talking-head master on a tripod, then video-calls each
member live (or drops in their pre-recorded cam / photo + audio). One host,
four call-ins, live test run, shout-outs, chained outro.

Target runtime: 3:30 max. The brief allows 2-3 minutes per member, but this is
one stitched video hosted by Nabil, so keep the total tight.

---

## Master script (Nabil, on camera)

### 0. Cold open (0:00-0:20)
On camera, project logo or the GridScript prompt on screen behind you:

> "We built GridScript, a small programming language with its own lexer,
> parser, and interpreter, for CSC4207. I'm Nabil, I handled the interpreter.
> Let me show you how we each built it, and how it maps to what we learned
> in lecture."

### 1. Your segment: interpreter (0:20-1:10)

Show, don't tell:

- 3 seconds on lecture slide (operational semantics / big-step evaluation)
- Cut to screen: `python3 gridscript.py tests/valid/patrol.gsc` running
- Back to talking head:

> "The interpreter walks the parse tree and applies one evaluation rule per
> construct, exactly like the big-step semantics rules from the lecture
> slides. If a rule fails at runtime, like adding a string to a number, the
> interpreter raises a type error. Watch."

Cut to screen: `python3 gridscript.py tests/invalid/type_error_add.gsc`

> "That's dynamic typing with runtime type checks, straight from the type
> systems lecture."

Transition: "But none of that runs without a parser. Ahmad, you're on."
Dial Ahmad.

### 2. Ahmad Auwal: parser (video call) (1:10-1:50)

Ask Ahmad: "Ahmad, what did you build, and which lecture topic is it?"

Ahmad answers (rehearsed, ~30s):

> "I built the parser. It's a recursive descent parser, one function per
> rule in the BNF grammar. That's the context-free grammar topic from
> lecture: each grammar rule became a function in the code. Precedence
> comes from the grammar levels, so 2 + 3 * 4 evaluates to 14, not 20."

If asked to demo, run: `python3 gridscript.py --ast tests/valid/scale.gsc`

### 3. Abubakar Muhammad Sulaiman: lexer (video call) (1:50-2:20)

Ask: "Abubakar, how does the source code become tokens?"

> "I built the lexer. It uses the regular expressions from the automata
> lecture. Numbers match `[0-9]+`, identifiers match
> `[a-zA-Z_][a-zA-Z0-9_]*`, and keywords are matched first from a reserved
> table. Maximal munch means the lexer always takes the longest match."

Optional demo: `python3 gridscript.py --tokens tests/valid/patrol.gsc`

### 4. Rukayya: AST + scoping (video call) (2:20-2:50)

Ask: "Rukayya, what happens to scope inside a function?"

> "I worked on the AST and the environment model. Only function calls
> create a new scope, and assignment always writes to the current scope.
> That's static scoping from the names and binding lecture. Here's the
> proof: a function that assigns x still leaves the global x untouched."

Demo: `python3 gridscript.py tests/valid/shadowing.gsc` (100 / 7 / 100)

### 5. Muhammad Salisu: tests + report (video call) (2:50-3:10)

Ask: "Salisu, how do we know it all works?"

> "I wrote the test suite. Valid programs are checked against expected
> output, invalid programs must fail with the exact error message. 61 unit
> tests, 17 integration tests, all passing. I also assembled the report."

Cut to Nabil's machine: `python3 run_tests.py` (17/17 PASS screenshot)

### 6. Shout-outs (3:10-3:25)

Nabil, on camera, one line each:

> "Ahmad owned the parser. Abubakar owned the lexer. Rukayya owned the
> scope model. Salisu owned the tests and the report."

### 7. Outro chain (3:25-3:40)

Each member recorded separately, close-up, one word each:

| Member | Says |
|---|---|
| Nabil | "We" |
| Ahmad | "we" |
| Rukayya | "are" |
| Abubakar | "grou" |
| Muhammad | "p" |

Edit: hard cut on each word, talking head switches with each cut, grid
split-screen on the final "p" if time allows. End card: all five names and
UG numbers, group 1, CSC4207.

---

## Recording checklist

- Nabil: tripod, camera at eye level, window light in front of you, dark
  plain background. Terminal font 18+, dark theme.
- Members on call: record the call locally on both sides (OBS or your
  editor's screen-share recording) so you get clean audio.
- Members who cannot record: collect a photo + a voice note of their lines,
  animate the photo to the audio in the edit.
- Collect every member's outro word in the same call, loud and clear, one
  take per word.
- Deliverables per member before edit: their line recording (or voice note
  + photo), and their outro word.

## Edit checklist

- Cut call-ins to the answer only; keep the question audio low under it.
- Screen recordings: zoom 120% on the terminal, cursor highlight on.
- Captions for every spoken line (many markers watch muted first).
- End card: names + UG numbers + "Group 1", CSC4207, 2026.
- Export 1080p, under 4 minutes total.
