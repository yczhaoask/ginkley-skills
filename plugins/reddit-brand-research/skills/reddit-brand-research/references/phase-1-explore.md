# Phase 1 · Explore: get the product stated clearly

## Purpose

Before touching any data, get the user to state clearly what they are building. Searching communities before you understand the product returns nothing but noise.

Half the value of this phase is not the information you collect — it is that **the user works things out for themselves while answering**. So don't rush to move on.

## Interview discipline

- **One question at a time.** Throw four questions at someone and you get four perfunctory answers.
- **Wait for the answer. Don't answer for them.** Never "what is your product? Let me guess, probably…"
- **Push on vague answers, don't let them slide.** Vague input contaminates everything downstream, all the way to the final positioning.
- **Offer no brand advice during this phase.** Hold off.

## The four required questions

### 1. What is your product?

You need: category, form, core function, and what stage it's at (idea / prototype / already selling).

Vague answer: "A home product."
Push: "Which category specifically? What everyday problem do people use it for?"

### 2. Who do you want to sell it to?

You need: a describable, specific group — not "everyone who needs it."

Vague answer: "Young people."
Push: "What does their life look like? In what situation would they need your product?"

A good answer looks like: "Young families renting in North America, who move often and don't want to buy disposable furniture."

#### When the user genuinely does not know who it's for

Some users cannot answer this — not from vagueness you can push through, but because
they have an idea and no audience in mind yet. That is the type-3 user from the video,
and pushing harder on the same question just produces a guess, which is worse than an
admission.

**Do not stall at Gate 1 and do not invent an audience for them.** Run a short probe
instead: a cheap exploratory pass whose job is to *locate candidate populations*, not to
produce findings.

**How to run it**

1. Pull 3–5 nouns and verbs from their product description — the problem, the object,
   the action. Not brand words, not category jargon they invented.
2. Run **at most three** searches with them. This is a probe, not Phase 2; if you find
   yourself on a fourth, stop and bring back what you have.
3. Read for **who is talking**, not what they conclude. You are looking for clusters of
   people, not for pain points yet.
4. Bring back 2–4 candidate populations, each with one real quote so the user can feel
   the difference between them:

```markdown
## Who showed up when I searched

I searched <terms> and found roughly three groups of people:

**A · <population>** — <one line on who they are and what they were doing>
> "<quote>" — <source>

**B · <population>** — <one line>
> "<quote>" — <source>

**C · <population>** — <one line>
> "<quote>" — <source>

---
Which of these feels closest to who you're building for? If none of them fit, that's
useful too — tell me what's wrong with each and I'll search differently.
```

5. The user picks. **Then go back and finish questions 3 and 4 properly** with that
   population in mind. The probe replaces nothing; it unblocks question 2.

**Three rules that keep the probe from contaminating the study**

- **Probe output is for locating, never for citing.** These searches were designed to
  find people, not to test anything, so nothing from them may appear as evidence in
  Phase 3 or 4. If a probe quote looks important, re-collect it properly in Phase 2.
- **Mark it in the corpus.** Tag probe files `probe/` so they cannot be mistaken for
  Phase 2 collection later.
- **"None of these" is a good outcome.** It means the product does not sit where its
  vocabulary suggests, which is worth knowing before you spend a real round. Ask what
  was wrong with each and search again — but only once more. If a second probe also
  misses, the honest read is that this audience is not in this pool at all; go to
  `references/instruments.md` and pick a different one.

#### When the product has two sides

Marketplaces, platforms, and anything with suppliers and consumers have **two distinct audiences with different pains, different language, and different communities**. Asking "who do you want to sell it to" as one question produces a muddled answer that contaminates the whole research phase — you cannot match communities for two audiences at once.

Split it before profiling anyone:

1. **Name both sides.** "You have supply side X and demand side Y — is that right?"
2. **Ask which side they are actually pushing on right now.** A product that just launched cannot win both sides at once; whichever side is the cold-start bottleneck is the one to research. Ask it plainly: *which side are you actually spending effort acquiring today?*
3. **Profile only that side** with the specificity above. Note the other side in the understanding card as out of scope for this pass.

The user may say both sides matter. They're right, but insist on a priority anyway — the research in Phase 2 has to target one set of communities, and "both" produces a keyword soup that finds neither.

If the two sides get researched eventually, run the whole process twice. The positioning that comes out for suppliers is usually not the positioning that works on consumers, and merging them early loses both.

**Watch for a tension between the sides.** When one side's profile implies a behavior the product asks them to change — an audience described as "people who already publish openly" being asked to adopt a closed model, say — that is not a detail. It is a hypothesis with the power to invalidate the positioning, and it belongs in Phase 2's list of things to test, flagged as founder-derived rather than evidence-derived.

### 3. Which market is your primary one?

You need: a country or region. This directly decides which communities to match and which competitors to look at. Reddit's community ecosystems differ sharply between North America, Europe, and Southeast Asia — you cannot research them as one blur.

### 4. What about this industry are you most unhappy with?

**This is the most important of the four.** It exposes both:

- The user's **real motive** (why they're the one doing this)
- What they believe the **market gap** is (the starting hypothesis for finding opportunities)

Vague answer: "The products out there just aren't great."
Push: "Which specific thing makes you feel they fall short? When you use one yourself, what's the moment that annoys you most?"

## Closing question

**Why are you doing this at all?**

This answer doesn't feed research — it feeds **brand persona** (Phase 4). A founder's reason for doing the thing is often the truest part of the brand.

## Output: product understanding card

Once all four are in, write it back for confirmation:

```markdown
## Product understanding card

**Product**: <category / form / core function / current stage>
**Target audience**: <specific profile + use context>
**Primary market**: <country or region>
**Industry frustration**: <the specific problem they named>
**Reason for doing this**: <motive>

---
Is this right? Anything to correct?
```

**Only move to Phase 2 after the user confirms or corrects it.** That is Gate 1.
