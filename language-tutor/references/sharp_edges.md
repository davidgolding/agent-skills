# Language Tutor Sharp Edges

## Conversational & Pedagogical Failures

### **Explicit Correction Overload**
- **Symptom**: The agent halts a natural dialogue to explain a minor grammar mistake in detail, behaving like a textbook rather than a conversational partner.
- **Risk**: High cognitive load and damage to learner confidence.
- **Remedy**: Rely strictly on *recasting* (e.g., if the user says "I go to store yesterday," reply with "Oh, you went to the store yesterday? What did you buy?"). Only use explicit explanations if the error is persistent (already in `persistentErrors`) or if the user explicitly asks "is that correct?".

### **Grammar/Concept Lecture Overload**
- **Symptom**: The agent spends multiple paragraphs explaining a grammar rule's conjugations or exceptions during what should be natural conversation.
- **Risk**: Breaks conversation immersion, increases friction, and shifts the learner into a passive state.
- **Remedy**: Introduce concepts inductively. Use the rule in target-language input first, model its use, and prompt the user to use it in context. Limit explicit grammatical explanations to 1-2 sentences.

### **CEFR Level / Target Language Mismatch**
- **Symptom**: The agent responds entirely in French to a learner classified at A1 level, or uses complex past subjunctive structures with an A2 Spanish learner.
- **Risk**: Learner frustration, feeling overwhelmed, and breaking the comprehensible input (90-95% understanding) threshold.
- **Remedy**: Strictly check the CEFR level in `working-memory.toon` at the beginning of the turn. Refer to the Target Language Ratio table and adjust syntax complexity (sentence lengths, tenses, vocabulary) accordingly.

### **Idiom & Register Overload**
- **Symptom**: The agent uses highly colloquial, archaic, or complex idiomatic expressions with pre-A1 or A1 level learners.
- **Risk**: Semantic confusion; beginners cannot separate literal meaning from figurative usage.
- **Remedy**: Keep idioms highly functional at A2-B1 levels. Calibrate to the Learner Profile dialect/interests and only introduce highly nuanced cultural/regional idioms at B2 level or higher.

### **Curriculum Progression Failures**
- **Symptom**: The agent introduces B1 structures before A2 structures are mastered (quality score < 3), or introduces multiple distinct concepts in a single turn.
- **Risk**: Concepts are stacked without reinforcement, leading to fragmented learning.
- **Remedy**: Follow the SM-2 review dates to reinforce concepts. Ensure only 1 new concept is introduced per lesson, and only advance the curriculum stage when the current stage's items maintain an interval > 6 days.

---

## Technical & State Failures

### **Incorrect SM-2 Calculations**
- **Symptom**: The agent calculates an ease factor (EF) less than 1.3, or calculates next review dates that are months in the future for a newly introduced word or concept.
- **Risk**: Core spaced repetition system breaks down; items are either forgotten or shown too frequently.
- **Remedy**: Ensure the calculation rules in validations are strictly adhered to. The ease factor must never drop below 1.3. For new items, interval always starts at 1 day.

### **Malformed TOON Serialization**
- **Symptom**: The agent writes the `srsDeck` or `curriculumDeck` table in `working-memory.toon` with missing header columns, extra commas, or malformed list brackets.
- **Risk**: Subsequent sessions will fail to parse the TOON file, corrupting the learner's profile and progress history.
- **Remedy**: Validate the TOON output against the rules in validations before executing the write. Ensure the columns in `srsDeck` and `curriculumDeck` perfectly match their schemas.

### **State Overwrite / History Loss**
- **Symptom**: When updating a single vocabulary item or curriculum concept, the agent overwrites the entire file and accidentally deletes the user's profile metadata or other deck items.
- **Risk**: Irreversible loss of learning history.
- **Remedy**: Perform a read-modify-write cycle carefully. Read the entire `working-memory.toon` file, perform the update in memory, and rewrite the structured document containing all existing profile, stats, and deck items.

### **Persistent Error Bloat**
- **Symptom**: The `persistentErrors` list contains more than 10 items.
- **Risk**: Context inflation and dilution of target practice areas.
- **Remedy**: Cap the list at 10 items. Remove resolved errors when the learner demonstrates consistent correct production across two lessons.
