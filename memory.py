import time

class Memory:
    def __init__(self):
        self.max_size = 1000
        self.left = self.max_size
        # list of (name, (start, size))
        self.memory = [('start', (0, 0)), ('end', (self.max_size, 0))]

    def alloc(self, size):
        if size < 1:
            raise ValueError("size_t should be a positive integer")
        if size > self.left:
            print("Out of memory")
            exit(1)

        ptr = hash(time.time())
        for (i, curr) in enumerate(self.memory[:-1]):
            (_, curr), (_, next) = curr, self.memory[i + 1]
            if next[0] - (curr[0] + curr[1]) >= size:
                self.memory.insert(i + 1, (ptr, (curr[0] + curr[1], size)))
                self.left -= size
                return ptr

        self.defragmentation()
        return self.alloc(size)

    def defragmentation(self):
        print("Defragmentation operated\n")
        new = [('start', (0, 0))]
        for i in self.memory[1:-1]:
            (ptr, (_, size)) = i
            (_, (l_start, l_size)) = new[-1]
            new.append((ptr, (l_start + l_size, size)))
        new.append(('end', (self.max_size, 0)))
        self.memory = new

    def free(self, ptr):
        to_remove = None
        for i in self.memory:
            (name, (_, size)) = i
            if name == ptr:
                to_remove = i
                break

        if to_remove == None:
            raise ValueError("bad address for free")

        self.memory.remove(i)
        self.left += size

    def mem(self):
        print(f"Dynamic allocation : {len(self.memory) - 2}, {self.max_size - self.left}")


if __name__ == "__main__":
    mem = Memory()
    a = mem.alloc(111)
    mem.mem()
    b = mem.alloc(222)
    mem.mem()
    c = mem.alloc(333)
    mem.mem()
    mem.free(b)
    mem.mem()
    d = mem.alloc(444)
    mem.mem()
    e = mem.alloc(555)
    mem.mem()