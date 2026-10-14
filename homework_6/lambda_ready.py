# -*- coding: ascii -*-
"""Named lambda calculus interpreter. Python 3.9+, standard library only."""
import argparse
import re
import sys
import unittest
from collections import namedtuple

Var = namedtuple('Var', 'name')
Lam = namedtuple('Lam', 'param body')
App = namedtuple('App', 'func arg')
NAME = re.compile(r'[A-Za-z_][A-Za-z_0-9]*\Z')
TOKEN = re.compile(r'[A-Za-z_][A-Za-z_0-9]*|[\\().]')


def show(t):
    if isinstance(t, Var):
        return t.name
    if isinstance(t, Lam):
        return '(\\{}. {})'.format(t.param, show(t.body))
    return '({} {})'.format(show(t.func), show(t.arg))


class Parser:
    def __init__(self, source):
        source = source.replace(chr(955), '\\')
        self.tokens = []
        self.i = 0
        pos = 0
        while pos < len(source):
            if source[pos].isspace():
                pos += 1
                continue
            match = TOKEN.match(source, pos)
            if match is None:
                raise ValueError('Invalid character at position {}'.format(pos + 1))
            self.tokens.append(match.group())
            pos = match.end()

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self, expected=None):
        token = self.peek()
        if token is None:
            raise ValueError('Unexpected end of input')
        if expected is not None and token != expected:
            raise ValueError('Expected {!r}, got {!r}'.format(expected, token))
        self.i += 1
        return token

    def expr(self):
        if self.peek() == '\\':
            self.take()
            params = []
            while self.peek() is not None and NAME.fullmatch(self.peek()):
                params.append(self.take())
            if not params:
                raise ValueError('A lambda needs at least one parameter')
            self.take('.')
            body = self.expr()
            for param in reversed(params):
                body = Lam(param, body)
            return body
        result = self.atom()
        while self.peek() == '(' or (self.peek() is not None and NAME.fullmatch(self.peek())):
            result = App(result, self.atom())
        return result

    def atom(self):
        if self.peek() == '(':
            self.take('(')
            result = self.expr()
            self.take(')')
            return result
        if self.peek() is not None and NAME.fullmatch(self.peek()):
            return Var(self.take())
        raise ValueError('Expected a variable or parentheses; wrap lambda arguments in parentheses')


def parse(source):
    p = Parser(source)
    result = p.expr()
    if p.peek() is not None:
        raise ValueError('Unexpected token: {!r}'.format(p.peek()))
    return result


def free(t):
    if isinstance(t, Var):
        return {t.name}
    if isinstance(t, Lam):
        return free(t.body) - {t.param}
    return free(t.func) | free(t.arg)


def names(t):
    if isinstance(t, Var):
        return {t.name}
    if isinstance(t, Lam):
        return {t.param} | names(t.body)
    return names(t.func) | names(t.arg)


def replace_free(t, variable, value):
    """Internal substitution: alpha conflicts must be resolved first."""
    if isinstance(t, Var):
        return value if t.name == variable else t
    if isinstance(t, Lam):
        if t.param == variable:
            return t
        return Lam(t.param, replace_free(t.body, variable, value))
    return App(replace_free(t.func, variable, value), replace_free(t.arg, variable, value))


def prepare_alpha(t, variable, value, used):
    """Make ONE necessary alpha rename, or return None."""
    if variable not in free(t):
        return None
    if isinstance(t, Lam):
        if t.param in free(value):
            i = 1
            fresh = '{}_{}'.format(t.param, i)
            while fresh in used:
                i += 1
                fresh = '{}_{}'.format(t.param, i)
            body = replace_free(t.body, t.param, Var(fresh))
            return Lam(fresh, body), 'rename {} to {} to avoid capture'.format(t.param, fresh)
        change = prepare_alpha(t.body, variable, value, used)
        if change is not None:
            return Lam(t.param, change[0]), change[1]
    if isinstance(t, App):
        change = prepare_alpha(t.func, variable, value, used)
        if change is not None:
            return App(change[0], t.arg), change[1]
        change = prepare_alpha(t.arg, variable, value, used)
        if change is not None:
            return App(t.func, change[0]), change[1]
    return None


def step(t, path='root'):
    """Full normal order: leftmost outermost, including lambda bodies."""
    if isinstance(t, App):
        if isinstance(t.func, Lam):
            f = t.func
            change = prepare_alpha(f.body, f.param, t.arg, names(t))
            if change is not None:
                return App(Lam(f.param, change[0]), t.arg), 'alpha', path + ': ' + change[1]
            detail = '{}: replace free {} with {} in {}'.format(path, f.param, show(t.arg), show(f.body))
            return replace_free(f.body, f.param, t.arg), 'beta', detail
        change = step(t.func, path + '.func')
        if change is not None:
            return App(change[0], t.arg), change[1], change[2]
        change = step(t.arg, path + '.arg')
        if change is not None:
            return App(t.func, change[0]), change[1], change[2]
    if isinstance(t, Lam):
        change = step(t.body, path + '.body')
        if change is not None:
            return Lam(t.param, change[0]), change[1], change[2]
    return None


def has_redex(t):
    if isinstance(t, Var):
        return False
    if isinstance(t, Lam):
        return has_redex(t.body)
    return isinstance(t.func, Lam) or has_redex(t.func) or has_redex(t.arg)


def evaluate(source, max_steps=100, emit=print):
    if max_steps < 0:
        raise ValueError('max_steps must be non-negative')
    t = parse(source)
    counts = {'alpha': 0, 'beta': 0}
    emit('0. ' + show(t))
    for i in range(1, max_steps + 1):
        change = step(t)
        if change is None:
            break
        t, rule, detail = change
        counts[rule] += 1
        emit('{}. [{}] {}'.format(i, rule, detail))
        emit('   => ' + show(t))
    done = not has_redex(t)
    emit('NORMAL FORM' if done else 'STEP LIMIT: unfinished (not a proof of divergence)')
    emit('alpha: {}, beta: {}'.format(counts['alpha'], counts['beta']))
    return t, done, counts


EXAMPLES = [
    ('Identity', r'(\x.x) a', 'a'),
    ('First argument', r'(\x.\y.x) a b', 'a'),
    ('Avoid variable capture', r'(\x.\y.x) y', r'\y_1.y'),
    ('Shadowing', r'(\x.\x.x) a', r'\x.x'),
    ('Church TRUE', r'(\t.\f.t) a b', 'a'),
    ('Church FALSE', r'(\t.\f.f) a b', 'b'),
    ('Church 1 + 2 = 3', r'(\m n f x.m f (n f x)) (\f x.f x) (\f x.f (f x))', r'\f x.f (f (f x))'),
    ('Church 2 * 2 = 4', r'(\m n f.m (n f)) (\f x.f (f x)) (\f x.f (f x))', r'\f x.f (f (f (f x)))'),
    ('Reduce inside lambda', r'\x.(\y.y) x', r'\x.x'),
    ('Ignore unused Omega', r'(\x.a) ((\z.z z) (\z.z z))', 'a'),
    ('Omega: stop after 8 steps', r'(\x.x x) (\x.x x)', None),
]


def demo():
    for title, source, expected in EXAMPLES:
        print('\n=== {} ==='.format(title))
        print('Input: ' + source)
        print('Expected: ' + (expected if expected is not None else 'STEP LIMIT'))
        evaluate(source, 8 if expected is None else 100)


def repl():
    print(r'Enter a term, e.g. (\x.x) a. Type quit to exit.')
    while True:
        try:
            source = input('lambda> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if source.lower() in ('quit', 'exit'):
            return
        if not source:
            continue
        try:
            evaluate(source)
        except (ValueError, RecursionError) as error:
            print('ERROR: ' + str(error))


class SelfTests(unittest.TestCase):
    def run_term(self, source, limit=100):
        return evaluate(source, limit, emit=lambda text: None)

    def test_examples(self):
        for title, source, expected in EXAMPLES:
            with self.subTest(title=title):
                t, done, counts = self.run_term(source, 8 if expected is None else 100)
                self.assertEqual(done, expected is not None)
                if expected is not None:
                    self.assertEqual(t, parse(expected))
                else:
                    self.assertEqual(counts['beta'], 8)

    def test_capture_trace(self):
        log = []
        t, done, counts = evaluate(r'(\x.\y.x) y', emit=log.append)
        self.assertEqual(free(t), {'y'})
        self.assertEqual(counts, {'alpha': 1, 'beta': 1})
        self.assertIn('[alpha]', log[1])

    def test_fresh_name(self):
        t, _, _ = self.run_term(r'(\x.\y.x y y_1) y')
        self.assertEqual(t, parse(r'\y_2.y y_2 y_1'))

    def test_nested_shadowing(self):
        t, _, counts = self.run_term(r'(\x.\y.\y.x y) y')
        self.assertEqual(t, parse(r'\y_1.\y_2.y y_2'))
        self.assertEqual(counts['alpha'], 2)

    def test_left_associativity(self):
        self.assertEqual(parse('a b c'), App(App(Var('a'), Var('b')), Var('c')))

    def test_multi_parameters(self):
        self.assertEqual(parse(r'\x y.x y'), parse(r'\x.\y.(x y)'))

    def test_roundtrip(self):
        for _, source, _ in EXAMPLES:
            self.assertEqual(parse(show(parse(source))), parse(source))

    def test_invalid_input(self):
        for source in ('', '()', '(a', 'a)', '\\x.', '\\.x', 'a + b', '1'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                parse(source)

    def test_step_boundary(self):
        self.assertTrue(self.run_term('a', 0)[1])
        self.assertFalse(self.run_term(r'(\x.x) a', 0)[1])
        self.assertTrue(self.run_term(r'(\x.x) a', 1)[1])

    def test_negative_limit(self):
        with self.assertRaises(ValueError):
            self.run_term('a', -1)

    def test_unicode_lambda(self):
        self.assertEqual(parse(chr(955) + 'x.x'), parse(r'\x.x'))


def main():
    parser = argparse.ArgumentParser(description='Lambda calculus interpreter (Python 3.9+)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--self-test', action='store_true')
    group.add_argument('--examples', action='store_true')
    group.add_argument('--expr', help='Evaluate one quoted term')
    group.add_argument('--repl', action='store_true')
    parser.add_argument('--max-steps', type=int, default=100)
    args = parser.parse_args()
    if args.max_steps < 0:
        parser.error('--max-steps must be non-negative')
    if args.self_test:
        print('Python: ' + sys.version.split()[0])
        result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(SelfTests))
        print('ALL TESTS PASSED' if result.wasSuccessful() else 'TESTS FAILED')
        return 0 if result.wasSuccessful() else 1
    if args.examples:
        demo()
    elif args.expr is not None:
        try:
            _, done, _ = evaluate(args.expr, args.max_steps)
            return 0 if done else 2
        except (ValueError, RecursionError) as error:
            print('ERROR: ' + str(error))
            return 1
    elif args.repl:
        repl()
    else:
        print('Lambda Calculus Interpreter')
        print('1. Run examples')
        print('2. Enter your own expression')
        try:
            choice = input('Choose 1 or 2 (Enter = 1): ').strip()
        except (EOFError, KeyboardInterrupt):
            return 0
        repl() if choice == '2' else demo()
    return 0


if __name__ == '__main__':
    sys.exit(main())
