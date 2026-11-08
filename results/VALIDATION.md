# Validation record - 8 November 2026

- `mvn package`: BUILD SUCCESS; 8 JUnit 5 test methods, 0 failures, 0 errors, 0 skipped.
- All assignment edit-distance values, both LPS reference arrays, all reference search results and empty-pattern rules passed.
- 100 deterministic short edit pairs agreed across all three methods. 100 deterministic search pairs agreed across naive, KMP and Java's `String.indexOf` oracle, including overlapping occurrences.
- `python tools/verify_results.py ../../work/repeat.csv`: PASS; 450 rows, 90 cases, five measured runs each. Every counter and answer repeated exactly in a second independent JVM run; time was deliberately excluded from equality.
- Each algorithm has at least four sizes, a largest/smallest ratio of at least four, and three purposeful input types. Every recorded time is positive.
- Five PNGs are generated exclusively from `results/results.csv`; medians use five raw rows per point. KMP work includes LPS character comparisons. Table and two-row interior-cell counts agree.
- Four PDF pages were rendered and visually inspected after correcting text wrapping using measured font widths. Labels, captions, scales, report numbers and raw rows were checked together.
- Runtime: Windows 11 amd64, Eclipse Temurin OpenJDK 25.0.2, Maven 3.10.0, Python 3.14, Matplotlib 3.11.2. The project compiles to Java 17 bytecode.

Limits: short-case timings are noisy, the warmup is modest, case order is fixed, recursive length 8 is a planned cap rather than a discovered failure threshold, and measured integer slots exclude JVM object overhead. Conclusions are limited to these inputs and measurements.
