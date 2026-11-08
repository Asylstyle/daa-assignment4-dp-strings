package city;

import java.util.Objects;

public final class TableDistance implements EditDistance {
    private final Counters counters = new Counters();
    public Counters counters() { return counters; }

    // State: dp[i][j] is the distance between prefixes a[0:i] and b[0:j].
    // Transition: min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+mismatch).
    // Base: dp[i][0]=i and dp[0][j]=j.
    public int distance(String a, String b) {
        Objects.requireNonNull(a); Objects.requireNonNull(b);
        counters.reset();
        int[][] dp = new int[a.length() + 1][b.length() + 1];
        for (int[] row : dp) counters.allocatedCells += row.length;
        for (int i = 0; i <= a.length(); i++) dp[i][0] = i;
        for (int j = 0; j <= b.length(); j++) dp[0][j] = j;
        for (int i = 1; i <= a.length(); i++) {
            for (int j = 1; j <= b.length(); j++) {
                counters.cells++;
                counters.comparisons++;
                int cost = a.charAt(i - 1) == b.charAt(j - 1) ? 0 : 1;
                dp[i][j] = Math.min(dp[i - 1][j] + 1,
                        Math.min(dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost));
            }
        }
        return dp[a.length()][b.length()];
    }
}
