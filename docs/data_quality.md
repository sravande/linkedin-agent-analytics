\# Data Quality Framework



\## Quality Dimensions



The platform validates five core data quality dimensions:



1\. Completeness

2\. Uniqueness

3\. Validity

4\. Timeliness

5\. Referential Integrity



\## Completeness



Required fact fields must not be NULL.



Critical fields include:



\- AgentSK

\- LeadSK

\- DateSK

\- InteractionID

\- InteractionType

\- EventTimestamp



\## Uniqueness



InteractionID must uniquely identify an outreach event.



Duplicate event identifiers are rejected from the warehouse load.



\## Validity



Business-domain values are validated against approved values.



\### Account Age Tier



\- <1 Month

\- 1 Month

\- 2-6 Months

\- 6-12 Months

\- 1+ Year



\### Risk Classification



\- Very High Risk

\- High Risk

\- Moderate Risk

\- Low Risk

\- Minimal Risk



\### Interaction Type



\- INVITE\_SENT

\- INVITE\_ACCEPTED

\- MESSAGE\_SENT

\- REPLY\_RECEIVED



Numeric measures are also validated.



For example:



\- Response time cannot be negative.

\- Daily limit utilisation must be between 0 and 100 percent.

\- Event counts cannot be negative.



\## Timeliness



Event timestamps must not be in the future.



A configurable freshness SLA can also be applied to determine

whether the source data has been refreshed within the expected

operational window.



\## Referential Integrity



Fact foreign keys must resolve to valid dimension records.



The following relationships are validated:



```text

Fact\_OutreachActivity.AgentSK

&#x20;   -> Dim\_Agent.AgentSK



Fact\_OutreachActivity.LeadSK

&#x20;   -> Dim\_Lead.LeadSK



Fact\_OutreachActivity.CampaignSK

&#x20;   -> Dim\_Campaign.CampaignSK



Fact\_OutreachActivity.DateSK

&#x20;   -> Dim\_Date.DateSK

