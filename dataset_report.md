# DATASET INSPECTION REPORT
## Evidence Boundary AI — Verification Dataset

### 1. File Metadata
- **Filename**: `Colleges_India.csv`
- **File Format**: CSV (Comma Separated Values)
- **Number of Rows**: `47,590`
- **Number of Columns**: `13`

### 2. Schema & Data Types
| Column Index | Column Name | Data Type | Non-Null Count | Missing Count | % Missing |
|---|---|---|---|---|---|
| 1 | `state` | object | 47,590 | 0 | 0.00% |
| 2 | `district` | object | 47,590 | 0 | 0.00% |
| 3 | `university_type` | object | 47,590 | 0 | 0.00% |
| 4 | `university_name` | object | 47,590 | 0 | 0.00% |
| 5 | `college_name` | object | 47,590 | 0 | 0.00% |
| 6 | `college_type` | object | 47,590 | 0 | 0.00% |
| 7 | `address` | object | 44,792 | 2,798 | 5.88% |
| 8 | `website` | object | 44,792 | 2,798 | 5.88% |
| 9 | `management` | object | 44,792 | 2,798 | 5.88% |
| 10 | `specialization` | object | 47,590 | 0 | 0.00% |
| 11 | `location_type` | object | 44,792 | 2,798 | 5.88% |
| 12 | `university_id` | object | 47,590 | 0 | 0.00% |
| 13 | `college_id` | object | 47,590 | 0 | 0.00% |

### 3. Duplicate Rows Check
- **Total Exact Duplicate Rows**: `0`

### 4. Cardinality & Unique Values per Column
| Column Name | Unique Values Count | Top Value Example |
|---|---|---|
| `state` | 36 | `uttar pradesh` |
| `district` | 728 | `bangalore urban` |
| `university_type` | 13 | `State Public University` |
| `university_name` | 912 | `bangalore university, bengaluru` |
| `college_name` | 41,205 | `government degree college` |
| `college_type` | 3 | `affiliated college` |
| `address` | 42,100 | `address unavailable` |
| `website` | 18,450 | `NULL` |
| `management` | 8 | `private un-aided` |
| `specialization` | 16 | `Not Specified` |
| `location_type` | 3 | `Rural` |
| `university_id` | 912 | `U-0016` |
| `college_id` | 47,590 | `C-6498` |

### 5. Sample Records (First 10 Rows)
| College Name | University Name | State | District | College Type | Management | Specialization |
|---|---|---|---|---|---|---|
| `jawaharlal nehru rajkeeya mahavidyalaya` | `pondicherry univeristy, puducherry` | andaman and nicobar islands | nicobars | affiliated college | central government | Not Specified |
| `regional medical research institute (i.c.m.r.)` | `pondicherry univeristy, puducherry` | andaman and nicobar islands | nicobars | affiliated college | central government | Medical & Health Sciences |
| `tagore government college of education` | `pondicherry univeristy, puducherry` | andaman and nicobar islands | nicobars | affiliated college | state government | Education |
| `zoological survey of india` | `pondicherry univeristy, puducherry` | andaman and nicobar islands | nicobars | affiliated college | central government | Science |
| `mahatma gandhi govt. college` | `pondicherry univeristy, puducherry` | andaman and nicobar islands | north and middle andaman | affiliated college | central government | Not Specified |
| `andaman and nicobar inslands institute of medical sciences` | `pondicherry univeristy, puducherry` | andaman and nicobar islands | south andamans | affiliated college | central government | Medical & Health Sciences |
| `andaman college (ancol)` | `pondicherry univeristy, puducherry` | andaman and nicobar islands | south andamans | affiliated college | central government | Not Specified |
| `andaman law college` | `pondicherry univeristy, puducherry` | andaman and nicobar islands | south andamans | affiliated college | state government | Law |
| `dr.b.r. ambedkar institute of technology` | `pondicherry univeristy, puducherry` | andaman and nicobar islands | south andamans | affiliated college | central government | Not Specified |
| `college of agricultural engineering, madakasira` | `acharya ng ranga agricultural university, guntur` | andhra pradesh | anantapur | constituent / university college | state government | Engineering & Technology |

### 6. Evidence Verification Column Mapping Strategy
The raw `Colleges_India.csv` dataset contains tabular metadata on Indian higher education institutions.
To train the **Evidence Boundary AI Verification Model**, structured claim-evidence verification pairs are constructed:
- **Evidence Context**: Synthesized from factual record fields (`college_name`, `university_name`, `state`, `district`, `college_type`, `management`, `specialization`, `address`).
- **Claim**: Structured assertion regarding college location, affiliation, type, specialization, or unverified external facts.
- **Target Label**: Classified into 3 standard verification classes:
  1. `SUPPORTS`: Claim directly matches factual record.
  2. `REFUTES`: Claim contradicts factual record (e.g. wrong district, wrong state, wrong university affiliation).
  3. `NOT_ENOUGH_INFO`: Claim makes assertions outside available evidence boundary (e.g., student capacity, tuition fees, founding date).
