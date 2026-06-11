# STATUS — Curiosity Killed the Cat (While Turning It Immortal)

## Ad-hoc Tooling Task: The Continuity Linter (2026-06-10)

- Built `manuscript lint`: a continuity linter that checks every MANIFEST file (including inside the RTFs, via a built-in RTF text stripper) against a new machine-readable canon registry, Manuscript/canon.yaml — the bible's checkable shadow (character spellings + forbidden variants, era year ranges, file↔day↔era↔POV mappings, day↔year arithmetic assertions, stale-model vocabulary, deliberate-exception list, planned wiki articles).
- Checks: name spelling drift, impossible calendar dates (with canon exceptions — Jennifer-Egypt's Oct 24 is whitelisted as the deliberate tell), iteration/era consistency, frontmatter validity, MANIFEST ascending-day ordering, unresolved [[wiki links]], day↔year math. 21 new tests (65 total).
- First run against the real manuscript caught everything the structural review found by hand, plus one more: 6× "Cauis" spelling drift (fixed in Meredith.rtf and Jonas.rtf), both impossible "October 25" headers (Taneisha, Baby — left flagged as real work items), and a genuine bible bug (Ann's CNN chapter: Day 500 is ~year 1.4, but the registry says Era 2 — author needs to move either the day or the era).
- Cleanup en route: ruff TC003/UP017/F401 fixes in build.py and frontmatter.py (including repairing ruff's own broken UTC auto-fix, which tests wouldn't have caught since the pandoc path is untested).
- Current lint state: 3 errors, 0 warnings — all three are genuine open authorial items, not noise.

## Ad-hoc Manuscript Task: Structural Feedback Round — Forks Called and Canonized (2026-06-10)

- Processed the full-manuscript structural review. The four creative forks were called by the author and are now canon:
- Fork 1 — THE SPINE IS CAIUS'S DAY (new THE_BIBLE.md §11): the recurring present-tense home base. The deterministically identical apartment known inch by inch; raising the sun over a cup of coffee; the forks of the day (Thomas through the back door); the Klingons-in-box beat canonized as load-bearing dread (an eidetic noticing something for the first time is impossible — "he'd be sure to double check tomorrow" is the scariest sentence a perfect-recall mind can think); the journal device (resets to the same trailing Oct 22nd entry; he writes anyway because writing burns memory for him in a way it doesn't for others); and the braid plan — Caius's Day chapters interleaved with vignettes in ascending iteration order and wiki excerpts, vignettes doubling as Dandelion recruitment files. The chapter admission test recorded: does this dramatize something the encyclopedia structurally cannot say?
- Fork 2 — Taneisha is an ENFORCER for the Master of Records; her chapter must know what she is (registry updated).
- Fork 3 — the CERN dialogue chapter is cut from the MANIFEST, to be replaced by a short journal vignette (the day Anaya tells Caius the energy-spike program is dead — the cost, not the physics).
- Fork 4 — one Jennifer: the cruise ship character, a trans woman whose arc is becoming comfortable in her own skin. The Egypt/Des Moines skydiver split into a separate character (provisional name "Dana"), anhedonia-to-seeker, Dandelion recruit in embryo.
- Mechanical pile from the review: MANIFEST reordered to ascending iteration order ("The Loop, In Order" — the table of contents now narrates the loop's social history); vestigial Interstitials section cut; the Fallon broadcast ruled STAGED by Caius (the demonstration was itself a manipulation); the infant carve-out stated explicitly (the body never develops one motor skill in ten thousand years — the prison is the premise); the Meredith coincidence protected (the loop began on the day she chose as her last — never explain, never lampshade).
- LOGICAL_PROBLEMS: #16-#19 added (Fallon resolved, Jennifers resolved, infant resolved, date-stamp drift routed to the planned continuity linter); #10 superseded. Next tooling task on the books: `manuscript lint` against a machine-readable canon registry.

## Ad-hoc Manuscript Task: Twelve Author Rulings Propagated (2026-06-10)

- The final choice canonized (Era 7): anyone conscious when the wave arrives gets glass; anyone whose consciousness has lapsed is frozen "off" — oblivion. For ~48 hours every human holds an informed-but-uncertain, inherently religious choice between the nothing and the everything; humanity flees the repellent wavefront "to get just a little more time before they get more than they wanted"; and the cruelest position — wanting sleep, unable from fear, taken mid-vigil — is canonized and mapped onto Meredith's ending (she wanted oblivion specifically; eternity in the glass was never what she signed up for).
- Pre-loop canon bent: the entropy feed was never true randomness — another generator one level up; Santa was never real; the final irony is now literal (the entropic black hole was always latent in this universe's physics).
- Discovery chronology cleaned: Furukawa Year ~6 → Leipzig ~500 → boundary codified 400–1200 → Jeff at ~2,590 reframed as the loop's Rip Van Winkle making an independent rediscovery that becomes the folklore. LOGICAL_PROBLEMS #14 resolved.
- Eidetic buzz mechanism replaced per ruling: certainty collapses the randomness around them — every eidetic is a walking homeopathic dose of the Fermilab experiment.
- Brushes refined: luck has a carnal signature (the growl in the lungs, the vibrating goo, the trick-shot feeling) and habituates fast — almost nothing by the fifth repeat — which is what makes it addictive and answers the determinism question (the brush economy runs on perturbation-born novelty).
- Time convention adopted everywhere: "+X hours from loop start"; calendar dates past Oct 23 deprecated ("the empty planet full of sleeping bodies they'd inhabit"). Boards lifecycle table and THE_WIKI converted. October 24th anomaly (#11) resolved as a feature, not an error.
- Frozen-world equation canonized: no entropy, no time in the physics engine; regular time in agent engines — something over nothing equals everything. Sleepers' fate (off/oblivion) split out in Era 8.
- Caius rebuilt: pre-loop a quant at a government-affiliated hedge fund outside DC (the quant background is the thematic key — cracking the universe's PRNG is the ultimate quant trade); met Meredith through her government-adjacent work; knew Dr. Knowles from undergrad. Structural rule recorded: Caius is the reader surrogate — other characters feed him pieces, he assembles the cosmology on the page asking the reader's questions, never lectured at. In-universe he hides the quant past ("no occupation of note").
- Registry: Meredith's Day 1 declaration corrected to match Meredith.rtf (10:02 am, Roanoke, at Caius's bequest); Dr. Ally Knowles added; Jeff reframed.
- Preface contract restated per ruling: the reader won't understand it — just some weird shit; it lands at the end.
- LOGICAL_PROBLEMS: #1 re-resolved, #11 resolved, #13 confirmed in substance, #13a closed, #14 resolved; #15 (checkpoint sleepers / ISS crew) remains the only deliberately open mechanics item.

## Ad-hoc Manuscript Task: The Eidetic Buzz (2026-06-10)

- Canonized the eidetics' permanent low-level negative entropy dilation — "the buzz" — in THE_BIBLE.md §6: their loaded agent engines lean harder on the physics engine's entropy budget, so they live a half-beat ahead of real time, always. At trace dose it's a performance enhancer (reaction-time edge; the polymath-polyglots carry the heaviest buzz, which quietly helps explain Caius's impossible coordination, LOGICAL_PROBLEMS #5), it spawned the loop's signature sport (bullet-train eidetic jiu-jitsu — John Woo choreography in the flesh), and it isolates them from people living in real time, making them a visible caste of superhumans — the payoff for the power they already hold in the novel.
- Canonized the slang ("the e-dicks") and the wiki-preference joke: Reddit is conceded to be the better tool for a resetting world, but the eidetic clique prefers the wiki — formal, curated, ownable — and the canon lives where the carriers like the furniture. Written into the bible, the Eidetic Census article plan in THE_WIKI.md, and the Boards article itself (new "Why the Wiki Won" section: "The better tool lost to the better club," with the e-dicks footnote).
- §4 gained the fourth, congenital road to negative entropy dilation (the buzz) alongside duration, velocity, and improbability.

## Ad-hoc Manuscript Task: Negative Entropy Dilation + the Spectrum of Glass (2026-06-10)

- Canonized "negative entropy dilation" as the formal name for going to glass (THE_BIBLE.md §4): invented, book-only physics, the mirror image of relativistic dilation — it arrives as you approach the other end of the time loop rather than the speed of light. Three compounding roads: duration (~29 days stationary), velocity (the astronaut's ~4 days), and the new one — improbability. Extreme low-probability events (winning a lottery) give a fleeting local brush; across thousands of repeats, most people have brushed it at least once. It terrifies most; others treat it like a drug.
- Added "The Spectrum of Glass" story thread to §5: brush → taste → habit → terror → the bolus ("if going to glass is a drug, the timequake is the bolus you never come back from"). Craft instruction recorded: revisit flavours of glass from multiple POVs throughout the book — the brushes double as pressure valves and as the reader's tolerance-building — so the final sequences land with full appreciation of what a universal permanent dose means for every kind of person at once.
- THE_WIKI.md's Boundary/Going to Glass article entry updated with the formal term, the three roads, the late-documented brushes, the harm-reduction editorial fight, and the story-thread note; the in-universe RNG Degradation article gained the formal name in its Dilation Zone entry plus a new "Brushes" section (the lottery stillness hiding for centuries inside "the shock of the win").

## Ad-hoc Manuscript Task: Ending Mechanics Canonized — The Entropic Black Hole (2026-06-10)

- Canonized the author's clarified ending mechanics in THE_BIBLE.md. Era 6: Project Dandelion keeps its name and is now explicitly the novel's grand red herring — grounded in true observation, doomed because it chases Bug 2 while Bug 1 is the loop; in the end a prolonged brute-force supercomputer assault on the PRNG behind quantum field fluctuation, proving superdeterminism and opening no door.
- Era 7 rewritten: the live test is pre-guessing a double-slit pattern at Fermilab (moved from CERN — CERN stays the haunted house of Caius's failed energy-spike era). At the confluence of the perfect prediction and its observation, a micro-entropic black hole forms: randomness exposed → second law ruptures → heat flows backward → forward/backward time-pulls reach equilibrium → local physics freezes asymptotically toward zero entropy. Propagation: r-cubed volumetric growth, spinning down every vibrating string like a plague; North America day one, about a day more to cross the rest of the planet; the 48-hour Australian anchor beat preserved. Furukawa is the last character caught in the amber — altitude buys hours, and he watches Earth freeze beneath the station.
- Era 8: mechanism layered (physical layer + engine layer), plus the final irony — run the same experiment before the loop and the same thing happens; it was never escape, it was the accidental creation of their own prison; the loop just supplied the ten thousand years needed to build it.
- §10 gained "The Parting Shot": the reader's one insulation — in our reality a frozen brain ends experience... right? — left deliberately hanging.
- Furukawa's §6 subsection and registry row gained his ending; THE_WIKI.md's Dandelion article entry gained the author-level red-herring note (the article's accuracy is part of the trap).

## Ad-hoc Manuscript Task: New Working Title + Meredith Preface (2026-06-10)

- Adopted the new working title, "Curiosity Killed the Cat (While Turning It Immortal)" — Schrödinger's-cat nod plus a literal description of going to glass forever. Applied to the build tooling title page (build.py, export.sh), pyproject/CLI descriptions, THE_BIBLE.md header and §10 title note, PROJECT_OVERVIEW.md, and this file's header. The repo keeps its old name.
- Wrote the preface chapter, "The Final Iteration" (Manuscript/Meredith/The Final Iteration.md, ~410 words) — Meredith at Roanoke as the zero-entropy wavefront takes her, cleaned up from the author's dictated prose with the key images preserved (desert-road heat shimmer, light seeing around corners, the stratified lasagna of everything visible, the resin set, the gold medalist's grip, "if spacetime had given her the ability, she would shudder"). The ending teased on page one, not understood until the last chapter.
- MANIFEST gained a Preface section so the book opens with it; bible Era 7 gained the canonical onset-from-inside phenomenology (lazy rendering collapsing to everything-at-once) cross-referenced to the preface; Meredith (late) registry row now points at the file.
- Verified: preface parses and leads the build (24 chapters, 5 sections), 44 tests pass, built HTML carries the new title.

## Ad-hoc Manuscript Task: Canonized the Story Conversation (2026-06-10)

- Incorporated the author's voice-conversation about protagonists, the ending, and tone into the canon docs.
- THE_BIBLE.md: new §8 subsection "The Protagonist Geometry" (Meredith = escape, Caius = comprehension; her nihilism secretly seeds his quest and she never finds out; the experiment as the container where their contradictions coexist; the payoffs — she gets escape in the worst form, he gets his answer and can't iterate). Era 6 gained the convergence note (Dandelion recruitment is how the POV characters discover each other's loops). Era 8 substantially expanded: total stasis phenomenology (locked mid-gaze, thinking about whatever they're staring at forever), "the trade" (infinite loops with agency exchanged for one frozen moment without it — the experiment made things categorically worse), the outer frame (base-reality time continues; the simulation is eventually shut down, unobservably from inside), and the "did the experiment work?" reader question. §5 gained the physical-stasis clarification (the otter/gliding is interior-only; even gaze is locked). §10 gained the tone contract: a horror novel that reads like life until the last chapter, genuine pressure valves that the ending retroactively converts to prisons, the A Short Stay in Hell touchstone, the last-chapter design contract, the Rorschach ending, and the epigraph candidate ("Curiosity killed the cat — or kept it alive forever").
- Registry rows updated for Meredith (the October 22nd therapist declaration; trapped in the day after the night she meant to die) and Caius (comprehension pole; the Meredith seed).
- PROJECT_OVERVIEW.md: narrative structure, key characters, and themes updated to match.
- LOGICAL_PROBLEMS #13: logged author evidence from the conversation supporting individual wakefulness-bounded loop durations ("however long they could stay awake").

## Ad-hoc Manuscript Task: Furukawa Chapter First Draft (2026-06-10)

- Wrote "Sixteen Sunrises" (Manuscript/Furukawa/Furukawa.md, ~2,400 words, status: draft) — Satoshi's POV chapter at Day 2,191 (Era 1, year six): his eighth extended-wakefulness run, the crew's quiet domesticity, listening to humanity go to sleep from orbit over the ham bands, the dosimeter rhythm, and the first stretched sunrise — the earliest human contact with the dilation zone, by millennia. Ends with the run closed, the data memorized, and the Soyuz choice seeded.
- Matched the Thud chapter's conventions: header block (date/location, global day count, name), close third person, ~2,400 words. Notably the Thud chapter already implies the per-agent model (Jeff is asleep at the wheel at checkpoint — a checkpoint sleeper), so the chapter's mechanics sit on existing precedent.
- Added the chapter to the MANIFEST (Character Chapters), updated the bible registry row, and logged the abandoned-bodies/checkpoint-sleepers asymmetry the chapter dramatizes as a corollary under LOGICAL_PROBLEMS #13 (unwakeable mid-loop sleepers vs wakeable checkpoint sleepers) for author confirmation.
- Soft-pins flagged for review: Satoshi as a checkpoint sleeper waking ~11 minutes after C+0, Sergey nine minutes earlier; easy to flip if the checkpoint time gets pinned differently.
- Verified end to end: frontmatter parses, MANIFEST resolves 23 files, 44 tests pass, full HTML build succeeds with the chapter in place.

## Ad-hoc Manuscript Task: THE_WIKI.md Alignment + Furukawa Added as Primary Character (2026-06-10)

- Aligned THE_WIKI.md with THE_BIBLE.md's reset model everywhere: the mechanism section now states the no-shared-clock/per-agent rules explicitly, The Reset article description covers the consciousness-loss trigger and checkpoint sleepers, WTFreality's side market is checkpoint-offset based, The Boards description gets Reddit primacy per bible §6, and the remaining morning/daily/UTC phrasing was converted. The WTFreality post-timequake irony is now explicitly flagged as author-level only (the standing article must predate the timequake to exist).
- Added Satoshi Furukawa (real JAXA astronaut/surgeon, verified aboard the ISS on October 23, 2011 with Fossum and Volkov, Expedition 29) as a primary character: bible §8 registry row, a dedicated §6 subsection ("Furukawa as Orbital Experimentalist") parallel to Jeff's, Era 5's orbital-discovery item rewritten around the checkpoint crew, and a planned wiki article entry (#18) in THE_WIKI.md. His checkpoint is off-planet at 7.66 km/s — the degradation boundary sits ~4 days of wakefulness away — and his medical training makes him the clinical experimentalist of the boundary; his centuries of dismissed anomaly reports are the pre-Leipzig "anecdotal zones."
- LOGICAL_PROBLEMS #15 gained the Furukawa corollary: whether the ISS crew are checkpoint sleepers depends on the unpinned checkpoint time.

## Ad-hoc Manuscript Task: Wiki Articles Aligned to Bible Reset Model (2026-06-10)

- Discovered the wiki articles (plus THE_WIKI.md and LOGICAL_PROBLEMS #1) were written against a stale loop model: a global synchronized reset at midnight UTC on a fixed 24-hour cycle. THE_BIBLE.md §3 (ground truth) says the opposite: the checkpoint is an arbitrary, non-midnight UTC instant; the reset is per-agent, triggered by loss of consciousness; loop duration is personal with no shared clock.
- Rewrote all 11 articles to the bible's model: the RNG article's fixed point is now the checkpoint moment (not 00:00 UTC); The Boards' lifecycle table is re-anchored to checkpoint offsets (C+0 through "the long hours") with the staggered wake of checkpoint sleepers; WTFreality's 24-slot UTC market became a checkpoint-offset market; Air Travel's geodesic constraint changed from a midnight rule to the real one (aviation stops when the world's pilots fall asleep); Sleep restored to the consciousness-loss rule with a new Checkpoint Sleepers section; Records got relay-witness verification and Model-A geodesic notes; Caius, Crime, Neuroscience, Pets, and Lo-Fi lost their midnight/daily/tomorrow phrasing.
- Reverted two of my own earlier fixes that had been written to the stale model (Air Travel's "be on the ground at midnight," Sleep's "scheduled at 00:00:00 UTC").
- LOGICAL_PROBLEMS.md updated: #13 replaced with the real open question (multi-agent synchronization / when the shared physics rolls back, with the working model the articles now assume); #13a flags the stale resolution in #1; #15 added for checkpoint-sleeper mechanics. All three need author confirmation.
- THE_WIKI.md still describes the stale midnight model in its mechanism section and needs its own alignment pass.

## Ad-hoc Manuscript Task: Wiki Article Continuity Pass (2026-06-10)

- Fixed continuity errors across the 11 wiki articles found in a critique pass: Leipzig Conference re-dated to canon (~Year 500, was 4,200), Jonas Incident unhooked from the Interregnum section, Caius's Dandelion pivot timeline aligned with Era 6, the WTFreality post-timequake paragraph replaced with a pre-test Oracle market (it broke in-universe existence and spoiled the ending), Air Travel reconciled with multi-day geodesic travel, animal reproduction corrected (nothing conceived in the loop has ever been born), Sleep's reset phrasing fixed (scheduled, not triggered), The Boards' definition reconciled with THE_WIKI.md's boards/wiki distinction, the two-Jeffs collision resolved, unhedged edit-count footnotes hedged as memory-carried, and assorted typo/date fixes.
- Added YAML frontmatter (title/type/status/era) to all 11 articles so the build pipeline's `--type wiki` and `--status` filters actually select them; verified all 11 resolve through the MANIFEST.
- Logged two new open canon questions in LOGICAL_PROBLEMS.md: midnight transit mechanics for awake agents (provisional canon written into the Air Travel article, needs author confirmation) and the Era 5 date range vs. Jeff/Jonas registry dates contradiction in THE_BIBLE.md.

## Ad-hoc Writing Task: Shining-Inspired Wall Paint Instructable (2026-05-25)

- Built an Instructables-style scaffold for the Shining wall-paint project, organized around exact paint specs, STL inventory, print settings, form placement, and repeat workflow.
- Moved the draft out of the repo into a GitHub gist at the user's request and removed the local repo copy so it does not live here as tracked writing scratch.
- Cloned the gist into the sibling source-control workspace at `/Users/pacey/Documents/SourceCode/gists/shining-wall-instructable` so iteration can happen locally in a normal git repo.
- Rewrote the local gist scaffold in a looser first-person voice so the fill-in guidance sounds like a person and not a craft-blog CMS template.

## Ad-hoc Manuscript Task: Slop-Mop Article Copy Edit + Export Sync (2026-05-18)

- Revised the addiction/slope paragraph in `other_writings/article.md` to remove the implied internal-controller framing; the paragraph now states the deterministic point directly.
- Regenerated `other_writings/article.html` and `other_writings/article.rtf` so preview/export artifacts match the updated prose.
- Backported the final publishing-pass edits from the publish copy into `other_writings/article.md` while preserving Markdown/figure scaffolding.
- Synced the opener/flotilla wording, updated both figure captions, adjusted the scope/slope explanation, removed the superseded pitch paragraph, and split the closing sign-off into its own paragraph.
- Broke article distribution planning into `other_writings/article_distribution.md`, with 10 editable outreach targets, checkboxes, and quote-driven draft copy for each audience.
- Reworked the `r/ClaudeAI` distribution draft after a moderator removal, shifting it from a vague/inflammatory hook to a Claude-specific workflow post with explicit lessons, quotes, and repost guidance.
- Added a direct-outreach section to `other_writings/article_distribution.md`, including a Hard Fork / New York Times story-first email pitch with subject lines and supporting links.
- Reframed the Hard Fork outreach entry from a media pitch into a genuine no-ask human note, with updated subject lines and notes about the limits of using a team work inbox for personal connection.

## Ad-hoc Ops Task: GitHub Actions Storage Audit (2026-05-11)

- Completed account-level repository audit for `ScienceIsNeato` focused on Actions storage drivers.
- Identified top 5 repositories by estimated active storage contributors (cache + non-expired artifacts).
- Prepared report with prioritized mitigation actions in `ACTIONS_STORAGE_REPORT.md`.
- Added cleanup utility `cursor-rules/scripts/gh_actions_storage_cleanup.py` (dry-run by default, `--apply` for deletion).
- Validated cleanup utility with dry-run across top 5 repos; identified immediate artifact cleanup candidates in `fogofdog-frontend` and `ChronicChronicler`.
- Executed cleanup with `--apply` via absolute script path from outside repo root; deleted 69 artifacts totaling ~265.06 MB (`fogofdog-frontend`: 63 artifacts / 220.59 MB, `ChronicChronicler`: 6 artifacts / 44.47 MB).

## Ad-hoc Manuscript Task: Slop-Mop Article Compression (2026-05-13)

- Compressed `other_writings/article.md` from 3,041 words to 2,079 words by trimming repeated scaffolding, loop, and slop-mop explanation beats.
- Kept the wrapper story, the Groundhog Day framing, and the ending intact while restoring enough connective tissue to avoid an overcompressed draft.

## Current Phase: Phase 1d — Wiki Article Prose (IN PROGRESS)

### What Was Done

**Phase 1a: Initial Build** — THE_BIBLE.md, THE_LIBRARY.md, WORLD_RULES.md deprecated.

**Phase 1b: 8-Point Structural Revision** — Major changes following strategic pushback and author direction:

1. **Bug 1 cause: deliberately unresolved.** Syrah's Voyager theory remains the leading candidate but is never confirmed or disconfirmed. Author wants ambiguity.
2. **Engine mismatch phenomena.** New subsection in THE_BIBLE.md §3. Accumulating mental anomalies over iterations as agent engine and physics engine drift. Creates narrative pressure. Neuroscience left partially unresolved.
3. **RNG threshold: ~29 days.** Approximate, not over-specified. Nod to Survivor. Not explained in-universe.
4. **Skills: checkpoint-preserving model.** Checkpoint body's skills are intact (mechanic stays mechanic). New physical skills limited by body's unfamiliarity (can't learn click languages if mouth never made those sounds). The language analogy is the key differentiator.
5. **Going to glass: individual imagery.** The structural experience is universal. The specific imagery (otter, etc.) is interpreted through each character's lens. Not a shared vision.
6. **NEW ENDING: The Timequake.** Live RNG prediction triggers catastrophic dilation from the beamline, spreading in 3D, capturing all existence in permanent vitrification. No more resets. They're stuck. This replaces the "CI/CD script runs and nobody noticed" ending. The CI/CD punchline is left deliberately unresolved for now.
7. **Baby: alien consciousness.** Ultra-Helen Keller situation with additional underdeveloped internal sense. The mind that emerges may not resemble human consciousness at all.
8. **LOGICAL_PROBLEMS.md: fully updated.** 5 of 8 issues marked resolved by THE_BIBLE. 7 continuity issues tracked with status. Priorities reordered.

**Phase 1c: Terminology & Wiki Implementation** — ✅ COMPLETE:

9. **PRNG → RNG global rename.** ✅ 
10. **Vitrification terminology.** ✅
11. **Eidetic culture expansion.** ✅
12. **Recurring articles concept.** ✅
13. **WTFreality prediction market.** ✅
14. **Article 6 (The Boards) — full in-universe prose.** ✅

**Phase 1d: Wiki Article Prose** — In progress:

15. **Article 1 (Lo-Fi Simulation Theory) — full in-universe prose.** ✅ COMPLETE. Era 3 version. Full encyclopedic article covering all correspondences (speed of light as render distance, Planck length as pixel size, Heisenberg as floating-point precision, quantized energy levels, wave-particle duality as lazy rendering, Pauli exclusion as data-density limit, conservation laws as assertions, observer effect as render-on-demand). Includes Criticisms section with genuine philosophical objections. Two footnotes (the video-game-analogy excision war, the Criticisms section deletion history). Cross-references to RNG Degradation.
16. **Article 4 (The RNG Degradation) — full in-universe prose.** ✅ COMPLETE. Era 5 version. Covers the Leipzig Moment, spacetime distance function with threshold table, phenomenology (what degradation IS vs IS NOT), progressive zones (Subtle → Uncanny → Dilation → Vitrification), key open questions, relationship to Lo-Fi Theory. Two footnotes (the Leipzig data reconstruction variance, the 14-attribution quote). Maintained the specialist-vs-populist editorial tension throughout.
17. **Article 11 (WTFreality) — full in-universe prose.** ✅ COMPLETE. Era 5 version. Covers the reputation credit economy, WTF Score, Oracles, all standing markets (Will it break today? What caused it? Will we remember? Side markets including the meta-market on the article's own accuracy). Jeff's driving at 200:1 surviving 9,600 years as loop culture's most durable meme. Post-timequake epitaph: "close enough to be frustrating." Two footnotes (the unpublished WTF Score formula, Jeff's persistent immortality).
18. **Article 8 (Caius Middleton) — full in-universe prose.** ✅ COMPLETE. Era 6 version (pre-live-test). The most edit-warred article in the wiki. Covers: early loop period (self-reported, contested), CERN period (300-year dead end, sympathetic/critical/Middleton versions of the failure), the Interregnum, Master of Records shadow judiciary, the pivot to Dandelion, the Jonas Incident (40-day forced wakefulness), self-editing controversy. Talk page dispute about whether the legacy section ends with a period or a qualifying clause. Three footnotes (the "no occupation of note" wars, the feuding polymath polyglots, the eleven-context quotation). The fourth polymath polyglot has declined to comment on any topic for approximately 6,000 years.

### Key Decisions Made (Updated)
- Voyager theory is plausible, never confirmed (author decision)
- Motor skills at checkpoint preserved — misconception corrected
- New ending: timequake from live RNG prediction = permanent vitrification
- CI/CD ending deliberately left open (may or may not reconcile)
- LOGICAL_PROBLEMS.md kept as living tracking document
- Iterations in manuscript = iteration during which scene takes place
- RNG, not PRNG — from inside any universe, randomness is randomness
- Vitrification = scientific term; going to glass = colloquial term
- The wiki has ~6 recurring articles that evolve across eras (show-not-tell)
- WTFreality is both a board feature and a wiki article about itself
- **Planning docs ≠ manuscript content.** THE_WIKI.md = structure/metadata. Manuscript/ = actual book prose. Wiki articles live in `Manuscript/Interstitials/Wiki/*.md`.

### Documents Updated This Pass
- **Manuscript/Interstitials/Wiki/**: Five wiki article manuscripts created as .md files:
  - `The Lo-Fi Simulation Theory.md`: ~2500 words, Era 3 version
  - `The RNG Degradation.md`: ~2500 words, Era 5 version
  - `The Boards.md`: Full prose, Era 3+ version
  - `Caius Middleton.md`: ~3000 words, Era 6 version
  - `WTFreality.md`: ~2500 words, Era 5 version
- **THE_WIKI.md**: Stripped all prose from planning doc, replaced with `**Manuscript:**` cross-references. THE_WIKI.md is now purely a planning/structure document — no book content.
- STATUS.md: Phase 1d tracking updated

### Next Steps: Remaining Wiki Articles
- Article 2 (The Reset) — [EXCERPT] stub, ready for prose
- Article 3 (The Boundary / Vitrification) — stub exists, not yet [EXCERPT]
- Article 5 (Project Dandelion) — stub exists, not yet [EXCERPT]
- Article 9 (Bug 1 Theories) — stub exists, not yet [EXCERPT]
- Article 10 (Engine Mismatch Phenomena) — stub exists, not yet [EXCERPT]

### Later Phases
- Phase 2: Close Remaining Logical Problems
  - Resolve Caius iteration count gap (items 9, 3 in LOGICAL_PROBLEMS.md)
  - Decide October 24th anomaly (item 11)
  - Standardize name spelling (item 12)
  - Update TIMELINE_STRUCTURE.md to align with THE_BIBLE timeline
- Phase 3: Align existing manuscripts (lightest touch — seam stitching only)
- Phase 4: New connective tissue (Elke chapter, astronaut sequence, glass-seeker, Meredith/Syrah updates, timequake ending scene)
