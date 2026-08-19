\# Warehouse Star Schema



The warehouse presentation layer uses a classic star schema.



\## Fact



\### Fact\_OutreachActivity



Grain:



> One row per individual outreach interaction event.



Examples:



\- Invite Sent

\- Invite Accepted

\- Message Sent

\- Reply Received



\## Dimensions



\### Dim\_Agent



Grain:



> One row per LinkedIn agent/account version.



SCD strategy:



> Type 2



\### Dim\_Lead



Grain:



> One row per targeted LinkedIn lead.



SCD strategy:



> Type 1



\### Dim\_Campaign



Grain:



> One row per outreach campaign.



SCD strategy:



> Type 1



\### Dim\_Date



Grain:



> One row per calendar day.



\## Relationships



Fact\_OutreachActivity connects to:



\- Dim\_Agent through AgentSK

\- Dim\_Lead through LeadSK

\- Dim\_Campaign through CampaignSK

\- Dim\_Date through DateSK

