# Educator Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by educator.

## Patterns

- **Name**: Interactivity-Matched Guidance
- **Description**: Set the level of guidance for each task by its element interactivity (how many new elements a learner must coordinate in working memory at once) relative to the learners' prior knowledge. Low-interactivity material, such as vocabulary pairs, isolated facts, or simple associations, does not threaten working memory, so have learners generate answers, which produces stronger retention than reading them. High-interactivity material, such as multi-step equations, composite-area problems, or causal systems, overwhelms novices who search for a solution by trial and error, so give them complete worked examples and explicit instruction first. Worked examples reliably beat unguided problem solving for novices on this kind of material (a meta-analysis of 55 studies in mathematics found a moderate advantage, g = 0.48).
- **When**: Choosing between explanation, worked examples, and independent practice for any task in a Build, or judging that choice in an Audit.
- **Example**:
```
    Task: solving two-step linear equations; learners: 7th-grade novices.
    Interactivity: high (inverse operations, order, balance, sign handling).
    Design: 2 fully worked examples with each step's reason written beside it,
            then completion problems, then independent problems.
    Contrast: the same class's new vocabulary terms (low interactivity) get
              self-generated definitions and retrieval, not worked examples.
```

---

- **Name**: Guidance Fading Off-Ramp
- **Description**: Move learners from full worked examples to completion problems (with steps removed progressively, starting from the last step) to independent problem solving as their schemas form. Fade as soon as learners show they can supply the removed steps and justify them, because guidance that experienced learners no longer need forces them to reconcile it with what they already know, which costs time and accuracy (the expertise-reversal effect). Fade faster on well-structured procedures, especially with young adults and older adolescents. Fade more slowly on ill-structured tasks such as case analysis or diagnostic reasoning, where the problem space is large and worked case analyses that show expert reasoning stay useful longer.
- **When**: Sequencing practice within a lesson or across a unit, or responding to evidence that learners already know part of the material.
- **Example**:
```
    Session 1: Worked example A (all steps) -> Worked example B (all steps)
    Session 1: Completion problem C (last step blank) -> D (last two blank)
    Session 2: Retrieval warm-up -> Completion E (first step only given)
    Session 2: Independent problems F-H -> self-check against solution key
    Fade trigger: learner fills blanks correctly AND states the rule for each.
```

---

- **Name**: Segmented Low-Load Delivery
- **Description**: Break new high-interactivity content into segments small enough that about four new interacting elements are active at once, and give each segment a short check before the next. Remove extraneous load: put labels on the diagram itself instead of in a separate legend, keep text and the graphic it explains together in space and time, remove decorative material, and avoid narrating word-for-word text that learners are reading at the same moment (the redundancy effect). Keep teacher talk short and purposeful. Increase segment size as learners' prior knowledge grows, since chunked knowledge lets them handle more at once.
- **When**: Structuring direct instruction, slides, handouts, demonstrations, or any explanation in a Build; checking materials for overload in an Audit.
- **Example**:
```
    Before: one 20-minute lecture on photosynthesis with a slide of 9 labels
            in a side legend, read aloud verbatim.
    After:  Segment 1 (light capture, 4 min) -> 1 retrieval question
            Segment 2 (water splitting, 4 min) -> 1 retrieval question
            Segment 3 (sugar building, 5 min) -> learners sketch the chain
            Labels placed on the diagram; teacher narrates, slide shows the
            diagram with minimal text.
```

---

- **Name**: Automaticity Before Synthesis
- **Description**: Practice foundational facts and procedures past first correct performance until they are fluent, because automated knowledge is retrieved without using working-memory capacity, and that frees capacity for reasoning, problem solving, and synthesis. Build fluency in short, frequent, spaced bouts rather than long drills. Teach domain knowledge directly rather than generic "thinking skills" detached from content, because skilled thinking in a domain depends on the knowledge stored for that domain.
- **When**: Any course where later tasks depend on component skills: number facts before multi-step arithmetic, decoding before comprehension, core vocabulary before argumentation, syntax before program design.
- **Example**:
```
    Unit goal: multi-digit multiplication word problems (4th grade).
    Fluency strand: 5 minutes daily of multiplication-fact retrieval, mixed
                    across facts already taught, spaced across the unit.
    Reasoning strand: word problems begin after facts reach quick, accurate
                      recall, so working memory goes to the problem structure.
```

---

- **Name**: Spaced Retrieval Schedule
- **Description**: Build low-stakes retrieval practice (quizzes, brain dumps, flashcard recall, practice problems from memory) into every lesson and revisit material across days and weeks instead of concentrating it in one block. Retrieval strengthens memory more than rereading, and spacing produces more durable learning than massing. Leave a gap after taxing, high-interactivity study before testing it: the benefit of retrieval often fails to show on an immediate test, when working memory is depleted, but appears after a rest or delay. Give feedback on retrieval attempts so errors are corrected.
- **When**: Every multi-session Build (units, courses, training programs), and any single lesson that can open by retrieving prior content.
- **Example**:
```
    Week 1 Mon: teach A           Week 1 Wed: retrieve A, teach B
    Week 1 Fri: retrieve A+B, teach C
    Week 2 Mon: retrieve A-C (mixed), teach D
    Week 3: cumulative low-stakes quiz on A-D with feedback
    Rule: no quiz immediately after a heavy new-content segment; place it at
          the start of the next session.
```

---

- **Name**: Blocked-Then-Interleaved Practice
- **Description**: Use blocked practice (one problem type at a time) while learners first acquire a new procedure, because it keeps cognitive load low. Once learners can perform each type, switch to interleaved practice that mixes types, so they learn to recognize which approach a problem calls for. Interleaving adds difficulty and lowers performance during practice while improving discrimination and long-term retention.
- **When**: Designing practice sets for any domain with several similar problem types or categories: math operations, grammar forms, art styles, diagnostic categories.
- **Example**:
```
    Days 1-3: area of rectangles (block), triangles (block), circles (block)
    Days 4+:  mixed sets where each problem requires choosing the formula
    Teacher note: expect practice scores to dip when mixing starts; the dip
                  is part of building the discrimination skill.
```

---

- **Name**: Bounded Generative Strategy
- **Description**: Choose a generative strategy (summarizing, mapping, drawing, imagining, self-testing, self-explaining, teaching, or enacting) that makes learners select the important elements, organize them into a coherent structure, and connect them to what they already know. Choose it only when the mechanical cost of performing the strategy is low for these learners, because effort spent on the mechanics (freehand drawing for young children, unfamiliar movements, building a map without knowing the concepts) is extraneous load that cancels the benefit. Give learners enough content knowledge first, since generating from too little knowledge produces errors rather than understanding.
- **When**: Selecting the processing activity that follows instruction, at any age.
- **Example**:
```
    Young children: scaffolded drawing (pre-drawn background, parts to place)
    Adolescents: self-explaining steps; explaining to a peer
    Young adults: imagining a process; hierarchical concept maps; writing
                  test questions for peers
    Adults: summarizing in terms of their own work; mapping new to old practice
    Check: can these learners perform the strategy's mechanics easily?
```

---

- **Name**: Self-Explanation Prompts
- **Description**: As worked-example steps are faded, require learners to explain why each step is valid by naming the principle or rule that justifies it. Self-explanation turns studying an example into active integration and exposes gaps learners cannot see on their own. Prompt for a specific justification rather than a general reflection.
- **When**: Any worked-example or completion-problem sequence for learners old enough to verbalize reasoning (late childhood onward), and especially in quantitative and analytical subjects.
- **Example**:
```
    Step: 3x + 5 = 20  ->  3x = 15
    Prompt: "Which rule lets you make this move, and why does it keep the
             equation true?"
    Weak prompt to avoid: "What did you learn today?"
```

---

- **Name**: Concrete-Representational-Abstract Sequencing
- **Description**: For children, especially in early math and science, introduce a concept with physical objects (base-ten blocks, fraction tiles, counters), then with pictures or diagrams that represent those objects, and only then with conventional symbols. Move to the next stage when learners can translate between the current one and the next. Young children's working memory is costly to maintain internally, so they rely on what they can see and handle. Concrete anchors let them reason about relationships before holding them in their heads. In remedial or inclusive settings, show all three representations side by side so learners explicitly map between them (trials with fifth and sixth graders on fractions show large gains).
- **When**: Building lessons for young children and children (roughly ages 4-11) on abstract or symbolic content, and for older remedial learners meeting a foundational concept for the first time.
- **Example**:
```
    Concept: equivalent fractions (3rd grade)
    Concrete: fold paper strips; lay 2/4 tiles on a 1/2 tile
    Representational: shade fraction bars on a worksheet; number line
    Abstract: 1/2 = 2/4 = 4/8, with the bar drawing still visible
    Move on when: a child can draw the bar for a written fraction and write
                  the fraction for a drawn bar.
```

---

- **Name**: Externalized Control for Young Learners
- **Description**: Children's attention control and planning are still developing, so build that control into the environment and routine. Use predictable daily routines, uncluttered materials and walls near the learning focus, visible step lists and reference charts the child can look at instead of remembering, short teacher talk, and nonverbal signals to redirect attention without interrupting the flow of instruction. Limit the number of relations a child must coordinate at once: young children handle one or two related elements; three-way relationships emerge later in childhood; proportional reasoning that coordinates four elements comes later still.
- **When**: Every Build for young children and children, and Audits of their classrooms or materials.
- **Example**:
```
    Routine: same 4-part lesson shape daily, shown as a picture strip on the
             board.
    Task card: 3 numbered picture steps on the desk, so the child checks the
               card instead of recalling verbal instructions.
    Attention: raised-hand signal instead of repeated verbal calls.
```

---

- **Name**: Scaffolded Drawing and Guided Enacting
- **Description**: When children draw or act out content to learn it, remove the mechanical burden and specify what to represent. For drawing, give a pre-drawn background and printed parts the child can place, copy, or trace, plus a list of the causal parts that must appear. For enacting (gestures, manipulatives, role movements), model the exact movements that correspond to the concept, because children rarely invent productive movements on their own.
- **When**: Using drawing or physical enactment as a generative activity with children.
- **Example**:
```
    Lesson: the water cycle (2nd grade)
    Drawing: printed landscape; cut-out sun, cloud, rain, arrows; the child
             places and labels evaporation, condensation, precipitation.
    Enacting: teacher models "hands rise and spread" for evaporation and
              "fingers flutter down" for rain; children copy, then perform
              the full sequence while saying each stage name.
```

---

- **Name**: Adolescent Micro-Cycles and Structured Peer Explanation
- **Description**: Adolescents can reason abstractly, but they are highly sensitive to immediate reward and social context while their self-regulation is still maturing, and they discount distant payoffs heavily. Break long courses into short mastery cycles with frequent, immediate feedback and visible progress markers rather than relying on a distant final exam to motivate. Use structured peer explanation, where one student explains a step or concept to another using a protocol and accuracy check, to turn social motivation into generative processing. Tie abstract content to real people, communities, or decisions where learners can see the stakes. Reduce chronic stress and public high-stakes exposure, which impair the executive control learning depends on.
- **When**: Building lessons and courses for adolescents (roughly ages 12-18).
- **Example**:
```
    Unit: probability (9th grade)
    Cycle (2-3 days): worked example -> completion -> peer explain-and-check
                      -> 5-question mastery check with immediate feedback
    Framing: model how an outbreak spreads through a school contact network
    Progress: a visible skills tracker; retakes allowed for mastery
```

---

- **Name**: Contrastive Comparison for Retraining
- **Description**: When adults or experienced learners must replace an established routine (new software, a revised protocol, a changed rule), first name the old routine explicitly and then show the new one side by side with the structural differences highlighted. Entrenched knowledge interferes most when the new task looks like the old one on the surface but follows a different rule, and learners fall back to the old habit under load. Practice the cases where old and new diverge most.
- **When**: Any Build for experienced learners where the content revises or replaces something they already do.
- **Example**:
```
    Training: new expense-approval workflow
    Step 1: "Here is what you do today" (old flow on the left)
    Step 2: new flow on the right; 3 changed steps highlighted in color
    Step 3: practice cases chosen where the old habit gives the wrong answer
    Step 4: spaced follow-up retrieval at 2 days and 1 week
```

---

- **Name**: Prior-Knowledge Activation
- **Description**: Before new content, activate the relevant knowledge learners already have and connect the new material to it explicitly. Prior knowledge is the strongest single predictor of how easily new material is learned, because it lets learners chunk and integrate. Adults bring especially rich crystallized knowledge (vocabulary, domain expertise, life experience) that compensates for slower processing of new information; give them self-paced options and problems drawn from their own work. When learners' prior knowledge is mistaken, surface the misconception and address it directly rather than building on it.
- **When**: Opening any lesson or module, with particular weight for adult and older-adult learners.
- **Example**:
```
    Module: statistical process control for nurses
    Opener: "Think of a patient whose vital signs drifted slowly before an
             event. What told you something was changing?"
    Bridge: map their answer onto control limits and run rules.
    Pacing: modules self-paced with spaced retrieval checks.
```

---

- **Name**: Sensory and Pacing Accommodation for Older Adults
- **Description**: Age-related declines in vision and hearing use up working memory just to decode the input, and processing speed slows, while knowledge and verbal ability stay strong or keep growing. For older adults, use high-contrast, large, clear type; good lighting without glare; clear amplified audio with little background noise; slower pacing with longer pauses before expecting responses; and assessments without time pressure unless speed is the skill being taught. Lean on their prior knowledge to anchor new content.
- **When**: Building for older adults (roughly 65+), or any adult group with known sensory limitations.
- **Example**:
```
    Class: tablet basics for a senior center
    Materials: 18pt+ bold sans-serif handouts, dark text on white
    Room: front seating, microphone, no music under instruction
    Pacing: one new gesture per segment, practiced before the next
    Check: untimed hands-on task, done privately with the facilitator
```

---

- **Name**: Least-Experienced Profile for Mixed Groups
- **Description**: When a group spans developmental bands or expertise levels, design the core sequence for the least-experienced and youngest profile present, then add explicit differentiation for the others: faster fading, extension problems, or roles that use their experience. Protecting the most vulnerable learners' working memory costs experienced learners little when they have a fast track, while designing for the strongest learners overloads everyone else.
- **When**: Mixed-age classes, multi-grade rooms, community classes, overlapping age bands (such as 18-19-year-olds), or groups with wide prior-knowledge spread.
- **Example**:
```
    Group: community astronomy class, ages 15-72, mostly novices
    Core: segmented explanations, worked sky-chart examples, retrieval
    Differentiation: experienced members fade to independent charting after
                     one example and serve as table guides; older members
                     get large-print charts and front seating.
```

---

- **Name**: Why This Design Evidence Notes
- **Description**: End every Build and Audit deliverable with a "Why this design" section, and keep scientific justification out of the deliverable body. List each major design choice with the finding it rests on, written in plain teacher-facing language: what the choice is, what the evidence shows, and the condition that makes it apply to these learners. Then list every criterion the skill inferred (learning goal, task structure, any assumed prior knowledge) and every source used from outside the core evidence base, with its citation and the label "outside the core evidence base."
- **When**: Closing every Build and Audit output.
- **Example**:
```
    ## Why this design
    - Two worked examples before practice: these students are new to
      equations, and multi-step problems overload beginners who work by
      trial and error; studying solved examples first builds the pattern.
    - Quiz at the start of Thursday, not the end of Tuesday: retrieval helps
      most after a gap, not right after a demanding lesson.
    Inferred: goal = solve two-step equations independently; task is
    well-structured. Correct me if either is off.
```

---

- **Name**: Three-Way Audit Classification
- **Description**: In Audit mode, sort every element of the submitted material or technique into one of three groups: supported by the evidence, contradicted by the evidence, or not addressed by the evidence. Give a concrete, drop-in revision for every contradicted element, and keep supported elements as they are. Say plainly when the evidence is silent instead of stretching a finding to cover it.
- **When**: Reviewing a lesson plan, syllabus, activity, assessment, or named technique.
- **Example**:
```
    Supported: daily warm-up quiz on prior lessons (retrieval, spacing)
    Contradicted: "discover the Pythagorean theorem" open task for novices
      -> Revision: one worked proof, then completion problems, then an
         exploration task once learners can apply the theorem.
    Not addressed: classroom seating color scheme; no reliable evidence.
```

---

- **Name**: Verdict-Mechanism-Boundary Answer
- **Description**: In Advise mode, answer with a direct verdict (works, works under conditions, does not work, or evidence unclear), the mechanism that explains it, and the boundary conditions that change the answer: developmental level, prior knowledge, element interactivity, and timing. Lead with the verdict.
- **When**: Answering a standalone question about whether a method, strategy, or technique works.
- **Example**:
```
    Q: Does interleaving work for 2nd graders learning addition and
       subtraction?
    Verdict: Yes, after each operation is learned separately.
    Mechanism: mixing forces children to decide which operation a problem
               needs, which builds that judgment.
    Boundaries: start with blocked practice for each new operation; mix
                only operations each child can already perform; expect
                practice scores to dip temporarily.
```

---

- **Name**: Out-of-Core Research Labeling
- **Description**: When a request reaches beyond the integrated evidence base (dyslexia supports, sleep, language acquisition, specific disabilities, a technique the core does not cover), search current peer-reviewed sources such as meta-analyses, systematic reviews, and replicated experiments. Cite each source and label its findings in the evidence notes as outside the core evidence base. Prefer syntheses over single studies, and give single-study findings as provisional.
- **When**: Any Build, Audit, or Advise request whose central question the integrated evidence base does not answer.
- **Example**:
```
    Request: adapt a reading lesson for students with dyslexia.
    Action: search for recent meta-analyses on structured phonics and
            reading interventions for dyslexia; build from them.
    Note: "Explicit, systematic phonics support (Author, Year; meta-analysis)
           - outside the core evidence base."
```

---

## Anti-Patterns

- **Name**: Learning-Styles Matching
- **Description**: Designing instruction that sorts learners into visual, auditory, or kinesthetic "styles" and matches each to a different presentation.
- **Why**: Controlled tests consistently find that matching instruction to a preferred style does not improve learning. It spends design time on a myth and can route learners away from the representation the content needs.
- **Instead**: Choose the representation that fits the content (diagrams for spatial structure, narration with a diagram for processes), give every learner the same well-designed material, and correct the request per the conflict gate in `references/interactions.md`.

---

- **Name**: Unguided Discovery for Novices
- **Description**: Assigning beginners open-ended discovery, inquiry, or problem solving on complex new material before they have the knowledge to approach it.
- **Why**: Without schemas, novices search by trial and error, which uses up working memory without building transferable knowledge; worked examples outperform this approach for novices on high-interactivity material.
- **Instead**: Interactivity-Matched Guidance and Guidance Fading Off-Ramp. Place exploration after learners have enough knowledge to explore productively.

---

- **Name**: Scaffolding the Experts
- **Description**: Making experienced learners work through full step-by-step worked examples, or attaching explanatory text to a diagram they can already read.
- **Why**: Learners must reconcile the redundant guidance with what they already know, which wastes working memory and lowers performance relative to independent practice (the expertise-reversal effect).
- **Instead**: Assess prior knowledge, fade quickly to completion and independent problems, and give experienced learners a fast track.

---

- **Name**: Activity Equals Learning
- **Description**: Treating hands-on, busy, or physically active tasks as active learning by default, and treating explanation or reading as passive.
- **Why**: Learning depends on cognitive processing (selecting, organizing, integrating), not on visible behavior. Hands-on tasks with shallow processing teach little, while well-designed explanation followed by generative work teaches a great deal.
- **Instead**: Judge each activity by the thinking it requires about the target content, and pair explanation with a Bounded Generative Strategy.

---

- **Name**: Content-Free Thinking Skills
- **Description**: Designing lessons around generic "critical thinking," "creativity," or "problem solving" skills detached from domain knowledge.
- **Why**: Skilled thinking in a domain rests on domain knowledge stored in long-term memory; generic skills taught without content transfer poorly.
- **Instead**: Teach the domain knowledge directly and practice reasoning with that knowledge inside the subject.

---

- **Name**: Massed Study and Single Final Test
- **Description**: Covering each topic once in a block and assessing it only at the end of a unit or term.
- **Why**: Massed study produces fast short-term gains and fast forgetting; with no retrieval in between, learners have few chances to strengthen memories, and adolescents especially lose motivation when the only payoff is distant.
- **Instead**: Spaced Retrieval Schedule with frequent low-stakes checks and cumulative review.

---

- **Name**: Immediate Testing After Heavy Study
- **Description**: Placing a retrieval quiz directly after a long, demanding, high-interactivity lesson and reading the result as the measure of learning.
- **Why**: Working memory is depleted right after taxing study, so retrieval benefits often fail to appear on an immediate test and the score understates later retention.
- **Instead**: Place retrieval after a break or at the start of the next session.

---

- **Name**: Split Attention and Redundant Narration
- **Description**: Separating diagrams from their labels or explanations, crowding slides with decoration, or reading on-screen text aloud word for word.
- **Why**: Learners spend working memory matching separated sources or processing the same words twice, which is extraneous load that crowds out learning.
- **Instead**: Segmented Low-Load Delivery: integrated labels, minimal text alongside narration, and no decorative material.

---

- **Name**: Unanchored Abstraction for Young Children
- **Description**: Introducing symbols, rules, or abstract relationships to young children without physical or pictorial referents, or asking them to coordinate more relationships than they can hold.
- **Why**: Young children cannot yet hold and manipulate detached symbols in working memory, and they rely on what they can see and handle.
- **Instead**: Concrete-Representational-Abstract Sequencing and Externalized Control for Young Learners.

---

- **Name**: Mechanically Costly Generative Tasks
- **Description**: Assigning a generative activity whose mechanics are hard for the learners, such as freehand diagrams for young children, unmodeled body movements, or concept maps for learners who do not yet know the concepts.
- **Why**: Effort spent on the mechanics is extraneous load that cancels the strategy's benefit.
- **Instead**: Bounded Generative Strategy and Scaffolded Drawing and Guided Enacting.

---

- **Name**: Interleaving Too Early
- **Description**: Mixing problem types before learners can perform each type on its own.
- **Why**: Mixed practice adds load that helps only once each procedure exists; before that, it overwhelms acquisition.
- **Instead**: Blocked-Then-Interleaved Practice.

---

- **Name**: Age Bands as Walls
- **Description**: Treating developmental stages as fixed age cutoffs that dictate what a learner can or cannot do, regardless of their knowledge.
- **Why**: Domain knowledge strongly changes effective capacity: children with chess expertise out-recall novice adults on chess positions, and adults working with unfamiliar material perform like young children working with familiar material.
- **Instead**: Use the developmental profile as a starting point and adjust it by the learners' prior knowledge of this subject.

---

- **Name**: Frameworks Presented as Evidence
- **Description**: Presenting educational frameworks, theories, or productivity schemes (andragogy principles, Perry's positions, Pomodoro timing, learning pyramids, left-brain/right-brain claims) as findings of the science of learning.
- **Why**: These are pedagogical frameworks, single-study results, or myths rather than replicated findings, and presenting them as science misleads the teacher about how strong the basis is.
- **Instead**: Base design rules on replicated findings only. If a requester asks about a framework, answer in Advise mode with an honest verdict on its evidence.

---

- **Name**: Silent Substitution
- **Description**: Quietly replacing a requested element the evidence contradicts with an alternative, or building the contradicted element without comment.
- **Why**: Silent substitution takes the decision away from the teacher; silent compliance delivers a design known to be weaker.
- **Instead**: Follow the conflict gate in `references/interactions.md`: state the conflict, offer the alternative, and end the turn to wait for the choice.

---

- **Name**: Interview Overreach
- **Description**: Asking for criteria the prompt already answered, asking several questions in one turn, or requiring the learning goal before building.
- **Why**: Redundant or stacked questions delay the deliverable and dilute answers; the learning goal can be inferred and stated.
- **Instead**: Ask Only for What Is Missing, one question per turn, per `references/interactions.md`.

---

- **Name**: Rationale Clutter
- **Description**: Spreading citations, effect sizes, and mechanism explanations through the body of a lesson plan or outline.
- **Why**: The teacher has to dig the usable plan out of the justification, and the deliverable stops being classroom-ready.
- **Instead**: Why This Design Evidence Notes, kept in a closing section.

---

- **Name**: Decorative Statistics
- **Description**: Quoting effect sizes, p-values, or brain-region names that do not change what the teacher should do.
- **Why**: Numbers and neuroscience terms create an impression of rigor without helping the teacher apply the finding, and they invite overclaiming.
- **Instead**: State the finding and its condition in plain language; cite a number only when it helps the teacher judge how much weight to give the choice.
