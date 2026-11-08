package city;

import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;

public final class Experiment {
    private static volatile int sink;
    private static final int RUNS = 5;
    private Experiment() {}

    public static void main(String[] args) throws Exception {
        Path output = Path.of(args.length == 0 ? "results/results.csv" : args[0]);
        Files.createDirectories(output.toAbsolutePath().getParent());
        try (PrintWriter csv = new PrintWriter(Files.newBufferedWriter(output, StandardCharsets.UTF_8))) {
            csv.println("algorithm,input,n,m,run,time_ms,calls,cells,comparisons,lps_comparisons,allocated_cells,answer,seed");
            for (String type : List.of("equal", "disjoint", "random")) {
                for (int n : new int[]{2,4,6,8,64,128,256,512,1024}) {
                    var pair = InputGenerator.edit(type, n);
                    for (EditDistance algorithm : new EditDistance[]{new RecursiveDistance(), new TableDistance(), new TwoRowDistance()}) {
                        if (algorithm instanceof RecursiveDistance && n > 8) continue;
                        String name = algorithm instanceof RecursiveDistance ? "recursive" : algorithm instanceof TableDistance ? "table" : "two_rows";
                        for (int warmup = 0; warmup < RUNS; warmup++) sink = algorithm.distance(pair.first(), pair.second());
                        for (int run = 1; run <= RUNS; run++) {
                            long start = System.nanoTime();
                            int answer = algorithm.distance(pair.first(), pair.second());
                            long elapsed = System.nanoTime() - start;
                            sink = answer;
                            row(csv, name, type, n, n, run, elapsed, algorithm.counters(), answer);
                        }
                    }
                }
            }
            for (String type : List.of("early_mismatch", "late_mismatch", "random")) {
                for (int n : new int[]{1024,2048,4096,8192}) {
                    var pair = InputGenerator.search(type, n);
                    for (StringSearch algorithm : new StringSearch[]{new NaiveSearch(), new KmpSearch()}) {
                        String name = algorithm instanceof NaiveSearch ? "naive" : "kmp";
                        for (int warmup = 0; warmup < RUNS; warmup++) sink = algorithm.search(pair.first(), pair.second()).size();
                        for (int run = 1; run <= RUNS; run++) {
                            long start = System.nanoTime();
                            int answer = algorithm.search(pair.first(), pair.second()).size();
                            long elapsed = System.nanoTime() - start;
                            sink = answer;
                            row(csv, name, type, n, pair.second().length(), run, elapsed, algorithm.counters(), answer);
                        }
                    }
                }
            }
        }
        System.out.println("Saved " + output);
    }

    private static void row(PrintWriter csv, String name, String type, int n, int m,
                            int run, long nanos, Counters c, int answer) {
        csv.printf(Locale.ROOT, "%s,%s,%d,%d,%d,%.6f,%d,%d,%d,%d,%d,%d,%d%n",
                name, type, n, m, run, nanos / 1_000_000.0, c.calls, c.cells,
                c.comparisons, c.lpsComparisons, c.allocatedCells, answer, InputGenerator.SEED);
    }
}
