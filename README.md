# City Search & Spell-Check

Java 17+ and Maven 3.9+ are required.

```sh
mvn test
mvn package
java -cp target/classes city.Experiment
```

Algorithms operate on UTF-16 code units, with unit-cost edits and zero-based search indices. Empty patterns throw `IllegalArgumentException`; null arguments throw `NullPointerException`. Counters reset for each valid call. Algorithm instances are not thread-safe.

## AI-use acknowledgement

OpenAI Codex assisted with implementation, tests, experiment tooling and report preparation. The repository includes executable checks and raw measurements for review.
