package city;

import java.util.List;

/** Returns every zero-based occurrence, including overlaps, in increasing order. */
public interface StringSearch {
    List<Integer> search(String text, String pattern);
    Counters counters();
}
