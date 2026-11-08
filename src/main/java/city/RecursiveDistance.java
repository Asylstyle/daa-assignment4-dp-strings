package city;

import java.util.Objects;

public final class RecursiveDistance implements EditDistance {
    private final Counters counters = new Counters();
    public Counters counters() { return counters; }

    // State: D(i,j) is the distance between prefixes a[0:i] and b[0:j].
    // Transition: equal last characters -> D(i-1,j-1); otherwise 1 + min(delete,insert,replace).
    // Base: D(0,j)=j and D(i,0)=i. No memoization is used.
    public int distance(String a, String b) {
        Objects.requireNonNull(a); Objects.requireNonNull(b);
        counters.reset();
        return solve(a, b, a.length(), b.length());
    }

    private int solve(String a, String b, int i, int j) {
        counters.calls++;
        if (i == 0) return j;
        if (j == 0) return i;
        counters.comparisons++;
        if (a.charAt(i - 1) == b.charAt(j - 1)) return solve(a, b, i - 1, j - 1);
        return 1 + Math.min(solve(a, b, i - 1, j - 1),
                Math.min(solve(a, b, i - 1, j), solve(a, b, i, j - 1)));
    }
}
