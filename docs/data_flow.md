\# End-to-End Data Flow



\## 1. Architecture Overview



The LinkedIn Agent Analytics Platform follows an incremental

ELT/ETL architecture from source API ingestion through the

warehouse presentation layer and finally into Power BI.



```text

┌─────────────────────────────────────┐

│ LinkedIn Agent / Polluxa API        │

│                                     │

│ - Agent metadata                    │

│ - Lead records                      │

│ - Outreach events                   │

└──────────────────┬──────────────────┘

&#x20;                  │

&#x20;                  │ REST API

&#x20;                  │ Incremental extraction

&#x20;                  │ Watermark

&#x20;                  ▼

┌─────────────────────────────────────┐

│ Python Ingestion Layer              │

│                                     │

│ - Authentication                    │

│ - API requests                      │

│ - Retry / exponential backoff       │

│ - Rate-limit handling               │

│ - Incremental extraction            │

└──────────────────┬──────────────────┘

&#x20;                  │

&#x20;                  ▼

┌─────────────────────────────────────┐

│ PostgreSQL Staging Layer             │

│                                     │

│ - Raw / staging records             │

│ - Pipeline metadata                 │

│ - Watermarks                        │

│ - Dead-letter records               │

└──────────────────┬──────────────────┘

&#x20;                  │

&#x20;                  │ Validation

&#x20;                  ▼

┌─────────────────────────────────────┐

│ Data Quality \& Transformation       │

│                                     │

│ - Required-field validation         │

│ - Type validation                   │

│ - Duplicate detection               │

│ - Invalid records → Dead Letter     │

│ - Business transformations          │

└──────────────────┬──────────────────┘

&#x20;                  │

&#x20;                  ▼

┌─────────────────────────────────────┐

│ Warehouse Presentation Layer        │

│                                     │

│ Dim\_Agent                           │

│ Dim\_Lead                            │

│ Dim\_Campaign                        │

│ Dim\_Date                            │

│ Fact\_OutreachActivity               │

└──────────────────┬──────────────────┘

&#x20;                  │

&#x20;                  │ SQL / Semantic Model

&#x20;                  ▼

┌─────────────────────────────────────┐

│ Power BI Analytics Layer            │

│                                     │

│ - DAX measures                      │

│ - KPI calculations                  │

│ - Agent analytics                   │

│ - Campaign analytics                │

│ - Outreach performance              │

└─────────────────────────────────────┘

