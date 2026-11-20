# Latent Profiles of Academic Achievement Among Rural Students in Peru

Code, processed results and specifications for the paper:

> Arenas Cancapa, K. M., & Huiza Pereyra, E. R. (2026). *Latent Profiles of Academic Achievement Among Rural Students in Peru: An Integrated EFA–IRT–LCA Analysis of PISA Data.* WAIMLAp 2026, Springer.

The pipeline combines **Exploratory Factor Analysis (EFA)**, **Item Response Theory (IRT)** and **Latent Class Analysis (LCA)** on PISA 2022 microdata for Peru (n = 6,968), with a focus on the rural subsample (n = 3,720). A national replication uses PISA 2018 (n = 6,086).

| Stage | Rural 2022 | National 2022 | National 2018 |
|---|---|---|---|
| Students | 3,720 | 6,968 | 6,086 |
| Variables after preprocessing (from 7,147) | 573 | 592 | 438 |
| Items retained by EFA | 198 | 235 | 229 |
| Items retained by IRT (a ≥ 0.50) | 129 | 152 | 161 |
| LCA solution | 4 classes (entropy 0.9753) | 7 classes | see paper |

**Results API:** `<URL pending>`

## 1. Get the PISA microdata

Raw PISA data are **not** included in this repository. Download them from the OECD:

- PISA 2022: https://www.oecd.org/en/data/datasets/pisa-2022-database.html
- PISA 2018: https://www.oecd.org/en/data/datasets/pisa-2018-database.html

Download the SAS data files for the student questionnaire, school questionnaire, teacher questionnaire, cognitive items and timing (`STU_QQQ`, `SCH_QQQ`, `TCH_QQQ`, `STU_COG`, `STU_TIM`, and `CRT_COG` for 2022). Place them under `data/` (the folder is git-ignored).

## 2. Environment

Python 3.11. Exact package versions are pinned in `requirements.txt`.

```bash
docker compose up --build     # JupyterLab at http://localhost:8888
```

The repository is mounted at `/workspace` inside the container; the notebooks read and write data under `/workspace/data/`. Without Docker: `pip install -r requirements.txt`.

## 3. Execution order

**Data preparation (`src/`)**

| # | Notebook | Purpose | Output |
|---|---|---|---|
| 0a | `src/sas_to_csv.ipynb` | Convert OECD SAS files to CSV | `data/collection_csv/*.csv` |
| 0b | `src/segment_variables.ipynb` | Keep Peru only (`CNT == "PER"`) | `data/collection_peru_csv/*.csv` |
| 0c | `src/merge_data_collection.ipynb` | Merge student, school, teacher and cognitive files | `data/collection_peru_csv/data_merge/COLLECT_COMP_PERU.csv` (6,968 × 7,147) |

**Analysis pipeline — rural sample (`notebooks_rural/`)**

| # | Notebook | Purpose | Main outputs |
|---|---|---|---|
| 1 | `01_data_cleansing/paso1_filtrado_pisa.ipynb` | Rural filter + 5 preprocessing filters | `dataset_filtrado.csv`, `plausible_values_referencia.csv`, `log_columnas_eliminadas.csv`, `mapeo_categoricos.json` |
| 2 | `02_learning/paso2_efa_por_bloques.ipynb` | EFA by thematic blocks | `efa_cargas_factoriales.csv`, `dataset_efa_items_seleccionados.csv`, `efa_resumen_top_items_por_factor.csv` |
| 3 | `02_learning/paso3_irt.ipynb` | IRT calibration (2PL / GRM) | `irt_parametros_todos.csv`, `irt_parametros_retenidos.csv`, `dataset_irt_items_finales.csv` |
| 4 | `02_learning/paso4_lca.ipynb` | LCA model selection and class assignment | `lca_resumen_ajuste.csv`, `dataset_lca_clases.csv`, `lca_rendimiento_por_clase.csv` |
| 5 | `03_interpretation/paso6_perfiles_clases.ipynb` | Class profiles, ANOVA validation, context | `tabla_perfiles_clases.csv`, `tabla_anova_factores.csv`, `tabla_contexto_*.csv` |
| 6 | `04_graphics/figures_pipeline.ipynb` | Paper figures | `04_graphics/figuras_articulo/*.png` |

**National samples (`notebooks/`)** — same steps 1–5 without the rural filter. The 2018 replication uses the same notebooks with the input/output paths set to the 2018 files.

## 4. Parameters

All values below are the ones used for the published results (`random_state = 42`).

| Stage | Parameter | Value |
|---|---|---|
| Rural filter | `SC001Q01TA` | "village/rural area (< 3,000)" and "small town (3,000 – ~15,000)" |
| Preprocessing | Max. missing per variable | 40% |
| | Excluded | IDs, sampling weights, plausible values, PISA derived indices |
| | Free-text variables | > 20% unique values |
| | Ordinal/categorical variable | ≤ 10 categories |
| | Near-zero variance | one category ≥ 95% |
| EFA | Package | `factor_analyzer`, oblimin rotation |
| | Factorability | KMO ≥ 0.50 and Bartlett's test, per block |
| | Number of factors | Kaiser criterion (eigenvalue > 1), max. 10 (student), 6 (each school block), 8 (financial literacy), 5 (other) |
| | Item retention | \|loading\| ≥ 0.40 |
| | Missing values | median imputation |
| IRT | Package / models | `girth`: 2PL (dichotomous), GRM (polytomous), MML estimation |
| | Item retention | discrimination a ≥ 0.50 |
| | Missing values | mode imputation |
| LCA | Package / model | `StepMix`, `measurement="categorical"`, `n_steps=1`, `max_iter=500`, `abs_tol=1e-6`, `random_state=42` |
| | Selection criteria | BIC, relative entropy ≥ 0.80, smallest class ≥ 5%, interpretability |
| Validation | Achievement score | mean of 30 plausible values (10 math, 10 reading, 10 science) |
| | Test | one-way ANOVA across classes |

## 5. Processed results

`results/` contains the outputs of every stage, with the same file names as in the table above:

```
results/2022/rural/      # main analysis
results/2022/national/
results/2018/national/   # replication
```

They are also available through the results API (see above).

## 6. License

- Code: MIT (see `LICENSE`).
- Processed results in `results/`: CC BY 4.0 (see `results/LICENSE`).
- PISA microdata belong to the OECD and are subject to its terms of use.

## Citation

```bibtex
@inproceedings{arenas2026latent,
  title     = {Latent Profiles of Academic Achievement Among Rural Students in Peru: An Integrated EFA--IRT--LCA Analysis of PISA Data},
  author    = {Arenas Cancapa, Kevin Maximiliano and Huiza Pereyra, Eric Raphael},
  booktitle = {WAIMLAp 2026},
  publisher = {Springer},
  year      = {2026}
}
```
