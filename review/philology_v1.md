# Philology review of draft v1 (55 verses)

Reviewed: `composition/drafts/v1.txt`, with glosses, sources and enjambment labels from `composition/drafts/v1.jsonl`, against `composition/brief.md` (§4 name renderings, §5.2 lexicon, §5.4 prohibitions). Reviewer: philologist agent, 2026-10-07. The scansion and provenance verifiers are separate (PHASES.md Phase 4); points for them are listed in §6.

## 1. Method and sources

* **Homeric evidence.** Every Homeric claim below comes from `python homer/concordance.py`. The text is Perseus: Monro and Allen's Iliad and Murray's Odyssey (homer/README.md). Each judgement in the table gives its query and hits; positions in square brackets use the half-foot numbering of homer/README.md. The verbatim outputs behind the FAIL and the key QUERY verdicts are in Appendix A. `check_line` was run once, on the remedy suggested for line 35.
* **Lexica.** LSJ entries for πάλιν, ἐξεναρίζω, δίς and ἐκφέρω were fetched from Perseus (`perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=…`) on 2026-10-07 and are quoted in Appendix A.6. I did not fetch Cunliffe and make no claim from it. Anything else is marked [unverified].
* **Enjambment.** I used Parry 1929 as summarised by Z. Dukat, "Enjambement as a Criterion for Orality in Homeric and South Slavic Epic Poetry", *Oral Tradition* 6/2-3 (1991) 303-315. The PDF was fetched from journal.oraltradition.org on 2026-10-07; the quotations are in Appendix A.7. I have not seen Parry's own text, so the wording below is Parry as quoted by Dukat. The criteria:
  * **Unperiodic.** The sentence could have ended with the verse but is continued by added descriptive matter, or by "a word or phrase or clause of the same grammatical structure as one in the foregoing verse" (Parry 1929:207, quoted by Dukat).
  * **Necessary.** The sentence cannot be complete at the verse end. Type 1 (Kirk's "periodic") is a subordinate clause followed by its main clause; type 2 (Kirk's "integral") splits subject from predicate, a verb from its object, and so on.
  * **None.** An actual strong stop.

  I applied Kirk's punctuation test as tabulated by Dukat: a strong stop actually printed (`.` `·` `;`) counts as none; a complete sentence with only a comma or no punctuation counts as unperiodic; an incomplete sentence counts as necessary. A verse that ends inside a ὡς δ᾽ ὅτε simile before its apodosis is necessary. The composer controls the punctuation, so the none/unperiodic split partly depends on it; lines 22, 29, 51 and 54 change category if the punctuation changes.
* **Verdicts.** PASS: no philological defect, though notes may still apply. FAIL: a defect in Homeric morphology, prosody or syntax, or a mismatch of sense, shown by the evidence. QUERY: a human decision is needed, typically a brief-sanctioned licence the evidence does not support, an unattested but possible usage, or an ambiguity of sense.
* **Reproducibility.** The verdict and enjambment counts in §2 and §5 were printed by the tally script in Appendix A.8, run on the table in §7 of this file.

## 2. Summary

**Verdicts (55 lines): PASS 36, FAIL 6, QUERY 13.**

**Failing lines (6):**

| line(s) | reason |
|---|---|
| 4 | Particle syntax: a single τε after the first conjunct with no καί or τε on the second ("A τε B"). Homer has τε … καί (Il. 1.7, the model; Il. 14.29) or τε on the second member (Il. 2.871, Od. 10.513). None of 159 verse-final name τε … name lines has the draft's shape. |
| 35 | ἄρ᾽ elided before the digammated dative οἱ. Homer never elides before dative οἱ (ἄρα οἱ 44x, ῥά οἱ 28x, δέ οἱ 254x; all 12 elided-word + οἱ hits are the plural article). Attested remedy: `εἰ μή οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός.` (εἰ μή οἱ Il. 17.71, 22.203), which passes check_line with no flags. |
| 39-40 | Il. 20.165-169 are cut, so the lion is no longer a clause subject. After "λέων ὣς·", οὐρῇ δὲ … μαστίεται, ἑὲ δ᾽ αὐτὸν ἐποτρύνει has Σέρβος as subject: the Serb lashes his flanks with his tail. The tense jumps from ὦρτο to gnomic present, and the gloss invents a relative ("that"). |
| 42-43 | A ὡς δ᾽ ὅτ᾽ simile with no apodosis; line 44 starts the scales. All 63 Homeric ὡς δ᾽ ὅτε/ὅτ᾽ similes have one: 59 by ὣς/ὥς/τώς and 4 by τοῖος/τόσσος. The model's own apodosis is Il. 22.165. |

**Query lines (13):**

| line(s) | question for a human |
|---|---|
| 15 | A verbless ὅτε-clause ("ἀλλ᾽ ὅτε δὴ τὸ τέταρτον, ὃ δ᾽ …"); all 5 Homeric instances of the formula have a verb. |
| 20, 24, 29, 30 | One decision covers all four. ἐξενάριξε means "slew and stripped" (LSJ), but here it is repeated on the same man (20 τρὶς … μιν, 24 δίς) or reciprocal (29-30: the slain man slays his slayer). §3.2/§5.2 sanction it for a break of serve. The glosses say "broke", which is the tennis referent, not a translation. |
| 23, 32 | πάλιν = "again": LSJ calls this sense "rare in Hom." and cites only Il. 2.276, in πάλιν αὖτις. The Homeric sense is "back". |
| 33 | τὸ δ᾽ has no stated antecedent (the nearest neuter is κῦδος). Homeric σήματα πάντων means "everyone's marks", a record throw; with §5.2's σήματα = "lines" it can be read as "out". The jsonl's "fastest serve of the match" contradicts brief 1.2. |
| 36 | Nothing says who threw the spear. Under the Homeric idiom (Il. 13.408, 22.274-275) the line says a spear missed Federer, the reverse of Djokovic's passing winner. |
| 48, 51 | Ζοκοβίδης needs a long ι at 11. Every Homeric -ίδης has short ι, including Κρονίδης (SSL, 26x), which the jsonl cites as the analogue for the long ι; no -ίδης ends a verse. |
| 50 | Νοβάκος needs a long ᾱ (metre-only), which is not Ionic; Homer keeps ᾱ only in some names (Ποσειδάων, Μαχάων). |
| 51 | Also an unmarked change of subject: προΐει (Federer serving) comes straight after Νοβάκος was subject in line 50. |
| 52 | Narrative asyndeton (no connective). |

## 3. Dialect

* **Digamma** is broken in line 35 (ἄρ᾽ οἱ). Every other hiatus before a once-digammated word sits inside an attested phrase: ὅ οἱ (9), ἐπὶ/κατὰ ἶσα (13, 21, 26), δαίμονι ἶσος (37), ἑὲ δ᾽ (40), and -το/-ος before ἰσόθεος (27, 41, 49), cf. Il. 23.677.
* **ᾱ in Νοβάκος (50)** is not Ionic. It is admissible only as a name licence like Ποσειδάων (50x) or Μαχάων (4x); see QUERY 50. The other renderings keep Ionic η: Φεδερῆρος, Ῥογῆρος, and Ζοκοβῆος/-ῆος rather than Attic -έως.
* **No Attic contractions.** Forms stay open where Homer keeps them open: ἄεθλον (not ἆθλον), ἀεθλοφόροι, τανηλεγέος, ἀντιθέου. The contracted θοῶς (24x) and τρωχῶσι (Il. 22.163) are themselves Homeric. Aeolic -εσσι (στήθεσσιν) and -φι (παλάμηφιν) occur only inside attested formulae.
* **Prosody of invented names.** Ζοκοβίδης ῑ (48, 51) and Νοβάκος ᾱ (50) are QUERY.
  * Ἑλβέτιος with short ι (5, 12, 19, 33, 46, 47, 52) has a real analogue in the ethnic suffix -ιος: Αἰγύπτιος scans LLSS at 6-8 (Od. 2.15, 4.385). It passes.
  * ἀντίθεος/-έου (4, 46): check_line's quantity warning is spurious. The short ι is attested by position, ἀντίθεος at 1-3 in Il. 9.623.

## 4. Lexicon

* **Prohibited words (brief §5.2/§5.4).** None of the listed words (γραμμή, στέγη, ὄχλος, ὥρα/ὥρη "hour", δίκτυον, ῥάβδος, χλόη, χόρτος, δικαστής, ἀθλητής, σφαιριστ-, ἡττ-) occurs in the draft. Checked with `homer/greek.py` loose forms.
* **Post-Homeric coinages, all sanctioned by §4/§5.3:**
  * Ἑλβέτιος. It is Latin-based (Helvetii [unverified]), and §5.4 says "no Latin-based words" while §4.1 and §5.3 list it as an approved rendering; a human should settle the conflict.
  * Σέρβος (post-Homeric ethnic [unverified]).
  * The name renderings Φεδερῆρος, Φεδερεύς, Ῥογῆρος, Ζοκοβεύς/-ῆος, Ζοκοβίδης and Νοβάκος. A second stem for one man (Φεδερῆρος beside Φεδερεύς) is paralleled by Πάτροκλος beside Πατροκλῆος (`--loose "πατροκληος" --word` → 7).
* **Homeric words in a non-Homeric sense:**
  * πάλιν "again" (23, 32): LSJ "rare in Hom." (only Il. 2.276); QUERY. In line 22, πάλιν "back" is the Homeric sense.
  * δίς + finite verb "on two occasions" (24, 33, 49, 50): Homer has only δὶς τόσσον (Od. 9.491; LSJ). §5.2 sanctions it on the analogy of τρίς + verb (Il. 5.436-437), so it is a note, not a verdict.
  * ἐξενάριξε for a break of serve (20, 24, 29, 30) and for the match (34, 53): LSJ gives "strip a foe slain; kill". Only the repeated or reciprocal uses are QUERY.
  * σήματα (33): Homeric "marks of the throws" (Od. 8.192, Il. 23.843), not "lines"; QUERY.
* **Tennis objects checked against the §5.2 table, all used as the table allows:**
  * ἀσπίς = racket (8).
  * ἔγχος/δόρυ/βέλος = stroke or ball (9, 12, 25, 35, 36, 52).
  * σφαῖρα (22).
  * κνημῖδες = shoes (6) and χιτών = shirt (7), as in §2.2.
  * διαμετρητῷ ἐνὶ χώρῳ (11).
  * ἄεθλον = set or match prize (15, 23, 28, 43).
  * προΐει/ἀκόντισε = serve (12, 25, 51).
  * οὐδ᾽ ἀφάμαρτε = winner (27, 50).
  * ἐτώσιον ἔκφυγε χειρός = error (35, 52).
  * καμάτῳ … γυῖα λέλυντο = fatigue (31).
  * ὀψὲ δὲ δή and δείελον ἦμαρ for time (32, 55), with no sunset.
* **Epithet economy.** κρατερός (Djokovic) and βοὴν ἀγαθός (Federer) are kept apart throughout. But ἀντίθεος (Djokovic, 4 and 46) and ἰσόθεος φώς (Federer, 27, 41, 49), together with δαίμονι ἶσος (37), all mean "godlike". That is legal under §5.4 (they are different epithets) but blurs the distinction §4 asks for.

## 5. Enjambment

Counts from the tally script (Appendix A.8), out of 55 lines:

| | none | unperiodic | necessary |
|---|---|---|---|
| composer (jsonl) | 35 (63.6%) | 12 (21.8%) | 8 (14.5%) |
| reviewer | 31 (56.4%) | 15 (27.3%) | 9 (16.4%) |
| Parry's Iliad sample (Dukat 1991:305, from Parry 1929:204) | 48.5% | 24.8% | 26.6% |

The reviewer disagrees with the composer on 8 lines:

| line | composer → reviewer | reason |
|---|---|---|
| 17 | unperiodic → necessary | Inside the ὡς δ᾽ ὅτε period; its main clause comes in 19. |
| 22 | none → unperiodic | Comma; line 23 continues with δεύτερον αὖ. |
| 29 | none → unperiodic | Comma, then τὸν δ᾽ αὖτ᾽. |
| 34 | necessary → unperiodic | The καί νύ κεν clause is complete; the εἰ μή clause is added. |
| 38 | unperiodic → none | A strong stop is printed. In Il. 20.164 the verse is followed by σίντης, ὅν τε …, but the draft cut that. |
| 43 | none → necessary | The simile period is never closed: FAIL 42-43. |
| 51 | none → unperiodic | Comma. |
| 54 | none → unperiodic | No stop is printed; μέν is answered by δέ in 55. |

Necessary enjambment is well below both Parry's Homeric figure (26.6%) and the brief's target (§2.7, "roughly a third"). If lines 39-40 and 42-43 are repaired by restoring Homeric syntax (a relative clause for the lion, a ὣς line for the horses), necessary enjambment will rise.

## 6. Points for the composer and the other verifiers (not philological verdicts)

* jsonl 22 cites Il. 5.156 for a dual subject with a plural verb, but there ἀμφοτέρω is an object. The correct parallels are Il. 5.275 and 16.337.
* jsonl 29 gives βοὴν ἀγαθὸν Μενέλαον as 6x; the concordance gives 5 (ἀγαθὸν Μενέλαον is 6).
* jsonl 33 calls point 357 "the fastest serve of the match", against brief 1.2 (202 km/h at 3:35:36).
* jsonl 48 and 51 justify ι long "as Κρονίδης", but Κρονίδης has short ι (positions 3.5-5 and 5.5-7 in all 26 hits).
* Line 12 has an uncited whole-line model, Il. 16.284.
* Line 5's πρῶτος (who kitted up first) and line 28's ὣς (the set taken "thus", by the rally) assert sequence and cause that are not in brief §1 (1.11 forbids inventing the order of the warm-up). These are for the provenance verifier.
* Brief §5.1 asks for at least two extended similes. With 38-40 and 42-43 failing, only the horse simile (16-19) is sound.
* Tooling: check_line passed line 35. It does not flag elision before a digammated word (οἱ). This should be reported to the owner of homer/check_line.py.

## 7. Per-line table
| n | verdict | findings (morphology, dialect, syntax, lexicon, sense, idiom) | evidence: query → hits | enjambment: composer → reviewer |
|---|---|---|---|---|
| 1 | PASS | ἄνδρε is a Homeric dual. δαΐφρονε is unattested, but the -ονε dual of a 3rd-declension adjective is regular: κρατερόφρονε (Od. 11.299), δαήμονε (Od. 16.253). Relative dual τώ is Homeric (Il. 3.238; Il. 9.5 τώ τε … ἄητον, with a dual verb). Od. 1.1 frame; περὶ νίκης keeps its slot 9.5-12. | `--ngram "ἄνδρα μοι ἔννεπε"` → Od. 1.1; `--loose "ανδρε" --word` → 9 (Il. 5.303, 11.432, 20.286 …); `--loose "δαιφρονε" --word` → 0; `--regex "\b\w+ονε\b" --on loose` → 10, incl. Od. 11.299, 16.253; `--regex ", τώ? (?!δ\|μὲν\|μέν)"` → Il. 3.238, 9.5, 12.146; `--ngram "περὶ νίκης"` → Il. 23.437, 23.496, 23.639 [9.5-12] | necessary → necessary |
| 2 | PASS | ἐμαρνάσθην is a 3rd-person dual imperfect; the second half is verbatim. | `--loose "εμαρνασθην" --word` → Il. 7.301, 17.382 [2-5]; `--ngram "ἔριδος πέρι θυμοβόροιο"` → Il. 7.301, 16.476, 20.253 [5.5-12]; `--loose "δηρον" --word --count` → 38 | unperiodic → unperiodic |
| 3 | PASS | Verbatim Il. 1.6. | `--ngram "ἐξ οὗ δὴ τὰ πρῶτα διαστήτην ἐρίσαντε"` → Il. 1.6 | necessary → necessary |
| 4 | FAIL | **Particle syntax.** The line has one τε, after the first conjunct, and nothing on the second ("A τε B"). Homer has τε … καί, as in the model Il. 1.7 and in Il. 14.29 Τυδεΐδης Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων, or τε on the second member, as in Il. 2.871 Νάστης Ἀμφίμαχός τε and Od. 10.513. Read Homerically, Ζοκοβεύς τε attaches backwards and βοὴν ἀγαθὸς Φεδερῆρος is left unconnected; the gloss's "and" is not in the Greek. Name slots are sound: Ζοκοβεύς is SSL at 3.5-5 like διογενὴς Ὀδυσεύς (6x), and Φεδερῆρος fits like βοὴν ἀγαθὸς Διομήδης (21x). | `--ngram "Ἀτρεΐδης τε ἄναξ ἀνδρῶν καὶ δῖος Ἀχιλλεύς"` → Il. 1.7; name τε … name at verse end (App. A.1b) → 159 lines, none of the form A τε B; single-τε six-word lines (App. A.1) → 15, all A B τε; `--ngram "τε βοὴν ἀγαθὸς"` → 0 | none → none |
| 5 | PASS | Ἑλβέτιος is a coinage sanctioned by §4.1/§5.3. Its short ι has a Homeric analogue in the ethnic suffix -ιος (Αἰγύπτιος LLSS). ἐδύσετο τεύχεα καλά is verbatim at 6-12. For the provenance check: πρῶτος says who kitted up first, which is not in the corpus (brief 1.11). | `--ngram "ἐδύσετο τεύχεα καλὰ"` → Il. 3.328, Od. 23.366; `--loose "αιγυπτιος" --word` → Od. 2.15, 4.385 [6-8]; `--ngram "δ᾽ ἄρα πρῶτος"` → 0 (δὲ πρῶτος 12x) | none → none |
| 6 | PASS | Verbatim. | `--ngram "κνημῖδας μὲν πρῶτα περὶ κνήμῃσιν ἔθηκε"` → Il. 3.330, 11.17, 16.131, 19.369 | unperiodic → unperiodic |
| 7 | PASS | χιτῶνα … ἔδυνε is supported by Il. 2.42 ἔνδυνε χιτῶνα. δεύτερον αὖτε is unattested beside δεύτερον αὖ (5x), but it is a minor expansion. | `--ngram "δεύτερον αὖ θώρηκα περὶ στήθεσσιν"` → 4; `--ngram "ἔνδυνε χιτῶνα"` → Il. 2.42; `--ngram "χιτῶνα περὶ στήθεσσι"` → Il. 2.416, 16.841; `--ngram "δεύτερον αὖτε"` → 0; `--ngram "δεύτερος αὖτε"` → Il. 7.248 | unperiodic → unperiodic |
| 8 | PASS | Verbatim Il. 11.32. ἀσπίς for the racket follows §5.2. The tmesis ἂν … ἕλετ᾽ is Homeric. | `--ngram "ἂν δ᾽ ἕλετ᾽ ἀμφιβρότην πολυδαίδαλον ἀσπίδα θοῦριν"` → Il. 11.32 | unperiodic → unperiodic |
| 9 | PASS | Verbatim. ἔγχος for the ball in hand follows §5.2. | `--ngram "εἵλετο δ᾽ ἄλκιμον ἔγχος ὅ οἱ παλάμηφιν ἀρήρει"` → Il. 3.338, Od. 17.4 | none → none |
| 10 | PASS | Σέρβος (a coinage) stands at 1-2 in the slot of Τρῶες/Αἴας/Ἕκτωρ δ᾽ αὖθ᾽ ἑτέρωθεν. The second half is verbatim. | `--ngram "* δ᾽ αὖθ᾽ ἑτέρωθεν"` → 8 (Il. 15.501 Αἴας, 16.755 Ἕκτωρ …); `--ngram "ἐδύσετο νώροπα χαλκόν"` → Il. 2.578, 11.16 | none → none |
| 11 | PASS | Verbatim. | `--ngram "καί ῥ᾽ ἐγγὺς στήτην διαμετρητῷ ἐνὶ χώρῳ"` → Il. 3.344 | none → none |
| 12 | PASS | A name substitution in a whole-line model that the jsonl does not cite: Il. 16.284 Πάτροκλος δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ. | `--ngram "δὲ πρῶτος"` → 12, incl. Il. 16.284; `--ngram "ἀκόντισε δουρὶ φαεινῷ" --count` → 14 | none → none |
| 13 | PASS | Verbatim. | `--ngram "ἔνθά σφιν κατὰ ἶσα μάχην ἐτάνυσσε Κρονίων"` → Il. 11.336 | none → none |
| 14 | PASS | Positive, absolute ἀφάμαρτε ("he missed"): in Homer the positive verb takes a genitive (Il. 8.119, 21.171 τοῦ μέν ῥ᾽ ἀφάμαρτεν) and the absolute use is negated (οὐδ᾽ ἀφάμαρτε). Acceptable. Frame τρὶς μὲν ἔπειτ᾽ + verb of shape SSLS, as Il. 5.436. | `--ngram "τρὶς μὲν ἔπειτ᾽"` → Il. 5.436, 11.462, 16.784, 20.445; `--loose "αφαμαρτε" --word` → 4; `--loose "αφαμαρτεν" --word` → 4 | unperiodic → unperiodic |
| 15 | QUERY | **Verbless ὅτε-clause.** "ἀλλ᾽ ὅτε δὴ τὸ τέταρτον," has no verb. All five Homeric instances have one (ἐπέσσυτο 4x; ἀφίκοντο Il. 22.208). Carrying ἀφάμαρτε over from line 14 into the subordinate clause is unparalleled. The gloss supplies "came". Apodotic ὃ δ᾽ with a change of subject is Homeric (Il. 5.438-439). | `--ngram "ἀλλ᾽ ὅτε δὴ τὸ τέταρτον"` → 5, all with a verb; `--regex "ὅτε δὴ τὸ \w+[,·.;]"` → 0; `--ngram "δεινὰ δ᾽ ὁμοκλήσας"` → Il. 5.439, 16.706, 20.448; `--ngram "ἐσσυμένως λάβ᾽ ἄεθλον"` → Il. 23.511 | none → none |
| 16 | PASS | Verbatim. | `--ngram "ὡς δ᾽ ὅτε τις στατὸς ἵππος ἀκοστήσας ἐπὶ φάτνῃ"` → Il. 6.506, 15.263 | necessary → necessary |
| 17 | PASS | Verbatim. | `--ngram "δεσμὸν ἀπορρήξας θείῃ πεδίοιο κροαίνων"` → Il. 6.507, 15.264 | unperiodic → necessary |
| 18 | PASS | Verbatim. Stopping after Il. 6.508 leaves a grammatical protasis. | `--ngram "εἰωθὼς λούεσθαι ἐϋρρεῖος ποταμοῖο"` → Il. 6.508, 15.265; `--ngram "κυδιόων ὑψοῦ δὲ κάρη ἔχει"` → Il. 6.509 | necessary → necessary |
| 19 | PASS | ὅ γ᾽ + appositive noun is Homeric (αὐτὰρ ὅ γ᾽ ἥρως 7x). None of the 72 ὅ γ᾽ + capital hits has a nominative proper name. Because the ethnic is used as a name, ὅ γ᾽ Ἑλβέτιος can sound like the Attic article ("the Swiss"); the γε keeps it pronominal. | `--ngram "ὣς ἄρ᾽ ὅ γ᾽"` → Il. 22.143, Od. 20.28; `--regex "ὅ γʼ [Α-ΩἈ-Ὼ]"` → 72; `--ngram "αὐτὰρ ὅ γ᾽ ἥρως" --count` → 7; `--loose "επεσσυτο" --word --count` → 12 | none → none |
| 20 | QUERY | **ἐξεναρίζω repeated on one victim.** LSJ gives "strip or spoil a foe slain in fight; kill, slay", so τρὶς … μιν ἐξενάριξε means "three times he slew and stripped him". The gloss "broke him" gives the tennis referent, not the Greek. §3.2/§5.2 sanction ἐξενάριξε for a break; whether it can be repeated is a class decision covering 20, 24, 29 and 30. Form and slot are fine. | `--loose "εξεναριξε" --word` → 15 (Il. 5.151, 6.20, 7.146 …: each a different victim, or the armour); `--loose "εξεναριξεν" --word` → 8; `--ngram "τρὶς δέ"` → 8 | none → none |
| 21 | PASS | | `--ngram "τὸ τρίτον αὖτ᾽"` → Il. 3.225, 23.842; `--ngram "ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε"` → Il. 12.436, 15.413 | none → none |
| 22 | PASS | A dual subject with a plural verb is Homeric (Il. 5.275 τὼ … ἦλθον; 16.337 τὼ … συνέδραμον); the jsonl cites Il. 5.156, which is not a subject. πάλιν here is "back", the Homeric sense. σφαῖρα follows §5.2. | `--loose "σφαιρ"` → Il. 13.204, Od. 6.100, 6.115, 8.372, 8.377; `--loose "αμφοτερω" --word` → 19; `--ngram "τὼ δὲ τάχ᾽ ἐγγύθεν ἦλθον"` → Il. 5.275; `--ngram "τὼ δ᾽ αὖτις ξιφέεσσι"` → Il. 16.337; `--ngram "ἔνθα καὶ ἔνθα" --count` → 32 | none → unperiodic |
| 23 | QUERY | **πάλιν = "again".** LSJ s.v. πάλιν: I "back, backwards (the usual sense in early Ep.)"; II "of Time, again, once more, rare in Hom.", with Il. 2.276 (πάλιν αὖτις) its only Homeric citation. Here πάλιν also duplicates δεύτερον αὖ. | `--ngram "πάλιν"` → 57 (Il. 1.116, 20.439, Od. 7.143 …); `--ngram "πάλιν αὖτις" --count` → 6; `--ngram "δεύτερον αὖ"` → 5 | none → none |
| 24 | QUERY | Same issue as 20 (δίς … ἐξενάριξε, with no object). δίς with a finite verb ("on two occasions") is not Homeric: LSJ cites only δὶς τόσσον (Od. 9.491). §5.2 sanctions δίς; the analogue is τρίς + verb (Il. 5.436-437). | `--loose "δις" --word` → Od. 9.491 only; `--ngram "τὸν δ᾽ αὖτ᾽" --count` → 28 | none → none |
| 25 | PASS | Φεδερεύς takes the Ἀχιλεύς slot of Il. 20.273. A second stem beside Φεδερῆρος is paralleled by heteroclite Πάτροκλος/Πατροκλῆος. | `--ngram "δεύτερος αὖτ᾽ Ἀχιλεὺς προΐει δολιχόσκιον ἔγχος"` → Il. 20.273; `--ngram "προΐει δολιχόσκιον ἔγχος" --count` → 13; `--loose "πατροκληος" --word --count` → 7; `--loose "πατροκλος" --word --count` → 44 | none → none |
| 26 | PASS | Verbatim. In Il. 12.436 the line is followed by πρίν γ᾽ ὅτε δή … (12.437); here καὶ βάλεν follows. | `--ngram "ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε"` → Il. 12.436, 15.413; `--ngram "πρίν γ᾽ ὅτε δὴ Ζεὺς κῦδος ὑπέρτερον"` → Il. 12.437 | unperiodic → unperiodic |
| 27 | PASS | | `--ngram "καὶ βάλεν οὐδ᾽ ἀφάμαρτε"` → Il. 11.350, 13.160; `--ngram "ἰσόθεος φώς" --count` → 14; `--ngram "ἀνίστατο ἰσόθεος φώς"` → Il. 23.677, Od. 20.124 | none → none |
| 28 | PASS | Relative ὡς (Il. 23.615) becomes demonstrative ὣς "thus". For the provenance check: "thus" ties the set to the rally of line 27, but Federer was broken at 2:49:12 before holding for 6-4. | `--ngram "τέτρατος ὡς ἔλασεν"` → Il. 23.615; `--ngram "πέμπτον δ᾽ ὑπελείπετ᾽ ἄεθλον"` → Il. 23.615; `--loose "ελαβεν" --word` → 3 | none → none |
| 29 | QUERY | Same class decision as 20: Federer is slain and stripped here and slays his slayer in line 30. The gloss "broke" is not a translation. The accusative formula is sound (βοὴν ἀγαθὸν Μενέλαον 5x; the jsonl says 6). | `--ngram "βοὴν ἀγαθὸν Μενέλαον" --count` → 5; `--ngram "ἀγαθὸν Μενέλαον"` → 6 | none → unperiodic |
| 30 | QUERY | As 29. | `--ngram "τὸν δ᾽ αὖτ᾽" --count` → 28; `--loose "εξεναριξε" --word` → 15 | none → none |
| 31 | PASS | Verbatim. | `--ngram "τῶν ῥ᾽ ἅμα τ᾽ ἀργαλέῳ καμάτῳ φίλα γυῖα λέλυντο"` → Il. 13.85 | none → none |
| 32 | QUERY | πάλιν = "again", as in 23; "won glory back" does not fit the 8-7 break either. ἄσπετον ἤρατο κῦδος is attested only inside the unreal καί νύ κεν frame; using it as a plain statement is acceptable. | `--ngram "ἄσπετον ἤρατο κῦδος"` → Il. 3.373, 18.165; `--ngram "ὀψὲ δὲ δὴ" --count` → 12 | none → none |
| 33 | QUERY | (a) τὸ δ᾽ has no stated antecedent; the nearest neuter singular is κῦδος (32), whereas the models name the missile (λίθος Od. 8.190; ἔγχος Il. 13.408, 22.275). (b) In Homer σήματα πάντων are the marks of all the other throwers, i.e. a record throw (Od. 8.192; Il. 23.843). With §5.2's σήματα = "lines" the line can be read as "the ball went out". (c) The jsonl calls point 357 "the fastest serve of the match", but brief 1.2 gives 202 km/h at 3:35:36. δίς: see 24. | `--ngram "ὃ δ᾽ ὑπέρπτατο σήματα πάντων"` → Od. 8.192; `--ngram "σήματα πάντων"` → Il. 23.843, Od. 8.192; `--loose "υπερπτατο" --word` → 4; `--ngram "βόμβησεν δὲ λίθος"` → Od. 8.190 | none → none |
| 34 | PASS | Unreal apodosis: καί νύ κεν + aorist indicative. | `--ngram "καί νύ κεν" --count` → 16; `--ngram "εἰ μὴ ἄρ᾽ ὀξὺ νόησε βοὴν ἀγαθὸς Διομήδης"` → Il. 8.91 | necessary → unperiodic |
| 35 | FAIL | **Elision before digammated οἱ.** ἄρ᾽ is elided before the dative pronoun οἱ (ϝοι). Homer never does this: ἄρα οἱ 44x, ῥά οἱ 28x, δέ οἱ 254x, and every elided word + οἱ in the text is the plural article or relative. The model has ὅττί ῥά οἱ. check_line passes the line because it does not test elision before digamma. Attested remedy: εἰ μή οἱ (Il. 17.71, 22.203); `εἰ μή οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός.` passes check_line with no flags (SDDDDS). | `--ngram "ἄρ᾽ οἱ"` → 1 (Il. 7.169 ἄρʼ οἵ γʼ, plural); `--regex "[^ ]ʼ οἱ [^ ]"` → 12, all plural; `--ngram "ἄρα οἱ" --count` → 44; `--ngram "ῥά οἱ" --count` → 28; `--ngram "δέ οἱ" --count` → 254; `--ngram "εἰ μή οἱ"` → Il. 17.71, 22.203 | none → none |
| 36 | QUERY | **Thrower not named.** Djokovic is not named anywhere in 32-36. In all five uses, στῆ δὲ μάλ᾽ ἐγγὺς ἰών is followed by the approacher's own action. In both uses of τὸ δ᾽ ὑπέρπτατο χάλκεον ἔγχος, the man who ducks is the target and the throw misses. Read Homerically, the line says Federer came close and a spear flew over him. That is the opposite of the fact: Djokovic's passing shot won the point. The gloss's "past him" is a fair rendering of ὑπέρ-, but nothing in the Greek says who threw. | `--ngram "στῆ δὲ μάλ᾽ ἐγγὺς ἰών"` → Il. 4.496, 5.611, 11.429, 12.457, 17.347; `--ngram "τὸ δ᾽ ὑπέρπτατο χάλκεον ἔγχος"` → Il. 13.408, 22.275; `--ngram "καὶ τὸ μὲν ἄντα ἰδὼν ἠλεύατο"` → Il. 22.274 | none → none |
| 37 | PASS | Verbatim. Line 38 supplies the apodotic δ᾽, as Il. 5.439 does. | `--ngram "ἀλλ᾽ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος"` → Il. 5.438, 16.705, 16.786, 20.447 | necessary → necessary |
| 38 | PASS | Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν as in line 10; the second half is verbatim. | `--ngram "ἐναντίον ὦρτο λέων ὣς"` → Il. 11.129, 20.164; `--ngram "λέων ὣς"` → 4 | unperiodic → none |
| 39 | FAIL | **Simile cut leaves the Serb with a tail.** Il. 20.165-169 are omitted, including σίντης, ὅν τε … (20.165), which makes the lion the subject. After "λέων ὣς·" the main clause οὐρῇ δὲ … μαστίεται therefore has Σέρβος as its grammatical subject: the Serb lashes his ribs and flanks with his tail. The tense also jumps from aorist ὦρτο to gnomic present with no simile frame. The gloss's "that" translates a relative pronoun that is not in the Greek. | `--ngram "σίντης ὅν τε καὶ ἄνδρες"` → Il. 20.165; `--ngram "ἀγρόμενοι πᾶς δῆμος"` → Il. 20.166; `--ngram "ἀλλ᾽ ὅτε κέν τις ἀρηϊθόων αἰζηῶν"` → Il. 20.167; `--ngram "ἐάλη τε χανών"` → Il. 20.168; `--ngram "ἐν δέ τέ οἱ κραδίῃ στένει ἄλκιμον ἦτορ"` → Il. 20.169; `--ngram "οὐρῇ δὲ πλευράς τε καὶ ἰσχία ἀμφοτέρωθεν"` → Il. 20.170 | necessary → necessary |
| 40 | FAIL | Same defect as 39: μαστίεται and ἐποτρύνει take Σέρβος as subject. The line itself is verbatim. | `--ngram "μαστίεται ἑὲ δ᾽ αὐτὸν ἐποτρύνει μαχέσασθαι"` → Il. 20.171 | none → none |
| 41 | PASS | Intransitive ἔκφερε, LSJ s.v. ἐκφέρω V "shoot forth (before the rest)", Il. 23.376, cf. 759. μετὰ δ᾽ ὄρνυτο is unattested but has close analogues in ἐπὶ δ᾽ ὄρνυτο and τὰς δὲ μετ᾽ ἐξέφερον. ἰσόθεος φώς without a name, as Il. 11.472. | `--ngram "ἔκφερ᾽"` → Il. 23.259, 23.759, 23.785; `--ngram "ἐπὶ δ᾽ ὄρνυτο"` → Il. 23.689, 23.759; `--ngram "μετὰ δ᾽ ὄρνυτο"` → 0; `--ngram "τὰς δὲ μέτ᾽ ἐξέφερον"` → Il. 23.377; `--ngram "ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς"` → Il. 11.472, 15.559, 16.632 | none → none |
| 42 | FAIL | **Simile without apodosis.** The ὡς δ᾽ ὅτ᾽ simile in 42-43 never gets its main clause; line 44 starts the scales. In Homer all 63 lines with ὡς δ᾽ ὅτε/ὅτ᾽ have an apodosis: in 59 a line beginning ὣς/ὥς/τώς follows within 2-13 lines, and the other 4 close with τοῖος/τόσσος (Il. 4.146, 4.280, 8.560, 17.266). The model's own apodosis is Il. 22.165. The line itself is verbatim. | `--ngram "ὡς δ᾽ ὅτ᾽ ἀεθλοφόροι περὶ τέρματα μώνυχες ἵπποι"` → Il. 22.162; App. A.3b script → 63 / 59 / 4 | necessary → necessary |
| 43 | FAIL | Same unit as 42; the broken construction falls at this verse end. | `--ngram "ῥίμφα μάλα τρωχῶσι τὸ δὲ μέγα κεῖται ἄεθλον"` → Il. 22.163; `--ngram "ὣς τὼ τρὶς Πριάμοιο πόλιν πέρι δινηθήτην"` → Il. 22.165 | none → necessary |
| 44 | PASS | Verbatim. | `--ngram "καὶ τότε δὴ χρύσεια πατὴρ ἐτίταινε τάλαντα"` → Il. 8.69, 22.209 | unperiodic → unperiodic |
| 45 | PASS | Verbatim. Note: brief §2.5A asked for κῆρε … θανάτοιο to be replaced; it is kept, and the jsonl gives the reason. | `--ngram "ἐν δ᾽ ἐτίθει δύο κῆρε τανηλεγέος θανάτοιο"` → Il. 8.70, 22.210 | unperiodic → unperiodic |
| 46 | PASS | Ζοκοβῆος ends in Ionic -ῆος like Ὀδυσῆος (64x). ἀντιθέου Ζοκοβῆος has exactly the shape of ἀντιθέου Ὀδυσῆος. Epithet economy: ἀντίθεος (Djokovic) and ἰσόθεος φώς (Federer) both mean "godlike"; they are different words, as §5.4 requires, but the sense is the same. | `--ngram "τὴν μὲν Ἀχιλλῆος τὴν δ᾽ Ἕκτορος ἱπποδάμοιο"` → Il. 22.211; `--ngram "τὴν μὲν ἄρ᾽"` → Il. 5.353, 18.148, Od. 19.440; `--ngram "ἀντιθέου Ὀδυσῆος"` → Od. 20.369 [7-12], 21.254; `--loose "οδυσηος" --word --count` → 64 | unperiodic → unperiodic |
| 47 | PASS | | `--ngram "ἕλκε δὲ μέσσα λαβών"` → Il. 8.72, 22.212; `--ngram "ῥέπε δ᾽"` → Il. 8.72, 22.212; `--ngram "κακὸν ἦμαρ" --count` → 7 | none → none |
| 48 | QUERY | **Ζοκοβίδης needs a long ι at position 11.** This is a metre-only quantity (§4.2) with no Homeric analogue. Every Homeric -ίδης patronymic has short ι: Κρονίδης is SSL at 3.5-5 or 5.5-7; Πριαμίδης and Δαρδανίδης are LSSL; no -ίδης or -ίδην ends a verse. The jsonl's "ι long … as Κρονίδης" is therefore mistaken. The rest is attested (τρὶς μὲν ἔπειτ᾽ ἐπόρουσε 3x; θοῶς 24x; κρατερὸς Διομήδης 20x). | `--loose "κρονιδης" --word` → 26 (Il. 2.111 [3.5-5], 2.375 [5.5-7] …); `--loose "πριαμιδης" --word` → 14 [1-3]; `--loose "δαρδανιδης" --word` → 4; `--regex "ίδη[ςνω][.,·;]?$"` → 0; `--regex "ΐδης[.,·;]?$"` → 0; `--ngram "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε"` → Il. 5.436, 16.784, 20.445 | unperiodic → unperiodic |
| 49 | PASS | ἀμύνετο + accusative "ward off", as ἀμύνετο νηλεὲς ἦμαρ. δίς: see 24. | `--loose "αμυνετο" --word` → Il. 11.484, 13.514; `--ngram "τόν γε" --count` → 25 | none → none |
| 50 | QUERY | Νοβάκος has a long ᾱ (metre-only, §4.2), which is not Ionic: Ionic shifts ᾱ to η [general dialect fact; unverified]. Homer does keep ᾱ in some names (Ποσειδάων 50x, Μαχάων 4x), so a name-specific licence is possible but needs a decision. περικλυτός is used of persons (Il. 11.104; Od. 1.325) and always at 6-8. δίς: see 24. | `--loose "περικλυτος" --word` → 14 [all 6-8]; `--ngram "δῖος Ὀδυσσεύς" --count` → 102; `--loose "ποσειδαων" --word --count` → 50; `--loose "μαχαων" --word --count` → 4 | none → none |
| 51 | QUERY | (a) Ζοκοβίδης long ι, as 48. (b) **Unmarked change of subject.** προΐει has no subject, and the last named subject is Νοβάκος (50), so the line reads "again he [Novak] served, and Djokovic struck back". The server of point 422 was Federer; only the later naming of Ζοκοβίδης signals the switch. | `--ngram "ὣς εἰπὼν προΐει"` → Il. 1.326; `--loose "προιει" --word --count` → 21; `--ngram "βάλε δ᾽"` → Il. 15.541, 16.737, Od. 24.179 | none → unperiodic |
| 52 | QUERY | **Asyndeton.** Two narrative main clauses are joined without δέ/αὐτάρ/ἀτάρ, because the model's ὅττί ῥά οἱ was replaced by a bare genitive. I flag rather than fail this because I did not measure how often Homeric narrative uses asyndeton. | `--ngram "ὅττί ῥά οἱ βέλος"` → Il. 14.407, 22.292; `--ngram "ἀντιθέου Ὀδυσῆος"` → Od. 21.254 (verse-initial genitive inside a continuing sentence) | none → none |
| 53 | PASS | | `--ngram "Διὸς δ᾽ ἐτελείετο βουλή"` → Il. 1.5, Od. 11.297 | none → none |
| 54 | PASS | Verbatim. | `--ngram "ὣς οἳ μὲν μάρναντο δέμας πυρὸς αἰθομένοιο"` → Il. 11.596, 13.673, 18.1; `--ngram "ὣς οἳ μὲν" --count` → 50 | none → unperiodic |
| 55 | PASS | Absolute τέλος "end", as in Il. 2.122 τέλος δ᾽ οὔ πώ τι πέφανται and Il. 11.439; τέλος ἦεν itself is unattested. δείελον ἦμαρ (Od. 17.606) is late afternoon, not sunset (§2.6). | `--ngram "τέλος ἦεν"` → 0; `--ngram "τέλος"` → 29; `--ngram "δείελον ἦμαρ"` → Od. 17.606; `--ngram "ὅτε τ᾽ ἤλυθε"` → Il. 5.803 | none → none |

## Appendix A. Verbatim evidence for the FAIL and the key QUERY verdicts

The blocks below are the output of `python homer/concordance.py` as run on 2026-10-07. Every other query is quoted in the table and can be rerun.

### A.1 Line 4 (τε)

```
# [L4a] python homer/concordance.py --ngram "Ἀτρεΐδης τε ἄναξ ἀνδρῶν καὶ δῖος Ἀχιλλεύς"
Il. 1.7      [1-12]  Ἀτρεΐδης τε ἄναξ ἀνδρῶν καὶ δῖος Ἀχιλλεύς.    <Ἀτρεΐδης τε ἄναξ ἀνδρῶν καὶ δῖος Ἀχιλλεύς>
-- 1 hit(s)

# [L4g] python homer/concordance.py --regex "^(?!.*\b(καὶ|καί|ἠδὲ|ἠδέ|ἰδὲ|ἠδʼ|ἰδʼ)\b)(?!.*\bτʼ)(?!.*\bτε\b.*\bτε\b)[^ ]+ [^ ]+ τε [^ ]+ [^ ]+ [^ ]+$" --limit 60
Il. 2.814    [1-12]  ἀθάνατοι δέ τε σῆμα πολυσκάρθμοιο Μυρίνης·    <ἀθάνατοι δέ τε σῆμα πολυσκάρθμοιο Μυρίνης·>
Il. 2.871    [1-12]  Νάστης Ἀμφίμαχός τε Νομίονος ἀγλαὰ τέκνα,    <Νάστης Ἀμφίμαχός τε Νομίονος ἀγλαὰ τέκνα,>
Il. 11.270   [1-12]  δριμύ, τό τε προϊεῖσι μογοστόκοι Εἰλείθυιαι    <δριμύ, τό τε προϊεῖσι μογοστόκοι Εἰλείθυιαι>
Il. 11.529   [1-12]  ἱππῆες πεζοί τε κακὴν ἔριδα προβαλόντες    <ἱππῆες πεζοί τε κακὴν ἔριδα προβαλόντες>
Il. 12.336   [1-12]  ἑσταότας, Τεῦκρόν τε νέον κλισίηθεν ἰόντα    <ἑσταότας, Τεῦκρόν τε νέον κλισίηθεν ἰόντα>
Il. 15.38    [1-12]  ὅρκος δεινότατός τε πέλει μακάρεσσι θεοῖσι,    <ὅρκος δεινότατός τε πέλει μακάρεσσι θεοῖσι,>
Il. 22.325   [1-12]  λαυκανίην, ἵνα τε ψυχῆς ὤκιστος ὄλεθρος·    <λαυκανίην, ἵνα τε ψυχῆς ὤκιστος ὄλεθρος·>
Od. 5.67     [1-12]  εἰνάλιαι, τῇσίν τε θαλάσσια ἔργα μέμηλεν.    <εἰνάλιαι, τῇσίν τε θαλάσσια ἔργα μέμηλεν.>
Od. 5.186    [1-12]  ὅρκος δεινότατός τε πέλει μακάρεσσι θεοῖσι,    <ὅρκος δεινότατός τε πέλει μακάρεσσι θεοῖσι,>
Od. 7.106    [1-12]  ἥμεναι, οἷά τε φύλλα μακεδνῆς αἰγείροιο·    <ἥμεναι, οἷά τε φύλλα μακεδνῆς αἰγείροιο·>
Od. 10.10    [1-12]  κνισῆεν δέ τε δῶμα περιστεναχίζεται αὐλῇ    <κνισῆεν δέ τε δῶμα περιστεναχίζεται αὐλῇ>
Od. 11.320   [1-12]  ἀνθῆσαι πυκάσαι τε γένυς ἐυανθέι λάχνῃ.    <ἀνθῆσαι πυκάσαι τε γένυς ἐυανθέι λάχνῃ.>
Od. 12.190   [1-12]  Ἀργεῖοι Τρῶές τε θεῶν ἰότητι μόγησαν,    <Ἀργεῖοι Τρῶές τε θεῶν ἰότητι μόγησαν,>
Od. 13.223   [1-12]  παναπάλῳ, οἷοί τε ἀνάκτων παῖδες ἔασι,    <παναπάλῳ, οἷοί τε ἀνάκτων παῖδες ἔασι,>
Od. 17.119   [1-12]  Ἀργεῖοι Τρῶές τε θεῶν ἰότητι μόγησαν.    <Ἀργεῖοι Τρῶές τε θεῶν ἰότητι μόγησαν.>
-- 15 hit(s)

# [L4e] python homer/concordance.py --ngram "τε βοὴν ἀγαθὸς"
-- 0 hit(s)

```

### A.2 Line 35 (elision before οἱ)

```
# [L35d] python homer/concordance.py --ngram "ἄρ᾽ οἱ" --limit 4
Il. 7.169    [2-3]  πάντες ἄρʼ οἵ γʼ ἔθελον πολεμίζειν Ἕκτορι δίῳ.    <ἄρʼ οἵ>
-- 1 hit(s)

# [L35k] python homer/concordance.py --regex "[^ ]ʼ οἱ [^ ]"  --limit 30
Il. 6.435    [6-12]  τρὶς γὰρ τῇ γʼ ἐλθόντες ἐπειρήσανθʼ οἱ ἄριστοι    <θʼ οἱ ἄ>
Od. 1.157    [8-12]  ἄγχι σχὼν κεφαλήν, ἵνα μὴ πευθοίαθʼ οἱ ἄλλοι·    <θʼ οἱ ἄ>
Od. 3.9      [1-3.5]  εὖθʼ οἱ σπλάγχνα πάσαντο, θεῷ δʼ ἐπὶ μηρίʼ ἔκαιον,    <θʼ οἱ σ>
Od. 3.153    [4-5]  ἠῶθεν δʼ οἱ μὲν νέας ἕλκομεν εἰς ἅλα δῖαν    <δʼ οἱ μ>
Od. 4.70     [8-12]  ἄγχι σχὼν κεφαλήν, ἵνα μὴ πευθοίαθʼ οἱ ἄλλοι·    <θʼ οἱ ἄ>
Od. 10.125   [1-3]  ὄφρʼ οἱ τοὺς ὄλεκον λιμένος πολυβενθέος ἐντός,    <ρʼ οἱ τ>
Od. 13.78    [1-5.5]  εὖθʼ οἱ ἀνακλινθέντες ἀνερρίπτουν ἅλα πηδῷ,    <θʼ οἱ ἀ>
Od. 14.375   [1-3]  ἀλλʼ οἱ μὲν τὰ ἕκαστα παρήμενοι ἐξερέουσιν,    <λʼ οἱ μ>
Od. 17.592   [8-12]  ἄγχι σχὼν κεφαλήν, ἵνα μὴ πευθοίαθʼ οἱ ἄλλοι·    <θʼ οἱ ἄ>
Od. 22.252   [1.5-4]  ἀλλʼ ἄγεθʼ οἱ ἓξ πρῶτον ἀκοντίσατʼ, αἴ κέ ποθι Ζεὺς    <θʼ οἱ ἓ>
Od. 23.48    [2-3]  νῦν δʼ οἱ μὲν δὴ πάντες ἐπʼ αὐλείῃσι θύρῃσιν    <δʼ οἱ μ>
Od. 24.386   [1-3]  ἔνθʼ οἱ μὲν δείπνῳ ἐπεχείρεον, ἀγχίμολον δὲ    <θʼ οἱ μ>
-- 12 hit(s)

# [L35f] python homer/concordance.py --ngram "ἄρα οἱ" --count
44

# [L35g] python homer/concordance.py --ngram "ῥά οἱ" --count
28

# [L35h] python homer/concordance.py --ngram "δέ οἱ" --count
254

# [L35a] python homer/concordance.py --ngram "βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός"
Il. 14.407   [3.5-12]  ὅττί ῥά οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός,    <βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός>
Il. 22.292   [3.5-12]  ὅττί ῥά οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός,    <βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός>
-- 2 hit(s)

# [L35l] python homer/concordance.py --ngram "εἰ μή οἱ"
Il. 17.71    [4-5.5]  Ἀτρεΐδης, εἰ μή οἱ ἀγάσσατο Φοῖβος Ἀπόλλων,    <εἰ μή οἱ>
Il. 22.203   [1-3]  εἰ μή οἱ πύματόν τε καὶ ὕστατον ἤντετʼ Ἀπόλλων    <εἰ μή οἱ>
-- 2 hit(s)

```

### A.3 Lines 42-43 (simile apodosis)

```
# [L42] python homer/concordance.py --ngram "ὡς δ᾽ ὅτ᾽ ἀεθλοφόροι περὶ τέρματα μώνυχες ἵπποι"
Il. 22.162   [1-12]  ὡς δʼ ὅτʼ ἀεθλοφόροι περὶ τέρματα μώνυχες ἵπποι    <ὡς δʼ ὅτʼ ἀεθλοφόροι περὶ τέρματα μώνυχες ἵπποι>
-- 1 hit(s)

# [L43c] python homer/concordance.py --ngram "ὣς τὼ τρὶς Πριάμοιο πόλιν πέρι δινηθήτην"
Il. 22.165   [1-12]  ὣς τὼ τρὶς Πριάμοιο πόλιν πέρι δινηθήτην    <ὣς τὼ τρὶς Πριάμοιο πόλιν πέρι δινηθήτην>
-- 1 hit(s)

# [L42b] python homer/concordance.py --ngram "τοῖοί τοι Μενέλαε μιάνθην"
Il. 4.146    [1-8]  τοῖοί τοι Μενέλαε μιάνθην αἵματι μηροὶ    <τοῖοί τοι Μενέλαε μιάνθην>
-- 1 hit(s)

# [L42c] python homer/concordance.py --ngram "τοῖαι ἅμ᾽ Αἰάντεσσι"
Il. 4.280    [1-5.5]  τοῖαι ἅμʼ Αἰάντεσσι διοτρεφέων αἰζηῶν    <τοῖαι ἅμʼ Αἰάντεσσι>
-- 1 hit(s)

# [L42d] python homer/concordance.py --ngram "τόσσα μεσηγὺ νεῶν"
Il. 8.560    [1-5]  τόσσα μεσηγὺ νεῶν ἠδὲ Ξάνθοιο ῥοάων    <τόσσα μεσηγὺ νεῶν>
-- 1 hit(s)

# [L42e] python homer/concordance.py --ngram "τόσσῃ ἄρα Τρῶες ἰαχῇ"
Il. 17.266   [1-7]  τόσσῃ ἄρα Τρῶες ἰαχῇ ἴσαν. αὐτὰρ Ἀχαιοὶ    <τόσσῃ ἄρα Τρῶες ἰαχῇ>
-- 1 hit(s)

```

### A.4 Lines 39-40 (Il. 20.164-171)

```
# [L38a] python homer/concordance.py --ngram "ἐναντίον ὦρτο λέων ὣς"
Il. 11.129   [6-12]  τὼ δὲ κυκηθήτην· ὃ δʼ ἐναντίον ὦρτο λέων ὣς    <ἐναντίον ὦρτο λέων ὣς>
Il. 20.164   [6-12]  Πηλεΐδης δʼ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς    <ἐναντίον ὦρτο λέων ὣς>
-- 2 hit(s)

# [L38b] python homer/concordance.py --ngram "σίντης ὅν τε καὶ ἄνδρες"
Il. 20.165   [1-5.5]  σίντης, ὅν τε καὶ ἄνδρες ἀποκτάμεναι μεμάασιν    <σίντης, ὅν τε καὶ ἄνδρες>
-- 1 hit(s)

# [L38f] python homer/concordance.py --ngram "ἀγρόμενοι πᾶς δῆμος"
Il. 20.166   [1-5.5]  ἀγρόμενοι πᾶς δῆμος· ὃ δὲ πρῶτον μὲν ἀτίζων    <ἀγρόμενοι πᾶς δῆμος>
-- 1 hit(s)

# [L38i] python homer/concordance.py --ngram "ἀλλ᾽ ὅτε κέν τις ἀρηϊθόων αἰζηῶν"
Il. 20.167   [3-12]  ἔρχεται, ἀλλʼ ὅτε κέν τις ἀρηϊθόων αἰζηῶν    <ἀλλʼ ὅτε κέν τις ἀρηϊθόων αἰζηῶν>
-- 1 hit(s)

# [L38g] python homer/concordance.py --ngram "ἐάλη τε χανών"
Il. 20.168   [3.5-7]  δουρὶ βάλῃ ἐάλη τε χανών, περί τʼ ἀφρὸς ὀδόντας    <ἐάλη τε χανών>
-- 1 hit(s)

# [L38h] python homer/concordance.py --ngram "ἐν δέ τέ οἱ κραδίῃ στένει ἄλκιμον ἦτορ"
Il. 20.169   [3-12]  γίγνεται, ἐν δέ τέ οἱ κραδίῃ στένει ἄλκιμον ἦτορ,    <ἐν δέ τέ οἱ κραδίῃ στένει ἄλκιμον ἦτορ>
-- 1 hit(s)

# [L38c] python homer/concordance.py --ngram "οὐρῇ δὲ πλευράς τε καὶ ἰσχία ἀμφοτέρωθεν"
Il. 20.170   [1-12]  οὐρῇ δὲ πλευράς τε καὶ ἰσχία ἀμφοτέρωθεν    <οὐρῇ δὲ πλευράς τε καὶ ἰσχία ἀμφοτέρωθεν>
-- 1 hit(s)

# [L38d] python homer/concordance.py --ngram "μαστίεται ἑὲ δ᾽ αὐτὸν ἐποτρύνει μαχέσασθαι"
Il. 20.171   [1-12]  μαστίεται, ἑὲ δʼ αὐτὸν ἐποτρύνει μαχέσασθαι,    <μαστίεται, ἑὲ δʼ αὐτὸν ἐποτρύνει μαχέσασθαι>
-- 1 hit(s)

```

### A.5 Lines 48, 51 (quantity of -ίδης)

```
# [L48l] python homer/concordance.py --loose "κρονιδης" --word --limit 8
Il. 2.111    [3.5-5]  Ζεύς με μέγα Κρονίδης ἄτῃ ἐνέδησε βαρείῃ,    <Κρονίδης>
Il. 2.375    [5.5-7]  ἀλλά μοι αἰγίοχος Κρονίδης Ζεὺς ἄλγεʼ ἔδωκεν,    <Κρονίδης>
Il. 4.5      [5.5-7]  αὐτίκʼ ἐπειρᾶτο Κρονίδης ἐρεθιζέμεν Ἥρην    <Κρονίδης>
Il. 4.166    [3.5-5]  Ζεὺς δέ σφι Κρονίδης ὑψίζυγος αἰθέρι ναίων    <Κρονίδης>
Il. 6.234    [5.5-7]  ἔνθʼ αὖτε Γλαύκῳ Κρονίδης φρένας ἐξέλετο Ζεύς,    <Κρονίδης>
Il. 7.69     [3.5-5]  ὅρκια μὲν Κρονίδης ὑψίζυγος οὐκ ἐτέλεσσεν,    <Κρονίδης>
Il. 8.141    [5.5-7]  νῦν μὲν γὰρ τούτῳ Κρονίδης Ζεὺς κῦδος ὀπάζει    <Κρονίδης>
Il. 8.414    [3.5-5]  οὐκ ἐάᾳ Κρονίδης ἐπαμυνέμεν Ἀργείοισιν.    <Κρονίδης>
-- 26 hit(s), 8 shown

# [L48i] python homer/concordance.py --loose "πριαμιδης" --word --limit 3
Il. 2.817    [1-3]  Πριαμίδης· ἅμα τῷ γε πολὺ πλεῖστοι καὶ ἄριστοι    <Πριαμίδης>
Il. 4.490    [1-3]  Πριαμίδης καθʼ ὅμιλον ἀκόντισεν ὀξέϊ δουρί.    <Πριαμίδης>
Il. 6.76     [1-3]  Πριαμίδης Ἕλενος οἰωνοπόλων ὄχʼ ἄριστος·    <Πριαμίδης>
-- 14 hit(s), 3 shown

# [L48j] python homer/concordance.py --loose "δαρδανιδης" --word --limit 3
Il. 3.303    [3-5]  τοῖσι δὲ Δαρδανίδης Πρίαμος μετὰ μῦθον ἔειπε·    <Δαρδανίδης>
Il. 7.366    [1-3]  Δαρδανίδης Πρίαμος, θεόφιν μήστωρ ἀτάλαντος,    <Δαρδανίδης>
Il. 22.352   [1-3]  Δαρδανίδης Πρίαμος· οὐδʼ ὧς σέ γε πότνια μήτηρ    <Δαρδανίδης>
-- 4 hit(s), 3 shown

# [L48g] python homer/concordance.py --regex "ίδη[ςνω][.,·;]?$"
-- 0 hit(s)

# [L48f] python homer/concordance.py --regex "ΐδης[.,·;]?$"
-- 0 hit(s)

```

### A.5b Lines 24 (δίς), 23/32 (πάλιν αὖτις), 15 (ὅτε-clause), 36 and 33 (ὑπέρπτατο, σήματα πάντων)

```
# [L24a] python homer/concordance.py --loose "δις" --word
Od. 9.491    [4-4]  ἀλλʼ ὅτε δὴ δὶς τόσσον ἅλα πρήσσοντες ἀπῆμεν,    <δὶς>
-- 1 hit(s)

# [L23b] python homer/concordance.py --ngram "πάλιν αὖτις" --count
6

# [L15a] python homer/concordance.py --ngram "ἐσσυμένως λάβ᾽ ἄεθλον"
Il. 23.511   [7-12]  ἴφθιμος Σθένελος, ἀλλʼ ἐσσυμένως λάβʼ ἄεθλον,    <ἐσσυμένως λάβʼ ἄεθλον>
-- 1 hit(s)

# [L15b] python homer/concordance.py --regex "ὅτε δὴ τὸ \w+[,·.;]" 
-- 0 hit(s)

# [L36a] python homer/concordance.py --ngram "στῆ δὲ μάλ᾽ ἐγγὺς ἰών"
Il. 4.496    [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰὼν καὶ ἀκόντισε δουρὶ φαεινῷ    <στῆ δὲ μάλʼ ἐγγὺς ἰὼν>
Il. 5.611    [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἀκόντισε δουρὶ φαεινῷ,    <στῆ δὲ μάλʼ ἐγγὺς ἰών>
Il. 11.429   [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰὼν καί μιν πρὸς μῦθον ἔειπεν    <στῆ δὲ μάλʼ ἐγγὺς ἰὼν>
Il. 12.457   [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἐρεισάμενος βάλε μέσσας    <στῆ δὲ μάλʼ ἐγγὺς ἰών>
Il. 17.347   [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἀκόντισε δουρὶ φαεινῷ,    <στῆ δὲ μάλʼ ἐγγὺς ἰών>
-- 5 hit(s)

# [L36b] python homer/concordance.py --ngram "τὸ δ᾽ ὑπέρπτατο χάλκεον ἔγχος"
Il. 13.408   [5.5-12]  τῇ ὕπο πᾶς ἐάλη, τὸ δʼ ὑπέρπτατο χάλκεον ἔγχος,    <τὸ δʼ ὑπέρπτατο χάλκεον ἔγχος>
Il. 22.275   [5.5-12]  ἕζετο γὰρ προϊδών, τὸ δʼ ὑπέρπτατο χάλκεον ἔγχος,    <τὸ δʼ ὑπέρπτατο χάλκεον ἔγχος>
-- 2 hit(s)

# [L36d] python homer/concordance.py --ngram "καὶ τὸ μὲν ἄντα ἰδὼν ἠλεύατο"
Il. 22.274   [1-8]  καὶ τὸ μὲν ἄντα ἰδὼν ἠλεύατο φαίδιμος Ἕκτωρ·    <καὶ τὸ μὲν ἄντα ἰδὼν ἠλεύατο>
-- 1 hit(s)

# [L33a] python homer/concordance.py --ngram "ὃ δ᾽ ὑπέρπτατο σήματα πάντων"
Od. 8.192    [5.5-12]  λᾶος ὑπὸ ῥιπῆς· ὁ δʼ ὑπέρπτατο σήματα πάντων    <ὁ δʼ ὑπέρπτατο σήματα πάντων>
-- 1 hit(s)

# [L33c] python homer/concordance.py --ngram "σήματα πάντων"
Il. 23.843   [9-12]  χειρὸς ἄπο στιβαρῆς, καὶ ὑπέρβαλε σήματα πάντων.    <σήματα πάντων>
Od. 8.192    [9-12]  λᾶος ὑπὸ ῥιπῆς· ὁ δʼ ὑπέρπτατο σήματα πάντων    <σήματα πάντων>
-- 2 hit(s)

```

### A.1b Line 4: name τε … name at verse end

```
# python homer/concordance.py --regex "[Α-ΩἈ-Ὼ]\w* τε (\w+ ){0,2}[Α-ΩἈ-Ὼ]\w*[.,·;]?$"
-- 159 hit(s). Examples of the pattern τε … καί after a name + epithet:
Il. 14.29    [3.5-12]  Τυδεΐδης Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων.
Il. 14.380   [3.5-12]  Τυδεΐδης Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων·
Il. 2.678    [3-12]  τῶν αὖ Φείδιππός τε καὶ Ἄντιφος ἡγησάσθην
# Hits 82-159 with " τε καὶ ", a second τε, and τʼ filtered out (… --format tsv | tail -n +82 | cut -f1,5 | grep -v " τε καὶ " | grep -v "τε.* τε" | grep -v " τʼ"):
# 23 lines remain. Every one is A B τε (τε on the second member, e.g. Od. 9.80 κῦμα ῥόος τε, Od. 10.513 Ἀχέροντα Πυριφλεγέθων τε, Il. 23.295 τὸν ἑόν τε Πόδαργον) or a generalising τε (ὅς τε, ὥς τε, ἵνα τε).
# Hits 1-81 were read in full: all are τε … καί, τε … τε, or one of those two kinds.
```

### A.3b Simile-apodosis count (lines 42-43)

The script below runs on the concordance module. It reads every hit of `Concordance().ngram("ὡς δ᾽ ὅτε")` and `ngram("ὡς δ᾽ ὅτ᾽")` and looks up to 14 lines ahead, in the same book, for a line whose first word is ὣς, ὥς or τώς:

```python
import sys; sys.path.insert(0, 'homer')
from concordance import Concordance; import greek as G
c = Concordance(); lines = c.lines
idx = {(l.work, l.book, l.line): i for i, l in enumerate(lines)}
seen, out = set(), []
for h in c.ngram("ὡς δ᾽ ὅτε") + c.ngram("ὡς δ᾽ ὅτ᾽"):
    i = idx[(h.work, h.book, h.line)]
    if i in seen: continue
    seen.add(i); found = None
    for d in range(1, 15):
        if i + d >= len(lines) or (lines[i+d].work, lines[i+d].book) != (lines[i].work, lines[i].book): break
        w = lines[i+d].text.split()[0]
        if G.loose(w) in ('ως', 'ωσ', 'τωσ') and w.startswith(('ὣ', 'ὥ', 'τώ', 'Ὣ', 'Ὥ')):
            found = d; break
    out.append((lines[i], found))
```

Output:

```
ὡς δ᾽ ὅτε/ὅτ᾽ lines: 63; with a line opening ὣς/ὥς/τώς within 14 lines: 59; without: 4
distance distribution: [(2, 13), (3, 21), (4, 10), (5, 4), (6, 7), (7, 2), (8, 1), (13, 1)]
NO-APODOSIS-LINE: Il. 4.141 ὡς δʼ ὅτε τίς τʼ ἐλέφαντα γυνὴ φοίνικι μιήνῃ
NO-APODOSIS-LINE: Il. 4.275 ὡς δʼ ὅτʼ ἀπὸ σκοπιῆς εἶδεν νέφος αἰπόλος ἀνὴρ
NO-APODOSIS-LINE: Il. 8.555 ὡς δʼ ὅτʼ ἐν οὐρανῷ ἄστρα φαεινὴν ἀμφὶ σελήνην
NO-APODOSIS-LINE: Il. 17.263 ὡς δʼ ὅτʼ ἐπὶ προχοῇσι διιπετέος ποταμοῖο
```

The four close with τοῖοί (Il. 4.146), τοῖαι (4.280), τόσσα (8.560) and τόσσῃ (17.266); see A.3. So all 63 have an apodosis.

### A.2b check_line on the suggested remedy for line 35

```
$ python homer/check_line.py "εἰ μή οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός."
[1] εἰ μή οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός.
  SDDDDS  (unique, tier 0, 1 scansion(s))
  licences: digamma@2(οἱ);hiatus@5.5(ὠκὺ)
  OK (no flags)
```

### A.6 LSJ (Perseus, fetched 2026-10-07)

* **πάλιν**: "I. of Place, *back, backwards* (the usual sense in early Ep.), mostly joined with Verbs of going, coming, etc." … "II. of Time, *again, once more*, rare in Hom." The only Homeric citation under II is Il. 2.276. Under I it cites Il. 1.116 (δόμεναι π. "give back"), Il. 20.439 and Od. 7.143, and π. αὖτις at Od. 14.356.
* **ἐξεναρίζω**: "strip or spoil a foe slain in fight" (Il. 4.488, 13.619); "kill, slay" (Il. 6.30; Od. 11.273).
* **δίς**: "*twice, doubly,* with Nouns, δ. τόσσον *twice* as much, Od. 9.491". No other Homeric citation.
* **ἐκφέρω** V, intransitive: "*shoot forth* (before the rest)", ὦκα δ᾽ ἔπειτα αἱ Φηρητιάδαο … ἔκφερον ἵπποι· τὰς δὲ μέτ᾽ ἐξέφερον Διομήδεος … ἵπποι, Il. 23.376, cf. 759.

### A.7 Enjambment source (Dukat 1991, *Oral Tradition* 6/2-3, pp. 303-305; PDF fetched from journal.oraltradition.org, 2026-10-07)

* p. 303: "We have unperiodic enjambement when the sentence, in Kirk's formulation, could have ended with the verse, but in fact is carried over into the succeeding verse by the adding of further descriptive matter (adverbial or epithetical) or, as Parry wrote, of 'a word or phrase or clause of the same grammatical structure as one in the foregoing verse' (1929:207)."
* pp. 303-304: necessary enjambement covers cases where "the sentence cannot be considered complete at the end of the verse". Type 1 is "a subordinate clause in the former verse … and … a main clause in the latter one" (Kirk's "periodic"). Type 2 has no possible stop (Kirk's "integral"), for example when the verse end separates subject from predicate, as in Od. 1.1-2.
* p. 305, table: 0 no enjambement = "(actual) strong stop"; 1 unperiodic = "(conceivable) strong stop, (actual) comma"; 2 necessary type 1 = comma; 3 necessary type 2 = none.
* p. 305, Parry's results (1929:204): Iliad 48.5% / 24.8% / 26.6%; Odyssey 44.8% / 26.6% / 28.5% (none / unperiodic / necessary).

Parry's TAPA article itself was not accessed: [unverified at first hand].

### A.8 Tally script (prints the counts in §2 and §5)

```python
# python tally.py review/philology_v1.md
import re, sys, collections
rows = []; inside = False
for line in open(sys.argv[1], encoding='utf-8'):
    if line.startswith('## '): inside = line.startswith('## 7.')
    if not inside or not re.match(r'^\| \d+ \|', line): continue
    cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
    comp, rev = [x.strip() for x in cells[-1].split('→')]
    rows.append((int(cells[0]), cells[1], comp, rev))
assert [r[0] for r in rows] == list(range(1, len(rows) + 1))
N = len(rows); v = collections.Counter(r[1] for r in rows)
print('lines', N); print('verdicts', dict(v))
for k in ('FAIL', 'QUERY'): print(k, [r[0] for r in rows if r[1] == k])
for who, i in (('composer', 2), ('reviewer', 3)):
    c = collections.Counter(r[i] for r in rows)
    print(who, {t: f"{c[t]} ({100*c[t]/N:.1f}%)" for t in ('none', 'unperiodic', 'necessary')})
print('disagreements', [(r[0], r[2], r[3]) for r in rows if r[2] != r[3]])
```
