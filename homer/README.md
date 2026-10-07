# homer/: text, concordance and hexameter scanner for the Iliad and Odyssey

Everything here can be rebuilt from scratch:

```
source .venv/bin/activate
make -C homer            # fetch + lines + scan + tables + n-grams + validation (about 2 minutes)
```

or step by step (from the repository root):

| step | command | writes |
|---|---|---|
| 1 | `python homer/fetch_text.py` | `corpus/raw/perseus/*.xml` (not committed), `homer/source.json` |
| 2 | `python homer/build_lines.py` | `homer/lines.tsv`, `homer/line_counts.tsv` |
| 3 | `python homer/build_tables.py` | `homer/scansion.tsv`, `homer/dichrona.tsv`, `homer/dichrona_analogy.tsv`, `homer/licences.tsv`, `homer/positions.tsv`, `homer/validation_stats.json` |
| 4 | `python homer/concordance.py --build-ngrams` | `homer/ngrams.tsv` |
| 5 | `python homer/validate.py` | `homer/validation.md` and the generated blocks of this README |

Tools for other agents:

```
python homer/concordance.py --ngram "πόδας ὠκὺς Ἀχιλλεύς"          # word n-gram, '*' = any word
python homer/concordance.py --loose "γλαυκωπις αθηνη" --format tsv  # accent/breathing-insensitive
python homer/concordance.py --exact "ἄναξ ἀνδρῶν" --word
python homer/concordance.py --regex "ἔπεα πτερόεντ"                 # --on loose to search the loose text
python homer/scan.py "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος"            # --all-solutions, --json
python homer/check_line.py "…verse…"          # or --file drafts.txt; --json; exit 0 = no flags
```

## 1. Text

Source: PerseusDL `canonical-greekLit`, master at commit
`01b725d835e6e733062ffd79e0efdbae1ba06e5c` (resolved with `git ls-remote` on
2026-10-07; the GitHub API was not available in this session).  The files are
fetched from `raw.githubusercontent.com` at that commit; `homer/source.json`
records URL, SHA-256 and git blob id of each file and the last commit that
touched it (found with a blobless clone):

| poem | file | edition (TEI header) | last commit touching file |
|---|---|---|---|
| Iliad | `data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc2.xml` | Homeri Opera, ed. D. B. Monro and T. W. Allen, Editio tertia, Oxford: Clarendon Press, 1908–1920 (vols. 1–2 = Iliad) | `ceeb60d9e9e0ebefd0f22b536e03a67084d2452a` (2026-09-18) |
| Odyssey | `data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml` | The Odyssey, ed. A. T. Murray, Loeb Classical Library, London: Heinemann / New York: Putnam, 1919 | `b864b282e1689a2c2a1ebb59ff8aa2b773cb50c1` (2026-09-15) |

Licence: the repository states that its contents are under Creative Commons
Attribution-ShareAlike 4.0; `lines.tsv`, `scansion.tsv` and `ngrams.tsv` are
derived from it and carry the same licence (attribution: Perseus Digital
Library, Tufts University).

`homer/lines.tsv`: `work` (Il/Od), `book`, `line` (the TEI `@n`, kept as a
string), `text` (NFC; the text content of `<l>` with whitespace collapsed;
never edited), `bracketed` (1 if the TEI wraps the line in `<del>`).  Rows are
in document order, so the edition's transpositions (Od. 3.305 before 3.304,
Od. 14.64 before 14.63) are kept.  The text uses U+02BC for elision; the tools
treat U+2019, U+0027 and U+1FBD the same way.  `homer/line_counts.tsv` gives
lines per book and the line numbers absent from each book.

<!-- BEGIN GENERATED: text -->
| poem | books | lines | line numbers absent in the edition |
|---|---|---|---|
| Il | 24 | 15687 | 9.458, 459, 460, 461; 11.543; 14.269 |
| Od | 24 | 12107 | 10.456; 16.101; 23.49 |

Lines marked `<del>` (bracketed) in the TEI: Il. 8.548, Il. 8.550, Il. 8.551, Il. 8.552.
<!-- END GENERATED: text -->

## 2. Concordance (`homer/concordance.py`)

`Concordance()` loads `lines.tsv` and, if present, `scansion.tsv`.  Methods
`exact`, `loose`, `regex(on="text"|"loose")` and `ngram` return `Hit`
objects (citation, line, matched text, word indices, metrical start and end).

* **exact**: substring of the NFC line (apostrophe variants unified).  Accents
  must match, including grave versus acute.
* **loose**: accents, breathings, diaeresis, iota subscript, case and
  punctuation ignored; final sigma = σ; elision mark kept.  `--word` restricts
  to whole words.
* **ngram**: whole words compared in loose form within one line; `*` matches
  any one word.
* **metrical positions**: the half-foot numbering below, for the first
  syllable of the first word and the last syllable of the last word touched
  by the match (word level: a match inside a word reports that word's
  positions).  A vowel-less elided word (δʼ, τʼ) takes the position of the
  syllable it is pronounced with.  Lines without a scansion give `-`.

`homer/ngrams.tsv`: every word n-gram of 2–7 words (within a line, loose
form) that occurs at least twice.  Columns: `n`, `ngram_loose`, `form` (the
most frequent attested spelling), `count` (occurrences), `lines` (distinct
lines), `main_position` (most frequent metrical localisation start-end) and
`main_position_share`, `citations` (first 20, each `Il. 1.58@7.5-12`; the
count is always complete).

## 3. Scanner (`homer/scan.py`)

### Metrical positions

Half-foot numbering: the longum of foot *f* is 2*f*−1; the biceps is 2*f*
(contracted biceps, or second short); the first short of a dactylic biceps is
2*f*−0.5.  Foot 3 is 5, 5.5, 6; the final syllable is 12.  Penthemimeral
caesura = word end at 5; trochaic (κατὰ τρίτον τροχαῖον) = 5.5;
hephthemimeral = 7; bucolic diaeresis = 8; Hermann's bridge concerns 7.5.

### Syllables

* Vowel nuclei: single vowels, the diphthongs αι ει οι υι αυ ευ ου ηυ ωυ
  (not if the second vowel has a diaeresis, or if the first carries an accent
  or breathing, as in Perseus's ἐύ, ὀίω), and ᾳ ῃ ῳ.
* The consonants between two nuclei form one cluster across word boundaries
  (an elided word contributes only its consonants).  ζ ξ ψ count double;
  the rough breathing is not a consonant.

### Quantities by rule (tier 0)

* **nature**: η ω, diphthongs, ᾳ ῃ ῳ, and α ι υ with a circumflex are long;
  ε ο are short; other α ι υ (dichrona) are open.
* **accent rules** for dichrona (soft, see `accent_contra`): circumflex on the
  penult, or acute on the antepenult, implies a short final α/ι/υ.
* **position**: two or more consonants after the vowel make the syllable
  long, within a word or across a word boundary.
* **muta cum liquida**: stop + λ ρ μ ν inside a word, or at the start of the
  next word, may leave a short vowel short.
* **epic correption** and **hiatus** (below), the **digamma** list, and the
  free choice of quantity for α ι υ.

Dichrona are resolved by fitting the line to the hexameter.  After a first
pass over the whole corpus, quantities fixed by unambiguous lines
(`dichrona.tsv`) and by analogy with other forms (`dichrona_analogy.tsv`) are
used as preferences in a second pass (contrary quantities cost a tier-1
licence); see section 4.

### Licences

Each licence has a tier and a cost, separately for the princeps (longum) and
the biceps.  For every line the scanner uses the lowest tier that yields any
scansion ("minimal licence"); within that tier the cheapest scansion is
reported first and all others are kept as alternatives.  References are to
D. B. Monro, *A Grammar of the Homeric Dialect*, 2nd ed. (Oxford: Clarendon
Press, 1891), read in the Internet Archive copy `grammarofhomeric00monruoft`
(OCR text downloaded to `corpus/raw/monro/`, not committed).  The examples
and counts in the table are generated from `licences.tsv` (lines with a
unique scansion only) and are therefore attested in this text.

<!-- BEGIN GENERATED: licences -->
| licence | tier princeps / biceps | cost p / b | description | Monro | instances in uniquely scanned lines | examples (word, first citation @ position) |
|---|---|---|---|---|---|---|
| `correption` | - / 0 | - / 0.1 | epic correption: final long vowel/diphthong shortened before a vowel | §380 | 8363 | καί (Il. 1.17@4); οἱ (Il. 1.188@10); μοι (Il. 1.76@9.5) |
| `hiatus_long` | 0 / 1 | 0.3 / 1 | final long vowel/diphthong kept long before a vowel (hiatus) | §380 | 2245 | ἤ (Il. 1.27@6); ἦ (Il. 1.133@1); τῷ (Il. 2.109@1) |
| `hiatus` | 0 / 0 | 0.2 / 0.2 | final short vowel not elided before a vowel (hiatus) | §§379, 382 | 748 | δέ (Il. 1.4@5.5); τε (Il. 2.90@10); πότνια (Il. 1.551@10) |
| `internal_correption` | - / 1 | - / 1 | long vowel/diphthong shortened before a vowel inside a word | §§381, 384 | 75 | δηΐων (Il. 2.544@5.5); μεμαυῖα (Il. 4.440@10); υἱέ (Il. 7.47@2) |
| `muta_cum_liquida` | - / 0 | - / 0.6 | stop + liquid/nasal inside a word does not make position | §370 | 97 | ἀφροδίτη (Il. 2.820@9.5); ἀλλοτρίης (Od. 9.535@3.5); ἀλλοτρίων (Il. 20.298@3.5) |
| `muta_cum_liquida_initial` | - / 0 | - / 0.4 | word-initial stop + liquid/nasal does not lengthen a preceding short final vowel | §370 | 610 | προσηύδα (Il. 1.201@9.5); πρός (Il. 1.609@1.5); βροτῶν (Il. 6.142@3.5) |
| `no_position_initial_cluster` | - / 2 | - / 2 | word-initial ζ / σ+consonant does not lengthen a preceding short final vowel | §370 | 6 | σκαμάνδρου (Il. 5.77@9.5); ζάκυνθον (Il. 2.634@1.5); σκάμανδρε (Il. 21.223@3.5) |
| `lengthening_liquid` | 1 / 2 | 0.5 / 1.5 | short final vowel lengthened before initial λ μ ν ρ σ (originally double) | §§371-372 | 438 | μέγα (Il. 1.454@5); μεγάροισι (Il. 5.270@7); μεγάροισιν (Il. 5.805@7) |
| `lengthening_closed` | 1 / - | 1 / - | short final syllable ending in a consonant lengthened in arsis before a vowel | §375 | 287 | γάρ (Il. 1.342@5); μῆτιν (Il. 2.169@9); χωόμενος (Il. 1.244@3) |
| `lengthening_hiatus` | 2 / - | 2.5 / - | short final vowel lengthened in arsis before a vowel | §§375, 390 (ἰάχω) | 0 | - |
| `metrical_lengthening` | 2 / - | 2 / - | short vowel lengthened in arsis before a single consonant (metrical licence) | §§386-387 | 11 | ὑποδείσαντες (Il. 12.413@7); ἐπεί (Od. 4.13@1); ἐπίτονος (Od. 12.423@1) |
| `synizesis` | 1 / 1 | 1 / 1 | two adjacent vowels in a word pronounced as one long syllable | §378 | 257 | σφεας (Il. 2.704@3); χρεώ (Il. 9.75@8); ἡμέας (Il. 8.211@2) |
| `synizesis_i` | 2 / 2 | 1.5 / 1.5 | ι or υ before a vowel pronounced consonantally (synizesis) | §378 | 5 | αἰγυπτίους (Od. 4.83@9); αἰγυπτίας (Il. 9.382@3); αἰγυπτίη (Od. 4.229@3) |
| `synizesis_cross` | 1 / 1 | 0.8 / 0.8 | synizesis across a word boundary (δή, ἤ, ἐπεί, μή, ἐγώ + vowel) | §378 | 24 | ἦ (Il. 5.349@1); δή (Il. 11.386@3); ἐπεί (Il. 13.777@3) |
| `digamma` | 0 / 0 | 0.05 / 0.05 | initial ϝ (lost digamma) counted as a consonant | §§388-392 | 3411 | οἱ (Il. 1.79@6); ἔπος (Il. 1.108@7); ἔργα (Il. 1.115@10) |
| `digamma_double` | 1 / 1 | 0.5 / 1 | initial σϝ/δϝ counted as two consonants | §§391, 394 | 33 | δήν (Il. 1.416@11); ἕθεν (Il. 6.62@7); δείσαντες (Od. 9.236@3) |
| `synizesis_rare` | 2 / 2 | 2 / 2 | synizesis of other vowel pairs inside a word (ἤιομεν) | §378 | 2 | ἀλλοειδέα (Od. 13.194@4); ἤιομεν (Od. 10.251@1) |
| `digamma_internal` | 0 / 0 | 0.05 / 0.05 | δϝ after the augment counts as two consonants (ἔδεισα = ἔδδεισα) | §394 | 14 | ἔδεισεν (Il. 1.33@3); ἔδεισαν (Od. 10.219@4); ἔδεισας (Il. 22.19@8) |
| `synizesis_cross_rare` | 2 / 2 | 2 / 2 | synizesis across a word boundary after another word (Πηλείδη ἔθελʼ) | §378 | 0 | - |
| `lengthening_liquid_internal` | 2 / 2 | 2 / 2.5 | short vowel lengthened before a single λ μ ν ρ σ inside a word (augment/compound: ἐλίσσετο) | §§371-372 | 7 | φιλομειδής (Il. 3.424@7); αἰόλου (Od. 10.60@4); βορέης (Il. 9.5@1) |
| `dichronon_contra` | 1 / 1 | 1.5 / 1.5 | α/ι/υ given the quantity contrary to its unambiguous attestations elsewhere | §§383-384 | 51 | ἀντικρύ (Il. 3.359@3); γάρ (Il. 9.377@4); μέγα (Il. 14.421@3) |
| `analogy_contra` | 1 / 1 | 1.5 / 1.5 | α/ι/υ given a quantity contrary to other word forms sharing the same beginning (homer/dichrona_analogy.tsv) | - | 81 | ἀνήρ (Il. 2.553@11); ἀπόλλωνος (Il. 1.14@9); ἀπόλλωνι (Il. 1.36@1) |
| `accent_contra` | 1 / 1 | 1.2 / 1.2 | α/ι/υ given a quantity contrary to the accentuation (σωτῆρα / antepenult rules) | §§373, 375 | 22 | ἀχιλλῆϊ (Il. 24.119@5); φλόγεα (Il. 5.745@5); αἶαν (Il. 23.493@2) |
<!-- END GENERATED: licences -->

Notes on particular licences:

* `correption` (Monro §380) and `hiatus_long` are the two treatments of a
  long final vowel or diphthong before a vowel; Homer keeps the length mainly
  in the princeps, so keeping it in the biceps is tier 1.
* `hiatus` is not a choice (the text shows the unelided vowel); it is
  recorded unless a digamma explains it.
* `digamma` (Monro §§388–392): words in `homer/digamma.tsv` may begin with a
  consonant ϝ, which blocks correption and hiatus and can make position
  after a final consonant.  Type `sw` (ἕο, οἱ, ἑός, ἁνδάνω, ἕξ …) may count as
  two consonants (`digamma_double`, ἀπὸ ἕο); type `dw` (δέος, δεινός, δήν …,
  Monro §394) makes the δ double; type `dw_aug` gives ἔδεισα = ἔδδεισα.
  The list is explicit (regular expressions on the loose form, or exact
  forms, with exclusions such as εἴπερ, ἵνα, the name Ἴδη); each row cites
  the Monro section.
* `lengthening_liquid` (§§371–372) applies before any initial λ μ ν ρ σ but
  only in the princeps at tier 1 (in the biceps tier 2, cf. πολλὰ
  λισσομένη); `check_line.py` flags it for words not attested with it.
* `metrical_lengthening` covers the cases Monro §§386–387 treats as
  licence (ἐπίτονος, ζεφυρίη, vocatives, headless lines such as ἐπεὶ δὴ …);
  for α ι υ the same effect is simply a long dichronon (ἀθάνατος,
  Πριαμίδης).

### Output (`homer/scansion.tsv`, one row per line)

`status` (unique / multiple / fail), `tier` (lowest licence tier needed),
`n_scansions`, `n_best` (scansions tied at the minimal cost), `pattern` (feet
1–5 as D/S plus the sixth foot, written S), `alt_patterns`, `quantities`
(L/S per syllable, X for the final anceps), `syllables` (orthographic
syllabification, `.` between syllables), `word_meter` (quantities per word;
`0` = vowel-less elided word), `word_positions` (start-end position of every
word), `wordend_orth` and `wordend_lex` (positions with word end), `caesurae`
(trithemimeral, penthemimeral, trochaic, hephthemimeral), `bucolic` (D = word
end after a dactylic fourth foot, S = after a spondaic one), `licences`
(`name@position(word)`), `features` (spondeiazon; naeke_bridge = word end
after a spondaic fourth foot), `anomalies` (no_main_caesura,
hermann_bridge = lexical word end at 7.5, diaeresis_after_3rd_foot,
tied_best, rare_licence = tier 2 needed, fail), `cost`.

### Word end: orthographic and lexical

Word end is placed after the syllable containing the word's last written
vowel (so an elided word ending in a consonant ends where that vowel's
syllable ends, like any word ending in a consonant before a vowel; a
vowel-less elided word has no word end of its own; cross-word synizesis
removes the word end).  *Lexical* word end additionally joins appositives
to their host: prepositives (prepositions, the unaccented proclitic article
ὁ ἡ αἱ, ἐν ἐς εἰς ἐκ ἐξ εἰ αἰ ὡς οὐ, καί, ἀλλά, ἠδέ, ἰδέ, οὐδέ, μηδέ, ἤ, ἠέ,
μή) belong to the next word; postpositives (unaccented enclitics and δέ,
γάρ, μέν, δή, οὖν, ἄρ/ἄρα, τε, γε, περ, κε(ν) …) to the preceding one.  The
Homeric article forms are mostly pronouns and are not treated as
appositives; nor are anastrophic prepositions (ἄπο, ἔπι).  These are
operational choices of this tool, not a claim about the literature.

## 4. Derived tables

* `dichrona.tsv`: for every word form (NFC, lower case, grave written acute,
  enclitic-induced second accent removed) and every α ι υ in it
  (`vowel_no` counts the vowel nuclei of the word), the quantity fixed by
  unambiguous attestations: `quantity` L / S / conflict, `n_long`,
  `n_short`, `contexts`, citations (first 10 each).  An attestation counts
  only if (a) the line has a unique scansion in pass 1, (b) the syllable
  shows the vowel's quantity (open or prevocalic syllable; a final vowel
  before a vowel, a final vowel in the princeps before a single consonant,
  and a final vowel before λ μ ν ρ σ are excluded because a licence could
  explain them; a syllable long by position is excluded), and (c) forcing
  the opposite quantity leaves the line unscannable even with the tier-1
  licences.  In pass 2 a form's quantity is used if all its attestations
  agree, or if at least 90% agree among five or more.
* `dichrona_analogy.tsv`: for word-internal α ι υ of forms with no
  attestation, the quantity shared by at least 90% (and at least three) of
  the attested forms that begin with the same letters up to the next vowel
  (keys shorter than three letters are not used).  Its leave-one-form-out
  accuracy is reported in `validation.md`.
* `licences.tsv`: every licence used in a line with a unique scansion,
  per word form: `licence`, `form`, `loose`, `count`, citations with
  positions.  For licences triggered by the following word
  (`lengthening_liquid`, `muta_cum_liquida_initial`,
  `no_position_initial_cluster`, `digamma`, `digamma_double`) the form is
  that following word.
* `positions.tsv`: for every metrical position, the number of
  uniquely-scanned lines in which it exists, and the number and share of
  them with orthographic (`freq_orth`) and lexical (`freq_lex`) word end
  there, plus the share per line and per poem.

## 5. `check_line.py`

Scans a new verse with exactly the corpus rules and preferences and prints
the scansion (pattern, syllables, positions, caesurae, licences with Homeric
parallels from `licences.tsv`).  Flags (exit code 1):

* `unmetrical`: no scansion;
* `rare_word_end`: a lexical word end (or orthographic with `--tier orth`)
  at a position where Homer has word end in < 1% of the lines in which the
  position exists (`positions.tsv`); Hermann's bridge is one such position;
* `licence_unattested`: a licence used with a word form for which
  `licences.tsv` has no instance (exact form, then loose form);
* `quantity_contrary`: an α ι υ given a quantity contrary to `dichrona.tsv`
  or to the analogy or accent rules.

Warnings (no effect on the exit code unless `--strict`): α ι υ whose
quantity is not attested for the form (the quantity used and its source are
named), alternative scansions, missing caesura and other anomalies.
`--json` prints a machine-readable summary.

## 6. Validation

<!-- BEGIN GENERATED: validate.py -->
Lines: Iliad 15687, Odyssey 12107, total 27794.

| configuration | unique | multiple | fail |
|---|---|---|---|
| core | 26261 (94.48%) | 95 (0.34%) | 1438 (5.17%) |
| tier<=1 | 27225 (97.95%) | 462 (1.66%) | 107 (0.38%) |
| pass 1 | 27257 (98.07%) | 532 (1.91%) | 5 (0.02%) |
| final | 27142 (97.65%) | 647 (2.33%) | 5 (0.02%) |

Final: tied best scansions 33 (0.12%). Manual checks: sample A: 50/50 agree.
<!-- END GENERATED: validate.py -->

Details, ablations, the failure taxonomy (50 sampled failures of the tier-0
rules, classified) and the explanation of every remaining failure are in
`homer/validation.md`.

## 7. Known limitations

* The minimal-licence principle can prefer a scansion that gives a
  dichronon an unusual quantity over one that needs a licence; the second
  pass corrects this where the form or its analogues are attested
  (`pattern_changed_pass1_to_pass2` in `validation_stats.json`), and the
  remaining alternatives are listed in `alt_patterns`.
* `dichrona.tsv` is keyed by spelling, so homographs share a row (δύω 'two'
  and 'sink'; ἰῷ 'one' and 'arrow'); they show up as conflicts.
* The digamma list follows Monro; ambiguous forms (possessive ὅς = relative
  ὅς) are left out, so hiatus before them appears as another licence.
* Lexical word end uses the simple appositive classes above.
* The text is the Perseus transcription of two different editions (OCT for
  the Iliad, Loeb for the Odyssey); readings are not normalised, and two of
  the five unscannable lines are due to the edition's spelling.
