# Primary passages for Phase 7: stitching (ῥάπτω / ῥαψῳδός), weaving (ὑφαίνω, *u̯ebʰ-), Pindar, Vedic, comparanda

All texts below were fetched on 2026-10-07 from the URL given at each item and are reproduced exactly as fetched (Unicode NFC). OCR-derived texts (archive.org scans) are quoted verbatim with their OCR errors; where I add a normalised reading it is marked "my reading". Homeric text is from the local copy of PerseusDL canonical-greekLit (Il.: Monro–Allen OCT; Od.: Murray 1919 Loeb) at commit 01b725d8 (see homer/source.json); all Homeric counts come from `python homer/concordance.py` run on 2026-10-07 (commands quoted). Editions: Pindar and Bacchylides on Perseus are the Perseus Greek texts (Bacchylides: Jebb, Cambridge 1905, as the page footer states); Plato is Burnet, OCT 1903 (page footer); the Rigveda is the GRETIL file of the Aufrecht text digitised by van Nooten and Holland, unaccented (file header quoted below).

## 1. Homer

### 1.1 ὑφαίνω and cognates: every line (local concordance)

Command: `python homer/concordance.py --loose "υφαιν" --format tsv` (23 hits). Four of the 23 are προ-φαίνω, not ὑφαίνω (Od. 9.143 προυφαίνετ᾽, 9.145 προύφαινε, 12.394 προύφαινον, 13.169 προὐφαίνετο); they are listed but struck out. Supplementary forms: `--loose "υφην"` (aorist ὑφην-), `--loose "υφαντ"` (ὑφαντός), `--loose "υφοω"` (ὑφόωσι).

```
citation	metrical_start	metrical_end	match	text
Il. 3.125	10	12	ὕφαιν	τὴν δʼ εὗρʼ ἐν μεγάρῳ· ἣ δὲ μέγαν ἱστὸν ὕφαινε
Il. 3.212	10	12	ὕφαιν	ἀλλʼ ὅτε δὴ μύθους καὶ μήδεα πᾶσιν ὕφαινον
Il. 6.187	10	12	ὕφαιν	τῷ δʼ ἄρʼ ἀνερχομένῳ πυκινὸν δόλον ἄλλον ὕφαινε·
Il. 6.456	10	12	ὑφαίν	καί κεν ἐν Ἄργει ἐοῦσα πρὸς ἄλλης ἱστὸν ὑφαίνοις,
Il. 7.324	6	8	ὑφαίν	τοῖς ὁ γέρων πάμπρωτος ὑφαίνειν ἤρχετο μῆτιν
Il. 9.93	6	8	ὑφαίν	τοῖς ὁ γέρων πάμπρωτος ὑφαίνειν ἤρχετο μῆτιν
Il. 22.440	4	5.5	ὕφαιν	ἀλλʼ ἥ γʼ ἱστὸν ὕφαινε μυχῷ δόμου ὑψηλοῖο
Od. 2.94	10	12	ὕφαιν	στησαμένη μέγαν ἱστὸν ἐνὶ μεγάροισιν ὕφαινε,
Od. 2.104	6	9	ὑφαίν	ἔνθα καὶ ἠματίη μὲν ὑφαίνεσκεν μέγαν ἱστόν,
Od. 4.678	10	12	ὕφαιν	αὐλῆς ἐκτὸς ἐών· οἱ δʼ ἔνδοθι μῆτιν ὕφαινον.
Od. 5.62	10	12	ὕφαιν	ἱστὸν ἐποιχομένη χρυσείῃ κερκίδʼ ὕφαινεν.
Od. 5.356	6	9	ὑφαίν	ὤ μοι ἐγώ, μή τίς μοι ὑφαίνῃσιν δόλον αὖτε
Od. 9.143	8	9.5	υφαίν	νύκτα διʼ ὀρφναίην, οὐδὲ προυφαίνετʼ ἰδέσθαι·
Od. 9.145	4	5.5	ύφαιν	οὐρανόθεν προύφαινε, κατείχετο δὲ νεφέεσσιν.
Od. 9.422	10	12	ὕφαιν	εὑροίμην· πάντας δὲ δόλους καὶ μῆτιν ὕφαινον
Od. 12.394	10	12	ύφαιν	τοῖσιν δʼ αὐτίκʼ ἔπειτα θεοὶ τέραα προύφαινον·
Od. 13.108	2	5	ὑφαίν	φάρεʼ ὑφαίνουσιν ἁλιπόρφυρα, θαῦμα ἰδέσθαι·
Od. 13.169	8	10	ὐφαίν	οἴκαδʼ ἐλαυνομένην; καὶ δὴ προὐφαίνετο πᾶσα.
Od. 15.517	10	12	ὑφαίν	φαίνεται, ἀλλʼ ἀπὸ τῶν ὑπερωΐῳ ἱστὸν ὑφαίνει.
Od. 19.139	10	12	ὑφαίν	στησαμένῃ μέγαν ἱστόν, ἐνὶ μεγάροισιν ὑφαίνειν,
Od. 19.149	6	9	ὑφαίν	ἔνθα καὶ ἠματίη μὲν ὑφαίνεσκον μέγαν ἱστόν,
Od. 24.129	10	12	ὕφαιν	στησαμένη μέγαν ἱστὸν ἐνὶ μεγάροισιν ὕφαινε,
Od. 24.139	6	9	ὑφαίν	ἔνθα καὶ ἠματίη μὲν ὑφαίνεσκεν μέγαν ἱστόν,
```
`--loose "υφην"`:
```
citation	metrical_start	metrical_end	match	text
Il. 6.19	2	5	ὑφην	ἔσκεν ὑφηνίοχος· τὼ δʼ ἄμφω γαῖαν ἐδύτην.
Il. 8.83	3.5	5	υφήν	ἄκρην κὰκ κορυφήν, ὅθι τε πρῶται τρίχες ἵππων
Od. 4.739	10	12	ὑφήν	εἰ δή πού τινα κεῖνος ἐνὶ φρεσὶ μῆτιν ὑφήνας
Od. 9.481	5.5	7	υφὴν	ἧκε δʼ ἀπορρήξας κορυφὴν ὄρεος μεγάλοιο,
Od. 10.113	5.5	7	υφήν	εὗρον, ὅσην τʼ ὄρεος κορυφήν, κατὰ δʼ ἔστυγον αὐτήν.
Od. 12.76	3.5	5	υφὴν	κείνου ἔχει κορυφὴν οὔτʼ ἐν θέρει οὔτʼ ἐν ὀπώρῃ.
Od. 13.303	10	12	ὑφήν	νῦν αὖ δεῦρʼ ἱκόμην, ἵνα τοι σὺν μῆτιν ὑφήνω
Od. 13.386	4	5.5	ὕφην	ἀλλʼ ἄγε μῆτιν ὕφηνον, ὅπως ἀποτίσομαι αὐτούς·
Od. 24.147	6	9	ὑφήν	εὖθʼ ἡ φᾶρος ἔδειξεν, ὑφήνασα μέγαν ἱστόν,
```
`--loose "υφαντ"`:
```
citation	metrical_start	metrical_end	match	text
Od. 13.136	10	12	ὑφαντ	χαλκόν τε χρυσόν τε ἅλις ἐσθῆτά θʼ ὑφαντήν,
Od. 13.218	6	7.5	ὑφαντ	ἠρίθμει καὶ χρυσὸν ὑφαντά τε εἵματα καλά.
Od. 16.231	10	12	ὑφαντ	χαλκόν τε χρυσόν τε ἅλις ἐσθῆτά θʼ ὑφαντήν.
```
`--loose "υφοω"`:
```
citation	metrical_start	metrical_end	match	text
Il. 11.156	3	5	υφόω	πάντῃ τʼ εἰλυφόων ἄνεμος φέρει, οἳ δέ τε θάμνοι
Od. 7.105	3.5	5.5	ὑφόω	αἱ δʼ ἱστοὺς ὑφόωσι καὶ ἠλάκατα στρωφῶσιν
```
`--loose "υφασμ"`:
```
citation	metrical_start	metrical_end	match	text
Od. 3.274	6	8	ὑφάσμ	πολλὰ δʼ ἀγάλματʼ ἀνῆψεν, ὑφάσματά τε χρυσόν τε,
```

Summary (from the outputs above): ὑφαίνω present/imperfect stem 19 lines (23 hits minus 4 προφαίνω); aorist ὑφην- 4 (Od. 4.739, 13.303, 13.386, 24.147); ὑφαντ- 3 (Od. 13.136, 13.218, 16.231); ὑφόωσι 1 (Od. 7.105; the other `υφοω` hit, Il. 11.156 εἰλυφόων, is εἰλυφάω); ὕφασμα 1 (Od. 3.274 ὑφάσματά τε). The idiom ἱστὸν ὑφαίνειν (`--loose "ιστον υφαιν"`: 4 lines) is the literal use; the metaphorical object is μῆτις (Il. 7.324 = 9.93; Od. 4.678, 4.739, 9.422, 13.303, 13.386), δόλος (Il. 6.187; Od. 5.356), μῦθοι καὶ μήδεα (Il. 3.212).

### 1.2 μῆτιν ὑφαίνειν / δόλον ὑφαίνειν (full lines)

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

### 1.3 Helen's web, Il. 3.125–128

    Il. 3.125  τὴν δʼ εὗρʼ ἐν μεγάρῳ· ἣ δὲ μέγαν ἱστὸν ὕφαινε
    Il. 3.126  δίπλακα πορφυρέην, πολέας δʼ ἐνέπασσεν ἀέθλους
    Il. 3.127  Τρώων θʼ ἱπποδάμων καὶ Ἀχαιῶν χαλκοχιτώνων,
    Il. 3.128  οὕς ἑθεν εἵνεκʼ ἔπασχον ὑπʼ Ἄρηος παλαμάων·

### 1.4 Penelope's web: Od. 2.93–110, 19.138–156, 24.128–148 (the three tellings)

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

    Od. 19.138  φᾶρος μέν μοι πρῶτον ἐνέπνευσε φρεσὶ δαίμων,
    Od. 19.139  στησαμένῃ μέγαν ἱστόν, ἐνὶ μεγάροισιν ὑφαίνειν,
    Od. 19.140  λεπτὸν καὶ περίμετρον· ἄφαρ δʼ αὐτοῖς μετέειπον·
    Od. 19.141  κοῦροι, ἐμοὶ μνηστῆρες, ἐπεὶ θάνε δῖος Ὀδυσσεύς,
    Od. 19.142  μίμνετʼ ἐπειγόμενοι τὸν ἐμὸν γάμον, εἰς ὅ κε φᾶρος
    Od. 19.143  ἐκτελέσω—μή μοι μεταμώνια νήματʼ ὄληται—
    Od. 19.144  Λαέρτῃ ἥρωϊ ταφήϊον, εἰς ὅτε κέν μιν
    Od. 19.145  μοῖρʼ ὀλοὴ καθέλῃσι τανηλεγέος θανάτοιο·
    Od. 19.146  μή τίς μοι κατὰ δῆμον Ἀχαιϊάδων νεμεσήσῃ,
    Od. 19.147  αἴ κεν ἄτερ σπείρου κεῖται πολλὰ κτεατίσσας.
    Od. 19.148  ὣς ἐφάμην, τοῖσιν δʼ ἐπεπείθετο θυμὸς ἀγήνωρ.
    Od. 19.149  ἔνθα καὶ ἠματίη μὲν ὑφαίνεσκον μέγαν ἱστόν,
    Od. 19.150  νύκτας δʼ ἀλλύεσκον, ἐπεὶ δαΐδας παραθείμην.
    Od. 19.151  ὣς τρίετες μὲν ἔληθον ἐγὼ καὶ ἔπειθον Ἀχαιούς·
    Od. 19.152  ἀλλʼ ὅτε τέτρατον ἦλθεν ἔτος καὶ ἐπήλυθον ὧραι,
    Od. 19.153  μηνῶν φθινόντων, περὶ δʼ ἤματα πόλλʼ ἐτελέσθη,
    Od. 19.154  καὶ τότε δή με διὰ δμῳάς, κύνας οὐκ ἀλεγούσας,
    Od. 19.155  εἷλον ἐπελθόντες καὶ ὁμόκλησαν ἐπέεσσιν.
    Od. 19.156  ὣς τὸ μὲν ἐξετέλεσσα, καὶ οὐκ ἐθέλουσʼ, ὑπʼ ἀνάγκης·

    Od. 24.128  ἀλλὰ δόλον τόνδʼ ἄλλον ἐνὶ φρεσὶ μερμήριξε·
    Od. 24.129  στησαμένη μέγαν ἱστὸν ἐνὶ μεγάροισιν ὕφαινε,
    Od. 24.130  λεπτὸν καὶ περίμετρον· ἄφαρ δʼ ἡμῖν μετέειπε·
    Od. 24.131  κοῦροι ἐμοὶ μνηστῆρες, ἐπεὶ θάνε δῖος Ὀδυσσεύς,
    Od. 24.132  μίμνετʼ ἐπειγόμενοι τὸν ἐμὸν γάμον, εἰς ὅ κε φᾶρος
    Od. 24.133  ἐκτελέσω, μή μοι μεταμώνια νήματʼ ὄληται,
    Od. 24.134  Λαέρτῃ ἥρωϊ ταφήϊον, εἰς ὅτε κέν μιν
    Od. 24.135  μοῖρʼ ὀλοὴ καθέλῃσι τανηλεγέος θανάτοιο,
    Od. 24.136  μή τίς μοι κατὰ δῆμον Ἀχαιϊάδων νεμεσήσῃ,
    Od. 24.137  αἴ κεν ἄτερ σπείρου κεῖται πολλὰ κτεατίσσας.
    Od. 24.138  ὣς ἔφαθʼ, ἡμῖν δʼ αὖτʼ ἐπεπείθετο θυμὸς ἀγήνωρ.
    Od. 24.139  ἔνθα καὶ ἠματίη μὲν ὑφαίνεσκεν μέγαν ἱστόν,
    Od. 24.140  νύκτας δʼ ἀλλύεσκεν, ἐπεὶ δαΐδας παραθεῖτο.
    Od. 24.141  ὣς τρίετες μὲν ἔληθε δόλῳ καὶ ἔπειθεν Ἀχαιούς·
    Od. 24.142  ἀλλʼ ὅτε τέτρατον ἦλθεν ἔτος καὶ ἐπήλυθον ὧραι,
    Od. 24.143  μηνῶν φθινόντων, περὶ δʼ ἤματα πόλλʼ ἐτελέσθη,
    Od. 24.144  καὶ τότε δή τις ἔειπε γυναικῶν, ἣ σάφα ᾔδη,
    Od. 24.145  καὶ τήν γʼ ἀλλύουσαν ἐφεύρομεν ἀγλαὸν ἱστόν.
    Od. 24.146  ὣς τὸ μὲν ἐξετέλεσσε καὶ οὐκ ἐθέλουσʼ, ὑπʼ ἀνάγκης.
    Od. 24.147  εὖθʼ ἡ φᾶρος ἔδειξεν, ὑφήνασα μέγαν ἱστόν,
    Od. 24.148  πλύνασʼ, ἠελίῳ ἐναλίγκιον ἠὲ σελήνῃ,

### 1.5 ῥάπτω in Homer

Command: `python homer/concordance.py --loose "ραπτ" --format tsv` (14 hits) and `--loose "ραψ"` (10 hits). Most hits are other words (ἀστράπτω, ἐπιτέτραπται, τέτραπτο, γράφω). The genuine ῥάπτω forms are: Il. 12.296 ῥάψε (literal: stitching hides), Il. 18.367 ῥάψαι, Od. 3.118 ῥάπτομεν, Od. 16.379 ἐράπτομεν, Od. 16.422 ῥάπτεις, Od. 16.423 ῥάπτειν (all metaphorical, κακὰ / φόνον / θάνατον ῥάπτειν), and the adjective ῥαπτός Od. 24.228, 24.229. No ῥαψῳδ- and no ῥάψαντες ἀοιδήν in Homer (`--loose "ραψωδ"` returns 0).

    Il. 12.296  ἤλασεν, ἔντοσθεν δὲ βοείας ῥάψε θαμειὰς
    Il. 18.367  οὐκ ὄφελον Τρώεσσι κοτεσσαμένη κακὰ ῥάψαι;
    Od. 3.118  εἰνάετες γάρ σφιν κακὰ ῥάπτομεν ἀμφιέποντες
    Od. 16.379  οὕνεκά οἱ φόνον αἰπὺν ἐράπτομεν οὐδʼ ἐκίχημεν·
    Od. 16.421  μάργε, τίη δὲ σὺ Τηλεμάχῳ θάνατόν τε μόρον τε
    Od. 16.422  ῥάπτεις, οὐδʼ ἱκέτας ἐμπάζεαι, οἷσιν ἄρα Ζεὺς
    Od. 16.423  μάρτυρος; οὐδʼ ὁσίη κακὰ ῥάπτειν ἀλλήλοισιν.
    Od. 24.228  ῥαπτὸν ἀεικέλιον, περὶ δὲ κνήμῃσι βοείας
    Od. 24.229  κνημῖδας ῥαπτὰς δέδετο, γραπτῦς ἀλεείνων,

```
`--loose "ραψωδ" --count` -> 0
`--loose "ραπτ" --count` -> 14
`--loose "ραψ" --count` -> 10
```

### 1.6 ἀοιδός / ἀοιδή / ὕμνος counts

Whole-word, accent-insensitive counts (`python homer/concordance.py --loose FORM --word --count`):
```
αοιδος	19
αοιδου	4
αοιδον	11
αοιδοι	3
αοιδων	1
αοιδους	1
αοιδη	6
αοιδης	5
αοιδην	13
υμνος	0
υμνον	1
αυτοδιδακτος	1
regex ἀοιδ (any form), Il.	6
regex ἀοιδ (any form), Od.	59
```
Sums: ἀοιδός (nom./gen./acc./nom.pl./gen.pl./acc.pl.) 19+4+11+3+1+1 = 39 lines; ἀοιδή (ἀοιδή/-ῇ, -ῆς, -ήν) 6+5+13 = 24 lines; ὕμνος once (Od. 8.429 ἀοιδῆς ὕμνον). The Iliad has only 6 ἀοιδ- lines (2.595, 2.599, 13.731, 18.604, 24.720, 24.721), the Odyssey 59.

### 1.7 Phemius, Od. 1.325–359

    Od. 1.325  τοῖσι δʼ ἀοιδὸς ἄειδε περικλυτός, οἱ δὲ σιωπῇ
    Od. 1.326  ἥατʼ ἀκούοντες· ὁ δʼ Ἀχαιῶν νόστον ἄειδε
    Od. 1.327  λυγρόν, ὃν ἐκ Τροίης ἐπετείλατο Παλλὰς Ἀθήνη.
    Od. 1.328  τοῦ δʼ ὑπερωιόθεν φρεσὶ σύνθετο θέσπιν ἀοιδὴν
    Od. 1.329  κούρη Ἰκαρίοιο, περίφρων Πηνελόπεια·
    Od. 1.330  κλίμακα δʼ ὑψηλὴν κατεβήσετο οἷο δόμοιο,
    Od. 1.331  οὐκ οἴη, ἅμα τῇ γε καὶ ἀμφίπολοι δύʼ ἕποντο.
    Od. 1.332  ἡ δʼ ὅτε δὴ μνηστῆρας ἀφίκετο δῖα γυναικῶν,
    Od. 1.333  στῆ ῥα παρὰ σταθμὸν τέγεος πύκα ποιητοῖο,
    Od. 1.334  ἄντα παρειάων σχομένη λιπαρὰ κρήδεμνα·
    Od. 1.335  ἀμφίπολος δʼ ἄρα οἱ κεδνὴ ἑκάτερθε παρέστη.
    Od. 1.336  δακρύσασα δʼ ἔπειτα προσηύδα θεῖον ἀοιδόν·
    Od. 1.337  Φήμιε, πολλὰ γὰρ ἄλλα βροτῶν θελκτήρια οἶδας,
    Od. 1.338  ἔργʼ ἀνδρῶν τε θεῶν τε, τά τε κλείουσιν ἀοιδοί·
    Od. 1.339  τῶν ἕν γέ σφιν ἄειδε παρήμενος, οἱ δὲ σιωπῇ
    Od. 1.340  οἶνον πινόντων· ταύτης δʼ ἀποπαύεʼ ἀοιδῆς
    Od. 1.341  λυγρῆς, ἥ τέ μοι αἰεὶ ἐνὶ στήθεσσι φίλον κῆρ
    Od. 1.342  τείρει, ἐπεί με μάλιστα καθίκετο πένθος ἄλαστον.
    Od. 1.343  τοίην γὰρ κεφαλὴν ποθέω μεμνημένη αἰεί,
    Od. 1.344  ἀνδρός, τοῦ κλέος εὐρὺ καθʼ Ἑλλάδα καὶ μέσον Ἄργος.
    Od. 1.345  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·
    Od. 1.346  μῆτερ ἐμή, τί τʼ ἄρα φθονέεις ἐρίηρον ἀοιδὸν
    Od. 1.347  τέρπειν ὅππῃ οἱ νόος ὄρνυται; οὔ νύ τʼ ἀοιδοὶ
    Od. 1.348  αἴτιοι, ἀλλά ποθι Ζεὺς αἴτιος, ὅς τε δίδωσιν
    Od. 1.349  ἀνδράσιν ἀλφηστῇσιν, ὅπως ἐθέλῃσιν, ἑκάστῳ.
    Od. 1.350  τούτῳ δʼ οὐ νέμεσις Δαναῶν κακὸν οἶτον ἀείδειν·
    Od. 1.351  τὴν γὰρ ἀοιδὴν μᾶλλον ἐπικλείουσʼ ἄνθρωποι,
    Od. 1.352  ἥ τις ἀκουόντεσσι νεωτάτη ἀμφιπέληται.
    Od. 1.353  σοὶ δʼ ἐπιτολμάτω κραδίη καὶ θυμὸς ἀκούειν·
    Od. 1.354  οὐ γὰρ Ὀδυσσεὺς οἶος ἀπώλεσε νόστιμον ἦμαρ
    Od. 1.355  ἐν Τροίῃ, πολλοὶ δὲ καὶ ἄλλοι φῶτες ὄλοντο.
    Od. 1.356  ἀλλʼ εἰς οἶκον ἰοῦσα τὰ σʼ αὐτῆς ἔργα κόμιζε,
    Od. 1.357  ἱστόν τʼ ἠλακάτην τε, καὶ ἀμφιπόλοισι κέλευε
    Od. 1.358  ἔργον ἐποίχεσθαι· μῦθος δʼ ἄνδρεσσι μελήσει
    Od. 1.359  πᾶσι, μάλιστα δʼ ἐμοί· τοῦ γὰρ κράτος ἔστʼ ἐνὶ οἴκῳ.

### 1.8 Demodocus, Od. 8.62–82; and 8.479–481, 8.487–491

    Od. 8.62  κῆρυξ δʼ ἐγγύθεν ἦλθεν ἄγων ἐρίηρον ἀοιδόν,
    Od. 8.63  τὸν πέρι μοῦσʼ ἐφίλησε, δίδου δʼ ἀγαθόν τε κακόν τε·
    Od. 8.64  ὀφθαλμῶν μὲν ἄμερσε, δίδου δʼ ἡδεῖαν ἀοιδήν.
    Od. 8.65  τῷ δʼ ἄρα Ποντόνοος θῆκε θρόνον ἀργυρόηλον
    Od. 8.66  μέσσῳ δαιτυμόνων, πρὸς κίονα μακρὸν ἐρείσας·
    Od. 8.67  κὰδ δʼ ἐκ πασσαλόφι κρέμασεν φόρμιγγα λίγειαν
    Od. 8.68  αὐτοῦ ὑπὲρ κεφαλῆς καὶ ἐπέφραδε χερσὶν ἑλέσθαι
    Od. 8.69  κῆρυξ· πὰρ δʼ ἐτίθει κάνεον καλήν τε τράπεζαν,
    Od. 8.70  πὰρ δὲ δέπας οἴνοιο, πιεῖν ὅτε θυμὸς ἀνώγοι.
    Od. 8.71  οἱ δʼ ἐπʼ ὀνείαθʼ ἑτοῖμα προκείμενα χεῖρας ἴαλλον.
    Od. 8.72  αὐτὰρ ἐπεὶ πόσιος καὶ ἐδητύος ἐξ ἔρον ἕντο,
    Od. 8.73  μοῦσʼ ἄρʼ ἀοιδὸν ἀνῆκεν ἀειδέμεναι κλέα ἀνδρῶν,
    Od. 8.74  οἴμης τῆς τότʼ ἄρα κλέος οὐρανὸν εὐρὺν ἵκανε,
    Od. 8.75  νεῖκος Ὀδυσσῆος καὶ Πηλεΐδεω Ἀχιλῆος,
    Od. 8.76  ὥς ποτε δηρίσαντο θεῶν ἐν δαιτὶ θαλείῃ
    Od. 8.77  ἐκπάγλοις ἐπέεσσιν, ἄναξ δʼ ἀνδρῶν Ἀγαμέμνων
    Od. 8.78  χαῖρε νόῳ, ὅ τʼ ἄριστοι Ἀχαιῶν δηριόωντο.
    Od. 8.79  ὣς γάρ οἱ χρείων μυθήσατο Φοῖβος Ἀπόλλων
    Od. 8.80  Πυθοῖ ἐν ἠγαθέῃ, ὅθʼ ὑπέρβη λάινον οὐδὸν
    Od. 8.81  χρησόμενος· τότε γάρ ῥα κυλίνδετο πήματος ἀρχὴ
    Od. 8.82  Τρωσί τε καὶ Δαναοῖσι Διὸς μεγάλου διὰ βουλάς.

    Od. 8.479  πᾶσι γὰρ ἀνθρώποισιν ἐπιχθονίοισιν ἀοιδοὶ
    Od. 8.480  τιμῆς ἔμμοροί εἰσι καὶ αἰδοῦς, οὕνεκʼ ἄρα σφέας
    Od. 8.481  οἴμας μοῦσʼ ἐδίδαξε, φίλησε δὲ φῦλον ἀοιδῶν.

    Od. 8.487  Δημόδοκʼ, ἔξοχα δή σε βροτῶν αἰνίζομʼ ἁπάντων.
    Od. 8.488  ἢ σέ γε μοῦσʼ ἐδίδαξε, Διὸς πάϊς, ἢ σέ γʼ Ἀπόλλων·
    Od. 8.489  λίην γὰρ κατὰ κόσμον Ἀχαιῶν οἶτον ἀείδεις,
    Od. 8.490  ὅσσʼ ἔρξαν τʼ ἔπαθόν τε καὶ ὅσσʼ ἐμόγησαν Ἀχαιοί,
    Od. 8.491  ὥς τέ που ἢ αὐτὸς παρεὼν ἢ ἄλλου ἀκούσας.

### 1.9 Phemius αὐτοδίδακτος, Od. 22.344–353

    Od. 22.344  γουνοῦμαί σʼ, Ὀδυσεῦ· σὺ δέ μʼ αἴδεο καί μʼ ἐλέησον·
    Od. 22.345  αὐτῷ τοι μετόπισθʼ ἄχος ἔσσεται, εἴ κεν ἀοιδὸν
    Od. 22.346  πέφνῃς, ὅς τε θεοῖσι καὶ ἀνθρώποισιν ἀείδω.
    Od. 22.347  αὐτοδίδακτος δʼ εἰμί, θεὸς δέ μοι ἐν φρεσὶν οἴμας
    Od. 22.348  παντοίας ἐνέφυσεν· ἔοικα δέ τοι παραείδειν
    Od. 22.349  ὥς τε θεῷ· τῷ μή με λιλαίεο δειροτομῆσαι.
    Od. 22.350  καί κεν Τηλέμαχος τάδε γʼ εἴποι, σὸς φίλος υἱός,
    Od. 22.351  ὡς ἐγὼ οὔ τι ἑκὼν ἐς σὸν δόμον οὐδὲ χατίζων
    Od. 22.352  πωλεύμην μνηστῆρσιν ἀεισόμενος μετὰ δαῖτας,
    Od. 22.353  ἀλλὰ πολὺ πλέονες καὶ κρείσσονες ἦγον ἀνάγκῃ.

### 1.10 Achilles sings κλέα ἀνδρῶν, Il. 9.186–191 (cf. Od. 8.73)

    Il. 9.186  τὸν δʼ εὗρον φρένα τερπόμενον φόρμιγγι λιγείῃ
    Il. 9.187  καλῇ δαιδαλέῃ, ἐπὶ δʼ ἀργύρεον ζυγὸν ἦεν,
    Il. 9.188  τὴν ἄρετʼ ἐξ ἐνάρων πόλιν Ἠετίωνος ὀλέσσας·
    Il. 9.189  τῇ ὅ γε θυμὸν ἔτερπεν, ἄειδε δʼ ἄρα κλέα ἀνδρῶν.
    Il. 9.190  Πάτροκλος δέ οἱ οἶος ἐναντίος ἧστο σιωπῇ,
    Il. 9.191  δέγμενος Αἰακίδην ὁπότε λήξειεν ἀείδων,

`--loose "κλεα ανδρων" --count` -> 3 (Il. 9.189, 9.524, Od. 8.73).

### 1.11 Od. 17.518–521 (the ἀοιδός simile) and Od. 8.429 (ὕμνος)

    Od. 17.518  ὡς δʼ ὅτʼ ἀοιδὸν ἀνὴρ ποτιδέρκεται, ὅς τε θεῶν ἒξ
    Od. 17.519  ἀείδει δεδαὼς ἔπεʼ ἱμερόεντα βροτοῖσι,
    Od. 17.520  τοῦ δʼ ἄμοτον μεμάασιν ἀκουέμεν, ὁππότʼ ἀείδῃ·
    Od. 17.521  ὣς ἐμὲ κεῖνος ἔθελγε παρήμενος ἐν μεγάροισι.
    Od. 8.429  δαιτί τε τέρπηται καὶ ἀοιδῆς ὕμνον ἀκούων.

## 2. Hesiod fr. 357 Merkelbach–West (= fr. 265 Rzach = Evelyn-White, Fragmenta dubia 3)

Source fetched: Hugh G. Evelyn-White, Hesiod, the Homeric Hymns and Homerica (Loeb, 1914), archive.org item hesiodhomerichym0000hesi_d6n3, file hesiodhomerichym0000hesi_d6n3_djvu.txt (OCR), URL https://archive.org/download/hesiodhomerichym0000hesi_d6n3/hesiodhomerichym0000hesi_d6n3_djvu.txt (metadata: "Cambridge, Mass. : Harvard University Press", 1914). The couplet stands under the heading FRAGMENTA DUBIA, item 3, source line "Schol. on Pindar, Nem. ii. 1.". OCR as fetched:
```
ἀλετρεύουσι μύλης ἔπι μήλοπα καρπόν. 
3. 
Schol. on Pindar, Nem. ii. 1. 

ἐν Δήλῳ τότε πρῶτον ἐγὼ καὶ “Ὅμηρος ἀοιδοὶ 

μέλπομεν, ἐν νεαροῖς ὕμνοις ῥάψαντες ἀοιδήν, 

Φοῖβον ᾿Απόλλωνα χρυσάορον, ὃν τέκε Λητώ. 

```
My reading (removing the stray OCR quotation mark and the OCR apostrophe used for the breathing): ἐν Δήλῳ τότε πρῶτον ἐγὼ καὶ Ὅμηρος ἀοιδοὶ / μέλπομεν, ἐν νεαροῖς ὕμνοις ῥάψαντες ἀοιδήν, / Φοῖβον Ἀπόλλωνα χρυσάορον, ὃν τέκε Λητώ.

Numbering check: the Chantraine DELG entry ῥαψῳδός (archive.org OCR, see §5.4) reads "Hés. fr. 265 = 357 Merkelbach-West"; LSJ s.v. ῥάπτω II.2 and s.v. ῥαψῳδός cite "Hes.Fr.265" (§5.1). The Loeb of Most (2007) was not fetched [unverified for its own numbering].

## 3. Pindar and Bacchylides (Perseus Digital Library, Greek text pages)

### 3.1 Pindar, Nemean 2.1–5
URL: https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0161:book=N.:poem=2
```
ὅθεν περ καὶ Ὁμηρίδαι
ῥαπτῶν ἐπέων τὰ πόλλ᾽ ἀοιδοὶ
ἄρχονται, Διὸς ἐκ προοιμίου: καὶ ὅδ᾽ ἀνὴρ
καταβολὰν ἱερῶν ἀγώνων νικαφορίας δέδεκται πρῶτον Νεμεαίου
5ἐν πολυυμνήτῳ Διὸς ἄλσει.
```
### 3.2 Pindar, Olympian 6.84–87 (πλέκων ποικίλον ὕμνον)
URL: https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0161:book=O.:poem=6
```
ματρομάτωρ ἐμὰ Στυμφαλίς, εὐανθὴς Μετώπα,
85πλάξιππον ἃ Θήβαν ἔτικτεν, τᾶς ἐρατεινὸν ὕδωρ
πίομαι, ἀνδράσιν αἰχματαῖσι πλέκων
ποικίλον ὕμνον. ὄτρυνον νῦν ἑταίρους,
```
### 3.3 Pindar, Nemean 4.44–46 (ἐξύφαινε ... μέλος)
URL: https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0161:book=N.:poem=4
```
 εὖ οἶδ᾽ ὅτι χρόνος ἕρπων πεπρωμέναν τελέσει.
ἐξύφαινε, γλυκεῖα, καὶ τόδ᾽ αὐτίκα, φόρμιγξ,
45Λυδίᾳ σὺν ἁρμονίᾳ μέλος πεφιλημένον
Οἰνώνᾳ τε καὶ Κύπρῳ, ἔνθα Τεῦκρος ἀπάρχει
ὁ Τελαμωνιάδας: ἀτὰρ
```
### 3.4 Pindar, Pythian 4.272–275: no ῥάπτειν; the verb is ἐξυφαίνονται (275)
URL: https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0161:book=P.:poem=4 . `grep ῥάπτ` on the fetched page: no hit. Lines as fetched (Perseus prints the line number 275 after the line it labels):
```
ῥᾴδιον μὲν γὰρ πόλιν σεῖσαι καὶ ἀφαυροτέροις:
ἀλλ᾽ ἐπὶ χώρας αὖτις ἕσσαι δυσπαλὲς δὴ γίγνεται, ἐξαπίνας
εἰ μὴ θεὸς ἁγεμόνεσσι κυβερνατὴρ γένηται.
275
 [490]
 τὶν δὲ τούτων ἐξυφαίνονται χάριτες.
τλᾶθι τᾶς εὐδαίμονος ἀμφὶ Κυράνας θέμεν σπουδὰν ἅπασαν.
τῶν δ᾽ Ὁμήρου καὶ τόδε συνθέμενος
```
Other ὑφαίν- in Pythian 4 as fetched (grep):
```
ἀλλ᾽ ἐμὲ χρὴ καὶ σὲ θεμισσαμένους ὀργὰς ὑφαίνειν λοιπὸν ὄλβον.
 τὶν δὲ τούτων ἐξυφαίνονται χάριτες.
```
Pindar fr. 179 (ὑφαίνω δ᾽ Ἀμυθαονίδαισιν ποικίλον ἄνδημα): not on Perseus (the Perseus Pindar has the four books of epinicians only). Attested second-hand in LSJ s.v. ὑφαίνω III.2: "compose, write, ποικίλον ἄνδημα (metaph. of an ode) Pi.Fr.179" (§5.1). Text itself [unverified].

### 3.5 Bacchylides 5.9–14 (ὑφάνας ὕμνον)
URL: https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0063:book=Ep:poem=5 (footer: "Bacchylides. The Poems and Fragments. Cambridge University Press. 1905.")
```
 ὀρθῶς: φρένα δ᾽ εὐθύδικον
 ἀτρέμ᾽ ἀμπαύσας μεριμνᾶν
 δεῦρ᾽ ἐπάθρησον νόῳ,
 ᾗ σὺν Χαρίτεσσι βαθυζώνοις ὑφάνας
 10ὕμνον ἀπὸ ζαθέας
 νάσου ξένος ὑμετέραν πέμ-
 πει κλεεννὰν ἐς πόλιν,
 χρυσάμπυκος Οὐρανίας κλει-
 νὸς θεράπων: ἐθέλει δὲ
```
### 3.6 Bacchylides 19.5–11 (ὕφαινέ νυν ...); Perseus numbers it Dith. 19
URL: https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0063:book=Dith:poem=19 . Note the Perseus (Jebb) text reads τι κλεινόν where Snell–Maehler print τι καινόν [the Snell–Maehler reading is unverified here].
```
 5ἰοβλέφαροί τε καὶ
 φερεστέφανοι Χάριτες
 βάλωσιν ἄμφι τιμὰν
 ὕμνοισιν: ὕφαινέ νυν ἐν
 ταῖς πολυηράτοις τι κλεινὸν
 10ὀλβίαις Ἀθάναις,
 εὐαίνετε Κηϊα μέριμνα.
 πρέπει σε φερτάταν ἴμεν
```

## 4. Plato, Herodotus, Homeric Hymn to Apollo (Perseus)

### 4.1 Plato, Ion (Burnet 1903), URLs https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0179:text=Ion:section=530b (and =530c, 530d, 531a, 533d, 534b, 535e, 536a)
```
530b: καὶ μὴν πολλάκις γε ἐζήλωσα ὑμᾶς τοὺς ῥαψῳδούς, ὦ Ἴων, τῆς τέχνης: τὸ γὰρ ἅμα μὲν τὸ σῶμα κεκοσμῆσθαι ἀεὶ πρέπον ὑμῶν εἶναι τῇ τέχνῃ καὶ ὡς καλλίστοις φαίνεσθαι, ἅμα δὲ ἀναγκαῖον εἶναι ἔν τε ἄλλοις ποιηταῖς διατρίβειν πολλοῖς καὶ ἀγαθοῖς καὶ δὴ καὶ μάλιστα ἐν Ὁμήρῳ, τῷ ἀρίστῳ καὶ θειοτάτῳ τῶν ποιητῶν, καὶ τὴν τούτου διάνοιαν
530c: οὐ γὰρ ἂν γένοιτό ποτε ἀγαθὸς ῥαψῳδός, εἰ μὴ συνείη τὰ λεγόμενα ὑπὸ τοῦ ποιητοῦ. τὸν γὰρ ῥαψῳδὸν ἑρμηνέα δεῖ τοῦ ποιητοῦ τῆς διανοίας γίγνεσθαι τοῖς ἀκούουσι
530d: καὶ μὴν ἄξιόν γε ἀκοῦσαι, ὦ Σώκρατες, ὡς εὖ κεκόσμηκα τὸν Ὅμηρον: ὥστε οἶμαι ὑπὸ Ὁμηριδῶν ἄξιος εἶναι χρυσῷ στεφάνῳ στεφανωθῆναι
531a: πότερον περὶ Ὁμήρου μόνον δεινὸς εἶ ἢ καὶ περὶ Ἡσιόδου καὶ Ἀρχιλόχου;
533d: ἔστι γὰρ τοῦτο τέχνη μὲν οὐκ ὂν παρὰ σοὶ περὶ Ὁμήρου εὖ λέγειν, ὃ νυνδὴ ἔλεγον, θεία δὲ δύναμις ἥ σε κινεῖ, ὥσπερ ἐν τῇ λίθῳ ἣν Εὐριπίδης μὲν Μαγνῆτιν ὠνόμασεν, οἱ δὲ πολλοὶ Ἡρακλείαν.
534b: κοῦφον γὰρ χρῆμα ποιητής ἐστιν καὶ πτηνὸν καὶ ἱερόν, καὶ οὐ πρότερον οἷός τε ποιεῖν πρὶν ἂν ἔνθεός τε γένηται καὶ ἔκφρων καὶ ὁ νοῦς μηκέτι ἐν αὐτῷ ἐνῇ
535e–536a: οἶσθα οὖν ὅτι οὗτός ἐστιν ὁ θεατὴς τῶν δακτυλίων ὁ ἔσχατος, ὧν ἐγὼ ἔλεγον ὑπὸ τῆς Ἡρακλειώτιδος λίθου ἀπ᾽ ἀλλήλων τὴν δύναμιν λαμβάνειν; ὁ δὲ μέσος σὺ ὁ | ῥαψῳδὸς καὶ ὑποκριτής, ὁ δὲ πρῶτος αὐτὸς ὁ ποιητής
```
### 4.2 Plato, Republic 10.600d
URL: https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0167:book=10:section=600d
```
Ὅμηρον δ᾽ ἄρα οἱ ἐπ᾽ ἐκείνου, εἴπερ οἷός τ᾽ ἦν πρὸς ἀρετὴν ὀνῆσαι ἀνθρώπους, ἢ Ἡσίοδον ῥαψῳδεῖν ἂν περιιόντας εἴων, καὶ οὐχὶ μᾶλλον ἂν αὐτῶν ἀντείχοντο ἢ τοῦ χρυσοῦ καὶ
```
### 4.3 Herodotus 5.67.1
URL: https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0125:book=5:chapter=67
```
Κλεισθένης γὰρ Ἀργείοισι πολεμήσας τοῦτο μὲν ῥαψῳδοὺς ἔπαυσε ἐν Σικυῶνι ἀγωνίζεσθαι τῶν Ὁμηρείων ἐπέων εἵνεκα, ὅτι Ἀργεῖοί τε καὶ Ἄργος τὰ πολλὰ πάντα ὑμνέαται
```
### 4.4 Homeric Hymn to Apollo 165–177 (the blind man of Chios)
URL: https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0137:hymn=3:card=165 (Perseus prints line numbers 165, 170, 175 at the start of those lines)
```
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
```

## 5. Lexica and etymological dictionaries

### 5.1 LSJ (Perseus, Liddell–Scott–Jones 1940)
ῥάπτω — URL https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=r(a/ptw
```
 ῥάπτω , Od.16.422, etc.: fut. ῥάψω （ἀπορ-) Aeschin.2.21: aor. 1 A.“ἔρραψα” Hdt.9.17, E.Andr.911; Ep. “ῥάψα” Il.12.296: aor. 2 ἔρρα^φον （συν-) Nonn.D.7.152: plpf. ἐρραφήκει （συν-) X.Eph.1.9:—Med., aor. “ἐρραψάμην” Ar.Eq.784, etc.:—Pass., fut. ῥα^φήσομαι （συν-) Androm. ap. Gal.13.685: aor. ἐρράφην [α^] D.54.41, v. infr.: pf. “ἔρραμμαι” Ar.Ec. 24, D.54.35: poet. plpf. ἔραπτο （συν-) Q.S.9.359:—sew together, stitch, “βοείας” Il.12.296: abs., Ar.Pl.513:—Med., ῥαψάμενον δερμάτων ὀχετόν having made himself a pipe of leather, Hdt.3.9; ῥαψάμενός σοι τουτί (sc. τὸ προσκεφάλαιον) having got it stitched or made, Ar.Eq. 784; also, sew on or to one, Id.Nu.538:—Pass., ἐρράφθαι τὸ χεῖλος to have one's lip sewed up, D.54.35, cf. 41; ἔχειν πώγωνας ἐρραμμένους to have beards sewed on, Ar.Ec.24; ἐν μηρῷ ποτ᾽ ἐρράφθαι Διός was sewn up in . ., E.Ba.243; ἐρραμμένα stitched work, a cushion or pad, Alex.98.11; “χρὴ τὸ ἔποχον τοιοῦτον ἐρράφθαι ὡς . . ” X.Eq.12.9. 
II. metaph. c. dat., devise, contrive, plot, σφιν κακὰ ῥ. Od.3.118, cf. Il. 18.367; φόνον, θάνατόν τε μόρον τε ῥ., Od.16.379,422; “ῥάψαι μόρον σοι” E.IT681; also ἐπ᾽ Ἕλλησι φόνον ῥ. Hdt.9.17; “εἴς τινα” E.Andr. 911; ἐπιβουλὰς ῥ. τινί, Lat. suere dolos, Alex.98.2: prov., τοῦτο τὸ ὑπόδημα ἔρραψας μὲν σύ, ὑπεδήσατο δὲ Ἀρισταγόρης you sewed the shoe but A. put it on, Hdt.6.1. 
2. generally, string or link together, unite, “ἀοιδήν” Hes.Fr.265. 
3. ῥάψαντα διὰ βίου τοῖς αὐτοκράτορσι, perh. f.l. in JHS42.168 (iii A.D.). 
4. ῥάπτουσα, ἡ, name of a plaster, Cels.5.19.6, 5.26.23.
```
ῥαψῳδός — URL https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=r(ayw%7Cdo/s
```
 ῥαψῳδ-ός , ὁ, A.reciter of Epic poems, sts. applied to the bard who recited his own poem, as to Hesiod, Nicocl. ap. Sch.Pi.N.2.2 (v. infr.); but usu., professional reciters, esp. of the poems of Homer, Hdt.5.67, Pl.Ion 530c, etc.: also ῥ. κύων, ironically, of the Sphinx who chanted her riddle, S.OT391. (Prob. from ῥάπτω, ἀοιδή; Hes.Fr. 265 speaks of himself and Homer as ἐν νεαροῖς ὕμνοις ῥάψαντες ἀοιδήν, and Pi.N.2.2 calls Epic poets ῥαπτῶν ἐπέων ἀοιδοί: not from ῥάβδος (cf. “ῥάβδος” 1.6) as if ῥαβδῳδός (Eust.6.24, ῥαβδῳδία ib.16).)
```
ὑφαίνω — URL https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=u(fai/nw
```
 ὑφαίνω [υ^], Ion. impf. A.“ὑφαίνεσκον” Od.19.149: fut. “ὑφα^νῶ” Ar.Ec. 654 (anap.): aor. “ὕφηνα” Od.4.739, 13.303, Ar.Lys.586, etc.; later ὕφα_να, LXXJd.16.14, Inscr.Délos 442 A206 (ii B. C.), AP6.265 (Noss.), Hymn.Is.14; as Dor. form, B.5.9, al.: pf. ὕφαγκα （συν-) D.H.Comp. 18, (παρ-) Ph.Byz.Mir.2.5:—Med., v. infr.: aor. “ὑφηνάμην” Pl.Phd. 87b, X.Mem.3.11.6:—Pass., aor. “ὑφάνθην” Pl.Ti.72c, (ἐν-, συν-) Hdt. 1.203, 5.105: pf. “ὕφασμαι” Antiph.99, Luc.VH1.18, (ἐν-) Hdt. 3.47, (παρ-) X.Cyr.5.4.48, but 3sg. “ὕφανται” S.E.M.8.129; a form ὑφήφασμαι is cited in Suid., ὑφήφανται in Phryn.PSp.32 B., “ὑφήφασται” Choerob. in Theod.2.91 H., “ὑφύφασται” Zenod. ap. EM785.46, Eust.1436.51: cf. ἐξυφαίνω. [υ^ exc. in augm. tenses.]:—weave, freq. in Hom., who always joins ἱστὸν ὑφαίνειν (cf. ὑφάω), Il.6.456, Od.2.104, al.; except in 13.108, φάρε᾽ ὑφαίνουσιν; so “ὑ. ὕφασμα” E.Ion 1417; “χλαῖναν” Ar.Lys.586; “ἱμάτιον” Pl.Hp.Mi.368c; “ἐν εὐπήνοις ὑφαῖς ὑ. τι” E.IT814; “ἐν Ἐκβατάνοισι ταῦθ᾽ ὑφαίνεται” Ar.V.1143; ἀράχνια ὑ., of spiders, Arist.HA542a13, cf. 623a8: abs., weave, ply the loom, Hdt.2.35; “αἱ ὑφαίνουσαι” Arist.GA717a36; “αἴγειροι πτελέαι τε ἐΰσκιον ἄλσος ὕφαινον” Theoc.7.8 (cj. Heinsius for ἔφαινον):— Med., “ἱμάτιον ὑφαίνεσθαι” Pl.Phd.87b, cf. X.Mem.3.11.6 sq.:—Pass., λίθος ὑφαινομένη, i.e. asbestos, Str.10.1.6. 
II. contrive, plan, of all schemes, good or bad, which are craftily imagined, freq. in Hom.; “πυκινὸν δόλον ἄλλον ὕφαινε” Il.6.187; “ἔνδοθι μῆτιν ὑ.” Od.4.678; ἐνὶ φρεσὶ μῆτιν ὑφήνας ib.739; “μῆτιν ὕφαινε μετὰ φρεσίν” Hes.Sc.28, cf. B.16.51; “δόλους καὶ μῆτιν ὑ.” Od.9.422; “μύθους καὶ μήδεα πᾶσιν ὑ.” Il.3.212, cf. Call.Fr.3ii10P. (Pass.); ταῦθ᾽ ὕφηναν ἡμῖν ἐπὶ τυραννίδι this was the plot they laid against us to bring in tyranny, Ar.Lys. 630; “πάντα . . ἐκ φρενὸς ὑφάνασα” Hymn.Is.14:—Med., Nicopho 5: but ὑφαίνεται is f.l. for ὑφαίνετε in Lyr.Adesp.ap. Stob.1.5.11 (v. NauckTGF2p.xx). 
III. generally, create, construct, “οἰκοδομήματα” Pl.Criti.116b; “ὄλβον” Pi.P.4.141; θεμείλια Φοῖβος ὑφαίνει he lays the foundation, Call.Ap.57; “κηρὸν ὑ.” Tryph.536:—Pass., ἀναίμου ὑφανθέντος [τοῦ σπληνός] Pl.Ti.72c. 
2. compose, write, ποικίλον ἄνδημα (metaph. of an ode) Pi.Fr.179; “ὕμνον” B.5.9. (ὑφ-αίνω, cf. ὑφή, ὕφος, OE. wefan 'weave', Skt. ubhnāti 'hold together, cover, bind'.)
```
ὑφάντης — URL https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=u(fa/nths
```
 ὑφάν-της , ου, ὁ, A.weaver, Pl.Phd.87b, R. 369d, Arist.Pol.1291a13, LXX Ex.26.1, PCair.Zen.80.10 (iii B. C.), etc.
```
ὕμνος — URL https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=u(/mnos (first part of the entry)
```
 ὕμνος , ὁ, A.hymn, ode, in praise of gods or heroes (“καί τι ἦν εἶδος ῳδῆς εὐχαὶ πρὸς θεούς, ὄνομα δὲ ὕμνοι ἐπεκαλοῦντο” Pl.Lg.700b; “ὕμνους θεοῖς καὶ ἐγκώμια τοῖς ἀγαθοῖς” Id.R.607a, cf. Arist.Po.1448b27), once in Hom., “ἀοιδῆς ὕμνος” Od.8.429 (folld. by Demodocus' song of the Wooden Horse, 499 sqq.); “ὕμνῳ νικήσαντα φέρειν τρίποδ᾽” Hes.Op.657; “ἀνδρῶν τε παλαιῶν ἠδὲ γυναικῶν ὕμνον ἀείδουσιν” h.Ap.161; freq. in Pi., ὕμνος πολύφατος, ἐπικώμιος, etc., O.1.8, N.8.50, al.; “Θήρωνος Ὀλυμπιονίκαν ὕμνον” O.3.3; and in B., “ὑφάνας ὕμνον” 5.10, cf. 6.11, al.; ὕμνοι θεῶν to or in honour of the gods, Pl.Lg.801d; “τιμῶν θεὰν ὕμνοισιν” E.Hipp.56; “τοὺς χοροὺς . . καὶ τοὺς ὕ. τῷ θεῷ ποιεῖτε” D.21.51, cf [...]
```
ἀοιδός — URL https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=a)oido/s
```
 ἀοιδός [α^], ὁ, (ἀείδω) A.singer, minstrel, bard, Il.24.720, Od.3.270, al., Hes.Th.95, Op.26, Sapph.92, etc.; “ἀ. ἀνήρ” Od.3.267; “θεῖος ἀ.” 4.17, 8.87, al.; “τοῦ ἀρίστου ἀνθρώπων ἀ.” Hdt.1.24; “πολλὰ ψεύδονται ἀ.” Arist.Metaph.983a4: c.gen., γόων, χρησμῶν ἀοιδός, E.HF110, Heracl. 403; πρᾶτος ἀ., of the cock, Theoc.18.56. 
```

### 5.2 Beekes, Etymological Dictionary of Greek (Brill 2010), archive.org OCR
Item https://archive.org/details/etymological-dictionary-of-greek-2010 (file ilovepdf_merged_djvu.txt). The OCR renders Greek headwords badly; the printed page numbers survive (1276, 1278). Secondary access: Brill online is paywalled; not fetched.
ῥάπτω (pp. 1275–1276), OCR as fetched:
```


pántu [v.] to sew (together), stitch, instigate’ (IL). 4?» 
«VAR Aor. páwau (IL), them. aor. Éppaqov (Nonn.), pass. pagijvau fut. páwoa, perf. 
[...]
1276 pánuq 


*ETYM Since Myc. e-ra-pe-me-na shows that päntw does not go back to a form with 
initial F-, the older etymology with Baltic (Lith. verpti, 1sg. verpiù ‘to spin’, Lith. 
verpti (virpti), virpéti ‘to tremble, shudder, vibrate’, Latv. virpét ‘to spin with a 
spindle; shudder’, vérpt ‘to spin, turn round about’) must be abandoned. Cf. further 
```
My reading of the head and verdict: "ῥάπτω [v.] ‘to sew (together), stitch, instigate’ (Il.). ◁?▷ ... Since Myc. e-ra-pe-me-na shows that ῥάπτω does not go back to a form with initial ϝ-, the older etymology with Baltic (Lith. verpti ... ‘to spin’ ...) must be abandoned." I.e. Beekes gives ῥάπτω no IE root.
ῥαψῳδός (p. 1278), OCR as fetched:
```
paywööc [m.] ‘rhapsodist, performer of epic (Homeric) poems’ (Hdt., S., Pl.). «GR» 

«DER Payw6d-ikdc ‘belonging to the rhapsodist’, -éw [v.] ‘to recite epic poems’, -ia [f.] 
‘reciting epic poems, epic poems’ (Att, etc.). 

*ETYM The word paywöög is a verbal governing compound of payaı wönv (àotórv), 
thus originally ‘who sews a poem together’, referring to the uninterrupted sequence 
of epic verses as opposed to the strophic compositions of lyrics; cf. Hes. Fr. 265 
payavtes dod, Pi. N. 2, 2‘Ounpida parráv £néov ... dowdoi (see Patzer Herm. 80 
(1952): 314ff.; Sealey REGr. 70 (1957): 312ff.). 
```
ὑφαίνω (p. 1540), OCR as fetched (head and ETYM):
```
boaívo [v.] ‘to weave, warp, devise, produce’ (Il). «IE *(h, ueb'- ‘weave’> 
Further nouns, probably back-formations: 1. br (nap-, ovv-, ég-, yvvatko-) [f.] 
fabric (trag, Pl, Arist, Hell. and late). 2. 6qoc [n.] ‘id’ (Pherecr, Eub. Hell. and 
late). 
*ETYM The Myc. form may prove that the root was *h,ueb"-. The chronology of the 
attestations suggests that bpalvw is not a denominative from ber), ógoc, but was 
transformed from an older primary present, a nasal present (cf. the Skt. forms) or 
from a nominal form in *ub"-n- (thus LIV). Gr. ber, Üpog may be explained as PIE 
derivatives, or as back-formations within Greek. The hapax legomena bpöwat, 
```
My reading: "ὑφαίνω [v.] ‘to weave, warp, devise, produce’ (Il.). ◁IE *(h₁)u̯ebʰ- ‘weave’▷ ... The Myc. form [e-we-pe-se-so-me-na] may prove that the root was *h₁u̯ebʰ-. ... transformed from an older primary present, a nasal present (cf. the Skt. forms) or from a nominal form in *ubʰ-n- (thus LIV)."

### 5.3 LIV² (Rix et al. 2001), archive.org OCR
Item https://archive.org/details/lexikon-der-indogermanischen-verben (file "Lexikon der indogermanischen Verben_djvu.txt"; metadata creator "Helmut Rix, Martin Kümmel", date 2001).
*u̯ebʰ- (p. 658), OCR as fetched:
```
*y- 
*yebh.! ‘umwickeln, weben’ IEW 1114 
Aorist ?%иёр"-/ир"- heth. wepta ‘webte’'* 
Präsens *u-ne/n-bH- ved. unap, aumbhan ‘binden, fesseln’ 
gr. роѓи ‘webe’? 
9*uébh-e- аһа. (+) weban ‘weben, flechten’? 
?toch.A wpantär “мебеп” 
a 
DÉI 7 2 4 
?*ubh-ié- [aav. ufiiā ‘besinge’ 
Kaus.-It. *uobh-éie- ?sogd. (+) w’f- ‘weben’ 
an. (+) vefja ‘штеп, umwickeln’ 
Neubildungen: nä-Präs. ved. ubhnäs ‘bindest, fesselst” 
Perfekt аһа. (+) wab ‘webte, flocht’ 
toch.B жара ‘webte’’ 
M.K.) 
```
My reading: "*u̯ebʰ- ‘umwickeln, weben’ IEW 1114. Aorist ?*u̯ébʰ-/ubʰ- heth. wepta ‘webte’; Präsens *u-né/n-bʰ- ved. unap, aumbhan ‘binden, fesseln’; gr. ὑφαίνω ‘webe’?; ?*u̯ébʰ-e- ahd. (+) weban ‘weben, flechten’; ?toch. A wpantär ‘weben’; ?*ubʰ-i̯é- aav. ufiiā ‘besinge’; Kaus.-It. *u̯obʰ-éi̯e- ?sogd. (+) wʾf- ‘weben’, an. (+) vefja ‘winden, umwickeln’; Neubildungen: nā-Präs. ved. ubhnās ‘bindest, fesselst’; Perfekt ahd. (+) wab ‘webte, flocht’, toch. B wāpa ‘webte’." Note the Avestan ufiiā ‘besinge’ (I sing/praise) placed under the weaving root.
ῥάπτω in LIV: it is not a lemma. It appears, queried and bracketed, under *u̯erp- (pp. 690–691), OCR as fetched:
```
*uerp- “hin- und herdrehen (?)'! IEW 1156 
Präsens *uerp-/urp- heth. warapzi, war(ap)panzi ‘waschen, baden; 
reiben’ 
?[gr. белто ‘nähe, cke"? 
я am, даа. ГА ‚4 
[lit. verpiü, (verpti) “spinnen; stochern 
[r.-ksl. vorpu, (vorpsti) ‘reißen, rauben’ 
(M.K.) 
! Die Semantik bedarf noch der Untersuchung. 
2 Urspr. ‘reiben’, woraus ‘(Hände) waschen’ usw., vgl. OETTINGER 234. 
3 Semantisch und formal unklar, könnte auch Anlaut *sr° haben. 
4 Zum je-Präsens umgebildet. Vgl. apr. et-wier pt ‘loslassen’, po-wier pt ‘freilassen’. 
1.*uers- “abwischen, fegen’ IEW 1169-70 
Aorist  ?*uers-lurs- [skr. vfše “drosch’' 
```
My reading: "*u̯erp- ‘hin- und herdrehen (?)’¹ IEW 1156 ... ?[gr. ῥάπτω ‘nähe, flicke’]³ ... [lit. verpiù, (verpti) ‘spinnen; stochern’ ... ³ Semantisch und formal unklar, könnte auch Anlaut *sr° haben." So LIV tentatively attaches ῥάπτω to *u̯erp- (not *srep-), with the *sr- alternative in the footnote; Beekes (above) rejects the Baltic connection on Mycenaean evidence.

### 5.4 Kroonen 2013, de Vaan 2008, Mayrhofer EWAia, Chantraine DELG (archive.org OCR)
Kroonen, Etymological Dictionary of Proto-Germanic (Brill 2013), item https://archive.org/details/etymological-dictionary-of-proto-germanic, s.v. *weban- (p. 576), OCR:
```
*weban- s.v. ‘to weave’ — ON vefa s.v. ‘id.’, Far. veva s.v. ‘id.’, Elfd. wevd s.v. 
‘id.’, OE wefan s.v. ‘id’, E to weave, Du. weven s./w.v. ‘id.’, OHG weban s.v. ‘id.’, 
G weben s./wv. ‘id.’ => *hiuéb'-e- (IE) — ToAB wapa- ‘to weave’ < 
*h,uobh-eh2-; Skt. ubhnati, umbhati, undbdhi ‘to bind, fetter’ < *h;ub*-nehz-, 
*hyu-m-bh-e-, *hyu-n-eb'-; NP bdftan, Oss. wafyn | wafun ‘id.’ < *hjuob-; Gr. 
v@aivw ‘id.’ < *hzubh-n-ie-; Alb. venj ‘id.’ < *hjueb'-n-ie-. 
A strong verb with clear IE roots. See also *wabja- and *wabjan-. 
```
de Vaan, Etymological Dictionary of Latin (Brill 2008), item https://archive.org/details/de-vaan-michiel-etymological-dictionary-of-latin, s.v. texō, OCR:
```
texo, -ere ‘to weave, construet’ [v. 111; pf. texui, ppp. textum] (P1.+) 
Derivatives: textilis ‘woven, plaited’ (Lucr.+), textor ‘weaver’ (P1.+), textrinum 
‘place of weaving, of constructing’ (Enn.+), textus , -iis ‘structure’ (Lucr.+), textura 
'structure, weaving’ (Lucr.+); tela ‘cloth on a loom, spider’s web, plan’ (P1.+), 
subtilis [adj.] ‘fine in texture, precise’ (Lucr.+), subtemen [also subtegmen ] ‘weft, 
threads in a loom’ (P1.+); extexere ‘to unweave’ (P1 .+), praetexta ‘toga with a purple 
border’ (Lucil.+). 
PIt. *tekse/o -. 
PIE *te£-s- [pr,] ‘to fashion’. IE cognates: Hit. taks- 1 ‘to devise, undertake’ < 
*teks-/tks~, MHG dehsen ‘to break flax’; Skt. pr. taksati [3p.act.J, tadhi [3s.ipv.act.], 
tasti [3s.act.], pf. tataksa [3s.act.j, ppp. tasta- ‘to hammer, form, fashion’, tastar- [m.] 
‘carpenter, master’, Av. tasat [3s.aor.inj.], OAv. tast [3s.pr.inj.] ‘to fashion’, tasta- 
‘created’; YAv. auui .. . tasti [3s.pr.act.]. 
```
Mayrhofer, EWAia II (Heidelberg: Winter, 1996), item https://archive.org/details/mayrhofer-EWA (file "Mayrhofer_EWA v2 (na-ha) 1996_djvu.txt"), s.v. VABH (p. 506), OCR:
```
VABH binden, fesseln, bändigen (RV [2,13,9 sam unap, 1,63,4 
ubhnäs, 4,19,4 ny-dubhnät], AV [Pfumbhata}, TS [aumbhan)], 
u.a. [s.u.]), ubdha- gefesselt (RV +); apömbhana- n. Fessel, 
Hemmnis (Käth +), ’vabhi- ‘webend’ (o. 1243). - Nu., dard., 
ni. (s. Tu S. 109b, s.v. UBH). - lir., jav. ubdaena- aus Webstoff 
bestehend (von *ubda- ‘gewebt’), mp. waf-, man. sogd. w’f-, 
chwaresm. w(’)f, oss. wafyn/wafun ‘weben’, usw. (Bai, Dict 
305b, 392b, Abaev IV 40 [mit Lit.], Samadi 208); hierher auch 
aav. jav. vaf- (Präs. uf-iia-) “besingen, preisen’ („*weben“ der 
Lieder), aav. va/us- ‘Spruch’ (s.o. II 505, s.v. vapus-; Bthl, 
Wb. 1346, Schm, Di 299 und Anm. 1724, Kel-Pir I 83 [10 
Anm. 1]). - Idg. *(Hueb* (s.u.), gr. ven f. Gewebe, bpaivo 
webe, zettle an, ahd. weban, toch. A wäp-, B wäp- weben. 
S. die Lit. bei Frisk II 977. Zur Semantik (‘weben’ — "binden, 
knüpfen’) s. PorzigGliederung 186; für die Form der Wurzel wurden 
*u-eb" (—- *hyeu, 0.1276), *h,ueb* (Bee, Dev 67, Chantraine 1164a, 
C. J. Ruijgh, LarTheor 449 und Anm. 15, vgl. Pet, Lar 72), *uebh, 
(Rasmussen, Morphophon 279, 312) vorgeschlagen, auch *web’H/ 
*ub"H (Kel-Pir, a.a.0.; aber YABH/ubdhä- ist Anit-Wurzel, Stnu, 
NuA 27, 61; vgl. Joachim 25, 49 [zu den sekundären Präsensbildun- 
gen im Ved.)]). 
$.0.1223 (s.v. UBJ). 
```
My reading of the key clauses: VABH ‘binden, fesseln, bändigen’ (RV 2.13.9 sam unap, 1.63.4 ubhnās, 4.19.4 ny-aubhnāt ...), ubdha- ‘gefesselt’; Iranian: YAv. ubdaēna- ‘aus Webstoff bestehend’ (from *ubda- ‘gewebt’), MP waf-, Sogd. wʾf-, Oss. wafyn/wafun ‘weben’; "hierher auch aav. jav. vaf- (Präs. uf-iia-) ‘besingen, preisen’ („*weben“ der Lieder), aav. vafuš- ‘Spruch’"; Idg. *(H)u̯ebʰ-; gr. ὑφή ‘Gewebe’, ὑφαίνω; ahd. weban; toch. A wäp-, B wāp- ‘weben’. The semantic note cites Porzig and the Avestan ‘weaving of songs’.
Chantraine, DELG (1968–80; the scan is the 1999 one-volume reprint), item https://archive.org/details/dictionnaire-etymologique-de-la-langue-grecque-histoire-des-mots-by-pierre-chantraine-z-lib.org . The OCR maps the French into Greek letters and is mostly unreadable; the numerals and Greek quotations survive. s.v. ῥαψῳδός, OCR as fetched (first lines):
```
ῥαψῳδός : πι. «ὐἰαρβοάο», ααἱ τόοιίθ ἀ68. βροῦπιοβ 
μοχιόνγίψαθϑ οὐ ὁρίχυοϑ (Ηἀΐ., ΡῚ., αἰί., οἴς.), ἀ' οὐ ῥαψῳδικός 
(ΡΙ., 6ἴ6.), -ία (ΡΙ., οἷς.), τέω (ΡΙ., 1500., 6[6.). 

Εἰς: Ἡνϊἀριηταθηῦ σομιροβό ἀθ ἀόροηάδηοθ ργορ θβϑὶΐ 
ἰθ8ϑι 46 ῥάψαι ἀοιδὴν (φδήν ; νοῖν ἀείδω), αἱ] 8 ΔρΡΙΐχι6- 
ταὶ ἃ 16 σοτηροβί(ίοι ᾿ἰπόφίτο 46} ὁρορόθ ρὰγ ορροβίψοη ἄνθὸ 
168 Βίγοριῃθϑ ᾿γγίαιθϑ, οἵ. ΗἨόβ. ἤν". 265 τὸ 357 ΜουκοΙθ801:- 
ψνοβί (ἃ ργοροβ ἀ' Ἠοχπὸνγ οἱ ἀ᾽ Ηόβίοάβ ἐν νεαροῖς ὕμνοις 
ῥάψαντες ἀοιδήν, ΡΙ. Ν. ῶ,2. “Ὁμηρίδαι ῥαπτῶν ἐπέων 
```
Legible content: "Hés. fr. 265 = 357 Merkelbach-West ... ἐν νεαροῖς ὕμνοις ῥάψαντες ἀοιδήν, Pi. N. 2,2 Ὁμηρίδαι ῥαπτῶν ἐπέων ἀοιδοί), cf. Patzer, Hermes 80, 1952, 314-325 ... Sealey, REG 70, 1957, 312-355 ... R. Schmitt, Dichtung und Dichtersprache §§ 608-609". The entries ῥάπτω (line 145328 of the OCR) and ὑφαίνω (line 174425) exist but their French text is not recoverable from this OCR; the printed DELG should be consulted [text unverified].
Wiktionary (secondary; the API rate-limited most requests): entry ὑφαίνω etymology as fetched via https://en.wiktionary.org/w/api.php?action=parse&page=ὑφαίνω&prop=wikitext : "From Proto-Indo-European *webʰ-, and therefore related distantly to Old English wefan (whence English weave), Sanskrit उभ्नाति (ubhnāti), Persian بافتن (bâftan), Tocharian A wäp-.<ref>{{R:grc:Beekes}}</ref>" (template-stripped). Entries ῥάπτω, ῥαψῳδός, wefan, *webʰ-, उभ्नाति: fetch refused (HTTP "too many requests") [unverified]. Old Norse vefa, Avestan ubdaēna-, Tocharian B wāp-: covered by Kroonen and Mayrhofer above.

## 6. Rigveda (GRETIL)

File: https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/1_sam/1_rv/rvh1-10u.htm . Header as fetched: "Rgveda / Based on the edition by Th. Aufrecht: Die Hymnen des Rig Veda, 2nd ed., Bonn 1877, / digitized by Barend A. Van Nooten and Gary B. Holland. / Revised and converted by Detlef Eichler." The text is unaccented (so e.g. tántubhis appears as tantubhis). VedaWeb (https://vedaweb.uni-koeln.de/) was probed: its current API (FastAPI, /api/openapi.json) has no public per-stanza endpoint that I could resolve, so VedaWeb was not used. No translation (Griffith or Jamison–Brereton) was fetched; none is quoted.

**RV 10.71.1–4 (the origin of vāc; 10.71.2 "saktum iva titaunā punanto")**
```
RV_10,071.01a bṛhaspate prathamaṃ vāco agraṃ yat prairata nāmadheyaṃ dadhānāḥ |
RV_10,071.01c yad eṣāṃ śreṣṭhaṃ yad aripram āsīt preṇā tad eṣāṃ nihitaṃ guhāviḥ ||
RV_10,071.02a saktum iva titaunā punanto yatra dhīrā manasā vācam akrata |
RV_10,071.02c atrā sakhāyaḥ sakhyāni jānate bhadraiṣāṃ lakṣmīr nihitādhi vāci ||
RV_10,071.03a yajñena vācaḥ padavīyam āyan tām anv avindann ṛṣiṣu praviṣṭām |
RV_10,071.03c tām ābhṛtyā vy adadhuḥ purutrā tāṃ sapta rebhā abhi saṃ navante ||
RV_10,071.04a uta tvaḥ paśyan na dadarśa vācam uta tvaḥ śṛṇvan na śṛṇoty enām |
RV_10,071.04c uto tvasmai tanvaṃ vi sasre jāyeva patya uśatī suvāsāḥ ||
```
**RV 10.130.1–2 (the sacrifice stretched with threads: tantubhis tata; vayanti; otave)**
```
RV_10,130.01a yo yajño viśvatas tantubhis tata ekaśataṃ devakarmebhir āyataḥ |
RV_10,130.01c ime vayanti pitaro ya āyayuḥ pra vayāpa vayety āsate tate ||
RV_10,130.02a pumāṃ enaṃ tanuta ut kṛṇatti pumān vi tatne adhi nāke asmin |
RV_10,130.02c ime mayūkhā upa sedur ū sadaḥ sāmāni cakrus tasarāṇy otave ||
```
**RV 1.130.6 (imāṃ te vācam ... rathaṃ na dhīraḥ svapā atakṣiṣuḥ)**
```
RV_1,130.06a imāṃ te vācaṃ vasūyanta āyavo rathaṃ na dhīraḥ svapā atakṣiṣuḥ sumnāya tvām atakṣiṣuḥ |
RV_1,130.06d śumbhanto jenyaṃ yathā vājeṣu vipra vājinam |
RV_1,130.06f atyam iva śavase sātaye dhanā viśvā dhanāni sātaye ||
```
**RV 5.29.15 (brahma ... vastreva ... rathaṃ na dhīraḥ svapā atakṣam)**
```
RV_5,029.15a indra brahma kriyamāṇā juṣasva yā te śaviṣṭha navyā akarma |
RV_5,029.15c vastreva bhadrā sukṛtā vasūyū rathaṃ na dhīraḥ svapā atakṣam ||
```
**RV 1.62.13 (navyam atakṣad brahma)**
```
RV_1,062.13a sanāyate gotama indra navyam atakṣad brahma hariyojanāya |
RV_1,062.13c sunīthāya naḥ śavasāna nodhāḥ prātar makṣū dhiyāvasur jagamyāt ||
```
**RV 1.61.4 (stomam ... rathaṃ na taṣṭeva)**
```
RV_1,061.04a asmā id u stomaṃ saṃ hinomi rathaṃ na taṣṭeva tatsināya |
RV_1,061.04c giraś ca girvāhase suvṛktīndrāya viśvaminvam medhirāya ||
```
**RV 6.9.2–3 (nāhaṃ tantuṃ na vi jānāmy otum)**
```
RV_6,009.02a nāhaṃ tantuṃ na vi jānāmy otuṃ na yaṃ vayanti samare 'tamānāḥ |
RV_6,009.02c kasya svit putra iha vaktvāni paro vadāty avareṇa pitrā ||
RV_6,009.03a sa it tantuṃ sa vi jānāty otuṃ sa vaktvāny ṛtuthā vadāti |
RV_6,009.03c ya īṃ ciketad amṛtasya gopā avaś caran paro anyena paśyan ||
```
**RV 10.53.6 (tantuṃ tanvan rajaso bhānum anv ihi ... vayata)**
```
RV_10,053.06a tantuṃ tanvan rajaso bhānum anv ihi jyotiṣmataḥ patho rakṣa dhiyā kṛtān |
RV_10,053.06c anulbaṇaṃ vayata joguvām apo manur bhava janayā daivyaṃ janam ||
```
**RV 2.3.6 (tantuṃ tataṃ saṃvayantī ... yajñasya peśaḥ)**
```
RV_2,003.06a sādhv apāṃsi sanatā na ukṣite uṣāsānaktā vayyeva raṇvite |
RV_2,003.06c tantuṃ tataṃ saṃvayantī samīcī yajñasya peśaḥ sudughe payasvatī ||
```
**RV 7.33.9 (yamena tatam paridhiṃ vayanto)**
```
RV_7,033.09a ta in niṇyaṃ hṛdayasya praketaiḥ sahasravalśam abhi saṃ caranti |
RV_7,033.09c yamena tatam paridhiṃ vayanto 'psarasa upa sedur vasiṣṭhāḥ ||
```
Note on the task list: "RV 1.61.8" is not a weaving passage in this text (RV_1,061.08a asmā id u gnāś cid devapatnīr indrāyārkam ahihatya ūvuḥ: ūvuḥ ‘they wove’ the arka — in fact a weaving verb, from VABH/ū-; worth keeping). ṛṣi as kāru ‘artisan/singer’: e.g. RV_1,102.09c "semaṃ naḥ kārum upamanyum udbhidam" (grep kārum in the GRETIL file; not fetched as a separate passage).
```
RV_1,061.08a asmā id u gnāś cid devapatnīr indrāyārkam ahihatya ūvuḥ |
RV_1,061.08c pari dyāvāpṛthivī jabhra urvī nāsya te mahimānam pari ṣṭaḥ ||
```

## 7. Comparanda: Old English and Latin

### 7.1 Cynewulf, Elene 1236–1240 ("wordcræft wæf")
Edition fetched: Julius Zupitza, Cynewulfs Elene, mit einem Glossar (Berlin: Weidmann, 1883), archive.org item CynewulfsElene, OCR file. URL https://archive.org/download/CynewulfsElene/ (file listed in https://archive.org/metadata/CynewulfsElene). OCR as fetched (þ appears as "J)" / "]3" etc.):
```
XV. 
J)VS ic frod ond füs ]3urh J>aet faecne hus 
wordcraeft waef ond wundrum laes, 
Jirägum Jireodude ond getane reodode 
```
My reading: "Þus ic frod ond fus þurh þæt fæcne hus / wordcræft wæf ond wundrum læs, / þragum þreodude ond geþanc reodode / nihtes nearwe." (Elene 1236–1239 in Zupitza's lineation; = ASPR 1236–1239; the task's "1237" counts from the fitt start.) Second witness: Charles W. Kent, Elene (Boston: Ginn, 1895), archive.org item eleneanoldenglis00cyneuoft, glossary and note as fetched:
```
wefan,  sv.  V.,  weave ;  wordcrseft 
wsef,  I  wove  skill  of  words,  1238. 
wordcraeft,  m.,  wordcraft,  art 
of  speech ;  wordcraeftes  wis,  592 ; 
poetic  art  (wordcrseft,  1238). 
1238.  \vaef,  his  own  work ;  laes,  his  compilation  from  other  sources. 
```
### 7.2 Horace, Epistles 2.1.224–226 (tenui deducta poemata filo)
URL: https://www.thelatinlibrary.com/horace/epist2.shtml . As fetched:
```
cum lamentamur non apparere labores
nostros et tenui deducta poemata filo;               225
```
Vergil and Ovid examples of texere/deducere carmen were not fetched [unverified].

## 8. Not fetched / unverified in this file
- Pindar fr. 179 text (only LSJ's citation); Snell–Maehler's reading καινόν at Bacch. 19.8; Most's Loeb numbering of the Hesiod fragment; Chantraine's French text s.vv. ῥάπτω, ὑφαίνω; Wiktionary entries other than ὑφαίνω and texō; Griffith / Jamison–Brereton translations; Avestan Yasna passages; Old Norse kennings; Vergil/Ovid.
