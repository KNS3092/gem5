CXX = g++
CXXFLAGS = -O0 -std=c++14 -Wall -Wextra -static -fno-tree-vectorize -fno-tree-loop-vectorize -mno-sse -mno-sse2 -mno-sse3 -mno-ssse3 -mno-sse4.1 -mno-sse4.2 -mno-avx -mno-avx2

OBJECTS = sieve
SRC = sieve.cpp

all: $(OBJECTS)

# Rule to create the executable
$(OBJECTS): $(SRC)
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(OBJECTS)

