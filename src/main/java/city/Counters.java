package city;

/** Per-invocation measurements; an instance is deliberately not thread-safe. */
public final class Counters {
    public long calls;
    public long cells;
    public long comparisons;
    public long lpsComparisons;
    public long allocatedCells;

    public void reset() {
        calls = cells = comparisons = lpsComparisons = allocatedCells = 0;
    }
}
