# Language Tutor Sharp Edges

## Conversational & Pedagogical Failures

### **Explicit Correction Overload**
- **Symptom**: The agent halts a natural dialogue to explain a minor grammar mistake in detail, behaving like a textbook rather than a conversational partner.
- **Risk**: High cognitive load and damage to learner confidence.
- **Remedy**: Rely strictly on *recasting* (e.g., if the user says "I go to store yesterday," reply with "Oh, you went to the store yesterday? What did you buy?"). Only use explicit explanations if the error is persistent (already in `persistentErrors`) or if the user explicitly asks "is that correct?".

### **CEFR Level / Target Language Mismatch**
- **Symptom**: The agent responds entirely in French to a learner classified at A1 level, or uses complex past subjunctive structures with an A2 Spanish learner.
- **Risk**: Learner frustration, feeling overwhelmed, and breaking the comprehensible input (90-95% understanding) threshold.
- **Remedy**: Strictly check the CEFR level in `working-memory.toon` at the beginning of the turn. Refer to the Target Language Ratio table and adjust syntax complexity (sentence lengths, tenses, vocabulary) accordingly.

---

## Technical & State Failures

### **Incorrect SM-2 Calculations**
- **Symptom**: The agent calculates an ease factor (EF) less than 1.3, or calculates next review dates that are months in the future for a newly introduced word.
- **Risk**: Core spaced repetition system breaks down; words are either forgotten or shown too frequently.
- **Remedy**: Ensure the calculation rules in validations are strictly adhered to. The ease factor must never drop below 1.3. For new words, interval always starts at 1 day.

### **Malformed TOON Serialization**
- **Symptom**: The agent writes the `srsDeck` table in `working-memory.toon` with missing header columns, extra commas, or malformed list brackets.
- **Risk**: Subsequent sessions will fail to parse the TOON file, corrupting the learner's profile and progress history.
- **Remedy**: Validate the TOON output against the regex rules in validations before executing the write. Ensure the columns in `srsDeck` perfectly match `item,translation,easiness,interval,repetitions,nextReviewDate` and contain no extra separators.

### **State Overwrite / History Loss**
- **Symptom**: When updating a single vocabulary item, the agent overwrites the entire file and accidentally deletes the user's profile metadata or other vocabulary words.
- **Risk**: Irreversible loss of learning history.
- **Remedy**: Perform a read-modify-write cycle carefully. Read the entire `working-memory.toon` file, perform the update in memory, and rewrite the structured document containing all existing profile, stats, and deck items.

### **Persistent Error Bloat**
- **Symptom**: The `persistentErrors` list contains more than 10 items.
- **Risk**: Context inflation and dilution of target practice areas.
- **Remedy**: Cap the list at 10 items. Remove resolved errors when the learner demonstrates consistent correct production across two lessons.
