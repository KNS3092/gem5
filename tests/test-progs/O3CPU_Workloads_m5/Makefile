CXX = g++
CXXFLAGS = -O0 -std=c++14 -Wall -Wextra -static -fno-tree-vectorize -fno-tree-loop-vectorize -mno-sse -mno-sse2 -mno-sse3 -mno-ssse3 -mno-sse4.1 -mno-sse4.2 -mno-avx -mno-avx2
CFLAGS = -I/home/kshroff/gem5/include -I/home/kshroff/gem5/include/gem5/
LDFLAGS = -L/home/kshroff/gem5/util/m5/build/x86/out -lm5

OBJECTS = randombranches
SRC = randombranches.cpp

all: $(OBJECTS)

# Rule to create the executable
$(OBJECTS): $(SRC)
	$(CXX) $(CXXFLAGS) $(CFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f $(OBJECTS)

