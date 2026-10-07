## 7. Weaving and stitching: ῥαψῳδός, ὑφαίνω and the craft words of composition

§6 tested the analogy on counts; this section asks what the Greeks called the activity. The names are craft words, and two crafts compete: the rhapsode stitches, the lyric poet weaves. Homer has ἀοιδός (39 lines) and ἀοιδή (24; ὕμνος once, Od. 8.429) but applies neither craft verb to poetry. Homeric figures are from `python homer/concordance.py` (commands in `paper/research/weaving_primary.md` §1); other passages are quoted as fetched there on 2026-10-07, source in a comment after each.

### 7.1 ῥαψῳδός and ῥάπτω

`--loose "ραψωδ" --count` returns 0: no ῥαψῳδός, no ῥαψῳδεῖν, in either poem. The simplex occurs: of the 14 `--loose "ραπτ"` and 10 `--loose "ραψ"` hits, mostly ἀστράπτω, τέτραπτο and γραπτῦς, the regex `ῥάπτ|ῥάψ|ῥαπτ|ἐράπτ` keeps eight lines:

    Il. 12.296  ἤλασεν, ἔντοσθεν δὲ βοείας ῥάψε θαμειὰς
    Il. 18.367  οὐκ ὄφελον Τρώεσσι κοτεσσαμένη κακὰ ῥάψαι;
    Od. 3.118  εἰνάετες γάρ σφιν κακὰ ῥάπτομεν ἀμφιέποντες
    Od. 16.379  οὕνεκά οἱ φόνον αἰπὺν ἐράπτομεν οὐδʼ ἐκίχημεν·
    Od. 16.421  μάργε, τίη δὲ σὺ Τηλεμάχῳ θάνατόν τε μόρον τε
    Od. 16.422  ῥάπτεις, οὐδʼ ἱκέτας ἐμπάζεαι, οἷσιν ἄρα Ζεὺς
    Od. 16.423  μάρτυρος; οὐδʼ ὁσίη κακὰ ῥάπτειν ἀλλήλοισιν.
    Od. 24.228  ῥαπτὸν ἀεικέλιον, περὶ δὲ κνήμῃσι βοείας
    Od. 24.229  κνημῖδας ῥαπτὰς δέδετο, γραπτῦς ἀλεείνων,
<!-- https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/01b725d835e6e733062ffd79e0efdbae1ba06e5c/data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc2.xml and .../tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml (homer/source.json) -->

The object is ox-hide (βοείας, twice) or a harm, κακά, φόνον, θάνατόν τε μόρον τε, never a song. Song is the object first in the lines the Pindar scholia give to Hesiod, then in Pindar's name for the Homeridae:

    ἐν Δήλῳ τότε πρῶτον ἐγὼ καὶ Ὅμηρος ἀοιδοὶ
    μέλπομεν, ἐν νεαροῖς ὕμνοις ῥάψαντες ἀοιδήν,
    Φοῖβον Ἀπόλλωνα χρυσάορον, ὃν τέκε Λητώ.
Hesiod fr. 357 Merkelbach–West (= 265 Rzach; Evelyn-White, Fragmenta dubia 3, "Schol. on Pindar, Nem. ii. 1"); the Loeb OCR with two stray marks removed, as read in weaving_primary.md §2.
<!-- https://archive.org/download/hesiodhomerichym0000hesi_d6n3/hesiodhomerichym0000hesi_d6n3_djvu.txt -->

    ὅθεν περ καὶ Ὁμηρίδαι
    ῥαπτῶν ἐπέων τὰ πόλλ᾽ ἀοιδοὶ
    ἄρχονται, Διὸς ἐκ προοιμίου:
Pindar, Nem. 2.1–3
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0161:book=N.:poem=2 -->

Both keep Homer's nouns and change only the verb. The compound noun is classical prose; Herodotus's rhapsodes compete, and are stopped because the poems praise Argos:

    Κλεισθένης γὰρ Ἀργείοισι πολεμήσας τοῦτο μὲν ῥαψῳδοὺς ἔπαυσε ἐν Σικυῶνι ἀγωνίζεσθαι τῶν Ὁμηρείων ἐπέων εἵνεκα, ὅτι Ἀργεῖοί τε καὶ Ἄργος τὰ πολλὰ πάντα ὑμνέαται
Herodotus 5.67.1
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0125:book=5:chapter=67 -->

Plato's rhapsode is a costumed performer and interpreter of Homer, moved by θεία δύναμις, not τέχνη; the Republic makes rhapsodizing an itinerant trade:

    Ion 530b: καὶ μὴν πολλάκις γε ἐζήλωσα ὑμᾶς τοὺς ῥαψῳδούς, ὦ Ἴων, τῆς τέχνης: τὸ γὰρ ἅμα μὲν τὸ σῶμα κεκοσμῆσθαι ἀεὶ πρέπον ὑμῶν εἶναι τῇ τέχνῃ καὶ ὡς καλλίστοις φαίνεσθαι, ἅμα δὲ ἀναγκαῖον εἶναι ἔν τε ἄλλοις ποιηταῖς διατρίβειν πολλοῖς καὶ ἀγαθοῖς καὶ δὴ καὶ μάλιστα ἐν Ὁμήρῳ, τῷ ἀρίστῳ καὶ θειοτάτῳ τῶν ποιητῶν, καὶ τὴν τούτου διάνοιαν
    Ion 530c: οὐ γὰρ ἂν γένοιτό ποτε ἀγαθὸς ῥαψῳδός, εἰ μὴ συνείη τὰ λεγόμενα ὑπὸ τοῦ ποιητοῦ. τὸν γὰρ ῥαψῳδὸν ἑρμηνέα δεῖ τοῦ ποιητοῦ τῆς διανοίας γίγνεσθαι τοῖς ἀκούουσι
    Ion 533d: ἔστι γὰρ τοῦτο τέχνη μὲν οὐκ ὂν παρὰ σοὶ περὶ Ὁμήρου εὖ λέγειν, ὃ νυνδὴ ἔλεγον, θεία δὲ δύναμις ἥ σε κινεῖ, ὥσπερ ἐν τῇ λίθῳ ἣν Εὐριπίδης μὲν Μαγνῆτιν ὠνόμασεν, οἱ δὲ πολλοὶ Ἡρακλείαν.
    Ion 535e–536a: οἶσθα οὖν ὅτι οὗτός ἐστιν ὁ θεατὴς τῶν δακτυλίων ὁ ἔσχατος, ὧν ἐγὼ ἔλεγον ὑπὸ τῆς Ἡρακλειώτιδος λίθου ἀπ᾽ ἀλλήλων τὴν δύναμιν λαμβάνειν; ὁ δὲ μέσος σὺ ὁ | ῥαψῳδὸς καὶ ὑποκριτής, ὁ δὲ πρῶτος αὐτὸς ὁ ποιητής
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0179:text=Ion:section=530b (and =530c, 533d, 535e, 536a); Burnet 1903 -->

    Rep. 10.600d: Ὅμηρον δ᾽ ἄρα οἱ ἐπ᾽ ἐκείνου, εἴπερ οἷός τ᾽ ἦν πρὸς ἀρετὴν ὀνῆσαι ἀνθρώπους, ἢ Ἡσίοδον ῥαψῳδεῖν ἂν περιιόντας εἴων, καὶ οὐχὶ μᾶλλον ἂν αὐτῶν ἀντείχοντο ἢ τοῦ χρυσοῦ καὶ
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0167:book=10:section=600d -->

The going about (περιιόντας) is older than the word: the Hymn to Apollo's blind man of Chios, an ἀοιδός who πωλεῖται and will carry the girls' κλέος round the cities, is Plato's itinerant without the stitching word:

    165ἀλλ᾽ ἄγεθ᾽ ἱλήκοι μὲν Ἀπόλλων Ἀρτέμιδιξύν,
    χαίρετε δ᾽ ὑμεῖς πᾶσαι: ἐμεῖο δὲ καὶ μετόπισθεν
    μνήσασθ᾽, ὁππότε κέν τις ἐπιχθονίων ἀνθρώπων
    ἐθάδ᾽ ἁνείρηται ξεῖνος ταλαπείριος ἐλθών:
    ὦ κοῦραι, τίς δ᾽ ὔμμιν ἀνὴρ ἥδιστος ἀοιδῶν
    170ἐνθάδε πωλεῖται, καὶ τέῳ τέρπεσθε μάλιστα;
    ὑμεῖς δ᾽ εὖ μάλα πᾶσαι ὑποκρίνασθαι ἀφήμως:
    τυφλὸς ἀνήρ, οἰκεῖ δὲ Χίῳ ἔνι παιπαλοέσσῃ
    τοῦ μᾶσαι μετόπισθεν ἀριστεύσουσιν ἀοιδαί.
    ἡμεῖς δ᾽ ὑμέτερον κλέος οἴσομεν, ὅσσον ἐπ᾽ αἶαν
    175ἀνθρώπων στρεφόμεσθα πόλεις εὖ ναιεταώσας:
    οἳ δ᾽ ἐπὶ δὴ πείσονται, ἐπεὶ καὶ ἐτήτυμόν ἐστιν.
Homeric Hymn to Apollo 165–176 (as fetched; Ἀρτέμιδιξύν and τοῦ μᾶσαι sic, for Ἀρτέμιδι ξύν and τοῦ πᾶσαι)
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0137:hymn=3:card=165 -->

The etymology of the simplex is unsettled: Beekes gives ῥάπτω no Indo-European root, since Mycenaean e-ra-pe-me-na shows no initial ϝ- and "the older etymology with Baltic (Lith. verpti ... 'to spin' ...) must be abandoned" [Beekes 2010 s.v. ῥάπτω, pp. 1275–1276, archive.org OCR]. LIV² has no lemma ῥάπτω; it stands bracketed and queried under *u̯erp- 'hin- und herdrehen (?)', with the note "Semantisch und formal unklar, könnte auch Anlaut *sr° haben" [LIV² 2001, pp. 690–691, OCR]. The compound is clearer: Beekes reads ῥαψῳδός as a verbal governing compound of ῥάψαι ᾠδήν (ἀοιδήν), "originally 'who sews a poem together', referring to the uninterrupted sequence of epic verses as opposed to the strophic compositions of lyrics" [Beekes 2010 s.v. ῥαψῳδός, p. 1278, OCR]. LSJ agrees and names the rival: "Prob. from ῥάπτω, ἀοιδή ...: not from ῥάβδος ... as if ῥαβδῳδός (Eust.6.24 ...)" [LSJ s.v. ῥαψῳδός]. Chantraine's entry is legible in the OCR only in its Greek and numerals (Hes. fr. 265 = 357 M-W, Pi. N. 2.2, Patzer 1952, Sealey 1957, Schmitt §§ 608–609) [Chantraine DELG s.v. ῥαψῳδός, text unverified].

### 7.2 ὑφαίνω and *u̯ebʰ-

`--loose "υφαιν"` returns 23 hits, four of them προφαίνω; with the four aorist ὑφην- forms that is 23 forms of ὑφαίνω, beside ὑφαντός 3, ὑφόωσι 1 (Od. 7.105, ὑφάω) and ὕφασμα 1 (Od. 3.274). The object is one of two things: the web, ἱστόν (φάρεʼ ὑφαίνουσιν, Od. 13.108, is the exception LSJ notes), or the plan, μῆτιν in seven lines, δόλον in two, μύθους καὶ μήδεα once; never ἀοιδή, ἔπεα or ὕμνος. The verb is localised: 13 of the 23 forms close the line at 10–12, seven begin at 6 after the trochaic caesura (Il. 7.324, 9.93; Od. 2.104, 5.356, 19.149, 24.139, 24.147), three stand elsewhere (positions in weaving_primary.md §1.1). So μῆτιν ὕφαινον/ὑφήνας/ὑφήνω is a line-end formula (9–12) in four lines, split by ἤρχετο in the whole-verse repeat Il. 7.324 = 9.93, and set before the trochaic caesura as an imperative at Od. 13.386:

    Il. 3.212  ἀλλʼ ὅτε δὴ μύθους καὶ μήδεα πᾶσιν ὕφαινον
    Il. 6.187  τῷ δʼ ἄρʼ ἀνερχομένῳ πυκινὸν δόλον ἄλλον ὕφαινε·
    Il. 7.324  τοῖς ὁ γέρων πάμπρωτος ὑφαίνειν ἤρχετο μῆτιν
    Il. 9.93  τοῖς ὁ γέρων πάμπρωτος ὑφαίνειν ἤρχετο μῆτιν
    Od. 4.678  αὐλῆς ἐκτὸς ἐών· οἱ δʼ ἔνδοθι μῆτιν ὕφαινον.
    Od. 4.739  εἰ δή πού τινα κεῖνος ἐνὶ φρεσὶ μῆτιν ὑφήνας
    Od. 5.356  ὤ μοι ἐγώ, μή τίς μοι ὑφαίνῃσιν δόλον αὖτε
    Od. 9.422  εὑροίμην· πάντας δὲ δόλους καὶ μῆτιν ὕφαινον
    Od. 13.303  νῦν αὖ δεῦρʼ ἱκόμην, ἵνα τοι σὺν μῆτιν ὑφήνω
    Od. 13.386  ἀλλʼ ἄγε μῆτιν ὕφηνον, ὅπως ἀποτίσομαι αὐτούς·
<!-- PerseusDL canonical-greekLit, commit 01b725d8, files as above -->

Helen's web is a picture of the war:

    Il. 3.125  τὴν δʼ εὗρʼ ἐν μεγάρῳ· ἣ δὲ μέγαν ἱστὸν ὕφαινε
    Il. 3.126  δίπλακα πορφυρέην, πολέας δʼ ἐνέπασσεν ἀέθλους
    Il. 3.127  Τρώων θʼ ἱπποδάμων καὶ Ἀχαιῶν χαλκοχιτώνων,
    Il. 3.128  οὕς ἑθεν εἵνεκʼ ἔπασχον ὑπʼ Ἄρηος παλαμάων·
<!-- PerseusDL canonical-greekLit, commit 01b725d8, tlg0012.tlg001 -->

Penelope's is introduced as a δόλος, plan and cloth being one object:

    Od. 2.93  ἡ δὲ δόλον τόνδʼ ἄλλον ἐνὶ φρεσὶ μερμήριξε·
    Od. 2.94  στησαμένη μέγαν ἱστὸν ἐνὶ μεγάροισιν ὕφαινε,
    Od. 2.95  λεπτὸν καὶ περίμετρον· ἄφαρ δʼ ἡμῖν μετέειπε·
    Od. 2.96  κοῦροι ἐμοὶ μνηστῆρες, ἐπεὶ θάνε δῖος Ὀδυσσεύς,
    Od. 2.97  μίμνετʼ ἐπειγόμενοι τὸν ἐμὸν γάμον, εἰς ὅ κε φᾶρος
    Od. 2.98  ἐκτελέσω, μή μοι μεταμώνια νήματʼ ὄληται,
    Od. 2.99  Λαέρτῃ ἥρωι ταφήιον, εἰς ὅτε κέν μιν
    Od. 2.100  μοῖρʼ ὀλοὴ καθέλῃσι τανηλεγέος θανάτοιο,
    Od. 2.101  μή τίς μοι κατὰ δῆμον Ἀχαιϊάδων νεμεσήσῃ.
    Od. 2.102  αἴ κεν ἄτερ σπείρου κεῖται πολλὰ κτεατίσσας.
    Od. 2.103  ὣς ἔφαθʼ, ἡμῖν δʼ αὖτʼ ἐπεπείθετο θυμὸς ἀγήνωρ.
    Od. 2.104  ἔνθα καὶ ἠματίη μὲν ὑφαίνεσκεν μέγαν ἱστόν,
    Od. 2.105  νύκτας δʼ ἀλλύεσκεν, ἐπεὶ δαΐδας παραθεῖτο.
    Od. 2.106  ὣς τρίετες μὲν ἔληθε δόλῳ καὶ ἔπειθεν Ἀχαιούς·
    Od. 2.107  ἀλλʼ ὅτε τέτρατον ἦλθεν ἔτος καὶ ἐπήλυθον ὧραι,
    Od. 2.108  καὶ τότε δή τις ἔειπε γυναικῶν, ἣ σάφα ᾔδη,
    Od. 2.109  καὶ τήν γʼ ἀλλύουσαν ἐφεύρομεν ἀγλαὸν ἱστόν.
    Od. 2.110  ὣς τὸ μὲν ἐξετέλεσσε καὶ οὐκ ἐθέλουσʼ ὑπʼ ἀνάγκης·
<!-- PerseusDL canonical-greekLit, commit 01b725d8, tlg0012.tlg002; the tellings at Od. 19.138–156 and 24.128–148 are quoted in full in paper/research/weaving_primary.md §1.4 -->

The block is told three times (Od. 2.93–110, 19.138–156, 24.128–148): 19 inflects the person (ὑφαίνεσκεν → ὑφαίνεσκον, ἔφαθʼ → ἐφάμην), 19 and 24 add a line (μηνῶν φθινόντων, περὶ δʼ ἤματα πόλλʼ ἐτελέσθη), and 24 adds a tail with the aorist:

    Od. 24.147  εὖθʼ ἡ φᾶρος ἔδειξεν, ὑφήνασα μέγαν ἱστόν,
    Od. 24.148  πλύνασʼ, ἠελίῳ ἐναλίγκιον ἠὲ σελήνῃ,
<!-- PerseusDL canonical-greekLit, commit 01b725d8, tlg0012.tlg002 -->

Here the etymology is secure. Beekes sets ὑφαίνω under IE *(h₁)u̯ebʰ- 'weave' (the Mycenaean form "may prove that the root was *h₁u̯ebʰ-") and takes the present, not as a denominative, but as "transformed from an older primary present, a nasal present (cf. the Skt. forms) or from a nominal form in *ubʰ-n- (thus LIV)" [Beekes 2010 s.v. ὑφαίνω, p. 1540, OCR]. LIV² gives *u̯ebʰ- 'umwickeln, weben' with a nasal present *u-né/n-bʰ- in Vedic unap, aumbhan 'binden, fesseln', ὑφαίνω 'webe' queried, OHG weban, and under ?*ubʰ-i̯é- Old Avestan ufiiā 'besinge' [LIV² 2001, p. 658, OCR]. Kroonen's *weban- 'to weave' (OE wefan) is "A strong verb with clear IE roots", with Tocharian AB wapa-, Skt. ubhnāti 'to bind, fetter', Oss. wafyn and Gr. ὑφαίνω < *h₁ubʰ-n-i̯e- as cognates (forms normalised from the OCR) [Kroonen 2013 s.v. *weban-, p. 576, OCR]. Mayrhofer's VABH 'binden, fesseln, bändigen' (ubdha- 'gefesselt') has YAv. ubdaēna- 'aus Webstoff bestehend', the Iranian verbs of weaving, and "hierher auch" Avestan vaf- (present uf-iia-) 'besingen, preisen', „*weben" der Lieder, with OAv. vafuš- 'Spruch' [Mayrhofer EWAia II s.v. VABH, p. 506, OCR]. Latin replaced the word: neither LIV nor Kroonen lists a Latin reflex, and de Vaan's texō 'to weave, construct' continues *teḱ-s- 'to fashion' beside Hittite taks- 'to devise, undertake', Skt. takṣati 'to hammer, form, fashion' and taṣṭar- 'carpenter', so that in Latin the weaving verb is the carpentry root [de Vaan 2008 s.v. texō, OCR].

The literature on poetry as weaving is cited by its verified records (`paper/research/references.md`), its arguments unread: Durante (1960, on "la terminologia relativa alla creazione poetica"; 1976, vol. II) and Schmitt (1967; §§ 608–609 per Chantraine; "Dichtung als Weben" [unverified]); West (2007, ch. 1, pp. 26–74); Tuck (2006), which derives Indo-European metrical poetry from patterned textiles, as its title says; Scheid and Svenbro (1996) on the weaving myths; Snyder (1981) on the "weaving imagery in Homer and the lyric poets" sampled next.

### 7.3 Pindar and Bacchylides

What Homer keeps for cloth and plans, the epinician poets say of the song, with the verbs of plaiting and weaving out:

    ματρομάτωρ ἐμὰ Στυμφαλίς, εὐανθὴς Μετώπα,
    85πλάξιππον ἃ Θήβαν ἔτικτεν, τᾶς ἐρατεινὸν ὕδωρ
    πίομαι, ἀνδράσιν αἰχματαῖσι πλέκων
    ποικίλον ὕμνον. ὄτρυνον νῦν ἑταίρους,
Pindar, Ol. 6.84–87
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0161:book=O.:poem=6 -->

    ἐξύφαινε, γλυκεῖα, καὶ τόδ᾽ αὐτίκα, φόρμιγξ,
    45Λυδίᾳ σὺν ἁρμονίᾳ μέλος πεφιλημένον
    Οἰνώνᾳ τε καὶ Κύπρῳ, ἔνθα Τεῦκρος ἀπάρχει
Pindar, Nem. 4.44–46
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0161:book=N.:poem=4 -->

    τὶν δὲ τούτων ἐξυφαίνονται χάριτες.
Pindar, Pyth. 4.275 (the ode also has ὑφαίνειν λοιπὸν ὄλβον; the fetched page has no ῥάπτ-)
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0161:book=P.:poem=4 -->

Pindar fr. 179, ὑφαίνω δ᾽ Ἀμυθαονίδαισιν ποικίλον ἄνδημα, is not on Perseus and rests on LSJ's "compose, write, ποικίλον ἄνδημα (metaph. of an ode) Pi.Fr.179" [text unverified]. Bacchylides has the plain verb with ὕμνος as object, and the imperative:

     ᾗ σὺν Χαρίτεσσι βαθυζώνοις ὑφάνας
     10ὕμνον ἀπὸ ζαθέας
     νάσου ξένος ὑμετέραν πέμ-
     πει κλεεννὰν ἐς πόλιν,
     χρυσάμπυκος Οὐρανίας κλει-
     νὸς θεράπων: ἐθέλει δὲ
Bacchylides 5.9–14 (Jebb 1905)
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0063:book=Ep:poem=5 -->

     ὕμνοισιν: ὕφαινέ νυν ἐν
     ταῖς πολυηράτοις τι κλεινὸν
     10ὀλβίαις Ἀθάναις,
     εὐαίνετε Κηϊα μέριμνα.
Bacchylides 19.8–11 (Perseus Dith. 19; Jebb's κλεινόν where Snell–Maehler are reported to print καινόν [unverified])
<!-- https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0063:book=Dith:poem=19 -->

The shift is of object, not of verb: ἱστόν and μῆτιν in Homer, ἀοιδήν in the Hesiodic lines, ὕμνον and μέλος here. Pindar has both figures and gives them to two genres, ῥαπτὰ ἔπη to the Homeridae and the ποικίλος hymn to himself: Beekes's epic line against strophe.

### 7.4 The Vedic parallels

The Rigveda has the same two figures and keeps them apart. Texts are from the GRETIL file of Aufrecht's edition (unaccented); no translation was fetched, and the glosses are the usual ones, from no entry consulted here [glosses unverified]. The first group stretches and weaves the sacrifice with threads (tantu) and weft (otu):

    RV_10,130.01a yo yajño viśvatas tantubhis tata ekaśataṃ devakarmebhir āyataḥ |
    RV_10,130.01c ime vayanti pitaro ya āyayuḥ pra vayāpa vayety āsate tate ||
    RV_10,130.02a pumāṃ enaṃ tanuta ut kṛṇatti pumān vi tatne adhi nāke asmin |
    RV_10,130.02c ime mayūkhā upa sedur ū sadaḥ sāmāni cakrus tasarāṇy otave ||
    RV_6,009.02a nāhaṃ tantuṃ na vi jānāmy otuṃ na yaṃ vayanti samare 'tamānāḥ |
    RV_6,009.02c kasya svit putra iha vaktvāni paro vadāty avareṇa pitrā ||
    RV_6,009.03a sa it tantuṃ sa vi jānāty otuṃ sa vaktvāny ṛtuthā vadāti |
    RV_6,009.03c ya īṃ ciketad amṛtasya gopā avaś caran paro anyena paśyan ||
    RV_10,053.06a tantuṃ tanvan rajaso bhānum anv ihi jyotiṣmataḥ patho rakṣa dhiyā kṛtān |
    RV_10,053.06c anulbaṇaṃ vayata joguvām apo manur bhava janayā daivyaṃ janam ||
    RV_2,003.06c tantuṃ tataṃ saṃvayantī samīcī yajñasya peśaḥ sudughe payasvatī ||
    RV_7,033.09c yamena tatam paridhiṃ vayanto 'psarasa upa sedur vasiṣṭhāḥ ||
    RV_1,061.08a asmā id u gnāś cid devapatnīr indrāyārkam ahihatya ūvuḥ |
<!-- https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/1_sam/1_rv/rvh1-10u.htm -->

In 6.9.2–3 the thread and the weft are what the son does not know and the father knows, the condition of speaking the vaktvāni in order; in 1.61.8 the gods' wives "wove" (ūvuḥ) the arka, a form the research file assigns to VABH [derivation unverified]. The second group is carpentry: the hymn (vāc, brahma, stoma) is fashioned (takṣ-) "like a chariot" (rathaṃ na) by a skilled man or a carpenter (taṣṭā):

    RV_1,130.06a imāṃ te vācaṃ vasūyanta āyavo rathaṃ na dhīraḥ svapā atakṣiṣuḥ sumnāya tvām atakṣiṣuḥ |
    RV_5,029.15c vastreva bhadrā sukṛtā vasūyū rathaṃ na dhīraḥ svapā atakṣam ||
    RV_1,062.13a sanāyate gotama indra navyam atakṣad brahma hariyojanāya |
    RV_1,061.04a asmā id u stomaṃ saṃ hinomi rathaṃ na taṣṭeva tatsināya |
<!-- same GRETIL file -->

and the hymn on the origin of speech adds a third figure, meal cleaned through a sieve:

    RV_10,071.01a bṛhaspate prathamaṃ vāco agraṃ yat prairata nāmadheyaṃ dadhānāḥ |
    RV_10,071.01c yad eṣāṃ śreṣṭhaṃ yad aripram āsīt preṇā tad eṣāṃ nihitaṃ guhāviḥ ||
    RV_10,071.02a saktum iva titaunā punanto yatra dhīrā manasā vācam akrata |
    RV_10,071.02c atrā sakhāyaḥ sakhyāni jānate bhadraiṣāṃ lakṣmīr nihitādhi vāci ||
    RV_10,071.03a yajñena vācaḥ padavīyam āyan tām anv avindann ṛṣiṣu praviṣṭām |
    RV_10,071.03c tām ābhṛtyā vy adadhuḥ purutrā tāṃ sapta rebhā abhi saṃ navante ||
    RV_10,071.04a uta tvaḥ paśyan na dadarśa vācam uta tvaḥ śṛṇvan na śṛṇoty enām |
    RV_10,071.04c uto tvasmai tanvaṃ vi sasre jāyeva patya uśatī suvāsāḥ ||
<!-- same GRETIL file -->

Greek splits the figures as Vedic does. Vedic takṣ- is, in de Vaan's entry, the cognate of Latin texō under *teḱ-s- [de Vaan 2008 s.v. texō, OCR]; that Greek τέκτων belongs there stands in no entry consulted here [unverified]. Homer's τέκτων (12 lines, `--regex "τέκτ(ων|ον)"`) is always a worker in wood or horn, τέκτονα δούρων (Od. 17.384), never a maker of words (`--loose "επεων τεκτ"`: 0); Pindar's ἐπέων ... τέκτονες (Pyth. 3.113), the match for the Vedic carpenter of hymns, was not fetched [unverified]. The weaving root reaches song in Iranian without a figure: Avestan vaf- 'besingen, preisen' is a plain verb of praising, placed by Mayrhofer under VABH and by LIV², with a query, under *u̯ebʰ- [Mayrhofer EWAia II s.v. VABH, p. 506; LIV² 2001, p. 658].

### 7.5 Stitching against weaving

The rhapsode literature is cited by its verified records only: Nagy's *Poetry as Performance* (1996) and *Plato's Rhapsody and Homer's Music* (2002), González (2013), Collins (2004, on the ἀγωνίζεσθαι of Hdt. 5.67) and Burkert's "Rhapsodes versus Stesichoros" (1987, pp. 43–62), whose title opposes the pair Pindar's usage keeps apart; how each reads ῥάπτειν is [unverified]. The texts support a narrower point. Stitching joins finished pieces edge to edge, as the hides of Il. 12.296; weaving makes the fabric on a frame, the ἱστός first set up (στησαμένη, Od. 2.94), and what is admired is the pattern, Helen's ἀέθλους and Pindar's ποικίλον. In Homer the two verbs share one figurative field, the plan and the harm, and neither reaches song; later Greek gave the two crafts to two kinds of poet.

Two witnesses stand outside Greek. Cynewulf closes the Elene with the figure:

    J)VS ic frod ond füs ]3urh J>aet faecne hus
    wordcraeft waef ond wundrum laes,
    Jirägum Jireodude ond getane reodode
Cynewulf, Elene 1236–1238 (Zupitza 1883, OCR as fetched); my reading: Þus ic frod ond fus þurh þæt fæcne hus / wordcræft wæf ond wundrum læs, / þragum þreodude ond geþanc reodode. Kent's glossary (1895) renders "wordcræft wæf, I wove skill of words" and notes "wæf, his own work; læs, his compilation from other sources".
<!-- https://archive.org/download/CynewulfsElene/ (file per https://archive.org/metadata/CynewulfsElene); https://archive.org/details/eleneanoldenglis00cyneuoft -->

Kent's gloss, whatever its merit, is the distinction this section needs: weaving is the poet's own making, gathering (læs) his taking from elsewhere. Horace gives not texere but the spinner's figure:

    cum lamentamur non apparere labores
    nostros et tenui deducta poemata filo;               225
Horace, Ep. 2.1.224–225
<!-- https://www.thelatinlibrary.com/horace/epist2.shtml -->

The poems are drawn out on a fine thread (deducta ... filo), the thread before the loom; texere carmen in Vergil and Ovid was not fetched [unverified].

### Connection to the composition records [to be completed after Phase 5]

The distinction will be tested on the poem of §5, whose records (`composition/final/poem.jsonl`) label every piece of every line ATTESTED-EXACT, ATTESTED-MODIFIED or COINAGE, with a concordance citation and, for modified pieces, a modification type. The attested pieces are the stitched units, ῥαπτὰ ἔπη; the modification types, inflection (ὑφαίνεσκεν → ὑφαίνεσκον), separation (μῆτιν ὑφαίνειν → ὑφαίνειν ἤρχετο μῆτιν), mobility (μῆτιν ὕφαινον at 9–12 against μῆτιν ὕφηνον at 3–5.5) and expansion (Od. 19.153 = 24.143), are the weaving operations. The count of each label and type, the share of COINAGE and the positions of modified pieces against their Homeric localisation will be read from the jsonl file when Phase 5 closes, by a script under `analysis/`, not by hand.
