package city;

/** Unit-cost Levenshtein distance over Java UTF-16 code units. */
public interface EditDistance {
    int distance(String a, String b);
    Counters counters();
}
