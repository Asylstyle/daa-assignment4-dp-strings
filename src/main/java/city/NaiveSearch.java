package city;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class NaiveSearch implements StringSearch {
    private final Counters counters = new Counters();
    public Counters counters() { return counters; }

    public List<Integer> search(String text, String pattern) {
        Objects.requireNonNull(text); Objects.requireNonNull(pattern);
        if (pattern.isEmpty()) throw new IllegalArgumentException("Pattern must not be empty");
        counters.reset();
        List<Integer> matches = new ArrayList<>();
        for (int start = 0; start <= text.length() - pattern.length(); start++) {
            int j = 0;
            while (j < pattern.length()) {
                counters.comparisons++;
                if (text.charAt(start + j) != pattern.charAt(j)) break;
                j++;
            }
            if (j == pattern.length()) matches.add(start);
        }
        return matches;
    }
}
