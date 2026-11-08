package city;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class KmpSearch implements StringSearch {
    private final Counters counters = new Counters();
    public Counters counters() { return counters; }

    /** Longest proper prefix which is also a suffix for every pattern prefix. */
    public int[] lps(String pattern) {
        Objects.requireNonNull(pattern);
        counters.reset();
        return buildLps(pattern);
    }

    private int[] buildLps(String pattern) {
        int[] lps = new int[pattern.length()];
        int i = 1, length = 0;
        while (i < pattern.length()) {
            counters.lpsComparisons++;
            if (pattern.charAt(i) == pattern.charAt(length)) lps[i++] = ++length;
            else if (length > 0) length = lps[length - 1];
            else i++;
        }
        return lps;
    }

    public List<Integer> search(String text, String pattern) {
        Objects.requireNonNull(text); Objects.requireNonNull(pattern);
        if (pattern.isEmpty()) throw new IllegalArgumentException("Pattern must not be empty");
        counters.reset();
        List<Integer> matches = new ArrayList<>();
        if (pattern.length() > text.length()) return matches;
        int[] lps = buildLps(pattern);
        int i = 0, j = 0;
        while (i < text.length()) {
            counters.comparisons++;
            if (text.charAt(i) == pattern.charAt(j)) {
                i++; j++;
                if (j == pattern.length()) {
                    matches.add(i - j);
                    j = lps[j - 1]; // Keep the border, so overlapping matches survive.
                }
            } else if (j > 0) j = lps[j - 1];
            else i++;
        }
        return matches;
    }
}
