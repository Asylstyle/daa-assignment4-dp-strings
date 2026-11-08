package city;

import java.util.Objects;

public final class TwoRowDistance implements EditDistance {
    private final Counters counters = new Counters();
    public Counters counters() { return counters; }

    // State: previous[j]=D(i-1,j), current[j]=D(i,j), with b as the shorter string.
    // Transition: min(previous[j]+1, current[j-1]+1, previous[j-1]+mismatch).
    // Base: previous[j]=j and current[0]=i; swap rows after each prefix of a.
    public int distance(String a, String b) {
        Objects.requireNonNull(a); Objects.requireNonNull(b);
        counters.reset();
        if (a.length() < b.length()) { String swap = a; a = b; b = swap; }
        int[] previous = new int[b.length() + 1];
        int[] current = new int[b.length() + 1];
        counters.allocatedCells += previous.length;
        counters.allocatedCells += current.length;
        for (int j = 0; j <= b.length(); j++) previous[j] = j;
        for (int i = 1; i <= a.length(); i++) {
            current[0] = i;
            for (int j = 1; j <= b.length(); j++) {
                counters.cells++;
                counters.comparisons++;
                int cost = a.charAt(i - 1) == b.charAt(j - 1) ? 0 : 1;
                current[j] = Math.min(previous[j] + 1,
                        Math.min(current[j - 1] + 1, previous[j - 1] + cost));
            }
            int[] swap = previous; previous = current; current = swap;
        }
        return previous[b.length()];
    }
}
