import json
import random
from datetime import datetime, timedelta

VERTICALS = {
    "Healthcare": {
        "concerns": ["HIPAA compliance", "patient data security", "EHR integration", "data privacy", "PHI handling", "audit trail requirements"],
        "use_cases": ["patient analytics", "clinical decision support", "population health management", "care coordination"],
        "problems": [
            "Our current analytics platform can't handle the volume of patient records we're processing. We're seeing 30-second query times on dashboards that clinicians need in real time.",
            "We have data siloed across five different EHR systems and there's no unified view of patient journeys. Clinicians are making decisions with incomplete information.",
            "We failed our last HIPAA audit because we couldn't demonstrate proper data lineage. We need to know exactly where patient data flows and who accessed it.",
            "Our population health models are running on stale data - sometimes 48 hours old. By the time we identify at-risk patients, interventions are already too late.",
        ],
        "functional_reqs": [
            "The system must support real-time ingestion from HL7 FHIR endpoints with sub-second latency for critical patient events.",
            "Users must be able to build custom clinical dashboards without engineering support, using a drag-and-drop interface.",
            "The platform must support automated patient cohort generation based on configurable clinical criteria including ICD-10 codes, lab results, and medication history.",
            "We need the ability to run federated queries across all five EHR data sources as if they were a single dataset.",
            "The system must generate automated alerts when patient risk scores exceed configurable thresholds.",
            "All data transformations must produce an auditable lineage trail showing source-to-destination data flow.",
        ],
        "nonfunctional_reqs": [
            "Dashboard queries must return results within 2 seconds for datasets up to 50 million records.",
            "The system must maintain 99.95% uptime with zero planned downtime during business hours.",
            "All data at rest and in transit must be encrypted using AES-256 and TLS 1.3 respectively.",
            "The platform must support role-based access control with at least 15 distinct permission levels aligned to clinical roles.",
            "System must be able to scale horizontally to handle a 10x increase in data volume over the next 3 years without architectural changes.",
            "Disaster recovery must support an RPO of 1 hour and an RTO of 4 hours.",
            "The system must comply with HIPAA, HITECH, and state-level privacy regulations simultaneously.",
        ]
    },
    "Financial Services": {
        "concerns": ["regulatory compliance", "fraud detection", "data governance", "SOC 2 compliance", "PCI DSS", "model risk management"],
        "use_cases": ["risk analytics", "customer behavior analysis", "portfolio optimization", "anti-money laundering"],
        "problems": [
            "Our fraud detection system has a 15% false positive rate which is costing us millions in manual review hours. We need to reduce that without increasing false negatives.",
            "Regulators are requiring us to demonstrate model explainability for all credit scoring decisions. Our current ML pipeline is essentially a black box.",
            "We're processing trades across 12 different asset classes and the reconciliation process takes 6 hours. By the time discrepancies are found, settlement windows have closed.",
            "Our risk models run in batch overnight but the market moves in real time. We need intraday risk recalculation to stay competitive.",
        ],
        "functional_reqs": [
            "The system must support real-time transaction scoring with the ability to process at least 10,000 transactions per second.",
            "All ML model outputs must include feature importance scores and decision explanations in human-readable format for regulatory review.",
            "The platform must support multi-entity resolution across accounts, customers, and counterparties with configurable matching rules.",
            "Users must be able to define custom risk scenarios and run Monte Carlo simulations on demand.",
            "The system must generate regulatory reports in formats compliant with Basel III, MiFID II, and Dodd-Frank requirements.",
            "We need full audit logging of every data access, transformation, and model execution with tamper-proof storage.",
        ],
        "nonfunctional_reqs": [
            "Transaction scoring must complete within 50 milliseconds at the 99th percentile.",
            "The system must support concurrent access by at least 500 analysts without performance degradation.",
            "All data must be retained for a minimum of 7 years in compliance with SEC and FINRA regulations.",
            "The platform must achieve SOC 2 Type II compliance within 6 months of deployment.",
            "System failover must complete within 30 seconds with zero data loss for in-flight transactions.",
            "The platform must support data residency requirements across multiple jurisdictions including EU, US, and APAC.",
        ]
    },
    "Retail": {
        "concerns": ["inventory optimization", "customer experience", "real-time data", "supply chain visibility", "omnichannel consistency", "seasonal demand patterns"],
        "use_cases": ["demand forecasting", "customer segmentation", "pricing optimization", "supply chain analytics"],
        "problems": [
            "We're losing $2M per quarter in markdowns because our demand forecasting is off by 20-30%. We're either overstocked or out of stock on key SKUs.",
            "Our customer data is fragmented across online, mobile, and in-store systems. We can't build a unified customer profile, so our personalization efforts are basically guesswork.",
            "Supply chain disruptions are taking us 3-4 days to detect. By then, empty shelves have already cost us significant revenue and customer goodwill.",
            "Our pricing team is making decisions based on weekly reports. Competitors are adjusting prices hourly and we're always a step behind.",
        ],
        "functional_reqs": [
            "The system must ingest point-of-sale data from 2,500 stores within 5 minutes of each transaction.",
            "The platform must support customer identity resolution across online, mobile app, in-store, and loyalty program touchpoints.",
            "Users must be able to create and test pricing rules with A/B testing capabilities including geographic and demographic segmentation.",
            "The system must generate automated replenishment recommendations based on real-time inventory levels, lead times, and forecasted demand.",
            "We need a unified product catalog that reconciles SKUs across all channels with support for product hierarchy and attribute management.",
            "The platform must support what-if scenario modeling for promotional campaigns including cannibalization effects.",
        ],
        "nonfunctional_reqs": [
            "The demand forecasting engine must process predictions for 500,000 SKUs across all locations within a 2-hour batch window.",
            "The customer data platform must handle 50 million unique customer profiles with sub-second lookup times.",
            "The system must maintain data freshness of 15 minutes or less for inventory positions across all stores.",
            "Platform must support a Black Friday traffic spike of 20x normal volume without service degradation.",
            "All PII must be handled in compliance with GDPR, CCPA, and applicable regional privacy regulations.",
            "The system must support 99.9% availability during store operating hours with maintenance windows limited to 2 AM - 5 AM local time.",
        ]
    },
    "Manufacturing": {
        "concerns": ["IoT integration", "predictive maintenance", "supply chain optimization", "quality control", "OT/IT convergence", "digital twin accuracy"],
        "use_cases": ["operational efficiency", "equipment monitoring", "production analytics", "yield optimization"],
        "problems": [
            "Unplanned equipment downtime is costing us $500K per incident. We have sensors on everything but no way to correlate the data into predictive insights.",
            "Our quality defect rate has climbed to 3.2% and we can't trace root causes because production data and quality data live in completely separate systems.",
            "We're collecting 2TB of IoT data per day from the factory floor but only analyzing about 5% of it. The rest just sits in cold storage because we don't have the tools to process it.",
            "Our supply chain planning still relies on spreadsheets. When a supplier misses a delivery, it takes 2 days to understand the downstream impact on production schedules.",
        ],
        "functional_reqs": [
            "The system must ingest and process streaming data from 50,000 IoT sensors with support for OPC UA, MQTT, and Modbus protocols.",
            "The platform must support digital twin modeling for at least 200 pieces of critical equipment with real-time state synchronization.",
            "Users must be able to define custom anomaly detection rules combining sensor thresholds, temporal patterns, and equipment context.",
            "The system must provide automated root cause analysis that correlates quality defects with upstream process parameters within 30 seconds.",
            "We need a production scheduling optimizer that accounts for equipment availability, material constraints, and order priorities.",
            "The platform must support integration with MES, ERP, and SCADA systems through configurable connectors.",
        ],
        "nonfunctional_reqs": [
            "IoT data ingestion must support sustained throughput of 1 million events per second with at-most-once delivery guarantees.",
            "Anomaly detection alerts must fire within 5 seconds of the triggering sensor reading.",
            "The system must retain raw sensor data for 90 days in hot storage and 5 years in cold storage with seamless query across tiers.",
            "The platform must operate in air-gapped environments with no internet connectivity for classified production facilities.",
            "System must support edge computing deployment for latency-sensitive use cases with eventual consistency to the central platform.",
            "The platform must achieve 99.99% uptime for the real-time monitoring subsystem.",
        ]
    },
    "Technology": {
        "concerns": ["scalability", "API performance", "data pipeline efficiency", "cloud architecture", "multi-tenancy", "developer experience"],
        "use_cases": ["product analytics", "user behavior tracking", "system monitoring", "feature experimentation"],
        "problems": [
            "Our product analytics pipeline has a 4-hour lag. Product managers are making feature decisions based on yesterday's data while A/B tests are running in real time.",
            "We've got 15 different microservices each with their own data store and there's no way to answer cross-service business questions without a week-long data engineering project.",
            "Our current data platform can't handle multi-tenant isolation properly. One large customer's queries regularly slow down the entire system for everyone else.",
            "Developer onboarding for our data platform takes 3 weeks. The tooling is so complex that engineers spend more time fighting infrastructure than writing analytics logic.",
        ],
        "functional_reqs": [
            "The system must support real-time event streaming with exactly-once semantics for product analytics events.",
            "The platform must provide a self-service query interface where product managers can explore data without writing SQL.",
            "We need automated feature flag integration that correlates experiment assignments with behavioral outcomes across the full conversion funnel.",
            "The system must support multi-tenant data isolation with configurable compute and storage quotas per tenant.",
            "The platform must provide a unified semantic layer that abstracts across all 15 microservice data stores.",
            "We need automated data pipeline monitoring with SLA tracking, freshness alerts, and dependency-aware failure notifications.",
        ],
        "nonfunctional_reqs": [
            "Event ingestion must handle 500,000 events per second at peak with less than 100ms end-to-end latency.",
            "Query response times for standard dashboards must be under 3 seconds for 95th percentile.",
            "The platform must support at least 200 concurrent analytical users without query queueing.",
            "New data source onboarding must be completable by a developer in under 4 hours including schema definition and pipeline setup.",
            "The system must support blue-green deployments with zero-downtime upgrades.",
            "Data encryption must be enforced at rest and in transit with customer-managed encryption keys for enterprise tenants.",
        ]
    }
}

PARTICIPANT_ROLES = [
    "Solution Engineer",
    "Solution Architect",
    "Technical Lead",
    "Data Engineer",
    "Product Manager",
    "Customer Success Manager"
]

COMPANIES = [
    "Acme Corp", "TechVenture Inc", "Global Industries", "Innovate Solutions",
    "DataFirst", "CloudScale", "NextGen Systems", "PrimeWorks", "Vertex Group",
    "Summit Technologies", "Horizon Enterprises", "Catalyst Corp", "Quantum Systems",
    "Fusion Analytics", "Apex Solutions", "Pioneer Tech", "Velocity Group",
    "Meridian Health Systems", "Atlas Financial Group", "Pinnacle Retail",
    "Sterling Manufacturing", "Cobalt Technologies"
]

FIRST_NAMES = [
    "Sarah", "Michael", "Jennifer", "David", "Emily", "James", "Lisa", "Robert",
    "Amanda", "Chris", "Rachel", "Kevin", "Michelle", "Brian", "Nicole", "Tom",
    "Jessica", "Daniel", "Ashley", "Matthew", "Priya", "Carlos", "Wei", "Aisha"
]

LAST_NAMES = [
    "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
    "Martinez", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin", "Lee",
    "Thompson", "White", "Harris", "Clark", "Patel", "Chen", "Nakamura", "Okonkwo"
]

# Call archetypes determine the overall flow of the conversation
CALL_ARCHETYPES = [
    "problem_discovery",       # Heavy on pain points and current-state problems
    "requirements_gathering",  # Focus on functional and non-functional requirements
    "architecture_review",     # Deep dive on technical architecture
    "mixed",                   # Blend of all three
]

def generate_timestamp(base_time, seconds):
    """Generate timestamp in MM:SS format"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

def generate_participant_name(role):
    """Generate a participant with name and role"""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last} ({role})"

def pick_speaker(participants, last_speaker=None):
    """Pick a speaker, slightly biased away from the last speaker for realism"""
    if last_speaker and len(participants) > 2 and random.random() < 0.7:
        candidates = [p for p in participants if p != last_speaker]
        return random.choice(candidates)
    return random.choice(participants)

def append_line(lines, current_time, speaker, text, pause_range=(12, 25)):
    """Append a dialogue line and advance the clock"""
    lines.append((current_time, speaker, text))
    return current_time + random.randint(*pause_range)

def generate_opening(participants, company, vertical):
    """Generate call opening with agenda setting"""
    host = participants[0]
    host_name = host.split(" (")[0]

    lines = []
    t = 0
    t = append_line(lines, t, host,
        f"Good morning everyone, thanks for joining today's call. I'm {host_name} and I'll be facilitating our discussion on the Foundry IQ implementation for {company}.", (8, 12))
    t = append_line(lines, t, host,
        "Before we jump in, let me do a quick round of introductions so everyone knows who's on the line.", (6, 10))

    for p in participants[1:]:
        name = p.split(" (")[0]
        role = p.split("(")[1].rstrip(")")
        intros = [
            f"Hi everyone, {name} here. I'm the {role} on this engagement. Excited to be part of this.",
            f"Hey team, I'm {name}, serving as {role}. Looking forward to a productive session.",
            f"Good morning. {name}, {role}. I've been working closely with the {company} team on the pre-work for this.",
            f"Hi, {name} here, {role}. Happy to dive into the details today.",
        ]
        t = append_line(lines, t, p, random.choice(intros), (5, 8))

    t = append_line(lines, t, host,
        "Great. So for today's agenda, I'd like to cover the current challenges you're facing, walk through the Foundry IQ solution approach, and then discuss implementation specifics. Sound good?", (8, 12))

    affirmer = random.choice(participants[1:])
    t = append_line(lines, t, affirmer,
        "Sounds good. I'd also like to make sure we carve out time toward the end to talk about requirements and success criteria.", (6, 10))

    t = append_line(lines, t, host,
        "Absolutely, we'll make sure we get to that. Let's get started.", (5, 8))

    return lines, t


def generate_problem_segment(participants, vertical_data, start_time):
    """Generate a problem-articulation segment"""
    lines = []
    t = start_time
    last_speaker = None

    facilitator = participants[0]
    t = append_line(lines, t, facilitator,
        "Let's start by getting a clear picture of the current pain points. Can someone walk us through the biggest challenges you're facing today?", (10, 15))

    # Pick 2 problems and discuss them in depth
    problems = random.sample(vertical_data["problems"], min(2, len(vertical_data["problems"])))

    for i, problem in enumerate(problems):
        speaker = pick_speaker(participants[1:], last_speaker)
        last_speaker = speaker
        t = append_line(lines, t, speaker, problem, (15, 22))

        # Follow-up questions and deeper discussion
        questioner = pick_speaker(participants, speaker)
        followups = [
            "Can you quantify the business impact of that? Like, what does that translate to in terms of revenue or operational cost?",
            "How long has this been a problem? And what have you tried so far to address it?",
            "Is that affecting all teams equally or are certain groups hit harder than others?",
            "Walk me through a specific example. What does that look like day-to-day for your team?",
            "And that's with your current tooling? What are you using today for that workflow?",
        ]
        t = append_line(lines, t, questioner, random.choice(followups), (12, 18))

        responder = pick_speaker(participants, questioner)
        impact_responses = [
            f"We estimate it's costing us roughly $1.5 million annually in lost productivity alone. And that doesn't account for the downstream effects on customer satisfaction.",
            f"It's been building for about 18 months. We did a POC with another vendor last year but it didn't scale past the pilot phase. That's why we're looking at Foundry IQ now.",
            f"The operations team is definitely hit the hardest. They're the ones dealing with the manual workarounds every single day. But it cascades - leadership can't get accurate reports either.",
            f"Sure. Just last week, we had a situation where the data was 36 hours stale. The team made a decision based on that data and it cost us a significant customer escalation.",
            f"We're using a mix of custom scripts, some legacy ETL tools, and honestly a lot of Excel. It's not sustainable and everyone knows it.",
        ]
        t = append_line(lines, t, responder, random.choice(impact_responses), (15, 22))

        # Someone connects it to Foundry IQ
        connector = pick_speaker(participants, responder)
        bridges = [
            "This is actually a great use case for Foundry IQ's ontology layer. By unifying the data model, we can eliminate a lot of those manual reconciliation steps.",
            "I've seen Foundry IQ address exactly this kind of challenge at other organizations. The key is getting the data integration right from the start.",
            "So one of the things Foundry IQ does really well is handle that data fragmentation problem. The platform's designed to bring together heterogeneous data sources into a coherent model.",
            "That's helpful context. From a Foundry IQ perspective, we'd approach this by first building a comprehensive ontology that maps all those data relationships.",
        ]
        t = append_line(lines, t, connector, random.choice(bridges), (12, 18))

        if i < len(problems) - 1:
            transition = pick_speaker(participants, connector)
            t = append_line(lines, t, transition,
                "That makes sense. What about the other challenges? I know we had a few more items on the list.", (8, 12))

    return lines, t


def generate_requirements_segment(participants, vertical_data, start_time):
    """Generate functional and non-functional requirements discussion"""
    lines = []
    t = start_time
    last_speaker = None

    facilitator = participants[0]
    t = append_line(lines, t, facilitator,
        "Alright, let's shift gears and talk about requirements. I want to make sure we capture both the functional needs - what the system must do - and the non-functional requirements around performance, security, and reliability.", (12, 16))

    # --- Functional Requirements ---
    t = append_line(lines, t, facilitator,
        "Let's start with functional requirements. What are the must-have capabilities for Phase 1?", (8, 12))

    func_reqs = random.sample(vertical_data["functional_reqs"], min(4, len(vertical_data["functional_reqs"])))
    for req in func_reqs:
        speaker = pick_speaker(participants[1:], last_speaker)
        last_speaker = speaker
        t = append_line(lines, t, speaker, req, (15, 22))

        # Discussion around the requirement
        discusser = pick_speaker(participants, speaker)
        req_discussions = [
            "That's clear. From an implementation standpoint, Foundry IQ can support that through the Pipeline Builder. We'd configure the data flows to match those specifications.",
            "Got it. I want to flag that one as high priority. Can we put a hard requirement around that in the design document?",
            "Makes sense. We should also think about how that requirement evolves over the next 12-18 months. Is that scope likely to expand?",
            "Noted. I'll map that to the specific Foundry IQ modules we'll need to configure. That touches the ontology layer and possibly the Workshop application.",
            "Good. Let me make sure I understand the acceptance criteria there. Are we talking about a binary pass/fail or are there graduated levels of compliance?",
            "I agree that's critical. We'll want to build automated tests around that requirement so we can validate it continuously as the platform evolves.",
        ]
        t = append_line(lines, t, discusser, random.choice(req_discussions), (12, 18))

    # Transition to non-functional
    transitioner = pick_speaker(participants)
    t = append_line(lines, t, transitioner,
        "Good, those functional requirements are solid. Now let's talk about the non-functional side. Performance, scalability, security - what are the hard constraints?", (10, 14))

    # --- Non-Functional Requirements ---
    nonfunc_reqs = random.sample(vertical_data["nonfunctional_reqs"], min(4, len(vertical_data["nonfunctional_reqs"])))
    for req in nonfunc_reqs:
        speaker = pick_speaker(participants[1:], last_speaker)
        last_speaker = speaker
        t = append_line(lines, t, speaker, req, (15, 22))

        discusser = pick_speaker(participants, speaker)
        nfr_discussions = [
            "That's a rigorous target. We'll need to validate that during the load testing phase. I'd suggest we build performance benchmarks into the acceptance criteria.",
            "Understood. Foundry IQ's architecture is designed to meet that kind of SLA. We'll document the specific configuration needed to achieve it.",
            "I want to make sure we're being realistic there. Let me check with the infrastructure team on what's achievable with the current resource allocation.",
            "That aligns with what I've seen in similar deployments. We should plan for capacity testing early in the implementation timeline.",
            "Critical requirement. I'll make sure we build monitoring dashboards in Foundry IQ that track this metric continuously so we can catch any degradation early.",
            "Noted. That's a hard constraint, not a nice-to-have. We'll design the architecture with that as a non-negotiable baseline.",
        ]
        t = append_line(lines, t, discusser, random.choice(nfr_discussions), (12, 18))

    return lines, t


def generate_architecture_segment(participants, vertical_data, start_time):
    """Generate a deep technical architecture discussion"""
    lines = []
    t = start_time
    last_speaker = None

    concern = random.choice(vertical_data["concerns"])
    use_case = random.choice(vertical_data["use_cases"])

    architecture_discussions = [
        f"Let's talk about the architecture for {use_case}. I'm proposing a three-tier approach within Foundry IQ: raw ingestion layer, a transformation layer, and then the ontology-backed application layer.",
        "For the ingestion layer, we'll set up connectors to all your source systems. Foundry IQ supports both batch and streaming ingestion, so we can configure each source based on its latency requirements.",
        "The transformation layer is where the heavy lifting happens. We'll use Foundry IQ's Code Repositories to write and version-control all our data transformations. Everything runs as managed Spark jobs.",
        f"On the {concern} front, we need to implement data classification at the ontology level. Foundry IQ has a tagging system that lets us mark sensitive fields and automatically enforce access policies.",
        "I want to walk through the data model. We've identified about 20 core object types in the ontology. Each one maps to a business entity and has defined relationships to other objects.",
        "For the application layer, I'm recommending we use Workshop to build the operational interfaces. It gives us the flexibility to create custom workflows without a full frontend development cycle.",
        "We should discuss the build pipeline. I'm thinking we use incremental builds wherever possible to keep compute costs down. Foundry IQ's build scheduler is quite sophisticated for dependency management.",
        "What about the API layer? We'll need external systems to both push data in and pull insights out. The Foundry IQ API supports both REST and GraphQL patterns.",
        "One thing I want to flag is the importance of getting the ontology right. In my experience, about 60% of implementation issues trace back to an ontology that doesn't accurately represent the business domain.",
        "Let's talk about monitoring and observability. We need to instrument the pipelines so we know immediately when data quality drops or a pipeline fails.",
        "For the Quiver analytics layer, we should pre-compute the most common aggregations. This gives us sub-second query performance for the dashboards that get the most traffic.",
        "I'm recommending we implement a medallion architecture - bronze for raw data, silver for cleaned and conformed data, and gold for business-ready aggregations and ontology objects.",
        "We also need to plan for data lifecycle management. Not everything needs to live in hot storage forever. Foundry IQ supports tiered storage policies.",
        f"For the {use_case} workflow specifically, I want to build a feedback loop where the model outputs are validated against actual outcomes and the model is retrained on a configurable schedule.",
        "Let's talk about environments. We'll need at least three - development, staging, and production. Foundry IQ supports project-level isolation which maps well to this.",
        "Security architecture is critical here. I'm proposing we implement project-level RBAC, field-level access controls on the ontology, and network-level isolation for the production environment.",
        "One architecture decision we need to make is whether to use Foundry IQ's native compute or bring our own Kubernetes cluster. There are trade-offs either way.",
        "For the CI/CD pipeline, I'm recommending we use Foundry IQ's Checks framework to run automated data quality validations on every build before promoting to production.",
    ]

    random.shuffle(architecture_discussions)
    selected = architecture_discussions[:random.randint(12, 16)]

    for text in selected:
        speaker = pick_speaker(participants, last_speaker)
        last_speaker = speaker
        t = append_line(lines, t, speaker, text, (14, 22))

        # ~40% chance of a follow-up question/clarification
        if random.random() < 0.4:
            responder = pick_speaker(participants, speaker)
            clarifications = [
                "Can you elaborate on that? How does that compare to the approach we discussed in the pre-call?",
                "That makes sense. One question though - how does that handle the edge case where we have conflicting data from two different sources?",
                "I like that approach. Have you seen that pattern work at this scale before?",
                "Agreed. Let me add that to the architecture decision record so we have it documented.",
                "Good point. We should validate that assumption during the POC phase before committing to it for the full rollout.",
                "Quick question on that - does Foundry IQ support that natively or would we need to build a custom extension?",
            ]
            t = append_line(lines, t, responder, random.choice(clarifications), (12, 18))

    return lines, t


def generate_closing(participants, start_time):
    """Generate call closing with action items"""
    lines = []
    t = start_time

    facilitator = participants[0]
    fac_name = facilitator.split(" (")[0]

    t = append_line(lines, t, facilitator,
        "We're getting close to time, so let me try to summarize the key takeaways and action items.", (8, 12))

    action_items = [
        f"I'll circulate the updated architecture diagram and ontology mapping by end of week for everyone to review.",
        "We need to finalize the data source inventory and get access credentials for the development environment.",
        "I'll draft the requirements document based on today's discussion and send it out for review by Thursday.",
        "Let's schedule a follow-up session specifically focused on the security and compliance architecture.",
        "I'll set up the Foundry IQ development environment so the team can start hands-on exploration.",
        "We should loop in the infrastructure team for the next call to discuss compute provisioning and network configuration.",
    ]

    selected_actions = random.sample(action_items, random.randint(3, 4))
    for action in selected_actions:
        speaker = pick_speaker(participants)
        t = append_line(lines, t, speaker, action, (10, 15))

    t = append_line(lines, t, facilitator,
        "Great. I'll send out meeting notes and the follow-up calendar invite today. Any final questions before we wrap?", (8, 12))

    closer = pick_speaker(participants[1:])
    closing_remarks = [
        "No, I think we covered a lot of ground today. Really productive session. Thanks everyone.",
        "Just want to say this was a great discussion. I feel much more confident about the Foundry IQ approach now.",
        "Nothing from my side. Appreciate everyone's time. Looking forward to the next steps.",
        "All good here. Let's keep the momentum going. Excited to see this come together.",
    ]
    t = append_line(lines, t, closer, random.choice(closing_remarks), (6, 10))

    t = append_line(lines, t, facilitator,
        f"Thanks everyone. Talk to you next week. Have a great rest of your day.", (5, 8))

    return lines, t


def generate_call(call_id, vertical, archetype):
    """Generate a single fake customer call targeting ~10 minutes"""
    vertical_data = VERTICALS[vertical]
    company = random.choice(COMPANIES)

    num_participants = random.randint(3, 5)
    selected_roles = random.sample(PARTICIPANT_ROLES, num_participants)
    participants = [generate_participant_name(role) for role in selected_roles]

    transcript = []

    # Opening (~1-1.5 min)
    opening_lines, t = generate_opening(participants, company, vertical)
    transcript.extend(opening_lines)

    # Main body based on archetype (~7-8 min)
    if archetype == "problem_discovery":
        seg, t = generate_problem_segment(participants, vertical_data, t)
        transcript.extend(seg)
        seg, t = generate_architecture_segment(participants, vertical_data, t)
        transcript.extend(seg)

    elif archetype == "requirements_gathering":
        # Brief problem context then deep requirements
        seg, t = generate_problem_segment(participants, vertical_data, t)
        transcript.extend(seg)
        seg, t = generate_requirements_segment(participants, vertical_data, t)
        transcript.extend(seg)

    elif archetype == "architecture_review":
        seg, t = generate_architecture_segment(participants, vertical_data, t)
        transcript.extend(seg)
        seg, t = generate_requirements_segment(participants, vertical_data, t)
        transcript.extend(seg)

    else:  # mixed
        seg, t = generate_problem_segment(participants, vertical_data, t)
        transcript.extend(seg)
        seg, t = generate_requirements_segment(participants, vertical_data, t)
        transcript.extend(seg)
        seg, t = generate_architecture_segment(participants, vertical_data, t)
        transcript.extend(seg)

    # Closing (~1 min)
    closing_lines, t = generate_closing(participants, t)
    transcript.extend(closing_lines)

    # Format
    call_transcript = "=" * 80 + "\n"
    call_transcript += f"CALL #{call_id:03d} - {company} ({vertical})\n"
    call_transcript += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
    call_transcript += f"Duration: ~{t // 60} minutes\n"
    call_transcript += f"Participants: {len(participants)}\n"
    call_transcript += f"Call Type: {archetype.replace('_', ' ').title()}\n"
    call_transcript += "=" * 80 + "\n\n"

    for time_sec, speaker, text in transcript:
        timestamp = generate_timestamp(0, time_sec)
        call_transcript += f"[{timestamp}] {speaker}:\n{text}\n\n"

    return call_transcript, {
        "call_id": call_id,
        "company": company,
        "vertical": vertical,
        "call_type": archetype,
        "participants": participants,
        "duration_seconds": t,
        "duration_minutes": round(t / 60, 1)
    }


def main():
    print("Generating 50 fake customer calls for Foundry IQ implementation testing...\n")

    all_transcripts = []
    metadata = []

    verticals_list = list(VERTICALS.keys())

    for i in range(1, 51):
        vertical = verticals_list[(i - 1) % len(verticals_list)]
        archetype = CALL_ARCHETYPES[(i - 1) % len(CALL_ARCHETYPES)]
        print(f"Generating call {i}/50 ({vertical} - {archetype})...")

        transcript, meta = generate_call(i, vertical, archetype)
        all_transcripts.append(transcript)
        metadata.append(meta)

    output_file = "fake_customer_calls_2.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for transcript in all_transcripts:
            f.write(transcript)
            f.write("\n\n")

    metadata_file = "calls_metadata_2.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✓ Generated 50 calls successfully!")
    print(f"✓ Transcripts saved to: {output_file}")
    print(f"✓ Metadata saved to: {metadata_file}")

    print("\nSummary:")
    for vertical in verticals_list:
        count = sum(1 for m in metadata if m['vertical'] == vertical)
        print(f"  - {vertical}: {count} calls")

    print("\nCall types:")
    for archetype in CALL_ARCHETYPES:
        count = sum(1 for m in metadata if m['call_type'] == archetype)
        print(f"  - {archetype.replace('_', ' ').title()}: {count} calls")

    durations = [m['duration_minutes'] for m in metadata]
    print(f"\nDuration stats:")
    print(f"  Average: {sum(durations)/len(durations):.1f} min")
    print(f"  Min:     {min(durations):.1f} min")
    print(f"  Max:     {max(durations):.1f} min")

if __name__ == "__main__":
    main()
