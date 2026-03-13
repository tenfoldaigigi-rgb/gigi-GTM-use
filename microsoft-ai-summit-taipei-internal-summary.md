# Microsoft AI Summit Taipei - Internal Summary for Tenfold AI

> **Audience:** Tech, Product, and Sales teams
> **Event:** Microsoft AI Summit Taipei, 2025
> **Source:** 25 presentation slides covering market data, demos, architecture, product announcements, and adoption learnings
> **Prepared:** March 2026

---

## TL;DR

Microsoft's message is clear: every company must evolve from "human with AI assistant" (Phase 1) to "human-led, agent-operated" (Phase 3). They're backing this with a new M365 E7 SKU (GA May 1, 2026), a full-stack agent platform (Foundry), and enterprise-grade governance (Agent 365). For Tenfold AI as a legal tech player, the most relevant signals are: **Legal is explicitly called out across all three phases**, patent analysis and compliance were featured as live demos, and Microsoft's own legal team already sees a 5% reduction in external spend. The window to position Tenfold AI's agents within this ecosystem is now — before M365 E7 ships.

---

## A. Market Context & Why Now

*Relevant slides: 1, 2, 3*

### The Capacity Crisis in APAC

| Metric | APAC | Global |
|--------|------|--------|
| Leaders saying productivity must increase | **61%** | 53% |
| Workers lacking time/energy for their work | **84%** | 80% |

**Taiwan specifically:** Only 47% of leaders feel urgency, but **90% of workers feel overwhelmed** — the highest worker burnout rate in all of APAC. This leader-worker perception gap is a selling opportunity: workers are desperate for help, but leadership hasn't felt the pain yet.

### Where Companies Are Investing (Next 6-12 Months)

Top AI investment areas by % of respondents ranking in their top 3 priorities:
- Product development (27%), Customer service (25%), Marketing (24%)
- **Legal ranks at 20%** — lower than average but still significant. This means Legal AI is not yet mainstream, giving first-movers an advantage.
- Cybersecurity, Finance efficiency, Financial forecasting all at 24%

### Skills Shift

LinkedIn's top 5 in-demand skills for 2025:
1. **AI literacy** (AI capability)
2. Conflict mitigation (human strength)
3. Adaptability (human strength)
4. Process optimization (human strength)
5. Innovative thinking (human strength)

**Implication:** 4 of 5 top skills are human — AI augments, it doesn't replace. This matters for legal: lawyers still drive strategy and judgment; AI handles the grunt work.

---

## B. Microsoft's "Frontier Firm" Framework

*Relevant slides: 4, 5, 6, 10*

### The Three Phases

| Phase | Model | What It Looks Like | Legal Examples |
|-------|-------|-------------------|----------------|
| **Phase 1** | Human + assistant | Copilot helps individual workers | Summarizing contracts, drafting memos, patent search |
| **Phase 2** | Human-agent teams | Agents as "digital colleagues" on specific tasks | Due diligence agent, compliance review agent |
| **Phase 3** | Human-led, agent-operated | Agents run entire workflows, humans set direction | Automated contract lifecycle mgmt, continuous compliance monitoring |

### Legal Use Cases Across All Three Phases

| Phase | Legal Use Cases Called Out by Microsoft |
|-------|----------------------------------------|
| **Phase 1** | Advisor work, patent management, expert consulting, litigation, risk mgmt, contracting, policy & compliance mgmt |
| **Phase 2** | Due diligence, risk mgmt and compliance |
| **Phase 3** | Automated compliance monitoring, contract lifecycle management |

---

## C. Demos & Use Cases

*Relevant slides: 7, 8, 9, 11, 12*

### Legal-Adjacent Demos (High Relevance to Tenfold AI)

**1. Patent Summarization & Comparison (Slide 8)**
- Copilot processes and compares patent documents side-by-side
- Extracts filing details, key claims, scope of application
- Identifies overlapping claims and potential conflicts
- **Time savings:** Hours of manual comparison → minutes
- **Tenfold relevance:** Direct overlap with legal document analysis capabilities

**2. Brand Certification / Product Compliance (Slide 11)**
- AI agent checks new product launches against complex portfolio rules
- Consults a knowledge base with multiple data sources
- **40x faster** approval vs. manual review
- Replaces institutional knowledge that previously lived in people's heads
- **Tenfold relevance:** Same pattern as contract compliance checking — agent consults rules/precedents, makes approve/reject recommendation

**3. FAQ Agent with Human-in-the-Loop (Slide 9)**
- Agent drafts FAQ content from service changes → human reviews → monitors usage
- **Tenfold relevance:** Same workflow pattern for generating legal advisories, policy updates, or client-facing compliance summaries

### Enterprise-Wide Demos

**4. Barclays "Colleague Agent" (Slide 12)** — The standout case study
- Company-wide deployment connecting 7+ systems (Workday, Salesforce, Jira, ServiceNow, Coupa, Confluence)
- Agent doesn't just answer questions — **takes actions** (raises compliance requests, submits leave, summarizes project status)
- Users don't need to know which system to query
- **Tenfold relevance:** Imagine a legal version — a single agent that checks compliance across multiple regulatory databases, contract management systems, and internal policies

**5. Quality Test Data Analysis (Slide 7)**
- Copilot in Excel for SPC data analysis
- Relevant for operations/manufacturing teams, less directly for legal

---

## D. Technology & Architecture

*Relevant slides: 19, 20, 21, 22, 23, 24*

### For the Tech Team

**1. Agentic Retrieval Pipeline (Slide 19)**

A 3-stage architecture that powers all the agent demos:

```
Stage 1 (LLM): Intent analysis → data source selection → query planning → self-reflection
    ↓
Stage 2 (Multi-source): Search Indexes + OneLake/Fabric + SharePoint + Bing → L2 ranking
    ↓ (SLM as Judge — if quality insufficient, loops back to Stage 1)
Stage 3 (LLM): Integrate results → synthesize answer → log activity
```

- **SLM as a Judge** for quality control is a cost-effective pattern — use a small model to evaluate retrieval quality before passing to the expensive LLM
- **Iterative retrieval loop** allows self-correction
- **Tenfold tech implication:** Our retrieval pipeline should consider similar SLM-as-judge patterns for grounding legal AI in case law / contract databases

**2. Two Multi-Agent Orchestration Patterns (Slide 20)**

| | Agent Orchestration | Workflow Orchestration |
|---|---|---|
| **Who controls flow** | LLM decides dynamically | Developer defines via code |
| **Flexibility** | High | Lower |
| **Predictability** | Lower | High |
| **Best for** | Open-ended tasks (customer queries) | Repeatable processes (compliance checks) |

**Tenfold tech implication:** Most legal workflows should use **Workflow Orchestration** (predictable, auditable, deterministic). Agent Orchestration is better for open-ended legal research queries.

**3. Foundry Agent Service — Full Platform Stack (Slides 21, 22)**

From bottom to top:
- **Models:** OpenAI, Llama, Grok, **Anthropic**, Mistral (multi-model, not locked in)
- **Foundry IQ:** Agent Memory for persistent context
- **Foundry Tools:** MCP, OpenAPI, Logic Apps, A2A (agent-to-agent)
- **Agent Service** → **Hosted Agents** → **Multi-agent Workflows**
- **One-click Publishing** to M365/A365

Key standards: **MCP** (Model Context Protocol), **OpenAPI**, **A2A** (Agent-to-Agent communication)

**Tenfold tech implication:** If we build agents compatible with MCP/OpenAPI/A2A standards, they can plug directly into the Microsoft ecosystem via Foundry. This is the integration path.

**4. Agent Observability & Evaluation (Slides 23, 24)**

- Full execution traces: every sub-agent, tool call, retrieval, with timing and token counts
- Automated quality scoring: Similarity, Coherence, String Check, Safety
- Version comparison across agent runs
- **Tenfold tech implication:** For legal AI, explainability is non-negotiable. We should build comparable tracing into our agents — every recommendation must be traceable back to source documents.

---

## E. Product & Packaging

*Relevant slides: 16, 17, 25*

### Microsoft 365 E7 — "The Frontier Worker Suite"

**General Availability: May 1, 2026**

| Component | What It Is |
|-----------|-----------|
| M365 E5 + Entra Suite | Enterprise productivity + identity |
| M365 Copilot | AI assistant (Phase 1-2) |
| Microsoft Agent 365 | Agent governance control plane (Phase 2-3) |

### Agent 365 — Control Plane for Agents

Three pillars:

| Pillar | What It Does |
|--------|-------------|
| **Observe** | Real-time monitoring of all agents |
| **Govern** | Lifecycle management — policies, permissions, compliance |
| **Secure** | Entra ID (agent identity), Defender (threat protection), Purview (data governance) |

**Key detail:** Agents get their own **Entra ID identity** — treated as first-class enterprise entities with the same security controls as human employees.

**Production deployment:** Unified management across all platforms (M365, Copilot Studio, custom, third-party), secure deployment via Entra/Defender/Purview, and connection to enterprise surfaces (Office apps, storage, Teams, semantic index).

---

## F. Adoption Success & Failure Factors

*Relevant slides: 13, 14, 15*

### Microsoft's Own Internal Results (95% CI, Statistically Significant)

| Department | Metric | Impact |
|------------|--------|--------|
| Customer Service | Case resolution speed | **+11.5%** |
| Sales | Revenue per seller | **+9.4%** |
| Marketing | Azure.com conversion rates | **+21.5%** |
| Finance | Cash collections resolution time | **-60%** |
| **Legal** | **External spend for regulatory work** | **-5% (projected)** |
| HR | Employee self-service accuracy | **+42%** |
| IT | Self-help success rate | **+36%** |

### PwC Study: Why Customers Succeed vs. Fail

The top 2 factors are the same for both groups — they're **table stakes**:
1. Had proper use case scenarios
2. Data quality

The **real differentiators:**

| Factor | Rank in Success | Rank in Failure | Interpretation |
|--------|----------------|-----------------|----------------|
| **Senior Management buy-in** | #4 | #10 (last) | Present when it works, absent when it doesn't |
| **AI Literacy** | #7 | #4 | Lack of literacy is a top killer |
| **Governance** | #10 | #6 | Becomes a concern when things go wrong |

### Real Customer Case Studies: What Works vs. What Doesn't

**What works — peer-to-peer learning culture:**

| Company | Winning Strategy |
|---------|-----------------|
| Sumitomo Corp | Hands-on training for 30+ incl. Chairman; "Copilot Ambassador" per division; regular newsletter |
| JBS | Licenses for everyone equally; hackathons after training; monitored usage by role |
| Honda Motor | Dedicated portal; community for mutual learning; shared prompting know-how |
| PERSOL Corp | Community via Viva Engage for peer sharing |

**What fails — IT-dependent, top-down rollout:**

| Anti-Pattern | Result |
|-------------|--------|
| No one to ask casually | Users stopped exploring |
| Manual distributed, no follow-up | Never read or studied |
| One training session, no follow-up | Abandoned |

**Bottom line:** Distribute licenses + walk away = failure. Build communities + ambassadors + hackathons = success.

---

## G. Implications for Tenfold AI (Legal Tech)

### Product Strategy

1. **Legal is explicitly featured across all three Frontier phases.** Microsoft sees Legal as a first-class AI adoption area — patent management, compliance, contracting, due diligence, litigation support. This validates Tenfold AI's market.

2. **The patent and compliance demos are our competition and our opportunity.** Microsoft showed generic Copilot doing patent comparison and brand compliance checking. Tenfold AI's opportunity is to go **deeper** — domain-specific legal AI that outperforms generic Copilot on accuracy, citation quality, and regulatory awareness.

3. **Phase 2 is where Tenfold AI should play right now.** Most enterprise legal teams are in Phase 1 (Copilot for drafting/summarizing). The jump to Phase 2 (dedicated legal agents for due diligence, compliance review, contract analysis) is where specialized legal tech creates the most value. Don't try to sell Phase 3 to Phase 1 teams.

4. **Build for MCP/OpenAPI/A2A compatibility.** If Tenfold AI agents are compatible with these standards, they can be deployed via Foundry and published to M365/A365 with one click. This makes us a plug-in to the Microsoft ecosystem, not a competitor to it.

5. **Workflow Orchestration is the right pattern for legal.** Legal processes need deterministic, auditable, repeatable workflows (contract review, compliance checking). Build agents using Workflow Orchestration with clear human checkpoints. Reserve Agent Orchestration for open-ended legal research.

6. **Explainability is a must-have, not a nice-to-have.** The agent tracing demo (Slide 23) shows every step, every source, every tool call. For legal AI, this is non-negotiable — every recommendation must link back to the statute, clause, or precedent that supports it.

### Sales & GTM Strategy

7. **Microsoft's 5% legal cost reduction is a weak number — we can beat it.** Microsoft's internal Legal result was the weakest across all 7 departments (5% projected reduction in external regulatory spend). This is because generic Copilot isn't built for deep legal work. Position Tenfold AI as the solution that delivers **Legal-grade results** that generic Copilot can't match.

8. **Ride the M365 E7 wave.** E7 ships May 1, 2026 — every enterprise E5 customer will be evaluating the upgrade. Tenfold AI should position as the legal agent that makes E7's Agent 365 more valuable. Partner with Microsoft sellers pitching E7 to legal departments.

9. **Lead with the adoption playbook.** The PwC data (Slide 14) and customer cases (Slide 15) give us a playbook for selling: (a) identify proper use cases first, (b) ensure data quality, (c) get senior management buy-in, (d) build a peer learning community. Offer this as part of our deployment package — not just software, but a success framework.

10. **Target Taiwan's perception gap.** 47% leader urgency vs. 90% worker overwhelm in Taiwan is an opportunity. Go bottom-up: demonstrate to legal practitioners how much time they save, then let demand pull leadership in.

11. **Use Barclays as the aspirational story.** When selling to enterprise legal teams, use the Barclays Colleague Agent as the aspirational end-state: "Imagine your legal team has a single agent that checks compliance across all your regulatory databases, contract systems, and internal policies — and takes action on your behalf."

12. **Governance is our Trojan horse into CISO conversations.** Legal AI touches sensitive data. Agent 365's Entra ID/Defender/Purview stack means we can say: "Your legal agents are protected by the same security controls as your employees." This matters for regulated industries.

### Technical Partnerships

13. **Explore Foundry Agent Service integration.** Tenfold AI agents built on or compatible with Foundry can be published directly to M365/A365. This distribution channel is potentially massive.

14. **Support multi-model.** Microsoft's platform supports OpenAI, Anthropic, Llama, Mistral. Tenfold AI should be model-agnostic where possible — customers may have preferences or compliance requirements around specific models.

15. **Build evaluation frameworks.** The agent evaluation dashboard (Slide 24) with Similarity, Coherence, Groundedness, and Safety metrics is the emerging standard. Tenfold AI should have comparable evaluation tooling for legal agents — especially around **Groundedness** (are we citing real sources?) and **Safety** (are we giving legally sound advice?).

---

## H. Microsoft's Call to Action (& What It Means for Us)

Microsoft's closing CTA maps directly to our opportunity:

| Microsoft's CTA | What It Means for Tenfold AI |
|-----------------|------------------------------|
| Assess which Frontier phase you are | We help legal teams assess their AI maturity and identify high-value use cases |
| Start exploring Agents | We ARE the legal agent they should explore |
| Ensure adoption framework is in place | We provide the adoption playbook (not just software) |
| Consider Agent 365 for governance | We integrate with Agent 365 for enterprise-grade governance |

---

## Appendix: Slide Index

| # | Title | Category |
|---|-------|----------|
| 1 | Human Labor is Reaching Its Limits | Market Data |
| 2 | Areas of Accelerated AI Investment | Market Data |
| 3 | In-Demand Skills for the New Era of Work | Market Data |
| 4 | The Journey to Becoming a "Frontier Firm" | Framework |
| 5 | AI Adoption Phase 1 - Copilot Use Cases | Use Cases |
| 6 | AI Adoption Phase 2 - Role-Specific Scenarios | Use Cases |
| 7 | Deep Analysis on Quality Test Data | Demo |
| 8 | Summarize & Compare Patent Info | Demo (Legal) |
| 9 | Updating External Services FAQs | Demo |
| 10 | AI Adoption Phase 3 - Independent Applications | Use Cases |
| 11 | Brand Certification Judgement | Demo |
| 12 | "Colleague Agent" - Barclays | Case Study |
| 13 | Copilot's Early Impact at Microsoft | Proof Points |
| 14 | Top 10 Reasons: Successful vs Not | Adoption Research |
| 15 | Learning from Customer Cases: KSF | Adoption Research |
| 16 | Microsoft 365 E7 - The Frontier Worker Suite | Product |
| 17 | Microsoft Agent 365 - Control Plane | Product |
| 18 | Call to Action | CTA |
| 19 | Agentic Retrieval Architecture | Architecture |
| 20 | Two Multi-Agent Collaboration Patterns | Architecture |
| 21 | Microsoft Agent Framework - Open Source | Platform |
| 22 | Foundry Agent Service - Full Stack | Platform |
| 23 | Agent Trace & Observability | Platform |
| 24 | Agent Evaluation Dashboard | Platform |
| 25 | Agents in Production - Agent 365 | Product |
