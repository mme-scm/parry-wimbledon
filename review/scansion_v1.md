# Scansion review: composition/drafts/v1.txt (55 verses)

Reviewer: scansion-verifier, 2026-10-07. Order of work: (1) independent scansion of every verse, syllable by syllable, with quantities justified from homer/dichrona.tsv, homer/dichrona_analogy.tsv, homer/digamma.tsv, homer/licences.tsv, homer/positions.tsv and concordance queries (appendix); (2) only then `python homer/check_line.py --file composition/drafts/v1.txt --json`; (3) only then composition/drafts/v1.jsonl. Invented names: quantities taken as given by composition/brief.md §4 ("metre only"). They are checked for consistency and for slot, not for quantity.

## Summary

* Verdicts: **PASS 47, FAIL 1, QUERY 7** (of 55).
* FAIL: 35 (ἄρ᾽ elided before enclitic dative οἱ (ϝοι): digamma neglected).
* QUERY: 27, 49 (the digamma of ἰσόθεος is used to make position after -ος, which is unattested for this word and contradicted 2/2); 19, 33, 46 (Ἑλβέτιος/-ίου at 3-5), 47 (Ἑλβετίου at 7-9), 41 (Σέρβος at 4-5): invented names in slots that brief §4 does not mark as passing, all metrically clean.
* Valid hexameters: 55/55. Each has a unique scansion. 54 are tier 0; verse 43 is tier 1 (lengthening before μέγα, the verbatim Il. 22.163).
* My scansion = composer's scansion = check_line on all 55 verses (pattern, L/S string, syllabification, word positions and licences identical). The recorded `check_line` block in the jsonl matches a fresh run (status, tier, flags, number of warnings).
* check_line: 0 flags, 0 unmetrical, exit 0. My 8 non-PASS verdicts rest on points the tool does not test: elision before a digamma word, which use of a digamma licence is attested for a given word, and the brief's slot list.
* Spondaic fifth feet: **none** (every fifth foot is a dactyl).
* Word end at a position with < 1% frequency (positions.tsv; only 7.5 qualifies: lexical 0.909%, orthographic 6.67%): **none**. Hermann's bridge is respected in all 55. Lexical word end at 11 (1.454%, above threshold) occurs only in the formulae ἰσόθεος φώς (27, 41, 49) and λέων ὣς (38).
* Main caesura: every verse has a penthemimeral or trochaic caesura.
* Licences used (all attested for the form in homer/licences.tsv): correption μοι (1), μή (35), λούεσθαι (18), καί (22, 39), κεῖται (43); hiatus ὠκύ (35, 52), ἰσχία (39); hiatus_long διαμετρητῷ (11); muta cum liquida ἀμφιβρότην (8), before πρῶτος (5; 1 Homeric instance, Od. 17.275), Κρονίων (13), κροαίνων (17); digamma οἱ (9), ἶσα (13, 21, 26), ἶσος (37), ἑέ (40), ἰσόθεος (27, 41, 49); lengthening before μέγα (43).

## Invented names: consistency and slots (brief §4)

| name | shape used | verses (slot) | brief passing slot | verdict |
|---|---|---|---|---|
| Φεδερῆρος / -ον | SSLX | 4, 14, 20, 24, 30, 34 nom.; 29 acc. (all 9.5-12, after βοὴν ἀγαθός/-όν) | 9.5-12 | consistent, in slot |
| Φεδερεύς | SSL | 25, 32 (3.5-5) | 3.5-5, 1.5-3 | consistent, in slot |
| Ῥογῆρος | SLX | 27, 49 (6-8, after τε / γε) | 6-8 after a vowel | in slot; see the digamma QUERY |
| Ἑλβέτιος / -ίου (ι short) | LSSL | 5, 12, 52 (1-3); 19, 33, 46 (3-5); 47 (7-9) | 1-3 only | quantity consistent; 4 verses outside the brief slot |
| Ζοκοβεύς / -ῆος | SSL / SSLX | 4, 23 (3.5-5); 46 gen. (9.5-12) | nom. 3.5-5, 1.5-3; gen. 9.5-12 | consistent, in slot; ζ is always preceded by a long (αὖ, -ος, -ου at a longum) |
| Ζοκοβίδης (ῑ) | SSLL | 48, 51 (9.5-12 after κρατερός) | 9.5-12 | consistent, in slot |
| Σέρβος | LX | 10, 29, 38, 53 (1-2); 41 (4-5) | 1-2; 11-12 after a vowel | consistent; verse 41 outside the brief slot |
| Νοβάκος (ᾱ) | SLX | 50 (10-12 after αὖτε) | 10-12 after a vowel | consistent, in slot |

Every occurrence gives each name the same quantities. Epithets are not shared: Federer has βοὴν ἀγαθός (7x) and ἰσόθεος φώς (3x); Djokovic has κρατερός (2x), ἀντίθεος (2x) and περικλυτός (1x). For the philologist, outside metre: verse 1 δαΐφρονε is a dual and covers both men.

## Per-verse table

Patterns are feet 1-5 plus the sixth foot (S), as in homer/scansion.tsv. "composer" = `scansion.pattern` in v1.jsonl; "check_line" = fresh run.

| n | mine | composer | check_line | licences | flags / notes | verdict |
|---|---|---|---|---|---|---|
| 1 | DDDDDS | DDDDDS | DDDDDS | correption@2(μοι) | δαΐφρονε: α S by dichrona_analogy (δαι=S, 12 forms; δαΐφρονα 11x S) | **PASS** |
| 2 | DSDDDS | DSDDDS | DSDDDS | - | - | **PASS** |
| 3 | SSDSDS | SSDSDS | SSDSDS | - | - | **PASS** |
| 4 | DDDDDS | DDDDDS | DDDDDS | - | ἀντίθεος: ι S, no dichrona row; concordance Il. 9.623 ἀντίθεος at 1-3 (same slot); Ζοκοβεύς 3.5-5 = brief slot | **PASS** |
| 5 | DDDDDS | DDDDDS | DDDDDS | muta_cum_liquida_initial@4(πρῶτος) | Ἑλβέτιος ι S metre-only, slot 1-3 = brief; τεύχεα α S: no dichrona row, accent rule (acute on antepenult) + same phrase Il. 3.328; MCL before πρῶτος attested 1x (Od. 17.275@2) | **PASS** |
| 6 | SSDSDS | SSDSDS | SSDSDS | - | - | **PASS** |
| 7 | DDDSDS | DDDSDS | DDDSDS | - | - | **PASS** |
| 8 | DDDDDS | DDDDDS | DDDDDS | muta_cum_liquida@3.5(ἀμφιβρότην) | - | **PASS** |
| 9 | DDDDDS | DDDDDS | DDDDDS | digamma@6(οἱ) | digamma οἱ after ὅ: exact Il. 3.338 | **PASS** |
| 10 | SDDDDS | SDDDDS | SDDDDS | - | - | **PASS** |
| 11 | SSDSDS | SSDSDS | SSDSDS | hiatus_long@9(διαμετρητῷ) | hiatus_long τῷ at 9: exact Il. 3.344 | **PASS** |
| 12 | DSDDDS | DSDDDS | DSDDDS | - | Ἑλβέτιος ι S metre-only, slot 1-3 = brief | **PASS** |
| 13 | SDDDDS | SDDDDS | SDDDDS | digamma@4(ἶσα);muta_cum_liquida_initial@9.5(Κρονίων) | - | **PASS** |
| 14 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 15 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 16 | DDDSDS | DDDSDS | DDDSDS | - | ἀκοστήσας final α L at 9: no dichrona row (excluded as licence-explicable); exact line Il. 6.506 = 15.263; acute on long penult implies long final (-σᾱς) | **PASS** |
| 17 | DSSDDS | DSSDDS | DSSDDS | muta_cum_liquida_initial@9.5(κροαίνων) | - | **PASS** |
| 18 | SSDSDS | SSDSDS | SSDSDS | correption@5.5(λούεσθαι) | - | **PASS** |
| 19 | DDDDDS | DDDDDS | DDDDDS | - | Ἑλβέτιος/-ίου at 3-5 (after ὅ γ᾽): not a brief §4.1 passing slot (brief lists 1-3 only); metrically clean here | **QUERY** |
| 20 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 21 | DDDDDS | DDDDDS | DDDDDS | digamma@4(ἶσα) | lex. word end only at 12 after πτόλεμός τε (orth. 11) | **PASS** |
| 22 | SDSDDS | SDSDDS | SDSDDS | correption@10(καὶ) | - | **PASS** |
| 23 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 24 | SDDDDS | SDDDDS | SDDDDS | - | - | **PASS** |
| 25 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 26 | SDDDDS | SDDDDS | SDDDDS | digamma@4(ἶσα) | exact Il. 12.436 = 15.413 | **PASS** |
| 27 | DDDSDS | DDDSDS | DDDSDS | digamma@8(ἰσόθεος) | ρος at 8 is long only if the ϝ of ἰσόθεος makes position after -ς. licences.tsv attests the digamma of ἰσόθεος 12x, all blocking hiatus after a vowel-final word; no Homeric ἰσόθεος follows -ς; both consonant-final cases (κίεν, Il. 2.565, 11.428) scan εν short, so ϝ there does not make position. check_line passes because it keys on the licence name. Also Naeke: word end at 8 after a spondaic 4th foot (7.0% of Homeric lines: no flag) | **QUERY** |
| 28 | DDSDDS | DDSDDS | DDSDDS | - | - | **PASS** |
| 29 | SDDDDS | SDDDDS | SDDDDS | - | - | **PASS** |
| 30 | SDDDDS | SDDDDS | SDDDDS | - | - | **PASS** |
| 31 | DDDDDS | DDDDDS | DDDDDS | - | ἀργαλέῳ α S: no dichrona row; exact line Il. 13.85 | **PASS** |
| 32 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 33 | DDDDDS | DDDDDS | DDDDDS | - | Ἑλβέτιος/-ίου at 3-5 (after βάλ᾽): not a brief §4.1 passing slot (brief lists 1-3 only); metrically clean here | **QUERY** |
| 34 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 35 | DDDDDS | DDDDDS | DDDDDS | correption@1.5(μὴ);hiatus@5.5(ὠκὺ) | ἄρ᾽ elided before enclitic dative οἱ (ϝοι): digamma neglected. No Homeric instance (all 12 elisions before unaccented οἱ are the article; Homer writes δέ οἱ 254x, ῥά οἱ 28x with hiatus). The model Il. 14.407 has ῥά οἱ. check_line has no licence for elision before ϝ and does not flag it. Fix that scans (check_line SDDDDS, tier 0, no flags): εἰ μή οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός | **FAIL** |
| 36 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 37 | DDDDDS | DDDDDS | DDDDDS | digamma@10(ἶσος) | - | **PASS** |
| 38 | SDDDDS | SDDDDS | SDDDDS | - | lex. word end at 11 (λέων ὣς; 1.45% lex., >1%), = Il. 20.164 second half | **PASS** |
| 39 | SSDDDS | SSDDDS | SSDDDS | correption@6(καὶ);hiatus@8(ἰσχία) | - | **PASS** |
| 40 | DDDSDS | DDDSDS | DDDSDS | digamma@3(ἑὲ) | - | **PASS** |
| 41 | DSDDDS | DSDDDS | DSDDDS | digamma@8(ἰσόθεος) | Σέρβος at 4-5: brief §4.2 passing slots are 1-2 and 11-12; metrically clean (composer cites Αἴας at 4-5, Il. 7.206) | **QUERY** |
| 42 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 43 | DSDDDS | DSDDDS | DSDDDS | lengthening_liquid@7(μέγα);correption@9.5(κεῖται) | tier 1 lengthening_liquid δὲ μέγα at 7: exact line Il. 22.163 (scansion.tsv has the same licence) | **PASS** |
| 44 | DSDDDS | DSDDDS | DSDDDS | - | - | **PASS** |
| 45 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |
| 46 | DDSDDS | DDSDDS | DDSDDS | - | Ἑλβέτιος/-ίου at 3-5 (after ἄρ᾽): not a brief §4.1 passing slot (brief lists 1-3 only); metrically clean here; ἀντιθέου ι S as Od. 20.369 (7-9); Ζοκοβῆος 9.5-12 = brief slot | **QUERY** |
| 47 | DDDDDS | DDDDDS | DDDDDS | - | Ἑλβετίου at 7-9: brief §4.1 tested 7-9 only after ἔπειτα (flagged for hiatus); here after δ᾽, no hiatus, metrically clean; slot not marked passing | **QUERY** |
| 48 | DDDDDS | DDDDDS | DDDDDS | - | Ζοκοβίδης ῑ metre-only, 9.5-12 after κρατερὸς = brief slot | **PASS** |
| 49 | DDDSDS | DDDSDS | DDDSDS | digamma@8(ἰσόθεος) | ρος at 8 is long only if the ϝ of ἰσόθεος makes position after -ς. licences.tsv attests the digamma of ἰσόθεος 12x, all blocking hiatus after a vowel-final word; no Homeric ἰσόθεος follows -ς; both consonant-final cases (κίεν, Il. 2.565, 11.428) scan εν short, so ϝ there does not make position. check_line passes because it keys on the licence name. Also Naeke: word end at 8 after a spondaic 4th foot (7.0% of Homeric lines: no flag) | **QUERY** |
| 50 | DDDDDS | DDDDDS | DDDDDS | - | Νοβάκος ᾱ metre-only, 10-12 after vowel-final αὖτε = brief slot | **PASS** |
| 51 | DDDDDS | DDDDDS | DDDDDS | - | Ζοκοβίδης ῑ metre-only, 9.5-12 = brief slot | **PASS** |
| 52 | DDDDDS | DDDDDS | DDDDDS | hiatus@5.5(ὠκὺ) | Ἑλβετίου ι S metre-only, slot 1-3 = brief; hiatus ὠκὺ ἐτώσιον as Il. 14.407 | **PASS** |
| 53 | SDDDDS | SDDDDS | SDDDDS | - | - | **PASS** |
| 54 | SSDDDS | SSDDDS | SSDDDS | - | - | **PASS** |
| 55 | DDDDDS | DDDDDS | DDDDDS | - | - | **PASS** |

## Discrepancies with the composer's jsonl and with check_line

Scansion: **none**. On all 55 verses the jsonl `scansion` fields (pattern, quantities, syllables, word_positions, licences) equal mine and the fresh check_line run.

Documentation and judgement:

1. The jsonl has no `quantity` field. Brief §4 and §5.5 ask for `quantity: metre-only`; the composer uses free-text `quantity_notes` instead. The notes do cover all 10 verses with metre-only names (5, 12, 19, 33, 46, 47, 48, 50, 51, 52), so this is a format discrepancy only.
2. `quantity_notes` is empty for three check_line warnings on Homeric words: τεύχεα α S (5), ἀκοστήσας α L at 9 (16), ἀργαλέῳ α S (31). All three are in verbatim Homeric wording (Il. 3.328, Il. 6.506, Il. 13.85), so they are harmless; the composer's δαΐφρονε (1) and ἀντίθεος/ἀντιθέου (4, 46) notes are correct.
3. `name_formula` labels Ἑλβέτιος at 3-5 (19, 33, 46) and at 7-9 (47) as "shape 2". Brief §4.3 defines shape 2 as line-initial LSSL at 1-3. The composer gives LSSL parallels at 3-5 (Δαρδανίδης, Il. 3.303), but the brief never tested or approved those slots.
4. Verses 27 and 49: the sources cite Il. 23.677 as the model for Ῥογῆρος ἰσόθεος φώς. There ἰσόθεος follows a vowel (ἀνίστατο), and no Homeric verse has it after -ς. The brief's own test line (τὸν δ᾽ ἠμείβετ᾽ ἔπειτα Ῥογῆρος ἰσόθεος φώς) has the same issue, so this is a brief-level question.
5. Verse 35: the modification note (ὅττί ῥά οἱ → εἰ μὴ ἄρ᾽ οἱ) does not say that the change gives up the digamma of οἱ.
6. check_line passes all 55. My verdict differs on 35 (FAIL) and on 19, 27, 33, 41, 46, 47, 49 (QUERY), for the reasons in the table. None of them is a scansion disagreement.

## Evidence commands (rerun from the repository root, `source .venv/bin/activate`)

* `python homer/check_line.py --file composition/drafts/v1.txt --json` (0 flagged of 55)
* `python homer/concordance.py --loose "ἰσόθεος"` (14 hits, all at 9-11; preceded by a vowel except κίεν in Il. 2.565, 11.428); `awk -F'\t' '($1=="Il"&&$2=="2"&&$3=="565")||($1=="Il"&&$2=="11"&&$3=="428")' homer/scansion.tsv` (κί.εν scanned SS before ἰ.σό.θε.ος)
* `python homer/concordance.py --regex "ʼ οἱ[ ,.·;]"` (12 hits; all article οἱ), `--ngram "δέ οἱ"` (254), `--ngram "ῥά οἱ"` (28), `--ngram "ἄρʼ οἱ"` (1, Il. 7.169 οἵ γʼ = pronoun)
* `python homer/check_line.py "εἰ μή οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός."` (SDDDDS, tier 0, no flags)
* `grep -P '^digamma\tἰσόθεος\t' homer/licences.tsv` (12, all @8 after a vowel-final word); `grep -P '^muta_cum_liquida_initial\tπρῶτος\t' homer/licences.tsv` (1, Od. 17.275@2)
* Naeke share: `awk -F'\t' 'NR>1&&$4=="unique"{n++;if($19~/naeke/)k++}END{print k,n}' homer/scansion.tsv` (1904 / 27162 = 7.0%)
* `python homer/concordance.py --loose "ἀντίθεος"` (Il. 9.623 at 1-3), `--loose "ἀντιθέου"` (Od. 20.369 at 7-9)

## Appendix: my scansion, syllable by syllable

Legend: L long, S short, X final anceps. Reasons: n = nature (η ω, diphthong, circumflex; ε ο short); p(..) = position, with the consonants; c = epic correption; h = hiatus; hl = long vowel kept in hiatus; d = digamma (homer/digamma.tsv) blocks hiatus or correption; dp = digamma makes position; m / mi = muta cum liquida inside a word / before an initial cluster leaves the vowel short; ll = lengthening before an initial liquid; dt = homer/dichrona.tsv (all attestations agree); an = dichrona_analogy.tsv; acc = accent rule; cc = concordance attestation (cited); MO = metre-only quantity of an invented name (brief §4). Syllables are written with the consonants they are pronounced with (δἄ = δ᾽ ἄ).

**1** ἄνδρε μοι ἔννεπε, Μοῦσα, δαΐφρονε, τὼ περὶ νίκης  
DDDDDS: ἄν L p(νδρ) · δρε S n · μοι S c · ἔν L p(νν) · νε S n · πε S n · Μοῦ L n · σα S dt · δα S an(δαι=S) · ΐ L p(φρ) · φρο S n · νε S n · τὼ L n · πε S n · ρὶ S dt · νί L dt · κης X  
licences: correption@2(μοι)

**2** δηρὸν ἐμαρνάσθην ἔριδος πέρι θυμοβόροιο,  
DSDDDS: δη L n · ρὸ S n · νἐ S n · μαρ L p(ρν) · νάσ L p(σθ) · θην L n · ἔ S n · ρι S dt · δος L p(ς π) · πέ S n · ρι S dt · θυ L dt · μο S n · βό S n · ροι L n · ο X  
licences: -

**3** ἐξ οὗ δὴ τὰ πρῶτα διαστήτην ἐρίσαντε  
SSDSDS: ἐξ L p(ξ) · οὗ L n · δὴ L n · τὰ L p(πρ) · πρῶ L n · τα S dt · δι S dt · ασ L p(στ) · τή L n · την L n · ἐ S n · ρί S dt · σαν L p(ντ) · τε X  
licences: -

**4** ἀντίθεος Ζοκοβεύς τε βοὴν ἀγαθὸς Φεδερῆρος.  
DDDDDS: ἀν L p(ντ) · τί S cc(ἀντίθεος Il. 9.623@1-3) · θε S n · ος L p(ς ζ) · Ζο S n · κο S n · βεύς L n · τε S n · βο S n · ὴν L n · ἀ S dt · γα S dt · θὸς L p(ς φ) · Φε S n · δε S n · ρῆ L n · ρος X  
licences: -

**5** Ἑλβέτιος δ᾽ ἄρα πρῶτος ἐδύσετο τεύχεα καλά·  
DDDDDS: Ἑλ L p(λβ) · βέ S n · τι S MO · ος L p(ς δ) · δἄ S dt · ρα S dt+mi(πρ) · πρῶ L n · το S n · σἐ S n · δύ L dt · σε S n · το S n · τεύ L n · χε S n · α S acc+cc(Il. 3.328) · κα L dt · λά X  
licences: muta_cum_liquida_initial@4(πρῶτος)

**6** κνημῖδας μὲν πρῶτα περὶ κνήμῃσιν ἔθηκε,  
SSDSDS: κνη L n · μῖ L n · δας L p(ς μ) · μὲν L p(ν π) · πρῶ L n · τα S dt · πε S n · ρὶ L p(κν) · κνή L n · μῃ L n · σι S dt · νἔ S n · θη L n · κε X  
licences: -

**7** δεύτερον αὖτε χιτῶνα περὶ στήθεσσιν ἔδυνε,  
DDDSDS: δεύ L n · τε S n · ρο S n · ναὖ L n · τε S n · χι S dt · τῶ L n · να S dt · πε S n · ρὶ L p(στ) · στή L n · θεσ L p(σσ) · σι S dt · νἔ S n · δυ L dt · νε X  
licences: -

**8** ἂν δ᾽ ἕλετ᾽ ἀμφιβρότην πολυδαίδαλον ἀσπίδα θοῦριν,  
DDDDDS: ἂν L p(ν δ) · δἕ S n · λε S n · τἀμ L p(μφ) · φι S dt+m(βρ) · βρό S n · την L n · πο S n · λυ S dt · δαί L n · δα S dt · λο S n · νἀσ L p(σπ) · πί S dt · δα S dt · θοῦ L n · ριν X  
licences: muta_cum_liquida@3.5(ἀμφιβρότην)

**9** εἵλετο δ᾽ ἄλκιμον ἔγχος, ὅ οἱ παλάμηφιν ἀρήρει.  
DDDDDS: εἵ L n · λε S n · το S n · δἄλ L p(λκ) · κι S dt · μο S n · νἔγ L p(γχ) · χο S n · σὅ S n · οἱ L n+d · πα S dt · λά S dt · μη L n · φι S dt · νἀ S dt · ρή L n · ρει X  
licences: digamma@6(οἱ)

**10** Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν ἐδύσετο νώροπα χαλκόν.  
SDDDDS: Σέρ L p(ρβ) · βος L p(ς δ) · δαὖ L n · θἑ S n · τέ S n · ρω L n · θε S n · νἐ S n · δύ L dt · σε S n · το S n · νώ L n · ρο S n · πα S dt · χαλ L p(λκ) · κόν X  
licences: -

**11** καί ῥ᾽ ἐγγὺς στήτην διαμετρητῷ ἐνὶ χώρῳ.  
SSDSDS: καί L n · ῥἐγ L p(γγ) · γὺς L p(ς στ) · στή L n · την L n · δι S dt · α S dt · με L p(τρ) · τρη L n · τῷ L hl · ἐ S n · νὶ S dt · χώ L n · ρῳ X  
licences: hiatus_long@9(διαμετρητῷ)

**12** Ἑλβέτιος δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ·  
DSDDDS: Ἑλ L p(λβ) · βέ S n · τι S MO · ος L p(ς δ) · δὲ L p(πρ) · πρῶ L n · το S n · σἀ S dt · κόν L p(ντ) · τι S dt · σε S n · δου L n · ρὶ S dt · φα S dt · ει L n · νῷ X  
licences: -

**13** ἔνθά σφιν κατὰ ἶσα μάχην ἐτάνυσσε Κρονίων.  
SDDDDS: ἔν L p(νθ) · θά L p(σφ) · σφιν L p(ν κ) · κα S dt · τὰ S dt+d · ἶ L n · σα S dt · μά S dt · χην L n · ἐ S n · τά S dt · νυσ L p(σσ) · σε S mi(κρ) · Κρο S n · νί L dt · ων X  
licences: digamma@4(ἶσα); muta_cum_liquida_initial@9.5(Κρονίων)

**14** τρὶς μὲν ἔπειτ᾽ ἀφάμαρτε βοὴν ἀγαθὸς Φεδερῆρος,  
DDDDDS: τρὶς L p(ς μ) · μὲ S n · νἔ S n · πει L n · τἀ S dt · φά S dt · μαρ L p(ρτ) · τε S n · βο S n · ὴν L n · ἀ S dt · γα S dt · θὸς L p(ς φ) · Φε S n · δε S n · ρῆ L n · ρος X  
licences: -

**15** ἀλλ᾽ ὅτε δὴ τὸ τέταρτον, ὃ δ᾽ ἐσσυμένως λάβ᾽ ἄεθλον.  
DDDDDS: ἀλ L p(λλ) · λὅ S n · τε S n · δὴ L n · τὸ S n · τέ S n · ταρ L p(ρτ) · το S n · νὃ S n · δἐσ L p(σσ) · συ S dt · μέ S n · νως L n · λά S dt · βἄ S dt · ε L p(θλ) · θλον X  
licences: -

**16** ὡς δ᾽ ὅτε τις στατὸς ἵππος ἀκοστήσας ἐπὶ φάτνῃ  
DDDSDS: ὡς L n · δὅ S n · τε S n · τις L p(ς στ) · στα S dt · τὸ S n · σἵπ L p(ππ) · πο S n · σἀ S dt · κοσ L p(στ) · τή L n · σα L acc(-σᾱς)+cc(Il. 6.506) · σἐ S n · πὶ S dt · φάτ L p(τν) · νῃ X  
licences: -

**17** δεσμὸν ἀπορρήξας θείῃ πεδίοιο κροαίνων  
DSSDDS: δεσ L p(σμ) · μὸ S n · νἀ S dt · πορ L p(ρρ) · ρή L n · ξας L p(ς θ) · θεί L n · ῃ L n · πε S n · δί S dt · οι L n · ο S mi(κρ) · κρο S n · αί L n · νων X  
licences: muta_cum_liquida_initial@9.5(κροαίνων)

**18** εἰωθὼς λούεσθαι ἐϋρρεῖος ποταμοῖο,  
SSDSDS: εἰ L n · ω L n · θὼς L n · λού L n · εσ L p(σθ) · θαι S c · ἐ S n · ϋρ L p(ρρ) · ρεῖ L n · ος L p(ς π) · πο S n · τα S dt · μοῖ L n · ο X  
licences: correption@5.5(λούεσθαι)

**19** ὣς ἄρ᾽ ὅ γ᾽ Ἑλβέτιος τότ᾽ ἐπέσσυτο δεύτερον αὖτε·  
DDDDDS: ὣς L n · σἄ S dt · ρὅ S n · γἙλ L p(λβ) · βέ S n · τι S MO · ος L p(ς τ) · τό S n · τἐ S n · πέσ L p(σσ) · συ S dt · το S n · δεύ L n · τε S n · ρο S n · ναὖ L n · τε X  
licences: -

**20** τρὶς δέ μιν ἐξενάριξε βοὴν ἀγαθὸς Φεδερῆρος.  
DDDDDS: τρὶς L p(ς δ) · δέ S n · μι S dt · νἐξ L p(ξ) · ξε S n · νά S dt · ρι L p(ξ) · ξε S n · βο S n · ὴν L n · ἀ S dt · γα S dt · θὸς L p · Φε S n · δε S n · ρῆ L n · ρος X  
licences: -

**21** τὸ τρίτον αὖτ᾽ ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε·  
DDDDDS: τὸ L p(τρ) · τρί S dt · το S n · ναὖ L n · τἐ S n · πὶ S dt+d · ἶ L n · σα S dt · μά S dt · χη L n · τέ S n · τα S dt · το L p(πτ) · πτό S n · λε S n · μός L p(ς τ) · τε X  
licences: digamma@4(ἶσα)

**22** σφαῖραν δ᾽ ἀμφοτέρω βάλλον πάλιν ἔνθα καὶ ἔνθα,  
SDSDDS: σφαῖ L n · ραν L p(ν δ) · δἀμ L p(μφ) · φο S n · τέ S n · ρω L n · βάλ L p(λλ) · λον L p(ν π) · πά S dt · λι S dt · νἔν L p(νθ) · θα S dt · καὶ S c · ἔν L p(νθ) · θα X  
licences: correption@10(καί)

**23** δεύτερον αὖ Ζοκοβεὺς πάλιν ἐσσυμένως λάβ᾽ ἄεθλον.  
DDDDDS: δεύ L n · τε S n · ρο S n · ναὖ L n · Ζο S n · κο S n · βεὺς L n · πά S dt · λι S dt · νἐσ L p(σσ) · συ S dt · μέ S n · νως L n · λά S dt · βἄ S dt · ε L p(θλ) · θλον X  
licences: -

**24** δὶς δ᾽ αὖτ᾽ ἐξενάριξε βοὴν ἀγαθὸς Φεδερῆρος·  
SDDDDS: δὶς L p(ς δ) · δαὖ L n · τἐξ L p(ξ) · ξε S n · νά S dt · ρι L p(ξ) · ξε S n · βο S n · ὴν L n · ἀ S dt · γα S dt · θὸς L p · Φε S n · δε S n · ρῆ L n · ρος X  
licences: -

**25** δεύτερον αὖ Φεδερεὺς προΐει δολιχόσκιον ἔγχος·  
DDDDDS: δεύ L n · τε S n · ρο S n · ναὖ L n · Φε S n · δε S n · ρεὺς L n · προ S n · ΐ S dt · ει L n · δο S n · λι S dt · χόσ L p(σκ) · κι S dt · ο S n · νἔγ L p(γχ) · χος X  
licences: -

**26** ὣς μὲν τῶν ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε,  
SDDDDS: ὣς L n · μὲν L p(ν τ) · τῶν L n · ἐ S n · πὶ S dt+d · ἶ L n · σα S dt · μά S dt · χη L n · τέ S n · τα S dt · το L p(πτ) · πτό S n · λε S n · μός L p(ς τ) · τε X  
licences: digamma@4(ἶσα)

**27** καὶ βάλεν, οὐδ᾽ ἀφάμαρτε, Ῥογῆρος ἰσόθεος φώς.  
DDDSDS: καὶ L n · βά S dt · λε S n · νοὐ L n · δἀ S dt · φά S dt · μαρ L p(ρτ) · τε S n · Ῥο S n · γῆ L n · ρος L dp(ς+ϝ) · ἰ L dt · σό S n · θε S n · ος L p(ς φ) · φώς X  
licences: digamma@8(ἰσόθεος) as position after -ς

**28** τέτρατον ὣς ἔλαβεν· πέμπτον δ᾽ ὑπελείπετ᾽ ἄεθλον.  
DDSDDS: τέ L p(τρ) · τρα S dt · το S n · νὣ L n · σἔ S n · λα S dt · βεν L p(ν π) · πέμ L p(μπ) · πτον L p(ν δ) · δὑ S dt · πε S n · λεί L n · πε S n · τἄ S dt · ε L p(θλ) · θλον X  
licences: -

**29** Σέρβος δ᾽ ἐξενάριξε βοὴν ἀγαθὸν Φεδερῆρον,  
SDDDDS: Σέρ L p(ρβ) · βος L p(ς δ) · δἐξ L p(ξ) · ξε S n · νά S dt · ρι L p(ξ) · ξε S n · βο S n · ὴν L n · ἀ S dt · γα S dt · θὸν L p(ν φ) · Φε S n · δε S n · ρῆ L n · ρον X  
licences: -

**30** τὸν δ᾽ αὖτ᾽ ἐξενάριξε βοὴν ἀγαθὸς Φεδερῆρος·  
SDDDDS: τὸν L p(ν δ) · δαὖ L n · τἐξ L p(ξ) · ξε S n · νά S dt · ρι L p(ξ) · ξε S n · βο S n · ὴν L n · ἀ S dt · γα S dt · θὸς L p · Φε S n · δε S n · ρῆ L n · ρος X  
licences: -

**31** τῶν ῥ᾽ ἅμα τ᾽ ἀργαλέῳ καμάτῳ φίλα γυῖα λέλυντο.  
DDDDDS: τῶν L n · ῥἅ S dt · μα S dt · τἀρ L p(ργ) · γα S cc(Il. 13.85) · λέ S n · ῳ L n · κα S dt · μά S dt · τῳ L n · φί S dt · λα S dt · γυῖ L n · α S dt · λέ S n · λυν L p(ντ) · το X  
licences: -

**32** ὀψὲ δὲ δὴ Φεδερεὺς πάλιν ἄσπετον ἤρατο κῦδος·  
DDDDDS: ὀ L p(ψ) · ψὲ S n · δὲ S n · δὴ L n · Φε S n · δε S n · ρεὺς L n · πά S dt · λι S dt · νἄσ L p(σπ) · πε S n · το S n · νἤ L n · ρα S dt · το S n · κῦ L n · δος X  
licences: -

**33** δὶς δὲ βάλ᾽ Ἑλβέτιος, τὸ δ᾽ ὑπέρπτατο σήματα πάντων.  
DDDDDS: δὶς L p(ς δ) · δὲ S n · βά S dt · λἙλ L p(λβ) · βέ S n · τι S MO · ος L p(ς τ) · τὸ S n · δὑ S dt · πέρ L p(ρπτ) · πτα S dt · το S n · σή L n · μα S dt · τα S dt · πάν L p(ντ) · των X  
licences: -

**34** καί νύ κεν ἐξενάριξε βοὴν ἀγαθὸς Φεδερῆρος,  
DDDDDS: καί L n · νύ S dt · κε S n · νἐξ L p(ξ) · ξε S n · νά S dt · ρι L p(ξ) · ξε S n · βο S n · ὴν L n · ἀ S dt · γα S dt · θὸς L p · Φε S n · δε S n · ρῆ L n · ρος X  
licences: -

**35** εἰ μὴ ἄρ᾽ οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός.  
DDDDDS: εἰ L n · μὴ S c · ἄ S dt · ροἱ L n [ἄρ᾽ elided before ϝοι: digamma neglected] · βέ S n · λο S n · σὠ L n · κὺ S dt+h · ἐ S n · τώ L n · σι S dt · ο S n · νἔκ L p(κφ) · φυ S dt · γε S n · χει L n · ρός X  
licences: correption@1.5(μή); hiatus@5.5(ὠκύ); elision before οἱ (no licence name; unattested)

**36** στῆ δὲ μάλ᾽ ἐγγὺς ἰών, τὸ δ᾽ ὑπέρπτατο χάλκεον ἔγχος.  
DDDDDS: στῆ L n · δὲ S n · μά S dt · λἐγ L p(γγ) · γὺ S dt · σἰ S dt · ών L n · τὸ S n · δὑ S dt · πέρ L p(ρπτ) · πτα S dt · το S n · χάλ L p(λκ) · κε S n · ο S n · νἔγ L p(γχ) · χος X  
licences: -

**37** ἀλλ᾽ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,  
DDDDDS: ἀλ L p(λλ) · λὅ S n · τε S n · δὴ L n · τὸ S n · τέ S n · ταρ L p(ρτ) · το S n · νἐ S n · πέσ L p(σσ) · συ S dt · το S n · δαί L n · μο S n · νι S dt+d · ἶ L n · σος X  
licences: digamma@10(ἶσος)

**38** Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς·  
SDDDDS: Σέρ L p(ρβ) · βος L p(ς δ) · δαὖ L n · θἑ S n · τέ S n · ρω L n · θε S n · νἐ S n · ναν L p(ντ) · τί S dt · ο S n · νὦρ L p(ρτ) · το S n · λέ S n · ω L n · νὣς X  
licences: -

**39** οὐρῇ δὲ πλευράς τε καὶ ἰσχία ἀμφοτέρωθεν  
SSDDDS: οὐ L n · ρῇ L n · δὲ L p(πλ) · πλευ L n · ράς L p(ς τ) · τε S n · καὶ S c · ἰσ L p(σχ) · χί S dt · α S dt+h · ἀμ L p(μφ) · φο S n · τέ S n · ρω L n · θεν X  
licences: correption@6(καί); hiatus@8(ἰσχία)

**40** μαστίεται, ἑὲ δ᾽ αὐτὸν ἐποτρύνει μαχέσασθαι.  
DDDSDS: μασ L p(στ) · τί S dt · ε S n · ται L d(ϝ of ἑέ) · ἑ S n · ὲ S n · δαὐ L n · τὸ S n · νἐ S n · πο L p(τρ) · τρύ L dt · νει L n · μα S dt · χέ S n · σασ L p(σθ) · θαι X  
licences: digamma@3(ἑέ)

**41** ἔκφερε δ᾽ αὖ Σέρβος, μετὰ δ᾽ ὄρνυτο ἰσόθεος φώς.  
DSDDDS: ἔκ L p(κφ) · φε S n · ρε S n · δαὖ L n · Σέρ L p(ρβ) · βος L p(ς μ) · με S n · τὰ S dt · δὄρ L p(ρν) · νυ S dt · το S n+d · ἰ L dt · σό S n · θε S n · ος L p(ς φ) · φώς X  
licences: digamma@8(ἰσόθεος)

**42** ὡς δ᾽ ὅτ᾽ ἀεθλοφόροι περὶ τέρματα μώνυχες ἵπποι  
DDDDDS: ὡς L n · δὅ S n · τἀ S dt · ε L p(θλ) · θλο S n · φό S n · ροι L n · πε S n · ρὶ S dt · τέρ L p(ρμ) · μα S dt · τα S dt · μώ L n · νυ S dt · χε S n · σἵπ L p(ππ) · ποι X  
licences: -

**43** ῥίμφα μάλα τρωχῶσι· τὸ δὲ μέγα κεῖται ἄεθλον·  
DSDDDS: ῥίμ L p(μφ) · φα S dt · μά S dt · λα L p(τρ) · τρω L n · χῶ L n · σι S dt · τὸ S n · δὲ L ll(μ) · μέ S n · γα S dt · κεῖ L n · ται S c · ἄ S dt · ε L p(θλ) · θλον X  
licences: lengthening_liquid@7(μέγα); correption@9.5(κεῖται)

**44** καὶ τότε δὴ χρύσεια πατὴρ ἐτίταινε τάλαντα,  
DSDDDS: καὶ L n · τό S n · τε S n · δὴ L n · χρύ L dt · σει L n · α S dt · πα S dt · τὴ L n · ρἐ S n · τί S dt · ται L n · νε S n · τά S dt · λαν L p(ντ) · τα X  
licences: -

**45** ἐν δ᾽ ἐτίθει δύο κῆρε τανηλεγέος θανάτοιο,  
DDDDDS: ἐν L p(ν δ) · δἐ S n · τί S dt · θει L n · δύ S dt · ο S n · κῆ L n · ρε S n · τα S dt · νη L n · λε S n · γέ S n · ος L p(ς θ) · θα S dt · νά S dt · τοι L n · ο X  
licences: -

**46** τὴν μὲν ἄρ᾽ Ἑλβετίου, τὴν δ᾽ ἀντιθέου Ζοκοβῆος,  
DDSDDS: τὴν L n · μὲ S n · νἄ S dt · ρἙλ L p(λβ) · βε S n · τί S MO · ου L n · τὴν L n · δἀν L p(ντ) · τι S cc(ἀντιθέου Od. 20.369@7-9) · θέ S n · ου L n · Ζο S n · κο S n · βῆ L n · ος X  
licences: -

**47** ἕλκε δὲ μέσσα λαβών· ῥέπε δ᾽ Ἑλβετίου κακὸν ἦμαρ.  
DDDDDS: ἕλ L p(λκ) · κε S n · δὲ S n · μέσ L p(σσ) · σα S dt · λα S dt · βών L n · ῥέ S n · πε S n · δἙλ L p(λβ) · βε S n · τί S MO · ου L n · κα S dt · κὸ S n · νἦ L n · μαρ X  
licences: -

**48** τρὶς μὲν ἔπειτ᾽ ἐπόρουσε θοῶς κρατερὸς Ζοκοβίδης,  
DDDDDS: τρὶς L p(ς μ) · μὲ S n · νἔ S n · πει L n · τἐ S n · πό S n · ρου L n · σε S n · θο S n · ῶς L n · κρα S dt · τε S n · ρὸς L p(ς ζ) · Ζο S n · κο S n · βί L MO · δης X  
licences: -

**49** δὶς δ᾽ ἄρ᾽ ἀμύνετο τόν γε Ῥογῆρος ἰσόθεος φώς·  
DDDSDS: δὶς L p(ς δ) · δἄ S dt · ρἀ S dt · μύ L dt · νε S n · το S n · τόν L p(ν γ) · γε S n · Ῥο S n · γῆ L n · ρος L dp(ς+ϝ) · ἰ L dt · σό S n · θε S n · ος L p(ς φ) · φώς X  
licences: digamma@8(ἰσόθεος) as position after -ς

**50** δὶς δὲ βάλ᾽, οὐδ᾽ ἀφάμαρτε, περικλυτὸς αὖτε Νοβάκος.  
DDDDDS: δὶς L p(ς δ) · δὲ S n · βά S dt · λοὐ L n · δἀ S dt · φά S dt · μαρ L p(ρτ) · τε S n · πε S n · ρι L p(κλ) · κλυ S dt · τὸ S n · σαὖ L n · τε S n · Νο S n · βά L MO · κος X  
licences: -

**51** δεύτερον αὖ προΐει, βάλε δ᾽ ἂψ κρατερὸς Ζοκοβίδης,  
DDDDDS: δεύ L n · τε S n · ρο S n · ναὖ L n · προ S n · ΐ S dt · ει L n · βά S dt · λε S n · δἂψ L p(ψ) · κρα S dt · τε S n · ρὸς L p(ς ζ) · Ζο S n · κο S n · βί L MO · δης X  
licences: -

**52** Ἑλβετίου βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός.  
DDDDDS: Ἑλ L p(λβ) · βε S n · τί S MO · ου L n · βέ S n · λο S n · σὠ L n · κὺ S dt+h · ἐ S n · τώ L n · σι S dt · ο S n · νἔκ L p(κφ) · φυ S dt · γε S n · χει L n · ρός X  
licences: hiatus@5.5(ὠκύ)

**53** Σέρβος δ᾽ ἐξενάριξε, Διὸς δ᾽ ἐτελείετο βουλή.  
SDDDDS: Σέρ L p(ρβ) · βος L p(ς δ) · δἐξ L p(ξ) · ξε S n · νά S dt · ρι L p(ξ) · ξε S n · Δι S dt · ὸς L p(ς δ) · δἐ S n · τε S n · λεί L n · ε S n · το S n · βου L n · λή X  
licences: -

**54** ὣς οἳ μὲν μάρναντο δέμας πυρὸς αἰθομένοιο  
SSDDDS: ὣς L n · οἳ L n · μὲν L p(ν μ) · μάρ L p(ρν) · ναν L p(ντ) · το S n · δέ S n · μας L p(ς π) · πυ S dt · ρὸ S n · σαἰ L n · θο S n · μέ S n · νοι L n · ο X  
licences: -

**55** ὀψὲ δὲ δὴ τέλος ἦεν, ὅτ᾽ ἤλυθε δείελον ἦμαρ.  
DDDDDS: ὀ L p(ψ) · ψὲ S n · δὲ S n · δὴ L n · τέ S n · λο S n · σἦ L n · ε S n · νὅ S n · τἤ L n · λυ S dt · θε S n · δεί L n · ε S n · λο S n · νἦ L n · μαρ X  
licences: -

