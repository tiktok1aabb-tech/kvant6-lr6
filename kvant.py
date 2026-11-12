# ЛР №6. Виртуальная машина «Квант-6». Главы 1–7.
import hashlib
import math
import os
import sys
import time
class LoadError(Exception):
    pass

class VMError(Exception):
    pass

# ГЛАВА 1. Загрузчик — читаем картридж и проверяем SHA-256.
class Cartridge:
    def __init__(self, owner, kind, heap, nglobals, entry,
                 consts=None, code=b'', version=(1, 0)):
        self.owner, self.kind = owner, kind
        self.heap, self.nglobals, self.entry = heap, nglobals, entry
        self.consts = [] if consts is None else consts
        self.code, self.version = code, version
class Reader:
    def __init__(self, data): self.data, self.pos = data, 0
    def take(self, n):
        if n < 0 or self.pos + n > len(self.data):
            raise LoadError('не хватает байтов в картридже')
        part = self.data[self.pos:self.pos + n]
        self.pos += n
        return part
    def u8(self): return self.take(1)[0]
    def u16(self): return int.from_bytes(self.take(2), 'big')
    def u32(self): return int.from_bytes(self.take(4), 'big')
def load(data):
    if len(data) < 36: raise LoadError('слишком короткий файл')
    if data[:4] != b'KVNT': raise LoadError('неверная сигнатура KVNT')
    body, check = data[:-32], data[-32:]
    if hashlib.sha256(body).digest() != check:
        raise LoadError('контрольная сумма SHA-256 не совпадает')
    r = Reader(body)
    try:
        r.take(4)
        version = (r.u8(), r.u8())
        if version != (1, 0): raise LoadError('неподдерживаемая версия формата')
        owner = r.take(r.u8()).decode('utf-8')
        kind, heap, count_globals = r.u8(), r.u16(), r.u8()
        entry, count = r.u16(), r.u16()
        strings = []
        for i in range(count): strings.append(r.take(r.u16()).decode('utf-8'))
        code = r.take(r.u32())
        if r.pos != len(body): raise LoadError('неверная длина секций картриджа')
        if entry >= len(code): raise LoadError('точка входа за пределами кода')
    except (UnicodeDecodeError, ValueError) as error:
        raise LoadError('повреждённый формат: ' + str(error))
    return Cartridge(owner, kind, heap, count_globals, entry, strings, code, version)

# ГЛАВА 2. Таблица команд и дизассемблер.
OPCODES = {
    0x00: ('NOP', ''), 0x01: ('PUSH', 'i'), 0x02: ('POP', ''),
    0x03: ('DUP', ''), 0x04: ('SWAP', ''),
    0x10: ('ADD', ''), 0x11: ('SUB', ''), 0x12: ('MUL', ''),
    0x13: ('DIV', ''), 0x14: ('MOD', ''), 0x15: ('NEG', ''),
    0x18: ('EQ', ''), 0x19: ('LT', ''), 0x1A: ('GT', ''), 0x1B: ('NOT', ''),
    0x20: ('LOAD', 'b'), 0x21: ('STORE', 'b'),
    0x22: ('GLOAD', 'b'), 0x23: ('GSTORE', 'b'),
    0x28: ('JMP', 'a'), 0x29: ('JZ', 'a'), 0x2A: ('JNZ', 'a'),
    0x2B: ('CALL', 'ab'), 0x2C: ('RET', ''), 0x2D: ('HALT', ''),
    0x30: ('NEW', ''), 0x31: ('GETF', ''), 0x32: ('SETF', ''),
    0x33: ('LEN', ''), 0x34: ('MEMINFO', 'b'),
    0x38: ('PRINT', ''), 0x39: ('PRINTC', ''), 0x3A: ('PRINTS', 'w'),
    0x3B: ('PIX', ''), 0x3C: ('ASSERT', 'w'),
    0x40: ('X1', ''), 0x41: ('X2', ''), 0x42: ('X3', '')
}
def decode(code, pc):
    if pc < 0 or pc >= len(code) or code[pc] not in OPCODES: return None
    name, form = OPCODES[code[pc]]
    args, pos = [], pc + 1
    for letter in form:
        size = 4 if letter == 'i' else 1 if letter == 'b' else 2
        if pos + size > len(code):
            raise VMError(f'pc={pc:04X}: обрезанная команда {name}')
        args.append(int.from_bytes(code[pos:pos + size], 'big', signed=letter == 'i'))
        pos += size
    return name, args, pos
def disassemble(cart):
    commands, labels = [], {cart.entry}
    pc = 0
    while pc < len(cart.code):
        d = decode(cart.code, pc)
        if d is None:
            commands.append((pc, '??', [cart.code[pc]]))
            pc += 1
            continue
        name, args, end = d
        form = OPCODES[cart.code[pc]][1]
        for i in range(len(form)):
            if form[i] == 'a': labels.add(args[i])
        commands.append((pc, name, args))
        pc = end
    lines = []
    for pc, name, args in commands:
        if pc in labels:
            label = f'L_{pc:04X}:'
            if pc == cart.entry: label += '    ; точка входа'
            lines.append(label)
        if name == '??':
            lines.append(f'  {pc:04X}  ??      0x{args[0]:02X}')
            continue
        form = OPCODES[cart.code[pc]][1]
        values = []
        for i in range(len(args)): values.append(f'L_{args[i]:04X}' if form[i] == 'a' else str(args[i]))
        line = f'  {pc:04X}  {name:<8}{", ".join(values)}'.rstrip()
        if name == 'PRINTS' and 0 <= args[0] < len(cart.consts): line += f'    ; {cart.consts[args[0]]!r}'
        lines.append(line)
    return '\n'.join(lines)

# ГЛАВА 3. Целые 32-битные числа, стек и арифметика.
def wrap32(x):
    x = x & 0xFFFFFFFF
    return x - 4294967296 if x >= 2147483648 else x
def java_div(a, b):
    if b == 0:
        raise VMError('деление на ноль')
    result = abs(a) // abs(b)
    return wrap32(-result if (a < 0) != (b < 0) else result)
def java_mod(a, b): return wrap32(a - b * java_div(a, b))

# ГЛАВА 5. Три скрытые команды индивидуального картриджа.
def x1(a, b): return wrap32(abs(a - b))
def x2(a, b): return wrap32(max(a, b))
def x3(a, b): return wrap32(math.gcd(a, b))
HIDDEN = {'X1': x1, 'X2': x2, 'X3': x3}
# ГЛАВЫ 4 И 6. Объекты в куче и сборщик мусора.
class HeapObject:
    def __init__(self, n, fill=0):
        self.items = [fill] * n
        self.alive, self.marked = True, False
    def __repr__(self): return f'<объект[{len(self.items)}]{"" if self.alive else " освобождён"}>'
class Heap:
    def __init__(self, capacity, no_limit=False):
        self.capacity, self.no_limit = capacity, no_limit
        self.objects, self.log = [], []
        self.used = self.peak = self.gc_count = 0
        self.allocated = self.freed = 0
    def alloc(self, n, vm, fill=0):
        if not isinstance(n, int) or not 1 <= n <= 4096: raise VMError('недопустимый размер массива NEW')
        cost = n + 1  # элементам нужен ещё один слот служебной информации
        if not self.no_limit and self.used + cost > self.capacity:
            self.collect(vm)
            if self.used + cost > self.capacity: raise VMError('OUT OF MEMORY')
        obj = HeapObject(n, fill)
        self.objects.append(obj)
        self.used += cost
        self.allocated += 1
        self.peak = max(self.peak, self.used)
        self.log.append((vm.steps, self.used, 'alloc'))
        return obj
    def collect(self, vm):
        self.gc_count += 1
        self.log.append((vm.steps, self.used, 'gc_before'))
        todo = [v for v in vm.roots() if isinstance(v, HeapObject) and v.alive]
        while todo:
            obj = todo.pop()
            if obj.marked: continue
            obj.marked = True
            for v in obj.items:
                if isinstance(v, HeapObject) and v.alive and not v.marked: todo.append(v)
        live = []
        for obj in self.objects:
            if obj.marked:
                obj.marked = False
                live.append(obj)
            else:
                obj.alive = False
                self.used -= len(obj.items) + 1
                self.freed += 1
        self.objects = live
        self.log.append((vm.steps, self.used, 'gc_after'))
class Frame:
    def __init__(self, ret, base):
        self.ret, self.base = ret, base
        self.locals = [0] * 16
# ГЛАВЫ 3 И 4. Выполнение команд картриджа.
class VM:
    def __init__(self, cart, hidden=None, heap_capacity=None,
                 no_limit=False, echo=False, trace=False):
        self.cart, self.code, self.pc = cart, cart.code, cart.entry
        self.stack, self.frames = [], [Frame(-1, 0)]
        self.globals = [0] * cart.nglobals
        self.heap = Heap(cart.heap if heap_capacity is None else heap_capacity, no_limit)
        self.screen = [[0] * 32 for i in range(32)]
        self.out, self.decoded = [], {}  # Глава 7: кэш декодированных команд
        self.steps, self.halted = 0, False
        self.echo, self.trace = echo, trace
        self.hidden = HIDDEN if hidden is None else hidden
    def push(self, value):
        if len(self.stack) >= 1024: raise VMError('переполнение стека')
        self.stack.append(value)
    def pop(self):
        if len(self.stack) <= self.frames[-1].base: raise VMError('стек пуст')
        return self.stack.pop()
    def pop_int(self):
        value = self.pop()
        if not isinstance(value, int): raise VMError('ожидалось число')
        return value
    def pop_ref(self):
        value = self.pop()
        if not isinstance(value, HeapObject): raise VMError('ожидалась ссылка')
        if not value.alive: raise VMError('обращение к освобождённому объекту')
        return value
    def roots(self):
        values = self.stack + self.globals
        for frame in self.frames: values += frame.locals
        return values
    def write(self, text):
        self.out.append(text)
        if self.echo: print(text, end='', flush=True)
    def output(self): return ''.join(self.out)
    def trace_line(self):
        d = decode(self.code, self.pc)
        name = '??' if d is None else (d[0] + ' ' + ', '.join(map(str, d[1]))).strip()
        values = ', '.join(str(v) for v in self.stack[-6:])
        return f'{self.steps:>8}  {self.pc:04X}  {name:<18} стек: [{values}]'
    def stats(self):
        h = self.heap
        return ('=== СТАТИСТИКА ===\n'
                f'команд выполнено:     {self.steps}\n'
                f'сборок мусора:        {h.gc_count}\n'
                f'пик / ёмкость кучи:   {h.peak} / {h.capacity}\n'
                f'занято в конце:       {h.used}\n'
                f'объектов создано:     {h.allocated}\n'
                f'объектов освобождено: {h.freed}\n')
    def run(self, max_steps=200_000_000):
        step = self.step  # Глава 7: не искать метод заново на каждом шаге
        while not self.halted:
            if self.steps >= max_steps: raise VMError('слишком много шагов — похоже на бесконечный цикл')
            if self.trace: print(self.trace_line(), file=sys.stderr)
            step()
    def step(self):
        pc = self.pc
        d = self.decoded.get(pc)
        if d is None: d = self.decoded[pc] = decode(self.code, pc)
        if d is None:
            byte = self.code[pc] if 0 <= pc < len(self.code) else 255
            raise VMError(f'pc={pc:04X}: неизвестная команда 0x{byte:02X}')
        name, args, self.pc = d
        self.steps += 1
        try:
            if name == 'NOP': pass
            elif name == 'PUSH': self.push(args[0])
            elif name == 'POP': self.pop()
            elif name == 'DUP':
                v = self.pop()
                self.push(v)
                self.push(v)
            elif name == 'SWAP':
                b, a = self.pop(), self.pop()
                self.push(b)
                self.push(a)
            elif name in ('ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'LT', 'GT'):
                b, a = self.pop_int(), self.pop_int()
                if name == 'ADD': v = wrap32(a + b)
                elif name == 'SUB': v = wrap32(a - b)
                elif name == 'MUL': v = wrap32(a * b)
                elif name == 'DIV': v = java_div(a, b)
                elif name == 'MOD': v = java_mod(a, b)
                elif name == 'LT': v = int(a < b)
                else: v = int(a > b)
                self.push(v)
            elif name == 'NEG': self.push(wrap32(-self.pop_int()))
            elif name == 'NOT': self.push(int(self.pop_int() == 0))
            elif name == 'EQ':
                b, a = self.pop(), self.pop()
                self.push(int(a == b if isinstance(a, int) and isinstance(b, int) else a is b))
            elif name in ('LOAD', 'STORE', 'GLOAD', 'GSTORE'):
                i = args[0]
                cells = self.globals if name.startswith('G') else self.frames[-1].locals
                if i >= len(cells): raise VMError('нет такой глобальной переменной' if name.startswith('G') else 'нет такой локальной переменной')
                if name.endswith('LOAD'): self.push(cells[i])
                else: cells[i] = self.pop()
            elif name == 'JMP': self.pc = args[0]
            elif name in ('JZ', 'JNZ'):
                v = self.pop()
                is_zero = isinstance(v, int) and v == 0
                if (name == 'JZ' and is_zero) or (name == 'JNZ' and not is_zero): self.pc = args[0]
            elif name == 'CALL':
                address, count = args
                if count > 16: raise VMError('слишком много аргументов для кадра')
                if len(self.frames) >= 256: raise VMError('слишком глубокая рекурсия')
                values = []
                for i in range(count): values.insert(0, self.pop())
                frame = Frame(self.pc, len(self.stack))
                frame.locals[:count] = values
                self.frames.append(frame)
                self.pc = address
            elif name == 'RET':
                if len(self.frames) == 1: raise VMError('RET из главной программы')
                result = self.pop()
                frame = self.frames.pop()
                del self.stack[frame.base:]
                self.pc = frame.ret
                self.push(result)
            elif name == 'HALT': self.halted = True
            elif name == 'NEW': self.push(self.heap.alloc(self.pop_int(), self))
            elif name in ('GETF', 'SETF'):
                value = self.pop() if name == 'SETF' else None
                i = self.pop_int()
                obj = self.pop_ref()
                if not 0 <= i < len(obj.items): raise VMError('индекс вне границ массива')
                if name == 'GETF': self.push(obj.items[i])
                else: obj.items[i] = value
            elif name == 'LEN': self.push(len(self.pop_ref().items))
            elif name == 'MEMINFO':
                h = self.heap
                values = [h.gc_count, h.used, h.peak, h.capacity]
                if args[0] >= len(values): raise VMError('неверный номер параметра MEMINFO')
                self.push(values[args[0]])
            elif name == 'PRINT': self.write(str(self.pop_int()))
            elif name == 'PRINTC':
                n = self.pop_int()
                if not 0 <= n <= 0x10FFFF: raise VMError('неверный код символа')
                self.write(chr(n))
            elif name == 'PRINTS':
                if args[0] >= len(self.cart.consts): raise VMError('нет такой строки')
                self.write(self.cart.consts[args[0]])
            elif name == 'ASSERT':
                if self.pop_int() == 0: raise VMError(f'ASSERT {args[0]}: тест не пройден')
            elif name == 'PIX':
                color, y, x = self.pop_int(), self.pop_int(), self.pop_int()
                if not (0 <= x < 32 and 0 <= y < 32 and 0 <= color < 8): raise VMError('PIX: координаты или цвет вне экрана')
                self.screen[y][x] = color
            elif name in ('X1', 'X2', 'X3'):
                if name not in self.hidden: raise VMError('неизвестная команда')
                b, a = self.pop_int(), self.pop_int()
                self.push(wrap32(self.hidden[name](a, b)))
            else: raise VMError('неизвестная команда')
        except VMError as error:
            raise VMError(f'pc={pc:04X} {name}: {error}') from error

# Запуск программы, сохранение экрана и графика.
COLORS = [
    (0, 0, 0), (59, 91, 219), (194, 59, 34), (143, 63, 160),
    (47, 158, 68), (35, 166, 201), (232, 197, 71), (242, 242, 238)
]
BENCH_EXPECTED = ('БЕНЧМАРК: КОЛЛАЦ, N = 5000\n'
                  'ЛУЧШЕЕ n = 3711, ДЛИНА = 237\n'
                  'СУММА ДЛИН = 387940\n')
def cartridge(file):
    with open(file, 'rb') as f:
        return load(f.read())
def save_png(screen, file):
    from PIL import Image
    image = Image.new('RGB', (32, 32))
    image.putdata([COLORS[screen[y][x]] for y in range(32) for x in range(32)])
    image.resize((320, 320), Image.Resampling.NEAREST).save(file)
    print('Экран сохранён:', file)
def plot_heap(log, capacity, file):
    import matplotlib.pyplot as plt
    if not log:
        return
    plt.figure(figsize=(10, 4))
    plt.plot([a for a, b, c in log], [b for a, b, c in log],
             linewidth=0.8, label='Занято слотов')
    plt.axhline(capacity, linestyle='--', color='gray', label='Ёмкость кучи')
    for event, color in [('gc_before', 'red'), ('gc_after', 'green')]:
        points = [(a, b) for a, b, c in log if c == event]
        plt.scatter([a for a, b in points], [b for a, b in points],
                    s=12, c=color)
    plt.xlabel('Номер команды')
    plt.ylabel('Занято слотов')
    plt.title('Память виртуальной машины Квант-6')
    plt.legend()
    plt.tight_layout()
    plt.savefig(file)
    plt.close()
    print('График кучи сохранён:', file)

def cmd_info(file):
    c = cartridge(file)
    print('Картридж:', c.owner)
    print('Версия:', str(c.version[0]) + '.' + str(c.version[1]))
    print('Тип картриджа:', c.kind)
    print('Ёмкость кучи:', c.heap)
    print('Глобальных переменных:', c.nglobals)
    print('Точка входа:', c.entry)
    print('Длина кода:', len(c.code))
    print('SHA-256: совпадает')
    for i in range(len(c.consts)): print(i, repr(c.consts[i]))

def cmd_dis(file, output=None):
    result = disassemble(cartridge(file))
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        print('Листинг сохранён:', output)
    else: print(result)

def cmd_run(file, no_limit=False, heap=None, out='out', trace=False):
    c = cartridge(file)
    vm = VM(c, no_limit=no_limit, heap_capacity=heap, trace=trace, echo=True)
    start = time.perf_counter()
    try:
        vm.run()
    except VMError as error:
        print('ОШИБКА VM:', error)
    print('\n' + vm.stats())
    print('время:', round(time.perf_counter() - start, 2), 'с')
    os.makedirs(out, exist_ok=True)
    save_png(vm.screen, os.path.join(out, 'screen_' + c.owner + '.png'))
    if vm.heap.log and not no_limit:
        plot_heap(vm.heap.log, vm.heap.capacity,
                  os.path.join(out, 'heap_' + c.owner + '.png'))

def calibrate(n=1500000):
    stack, x = [], 1
    start = time.perf_counter()
    for i in range(n):
        stack.append(i)
        stack.append(x)
        b, a = stack.pop(), stack.pop()
        x = (a + b if i % 2 == 0 else a ^ b) & 65535
    return n / (time.perf_counter() - start)

def cmd_bench(file, profile=False):
    vm = VM(cartridge(file))
    if profile:
        import cProfile
        profiler = cProfile.Profile()
        profiler.enable()
    start = time.perf_counter()
    try: vm.run()
    except VMError as error:
        print('ОШИБКА VM:', error)
        return
    finally:
        if profile: profiler.disable()
    sec = time.perf_counter() - start
    if profile:
        import pstats
        pstats.Stats(profiler).sort_stats('tottime').print_stats(12)
    print(vm.output(), end='')
    good = vm.output() == BENCH_EXPECTED
    speed = vm.steps / sec
    print('команд:', vm.steps, 'время:', round(sec, 2), 'с',
          'скорость:', round(speed), 'команд/с')
    print('ответ верный:', 'ДА' if good else 'НЕТ')
    if good: print('КВАНТ-ИНДЕКС:', round(speed / calibrate() * 1000))

def start():
    args = sys.argv[1:]
    if not args:
        args = ['run', os.path.join(os.path.dirname(__file__), '25КИ318.kv6')]
        print('Запускаю твой картридж 25КИ318.kv6')
    if len(args) < 2:
        print('Пример: python kvant.py run "25КИ318.kv6"')
        return
    command, file = args[:2]
    try:
        if command == 'info': cmd_info(file)
        elif command == 'dis':
            output = args[args.index('-o') + 1] if '-o' in args else None
            cmd_dis(file, output)
        elif command == 'run':
            folder = args[args.index('--out') + 1] if '--out' in args else 'out'
            size = int(args[args.index('--heap') + 1]) if '--heap' in args else None
            cmd_run(file, '--no-limit' in args, size, folder, '--trace' in args)
        elif command == 'bench':
            cmd_bench(file, '--profile' in args)
        else: print('Неизвестная команда:', command)
    except (LoadError, VMError, FileNotFoundError, ValueError) as error:
        print('Ошибка:', error)
if __name__ == '__main__':
    start()
