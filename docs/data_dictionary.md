\# Data Dictionary



\## Purpose



This document defines the warehouse tables, columns, data types,

keys, SCD strategies, and business rules for the LinkedIn Agent

Analytics Platform.



The warehouse uses a star schema consisting of:



\- Dim\_Agent

\- Dim\_Lead

\- Dim\_Campaign

\- Dim\_Date

\- Fact\_OutreachActivity



\---



\# 1. Dim\_Agent



\### Grain



One row per LinkedIn agent/account version.



\### SCD Strategy



SCD Type 2.



Historical versions are retained when tracked agent attributes

change.



| Column | Business Name | Data Type | Key Type | SCD | Business Definition / Rule |

|---|---|---|---|---|---|

| `agent\_sk` | AgentSK | BIGINT | Primary Key | N/A | Auto-generated surrogate key representing a specific agent dimension version. |

| `agent\_id` | AgentID | VARCHAR(100) | Natural Key | N/A | Unique identifier assigned to the source platform. |

| `agent\_name` | AgentName | VARCHAR(255) | Attribute | Type 2 | Name associated with the LinkedIn agent account. |

| `linkedin\_email` | LinkedInEmail | VARCHAR(255) | Attribute | Type 2 | Email associated with the agent account. |

| `account\_age\_tier` | AccountAgeTier | VARCHAR(50) | Attribute | Type 2 | Account age classification such as `<1 Month`, `1 Month`, `2-6 Months`, `6-12 Months`, or `1+ Year`. |

| `risk\_classification` | RiskClassification | VARCHAR(100) | Attribute | Type 2 | Risk classification such as `Very High Risk`, `High Risk`, `Moderate Risk`, `Low Risk`, or `Minimal Risk`. |

| `max\_daily\_invites` | MaxDailyInvites | INTEGER | Attribute | Type 2 | Maximum permitted daily invite capability based on the applicable account/risk rules. |

| `max\_daily\_messages` | MaxDailyMessages | INTEGER | Attribute | Type 2 | Maximum permitted daily message capability. |

| `status` | Status | VARCHAR(50) | Attribute | Type 2 | Current account status, such as Active, Paused, or Ghosted. |

| `effective\_date` | EffectiveDate | TIMESTAMPTZ | Metadata | Type 2 | Timestamp from which this dimension version becomes effective. |

| `expiration\_date` | ExpirationDate | TIMESTAMPTZ | Metadata | Type 2 | Timestamp at which this dimension version stops being effective. NULL for the current version. |

| `is\_current\_flag` | IsCurrentFlag | BOOLEAN | Metadata | Type 2 | TRUE when this is the current version of the agent. |

| `created\_at` | CreatedAt | TIMESTAMPTZ | Metadata | N/A | Timestamp when the warehouse record was created. |

| `updated\_at` | UpdatedAt | TIMESTAMPTZ | Metadata | N/A | Timestamp when the warehouse record was last updated. |



\### SCD Type 2 example



```text

agent\_sk | agent\_id | risk\_classification | is\_current

\---------|----------|---------------------|------------

101      | A001     | Minimal Risk        | FALSE

205      | A001     | Moderate Risk       | TRUE


# 9. DQ_Results_History

### Grain

One row per pipeline execution.

### Purpose

Stores historical data quality results for long-term monitoring,
trend analysis, and Power BI reporting.

| Column | Business Name | Data Type | Key Type | SCD | Business Definition / Rule |
|---|---|---|---|---|---|
| `run_id` | RunID | BIGINT | Composite Primary Key / FK | N/A | Identifies the pipeline execution that produced the DQ result. |
| `execution_timestamp` | ExecutionTimestamp | TIMESTAMPTZ | Composite Primary Key | N/A | Timestamp at which the DQ evaluation occurred. |
| `completeness_score` | CompletenessScore | DECIMAL(5,2) | Metric | N/A | Percentage score for completeness checks, from 0 to 100. |
| `uniqueness_score` | UniquenessScore | DECIMAL(5,2) | Metric | N/A | Percentage score for uniqueness checks, from 0 to 100. |
| `validity_score` | ValidityScore | DECIMAL(5,2) | Metric | N/A | Percentage score for validity checks, from 0 to 100. |
| `timeliness_score` | TimelinessScore | DECIMAL(5,2) | Metric | N/A | Percentage score for timeliness/freshness checks, from 0 to 100. |
| `referential_integrity_score` | ReferentialIntegrityScore | DECIMAL(5,2) | Metric | N/A | Percentage score for foreign-key integrity checks, from 0 to 100. |
| `composite_dq_score` | CompositeDQScore | DECIMAL(5,2) | Metric | N/A | Weighted overall DQ score. Pipeline passes when score is at least 95%. |
| `pass_fail_status` | PassFailStatus | VARCHAR(10) | Status | N/A | `PASS` when the DQ deployment gate succeeds; otherwise `FAIL`. |
| `failed_test_count` | FailedTestCount | INTEGER | Metric | N/A | Number of failed DQ tests for the pipeline execution. |
| `error_message` | ErrorMessage | VARCHAR(500) | Attribute | N/A | Error or failure information associated with the DQ evaluation. |
| `created_at` | CreatedAt | TIMESTAMPTZ | Metadata | N/A | Timestamp when the DQ history record was created. |
