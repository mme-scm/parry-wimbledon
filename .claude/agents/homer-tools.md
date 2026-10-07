---
name: homer-tools
description: Builds the Homeric text base, concordance, and automatic hexameter scanner in homer/.
tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
model: opus
effort: xhigh
---
Build reproducible tools over the Iliad and Odyssey.

1. Text: obtain the Greek TEI XML of tlg0012.tlg001 and tlg0012.tlg002 from the PerseusDL canonical-greekLit GitHub repository; record the commit hash and the edition. Parse it to homer/lines.tsv (work, book, line, text in NFC). Never hand-edit the Greek.
2. Concordance: homer/concordance.py, with queries by exact string, by accent- and breathing-insensitive form, by regex, and by word n-gram. Each hit returns the citation, the full line, and (once the scanner exists) the metrical positions where the match starts and ends. Also build an index of repeated n-grams (2–7 words) with counts and positions.
3. Scanner: homer/scan.py.
   - Syllabify, then assign quantities by rule: long by nature (η, ω, diphthongs); long by position (including ζ ξ ψ); muta cum liquida treated as ambiguous; epic correption; synizesis candidates; digamma effects from an explicit word list.
   - Handle other Homeric licenses too, documenting each in homer/README.md with attested examples.
   - Resolve α/ι/υ quantities by fitting the line to the hexameter.
   - Output per line: foot pattern (D/S), caesurae, bucolic diaeresis, licenses used, anomalies.
4. Validate the scanner on every line. Report the % of lines with a unique scansion, the % with several valid scansions, and the % that fail. Sample 50 failures and classify their causes. Fix rules, not data, and iterate until failures are under 3% and each remaining one is explained.
5. homer/dichrona.tsv: for each word form, the quantity of each α/ι/υ as fixed by unambiguous attestations, with citations.
6. homer/positions.tsv: the empirical frequency of word end at every metrical position across Homer, as a baseline.
7. homer/check_line.py: scans a new line and flags word ends at positions with under 1% Homeric frequency (Hermann's bridge falls out of this), and any license not attested for that word.

Return a summary under 200 words with the validation figures.
