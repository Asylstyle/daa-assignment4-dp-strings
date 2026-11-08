# City Search & Spell-Check

**Assylzhan Amangeldi | SE2526 | DAA Assignment 4**

[GitHub repository](https://github.com/Asylstyle/daa-assignment4-dp-strings) - branch `main`, figure revision `v1.1`; original release `v1.0` is preserved.

Java 17+ and Maven 3.9+ are required.

```sh
mvn test
mvn package
java -cp target/classes city.Experiment
```

Algorithms operate on UTF-16 code units, with unit-cost edits and zero-based search indices. Empty patterns throw `IllegalArgumentException`; null arguments throw `NullPointerException`. Counters reset for each valid call. Algorithm instances are not thread-safe.

## Read the results

- [Four-page report](REPORT.pdf) and [Markdown version](REPORT.md).
- [Design recorded before the experiment](docs/EXPERIMENT_DESIGN.md).
- [450 raw measurement rows](results/results.csv) and [five PNG charts](results/plots/).
- [Exact plotted points](results/plot_data.csv), including medians and observed timing ranges.
- [Validation record](results/VALIDATION.md).

`src/main/java/city` contains the five algorithms, counters, input generator and experiment runner. `src/test/java/city` contains JUnit 5 references, edge cases, counter checks and seeded cross-checks.

## Reproduce the figures and report

Python 3.10+ is needed only for plots and PDF generation, not for Java algorithms or tests.

```sh
python -m pip install -r requirements.txt
python tools/verify_results.py
python tools/plots.py
python tools/report.py
```

To check reproducibility without overwriting the submitted measurements:

```sh
java -cp target/classes city.Experiment target/replay.csv
python tools/verify_results.py target/replay.csv
```

Inputs, answers and counters must match exactly. `time_ms` varies with the computer and JVM state; each chart uses the median of five measured invocations after five warmups. KMP timing and total comparison plots include LPS construction. The recursive experiment deliberately stops at length 8; iterative versions continue to 1024. Allocated slots measure integer array payload, not total JVM heap usage. No dates or commit timestamps were backdated.

## Submission

The updated project uses 28 substantive commits on `main`, with one figure-quality commit after the original 27-commit `v1.0` release. Tag `v1.1` identifies the updated figures and report. Submit `DAA_Assignment4_Assylzhan_Amangeldi_SE2526.zip` to Moodle and include the repository link. The ZIP includes source, tests, raw data, PNG plots and both report formats; generated build folders are excluded. Moodle submission is a separate step.

## AI-use acknowledgement

OpenAI Codex assisted with implementation, tests, experiment tooling and report preparation. The repository includes executable checks and raw measurements for review.
