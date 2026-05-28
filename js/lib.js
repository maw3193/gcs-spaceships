function euclideanDiv(x, y) {
  return Math.sign(y) * Math.floor(x / Math.abs(y));
}

function euclideanMod(x, y) {
  const z = Math.abs(y);
  return ((x % z) + z) % z;
}

function extrapolateTable(idx, table, base=10) {
    var mul = 1;
    // looking like some kind of division with remainder
    // weight from size modifier is:
    // [ 0,  1,   2,   3,     4,     5,      6,      7,       8,       9,        10]
    // [10, 30, 100, 300, 1'000, 3'000, 10'000, 30'000, 100'000, 300'000, 1'000'000]
    // thus, also the imaginary
    // [  -6,   -5,  -4,  -3, -2, -1]
    // [0.01, 0.03, 0.1, 0.3,  1,  3]
    // So, imagine that table was just [10, 30]
    // for 3, 3/2 is 1r1, 10^1 * table[1] = 300
    // for -3, -3/2 is -1r1, ..., 10^-2 * table[1] = 0.3
    // 3/2 to 1r1 is euclideanDiv(3, 2) r 
    const exponent = euclideanDiv(idx, table.length);
    const newIdx = euclideanMod(idx, table.length);
    return table[newIdx] * (base ** exponent);
}

function systemSizeToWeight(sizeModifier) {
    return extrapolateTable(sizeModifier, [10, 30]);
}

