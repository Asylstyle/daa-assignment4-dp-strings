package city;

import java.util.Random;

/** Each case gets its own seed, so changing experiment order cannot change inputs. */
public final class InputGenerator {
    public static final long SEED = 20261108L;
    public record Pair(String first, String second) {}
    private InputGenerator() {}

    private static String randomWord(Random random, int length) {
        StringBuilder word = new StringBuilder(length);
        for (int i = 0; i < length; i++) word.append((char) ('A' + random.nextInt(4)));
        return word.toString();
    }
    public static Pair edit(String type, int n) {
        return switch (type) {
            case "equal" -> new Pair("A".repeat(n), "A".repeat(n));
            case "disjoint" -> new Pair("A".repeat(n), "B".repeat(n));
            case "random" -> {
                Random random = new Random(SEED + n);
                yield new Pair(randomWord(random, n), randomWord(random, n));
            }
            default -> throw new IllegalArgumentException("Unknown edit input: " + type);
        };
    }
    public static Pair search(String type, int n) {
        int m = n / 16;
        return switch (type) {
            case "early_mismatch" -> new Pair("B".repeat(n), "A".repeat(m));
            case "late_mismatch" -> new Pair("A".repeat(n), "A".repeat(m - 1) + "B");
            case "random" -> {
                Random random = new Random(SEED + 31L * n);
                yield new Pair(randomWord(random, n), randomWord(random, m));
            }
            default -> throw new IllegalArgumentException("Unknown search input: " + type);
        };
    }
}
