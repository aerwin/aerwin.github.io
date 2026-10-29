---
layout: post
title: "Building Production Agentic AI at IBM: Architecture, Decisions, and What We Learned"
date: '2026-08-23T09:00:00.000-05:00'
description: "How IBM's Technology Lifecycle Services built a multi-agent system from scratch — the architecture, the decisions, and the lessons, from its chief architect."
tags:
- langgraph
- agents
- agentic-ai
- architecture
- ibm
- a2a
- mcp
- cloud
categories: [AI, Agentic AI]
image:
  path: "/images/2026-08-23-building-production-agentic-ai-at-ibm/agent-platform-architecture.png"
  show: false
---

> **TL;DR** — IBM's Technology Lifecycle Services built a multi-agent system from scratch — the agents themselves in Python with LangGraph. In production since fall 2025, it gives every TLS role one place to ask questions that used to span a dozen systems. What I'd tell someone starting the same project:
>
> - **Use A2A for every agent boundary, MCP for every tool boundary.** That uniformity is what let five of our six specialist agents be built by separate teams, one in an entirely separate environment.
> - **Carry the user's identity through every hop — propagate or exchange, never substitute a service account.** The moment one delegation drops the caller's identity, authorization quietly leaves the enterprise's model for yours. Easy to get wrong, brutal to retrofit.
> - **Instrument before you build — evals, traces, business metrics — with tools that exist today.** We flew blind too long: tracing stalled on shifting internal roadmaps, evals arrived after the changes they should have guarded, and a business baseline never arrived at all. Sooner would have mattered more than any architectural decision.
> - **The real constraint was never agent code — it was data access.** Everyone wants an agent factory, a team stamping out new agents; we needed a data factory — finding the systems of record, negotiating access, building the tool layer.
> - **Independent teams are easy to add and hard to align.** The same boundaries that let them plug in let each prioritize its own backlog. We shipped a better reasoning pattern everyone agreed made sense; most of our agents still don't use it.
{: .prompt-info }

## Introduction

As I described in my [previous post on building trustworthy AI](/2024/07/building-trustworthy-ai-a-practical-solution-guide-for-enterprise-ai-teams.html), I'm a senior architect in the **IBM Infrastructure AI Center of Excellence (AI CoE)**, a group focused on accelerating responsible AI adoption across the [IBM Infrastructure](https://www.ibm.com/solutions/it-infrastructure) business unit — putting AI to work for IBM's own employees, not just its clients. For the past couple of years I've been something of a double agent: officially part of the AI CoE, but embedded full-time in IBM's **[Technology Lifecycle Services (TLS)](https://www.ibm.com/services/technology-lifecycle-services)** organization, where I've been serving as Chief Architect for the **TLS Agentic Platform**. TLS is a large organization with thousands of employees within IBM Infrastructure that provides hardware and software support, maintenance, and lifecycle management worldwide.

The **TLS Agentic Platform** is the full system: a multi-agent AI system, the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) tool servers and APIs that connect it to enterprise data, and the cloud environment everything runs on. Its front end is the **TLS Concierge** — a single AI experience built to give every TLS employee one place to go. One interface, one conversation, whether the question is about a support case, a hardware asset, a contract, or a client's history. The goal is to eliminate the context-switching across a dozen different systems that currently consumes so much of a TLS professional's day. We built it from the ground up and had real users in production within months of starting — and have been evolving it ever since.

If you read my [earlier post on the IBM Cloud console's evolution from monolith to microservices](/2021/08/evolving-the-ibm-cloud-console-with-microservices-a-nodejs-success-story.html), this post is the next chapter of that same story. The architectural philosophy is the same: decompose complexity into independently deployable units, build shared infrastructure that scales, be honest about what went wrong. But the technology has shifted in ways nobody in the industry fully anticipated — that post predates the ChatGPT moment by over a year. The services are still independently deployed, the patterns are still familiar — but when a service's core logic is an LLM reasoning over tools rather than deterministic code executing a defined path, the differences matter in ways that aren't obvious until you're operating one in production.

That context matters for everything that follows. Every architectural decision I'll describe was made inside a real service organization at real scale, where an agent giving bad information to an IBM employee can have real consequences for an actual client. Enterprise AI constraints — compliance, audit trails, long-running operations — were not academic concerns here. They were the requirements that shaped the architecture from day one.

## TLS and Its AI Strategy

TLS has been on a deliberate AI journey for several years. IBM Fellows Bala Rajaraman and Kyle Brown wrote about the [vision behind TLS's AI investment](https://www.ibm.com/new/product-blog/technology-lifecycle-services-envisioning-the-next-generation-of-support-with-ai): using AI to move TLS from a reactive support model to a proactive, insight-driven one, measuring success not just by ticket resolution metrics but by the client outcomes those metrics are supposed to represent. IBM VP Dylan Boday [frames the operational case](https://www.ibm.com/think/insights/integrating-data-center-support-lower-costs-and-decrease-downtime-with-your-support-strategy): integrated data center support reduces downtime and total cost of ownership when the people and tools providing that support have the right information at the right moment. IBM VP Bina Hallman [describes the practical shape of that investment](https://www.ibm.com/think/topics/ai-for-it-support): watsonx-powered Agent Assist surfacing relevant knowledge during case work, AI-generated case summaries reducing the effort of managing complex multi-week engagements, and automated Call Home processing that handles 91% of hardware error notifications end-to-end without client intervention.

Agents in the agentic sense — autonomous systems reasoning over tools and acting on their own — appear nowhere in those posts. For the first few years, TLS's AI work was focused on AI-infused features and assistive tooling: surface the relevant data, reduce manual lookup, give support engineers better information faster. That work established some early data pipelines and integrations, but TLS didn't yet have a coherent AI platform to build on. A significant part of my first year embedded in TLS was helping design and build that foundation: a secure cloud environment for running AI workloads, integrations to the systems of record, a model deployment and governance framework drawing on the AI CoE work I described in my trustworthy AI post. When agentic AI moved from research curiosity to production reality, that platform is what made it possible to go from a workshop in May 2025 to real users in production by fall, with the platform continuing to grow from there. That's what this post is about: what building that agentic layer actually looked like, on top of an existing AI foundation, inside a large service organization with real production requirements.

### Personas and Use Cases

Understanding who your users are and what they're trying to accomplish is old advice. It binds harder on an agentic system: you aren't designing screens for tasks you've already scoped, you're building something that has to handle whatever a user thinks to ask. The initial use case centered on the **Technical Escalation Manager (TEM)**, a role that can spend hours of manual effort getting up to speed on a new escalation before reaching out to a client: reading through long case histories, cross-referencing asset data, finding relevant technical documentation. That's a real operational pain point in a large service organization, not a demo use case invented for a conference talk, and it was the seed the rest of the platform grew from.

From that starting point the platform expanded to cover a broader set of TLS roles. Below is a sampling of key personas and the kinds of scenarios the platform supports for each.

<div class="wrapped-table" markdown="1">

| Role | Description | Representative scenarios |
|---|---|---|
| **Technical Escalation Manager** | Manages critical escalations and coordinates technical resources | Rapidly get up to speed on a new escalation — case history, asset details, business impact — so the first client conversation is informed and productive; draft status updates grounded in the actual case data |
| **Client Manager / Client Success Manager** | Owns overall client relationship and success | Interactively explore a client's support history; generate tailored insights and PowerPoint content for a client review |
| **High Availability Center of Competence (HACoC) Specialist** | Cross-platform high-availability architecture and consulting | Analyze a client's infrastructure environment ahead of a workshop; generate a findings and recommendations report post-session |
| **Sales / Global Contract Office** | Drives revenue; manages contract portfolio | Ask natural-language questions about contract terms and obligations; identify revenue opportunities embedded in existing agreements |
| **Technical Account Manager / Client Availability Leader** | Proactive technical guidance and availability management | Surface asset visibility gaps and proactive risk indicators across a client's installed base |
| **Remote Technical Support** | Front-line technical support engineers resolving client issues | Pull relevant technical documentation and case history for an active support issue |

</div>

### TLS Concierge

The **TLS Concierge** is the front end of the platform, built on IBM's [Carbon for AI](https://carbondesignsystem.com/guidelines/carbon-for-ai/) design system to give every TLS role a single place to work. Its centerpiece is **AskTLS**, an open-ended chat for any persona: type a question, and the platform figures out which agents and data sources are needed to answer it. Alongside it sit workflows tailored to specific personas — experiences that feature the same conversational core but structure it around a particular role's tasks rather than leaving everything to open-ended chat.

The screenshot below shows AskTLS handling the kind of question a Technical Escalation Manager might ask when first picking up a new escalation: a natural-language query about the major events in a case, answered with a synthesized, structured timeline pulled from the case system. Ready to read in seconds rather than assembled manually over the course of hours.

<img src="/images/2026-08-23-building-production-agentic-ai-at-ibm/tls_concierge.png"
       alt="TLS Concierge"
       style="border: 1px solid rgba(0,0,0,0.12); border-radius: 4px;">
*The TLS Concierge with AskTLS open — one front end giving every TLS role access to the full agentic platform.*

## Full System Architecture

The **TLS Agentic Platform** spans the full stack: from the Concierge front end through the multi-agent system to the cloud infrastructure described below. It began with the TEM use case; the architecture that emerged from that initial work is what's in production today.

<img src="/images/2026-08-23-building-production-agentic-ai-at-ibm/agent-platform-architecture.png"
       alt="Multi-Agent Platform Architecture"
       style="border: 1px solid rgba(0,0,0,0.12); border-radius: 4px;">
*The TLS Agentic Platform in production. A representative slice — the Supervisor routes to more specialist agents than are shown individually.*

The diagram reads top to bottom, from the user interface down through the agents to the systems of record. The legend tells the visual story: the dark blue Supervisor sits at the top of the agent hierarchy; lighter blue boxes are the specialist agents; grey filled boxes are MCP tool servers; plain white boxes are APIs, services, and data stores; and dashed boxes are external systems the platform doesn't own. The line colors carry the protocols — blue for A2A between agents, slate for MCP from an agent to a tool server, grey for ordinary service and data calls. Here's what each layer does.

**Frontend.** The Concierge UI never speaks directly to agents. It routes through a [Next.js](https://nextjs.org/) Backend for Frontend (BFF) layer that handles authentication, session management, rate limiting, and the SSE streaming connection to the browser. The BFF talks to the Supervisor Agent using [Agent2Agent (A2A)](https://a2a-protocol.org/), the same protocol the agents use among themselves. A separate external-facing Support Insights UI, owned by the [IBM Support Insights](https://www.ibm.com/products/support-insights) team, surfaces analytics and reporting over its own data.

**Agents.** Behind the BFF sits the Supervisor Agent, the system's routing intelligence. All agents are built in Python using [LangGraph](https://www.langchain.com/langgraph); most began on a standard ReAct loop, and the platform is now moving toward the skills-based deep agent pattern described later. The Supervisor receives every user request, determines intent, and delegates to the appropriate specialist agent via A2A rather than an in-process call — a choice I'll come back to below. Each specialist is an independently deployed service responsible for a distinct domain:

<div class="wrapped-table" markdown="1">

| Agent | Domain |
|---|---|
| **Case Agent** | Case summaries, timelines, and similar-case retrieval |
| **Asset Agent** | Hardware inventory and software version data (hosted in a separate environment by the Support Insights team) |
| **Doc Agent** | RAG over technical documentation |
| **Client Management Agent** | Analytics, chart generation, automated reporting |
| **Contract Agent** | Contract intelligence and natural-language query |
| **HACoC Agent** | Infrastructure analysis, workshop preparation |

</div>

Only the Supervisor and the Case Agent were built by the platform team itself. Every other agent was built and is owned by a separate team — the Doc Agent, Client Management Agent, Contract Agent, HACoC Agent, and Asset Agent all came from the domain teams closest to those problems. That ownership split isn't something the diagram shows; the boxes describe where things run, not who built them. That's the design working as intended: each team owns its domain, deploys independently, and the Supervisor routes to whatever is available without needing to know where it runs or who built it. The Asset Agent is the one case where the deployment boundary makes the ownership split visible — it runs in an entirely separate environment — and I'll come back to it below.

The agents were deliberately designed to serve multiple personas across use cases rather than mapping one-to-one to a role. A single question from a TEM like "does the hardware in this case have the latest software level, and if not is there a migration guide?" might simultaneously invoke the Case Agent for the case details, the Asset Agent for the hardware and software version data, and the Doc Agent to find the relevant documentation — all transparently, within a single response. Similarly, a client manager reviewing support history might draw on both the Client Management Agent and the Case Agent in the same conversation. The Supervisor routes every request to whichever agent or combination of agents can best answer it, without the user needing to know which agent handled what.

**MCP Tool Servers.** Each agent accesses data through [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) servers, lightweight services that expose specific APIs as callable tools. The Case MCP Server wraps the Salesforce proxy API; the Documentation MCP Server fronts the internal RAG API; the Asset MCP Server connects to the Support Insights data layer; and so on. Why the tools live behind their own service boundary — and what that buys — is a decision in its own right, covered below. One of those tool servers closes a loop with where TLS started. Agent Assist began as an automation that watched for new cases, found similar ones, and posted what it found back into the case record. The Agent Assist MCP Server exposes that same watsonx-powered retrieval as a tool, so it now runs on demand, in response to what a user actually asks.

**APIs, data stores, and external systems.** At the base are the actual systems of record: Salesforce, which is the platform for case management; Cloud Object Storage; a Milvus vector store; and a set of internal enterprise data feeds. These are accessed only through the MCP layer; agents never call external APIs directly.

**Observability and model access.** Two shared services sit alongside the agent layer rather than within it. [Langfuse](https://langfuse.com/) collects distributed traces across every agent invocation. [LiteLLM](https://www.litellm.ai/) provides a unified interface to the underlying language models, making it straightforward to swap or route across model providers without changing agent code.

**Identity across the call path.** The user's authorization token is propagated the full length of a request: BFF to Supervisor, Supervisor to specialist agent, agent to MCP server, MCP server to the underlying API. No hop substitutes a service account, and where the request crosses into a system with its own identity provider — Support Insights for asset data, or an enterprise backend like Salesforce — the token is exchanged rather than dropped. [IBM Verify](https://www.ibm.com/products/verify) performs the [OAuth 2.0 token exchange](https://docs.verify.ibm.com/verify/docs/oauth-20-token-exchange), so the same user arrives on the other side. Propagate or exchange, never substitute. The effect is that each system of record applies the same access controls to an agent's request that it would if that person queried it directly; the platform never becomes the arbiter of who can see what. This is easy to get wrong and hard to retrofit: every delegation in a multi-agent system is a chance to lose the caller's identity, and the moment one hop does, authorization has quietly moved out of the enterprise's existing model and into yours.

**Shared platform code.** One piece of the platform isn't in the diagram, because it isn't a service. The **AI CoE Agent Utils** is a Python library I created that every agent and MCP server is built from: base classes for A2A-enabled LangGraph agents and MCP servers, plus the cross-cutting machinery that would otherwise be reimplemented in every repo — tracing, authentication, header propagation, state persistence. The diagram shows what runs; this is what it's made of. I'll come back to why it exists below.

### Ecosystem Interoperability

The platform was designed from the start as an open node in a broader ecosystem, not a closed system. Both A2A and MCP are bidirectional at the platform boundary.

<img src="/images/2026-08-23-building-production-agentic-ai-at-ibm/ecosystem-interoperability.png"
       alt="Ecosystem Interoperability"
       style="border: 1px solid rgba(0,0,0,0.12); border-radius: 4px;">
*The platform is simultaneously a provider of agents and tools to external orchestrators, and an orchestrator of external agents and tools itself.*

On the A2A side: inbound, any external application, assistant, or agent that speaks A2A can call any of the platform's specialist agents directly — the Concierge and its BFF are just one client of many the architecture can support. Outbound, the Supervisor can delegate to agents running on entirely different platforms: [Salesforce Agentforce](https://www.salesforce.com/agentforce/), [IBM watsonx Orchestrate](https://www.ibm.com/products/watsonx-orchestrate), or any other A2A-compliant system.

On the MCP side: inbound, any external system that speaks MCP can connect to the platform's tool servers and use them directly, without going through the agent layer at all. Outbound, the platform's agents can call MCP servers hosted on other platforms, consuming external tools the same way they consume their own.

Open doesn't mean unauthenticated, and the identity rule runs in both directions. Inbound callers perform the token exchange themselves before calling, arriving with a token minted for this platform rather than a general-purpose enterprise one. It's validated through App ID, which federates to IBM's enterprise identity provider, and from there it propagates exactly as it would from the Concierge — the boundary is open to any compliant client, not to any request.

The practical result is that the TLS Agentic Platform can act as either an orchestrator of external agents or a provider of agents and tools to external orchestrators, depending on the use case. This is what open standards for agent interoperability make possible in practice — and it was a deliberate design choice, not an afterthought.

### Cloud Infrastructure

The TLS Agentic Platform runs inside the **TLS AI Platform**, a secure [IBM Cloud](https://www.ibm.com/cloud) environment purpose-built to host TLS production workloads. The diagram below shows how the agentic stack maps to the underlying cloud infrastructure.

![TLS Agentic Platform — Cloud Deployment](/images/2026-08-23-building-production-agentic-ai-at-ibm/agentic-platform-cloud-deployment.drawio.png)

The agent workloads — BFF, Supervisor, specialist agents, and MCP tool servers — run inside an **[IBM Cloud Kubernetes Service (IKS)](https://www.ibm.com/products/kubernetes-service)** cluster. Each workload runs in its own namespace with dedicated resource quotas. Cross-namespace communication is blocked by default; Kubernetes network policies and an Istio service mesh enforce network isolation, and individual services must explicitly declare which internal and external endpoints they need to reach during onboarding.

Model inference is handled by **[Red Hat AI Inference](https://www.ibm.com/products/redhat-ai)** (accessed via **LiteLLM**), keeping model calls within the IBM Cloud boundary. Distributed tracing flows through **Langfuse**, also deployed within the cluster.

The data and storage layer provides each onboarded service with its own instances of whichever data services it needs:

- **[Cloud Object Storage](https://www.ibm.com/products/cloud-object-storage)**
- **[Cloudant](https://www.ibm.com/products/cloudant)**
- **[PostgreSQL](https://www.ibm.com/products/databases-for-postgresql)**
- **[watsonx.data](https://www.ibm.com/products/watsonx-data)**, providing the managed **Milvus** vector database used for RAG workloads across the platform

The security and operations layer includes:

- **[Secrets Manager](https://www.ibm.com/products/secrets-manager)** for credential management
- **[IBM App ID](https://www.ibm.com/products/app-id)** for authentication and authorization
- **[IBM Cloud Logs](https://www.ibm.com/products/cloud-logs)** for audit and application logging
- **[IBM Cloud Monitoring](https://www.ibm.com/products/cloud-monitoring)** for observability

At the base, the platform connects outward to the enterprise APIs and data sources that the MCP tool servers wrap and expose to agents.

The platform is designed for multi-region deployment with multi-availability-zone resilience within each region, giving the production system the reliability characteristics a large organization's tooling requires. The governance, security, and trustworthy-AI standards underpinning all of this are covered in depth in [*Building Trustworthy AI: A Practical Solution Guide for Enterprise AI Teams*](/2024/07/building-trustworthy-ai-a-practical-solution-guide-for-enterprise-ai-teams.html) — the earlier post I referenced in the introduction.

## Key Architectural Decisions

We took that system from nothing to production, and kept building. That journey produced a set of decisions I'd make the same way again, and a few I'd make differently. Here's an honest account of both — what we chose, why, and what the alternatives would have cost us.

### Why LangGraph?

The first real decision was whether to use a code-first framework at all, and by May 2025 there were credible options either way. [IBM watsonx Orchestrate](https://www.ibm.com/products/watsonx-orchestrate) was the natural IBM-native option, a low-code/no-code platform for building AI agents and automations. For some use cases it's a reasonable starting point, and for teams without deep engineering capacity it lowers the barrier to getting something running.

But I've seen this pattern enough times across enough projects to trust the instinct: low-code and no-code platforms are fast until they're not. There is always a point where the business requirement doesn't fit the abstraction, and at that point you either accept the constraint or start dropping down into escape hatches — custom code extensions, workarounds, undocumented integration points. In a production system with a wide range of complex, evolving use cases, I didn't want the platform's ceiling to be determined by what the low-code layer happened to support. The decision to go code-first was made early and I haven't second-guessed it.

Within the code-first space, we chose LangGraph. It stays close to the mechanics rather than hiding them: you define the nodes and the edges yourself, state is explicit and persists across steps, and streaming happens at node granularity rather than only on the final answer. Control flow is code you write, not behavior you hope the model produces. That level of control has been worth the steeper initial learning curve at every stage of the project.

Worth noting: Orchestrate has evolved considerably in the year since we made this decision. The product now explicitly spans the full spectrum from no-code to pro-code — a visual drag-and-drop builder for teams that want to move fast without writing code, and an Agent Development Kit (ADK) with Python, APIs, OpenAPI, and MCP server support for teams that want full control. Critically, it now supports importing existing LangGraph agents and deploying them through Orchestrate's control plane, which provides observability, optimization, and governance without requiring a rewrite. Teams evaluating this choice today are looking at a meaningfully different product than the one we evaluated in 2025, and the gap between the low-code and code-first options is narrower than it was.

### Why A2A?

The Agent2Agent (A2A) protocol gives each agent an HTTP endpoint and a self-describing `AgentCard` — identity, skills, and required authentication — so a client can discover an agent and know how to call it securely. What makes it more than a service description is what it models above the call. The remote agent is deliberately opaque: callers see skills and results, never the tools, memory, or reasoning behind them. And an exchange isn't assumed to be a single round trip — an agent can answer immediately, or open a `Task` with its own ID and lifecycle that runs long, asks a clarifying question, and streams results as they emerge, with clients polling, subscribing over Server-Sent Events, or receiving a webhook push. Agents stay independently deployable in any language with an A2A server implementation, and a new specialist can join the platform without touching the Supervisor.

The alternative is in-process subagents: one Python process, agents as library calls. That's simpler to start with and is genuinely the right answer for some use cases. The key practical difference: if you want your agents to be independently versioned, independently deployed, independently scaled, and independently testable, A2A is the right abstraction. For TLS, where different teams own different agents and deployment isolation is a production requirement, that independence isn't optional. The Asset Agent — running in a completely separate environment, operated by a different team, connected purely via A2A — is the clearest demonstration of that benefit.

### Why MCP for Tools?

Model Context Protocol (MCP) is an open standard for exposing tools to LLMs. The alternative was binding tools directly into each agent as LangGraph functions, which is simpler and perfectly reasonable when you have one agent. It stops scaling the moment you have six. Two agents needing case data means two copies of the same client code, two sets of credentials to rotate, and two places to fix a bug. MCP puts the tool behind a service boundary instead: multiple agents connect to the same server, and the team that owns a tool can evolve it on their own schedule without coordinating a release with every agent that consumes it. That last property mattered because the same distributed teams that built the agents also built the MCP servers.

### Why BFF-as-A2A-Client?

The web UI does not speak A2A directly from the browser. Instead, a Backend-for-Frontend (BFF) service (a pattern you'll recognize from the [microservices post](/2021/08/evolving-the-ibm-cloud-console-with-microservices-a-nodejs-success-story.html)) acts as the A2A client and exposes a Server-Sent Events (SSE) endpoint to the browser.

This is the right layering for two reasons. First, SSE is the natural browser protocol for streaming updates — no WebSocket upgrade, no long-poll, native in every browser. Second, authentication, rate limiting, and connection management belong in the BFF — the architecture section already put them there — not in the browser. Keeping those concerns out of the frontend makes both layers simpler and easier to evolve independently.

Speaking A2A rather than an interface specific to our Supervisor also made the frontend portable. The same UI components and the same BFF can front any A2A-compliant agent — an application with an entirely different supervisor could reuse the whole stack.

### Why Deep Agents?

Most of our agents started with the [ReAct](https://www.ibm.com/think/topics/react-agent) loop — think, act, observe, repeat. It's effective for narrow, well-scoped tasks. But in a support context where queries require multi-step reasoning, synthesizing information across several sources, and maintaining coherent context through a complex interaction, it hits a ceiling. The model works one step at a time without a strong mechanism for planning, chaining intermediate conclusions, or routing to specialized behavior based on the nature of the task.

The way past it came from looking outward. AI assistants like IBM Bob, Claude, and others were demonstrating noticeably deeper reasoning, and digging into how they worked led us to [LangChain's deep agent harness](https://docs.langchain.com/oss/python/deepagents/overview).

The harness keeps the same tool-calling loop underneath, but wraps it in the scaffolding that makes long tasks survivable:

- **Persistent memory** in `AGENTS.md` files loaded at startup
- **Skills**, each a self-contained directory following the [Agent Skills specification](https://agentskills.io/specification) that bundles instructions with the scripts, reference documents, and templates a task needs
- **Subagents** that take an isolated slice of work in their own context window and hand back a single compact result
- **Automatic summarization and offloading** so a long run stays inside the model's context limit

Skills load progressively — every skill's name and description in context from the start, the full instructions only when the agent decides one applies, the bundled files only if the work reaches them — which is what makes a large library of them affordable. A new capability is a new skill directory rather than a change to the agent's core graph. The result is an agent that can decompose a problem, carry context forward, and route to specialized behavior rather than pushing everything through a single undifferentiated loop.

### Why the AI CoE Agent Utils?

Early in the project it became clear we had a copy-paste problem. A2A, LangGraph, and MCP each ship their own libraries, but none of them covered the full composition of everything we needed — so every agent and MCP server began as sample code stitched together from several tutorials, then customized locally. The result wasn't just duplicated code; it was code that had already diverged. When a fix or enhancement was needed (an authentication pattern, a tracing hook, a configuration convention) it had to be applied to every repo independently, against a slightly different starting point each time. The solution was a shared Python library I created called the **AI CoE Agent Utils**: the "glue code" that makes LangGraph, A2A, and MCP work together consistently across the platform, while removing most of the boilerplate each team would otherwise write from scratch.

A sampling of what the library provides:

- **Base classes and helpers** for building A2A-enabled LangGraph agents and MCP servers
- **Distributed tracing**, wired into Langfuse automatically for every service
- **Authentication and authorization middleware**, plus custom header propagation across agent chains
- **PostgreSQL-backed state persistence**, set up with a few standard environment variables, so a conversation survives a restart or a reroute to a different instance of the agent
- **The deep agent harness** described above, reduced to configuration so a team supplies `AGENTS.md` and its skills rather than integration code
- **A [Promptfoo](https://www.promptfoo.dev/docs/getting-started/) integration** for LLM-graded evals, making it straightforward to add evaluation coverage to any agent

Central to the library is the factory pattern: a factory class that constructs an agent with all its dependencies (LLM, tools, tracing, MCP connections) injected at construction time rather than scattered through application code. The factory is also the single injection point for observability. Wire Langfuse tracing into the factory once, and every agent created by any factory automatically produces traces. Without that clean injection point, adding tracing post-hoc becomes a distributed find-and-update exercise across every agent repo.

What began as TLS glue code turned out not to be TLS-specific. I took it back to my AI CoE team, where it became a formal inner source project across IBM Infrastructure — I led the squad and kept writing code, but much of what the library grew into was other people's work. It's now used by every agent and MCP server in the platform, and by teams beyond TLS: the AI CoE adopted it to build agents in their own AI assistant, IBM's Supply Chain team took it up as well, and the IBM Power team began using it and contributing code back.

## What We Learned Along the Way

The architectural decisions above are largely things I'd repeat. The lessons below are the ones that came at a cost. Some of them are the same lessons from the microservices post, wearing new clothes — not because the lesson was forgotten, but because a new paradigm resets the conditions that produce it. New tooling, new pressure to ship something visible, and a set of stakeholders, product managers, designers, and engineers who haven't yet paid the price for skipping it. Knowing what matters isn't the same as getting it prioritized, and closing that gap turned out to be its own piece of work.

### Build observability in from day one

This one and the two that follow are my biggest regrets, and they're the same regret at three levels: knowing what the system did, knowing whether a change improved it, and knowing whether any of it mattered. This is a lesson from the microservices era too. I wrote in that post about how we'd [greatly underestimated the importance of monitoring and troubleshooting](/2021/08/evolving-the-ibm-cloud-console-with-microservices-a-nodejs-success-story.html#monitoring-and-troubleshooting) and how we'd been "flying blind" until we built something to fix it. I knew the lesson going into this project and pushed for observability early. The friction was a different kind. Strategic internal solutions were on the way, so we tried them — and then the strategy shifted, ownership changed hands, and what we'd integrated against was no longer where things were going. That happened more than once. The cost wasn't just the waiting; it was integration work spent on platforms that never arrived in the form we'd planned for. We eventually cut through it by going open source with Langfuse, and I wish we'd made that call much earlier.

In a multi-agent system, the visibility problem is at least as hard as it was for microservices. An agent that calls a supervisor that calls three specialists that each call multiple MCP tools isn't a system you can reason about from log files alone. Langfuse gave us distributed traces showing exactly what happened, in what order, how long each step took, and what the model actually said at each step. The lesson for enterprise teams: be wary of taking a hard dependency on a platform that is still a roadmap item, however credible the roadmap. Pick something proven and available today, wire it in behind an interface you control, and revisit when the strategic option actually exists.

### Evals are not optional — and not having them has consequences

Tracing shows you what happened on one run. Evals tell you whether a change made things better across many. LLM-based systems don't have a stable test suite in the traditional sense: the model's behavior shifts with every prompt change, every model upgrade, every new tool. The only reliable way to know whether a change made things better or worse is a solid evaluation framework with representative scenarios and clear pass/fail criteria. We eventually built that into the AI CoE Agent Utils as a Promptfoo integration, so any agent on the platform could add eval coverage cheaply. It arrived later than it should have, and the gap slowed us down. When agents started producing subtly wrong answers in certain cases, we didn't always have the scaffolding to know it had happened, let alone catch it before users did. An eval framework isn't a nice-to-have you add when the system matures. It's load-bearing infrastructure that needs to exist before you start making consequential changes.

### Evals tell you the agent was right. KPIs tell you it mattered.

We were good at shipping and bad at measuring. We knew the platform was being used, and we heard from users that it helped — but we never put rigorous KPIs in place. No baseline for how long escalation prep actually took before. No consistent measure of how much of that we removed. No agreed definition of what "working" meant at the business level.

The costs compound. Without a baseline you can't prove value to the people funding the work. You can't tell which agent is earning its keep and which is a science project. And you end up arguing about impact from anecdotes, which means the most vivid story wins rather than the most representative one.

It's the same failure as the eval gap, one layer up — and like the eval gap, far harder to retrofit than it would have been to build in from the start. If you're standing up an agentic platform now, define what success looks like numerically before you write the first agent, and instrument for it on day one.

### The right thing doesn't get into the plan by itself

Sometimes you can see exactly what needs to be built, you build it, and it still doesn't get used. The deep agent migration is my clearest example. I prototyped with LangChain's harness, liked what I saw, and built the integration into the AI CoE Agent Utils so any agent on the platform could opt in by writing skills. I demoed it. Stakeholders and developers liked it. By early 2026 I was pushing it hard.

Most of our agents still aren't deep agents.

Not because anyone disagreed, and not because the migration is difficult — but because most of those agents belong to other teams, each with its own domain backlog, and reworking a functioning agent reads as a large change with schedule risk attached. Anything that isn't new function loses to new function almost every time. That's the same force described in the technical debt section below — and "it already works" is a hard argument to beat when there's a backlog.

There's a paradox in that. The deep agent pattern was the thing that would have made fixing existing problems and building new function faster — skills are additive, so a new capability becomes a new skill rather than a change to a graph every use case shares. More than that, some of the new function in the backlog was unlikely to work well without it. The change being deferred as a threat to the schedule was, I believe, the fastest path to the things the schedule was protecting.

I made that argument, more than once. It didn't land. What came back was never a counterargument — just the reminder, in one form or another, that the schedule came first and the migration had better not threaten it. The work had already been filed as a detour, and an argument is hard to land once that view is set.

It also didn't help that I couldn't prove the claim. Without a solid set of golden questions and eval coverage across agents, I could show that a deep agent handled a hard query well, but not that it handled a representative set measurably better than what we already had. The eval gap and the adoption gap turned out to be the same problem seen from two sides: the argument I needed to make required evidence I hadn't built the means to produce.

If I were doing it again I'd treat adoption as a distinct piece of work with its own plan, its own owner, and its own place on the schedule — part of what was committed, rather than something to make the case for alongside it. I tried to get it there and didn't succeed. Whether that was a failure of persuasion on my part or a structural fact about how committed roadmaps work, I still don't know. What I'm sure of is that anything outside the plan competes with the plan, and usually loses.

Several of the remaining agents are migrating now. That's the right outcome, but it arrived later than it needed to.

### New features vs. technical debt: agentic systems are not immune

The deep agent migration is the specific case. The general one is worth stating plainly. There is always pressure to add new capabilities: a new agent, a new data source, a new workflow. That pressure is real and the use cases are often legitimate. But agentic systems accumulate technical debt in ways that are easy to underestimate — prompt engineering decisions that made sense for one use case quietly break another, tool interfaces that were expedient early on become bottlenecks, test coverage that was deferred starts to matter. None of that is unique to agentic systems. What is different is that when the agent's reasoning is the product, deferred quality work shows up in ways that are harder to diagnose and more visible to users.

### Data access is the long pole in the tent

Everyone says AI is only as good as its data. That's true, and also an understatement when you're building inside a large enterprise. The complexity we encountered wasn't in the agent code. It was in everything that had to happen before the agent could call a tool and get a real answer back: identifying which system of record actually held the data a given use case needed, determining whether that data was accessible at all or locked behind a team that had never been asked to expose it, negotiating authentication and authorization across organizational boundaries, and building the MCP servers or wrapper APIs to surface the data in a form agents could use. None of that shows up in architecture diagrams, and none of it is fast.

We were able to move quickly on early prototypes precisely because we mocked the MCP endpoints, and those prototypes were genuinely useful for validating agent behavior and building confidence in the approach. But there's a hard limit on how far a mocked data layer takes you. Nothing is real until the actual data is flowing, and in an enterprise environment, getting that data flowing requires work that no amount of clever agent architecture can shortcut.

The instinct in fast-moving teams is often to accelerate by building more agents — to stand up an "agent factory" that can stamp out new capabilities quickly. I came to believe the bigger constraint was a data factory: a dedicated effort to identify the right data sources, establish the integrations, sort out the authorization, and build the tool layer that makes that data reliably accessible to agents. The agent work is the visible part. The data access work is what determines whether any of it actually delivers value to a user.

### Enterprise policy decides what you build with, and when

Building AI inside a large enterprise means working inside a policy envelope you don't set: what's approved, what's compliant, what's been procured, what a security review will pass. Most of those constraints are legitimate — they usually exist because somebody learned something the hard way — but the timing is never yours. The observability tooling delay earlier in these lessons was one version of this. Data access was another. Model availability was the sharpest.

You rarely have free choice of model. Ours had to be open-weight and served from inside the IBM Cloud boundary — commercial frontier models reached over a vendor API were not an option for the data we handle.

We also made a deliberate choice not to run inference ourselves. Standing up and operating GPUs is a specialized job, and there were teams inside IBM whose job it was; our job was agents. So we consumed inference as a managed service — watsonx first, later [Red Hat AI Inference on IBM Cloud](https://newsroom.ibm.com/2026-05-12-ibm-announces-red-hat-ai-inference-and-red-hat-openshift-virtualization-service-on-ibm-cloud). Bringing your own model was technically possible, but the economics of dedicated hardware never made sense for a team our size.

I'd make that call again, and it has a price: your model menu becomes your inference provider's roadmap. [`gpt-oss-120b`](https://huggingface.co/openai/gpt-oss-120b) became available to us late in 2025 and appeared to meaningfully improve exactly the planning-heavy work the deep agent shift was meant to enable — without changing a single graph, skill, or tool. I say "appeared" deliberately: this was just the kind of claim the eval gap left us unable to prove. Gemma 4 ([`gemma-4-31B-it`](https://huggingface.co/google/gemma-4-31B-it)) was announced in April 2026, but only became available to us when Red Hat AI Inference on IBM Cloud reached general availability the following month. We're evaluating it now against the same workloads, partly on the strength of what other teams have reported.

What you can control is how fast you move once an option appears. We put LiteLLM in front of every model call as part of preparing the move to Red Hat AI Inference — and because the Agent Utils factory already owned how models are constructed and injected, even that migration was a configuration change rather than a rewrite. With LiteLLM in place, changing inference backends never touched agent code, and neither did pointing agents at a different model. The harder half is qualification — knowing whether a new model is actually better for your workloads, not just newer. Keep the model swappable, keep a set of evals ready to answer that question, and the lag between "available" and "in production" is at least yours to own. The general form: you don't control when a constraint lifts, only how much work it takes to move when it does.

## Conclusion

The plain version first: this worked. A team that started with no agentic system had a multi-agent platform in production within months, and it has been serving real TLS users ever since. Most of the agents running on it were built by teams that didn't build the platform, and they interoperate anyway. The shared library, AI CoE Agent Utils, became an inner source project and was adopted by other teams across the business unit. Serving as the platform's chief architect has been one of the best roles I've had at IBM, and working with this team has been the best part of it. Everything in the lessons above is the cost of having actually built the thing, not a reason someone shouldn't.

I'm writing this at a moment of transition. Like a lot of large organizations, IBM is consolidating: what began as separate agentic efforts in different corners of the business is converging toward shared platforms. That's a natural evolution, and in some ways it's a validation of the approach. The patterns we landed on — skills-based agents, supervisor orchestration, governed data access — are the same ones other teams across IBM arrived at on their own. When you have no uniform platform and have to build one yourself, you tend to discover the same constraints everyone else does.

My own role is shifting with it, moving from Chief Architect of the TLS Agentic Platform to a broader focus on empowering IBM Infrastructure sellers and clients with the insights they need to make informed decisions and achieve better outcomes. More than two years embedded in TLS — first helping define the underlying platform for running AI solutions in production and then building the agentic layer on top of it — means I'm carrying a grounded understanding of what it actually takes to make AI work in a large service organization, not just what it takes to demo it. It's the same bittersweet feeling I had [leaving the IBM Cloud console team](/2021/08/evolving-the-ibm-cloud-console-with-microservices-a-nodejs-success-story.html).

None of what I've described here was built by one person. The TLS Agentic Platform is the product of contributions from teams across TLS and the AI CoE — engineers, architects, product managers, and domain experts who brought the use cases, the data, the integrations, and the operational knowledge that made the system real. What's in this post is my account of what we built together and why.

Special thanks to the executive sponsors on the TLS side — IBM VPs [Bina Hallman](https://www.linkedin.com/in/bina-hallman/) and [Cristiane Hilkner](https://www.linkedin.com/in/cristiane-hilkner-2512aa/) and IBM Fellow [Bala Rajaraman](https://www.linkedin.com/in/bxrbxr/) — who not only championed this work but welcomed me in and treated me as one of their own rather than an outsider from another group. And to IBM VPs [R "Doc" Vaidhyanathan](https://www.linkedin.com/in/docvaidhyanathan/) and [Susan Cohen](https://www.linkedin.com/in/susan-cohen-57648743/), whose support and trust on the AI CoE side made the whole double-agent arrangement possible.

## What's Next

There's a lot more to say about how these pieces actually work in practice. Upcoming posts will go deep on specific patterns — the factory pattern and how it wires LangGraph, A2A, and observability together; what deep agent memory and skills look like in code; and how to approach evals for an LLM-based system where the right answer isn't deterministic. Each will include working code you can run. If any of those topics are particularly relevant to something you're building, I'd love to hear about it — reach out on [LinkedIn](https://www.linkedin.com/in/tonyerwin/) or leave a comment below.

*Portions of this post were developed with assistance from AI tools including [IBM Bob](https://bob.ibm.com/), an AI coding assistant. All content has been reviewed, validated, and approved by the author, who maintains full responsibility for its accuracy and recommendations.*
