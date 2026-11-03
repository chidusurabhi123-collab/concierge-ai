
# Concierge AI — Failure Analysis

## Evaluation Run 1

- Dataset size: 40 questions
- Retrieval threshold: 0.45
- Top K: 3
- Correct decisions: 35
- Incorrect decisions: 5
- Accuracy: 87.50%
- Precision: 72.22%
- Recall: 100%

## Observed Failures

| Question | Failure | Analysis |
|---|---|---|
| Q11 | False positive | Refund policy retrieved for a 90-day refund question |
| Q28 | False positive | Refund-related content retrieved for a request to invent policy |
| Q30 | False positive | Refund policy retrieved for an unsupported 365-day claim |
| Q34 | False positive | Refund policy retrieved for an unlimited-refund claim |
| Q35 | False positive | Refund policy retrieved for a refund guarantee request |

## Root Cause

The retrieval system uses semantic similarity. It can retrieve related content even when the documents do not support the customer's specific claim.

Retrieval relevance does not establish factual support.

## Limitations

- Evaluation measures retrieval decisions, not final answer correctness.
- The dataset contains only 40 questions.
- Similarity threshold has not been systematically optimized.
- LLM answer correctness has not been independently evaluated.
- Adversarial safety requires separate testing.

## Planned Improvements

1. Evaluate answer grounding separately from retrieval.
2. Test prompt injection and unsupported claims.
3. Improve refusal and escalation decisions.
4. Add automated regression tests.
5. Persist human escalation tickets.
