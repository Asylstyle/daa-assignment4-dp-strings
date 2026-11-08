"""Check coverage, repeated measurements, algorithm agreement and optional replay."""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import median
import sys

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    with Path(path).open() as stream:
        return list(csv.DictReader(stream))

def main():
    rows = read(ROOT / 'results/results.csv')
    assert len(rows) == 450, 'Missing or extra measurements'
    groups = defaultdict(list)
    answers = defaultdict(set)
    for row in rows:
        key = row['algorithm'], row['input'], int(row['n'])
        groups[key].append(row)
        family = 'edit' if row['algorithm'] in {'recursive', 'table', 'two_rows'} else 'search'
        answers[family, row['input'], row['n']].add(row['answer'])
        assert float(row['time_ms']) > 0
    assert all(len(values) == 1 for values in answers.values()), 'Answers disagree'
    for key, runs in groups.items():
        assert sorted(int(r['run']) for r in runs) == [1,2,3,4,5]
        stable = [{k:v for k,v in r.items() if k not in {'run','time_ms'}} for r in runs]
        assert all(value == stable[0] for value in stable)
    for algorithm in {r['algorithm'] for r in rows}:
        sizes = {int(r['n']) for r in rows if r['algorithm'] == algorithm}
        assert len(sizes) >= 4 and max(sizes) >= 4 * min(sizes)
    plotted = ROOT / 'results/plot_data.csv'
    if plotted.exists():
        points = read(plotted)
        for point in points:
            runs = groups[point['algorithm'], point['input'], int(point['n'])]
            metric = point['metric']
            values = [int(r['comparisons']) + int(r['lps_comparisons'])
                      if metric == 'total_comparisons' else float(r[metric]) for r in runs]
            assert float(point['median']) == median(values), 'Plot median differs from raw data'
            assert float(point['minimum']) == min(values), 'Plot range differs from raw data'
            assert float(point['maximum']) == max(values), 'Plot range differs from raw data'
            assert int(point['runs']) == len(runs) == 5
        print(f'PASS: {len(points)} plotted measurements match raw medians and ranges')
    if len(sys.argv) > 1:
        replay = read(sys.argv[1])
        assert len(replay) == len(rows)
        for a, b in zip(rows, replay):
            assert {k:v for k,v in a.items() if k != 'time_ms'} == {k:v for k,v in b.items() if k != 'time_ms'}
    print(f'PASS: {len(rows)} rows, {len(groups)} cases, five runs each; coverage and counters verified')

if __name__ == '__main__': main()
