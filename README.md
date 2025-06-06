# Privacy Workshop Cup 2022 - Data Anonymization & De-anonymization System

This project was developed for the **Privacy Workshop Cup 2022**, a data anonymization and de-anonymization capture-the-flag competition held in Japan. Our team achieved **4th place out of 15 teams in the defense phase**.

## Project Overview

The system implements a privacy-preserving data processing pipeline using:

- **Multi-threading and Multi-processing** on multi-core servers
- **Genetic algorithm-based encryption algorithm**, incorporating privacy engineering techniques:
  - *k-anonymity*
  - *Differential Privacy*
  - Other privacy engineering methods
- **Monte Carlo method-based decryption algorithm** for re-identification

The core components are:

1. **Data Anonymization**  
   - Leverages genetic algorithms to evolve optimal encryption keys.  
   - Incorporates privacy metrics to ensure data remains anonymized.

2. **Data De-anonymization**  
   - Uses a Monte Carlo-based approach with parallel processing to reverse-engineer potential data mappings.

## Technologies Used

- **Python (multi-threading and multi-processing)**
- **Genetic Algorithms**
- **Monte Carlo Methods**
- **Privacy Engineering (k-anonymity, Differential Privacy)**

## Outcome

- **4th place in the defense phase** (15 teams participated).  
- The system balanced high privacy protection with computational efficiency.

## Acknowledgments

Thanks to the PWS Cup 2022 organizers for providing the platform and to my teammates for their collaboration and feedback.
