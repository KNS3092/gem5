# Cross-compiler settings
CXX = aarch64-linux-gnu-g++
CXXFLAGS = -O0 -std=c++14 -Wall -Wextra
LDFLAGS = -static
SRC = randombranches.cpp
TARGET = randombranches

all: $(TARGET)

# Rule to create the static executable directly from the source
$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $@ $<

