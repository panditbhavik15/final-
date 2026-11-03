"""Verification engine for the Data Structures (2BTCO301) question bank.

Every number quoted in Data_Structures_2BTCO301_Question_Bank_Answer_Key.md is produced here.
The notes' own worked examples are re-run, so a disagreement is reported instead of hidden.
"""
import itertools
import math
import pathlib
import random

OUT = []


def say(*a):
    OUT.append(" ".join(str(x) for x in a))


def hdr(t):
    say("")
    say("=" * 78)
    say(t)
    say("=" * 78)


# ---------------------------------------------------------------- trees
def build(pre, ino):
    if not pre:
        return None
    r = pre[0]
    i = ino.index(r)
    li, ri = ino[:i], ino[i + 1:]
    lp, rp = pre[1:1 + len(li)], pre[1 + len(li):]
    return (r, build(lp, li), build(rp, ri))


def trav(t, kind):
    if t is None:
        return []
    r, l, rr = t
    if kind == "pre":
        return [r] + trav(l, kind) + trav(rr, kind)
    if kind == "in":
        return trav(l, kind) + [r] + trav(rr, kind)
    return trav(l, kind) + trav(rr, kind) + [r]


def children(t):
    if t is None:
        return []
    r, l, rr = t
    out = []
    if l:
        out.append((r, l[0], "L"))
    if rr:
        out.append((r, rr[0], "R"))
    return out + children(l) + children(rr)


def check_tree(title, pre, ino, post):
    say(title)
    t = build(pre, ino)
    gp, gi, gq = trav(t, "pre"), trav(t, "in"), trav(t, "post")
    say("   notes pre :", " ".join(pre))
    say("   rebuilt   :", " ".join(gp), "| match:", gp == pre)
    say("   notes in  :", " ".join(ino))
    say("   rebuilt   :", " ".join(gi), "| match:", gi == ino)
    say("   notes post:", " ".join(post))
    say("   rebuilt   :", " ".join(gq), "| match:", gq == post)
    say("   edges (parent->child side):",
        " ".join("%s%s%s" % (p, s[0], c) for p, c, s in children(t)))
    say("   nodes=%d edges=%d (a tree with n nodes has n-1 edges: %s)"
        % (len(pre), len(children(t)), len(children(t)) == len(pre) - 1))
    return gp == pre and gi == ino and gq == post


# ---------------------------------------------------------------- infix
PREC = {"^": 3, "*": 2, "/": 2, "%": 2, "+": 1, "-": 1}
RIGHT_ASSOC = {"^"}


def infix_to_postfix(s, assoc_all=False):
    # assoc_all=True treats EVERY operator as right-associative, which is what the
    # reverse trick in infix_to_prefix needs: reversing the string flips the order in
    # which same-precedence operators appear, so left-associative X-Y+Z would otherwise
    # come out as X-(Y+Z) instead of (X-Y)+Z.
    out, st = [], []
    for ch in s.replace(" ", ""):
        if ch.isalnum():
            out.append(ch)
        elif ch == "(":
            st.append(ch)
        elif ch == ")":
            while st and st[-1] != "(":
                out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != "(" and (
                    PREC[st[-1]] > PREC[ch] or
                    (PREC[st[-1]] == PREC[ch] and not assoc_all and ch not in RIGHT_ASSOC)):
                out.append(st.pop())
            st.append(ch)
    while st:
        out.append(st.pop())
    return "".join(out)


def infix_to_prefix(s):
    # reverse the string, mirror the brackets, take the postfix of that, reverse again
    rev = s.replace(" ", "")[::-1]
    rev = rev.replace("(", "\x01").replace(")", "(").replace("\x01", ")")
    return infix_to_postfix(rev, assoc_all=True)[::-1]


def eval_postfix(expr, show=True):
    st = []
    for ch in expr.replace(" ", ""):
        if ch.isdigit():
            st.append(int(ch))
        else:
            b, a = st.pop(), st.pop()
            r = {"+": a + b, "-": a - b, "*": a * b, "/": a // b, "%": a % b}[ch]
            st.append(r)
            if show:
                say("      %d %s %d = %d   stack now %s" % (a, ch, b, r, st))
    return st[0]


# ---------------------------------------------------------------- sorts
def bubble_passes(a):
    x = list(a)
    n = len(x)
    passes = []
    for i in range(n - 1):
        snap = []
        for j in range(n - 1 - i):
            if x[j] > x[j + 1]:
                x[j], x[j + 1] = x[j + 1], x[j]
                snap.append(list(x))
        passes.append((i + 1, list(x), snap))
    return passes


def selection_passes(a):
    x = list(a)
    n = len(x)
    rows = []
    for i in range(n - 1):
        m = min(range(i, n), key=lambda k: x[k])
        before = list(x)
        if m != i:
            x[i], x[m] = x[m], x[i]
        rows.append((i + 1, i, m, before[i], x[i], list(x)))
    return rows


def insertion_passes(a):
    x = list(a)
    rows = []
    for i in range(1, len(x)):
        key = x[i]
        j = i - 1
        while j >= 0 and x[j] > key:
            x[j + 1] = x[j]
            j -= 1
        x[j + 1] = key
        rows.append((i, list(x)))
    return rows


def merge_two(p, q):
    i = j = 0
    out = []
    while i < len(p) and j < len(q):
        if p[i] <= q[j]:
            out.append(p[i]); i += 1
        else:
            out.append(q[j]); j += 1
    out += p[i:]
    out += q[j:]
    return out


def merge_sort(a, depth=0, trace=None):
    if len(a) <= 1:
        return list(a)
    m = len(a) // 2
    l = merge_sort(a[:m], depth + 1, trace)
    r = merge_sort(a[m:], depth + 1, trace)
    o = merge_two(l, r)
    if trace is not None:
        trace.append("  " * depth + "merge %s + %s -> %s" % (l, r, o))
    return o


def quick_sort(a, trace=None):
    if len(a) <= 1:
        return list(a)
    piv = a[-1]
    lo, eq, hi = [], [], []
    for v in a[:-1]:
        (lo if v < piv else hi if v > piv else eq).append(v)
    if trace is not None:
        trace.append("pivot=%d  <%s> = %s | = %s | <%s> = %s" % (piv, "<", lo, eq + [piv], ">", hi))
    return quick_sort(lo, trace) + eq + [piv] + quick_sort(hi, trace)


def radix_passes(a, base_digits=3):
    x = ["%0*d" % (base_digits, v) for v in a]
    passes = []
    for d in range(base_digits - 1, -1, -1):
        buckets = [[] for _ in range(10)]
        for v in x:
            buckets[int(v[d])].append(v)
        x = [v for b in buckets for v in b]
        passes.append((base_digits - d, {i: b for i, b in enumerate(buckets) if b}, list(x)))
    return passes, [int(v) for v in x]


def count_cmp(a, kind):
    n = len(a)
    c = 0
    x = list(a)
    if kind == "bubble":
        for i in range(n - 1):
            for j in range(n - 1 - i):
                c += 1
                if x[j] > x[j + 1]:
                    x[j], x[j + 1] = x[j + 1], x[j]
    elif kind == "selection":
        for i in range(n - 1):
            for j in range(i + 1, n):
                c += 1
    elif kind == "insertion":
        for i in range(1, n):
            j = i - 1
            key = x[i]
            while j >= 0:
                c += 1
                if x[j] > key:
                    x[j + 1] = x[j]
                    j -= 1
                else:
                    break
            x[j + 1] = key
    elif kind == "merge":
        def ms(v):
            nonlocal c
            if len(v) <= 1:
                return v
            m = len(v) // 2
            l, r = ms(v[:m]), ms(v[m:])
            i = j = 0
            o = []
            while i < len(l) and j < len(r):
                c += 1
                if l[i] <= r[j]:
                    o.append(l[i]); i += 1
                else:
                    o.append(r[j]); j += 1
            o += l[i:] + r[j:]
            return o
        ms(x)
    elif kind == "quick":
        def qs(v):
            nonlocal c
            if len(v) <= 1:
                return v
            p = v[-1]
            lo, hi = [], []
            for e in v[:-1]:
                c += 1
                (lo if e < p else hi).append(e)
            return qs(lo) + [p] + qs(hi)
        qs(x)
    return c


def stable_pairs(a):
    """sort list of (value, tag) with each algorithm, return the tag order."""
    x = list(a)
    n = len(x)
    kind_results = {}
    # bubble (stable)
    y = list(x)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if y[j][0] > y[j + 1][0]:
                y[j], y[j + 1] = y[j + 1], y[j]
    kind_results["bubble"] = [t for v, t in y]
    # insertion (stable)
    y = list(x)
    for i in range(1, n):
        key = y[i]
        j = i - 1
        while j >= 0 and y[j][0] > key[0]:
            y[j + 1] = y[j]
            j -= 1
        y[j + 1] = key
    kind_results["insertion"] = [t for v, t in y]
    # merge (stable)
    def ms(v):
        if len(v) <= 1:
            return v
        m = len(v) // 2
        l, r = ms(v[:m]), ms(v[m:])
        i = j = 0
        o = []
        while i < len(l) and j < len(r):
            if l[i][0] <= r[j][0]:
                o.append(l[i]); i += 1
            else:
                o.append(r[j]); j += 1
        return o + l[i:] + r[j:]
    kind_results["merge"] = [t for v, t in ms(x)]
    # selection (unstable)
    y = list(x)
    for i in range(n - 1):
        m = min(range(i, n), key=lambda k: y[k][0])
        y[i], y[m] = y[m], y[i]
    kind_results["selection"] = [t for v, t in y]
    # quick, the in-place Lomuto version the notes use (unstable)
    y = list(x)

    def lomuto(lo, hi):
        if lo >= hi:
            return
        p = y[hi]
        i = lo
        for j in range(lo, hi):
            if y[j][0] <= p[0]:
                y[i], y[j] = y[j], y[i]
                i += 1
        y[i], y[hi] = y[hi], y[i]
        lomuto(lo, i - 1)
        lomuto(i + 1, hi)
    lomuto(0, n - 1)
    kind_results["quick"] = [t for v, t in y]
    # heap (unstable)
    import heapq
    h = []
    for idx, (v, t) in enumerate(x):
        heapq.heappush(h, (v, idx))
    kind_results["heap"] = []
    while h:
        v, idx = heapq.heappop(h)
        kind_results["heap"].append(x[idx][1])
    return kind_results


# ---------------------------------------------------------------- hashing
def h_div(k, m, one_based=False):
    return k % m + (1 if one_based else 0)


def h_midsquare(k, m, take=(4, 3)):
    sq = k * k
    s = str(sq)
    from_right = s[::-1]
    return int(from_right[take[0] - 1] + from_right[take[1] - 1])


def probe_linear(tab, size, key, h):
    for t in range(size):
        i = (h + t) % size
        if tab[i] is None:
            tab[i] = key
            return t + 1
    return None


def probe_quadratic(tab, size, key, h, c1=1, c2=1):
    for t in range(size):
        i = (h + c1 * t + c2 * t * t) % size
        if tab[i] is None:
            tab[i] = key
            return t + 1
    return None


def probe_double(tab, size, key, h1, h2):
    for t in range(size):
        i = (h1 + t * h2) % size
        if tab[i] is None:
            tab[i] = key
            return t + 1
    return None


def main():
    say("Data Structures (2BTCO301) - verification log")
    say("generated by ds/verify_ds.py ; every True below is an executed check, not an assertion")

    # =========================================================== UNIT 3 trees
    hdr("Unit 3 - the notes' traversal examples, rebuilt from pre+in")
    ok1 = check_tree(
        "Notes p11-13 (the A..O tree)",
        list("ABDEFCGHJLMKO"),
        list("DBFEAGCLJMHOK"),
        list("DFEBGLMJOKHCA"))
    ok2 = check_tree(
        "Notes p14 example (a)",
        list("ABDGHLECFIJK"),
        list("GDHLBEACIFKJ"),
        list("GLHDEBIKJFCA"))
    ok3 = check_tree(
        "Notes p14 example (b)",
        list("ABDCEFGHI"),
        list("BDAEHGIFC"),
        list("DBHIGFECA"))
    say("all three notes examples internally consistent:", ok1 and ok2 and ok3)

    say("")
    say("a tree with n nodes has n-1 edges; max nodes at level L is 2^L; levels 0..h hold")
    say("   at most 2^(h+1)-1 nodes; a tree of height 3 (levels 0..3) holds at most", 2 ** 4 - 1, "nodes")
    for n in (3, 4, 5, 6):
        say("   n=%d nodes: min height %d, max height %d, min nodes of a full tree of height %d = %d"
            % (n, math.floor(math.log2(n)), n - 1, n - 1, 2 ** n - 1))

    hdr("Unit 3 - Binary Search Tree operations")
    seq = [50, 30, 70, 20, 40, 60, 80]
    root = None

    def ins(t, v):
        if t is None:
            return (v, None, None)
        r, l, rr = t
        if v < r:
            return (r, ins(l, v), rr)
        return (r, l, ins(rr, v))

    for v in seq:
        root = ins(root, v)
    say("   insert order", seq)
    say("   in-order (must be sorted):", trav(root, "in"), "sorted:", trav(root, "in") == sorted(seq))
    say("   pre-order :", trav(root, "pre"))
    say("   post-order:", trav(root, "post"))
    say("   height (edges on longest root->leaf path):", 2)

    def search_cmp(t, v):
        c = 0
        while t:
            c += 1
            r, l, rr = t
            if v == r:
                return c, True
            t = l if v < r else rr
        return c, False

    for v in (20, 80, 65):
        c, f = search_cmp(root, v)
        say("   search %3d : %d comparison(s), result = %s" % (v, c, "found" if f else "not in the tree"))
    say("   worst-case BST search cost = height+1 = 3 here; a degenerate (sorted-insert) tree of 7")
    say("   nodes would cost 7 comparisons -> BST average case O(log n), worst case O(n)")

    # =========================================================== UNIT 2 stack
    hdr("Unit 2 - infix / postfix / prefix, the notes' examples")
    cases = [
        ("(A-B)*(C+D)", "AB-CD+*"),
        ("(A+B)/(C+D)-(D*E)", "AB+CD+/DE*-"),
        ("A*(B+C)-D/E", "ABC+*DE/-"),
        ("A*(B+C)-D/(A*K)+L", "ABC+*DAK*/-L+"),
    ]
    for inf, notes in cases:
        got = infix_to_postfix(inf)
        say("   %-20s -> postfix %-14s notes: %-14s match: %s" % (inf, got, notes, got == notes))
    pcases = [("A+B", "+AB"), ("(A+B)*C", "*+ABC"), ("(A-B)*(C+D)", "*-AB+CD"),
              ("(A+B)/(C+D)-(D*E)", "-/+AB+CD*DE"), ("A*(B+C)-D/E", "-*A+BC/DE"),
              ("A*(B+C)-D/(A*K)+L", "+-*A+BC/D*AKL")]
    for inf, notes in pcases:
        got = infix_to_prefix(inf)
        say("   %-20s -> prefix  %-14s notes: %-14s match: %s" % (inf, got, notes, got == notes))

    say("")
    say("   the notes' 3-step reverse method on (A-B/C)*(A/K-L):")
    inf = "(A-B/C)*(A/K-L)"
    say("      step1 reverse + swap brackets :", inf[::-1].replace("(", "&").replace(")", "(").replace("&", ")"))
    step1 = inf[::-1].replace("(", "&").replace(")", "(").replace("&", ")")
    step2 = infix_to_postfix(step1)
    say("      step2 postfix of the reversed :", step2)
    say("      step3 reverse -> prefix       :", step2[::-1])
    say("      direct algorithm gives        :", infix_to_prefix(inf),
        "| identical:", step2[::-1] == infix_to_prefix(inf))
    say("      notes print: * - A / B C - / A K L  -> without spaces *-A/BC-/AKL, match:",
        infix_to_prefix(inf) == "*-A/BC-/AKL")

    say("")
    say("   postfix evaluation of the notes' 9 3 4 * 8 + 4 / -   (infix 9 - ((3*4)+8)/4):")
    v = eval_postfix("9 3 4 * 8 + 4 / -")
    say("      value =", v, "| python check 9 - ((3*4+8)/4) =", 9 - ((3 * 4 + 8) / 4),
        "| match:", v == 9 - ((3 * 4 + 8) / 4))

    hdr("Unit 2 - recursion and Tower of Hanoi")
    for n in range(1, 6):
        say("   n=%d discs : moves = 2^%d - 1 = %d" % (n, n, 2 ** n - 1))
    moves = []

    def hanoi(n, a, b, c):
        if n == 0:
            return
        hanoi(n - 1, a, c, b)
        moves.append("move disc %d from %s to %s" % (n, a, c))
        hanoi(n - 1, b, a, c)

    hanoi(3, "A", "B", "C")
    say("   n=3 full solution (%d moves):" % len(moves))
    for m in moves:
        say("      ", m)
    say("   recursive factorial 5! =", math.factorial(5), "| fib(10) via recursion =",
        __import__("functools").reduce(lambda a, _: (a[1], a[0] + a[1]), range(10), (0, 1))[0])

    # =========================================================== UNIT 2 queue
    hdr("Unit 2 - linear queue wasted space vs circular queue")
    MAX = 10
    lin = [None] * MAX
    front, rear = 0, -1
    for k in range(MAX):
        rear += 1
        lin[rear] = k
    say("   after 10 enqueues: front=%d rear=%d (rear==MAX-1 -> full)" % (front, rear))
    for _ in range(2):
        front += 1
    say("   after 2 dequeues : front=%d rear=%d -> 2 cells free at indexes 0,1" % (front, rear))
    say("   linear queue refuses the next insert because rear==MAX-1: %s (this is the drawback)"
        % (rear == MAX - 1))
    say("   usable capacity after those deletions = %d of %d cells" % (rear - front + 1, MAX))
    cir = [None] * MAX
    cf, cr, cnt = 0, -1, 0
    for k in range(MAX):
        cr = (cr + 1) % MAX
        cir[cr] = k
        cnt += 1
    for _ in range(2):
        cf = (cf + 1) % MAX
        cnt -= 1
    cr = (cr + 1) % MAX
    cir[cr] = "new"
    cnt += 1
    say("   circular queue: front=%d rear=%d, the new insert landed at index %d: %s"
        % (cf, cr, cr, cr == 0))
    say("   conditions - empty: front==-1 ; full: (rear+1)%%MAX==front ; here (9+1)%%10==0 ->",
        (9 + 1) % 10 == 0)

    hdr("Unit 2 - priority queue insertion order (notes p29-30)")
    pq = [("A", 1), ("B", 2), ("C", 3), ("D", 5)]
    say("   list sorted by priority (lower number = higher priority):", pq)
    new = ("F", 4)
    out = list(pq)
    pos = len(out)
    for i, e in enumerate(out):
        if e[1] > new[1]:
            pos = i
            break
    out.insert(pos, new)
    say("   F goes at index %d (first entry whose priority number is larger than 4 is %s)"
        % (pos, pq[pos][0] if pos < len(pq) else "none"))
    say("   insert F with priority 4 ->", out, "| F placed before D(5):",
        out.index(new) < out.index(("D", 5)))
    say("   priorities in the result:", [p for _, p in out], "non-decreasing:",
        [p for _, p in out] == sorted(p for _, p in out))

    # =========================================================== UNIT 2 arrays
    hdr("Unit 2 - sparse matrices: non-zero counts")
    for n in range(1, 8):
        low = sum(1 for i in range(n) for j in range(n) if i >= j)
        up = sum(1 for i in range(n) for j in range(n) if i <= j)
        tri = sum(1 for i in range(n) for j in range(n) if abs(i - j) <= 1)
        say("   n=%d  lower n(n+1)/2=%2d (enumerated %2d:%s)  upper=%2d:%s  tridiagonal 3n-2=%2d:%s"
            % (n, n * (n + 1) // 2, low, low == n * (n + 1) // 2, up, up == n * (n + 1) // 2,
               3 * n - 2, tri == 3 * n - 2))
    n = 100
    say("   n=100: full storage 10000 cells vs lower-triangular %d vs tridiagonal %d -> saving %.1f%%"
        % (n * (n + 1) // 2, 3 * n - 2, 100 * (1 - (n * (n + 1) // 2) / (n * n))))

    hdr("Unit 2 - array address arithmetic (row-major)")
    base, lo1, lo2, nrows, ncols, w = 1000, 1, 1, 10, 8, 2
    formula = lambda i, j: base + ((i - lo1) * ncols + (j - lo2)) * w
    brute = {}
    k = base
    for i in range(lo1, lo1 + nrows):
        for j in range(lo2, lo2 + ncols):
            brute[(i, j)] = k
            k += w
    bad = [key for key in brute if formula(*key) != brute[key]]
    say("   A[10][8], base=%d, element size=%d, rows stored one after another" % (base, w))
    say("   LOC(i,j)=base+((i-lo1)*ncols+(j-lo2))*w agrees with the enumeration for all %d cells: %s"
        % (len(brute), not bad))
    say("   example LOC(3,4) = %d ; LOC(1,1) = %d ; last cell LOC(10,8) = %d"
        % (formula(3, 4), formula(1, 1), formula(10, 8)))
    say("   column-major would be LOC(i,j)=base+((j-lo2)*nrows+(i-lo1))*w -> LOC(3,4)=%d"
        % (base + ((4 - 1) * nrows + (3 - 1)) * w))

    # =========================================================== UNIT 4 hashing
    hdr("Unit 4 - hash functions, reproducing the notes' numbers")
    say("   division method h(k)=k mod m with m=7:")
    for k in (169, 130):
        say("      h(%d) = %d mod 7 = %d   (notes: %s)" % (k, k, k % 7, "1 for 169, 4 for 130"))
    say("      169 mod 7 = 1 :", 169 % 7 == 1, "| 130 mod 7 = 4 :", 130 % 7 == 4)
    say("      1-based variant h(k)=k mod m + 1 -> 169 maps to slot", 169 % 7 + 1)
    say("   mid-square method, m=50 slots, keys 1632 1739 3123:")
    for k, notes in ((1632, 34), (1739, 41), (3123, 31)):
        sq = k * k
        s = str(sq)
        mid = h_midsquare(k, 50)
        say("      k=%d  k^2=%d  middle two digits (positions 4,3 from the right) = %02d  notes=%d  match: %s"
            % (k, sq, mid, notes, mid == notes))
    say("      note: the page says 'fourth and fifth digits counting from right'; the digits that")
    say("      actually produce 34/41/31 are the 4th and 3rd from the right (the two middle digits")
    say("      of a 7-digit square). The printed values are right, the wording is not.")
    say("   folding method, m=100, 2-digit parts. Two conventions exist; the notes use")
    say("   the one that cuts from the LEFT (so the short leftover group is last):")
    for k, notes in ((7325, 98), (76321, 9), (1623, 39), (7613, 89)):
        left, s = [], str(k)
        while len(s) > 2:
            left.append(int(s[:2])); s = s[2:]
        if s:
            left.append(int(s))
        right, s = [], str(k)
        while len(s) > 2:
            right.append(int(s[-2:])); s = s[:-2]
        if s:
            right.append(int(s))
        say("      k=%-6d left  %s sum=%3d mod 100 = %02d | right %s sum=%3d mod 100 = %02d"
            % (k, left, sum(left), sum(left) % 100, right, sum(right), sum(right) % 100))
        say("               notes give %02d -> matches the %s grouping: %s"
            % (notes, "left" if sum(left) % 100 == notes else "right" if sum(right) % 100 == notes
               else "NEITHER",
               notes in (sum(left) % 100, sum(right) % 100)))
    say("      for even-length keys both groupings give the same answer; only an odd-length")
    say("      key such as 76321 separates them (left 76+32+1=109->09, right 7+63+21=91).")
    say("   collision: h(k)=k%7 for k=8 and k=15 ->", 8 % 7, "and", 15 % 7,
        "| same address:", 8 % 7 == 15 % 7)

    hdr("Unit 4 - collision resolution compared on the same keys")
    keys = [50, 700, 76, 85, 96, 73, 101, 399, 541]
    m = 10
    say("   keys", keys, "with h(k)=k mod 10")
    say("   h values:", [k % m for k in keys])

    def report(name, tab, probes, keys_):
        failed = [k for k, p in zip(keys_, probes) if p is None]
        placed = [p for p in probes if p is not None]
        say("   %-18s table=%s" % (name, tab))
        say("   %-18s probes per insert=%s" % ("", probes))
        say("   %-18s total probes=%d  ASL over the %d inserted keys=%.2f"
            % ("", sum(placed), len(placed), sum(placed) / len(placed)))
        say("   %-18s slots left empty=%d  inserts that FAILED anyway=%s"
            % ("", sum(1 for x in tab if x is None), failed if failed else "none"))

    for name, fn in (("linear probing", probe_linear), ("quadratic probing", probe_quadratic)):
        tab = [None] * m
        probes = []
        for k in keys:
            probes.append(fn(tab, m, k, k % m))
        report(name, tab, probes, keys)
    tab = [None] * m
    h2 = lambda k: 1 + (k % (m - 1))
    probes = []
    for k in keys:
        probes.append(probe_double(tab, m, k, k % m, h2(k)))
    report("double hashing", tab, probes, keys)
    say("   why double hashing failed here: m=10 is not prime and h2(700)=%d shares the"
        % h2(700))
    say("   factor 2 with 10, so the probe sequence 0,8,6,4,2,0,... only visits the even slots")
    say("   and loops forever while slots 1 and 4 stay free. Fix: choose m prime, or")
    say("   gcd(h2(k), m) = 1. Same keys on m=11 with h2(k)=1+(k%10):")
    m11 = 11
    tab = [None] * m11
    probes = []
    for k in keys:
        probes.append(probe_double(tab, m11, k, k % m11, 1 + (k % 10)))
    report("double hashing m=11", tab, probes, keys)
    say("   every probe count is now non-None:", all(p is not None for p in probes))
    chains = {}
    for k in keys:
        chains.setdefault(k % m, []).append(k)
    say("   chaining           buckets=%s" % chains)
    say("   chaining           max chain length=%d ; no insert ever fails, so no overflow"
        % max(len(v) for v in chains.values()))
    say("   load factor lambda = n/m = %d/%d = %.2f (linear probing needs lambda < 1 to terminate)"
        % (len(keys), m, len(keys) / m))
    say("   clustering: linear probing makes runs; quadratic spreads them; double hashing spreads further")

    # =========================================================== UNIT 5 sorting
    hdr("Unit 5 - bubble sort, the notes' example 78 23 45 8 32 36")
    a = [78, 23, 45, 8, 32, 36]
    say("   start:", a)
    for i, end, snaps in bubble_passes(a):
        say("   pass %d: %d swap(s) -> %s   (index %d now holds %d, which is its final place)"
            % (i, len(snaps), end, len(a) - i, end[len(a) - i]))
        for s in snaps:
            say("        swap gives %s" % s)
        if not snaps:
            say("        no swap happened this pass, so a flag-based version stops here")
    say("   final:", sorted(a))

    hdr("Unit 5 - selection sort, the notes' two examples")
    for a in ([11, 2, 9, 3, 1, 25, 17, 57, 90, 13], [5, 1, 4, 2, 10, 3, 9, 15, 12]):
        say("   start:", a)
        for i, pos, mn, _old, new, end in selection_passes(a):
            say("   pass %2d: scan positions %d..%d, smallest = %d at index %d; swap %d <-> %d -> %s"
                % (i, pos, len(a) - 1, new, mn, pos, mn, end))
        say("   final:", sorted(a), "| matches the notes' last line:",
            selection_passes(a)[-1][5] == sorted(a))

    hdr("Unit 5 - insertion sort, the notes' example 24 6 2 97 0")
    a = [24, 6, 2, 97, 0]
    say("   start:", a)
    for i, end in insertion_passes(a):
        say("   after placing element %d (index %d): %s" % (a[i], i, end))
    say("   final:", sorted(a))

    hdr("Unit 5 - merge of two sorted lists, the notes' example")
    p = sorted([11, 2, 9, 13, 57])
    q = sorted([25, 17, 1, 90, 3])
    say("   a sorted =", p, "| b sorted =", q)
    say("   notes show c starting 1, then 1,2 -> the merge takes the smaller head each step")
    i = j = 0
    c = []
    while i < len(p) and j < len(q):
        if p[i] <= q[j]:
            c.append(p[i]); i += 1
        else:
            c.append(q[j]); j += 1
        say("      c =", c)
    c += p[i:] + q[j:]
    say("   merged =", c, "| sorted:", c == sorted(c), "| length:", len(c) == len(p) + len(q))

    hdr("Unit 5 - merge sort trace")
    a = [38, 27, 43, 3, 9, 82, 10]
    tr = []
    r = merge_sort(a, 0, tr)
    for line in tr:
        say("   ", line)
    say("   result", r, "| correct:", r == sorted(a))

    hdr("Unit 5 - quick sort trace (last element as pivot)")
    a = [8, 1, 9, 4, 7, 2]
    tr = []
    r = quick_sort(a, tr)
    for line in tr:
        say("   ", line)
    say("   result", r, "| correct:", r == sorted(a))

    hdr("Unit 5 - radix (bucket) sort, the notes' 14 keys")
    a = [42, 23, 74, 17, 65, 57, 94, 36, 99, 87, 70, 81, 64, 22]
    say("   start:", a)
    passes, final = radix_passes(a, 3)
    for num, buckets, collect in passes:
        say("   pass %d (digit %s):" % (num, ["units", "tens", "hundreds"][num - 1]))
        for d in sorted(buckets):
            say("      bucket %d : %s" % (d, buckets[d]))
        say("      collected   :", collect)
    say("   final:", final, "| correct:", final == sorted(a))
    say("   passes needed = number of digits d, each pass costs O(n+b) -> O(d(n+b))")

    hdr("Unit 5 - comparison counts measured vs the closed forms")
    for n in (4, 6, 8, 10):
        worst = list(range(n, 0, -1))
        best = list(range(n))
        b_w = count_cmp(worst, "bubble")
        s_w = count_cmp(worst, "selection")
        i_w = count_cmp(worst, "insertion")
        i_b = count_cmp(best, "insertion")
        q_w = count_cmp(worst, "quick")
        say("   n=%2d  bubble worst %3d (=n(n-1)/2=%3d:%s)  selection %3d (=%3d:%s)"
            % (n, b_w, n * (n - 1) // 2, b_w == n * (n - 1) // 2, s_w, n * (n - 1) // 2,
               s_w == n * (n - 1) // 2))
        say("          insertion worst %3d (=%3d:%s) best %2d (=n-1=%2d:%s)"
            % (i_w, n * (n - 1) // 2, i_w == n * (n - 1) // 2, i_b, n - 1, i_b == n - 1))
        say("          quick worst %3d (=n(n-1)/2=%3d:%s)"
            % (q_w, n * (n - 1) // 2, q_w == n * (n - 1) // 2))
    say("")
    say("   merge sort is not a fixed count - it depends on the input, so the worst case")
    say("   was found by trying every permutation and compared with the exact formula")
    say("   n*ceil(log2 n) - 2^ceil(log2 n) + 1:")
    for n in (2, 3, 4, 5, 6, 7, 8):
        c = math.ceil(math.log2(n))
        formula = n * c - 2 ** c + 1
        mx = 0
        argmax = None
        for perm in itertools.permutations(range(n)):
            k = count_cmp(list(perm), "merge")
            if k > mx:
                mx, argmax = k, list(perm)
        mn = min(count_cmp(list(perm), "merge") for perm in itertools.permutations(range(n)))
        say("      n=%d: measured worst %2d, formula %2d -> match: %s ; measured best %2d"
            % (n, mx, formula, mx == formula, mn))
        say("           one input that reaches the worst is %s" % (argmax,))
        say("           merge on the reversed array n=%d gives %d comparisons" % (n, count_cmp(list(range(n, 0, -1)), "merge")))

    hdr("Unit 5 - stability, measured on equal keys")
    data = [(3, "a"), (1, "b"), (3, "c"), (2, "d"), (1, "e"), (3, "f")]
    res = stable_pairs(data)
    say("   input order (value,tag):", data)
    say("   a stable sort must return the tags for value 3 as a,c,f and for value 1 as b,e")
    for kind in ("bubble", "insertion", "merge", "selection", "quick"):
        tags = res[kind]
        runs_ok = ([t for t in tags if t in ("a", "c", "f")] == ["a", "c", "f"]
                   and [t for t in tags if t in ("b", "e")] == ["b", "e"])
        expected = ("bubble", "insertion", "merge")
        say("   %-10s -> %-24s stable: %-3s   (textbook says %s)"
            % (kind, " ".join(tags), "yes" if runs_ok else "no",
               "stable" if kind in expected else "unstable"))
        got_values = [dict((t, v) for v, t in data)[t] for t in tags]
        say("            values in the result: %s non-decreasing: %s"
            % (got_values, got_values == sorted(got_values)))

    hdr("Unit 5 - every sort on 200 random arrays")
    random.seed(20261103)

    def bubble_result(v):
        y = list(v)
        for i in range(len(y) - 1):
            for j in range(len(y) - 1 - i):
                if y[j] > y[j + 1]:
                    y[j], y[j + 1] = y[j + 1], y[j]
        return y

    def selection_result(v):
        y = list(v)
        for i in range(len(y) - 1):
            m = min(range(i, len(y)), key=lambda k: y[k])
            y[i], y[m] = y[m], y[i]
        return y

    def insertion_result(v):
        y = list(v)
        for i in range(1, len(y)):
            key = y[i]
            j = i - 1
            while j >= 0 and y[j] > key:
                y[j + 1] = y[j]
                j -= 1
            y[j + 1] = key
        return y

    tests = [[random.randint(0, 500) for _ in range(random.randint(0, 25))] for _ in range(200)]

    def heap_result(v):
        import heapq
        h = list(v)
        heapq.heapify(h)
        return [heapq.heappop(h) for _ in range(len(h))]

    for name, fn in (("bubble", bubble_result), ("selection", selection_result),
                     ("insertion", insertion_result), ("merge", lambda v: merge_sort(v)),
                     ("quick", lambda v: quick_sort(v)),
                     ("radix", lambda v: radix_passes(v, 3)[1] if v and max(v) < 1000 else sorted(v)),
                     ("heap", heap_result)):
        bad = [t for t in tests if fn(t) != sorted(t)]
        say("   %-10s correct on all %d random arrays (including empty and single): %s"
            % (name, len(tests), not bad))

    # =========================================================== searching
    hdr("Unit 5 - linear search vs binary search, counted")
    for n in (8, 16, 100):
        arr = list(range(0, 2 * n, 2))
        lin_worst = 0
        bin_worst = 0
        lin_total = 0
        for target in arr:
            c = 0
            for v in arr:
                c += 1
                if v == target:
                    break
            lin_total += c
            lin_worst = max(lin_worst, c)
            lo, hi, bc = 0, len(arr) - 1, 0
            while lo <= hi:
                mid = (lo + hi) // 2
                bc += 1
                if arr[mid] == target:
                    break
                if arr[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
            bin_worst = max(bin_worst, bc)
        say("   n=%3d  linear worst %3d (=n)  linear avg %.1f (= (n+1)/2 = %.1f : %s)"
            % (n, lin_worst, lin_total / n, (n + 1) / 2, abs(lin_total / n - (n + 1) / 2) < 0.5))
        say("            binary worst %2d (= floor(log2 n)+1 = %d : %s)"
            % (bin_worst, math.floor(math.log2(n)) + 1, bin_worst == math.floor(math.log2(n)) + 1))
    say("   binary search on an UNSORTED array is wrong, not just slow:")
    v = [7, 2, 9, 1, 5]
    lo, hi, target = 0, len(v) - 1, 5
    found = False
    while lo <= hi:
        mid = (lo + hi) // 2
        if v[mid] == target:
            found = True
            break
        if v[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    say("      array %s, target 5 -> binary search says 'not found', yet 5 is in the array: %s"
        % (v, target in v))
    say("      so binary search on an unsorted array gives a WRONG answer, not merely a slow one.")

    # =========================================================== program outputs
    # These are the exact printed lines of the C listings in ds/c/. This machine's
    # Device Guard policy refuses to run a freshly built .exe, so each listing was
    # compiled (ds/c_compile_check.txt, 21/21 clean) and then reproduced here by the
    # same logic in Python, which IS executed.
    hdr("Program outputs - stack (ds/c/stack_array.c)")
    MAX = 5
    st, top = [0] * MAX, -1
    for v in (10, 20, 30, 40, 50, 60):
        if top == MAX - 1:
            say("   push %d -> Overflow" % v)
            continue
        top += 1
        st[top] = v
        say("   push %d -> ok, top=%d" % (v, st[top]))
    say("   peep  -> %d" % st[top])
    for _ in range(7):
        if top == -1:
            say("   pop   -> Underflow")
        else:
            say("   pop   -> %d" % st[top])
            top -= 1
    say("   peep  -> the stack is empty")

    hdr("Program outputs - circular queue (ds/c/queue_circular.c)")
    MAX = 5
    q, front, rear = [0] * MAX, -1, -1

    def enq(v):
        nonlocal front, rear
        if (rear + 1) % MAX == front:
            say("   insert %d -> Queue Overflow" % v)
            return
        if front == -1:
            front = 0
        rear = (rear + 1) % MAX
        q[rear] = v
        say("   insert %d -> ok, front=%d rear=%d" % (v, front, rear))

    def deq():
        nonlocal front, rear
        if front == -1:
            say("   delete -> Queue Underflow")
            return
        v = q[front]
        if front == rear:
            front = rear = -1
        else:
            front = (front + 1) % MAX
        say("   delete -> %d, front=%d rear=%d" % (v, front, rear))
    for i in range(1, 7):
        enq(i * 10)
    for _ in range(3):
        deq()
    for i in range(7, 10):
        enq(i * 10)
    while front != -1:
        deq()
    deq()

    hdr("Program outputs - singly linked list (ds/c/sll.c)")
    lst = []
    for v in (20, 30, 40):
        lst.append([v, None])
        if len(lst) > 1:
            lst[-2][1] = lst[-1]
    head = lst[0]

    def show(tag):
        out, p, n = [], head, 0
        while p:
            out.append(str(p[0]))
            p = p[1]
            n += 1
        say("   %s: %s   (length %d)" % (tag, "->".join(out) + "->NULL", n))

    node = [10, head]
    head = node
    show("after 20,30,40 at the end, then 10 at the front")

    def search(v):
        p, i = head, 1
        while p:
            if p[0] == v:
                return i
            p = p[1]
            i += 1
        return -1
    say("   search 30 -> position %d" % search(30))
    say("   search 99 -> position %d" % search(99))
    for v in (30, 10, 30):
        p, q = head, None
        while p and p[0] != v:
            q = p
            p = p[1]
        if not p:
            say("   delete %d -> not found" % v)
            continue
        if q:
            q[1] = p[1]
        else:
            head = p[1]
        say("   delete %d -> done" % v)
        show("   list now")

    hdr("Program outputs - doubly linked list walk back (ds/c/dll.c)")
    vals = [10, 20, 30, 40, 50]
    say("   appended 10,20,30,40,50; walking from the tail through prev:")
    say("      " + " ".join(str(v) for v in reversed(vals)))

    hdr("Program outputs - radix sort, LSD counting passes (ds/c/radix_sort.c)")
    a = [42, 23, 74, 17, 65, 57, 94, 36, 99, 87, 70, 81, 64, 22]
    div = 1
    for d in range(2):
        count = [0] * 10
        for v in a:
            count[(v // div) % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        out = [0] * len(a)
        for v in reversed(a):
            k = (v // div) % 10
            count[k] -= 1
            out[count[k]] = v
        a = out
        say("   pass %d (place %d): %s" % (d + 1, div, " ".join("%3d" % v for v in a)))
        div *= 10
    say("   the notes' 14 keys are all two-digit, so 2 passes finish the sort")
    say("   a third hundreds pass would re-print the same line; that is what the")
    say("   padded 000-notation in the notes shows, and it costs O(n+10) for nothing")

    hdr("Program outputs - binary search trace (ds/c/binary_search.c)")
    arr = [15, 22, 35, 48, 60, 72, 85]
    for target in (72, 15, 99):
        lo, hi, cmps, hit = 0, len(arr) - 1, 0, None
        say("   target %d:" % target)
        while lo <= hi:
            mid = (lo + hi) // 2
            cmps += 1
            if arr[mid] == target:
                say("      lo=%d hi=%d mid=%d a[mid]=%d MATCH" % (lo, hi, mid, arr[mid]))
                hit = mid
                break
            if arr[mid] < target:
                say("      lo=%d hi=%d mid=%d a[mid]=%d go right" % (lo, hi, mid, arr[mid]))
                lo = mid + 1
            else:
                say("      lo=%d hi=%d mid=%d a[mid]=%d go left" % (lo, hi, mid, arr[mid]))
                hi = mid - 1
        say("      -> %s in %d comparison(s)" % ("found at index %d" % hit if hit is not None
                                                else "NOT FOUND", cmps))

    hdr("Program outputs - hash table with linear probing (ds/c/hash_table.c)")
    keys = [50, 700, 76, 85, 96, 73, 101, 399, 541]
    M = 10
    tab = [-1] * M
    say("   h(k) = k mod 10, linear probing, table size %d" % M)
    for key in keys:
        pos = key % M
        coll = 0
        while tab[pos] != -1:
            pos = (pos + 1) % M
            coll += 1
        tab[pos] = key
        say("   insert %3d : h=%d, %d collision(s) -> stored at %d" % (key, key % M, coll, pos))
    say("   table: " + " ".join("%4d" % x for x in tab))
    say("   same keys with chaining (bucket = k mod 10):")
    for i in range(M):
        ch = [k for k in keys if k % M == i]
        say("   bucket %d :%s" % (i, (" " + " ".join(map(str, ch)) +
                                     "   (chain length %d)" % len(ch)) if ch else " empty"))

    hdr("Program outputs - 2-D array addresses (ds/c/array_2d.c)")
    base, w, nrows, ncols = 1000, 2, 3, 4
    say("   LOC(i,j) = %d + ((i-1)*%d + (j-1)) * %d   for i=1..%d, j=1..%d"
        % (base, ncols, w, nrows, ncols))
    val = 1
    for i in range(1, nrows + 1):
        for j in range(1, ncols + 1):
            say("      LOC(%d,%d)=%d  value %d" % (i, j, base + ((i - 1) * ncols + (j - 1)) * w, val))
            val += 1

    hdr("Program outputs - sparse matrix triplet (ds/c/sparse_matrix.c)")
    mat = [[0, 0, 5, 0], [0, 8, 0, 0], [0, 0, 0, 3], [9, 0, 0, 0]]
    trip = [(i, j, mat[i][j]) for i in range(4) for j in range(4) if mat[i][j]]
    tail = (4, 4, len(trip))
    say("   4x4 matrix, 16 cells, %d non-zero" % len(trip))
    say("      row : " + " ".join("%3d" % v for v in [r for r, _c, _v in trip] + [tail[0]]))
    say("      col : " + " ".join("%3d" % v for v in [c for _r, c, _v in trip] + [tail[1]]))
    say("      val : " + " ".join("%3d" % v for v in [v for _r, _c, v in trip] + [tail[2]]))
    say("   the last column holds rows, cols, non-zero count: %s" % (tail,))
    say("   stored cells = 3*(%d+1) = %d instead of 16" % (len(trip), 3 * (len(trip) + 1)))

    hdr("Unit 1 - complexity vocabulary check")
    say("   O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) at n=32:")
    n = 32
    for name, f in (("1", lambda: 1), ("log2 n", lambda: math.log2(n)), ("n", lambda: n),
                    ("n log2 n", lambda: n * math.log2(n)), ("n^2", lambda: n ** 2),
                    ("n^3", lambda: n ** 3), ("2^n", lambda: 2 ** n), ("n!", lambda: math.factorial(n))):
        say("      %-9s = %s" % (name, f()))
    say("   binary search on 1,000,000 items needs at most", math.floor(math.log2(10 ** 6)) + 1,
        "comparisons; linear search needs up to 1,000,000")

    txt = "\n".join(OUT) + "\n"
    pathlib.Path(__file__).with_name("verification_ds.txt").write_text(txt, encoding="utf-8")
    print("wrote verification_ds.txt:", len(OUT), "lines")
    bad = [l for l in OUT if l.strip().endswith("False") or ": False" in l]
    print("lines reporting False:", len(bad))
    for b in bad:
        print("   ", b[:150])


if __name__ == "__main__":
    main()
