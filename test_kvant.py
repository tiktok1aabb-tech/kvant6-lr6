#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автопроверка «Квант-6».

    python test_kvant.py        — все главы по порядку
    python test_kvant.py 3      — только глава 3
    python test_kvant.py 1 2 3  — главы 1–3

В PyCharm: правый клик по этому файлу -> Run 'test_kvant'.

Тесты ничего не исправляют и ничего не подсказывают «в лоб»: они говорят,
ЧТО ожидалось и ЧТО получилось, и куда посмотреть в задачнике.
Свой картридж (<номер>.kv6) положите рядом с kvant.py — тесты его найдут.
"""

import base64
import glob
import hashlib
import os
import sys
import traceback
import unittest

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
if os.name == 'nt':
    os.system('')          # включает цвета в консоли Windows

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kvant  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ────────────────────────────────────────────────────────────────────────
#  Эталоны демонстрационного картриджа
# ────────────────────────────────────────────────────────────────────────
DEMO = base64.b64decode('S1ZOVAEACNCU0JXQnNCeAABUAQBsAAcAHNCf0KDQmNCS0JXQoiwg0JrQktCQ0J3Qoi02IQoABjEwISA9IAAPCtCh0J/QmNCh0JrQmDogABwK0KHQkdCe0KDQntCaINCc0KPQodCe0KDQkDogABAsINCX0JDQndCv0KLQnjogAAosINCf0JjQmjogAAEKAAAB7yAAIAERAxIsIAABAAAAAhkpABkBAAAAASwgACAAAQAAAAERKwAIARIsIAEhAwEAAAAAIQEgACkAaQEAAAACMCECIAIBAAAAACAAIAMSMiACAQAAAAEgATIgAiEBIAABAAAAAREhACgANCABLDoAAAEAAAAAIQAgAAEAAAAgGSkBXAEAAAAAIQEgAQEAAAAgGSkBTwEAAAABIQIgAQEAAAAQKwAAAiAAAQAAABArAAACECEDIAMBAAAAqRkpAMUBAAAABiECIAEBAAAACysAAAIgAAEAAAAMKwAAAhABAAAABRkpAOwBAAAAACECIAEBAAAAFSsAAAIgAAEAAAAMKwAAAhABAAAABRkpARMBAAAAACECIAABAAAAERopATsgAwEAAABSGSkBOyADAQAAAC0aKQE7AQAAAAIhAiABIAAgAjsgAQEAAAABECEBKACIIAABAAAAARAhACgAdjoAAQEAAAAKKwAIATg6AAIBAAAAAjAjAAEAAAAAIQAgAAEAAAAMGSkB2QEAAAAGIAABAAAAARArACkCIQEgAQEAAAABMQEAAAAAMTgBAAAAIDkgAAEAAAADFCoBzCIAIAABAAAAAxMBAAAAAhQgATIgAAEAAAABECEAKAF7OgADNAA4OgAENAE4OgAFNAI4OgAGLWKjQ3ZBOttzp+BB/favFpuIJCHvkOUB5AtCu+Q72acH')
DEMO_LISTING = '''L_0000:
  0000  LOAD    0
  0002  LOAD    1
  0004  SUB
  0005  DUP
  0006  MUL
  0007  RET
L_0008:
  0008  LOAD    0
  000A  PUSH    2
  000F  LT
  0010  JZ      L_0019
  0013  PUSH    1
  0018  RET
L_0019:
  0019  LOAD    0
  001B  LOAD    0
  001D  PUSH    1
  0022  SUB
  0023  CALL    L_0008, 1
  0027  MUL
  0028  RET
L_0029:
  0029  LOAD    1
  002B  STORE   3
  002D  PUSH    0
  0032  STORE   1
L_0034:
  0034  LOAD    0
  0036  JZ      L_0069
  0039  PUSH    2
  003E  NEW
  003F  STORE   2
  0041  LOAD    2
  0043  PUSH    0
  0048  LOAD    0
  004A  LOAD    3
  004C  MUL
  004D  SETF
  004E  LOAD    2
  0050  PUSH    1
  0055  LOAD    1
  0057  SETF
  0058  LOAD    2
  005A  STORE   1
  005C  LOAD    0
  005E  PUSH    1
  0063  SUB
  0064  STORE   0
  0066  JMP     L_0034
L_0069:
  0069  LOAD    1
  006B  RET
L_006C:    ; точка входа
  006C  PRINTS  0    ; 'ПРИВЕТ, КВАНТ-6!\\n'
  006F  PUSH    0
  0074  STORE   0
L_0076:
  0076  LOAD    0
  0078  PUSH    32
  007D  LT
  007E  JZ      L_015C
  0081  PUSH    0
  0086  STORE   1
L_0088:
  0088  LOAD    1
  008A  PUSH    32
  008F  LT
  0090  JZ      L_014F
  0093  PUSH    1
  0098  STORE   2
  009A  LOAD    1
  009C  PUSH    16
  00A1  CALL    L_0000, 2
  00A5  LOAD    0
  00A7  PUSH    16
  00AC  CALL    L_0000, 2
  00B0  ADD
  00B1  STORE   3
  00B3  LOAD    3
  00B5  PUSH    169
  00BA  LT
  00BB  JZ      L_00C5
  00BE  PUSH    6
  00C3  STORE   2
L_00C5:
  00C5  LOAD    1
  00C7  PUSH    11
  00CC  CALL    L_0000, 2
  00D0  LOAD    0
  00D2  PUSH    12
  00D7  CALL    L_0000, 2
  00DB  ADD
  00DC  PUSH    5
  00E1  LT
  00E2  JZ      L_00EC
  00E5  PUSH    0
  00EA  STORE   2
L_00EC:
  00EC  LOAD    1
  00EE  PUSH    21
  00F3  CALL    L_0000, 2
  00F7  LOAD    0
  00F9  PUSH    12
  00FE  CALL    L_0000, 2
  0102  ADD
  0103  PUSH    5
  0108  LT
  0109  JZ      L_0113
  010C  PUSH    0
  0111  STORE   2
L_0113:
  0113  LOAD    0
  0115  PUSH    17
  011A  GT
  011B  JZ      L_013B
  011E  LOAD    3
  0120  PUSH    82
  0125  LT
  0126  JZ      L_013B
  0129  LOAD    3
  012B  PUSH    45
  0130  GT
  0131  JZ      L_013B
  0134  PUSH    2
  0139  STORE   2
L_013B:
  013B  LOAD    1
  013D  LOAD    0
  013F  LOAD    2
  0141  PIX
  0142  LOAD    1
  0144  PUSH    1
  0149  ADD
  014A  STORE   1
  014C  JMP     L_0088
L_014F:
  014F  LOAD    0
  0151  PUSH    1
  0156  ADD
  0157  STORE   0
  0159  JMP     L_0076
L_015C:
  015C  PRINTS  1    ; '10! = '
  015F  PUSH    10
  0164  CALL    L_0008, 1
  0168  PRINT
  0169  PRINTS  2    ; '\\nСПИСКИ: '
  016C  PUSH    2
  0171  NEW
  0172  GSTORE  0
  0174  PUSH    0
  0179  STORE   0
L_017B:
  017B  LOAD    0
  017D  PUSH    12
  0182  LT
  0183  JZ      L_01D9
  0186  PUSH    6
  018B  LOAD    0
  018D  PUSH    1
  0192  ADD
  0193  CALL    L_0029, 2
  0197  STORE   1
  0199  LOAD    1
  019B  PUSH    1
  01A0  GETF
  01A1  PUSH    0
  01A6  GETF
  01A7  PRINT
  01A8  PUSH    32
  01AD  PRINTC
  01AE  LOAD    0
  01B0  PUSH    3
  01B5  MOD
  01B6  JNZ     L_01CC
  01B9  GLOAD   0
  01BB  LOAD    0
  01BD  PUSH    3
  01C2  DIV
  01C3  PUSH    2
  01C8  MOD
  01C9  LOAD    1
  01CB  SETF
L_01CC:
  01CC  LOAD    0
  01CE  PUSH    1
  01D3  ADD
  01D4  STORE   0
  01D6  JMP     L_017B
L_01D9:
  01D9  PRINTS  3    ; '\\nСБОРОК МУСОРА: '
  01DC  MEMINFO 0
  01DE  PRINT
  01DF  PRINTS  4    ; ', ЗАНЯТО: '
  01E2  MEMINFO 1
  01E4  PRINT
  01E5  PRINTS  5    ; ', ПИК: '
  01E8  MEMINFO 2
  01EA  PRINT
  01EB  PRINTS  6    ; '\\n'
  01EE  HALT'''
DEMO_OUTPUT = ('ПРИВЕТ, КВАНТ-6!\n10! = 3628800\nСПИСКИ: 2 4 6 8 10 12 14 16 18 20 22 24 \n'
               'СБОРОК МУСОРА: 5, ЗАНЯТО: 75, ПИК: 84\n')
DEMO_OUTPUT_NOLIMIT = DEMO_OUTPUT.replace('СБОРОК МУСОРА: 5, ЗАНЯТО: 75, ПИК: 84',
                                          'СБОРОК МУСОРА: 0, ЗАНЯТО: 219, ПИК: 219')
DEMO_SCREEN = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111166666666611111111111111111111166666666666661111111111111111166666666666666666111111111111116666666666666666666111111111111666666666666666666666111111111116666666666666666666661111111111666666066666666606666661111111116666600066666660006666611111111666660000066666000006666611111116666660006666666000666666111111166666660666666666066666661111111666666666666666666666666611111116666666666666666666666666111111166666666666666666666666661111111666622666666666666622666611111116666226666666666666226666111111166662226666666666622266661111111166662226666666662226666111111111666662226666666222666661111111111666662222222222266666111111111116666662222222226666661111111111116666666662666666666111111111111116666666666666666611111111111111111666666666666611111111111111111111166666666611111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'

# ────────────────────────────────────────────────────────────────────────
#  Маленький ассемблер — чтобы писать тестовые программы словами
# ────────────────────────────────────────────────────────────────────────
OPS = {
    'NOP': (0x00, ''), 'PUSH': (0x01, 'i'), 'POP': (0x02, ''), 'DUP': (0x03, ''), 'SWAP': (0x04, ''),
    'ADD': (0x10, ''), 'SUB': (0x11, ''), 'MUL': (0x12, ''), 'DIV': (0x13, ''), 'MOD': (0x14, ''),
    'NEG': (0x15, ''), 'EQ': (0x18, ''), 'LT': (0x19, ''), 'GT': (0x1A, ''), 'NOT': (0x1B, ''),
    'LOAD': (0x20, 'b'), 'STORE': (0x21, 'b'), 'GLOAD': (0x22, 'b'), 'GSTORE': (0x23, 'b'),
    'JMP': (0x28, 'a'), 'JZ': (0x29, 'a'), 'JNZ': (0x2A, 'a'), 'CALL': (0x2B, 'ab'), 'RET': (0x2C, ''),
    'HALT': (0x2D, ''), 'NEW': (0x30, ''), 'GETF': (0x31, ''), 'SETF': (0x32, ''), 'LEN': (0x33, ''),
    'MEMINFO': (0x34, 'b'), 'PRINT': (0x38, ''), 'PRINTC': (0x39, ''), 'PRINTS': (0x3A, 'w'),
    'PIX': (0x3B, ''), 'ASSERT': (0x3C, 'w'),
}
SIZE = {'i': 4, 'b': 1, 'w': 2, 'a': 2}


def asm(*prog):
    """asm('PUSH 2', 'PUSH 3', 'ADD', 'f:', 'CALL f 1', 'HALT') -> (bytes, {метка: адрес})"""
    items, labels, pc = [], {}, 0
    for line in prog:
        line = line.strip()
        if line.endswith(':'):
            labels[line[:-1]] = pc
            continue
        name, *args = line.split()
        code, form = OPS[name]
        items.append((name, args))
        pc += 1 + sum(SIZE[t] for t in form)
    out = bytearray()
    for name, args in items:
        code, form = OPS[name]
        out.append(code)
        for t, a in zip(form, args):
            v = labels[a] if t == 'a' and a in labels else int(a)
            out += v.to_bytes(SIZE[t], 'big', signed=(t == 'i'))
    return bytes(out), labels


def cart(*prog, heap=1000, nglobals=4, consts=('привет',), entry='main'):
    code, labels = asm(*prog)
    return kvant.Cartridge(owner='ТЕСТ', kind=0, heap=heap, nglobals=nglobals,
                           entry=labels.get(entry, 0), consts=list(consts), code=code)


def file_bytes(owner='ТЕСТ', code=b'\x2D', consts=('a',), magic=b'KVNT', heap=10, entry=0,
               code_len=None, fix_sha=True):
    """Собрать файл картриджа побайтно (для тестов загрузчика)."""
    o = owner.encode()
    b = bytearray(magic + bytes([1, 0, len(o)]) + o + bytes([0]) + heap.to_bytes(2, 'big')
                  + bytes([2]) + entry.to_bytes(2, 'big') + len(consts).to_bytes(2, 'big'))
    for s in consts:
        e = s.encode()
        b += len(e).to_bytes(2, 'big') + e
    b += (len(code) if code_len is None else code_len).to_bytes(4, 'big') + code
    return bytes(b) + (hashlib.sha256(b).digest() if fix_sha else bytes(32))


def vm_of(*prog, no_limit=True, **kw):
    heap = kw.pop('heap', 1000)
    return kvant.VM(cart(*prog, heap=heap, **kw), no_limit=no_limit)


def run(*prog, **kw):
    vm = vm_of(*prog, **kw)
    vm.run(max_steps=100_000)
    return vm


def own_cartridges():
    """Свои картриджи ищем по заголовку файла, не трогая kvant.load студента:
    иначе, пока загрузчик не написан (или в нём ошибка), картридж «не находится»."""
    found = []
    for p in sorted(glob.glob(os.path.join(HERE, '*.kv6'))):
        try:
            with open(p, 'rb') as f:
                data = f.read(512)
        except OSError:
            continue
        if data[:4] != b'KVNT' or len(data) < 8:
            continue
        olen = data[6]
        owner = data[7:7 + olen].decode('utf-8', 'replace')
        kind = data[7 + olen] if len(data) > 7 + olen else -1
        if kind == 0 and owner != 'ДЕМО':
            found.append(p)
    return found


def same_line(t, got, exp, i):
    g = got[i].rstrip() if i < len(got) else '<строки нет>'
    if g != exp[i]:
        t.fail(f'строка {i + 1} листинга\n  ожидалось: {exp[i]!r}\n  получено:  {g!r}')


def code_line(t, vm, prefix, name, err):
    line = next((s for s in vm.output().splitlines() if s.startswith(prefix)), None)
    if line is None:
        t.fail(f'{name}: до строки {prefix} машина не дошла. ' + (f'Остановка: {err}' if err else ''))
    return line


class KvantTest(unittest.TestCase):
    chapter = 0
    title = ''
    maxDiff = 2000

    def vm_error(self, *prog, **kw):
        """Запустить программу и вернуть текст VMError (или провалить тест)."""
        try:
            run(*prog, **kw)
        except kvant.VMError as e:
            return str(e)
        self.fail('ожидалась остановка с VMError, а машина отработала без ошибок')

    def assertErr(self, msg, *needles):
        low = msg.lower()
        for n in needles:
            if n.lower() in low:
                return
        self.fail(f'в сообщении об ошибке нет слов {" / ".join(repr(n) for n in needles)}: {msg!r}')

    def own(self):
        found = own_cartridges()
        if not found:
            self.skipTest('положите свой картридж <номер>.kv6 рядом с kvant.py')
        with open(found[0], 'rb') as f:
            return os.path.basename(found[0]), kvant.load(f.read())


# ════════════════════════════════════════════════════════════════════════
class Ch1Loader(KvantTest):
    chapter, title = 1, 'Загрузчик'

    def test_1_reader(self):
        """Reader читает u8, u16, u32 старшим байтом вперёд
        Подсказка: глава 1, «Порядок байтов». int.from_bytes(b, 'big')."""
        r = kvant.Reader(bytes([1, 2, 3, 4, 5, 6, 7]))
        self.assertEqual(r.u8(), 1)
        self.assertEqual(r.u16(), 0x0203, 'u16 из байтов 02 03 должно быть 515')
        self.assertEqual(r.u32(), 0x04050607)
        self.assertEqual(r.pos, 7, 'курсор должен сдвинуться на 7 байт')

    def test_2_reader_eof(self):
        """Reader.take не читает за концом данных — LoadError
        Подсказка: срез за концом bytes не падает, а тихо возвращает меньше байт — проверьте длину сами."""
        with self.assertRaises(kvant.LoadError):
            kvant.Reader(b'\x01').take(2)

    def test_3_demo_header(self):
        """Заголовок ДЕМО: владелец, тип, куча, глобальные, точка входа
        Подсказка: глава 1, таблица формата и разбор ДЕМО по байтам."""
        c = kvant.load(DEMO)
        self.assertEqual(c.owner, 'ДЕМО')
        self.assertEqual(c.kind, 0)
        self.assertEqual(c.heap, 84)
        self.assertEqual(c.nglobals, 1)
        self.assertEqual(c.entry, 0x6C, 'точка входа ДЕМО — 0x006C')

    def test_4_demo_pool_and_code(self):
        """Пул строк и секция кода ДЕМО
        Подсказка: строки — в UTF-8: bytes.decode('utf-8')."""
        c = kvant.load(DEMO)
        self.assertEqual(len(c.consts), 7)
        self.assertEqual(c.consts[0], 'ПРИВЕТ, КВАНТ-6!\n')
        self.assertEqual(len(c.code), 495)
        self.assertEqual(bytes(c.code[:4]), bytes([0x20, 0x00, 0x20, 0x01]))

    def test_5_bad_checksum(self):
        """Испорченный байт — LoadError (SHA-256 не сходится)
        Подсказка: hashlib.sha256(тело).digest() сравните с последними 32 байтами."""
        bad = bytearray(DEMO)
        bad[300] ^= 0x01
        with self.assertRaises(kvant.LoadError):
            kvant.load(bytes(bad))

    def test_6_bad_magic(self):
        """Чужая сигнатура — LoadError, даже если сумма верна"""
        with self.assertRaises(kvant.LoadError):
            kvant.load(file_bytes(magic=b'KVNX'))

    def test_7_truncated(self):
        """Обрезанный или «врущий» файл — LoadError, а не IndexError
        Подсказка: длина кода в заголовке больше, чем байтов на самом деле."""
        with self.assertRaises(kvant.LoadError):
            kvant.load(DEMO[:30])
        with self.assertRaises(kvant.LoadError):
            kvant.load(file_bytes(code=b'\x2D', code_len=50))

    def test_8_tiny_file(self):
        """Загрузка минимального картриджа, собранного тестом"""
        c = kvant.load(file_bytes(owner='22АБ1', code=b'\x00\x2D', consts=('x', 'юникод'), heap=300, entry=1))
        self.assertEqual((c.owner, c.heap, c.entry, c.consts, bytes(c.code)),
                         ('22АБ1', 300, 1, ['x', 'юникод'], b'\x00\x2D'))


# ════════════════════════════════════════════════════════════════════════
class Ch2Disasm(KvantTest):
    chapter, title = 2, 'Дизассемблер'

    def test_1_decode_push(self):
        """decode: PUSH с положительным и отрицательным числом
        Подсказка: операнд i32 — СО ЗНАКОМ: int.from_bytes(..., 'big', signed=True)."""
        self.assertEqual(kvant.decode(bytes([0x01, 0, 0, 0, 42]), 0), ('PUSH', [42], 5))
        self.assertEqual(kvant.decode(bytes([0x01, 0xFF, 0xFF, 0xFF, 0xF9]), 0), ('PUSH', [-7], 5))

    def test_2_decode_other(self):
        """decode: команды с операндами u8, u16 и с двумя операндами"""
        code = bytes([0x00, 0x20, 0x03, 0x29, 0x01, 0x2C, 0x2B, 0x00, 0x08, 0x02])
        self.assertEqual(kvant.decode(code, 0), ('NOP', [], 1))
        self.assertEqual(kvant.decode(code, 1), ('LOAD', [3], 3))
        self.assertEqual(kvant.decode(code, 3), ('JZ', [300], 6))
        self.assertEqual(kvant.decode(code, 6), ('CALL', [8, 2], 10))

    def test_3_decode_unknown(self):
        """decode: неизвестный код операции — None"""
        self.assertIsNone(kvant.decode(bytes([0x77]), 0))

    def test_4_listing_start(self):
        """Листинг ДЕМО: первые 12 строк
        Подсказка: формат — глава 2: два пробела, адрес из 4 hex-цифр, два пробела, мнемоника шириной 8."""
        got = kvant.disassemble(kvant.load(DEMO)).splitlines()
        exp = DEMO_LISTING.splitlines()
        for i in range(12):
            same_line(self, got, exp, i)

    def test_5_listing_full(self):
        """Листинг ДЕМО совпадает с эталоном строка в строку
        Подсказка: метки ставятся у ВСЕХ адресов переходов и вызовов и у точки входа."""
        got = [s.rstrip() for s in kvant.disassemble(kvant.load(DEMO)).splitlines()]
        exp = DEMO_LISTING.splitlines()
        for i in range(len(exp)):
            same_line(self, got, exp, i)
        if len(got) > len(exp):
            self.fail(f'лишние строки в конце листинга, первая: {got[len(exp)]!r}')


# ════════════════════════════════════════════════════════════════════════
class Ch3Stack(KvantTest):
    chapter, title = 3, 'Стековый интерпретатор'

    def test_01_wrap32(self):
        """wrap32 отбрасывает старшие биты, как int в Java
        Подсказка: глава 3, «Дополнительный код»."""
        for x, e in [(0, 0), (5, 5), (-5, -5), (2**31 - 1, 2**31 - 1), (2**31, -2**31),
                     (2**32, 0), (65536 * 65536, 0), (-2**31 - 1, 2**31 - 1), (3 * 2**32 + 7, 7)]:
            self.assertEqual(kvant.wrap32(x), e, f'wrap32({x})')

    def test_02_java_div(self):
        """Деление и остаток округляются к нулю, а не вниз
        Подсказка: глава 3, «Деление: Python против Java». -7 // 2 в Python даёт -4, а нужно -3."""
        cases = [(7, 2, 3, 1), (-7, 2, -3, -1), (7, -2, -3, 1), (-7, -2, 3, -1), (6, 3, 2, 0),
                 (-2**31, -1, -2**31, 0), (1, 5, 0, 1), (-1, 5, 0, -1)]
        for a, b, q, r in cases:
            self.assertEqual(kvant.java_div(a, b), q, f'java_div({a}, {b})')
            self.assertEqual(kvant.java_mod(a, b), r, f'java_mod({a}, {b})')

    def test_03_div_zero(self):
        """Деление на ноль — VMError, а не ZeroDivisionError"""
        with self.assertRaises(kvant.VMError):
            kvant.java_div(1, 0)

    def test_04_push_halt(self):
        """PUSH кладёт числа, HALT останавливает, счётчик команд считает
        Подсказка: глава 3, «Цикл выборки». steps += 1 на каждую команду, включая HALT."""
        vm = run('PUSH 1', 'PUSH -2', 'PUSH 300', 'HALT')
        self.assertEqual(vm.stack, [1, -2, 300])
        self.assertEqual(vm.steps, 4)
        self.assertTrue(vm.halted)

    def test_05_arith_order(self):
        """ADD/SUB/MUL/DIV/MOD: порядок операндов (вершина — второй)
        Подсказка: «… a b → … a−b»: сначала снимается b, потом a."""
        vm = run('PUSH 10', 'PUSH 3', 'SUB', 'PUSH 4', 'MUL', 'PUSH 5', 'ADD',
                 'PUSH -9', 'PUSH 2', 'DIV', 'PUSH -9', 'PUSH 2', 'MOD', 'HALT')
        self.assertEqual(vm.stack, [33, -4, -1])

    def test_06_overflow(self):
        """32-битное переполнение в ADD, MUL, NEG"""
        vm = run('PUSH 2147483647', 'PUSH 1', 'ADD', 'PUSH 65536', 'PUSH 65536', 'MUL',
                 'PUSH -2147483648', 'NEG', 'PUSH -2147483648', 'PUSH -1', 'DIV', 'HALT')
        self.assertEqual(vm.stack, [-2147483648, 0, -2147483648, -2147483648])

    def test_07_compare(self):
        """EQ, LT, GT, NOT дают числа 1 и 0"""
        vm = run('PUSH 3', 'PUSH 5', 'LT', 'PUSH 3', 'PUSH 5', 'GT', 'PUSH 4', 'PUSH 4', 'EQ',
                 'PUSH 0', 'NOT', 'PUSH 7', 'NOT', 'HALT')
        self.assertEqual(vm.stack, [1, 0, 1, 1, 0])

    def test_08_dup_swap_pop(self):
        """DUP, SWAP, POP"""
        vm = run('PUSH 1', 'PUSH 2', 'SWAP', 'DUP', 'PUSH 9', 'POP', 'HALT')
        self.assertEqual(vm.stack, [2, 1, 1])

    def test_09_vars(self):
        """LOAD/STORE (локальные) и GLOAD/GSTORE (глобальные), начальные значения 0"""
        vm = run('PUSH 5', 'STORE 3', 'LOAD 3', 'LOAD 3', 'MUL', 'GSTORE 1', 'GLOAD 1', 'LOAD 7', 'GLOAD 0', 'HALT')
        self.assertEqual(vm.stack, [25, 0, 0])

    def test_10_jumps(self):
        """JMP, JZ, JNZ: цикл суммирует 1…10
        Подсказка: переход — это просто self.pc = адрес."""
        vm = run('PUSH 0', 'STORE 0', 'PUSH 10', 'STORE 1',
                 'top:', 'LOAD 1', 'JZ end', 'LOAD 0', 'LOAD 1', 'ADD', 'STORE 0',
                 'LOAD 1', 'PUSH 1', 'SUB', 'STORE 1', 'JMP top',
                 'end:', 'LOAD 0', 'PUSH 1', 'JNZ ok', 'PUSH 999', 'ok:', 'HALT')
        self.assertEqual(vm.stack, [55])

    def test_11_print(self):
        """PRINT, PRINTC, PRINTS пишут в vm.out без переводов строк
        Подсказка: используйте готовый метод self.write(текст)."""
        vm = run('PRINTS 0', 'PUSH -42', 'PRINT', 'PUSH 33', 'PRINTC', 'PUSH 1046', 'PRINTC', 'HALT')
        self.assertEqual(vm.output(), 'привет-42!Ж')

    def test_12_errors(self):
        """Ошибки: пустой стек, деление на ноль, ASSERT, нет глобальной, LOAD 16
        Подсказка: глава 3, «Когда машина должна остановиться»."""
        self.assertErr(self.vm_error('POP', 'HALT'), 'стек пуст')
        self.assertErr(self.vm_error('PUSH 1', 'PUSH 0', 'DIV', 'HALT'), 'деление на ноль')
        self.assertErr(self.vm_error('PUSH 0', 'ASSERT 7', 'HALT'), 'ASSERT 7')
        self.assertErr(self.vm_error('GLOAD 9', 'HALT', nglobals=2), 'глобальн')
        self.assertErr(self.vm_error('LOAD 16', 'HALT'), 'локальн', '0…15', '0..15', '15')

    def test_13_error_has_address(self):
        """Сообщение об ошибке содержит адрес и мнемонику: pc=0005 DIV: …"""
        msg = self.vm_error('PUSH 1', 'PUSH 0', 'DIV', 'HALT')
        self.assertIn('pc=000A', msg)
        self.assertIn('DIV', msg)

    def test_14_unknown(self):
        """Неизвестный код операции — «неизвестная команда 0x77»"""
        vm = kvant.VM(kvant.Cartridge('Т', 0, 10, 1, 0, [], bytes([0x77])), no_limit=True)
        with self.assertRaises(kvant.VMError) as cm:
            vm.run()
        self.assertErr(str(cm.exception), 'неизвестная команда 0x77')


# ════════════════════════════════════════════════════════════════════════
class Ch4Calls(KvantTest):
    chapter, title = 4, 'Вызовы функций, массивы и экран'

    def test_01_call_args(self):
        """CALL f, 3: первый положенный аргумент — в L[0]
        Подсказка: глава 4, «CALL по шагам». Снятые со стека значения идут в обратном порядке!"""
        vm = run('f:', 'LOAD 0', 'PUSH 10000', 'MUL', 'LOAD 1', 'PUSH 100', 'MUL', 'ADD', 'LOAD 2', 'ADD', 'RET',
                 'main:', 'PUSH 1', 'PUSH 2', 'PUSH 3', 'CALL f 3', 'HALT')
        self.assertEqual(vm.stack, [10203])
        self.assertEqual(len(vm.frames), 1, 'после RET должен остаться один кадр')

    def test_02_ret_cleans(self):
        """RET убирает всё, что функция оставила выше дна кадра"""
        vm = run('f:', 'PUSH 7', 'PUSH 8', 'PUSH 9', 'PUSH 42', 'RET',
                 'main:', 'PUSH 111', 'CALL f 0', 'HALT')
        self.assertEqual(vm.stack, [111, 42])

    def test_03_base_protects(self):
        """Функция не может снять значения вызывающего — «стек пуст»
        Подсказка: pop() сравнивает высоту стека с self.frame.base."""
        self.assertErr(self.vm_error('f:', 'POP', 'PUSH 0', 'RET', 'main:', 'PUSH 5', 'CALL f 0', 'HALT'), 'стек пуст')

    def test_04_recursion(self):
        """Рекурсия: 10! = 3628800, у каждого вызова свои локальные"""
        vm = run('fact:', 'LOAD 0', 'PUSH 2', 'LT', 'JZ rec', 'PUSH 1', 'RET',
                 'rec:', 'LOAD 0', 'LOAD 0', 'PUSH 1', 'SUB', 'CALL fact 1', 'MUL', 'RET',
                 'main:', 'PUSH 10', 'CALL fact 1', 'HALT')
        self.assertEqual(vm.stack, [3628800])

    def test_05_locals_isolated(self):
        """Вызванная функция не портит L[...] вызывающей"""
        vm = run('f:', 'PUSH 99', 'STORE 5', 'PUSH 0', 'RET',
                 'main:', 'PUSH 7', 'STORE 5', 'CALL f 0', 'POP', 'LOAD 5', 'HALT')
        self.assertEqual(vm.stack, [7])

    def test_06_call_errors(self):
        """RET из главной программы и бесконечная рекурсия — VMError, а не RecursionError
        Подсказка: кадры — это список в вашей машине, а не вызовы функций Python."""
        self.assertErr(self.vm_error('PUSH 1', 'RET'), 'RET из главной', 'главн')
        self.assertErr(self.vm_error('f:', 'CALL f 0', 'RET', 'main:', 'CALL f 0', 'HALT'), 'рекурси', 'кадр')

    def test_07_arrays(self):
        """NEW, LEN, GETF, SETF; новый массив заполнен нулями
        Подсказка: SETF: «… ref i v →» — вершина v, под ней i, ещё ниже ref."""
        vm = run('PUSH 3', 'NEW', 'STORE 0', 'LOAD 0', 'PUSH 2', 'PUSH 77', 'SETF',
                 'LOAD 0', 'LEN', 'LOAD 0', 'PUSH 2', 'GETF', 'LOAD 0', 'PUSH 0', 'GETF', 'HALT')
        self.assertEqual(vm.stack, [3, 77, 0])

    def test_08_array_errors(self):
        """Индекс вне границ, размер 0, число вместо ссылки, ссылка вместо числа"""
        self.assertErr(self.vm_error('PUSH 2', 'NEW', 'PUSH 2', 'GETF', 'HALT'), 'границ', 'индекс')
        self.assertErr(self.vm_error('PUSH 0', 'NEW', 'HALT'), 'размер', 'NEW')
        self.assertErr(self.vm_error('PUSH 5', 'LEN', 'HALT'), 'ссылк')
        self.assertErr(self.vm_error('PUSH 1', 'NEW', 'PUSH 1', 'ADD', 'HALT'), 'числ')

    def test_09_refs(self):
        """Ссылки: EQ по тождественности, ссылка ≠ 0, JNZ на ссылке переходит
        Подсказка: два одинаковых пустых массива — разные объекты (is, а не ==)."""
        vm = run('PUSH 2', 'NEW', 'STORE 0', 'LOAD 0', 'LOAD 0', 'EQ',
                 'LOAD 0', 'PUSH 2', 'NEW', 'EQ', 'LOAD 0', 'PUSH 0', 'EQ',
                 'LOAD 0', 'JNZ yes', 'PUSH 999', 'yes:', 'LOAD 0', 'JZ no', 'PUSH 5', 'no:', 'HALT')
        self.assertEqual(vm.stack, [1, 0, 0, 5])

    def test_10_pix(self):
        """PIX x y c рисует на экране; вне экрана — ошибка"""
        vm = run('PUSH 3', 'PUSH 5', 'PUSH 6', 'PIX', 'PUSH 31', 'PUSH 0', 'PUSH 2', 'PIX', 'HALT')
        self.assertEqual(vm.screen[5][3], 6, 'screen[y][x]: y — строка, x — столбец')
        self.assertEqual(vm.screen[0][31], 2)
        self.assertErr(self.vm_error('PUSH 32', 'PUSH 0', 'PUSH 1', 'PIX', 'HALT'), 'PIX', 'экран')

    def test_11_meminfo(self):
        """Учёт занятости: массив из n элементов — n + 1 слот, MEMINFO 1 и 2"""
        vm = run('PUSH 4', 'NEW', 'POP', 'PUSH 1', 'NEW', 'POP', 'MEMINFO 1', 'MEMINFO 2', 'MEMINFO 3', 'HALT', heap=50)
        self.assertEqual(vm.stack, [7, 7, 50])
        self.assertEqual(vm.heap.allocated, 2)

    def test_12_demo_nolimit(self):
        """ДЕМО без ограничения кучи: вывод и ровно 95113 команд
        Подсказка: если число команд не то — сравните свою трассу (--trace) с листингом."""
        vm = kvant.VM(kvant.load(DEMO), no_limit=True)
        vm.run()
        self.assertEqual(vm.output(), DEMO_OUTPUT_NOLIMIT)
        self.assertEqual(vm.steps, 95113)

    def test_13_demo_screen(self):
        """Экран ДЕМО совпадает с эталоном пиксель в пиксель"""
        vm = kvant.VM(kvant.load(DEMO), no_limit=True)
        vm.run()
        got = ''.join(str(c) for row in vm.screen for c in row)
        bad = [i for i in range(1024) if got[i] != DEMO_SCREEN[i]]
        self.assertFalse(bad, f'не совпадает {len(bad)} пикселей, первый — x={bad[0] % 32 if bad else 0}, y={bad[0] // 32 if bad else 0}')

    def test_14_own_image(self):
        """Ваш картридж: САМОТЕСТ-1 пройден, изображение выведено"""
        name, c = self.own()
        vm = kvant.VM(c, no_limit=True)
        err = ''
        try:
            vm.run()
        except kvant.VMError as e:
            err = str(e)
        out = vm.output()
        self.assertIn('ИЗОБРАЖЕНИЕ ВЫВЕДЕНО', out, f'{name}: машина остановилась раньше: {err or out[-80:]}')


# ════════════════════════════════════════════════════════════════════════
class Ch5Hidden(KvantTest):
    chapter, title = 5, 'Скрытые команды X1–X3'

    def test_1_hidden_defined(self):
        """В HIDDEN описаны все три команды
        Подсказка: глава 5. Начните с выписывания тестов САМОТЕСТ-2 из листинга."""
        if not kvant.HIDDEN:
            raise NotImplementedError('HIDDEN пока пуст')
        missing = [x for x in ('X1', 'X2', 'X3') if x not in kvant.HIDDEN]
        self.assertFalse(missing, f'ещё не разгаданы: {", ".join(missing)}')

    def test_2_hidden_32bit(self):
        """Скрытые команды возвращают 32-битные числа на любых входах"""
        if not kvant.HIDDEN:
            raise NotImplementedError('HIDDEN пока пуст')
        samples = [(0, 0), (1, 1), (-1, 1), (-2**31, 31), (2**31 - 1, 35), (123456789, -987654321), (-100, 40)]
        for x, f in kvant.HIDDEN.items():
            for a, b in samples:
                r = f(a, b)
                self.assertIsInstance(r, int, f'{x}({a}, {b}) вернула {r!r}, а нужно целое число')
                self.assertTrue(-2**31 <= r < 2**31, f'{x}({a}, {b}) = {r} — выходит за 32 бита, нужен wrap32')

    def test_3_own_code1(self):
        """Ваш картридж: САМОТЕСТ-2 пройден, КОД-1 … ПРОВЕРКА: ДА
        Подсказка: если остановка на ASSERT k — найдите ASSERT k в листинге и посмотрите, какие числа проверяются."""
        name, c = self.own()
        vm = kvant.VM(c, no_limit=True)
        err = ''
        try:
            vm.run()
        except kvant.VMError as e:
            err = str(e)
        line = code_line(self, vm, 'КОД-1', name, err)
        self.assertTrue(line.endswith('ДА'), line)


# ════════════════════════════════════════════════════════════════════════
class Ch6Heap(KvantTest):
    chapter, title = 6, 'Куча и сборщик мусора'

    def test_01_trigger_exact(self):
        """Сборка запускается, только когда used + (n+1) > ёмкости — не раньше
        Подсказка: глава 6, правило 3. «>», а не «>=»."""
        vm = run('PUSH 4', 'NEW', 'POP', 'PUSH 4', 'NEW', 'POP', 'MEMINFO 0', 'MEMINFO 1',
                 'PUSH 1', 'NEW', 'POP', 'MEMINFO 0', 'MEMINFO 1', 'HALT', heap=10, no_limit=False)
        self.assertEqual(vm.stack, [0, 10, 1, 2], '[сборок, занято] до и после третьего NEW')

    def test_02_oom(self):
        """Если и после сборки места нет — OUT OF MEMORY"""
        self.assertErr(self.vm_error('PUSH 10', 'NEW', 'HALT', heap=5, no_limit=False), 'OUT OF MEMORY')

    def test_03_garbage_freed(self):
        """Недостижимые объекты освобождаются, счётчики freed и used верны"""
        vm = run('PUSH 3', 'NEW', 'POP', 'PUSH 3', 'NEW', 'POP', 'PUSH 3', 'NEW', 'HALT', heap=8, no_limit=False)
        self.assertEqual((vm.heap.gc_count, vm.heap.freed, vm.heap.used, vm.heap.allocated), (1, 2, 4, 3),
                         '(сборок, освобождено, занято, создано)')

    def test_04_root_stack(self):
        """Корни: объект, лежащий только на стеке, переживает сборку
        Подсказка: если забыть стек, объект освободится прямо посреди вычисления."""
        vm = run('PUSH 3', 'NEW', 'PUSH 3', 'NEW', 'POP', 'PUSH 3', 'NEW', 'POP', 'LEN', 'HALT', heap=8, no_limit=False)
        self.assertEqual(vm.stack, [3])

    def test_05_root_all_frames(self):
        """Корни: локальные ВСЕХ кадров, а не только текущего"""
        vm = run('f:', 'PUSH 3', 'NEW', 'POP', 'PUSH 3', 'NEW', 'POP', 'PUSH 0', 'RET',
                 'main:', 'PUSH 3', 'NEW', 'STORE 4', 'CALL f 0', 'POP', 'LOAD 4', 'LEN', 'HALT', heap=8, no_limit=False)
        self.assertEqual(vm.stack, [3])

    def test_06_root_globals(self):
        """Корни: глобальные переменные"""
        vm = run('PUSH 3', 'NEW', 'GSTORE 2', 'PUSH 3', 'NEW', 'POP', 'PUSH 3', 'NEW', 'POP',
                 'GLOAD 2', 'LEN', 'HALT', heap=8, no_limit=False)
        self.assertEqual(vm.stack, [3])

    def test_07_reachable_inside(self):
        """Достижимость через элементы объектов: корень -> A -> B, B жив"""
        vm = run('PUSH 1', 'NEW', 'STORE 0', 'LOAD 0', 'PUSH 0', 'PUSH 2', 'NEW', 'SETF',
                 'PUSH 2', 'NEW', 'POP', 'PUSH 2', 'NEW', 'POP',
                 'LOAD 0', 'PUSH 0', 'GETF', 'LEN', 'HALT', heap=8, no_limit=False)
        self.assertEqual(vm.stack, [2])
        self.assertGreaterEqual(vm.heap.gc_count, 1)

    def test_08_cycle(self):
        """Кольцо из двух объектов без внешних ссылок — мусор (подсчёт ссылок тут бессилен)
        Подсказка: глава 6, «Почему не подсчёт ссылок»."""
        vm = run('PUSH 1', 'NEW', 'STORE 0', 'PUSH 1', 'NEW', 'STORE 1',
                 'LOAD 0', 'PUSH 0', 'LOAD 1', 'SETF', 'LOAD 1', 'PUSH 0', 'LOAD 0', 'SETF',
                 'PUSH 0', 'STORE 0', 'PUSH 0', 'STORE 1', 'PUSH 4', 'NEW', 'HALT', heap=6, no_limit=False)
        self.assertEqual((vm.heap.gc_count, vm.heap.freed), (1, 2))

    def test_09_freed_is_dead(self):
        """Обращение к освобождённому объекту — VMError
        Подсказка: pop_ref проверяет obj.alive."""
        vm = vm_of('LEN', 'HALT')
        dead = kvant.HeapObject(2)
        dead.alive = False
        vm.stack.append(dead)
        with self.assertRaises(kvant.VMError) as cm:
            vm.run()
        self.assertErr(str(cm.exception), 'освобожд')

    def test_10_log(self):
        """Журнал кучи для графика: события alloc, gc_before, gc_after"""
        vm = run('PUSH 3', 'NEW', 'POP', 'PUSH 3', 'NEW', 'POP', 'PUSH 3', 'NEW', 'HALT', heap=8, no_limit=False)
        kinds = [e[2] for e in vm.heap.log]
        self.assertEqual(kinds, ['alloc', 'alloc', 'gc_before', 'gc_after', 'alloc'])

    def test_11_demo_gc(self):
        """ДЕМО с кучей 84: 5 сборок, пик 84, занято 75, создано 73, освобождено 48"""
        vm = kvant.VM(kvant.load(DEMO))
        vm.run()
        h = vm.heap
        self.assertEqual(vm.output(), DEMO_OUTPUT)
        self.assertEqual((h.gc_count, h.peak, h.used, h.allocated, h.freed), (5, 84, 75, 73, 48),
                         '(сборок, пик, занято, создано, освобождено)')

    def test_12_own_code2(self):
        """Ваш картридж: КОД-2 … ПРОВЕРКА: ДА и послание инженера
        Подсказка: КОД-1 «ДА», а КОД-2 «НЕТ» — ошибка в учёте памяти, а не в командах."""
        name, c = self.own()
        vm = kvant.VM(c)
        err = ''
        try:
            vm.run()
        except kvant.VMError as e:
            err = str(e)
        line = code_line(self, vm, 'КОД-2', name, err)
        self.assertTrue(line.endswith('ДА'), line)


CHAPTERS = [Ch1Loader, Ch2Disasm, Ch3Stack, Ch4Calls, Ch5Hidden, Ch6Heap]
LEVELS = {4: '«3» — машина работает', 5: '«4» — скрытые команды разгаданы', 6: '«5» — память под контролем'}


# ────────────────────────────────────────────────────────────────────────
#  Красивый вывод
# ────────────────────────────────────────────────────────────────────────
USE_COLOR = sys.stdout.isatty() or 'PYCHARM_HOSTED' in os.environ
if os.environ.get('NO_COLOR'):
    USE_COLOR = False


def col(text, code):
    return f'\033[{code}m{text}\033[0m' if USE_COLOR else text


GREEN, RED, YEL, DIM, BOLD = '32', '31', '33', '2', '1'


class Collect(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.items = []

    def addSuccess(self, test):
        self.items.append((test, 'ok', None))

    def addFailure(self, test, err):
        self.items.append((test, 'fail', err))

    def addError(self, test, err):
        kind = 'todo' if issubclass(err[0], NotImplementedError) else 'error'
        self.items.append((test, kind, err))

    def addSkip(self, test, reason):
        self.items.append((test, 'skip', reason))


def describe(test):
    doc = (getattr(test, test._testMethodName).__doc__ or test._testMethodName).strip().splitlines()
    title = doc[0].strip()
    hint = ' '.join(s.strip() for s in doc[1:]).strip()
    return title, hint


def friendly(text):
    """'-4 != -3 : java_div(-7, 2)'  ->  'java_div(-7, 2): получено -4, ожидалось -3'"""
    import re
    m = re.match(r'^(.*?) != (.*?) : (.*)$', text, re.S)
    if m and '\n' not in m.group(1) and '\n' not in m.group(2):
        return f'{m.group(3)}: получено {m.group(1)}, ожидалось {m.group(2)}'
    m = re.match(r'^(False|True) is not (true|false) : (.*)$', text, re.S)
    if m:
        return m.group(3)
    return text


def where(tb):
    for fr in reversed(traceback.extract_tb(tb)):
        if os.path.basename(fr.filename) == 'kvant.py':
            return f'kvant.py, строка {fr.lineno}: {fr.line}'
    return ''


def main(argv):
    wanted = {int(a) for a in argv if a.isdigit()}
    chapters = [c for c in CHAPTERS if not wanted or c.chapter in wanted]
    total = passed = 0
    details_left = 3
    green_upto = 0
    print(col('КВАНТ-6 · автопроверка', BOLD))
    if own_cartridges():
        print(col(f'Ваш картридж: {os.path.basename(own_cartridges()[0])}', DIM))
    else:
        print(col('Свой картридж не найден — положите <номер>.kv6 рядом с kvant.py', YEL))
    all_green_so_far = True
    for cls in chapters:
        res = Collect()
        unittest.TestLoader().loadTestsFromTestCase(cls).run(res)
        oks = sum(1 for _t, k, _e in res.items if k == 'ok')
        todo = sum(1 for _t, k, _e in res.items if k == 'todo')
        n = len(res.items)
        total += n
        passed += oks
        skips = sum(1 for _t, k, _e in res.items if k == 'skip')
        idle = todo and todo + skips == n
        if oks == n:
            mark = col('✔', GREEN)
        elif idle:
            mark = col('○', DIM)
        else:
            mark = col('✘', RED) if oks == 0 else col('◐', YEL)
        status = f'{oks}/{n}'
        if idle:
            first = next(str(e[1]) for _t, k, e in res.items if k == 'todo')
            waits = first.split(':')[0] if first.startswith('Глава') else ''
            status = 'ещё не начата' + (col(f'  (сначала — {first})', DIM) if waits and waits != f'Глава {cls.chapter}' else '')
        print(f'\n{mark} {col(f"Глава {cls.chapter}. {cls.title}", BOLD)}  {status}')
        if idle:
            all_green_so_far = False
            continue
        for test, kind, err in res.items:
            title, hint = describe(test)
            if kind == 'ok':
                print(f'   {col("✔", GREEN)} {title}')
            elif kind == 'todo':
                print(f'   {col("○", DIM)} {title} {col("— TODO: " + str(err[1]), DIM)}')
            elif kind == 'skip':
                print(f'   {col("–", YEL)} {title} {col("(" + str(err) + ")", YEL)}')
            else:
                print(f'   {col("✘", RED)} {title}')
                if details_left > 0:
                    details_left -= 1
                    exc = err[1]
                    if kind == 'fail':
                        msg = friendly(str(exc)).split('\n')
                        print(col('       ' + '\n       '.join(m for m in msg[:8] if m), RED))
                    else:
                        print(col(f'       упало: {type(exc).__name__}: {exc}', RED))
                        w = where(err[2])
                        if w:
                            print(col(f'       где: {w}', RED))
                    if hint:
                        print(col(f'       {hint}', YEL))
        if all_green_so_far and oks == n and not any(k == 'skip' for _t, k, _e in res.items):
            green_upto = cls.chapter
        else:
            all_green_so_far = False
    bar_len = 30
    filled = round(bar_len * passed / total) if total else 0
    print('\n' + col('█' * filled, GREEN) + col('░' * (bar_len - filled), DIM) + f'  {passed} из {total} проверок')
    if not wanted:
        lvl = max((k for k in LEVELS if green_upto >= k), default=None)
        if lvl:
            print(col(f'Уровень по тестам: {LEVELS[lvl]} (его ещё нужно подтвердить на защите)', GREEN))
        else:
            print('Уровень «3» засчитывается по тестам, когда пройдены главы 1–4.')
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
