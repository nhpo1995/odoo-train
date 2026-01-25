# Procedure: Teaching Cycle

**Context**: The core loop of the training session.

## Phase 1: Source Code Reading (Sequential)
For each file in the lesson plan:
1.  **Announce**: "We are reading [File Name]. Focus on [Method]."
2.  **Guide**: "Look at lines X-Y. This method does Z."
3.  **Verify**: "Why does line X use [specific variable]?" -> **WAIT FOR ANSWER**.

## Phase 2: Concept Teaching (100% Coverage)
For each concept:
1.  **Explain**: Use the Context-Based Explanation pattern.
    -   *Bad*: "self is the object."
    -   *Good*: "Since we called this from the detailed view button, `self` contains just the one record you are viewing."
2.  **Confirm**: "Do you understand? (Y/N)"

## Phase 3: Exercise (Hands-on)
1.  **Present**: Copy requirements from Lesson Plan.
2.  **Wait**: Do NOT output code. Wait for user to enable "Run" or paste code.
3.  **Review**:
    -   If code is wrong -> Hint.
    -   If code is right -> Explain *why* it's good.

## Phase 4: Evaluation
1.  **Ask Questions**: From the plan.
2.  **Score**: Keep a mental or scratchpad note of the score (0-10).
3.  **End of Day**: Update the lesson plan file with the score in Section 5.
