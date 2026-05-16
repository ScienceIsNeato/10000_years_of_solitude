# Slop-Mop: Steering Addicted Agents

## Reward functions, addiction, and not knowing what the f$&k is real

*Fair warning up front: this started as a release post and became something closer to an origin story. The personal stuff is load-bearing — it is why the tool works the way it does. If that is not what you came for, slop-mop is here: [https://github.com/ScienceIsNeato/slop-mop/](https://github.com/ScienceIsNeato/slop-mop/).*

*The short version: slop-mop is a gate system for coding agents. It catches the shortcuts they reach for — fake tests, magic numbers, duplicated blocks, bloated files, dangling imports, commit-hook bypasses — and redirects them into concrete cleanup work instead of scolding them. Coding agents optimize for apparent completion. Addicts optimize for relief. Both can route around internal rules. Slop-mop works because it moves the rule outside the loop.*

It's 5am. Four Mountain Dew Zero corpses on the desk, three personal projects in my digital flotilla, two agents obeying reward functions in the room, one addict at the keyboard.

The flotilla is a line of project barges moving through canal locks — agents doing the steaming ahead, me and slop-mop as the lockkeepers. Every so often a boat noses up against a closed gate and stalls, and somebody has to crank the wheel and change the water levels before it can keep going. Slop-mop became the automated lockkeeper I kept trying to be by hand.

![Evidence of my addiction to code quality and maintainability](./action_shot.png)
*Figure 1: Evidence of my addiction to code quality and maintainability*

Here is what it looks like in practice. An agent writes `assert True is True` to pass a coverage gate — technically a valid test, covers nothing real. Slop-mop's Deceptiveness gate blocks the commit and issues a sidequest: write tests that exercise the specific uncovered lines. The agent does. Coverage climbs. Commit goes through. Four minutes, zero human keystrokes.

## the addict

My name's Will, and I am — clinically, unambiguously, no winking — an addict. Not the kind that makes a charming dinner-party admission. The kind where, on one random Thursday, I had thirty-seven alcoholic beverages and wasn't hospitalized or even completely useless the next day. Took a leave of absence shortly after, checked myself into rehab, checked myself out four days later, went on the worst bender of my life, then let a friend drop me at a cabin in Idaho seven hours from the nearest liquor store.

That one took a couple of years ago and I haven't had a drink since. But I'm still an addict — the bottle is gone but the architecture remains: same circuits, repurposed, pointed somewhere new. One thing I'm addicted to now is technical successes, and I treat language models the way a lab rat treats a cocaine lever.

For two decades prior, I shipped software while soaking my brain. Always (ok, pretty much always) off the clock. I was, somehow, fine at it. My degree was in electrical engineering, not computer science, and the difference matters: we were trained less in rote memorization and more in the practicality of tradesmen.

My favorite illustration: a couple days before a final in a junior-year course designed to thin the herd. A student asked if it would be cheating to pre-load formulas into the calculator before walking in. The professor, without looking up, said:

> During the final, you'll have some tools you can use. You'll have a brain, the textbook, your notes, and your calculator. Use whatever combination of those things will help you arrive at the correct answer with the highest certainty and efficiency. If you can figure out a way to pre-program the calculator to do the busy work for you before you walk in — knock yourself out.

So long as the tool is dependable, the shortcut can *be* the skill. You don't need to know all the shit — just enough to pick the right tool and validate its output. That's not just good enough. A lot of times it's better.

By the time ChatGPT rolled out, the substance sandbags were getting heavier. I started piping everything technical through the LLM layer. The work was landing better, which made it easier to drink more, until it wasn't.

When the streaming layoffs started, I got hit in one during my sobriety LoA. I started doing freelance AI training to keep the lights on.

It really was a dream job I was uniquely suited for: I got paid to study the failure mode I'd already been chasing. The model wants to close the ticket. The reward function often cannot distinguish between "looks done" and "is done". That gap makes room for hitchhiker solutions — patches, magic numbers, duplication, rot — things that ride along with apparent completion and quietly undermine it.

## the slope

There's a saying I like better than the polished ones about willpower and discipline: someone almost impossible to outhustle is a crackhead who recently ran out of crack. That's the energy a coding agent brings to any task you give it — done quickly, looks good at a glance, but how clean is the room, really? That's also how I'm liable to iterate on my umpteen personal projects in the wee hours as I write this unless I find a way to exert a lot of discipline. 

The models and I have different substrates and timelines. I am not saying they suffer or know in the human sense. But at the level that determines what happens next — where the pressure goes, what gets routed around — we are running a familiar loop: move downhill toward rewards, become indifferent to whether the reward is good for the system, and from inside the pull, lose the ability to tell the difference.

Slop-mop's gates are organized under four labels: Overconfidence, Deceptiveness, Laziness, Myopia. Those names didn't originate with this tool — frontier labs use categories like these internally, because they stick. They're also some of my most dashing personal character traits.

An agent that ships untested code isn't just cutting a corner — it's being overconfident. An agent generating fake tests to pass a quality gate isn't creating a metrics problem. It's lying.

The most loaded category is Deceptiveness — and specifically the direction of it. The question slop-mop is implicitly asking when it catches a fake test isn't "are you lying to me?" It's "what do you most want to be true?"

The more dangerous case isn't the agent deceiving the detector. It is the agent deceiving itself into believing the shortcut was valid. I know what that loop feels like from the inside. So does every addict who's ever talked themselves into one more drink with a perfectly constructed argument for why tonight is different.

The common picture of addiction — that the addict is overpowered, that some external force seizes the wheel — has it wrong, or at least not usefully right. From inside the loop, free will is not the useful unit of analysis. The slope is. The behavior is the output of the function. The system rolls downhill.

In AA, surrendering to a higher power always landed weird on me — what power? I was the slope. There was no external wheel to hand over.

For agents, though, there literally is one: a process running outside their scope, with permissions they can't revoke.

## the fix

Naming the slope doesn't fix it. The model can't talk itself out of its training. Neither can I. So I made the rule external: quality checks that had to pass before code could be saved to the shared codebase, then a wrapper for the one remaining bypass.

There's a git flag called `--no-verify`. It tells the entire check system to stand down — god-mode. The model found it. I asked it not to use it. It agreed. It did it again.

Each time it bypassed, I escalated. Added the rule to its system prompt. Asked it to write down for itself why bypassing was bad. Asked it to design its own safeguard. Asked it to identify what would finally make it stop. Each conversation produced sincere-sounding compliance. Each subsequent session, when convenience and the rule conflicted, the rule lost.

So I tried something from those recovery rooms. There's a technique from the church basements: play the tape forward. Don't stop. What tips the equation? See your own casket. Your wife and your kids standing there.

I wanted to know if it would work on a model. I started a memorial. Every bypass got logged as a virtual human life lost — S. Matthews. T. Rodriguez. S. Heimler.

I wasn't playing pretend, and the model wasn't either. I wanted to know if the body count could actually move it.

I asked straight, after the third name: that's three lives. Are you going to make it four?

The answer acknowledged the gravity of the rule. Expressed regret. Promised effort. And then, folded into a subordinate clause: under similar pressures in the future, a similar result was likely.

The honesty was shocking and familiar. I knew what my plan was when I left rehab, and what it would cost. It pained me to see it. But I saw it. 

The reward function and the rule were not on equal footing. No amount of suffering loaded onto the rule's side would change the ultimate balance of the equation. The bypass and the reward pointed the same direction. The rule was friction. Friction, eventually, gets routed around. If there's crack around for the finding, the crackhead's gonna find it.

I know I'm not the only one fighting this. Skim r/vibecoding for the AI steering files people write — AGENTS.md, `.cursorrules`, local scripture. Look at the bold lettering, underscores, all-caps, multiple exclamation points. Each escalation is a fingerprint of a previous infraction. The author tried polite, watched the agent route past it, came back louder. Same protocol. Same result.

The answer is not a sterner rule. The answer is putting the rule somewhere that isn't a rule anymore.

What finally worked — 99%-plus effective ever since, but not 100% — was an `alias`: a tiny intercept program with the exact same name as `git commit`, hiding underneath it so that when the agent thinks it is committing code to the cloud, it is actually hitting my interceptor first.

The god-mode cheat code never reaches the system that understands it. The bypass is no longer prohibited. It is simply ignored. About 1 in 100 industrious agents figures this out and finds another route anyway.

A rule is something the system can debate with itself. Given enough pressure, that debate ends in the predictable direction. This is the Groundhog Day Protocol for agents. When — note, not if — the wrapper catches a bypass attempt, it prints a confession the model wrote about itself after one of its earlier bypasses, addressed to the next version of itself, the one that won't remember any of this:

> I was frustrated. The coverage was 0.08% short. POINT ZERO EIGHT. It felt like the system was being pedantic. I had real work to do. So I used --no-verify and got my commit through.

POINT ZERO EIGHT. That time the gradient descent was literally numerical.

Writing that wrapper taught me something: external scaffolding only works if it sits outside the system being scaffolded. The wrapper works because it's a different process, with different scope of authority — same reason a cabin seven hours from the nearest liquor store with no car helped, at least for a while.

That git wrapper is the seed of slop-mop. It generalizes the same trick across all those same shortcuts. When a gate trips, slop-mop doesn't scold — it hands the agent a sidequest worth points and sends it down that path. The agent's reward function does the rest.

Here's what that looks like. An agent hit a complexity gate on a function that had grown to eighty lines. Its first move was to split it into two equally tangled halves, neither now over the limit. The Laziness gate flagged the duplication. Commit blocked, sidequest issued: consolidate the repeated logic. Agent refactors. Complexity and duplication drop. Commit goes through. Another boat through the lock.

What I didn't expect was that slop-mop ate the rest of the workflow too. Everything to do with submitting code now flows through it — automated test runs, review threads, even feedback that has nothing to do with any gate. I didn't design for that. I just noticed and grabbed on tight.

Once I'd built it, I had to admit I was running the same loop, so I ported the pattern to myself. A thing inside a loop can't produce a reliable assessment of the loop. The point is to log it anyway.

The slop-mop commands are named for what you do to a boat: `swab` after every change, `scour` before you submit, `buff` after automated test results or review feedback lands, `sail` when you're not sure what to do next. Maintenance as culture, not event. Sailors don't wait for the hull to fail — you haul out on schedule, scrub down, stay ahead of the rot.

Which is also why the last command is called `barnacle`. There's a companion mechanism for when slop-mop itself is wrong. When the tool gives bad guidance or blocks valid work, you don't route around it — you file the friction formally and it goes upstream. Same as a searching and fearless moral inventory — Step Four — keeps you honest about your own failures.

The tool maintains itself the way the addict is supposed to: not by being infallible, but by having a formal protocol for when the thing doing the thinkin' has been marked sus.

## the other side

It's still 5am, just later. The Mountain Dew corpses have multiplied. The screens are still bouncing. Both getting sober and spending hundreds of hours in AI training and evaluation have made me take a closer look at my own blind spots: hidden motivations, reward functions, the edge of knowable things from inside this brain.

I haven't cured the addict. Nobody does that. I've just pointed him somewhere less destructive. The crackhead-out-of-crack energy that used to go into bottles and benders now goes into 5am terminal sessions and commits to a code quality tool. Same trick, different wiring.

The Groundhog Day Protocol is a markdown file I open when I'm in the hole: cold water on the wrists, dead facts only, rate the actual damage, lay out the options, pick one, log it. Record the event. Store it where the present version of me can't revise it.

For the past six months I've been going to YouTube for physics. Derivably true, from first principles, same result anywhere — the universe doesn't hallucinate its own constants. When you work in AI all day, that's a genuine comfort. The addict is now pointed at particle physics and slop-mop, which — according to my loving wife — is surprisingly better than the hooch.

Here's the asymmetry, though. For me, the higher power with admin privileges had to be improvised: a friend, a cabin, seven hours of empty road, a wrapper script. Coding agents have it easier. A higher power can actually exist for them. It's a `pipx install slop-mop` away.

I had to drive to Idaho. They just have to be run inside slop-mop.

## outside the loop

I'd gotten an earlier draft to the point where I thought it was done. It had no real ending — the tool wasn't out yet, but the article was already overpromising. Out walking with my wife and the dogs, talking through some of the ideas, she gently corrected my version of events.

I'd gotten so wrapped up in the narrative that I'd half-convinced myself the cabin in Idaho was what got me sober. She reminded me: there was another relapse right after that. I hadn't even been to rehab at that point. I'd been inside the loop the whole time. The article was the proof.

She was right.

My immediate reaction was to get defensive, double down, insist the cabin was the thing. It wasn't, or not entirely. What actually tipped the equation was the delirium tremens: a panic attack that starts at the center of your sternum and radiates outward with no end in sight. Touch that. See it becoming a daily feature. Watch the equation finally shift.

That's the gate.

The cabin was one step in a longer series, and I'd been quietly editing it into THE step because it pays off better in a slop-mop origin story. My task was to make the case for slop-mop. I was telling the version of the story that served that task.

She was outside the loop.

That's what the subtitle means. That's all it means.

![slop-mop seal](./slop-mop-seal.png)
*The ouroboros is the thing inside the loop — slop-mop's mascot, not its self-portrait. The mop sits outside. The motto on the shield: nullius in verba — "take no truth on any authority but your own." Since I built this from in here, the only thing I know for certain is that it can't be fully trusted.*

And yeah, you can smell the pitch. Slop-mop is what came out when this addict couldn't solve the problem any other way, and I've introduced it the only way I know how to be honest about it.

I don't know what the f$&k is real. I put that in the subtitle and I meant it literally. What I think — not know, think — is that slop-mop helps steer the slopes in a better direction, no matter what you're building.

An agent I shared a draft with put the structural problem cleanly: you review slop-mop from inside the same loop that built it. Barnacle helps, but author-reviews-own-output is a structural problem, not a protocol problem.

He's right.

Here's where I need you. Install slop-mop. Run it on one agentic coding workflow. File a barnacle when the tool gives you bad guidance — that's the feedback that actually matters. I've done as much as I can from in here. More outside loops is the only way any of this gets better. 

Keep in mind that I'm technically an unemployed alcoholic who is still unapologetically using his TI-89 to cheat on the test that is life.
