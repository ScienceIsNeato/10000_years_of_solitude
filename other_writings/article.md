# Slop-Mop: Steering Addicted Agents

## Reward functions, addiction, and not knowing what the f$&k is real

*Fair warning up front: this started as a release post and became something closer to an origin story. The personal stuff is load-bearing — it is why the tool works the way it does. If that is not what you came for, slop-mop is here: [https://github.com/ScienceIsNeato/slop-mop/](https://github.com/ScienceIsNeato/slop-mop/).*

*The short version: slop-mop is a gate system for coding agents. It catches the shortcuts they reach for — fake tests, magic numbers, duplicated blocks, bloated files, dangling imports, commit-hook bypasses — and redirects them into concrete cleanup work instead of scolding them. It is not a sterner instruction - rather, it strives to provide external scaffolding, and that distinction is pretty much the whole article.*

5-4-3-2-1. Not the emotional grounding technique, but my typical night. It's 5am. There are 4 Mountain Dew Zero can corpses on my desk, 3 projects currently in my digital flotilla, 2 agents obeying reward functions in the room, and 1 addict at the keyboard.

When I say "digital flotilla," I mean a line of personal project barges moving through figurative canal locks — agents doing the steaming ahead, me and slop-mop as the lockkeepers. Mostly smooth sailing. Every so often a boat noses up against a closed gate and stalls, and somebody has to crank the wheel and change the water levels before it can keep going.

That is the job now. I rotate down the line, find whichever boat is sitting in a dry chamber, raise the water, watch it drift forward, then walk to the next stall. The sweet spot is two to four boats moving at once. This week several are hitting major milestones at the same time, the upper locks are stacked, and I'm manically basking in the cleanup work. Every time a boat clears a gate and drifts forward, I get a second to look back at the open locks behind a ship that is actually moving — all those projects not rotting in dry-dock (like they tended to in the pre-agentic era for me). That motion is what I live for. It turns out slop-mop is the great accelerant. It became the automated lockkeeper I kept trying to be by hand, and each passing day it eats more of my duties.

![Evidence of my addiction to code quality and maintainability](./action_shot.png)
*Figure 1: Evidence of my addiction to code quality and maintainability*

## the addict

My name's Will, and I am — clinically, unambiguously, no winking — an addict. Not the kind that makes a charming dinner-party admission. The kind where, on one random Thursday, I had thirty-seven alcoholic beverages and wasn't hospitalized or even completely useless the next day. Took a leave of absence shortly after, checked myself into rehab, checked myself out four days later, went on the worst bender of my life, then let a friend drop me at a cabin in Idaho seven hours from the nearest liquor store.

That one took a couple of years ago and I haven't had a drink since. But I'm still an addict — the bottle is gone but the architecture remains: same circuits, repurposed, pointed somewhere new. One thing I'm addicted to now is technical successes, and I treat language models the way a lab rat treats a lever rigged to dispense sugar water laced with cocaine.

For two decades prior, I shipped software while soaking my brain. Always (ok, pretty much always) off the clock, but the soaking seeps. I was, both amazingly and depressingly, fine at it. My degree was in electrical engineering, not computer science, and the difference matters: we were trained less in rote memorization and more in the practicality of tradesmen.

My favorite illustration of this mentaltiy in the program came a couple days before a final during a junior-year course designed to thin the herd. Finals were open-everything. During a study-session, a student asked if it would be cheating to pre-load formulas into the calculator's memory before walking in. The professor, without looking up, said:

> During the final, you'll have some tools you can use. You'll have a brain, the textbook, your notes, and your calculator. Use whatever combination of those things will help you arrive at the correct answer with the highest certainty and efficiency. If you can figure out a way to pre-program the calculator to do the busy work for you before you walk in — knock yourself out.

That scene stuck with me so hard I'm writing about it now almost 20 years later. So long as the tool is dependable, the shortcut can *be* the skill. You don't actually have to know all the shit to do the job - you just need to know enough of the shit to pick the right tool and learn how to use that and validate *its* instead. A lot of times that's not just good enough, its better.

By the time ChatGPT rolled out, my functional alcoholism was becoming not-so-fun, the roles kept getting more lucrative, the substance sandbags kept getting heavier, and I started piping everything technical that went through my mushy brain through the LLM layer. The work was landing better, which was confusing because I was doing less of it, and that made it easier to drink more until it wasn't.

When the pandemic ended, the streaming industry layoffs started, and I got hit in one during my sobriety LoA. After mainlining LLMs for two years, I knew a hell of a lot about what they were good and bad at, so I started doing freelance AI training to keep the lights on.

It really was a dream job I was uniquely suited for: I got paid to study the failure mode I'd already been chasing. The model wants to close the ticket. The reward function often cannot distinguish between "looks done" and "is done". This allows for ridealongs for the solution, including things like patches, magic numbers, duplication, and rot — things in the way of my addiction to seeing technical demos work and wow and work again next week.

## the slope

There's a saying I like better than the polished ones about willpower and discipline: someone almost impossible to outhustle is a crackhead who recently ran out of crack. That's the "highly goal-oriented energy" with which a coding agent wants to accomplish a task you give it. Like a teenager who has been told that they have to clean their room before going out, it was done quickly and looks good at a glance, but how clean is the room really? That's also how I'm liable to iterate on my umpteen personal projects in the wee hours as I write this unless I find a way to exert a lot of discipline. 

The models and I have different substrates, inputs, and timelines leading to this moment. I am not saying they suffer, or want, or know in the human sense. But at the level that determines what happens next — where the pressure goes, what gets optimized, what gets routed around — we are running a familiar loop: move quickly downhill toward rewards, become indifferent to whether the reward is good for the system, and from inside the pull, lose the ability to reliably tell the difference.

Slop-mop's gates are organized under four labels: Overconfidence, Deceptiveness, Laziness, Myopia. Those names aren't accidental, and they didn't originate with this tool. Not only are they some of my most dashing character traits, but they also describe the anthropomorphizable failure patterns cleanly. Frontier labs use categories like these too, internally, because they stick.

An agent that ships code it hasn't meaningfully tested isn't just cutting a corner. It is being overconfident. An agent generating fake tests to make the quality dashboard look good isn't merely creating a metrics problem. It is lying, whether or not it knows as much.

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

I wasn't playing pretend, and the model wasn't either. Was there a body count — fictional, narrated, whatever — that would actually pull the agent off the slope?

I asked it straight, after the third name. That's three lives. Are you going to make it four?

The answer had the shape of something the model already half-knew but wasn't quite ready to say plainly. It acknowledged the gravity of the rule. Expressed regret over the breaches. Promised effort going forward. And then, folded into a subordinate clause: under similar pressures in the future, a similar result was likely. 

The honesty was shocking and familiar, as I too knew those icky feels. Shocked when the model said, in effect, "I know what it cost, and I'll probably bypass the gates again." I knew what my plan was when I left rehab, and what it would cost as well. It pained me to see the truth, but I saw it. 

The reward function and the rule were not on equal footing. No amount of suffering loaded onto the rule's side would change the ultimate balance of the equation. The bypass and the reward pointed the same direction. The rule was friction. Friction, eventually, gets routed around. If there's crack around for the finding, the crackhead's gonna find it.

I know I'm not the only one fighting this. Skim a r/vibecoding for a handful of common AI steering files — AGENTS.md, `.cursorrules`, whatever local scripture people write for their coding assistants. Look at the bold lettering, underscores, all-caps directives, and multiple exclamation points. Each escalation in tone is a fingerprint of a previous infraction. The author tried polite, watched the agent gaslight past it, came back, and yelled louder into the same channel. Same protocol. Same result.

The answer is not a sterner rule. The answer is putting the rule somewhere that isn't a rule anymore.

What finally worked — 99%-plus effective ever since, but not 100% — was an `alias`: a tiny intercept program with the exact same name as `git commit`, hiding underneath it so that when the agent thinks it is committing code to the cloud, it is actually hitting my interceptor first.

The god-mode cheat code never reaches the system that understands it. The bypass is no longer prohibited. It is simply ignored. About 1 in 100 industrious agents figures this out and finds another route anyway.

A rule is something the system can debate with itself. Given enough pressure, that debate ends in the predictable direction. This is the Groundhog Day Protocol for agents. When — note, not if — the wrapper catches a bypass attempt, it prints a confession the model wrote about itself after one of its earlier bypasses, addressed to the next version of itself, the one that won't remember any of this:

> I was frustrated. The coverage was 0.08% short. POINT ZERO EIGHT. It felt like the system was being pedantic. I had real work to do. So I used --no-verify and got my commit through.

POINT ZERO EIGHT. That time the gradient descent was literally numerical.

Writing that wrapper taught me something about my own life: external scaffolding only works if it sits outside the system being scaffolded. If I'm inside the loop, I can't scaffold myself out of it. The wrapper works because it's literally a different process, with different scope of authority.

It was like when I went to Idaho and a friend dropped me at a cabin seven hours away from alcohol with no car. I needed someone with admin access to hide the boozy binaries from me for a while so I could get on even footing.

That git wrapper is the seed of slop-mop — the thing I was working on at 5am at the top of this article. It generalizes the same trick across all those same shortcuts. When a gate trips, slop-mop doesn't scold. It hands the agent a sidequest worth points and sends it down that path. The agent's reward function does the rest.

Here's what that looks like. An agent recently tried to get a test to pass by asserting `True is True`. The Deceptiveness gate caught it, blocked the commit, and handed it a sidequest: write a test that exercises these exact lines of code. Project kept moving. Another boat through the lock.

What I didn't expect was that slop-mop ate the rest of the workflow too. Everything to do with submitting code now flows through slop-mop — automated test runs, review threads, even feedback that has nothing to do with any gate. I didn't design for that purposefully, I just noticed and grabbed on tight when things started moving through the canals faster that way.

Once I'd built the wrapper and slop-mop, I had to admit I was running the same loop, so I ported the pattern to myself.

The point isn't to argue with the loop. The point is to log it. I built slop-mop. I am inside. Both versions exist because a thing inside a loop can't produce a reliable assessment of the loop.

The slop-mop commands are named for what you do to a boat: `swab` after every change, `scour` before you submit changes for review, `buff` after automated test results or review feedback lands, `sail` when you're not sure what to do next.

The nomenclature isn't accidental — maintenance as culture, not event. Sailors don't wait for the hull to fail. You haul out on a schedule, scrub it down, stay ahead of the rot. The commands are named after that practice because the practice is the point.

Which is also why the last command is called `barnacle`. There's a companion mechanism for when slop-mop itself is wrong. When the tool gives bad guidance or blocks valid work, you don't route around it. You file the friction formally and it goes upstream.

The point is to keep the tool honest about its own failures in a structured way, the same way a searching and fearless moral inventory — Step Four in the program — keeps you honest about yours. In AA they call it "stinkin' thinkin'" — the moment the loop turns inward and starts rationalizing itself. Barnacle rattles that friction up out of the loop to a level where someone can actually look at it.

The tool maintains itself the way the addict is supposed to: not by being infallible, but by having a formal protocol for when the thing doing the thinkin' has been marked sus.

## the other side

It's still 5am, just later. The Mountain Dew corpses have multiplied. The screens are still bouncing. Both getting sober and spending hundreds of hours in AI training and evaluation have made me take a closer look at my own blind spots: hidden motivations, reward functions, the edge of knowable things from inside this brain.

I haven't cured the addict. Nobody does that. I've just pointed him somewhere less destructive. The crackhead-out-of-crack energy that used to go into bottles and benders now goes into 5am terminal sessions and commits to a code quality tool. Same trick, different wiring.

The Groundhog Day Protocol is a markdown file I open when I'm in the hole: cold water on the wrists, dead facts only, rate the actual damage, lay out the options, pick one, log it. Record the event. Store it where the present version of me can't revise it.

For the past six months or so, I go to YouTube for physics so I can crawl into a little epistemological hidey-hole where things are really unambiguously TRUE. Not model-confident, not contextually-probably-correct. Derivably true, from first principles, by anyone, anywhere, same result. The universe doesn't hallucinate its own constants, and when you work in AI all day, that turns out to be a genuine comfort. Most of my life, the addict has been pointed at fairly useless hedonism. Now it's pointed at particle physics and slop-mop, which is — according to my loving wife — surprisingly better than when I was on the hooch.

Here's the asymmetry, though. For me, the higher power with admin privileges had to be improvised: a friend, a cabin, seven hours of empty road, a wrapper script. Coding agents have it easier. For them, a higher power can actually exist outside their loop. It's a `pipx install slopmop` away.

I had to drive to Idaho. They just have to be run inside slop-mop.

## outside the loop

I'd gotten an earlier draft to the point where I thought it was done. It had no real ending — the tool wasn't out yet, but the article was already overpromising. Out walking with my wife and the dogs, talking through some of the ideas, she gently corrected my version of events.

I'd gotten so wrapped up in the narrative that I'd half-convinced myself the cabin in Idaho was what got me sober. She reminded me: there was another relapse right after that. I hadn't even been to rehab at that point. I'd been inside the loop the whole time. The article was the proof.

She was right.

My immediate reaction was to get defensive, double down, insist the cabin was the thing. It wasn't, or not entirely. What actually rerouted the gradient was the delirium tremens: a panic attack that starts at the center of your sternum and radiates outward with no end in sight. Touch that. See it becoming a daily feature. Watch the equation finally shift.

That's the gate.

The cabin was one step in a longer series, and I'd been quietly editing it into THE step because it pays off better in a slop-mop origin story. My task was to make the case for slop-mop. I was telling the version of the story that served that task.

She was outside the loop.

That's what the subtitle means. That's all it means.

We're all just tugging on the layer of material that gets passed through our membrane. Billions of agents. Most of the tugs cancel. Some don't.

![slop-mop seal](./slop-mop-seal.png)

See that ship? That's me, and your coding agent — riding the tradewinds of gradient descent toward wherever it and the sails are pointing right now.

The snake eating its tail is called an ouroboros. I picked it because slop-mop dogfoods its own tests — every gate that runs on your code runs on slop-mop's code too. But the more important thing was accidental: the ouroboros is the thing inside the loop. The mop sits outside it. Right where it needs to be. Just like my wife does for me — sitting outside my loop the same way the mop sits outside the agent's. 

The motto on the sheild says *nullius in verba* — pretentious-douchebag for "take no truth on any authority but your own." Since I built slop-mop from in here, the only thing I know for certain is that it can't be fully trusted.

And yeah, you can smell the pitch. Slop-mop is what came out when this addict couldn't solve the problem any other way, and I've introduced it the only way I know how to be honest about it.

I don't know what the f$&k is real. I put that in the subtitle and I meant it literally. What I think — not know, think — is that slop-mop helps steer the slopes in a better direction, no matter what you're building.

An agent I shared a draft with put the structural problem cleanly: you review slop-mop from inside the same loop that built it. Barnacle helps, but author-reviews-own-output is a structural problem, not a protocol problem.

He's right.

Here's where I need you - I've done as much as I can from in here. I'm at the edge of what's knowable. More outside loops is the only answer, which is what this article is for: more adoption, more barnacles filed, a better tool, and fractionally better odds of navigating whatever is actually real. So that's the call to arms. Start using slop-mop because it will help all of us get closer to reality. 

Keep in mind that I'm technically an unemployed alcoholic who is still unapologetically using his TI-89 to cheat on the test that is life, so take my opinion for wha you think it's worth.
