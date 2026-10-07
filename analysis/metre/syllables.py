"""Rule-based English syllable counter for ASR commentary tokens (plan.md section 3).

No pronouncing dictionary is available offline, so syllables are estimated by vowel-group counting with the
corrections documented below. Digits are first expanded to British English number words.

Rules, in order (applied to a lower-cased token from common.tokenize):
  1. Contractions: the part before the apostrophe is counted; "n't" adds 1 unless the base is do/ca/wo/ai/sha/are/were
     (don't, can't, won't, ain't, shan't, aren't, weren't are one syllable); 'll, 've, 'd add 1 after a consonant-final base
     (it'll, should've, it'd); 's adds 1 after a sibilant (s, x, z, ch, sh, ce, ge); 're, 'm add nothing.
  2. Tokens with digits: numbers are read as British English words ("350" = three hundred and fifty, years 1900-2099 as two
     pairs, "0" = love, ordinals such as "1st" = first); the syllables of those words are summed.
  3. Words in EXCEPTIONS take the listed count.
  4. Otherwise: "qu"/"gu" before a vowel count u as a consonant; a final silent "e" is dropped (not after consonant+l or consonant+r, not "ee");
     a final "es" is silent unless preceded by a sibilant, c, g, i, consonant+l or consonant+r; a final "ed" is silent unless preceded by t or d;
     vowel groups [aeiouy]+ are counted ("y" at the start of a word is a consonant); +1 for "ing" after a vowel (going, playing),
     +1 for "ia" not after c/t (Serbia), +1 for "iu" (stadium), +1 for "io" not in -tion/-sion/-cion/-tious/-cious (ratio),
     +1 for "ua" not after q/g (actual); -1 for an internal silent e in -ely/-ement/-eful/-eness; minimum 1.
Accuracy is measured on a hand-coded fixture (FIXTURE below; input data, not a result) by check() and written to results/.
"""
import re

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
ORD = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth", "nine": "ninth",
       "twelve": "twelfth"}

EXCEPTIONS = {
    "the": 1, "be": 1, "he": 1, "she": 1, "we": 1, "me": 1, "are": 1, "were": 1, "there": 1, "where": 1, "here": 1,
    "every": 2, "everything": 3, "everybody": 4, "everyone": 3, "evening": 2, "different": 2, "difference": 2,
    "area": 3, "idea": 3, "video": 3, "rodeo": 3, "real": 1, "really": 2, "being": 2, "quiet": 2, "science": 2,
    "create": 2, "created": 3, "creating": 3, "lion": 2, "poem": 2, "poet": 2, "chaos": 2, "naive": 2,
    "business": 2, "family": 3, "camera": 3, "several": 3, "interesting": 3, "favourite": 3, "favorite": 3,
    "someone": 2, "somebody": 3, "something": 2, "sometimes": 2, "somewhere": 2, "anyone": 3, "nowhere": 2,
    "whereas": 2, "fire": 1, "hour": 1, "our": 1, "their": 1, "theirs": 1, "lower": 2, "power": 2, "tower": 2,
    "flower": 2, "shower": 2, "towel": 2, "towels": 2, "player": 2, "players": 2, "prayer": 1, "layer": 2,
    "maybe": 2, "people": 2, "recipe": 3, "simile": 3, "apostrophe": 4, "epitome": 4, "hyperbole": 4,
    "wednesday": 2, "vehicle": 3, "colonel": 2, "iron": 2, "ocean": 2, "fuel": 2, "cruel": 2, "dual": 2,
    "doing": 2, "going": 2, "seeing": 2, "agreeing": 3, "fluent": 2, "influence": 3, "continue": 3,
    "deuce": 1, "juice": 1, "serve": 1, "serves": 1, "ace": 1, "aces": 2, "hawkeye": 2, "hawk-eye": 2,
    "djokovic": 3, "federer": 3, "alcaraz": 3, "nadal": 2, "novak": 2, "roger": 2, "carlos": 2, "rafa": 2,
    "wimbledon": 3, "boris": 2, "becker": 2, "medvedev": 3, "sinner": 2, "andy": 2, "murray": 2,
    "tiebreak": 2, "tiebreaker": 3, "breakpoint": 2, "forehand": 2, "backhand": 2, "baseline": 2,
    "unforced": 2, "rally": 2, "rallies": 2, "volley": 2, "volleys": 2, "championship": 3, "championships": 3,
    "yes": 1, "yeah": 1, "oh": 1, "ooh": 1, "wow": 1, "whoa": 1, "uh": 1, "um": 1, "ah": 1, "aha": 2,
    "okay": 2, "ok": 2, "mr": 2, "mrs": 2, "ms": 1, "vs": 2, "km": 3, "mph": 3, "tv": 2, "bbc": 3, "atp": 3,
    "usa": 3, "uk": 2, "us": 1,
    "hundred": 2, "hundreds": 2, "nineteen": 2, "ninety": 2, "nineties": 2, "rhythm": 2, "rhythms": 2,
}


def _two_digit(n):
    if n < 20:
        return [ONES[n]]
    t, o = divmod(n, 10)
    return [TENS[t]] + ([ONES[o]] if o else [])


def number_words(n):
    """British English cardinal reading of a non-negative integer (with 'and' after hundreds)."""
    if n == 0:
        return ["love"]  # in tennis commentary a standalone 0 is read 'love'
    if 1900 <= n <= 1999 or 2010 <= n <= 2099:
        hi, lo = divmod(n, 100)
        return _two_digit(hi) + (["hundred"] if lo == 0 else (["oh"] + [ONES[lo]] if lo < 10 else _two_digit(lo)))
    if n >= 1_000_000:
        hi, lo = divmod(n, 1_000_000)
        return number_words(hi) + ["million"] + (number_words_nonzero(lo) if lo else [])
    if n >= 1000:
        hi, lo = divmod(n, 1000)
        rest = []
        if lo:
            rest = (["and"] if lo < 100 else []) + number_words_nonzero(lo)
        return number_words_nonzero(hi) + ["thousand"] + rest
    if n >= 100:
        hi, lo = divmod(n, 100)
        return [ONES[hi], "hundred"] + (["and"] + _two_digit(lo) if lo else [])
    return _two_digit(n)


def number_words_nonzero(n):
    return ["zero"] if n == 0 else (number_words(n) if n != 0 else [])


def digits_to_words(tok):
    """Expand a token containing digits ('15', '350', '1st', '2019', '6-4' is already split by the tokenizer)."""
    m = re.fullmatch(r"(\d+)(st|nd|rd|th|s)?", tok)
    if not m:
        # mixed tokens such as '4k' or 'b2b': read digit runs as numbers, letters as letters-words
        out = []
        for part in re.findall(r"\d+|[a-z]+", tok):
            out += digits_to_words(part) if part.isdigit() else [part]
        return out
    num = int(m.group(1)) if len(m.group(1)) < 10 else 0
    words = number_words(num) if m.group(1) != "0" or not m.group(2) else ["zero"]
    suf = m.group(2)
    if suf in ("st", "nd", "rd", "th") and words:
        last = words[-1]
        words = words[:-1] + [ORD.get(last, last[:-1] + "ieth" if last.endswith("y") else last + "th")]
    elif suf == "s" and words:  # '90s'
        words = words[:-1] + [words[-1] + "s"]
    return words


SIBILANT_END = re.compile(r"(s|x|z|ch|sh|ce|ge)$")


def _basic(w):
    w = re.sub(r"[^a-z]", "", w)
    if not w:
        return 0
    if w in EXCEPTIONS:
        return EXCEPTIONS[w]
    x = w
    x = re.sub(r"(q|g)u(?=[aeiouy])", r"\1w", x)        # qu/gu + vowel: u is a glide
    if x.endswith("es") and len(x) > 3:
        stem = x[:-2]
        if not (SIBILANT_END.search(stem) or re.search(r"[^aeiouy][lr]$", stem) or stem.endswith(("i", "c", "g"))):
            x = stem + "s"                                # serves, times, games -> silent e
    elif x.endswith("ed") and len(x) > 3 and x[-3] not in "td" and x[-3] not in "aeiouy":
        x = x[:-2] + "d"                                  # played/served -> silent e
    elif x.endswith("ed") and len(x) > 3 and x[-3] == "y":  # played
        x = x[:-2] + "d"
    if x.endswith("e") and not x.endswith("ee") and len(x) > 2:
        if not re.search(r"[^aeiouy][lr]e$", x):
            x = x[:-1]                                    # silent final e
    groups = re.findall(r"[aeiouy]+", x[0].replace("y", "b") + x[1:])
    n = len(groups)
    if re.search(r"[aeiouy]ing$", x):
        n += 1
    n += len(re.findall(r"(?<![ct])ia", x))
    n += len(re.findall(r"iu", x))
    n += len(re.findall(r"io(?!n)", x)) - len(re.findall(r"[tc]ious", x))
    n += len(re.findall(r"(?<![qg])ua", x))
    n -= len(re.findall(r"[^aeiouy]e(ly|ment|ful|ness)", x))
    return max(1, n)


def count_token(tok):
    """Syllables of one token from common.tokenize (lower-case, apostrophes kept, no hyphens)."""
    if any(c.isdigit() for c in tok):
        return sum(_basic(w) for w in digits_to_words(tok))
    if "'" in tok:
        base, _, suf = tok.partition("'")
        if suf == "t" and base.endswith("n"):
            b = base[:-1]
            if b in ("do", "ca", "wo", "ai", "sha", "are", "were", "can"):
                return _basic(base if b in ("ca",) else b) if b not in ("are", "were") else 1
            return _basic(b) + 1
        n = _basic(base)
        if suf in ("ll", "ve", "d") and base and base[-1] not in "aeiouy":
            n += 1
        elif suf == "s" and SIBILANT_END.search(base):
            n += 1
        return n
    return _basic(tok)


def count_tokens(tokens):
    return sum(count_token(t) for t in tokens)


# Hand-coded fixture (input data): common commentary words and their syllable counts in standard British pronunciation.
FIXTURE = {
    "game": 1, "set": 1, "match": 1, "point": 1, "break": 1, "love": 1, "fifteen": 2, "thirty": 2, "forty": 2,
    "advantage": 3, "deuce": 1, "serve": 1, "served": 1, "serving": 2, "server": 2, "return": 2, "returned": 2,
    "returning": 3, "forehand": 2, "backhand": 2, "volley": 2, "winner": 2, "winners": 2, "error": 2, "errors": 2,
    "unforced": 2, "double": 2, "fault": 1, "faults": 1, "second": 2, "first": 1, "championship": 3,
    "wimbledon": 3, "federer": 3, "djokovic": 3, "novak": 2, "roger": 2, "tiebreak": 2, "challenge": 2,
    "challenging": 3, "beautiful": 3, "brilliant": 2, "incredible": 4, "unbelievable": 5, "absolutely": 4,
    "definitely": 4, "pressure": 2, "moment": 2, "moments": 2, "important": 3, "opportunity": 5, "chance": 1,
    "chances": 2, "played": 1, "playing": 2, "player": 2, "players": 2, "plays": 1, "shot": 1, "shots": 1,
    "position": 3, "decision": 3, "nervous": 2, "tension": 2, "finally": 3, "actually": 4, "usually": 4,
    "really": 2, "little": 2, "simple": 2, "single": 2, "people": 2, "crowd": 1, "court": 1, "centre": 2,
    "line": 1, "lines": 1, "baseline": 2, "net": 1, "cross": 1, "down": 1, "wide": 1, "body": 2, "the": 1,
    "and": 1, "that's": 1, "it's": 1, "he's": 1, "doesn't": 2, "didn't": 2, "couldn't": 2, "don't": 1,
    "can't": 1, "won't": 1, "there's": 1, "what's": 1, "let's": 1, "we've": 1, "i'm": 1, "you're": 1,
    "it'll": 2, "should've": 2, "matches": 2, "aces": 2, "times": 1, "games": 1, "sets": 1, "wanted": 2,
    "needed": 2, "finished": 2, "missed": 1, "changed": 1, "excited": 3, "created": 3, "quality": 3,
    "question": 2, "language": 2, "previous": 3, "serious": 3, "precious": 2, "ratio": 3, "stadium": 3,
    "serbia": 3, "australia": 4, "media": 3, "special": 2, "lately": 2, "completely": 3, "statement": 2,
    "careful": 2, "going": 2, "doing": 2, "being": 2, "seeing": 2, "again": 2, "against": 2, "into": 2,
    "over": 2, "under": 2, "every": 2, "another": 3, "together": 3, "history": 3, "fifth": 1, "final": 2,
    "finals": 2, "title": 2, "titles": 2, "singles": 2, "doubles": 2, "momentum": 3, "rhythm": 2,
    "15": 2, "30": 2, "40": 2, "0": 1, "2019": 4, "350": 6, "100": 3, "1st": 1, "8": 1, "12": 1, "13": 2,
}


def check():
    """Accuracy of count_token on the hand-coded fixture."""
    rows = [(w, gold, count_token(w)) for w, gold in FIXTURE.items()]
    wrong = [(w, g, c) for w, g, c in rows if g != c]
    return {"n_fixture_words": len(rows), "n_exact": len(rows) - len(wrong),
            "accuracy": round((len(rows) - len(wrong)) / len(rows), 4),
            "mean_abs_error": round(sum(abs(g - c) for _, g, c in rows) / len(rows), 4),
            "errors": [{"word": w, "gold": g, "counted": c} for w, g, c in wrong],
            "n_fixture_words_in_exception_list": sum(w in EXCEPTIONS for w in FIXTURE),
            "accuracy_excluding_exception_list": round(
                sum(g == c for w, g, c in rows if w not in EXCEPTIONS) / sum(w not in EXCEPTIONS for w in FIXTURE), 4)}


if __name__ == "__main__":
    import json
    print(json.dumps(check(), indent=1))
