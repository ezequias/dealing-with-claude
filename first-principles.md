# First Principles Thinking for a Software Architect (output from Claude Haiku 5.5)

## 1. What the idea is

**First principles thinking** means reducing a problem to the basic truths that cannot be broken down further, then reasoning upward from those truths to build a solution. The opposite is **reasoning by analogy**: "Netflix uses microservices, so we should too" or "our last project used Spring, so this one will too."

Aristotle described first principles as the "first basis from which a thing is known." Modern engineers use the idea to avoid inheriting assumptions they never examined.

A simple way to see the difference:

| Reasoning by analogy | Reasoning from first principles |
|---|---|
| "We always do it this way." | "What must be true for this system to work?" |
| Copies what others did | Derives what fits this context |
| Fast, but fragile in new contexts | Slower, but adapts to new constraints |
| Hides assumptions | Exposes assumptions |

## 2. Why it matters for an architect

An architect constantly makes decisions under uncertainty: which database, which style, how to split modules, whether to add a queue. Mostof these decisions come with *inherited beliefs*:

- "We need microservices for scalability."
- "We need an abstraction layer in case we change databases."
- "Every service needs its own repository class."

Some of these beliefs are true in certain contexts and false in others. First principles thinking forces you to ask: **which of these beliefs rest on a real constraint in *our* system?**

## 3. The method, step by step

**Step 1: State the decision and the assumption.**
Write it plainly. *"We want to split billing into a separate service."*

**Step 2: Ask "why?" until you hit bedrock.**
- Why split? → So billing can scale independently.
- Why does it need to scale independently? → Does it actually have a different load profile?
- Let the data answer. If billing handles 20 requests per minute, the premise collapses.

**Step 3: List the fundamental truths.**
These are facts about your system, your team, and physics, not opinions. Examples:
- Networks fail, and calls between components can time out.
- Each change that touches many modules costs time and risk.
- A team of four people can only hold so much in working memory.
- Data outlives code. Schemas are harder to change than classes.
- Latency between services is orders of magnitude greater than a method call in-process.

**Step 4: Rebuild a solution using only those truths.**
Ignore the "usual" architecture. Construct the simplest design that satisfies the truths and the actual requirements.

**Step 5: Validate and stay honest.**
Compare the rebuilt solution against the conventional one. Check the cost, the risk, and whether you're rationalizing a preference you already had.

## 4. A worked example

**Scenario:** An e-commerce team wants to send order confirmations to customers. The proposal is a Kafka cluster, three new services, and an event schema registry.

**Reasoning by analogy** says: "Large companies use event-driven architecture, so we should."

**First principles:**
- *Truth 1:* Confirmation emails can arrive a few seconds late without harm.
- *Truth 2:* We must never lose an order confirmation that was committed.
- *Truth 3:* The volume is about 50 orders per minute.
- *Truth 4:* The team has four engineers and no experience operating Kafka.

**Rebuilt solution:** Write an "outbox" row in the same database transaction as the order. A scheduled job reads pending rows and sends emails, marking them as sent.

```java
@Transactional
public void placeOrder(Order order) {
    orders.save(order);
    outbox.save(new OutboxEvent("ORDER_CONFIRMATION", order.getId()));
}

@Scheduled(fixedDelay = 5000)
public void dispatchPending() {
    for (OutboxEvent event : outbox.findPending()) {
        mailer.sendConfirmation(event.getOrderId());
        event.markSent();
        outbox.save(event);
    }
}
```

This satisfies the truths: the confirmation is never lost (same transaction), delay is acceptable, and throughput is trivial. It also keeps the option open. If volume grows a hundredfold, you can replace the scheduler with a broker without changing the business rule.

Note the outcome: the analogy-based design was not necessarily wrong for a larger company. It was wrong *for this context*.

## 5. How this connects to the design principles

The principles in the reference guide (SOLID, DRY, KISS, YAGNI, Separation of Concerns, Composition over Inheritance, Law of Demeter) are best understood as **conclusions derived from first principles**. Each one rests on a truth:

| Principle | First principle underneath |
|---|---|
| **DRY** | Knowledge duplicated in several places diverges over time, so every change becomes a consistency risk. |
| **YAGNI** | Unused code has a real maintenance cost, and predictions about the future are often wrong. |
| **KISS** | Human cognitive capacity is limited, so complex code is expensive to verify. |
| **Separation of Concerns** | Changes in one kind of knowledge (HTTP, rules, storage) should not force changes in others. |
| **Law of Demeter** | Each dependency on an object's internal structure is a point of future change. |
| **Composition over Inheritance** | Inheritance couples the subclass to the parent's full behavior, so the parent's changes propagate. |

This gives you a powerful tool. When a principle seems to conflict with a situation, or when you face a new kind of problem where no principle clearly applies, go back to the truths. The principle is a shortcut; first principles are the map beneath it.

## 6. Pitfalls to avoid

1. **Reinventing everything.** First principles is not an excuse to ignore proven knowledge. Use Chesterton's Fence: before removing a rule, understand why it exists. Many "unnecessary" conventions encode lessons learned the hard way.
2. **Analysis paralysis.** Not every decision deserves a full derivation. Apply the method to decisions that are expensive or hard to reverse.
3. **Choosing your truths conveniently.** It is easy to label a preference as a "fundamental truth." Test each truth against data: measurements, incidents, team capacity.
4. **Ignoring the team.** Your rebuilt design must also be operable and understandable by the people who will maintain it.
5. **Confusing novelty with insight.** A design that is different from the norm is not automatically better. It must solve the truths moreeffectively.

## 7. A practical checklist

Before a significant architectural decision, ask:

- What exactly are we deciding, and what is the assumption behind it?
- Which constraints are real (measured, contractual, physical) and which are inherited habits?
- What is the simplest design that satisfies the real constraints?
- What does this decision cost to reverse? Prefer reversible choices ("two-way doors") when uncertainty is high.
- Which principles from the guide does the design honor, and which does it trade off, and why?
- Would I make the same choice if the conventional pattern did not exist?

## 8. Summary

For a software architect, first principles thinking is a discipline of **questioning inherited assumptions** and **reasoning from the realconstraints** of the system, the team, and the environment. It does not replace established design principles; it explains where they comefrom and tells you when they apply. The architect who thinks this way asks not "what is the standard?" but "what must be true, and what isthe simplest design that makes it so?"