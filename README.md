# Hit_Expansion_Generative_Modelling

This repository contains the source code for our Small Molecule Targeted Generative Modelling API, a project for Artificial Intelligence in Drug Discovery, a module from the Medical Informatics MSc at fachhochschule nordwestschweiz (FHNW), Muttenz, Switzerland. Our tool consist on a user-friendly interface for hit expansion that given a initial hit the suer can expand its hit with similar compound with varied properties.

## Introduction
The exploration and generation of novel molecular structures is a critical aspect of drug discovery and related fields. Traditional methods can be time-consuming and expensive, making the use of computational models increasingly attractive. Our API utilizes a generative model approach, learning from a large dataset of molecular structures expressed in the SELFIES language - a 100% robust molecular string representation developed in [1].

The generative model employed here wasd eveloped in [2] and is available through the HuggingFace infrastructure. The authors developed a Molecular language model as a multi task generator and is capable of producing molecular structures with properties similar to those of the given hit. 

Recognizing the challenge in comparing and ranking different generative models, we externally validated the large language model with the Molecular Sets (MOSES) benchmarking platform developed in [3]. MOSES provides training and testing datasets, along with a comprehensive set of metrics to evaluate the quality and diversity of generated structures. 

The API facilitates easy integration of our generative modelling tool into existing workflows and applications, accelerating the process of molecular discovery and design.
## API Usage

1. Clone repository
```
git clone git@github.com:molinamarcvdb/Small_Mol_Gen_Mod_Api.git
```
2. Install dependencies
```
python -m pip install -r requirements.txt
```
3. Download molecule properties prediction model available at the link and add it to the project directory. Link: https://drive.google.com/file/d/1d_c_jOZzhrnhEHDYTg1VU6UvHpa4vbB4/view?usp=sharing


## References

[1] Krenn, M., Häse, F., Nigam, A., Friederich, P., & Aspuru-Guzik, A. (2020). Self-Referencing Embedded Strings (SELFIES): A 100% robust molecular string representation. Machine Learning: Science and Technology, 1(4), 045024. https://doi.org/10.1088/2632-2153/aba947

[2] Fang, Y., Zhang, N., Chen, Z., Fan, X., & Chen, H. (2023, May 18). Domain-Agnostic Molecular Generation with Self-feedback. ArXiv.org. https://doi.org/10.48550/arXiv.2301.11259

[3] Polykovskiy, D., Zhebrak, A., Sanchez-Lengeling, B., Golovanov, S., Tatanov, O., Belyaev, S., Kurbanov, R., Artamonov, A., Aladinskiy, V., Veselov, M., Kadurin, A., Johansson, S., Chen, H., Nikolenko, S., Aspuru-Guzik, A., & Zhavoronkov, A. (2020). Molecular Sets (MOSES): A Benchmarking Platform for Molecular Generation Models. Frontiers in Pharmacology, 11. https://doi.org/10.3389/fphar.2020.565644

