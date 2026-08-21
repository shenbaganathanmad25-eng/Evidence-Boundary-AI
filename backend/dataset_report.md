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
| 1 | `state` | str | 47,590 | 0 | 0.00% |
| 2 | `district` | str | 47,589 | 1 | 0.00% |
| 3 | `university_type` | str | 47,589 | 1 | 0.00% |
| 4 | `university_name` | str | 47,589 | 1 | 0.00% |
| 5 | `college_name` | str | 47,589 | 1 | 0.00% |
| 6 | `college_type` | str | 47,589 | 1 | 0.00% |
| 7 | `address` | str | 44,531 | 3,059 | 6.43% |
| 8 | `website` | str | 36,097 | 11,493 | 24.15% |
| 9 | `management` | str | 44,531 | 3,059 | 6.43% |
| 10 | `specialization` | str | 47,590 | 0 | 0.00% |
| 11 | `location_type` | str | 44,531 | 3,059 | 6.43% |
| 12 | `university_id` | str | 47,589 | 1 | 0.00% |
| 13 | `college_id` | str | 47,589 | 1 | 0.00% |

### 3. Duplicate Rows Check
- **Total Exact Duplicate Rows**: `0`

### 4. Cardinality & Unique Values per Column
| Column Name | Unique Values Count | Top Value Example |
|---|---|---|
| `state` | 37 | `uttar pradesh` |
| `district` | 705 | `bengaluru urban` |
| `university_type` | 9 | `State Public University ` |
| `university_name` | 442 | `makhanlal chaturvedi national university` |
| `college_name` | 47,070 | `government college of nursing` |
| `college_type` | 7 | `affiliated college` |
| `address` | 43,471 | `, ,` |
| `website` | 32,981 | `www.sinhgad.edu` |
| `management` | 7 | `private un-aided` |
| `specialization` | 13 | `Not Specified` |
| `location_type` | 3 | `Rural` |
| `university_id` | 442 | `U-0283` |
| `college_id` | 47,590 | `C-10` |

### 5. Sample Records (First 10 Rows)
| College Name | University Name | State | District | College Type | Management | Specialization |
|---|---|---|---|---|---|---|
| `jawaharlal nehru rajkeeya  mah` | `pondicherry univeristy, puduch` | andaman and nicobar islands | nicobars | affiliated college | central government | Not Specified |
| `regional medical research inst` | `pondicherry univeristy, puduch` | andaman and nicobar islands | nicobars | affiliated college | central government | Medical & Health Sciences |
| `tagore government college of e` | `pondicherry univeristy, puduch` | andaman and nicobar islands | nicobars | affiliated college | state government | Education |
| `zoological survey of india` | `pondicherry univeristy, puduch` | andaman and nicobar islands | nicobars | affiliated college | central government | Science |
| `mahatma gandhi govt. college` | `pondicherry univeristy, puduch` | andaman and nicobar islands | north and middle andaman | affiliated college | central government | Not Specified |
| `andaman and nicobar inslands i` | `pondicherry univeristy, puduch` | andaman and nicobar islands | south andamans | affiliated college | central government | Medical & Health Sciences |
| `andaman college (ancol)` | `pondicherry univeristy, puduch` | andaman and nicobar islands | south andamans | affiliated college | central government | Not Specified |
| `andaman law college` | `pondicherry univeristy, puduch` | andaman and nicobar islands | south andamans | affiliated college | state government | Law |
| `dr.b.r. ambedkar institute of ` | `pondicherry univeristy, puduch` | andaman and nicobar islands | south andamans | affiliated college | central government | Not Specified |
| `college of agricultural engine` | `acharya ng ranga agricultural ` | andhra pradesh | anantapur | constituent / university college | state government | Engineering & Technology |

### 6. Evidence Verification Column Mapping Strategy
The raw `Colleges_India.csv` dataset contains tabular metadata on Indian higher education institutions.
To train the **Evidence Boundary AI Verification Model**, structured claim-evidence verification pairs are constructed:
- **Evidence Context**: Synthesized from factual record fields (`college_name`, `university_name`, `state`, `district`, `college_type`, `management`, `specialization`, `address`).
- **Claim**: Structured assertion regarding college location, affiliation, type, specialization, or unverified external facts.
- **Target Label**: Classified into 3 standard verification classes:
  1. `SUPPORTS`: Claim directly matches factual record.
  2. `REFUTES`: Claim contradicts factual record (e.g. wrong district, wrong state, wrong university affiliation).
  3. `NOT_ENOUGH_INFO`: Claim makes assertions outside available evidence boundary (e.g., student capacity, tuition fees, founding date).