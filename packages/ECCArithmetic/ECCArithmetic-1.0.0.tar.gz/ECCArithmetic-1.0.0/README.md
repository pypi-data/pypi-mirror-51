# ECCArithmetic

## Installation
```
pip install ECCArithmetic
```

## Generate the Curve
```
from ECCArithmetic.ec import *

Curve = EC(0, 5, 2, 23981)

```

## PickGenerator
```python
from ECCArithmetic.ec import *

Curve = EC(0, 5, 2, 23981)
G = Curve.pickGenerator()

```

## PickPoint
```python
from ECCArithmetic.ec import *

Curve = EC(0, 5, 2, 23981)
P = Curve.pickPoint()
```

## isPointOnEC
Multiplication is realised with the double and add algorithm.
```python
from ECCArithmetic.ec import *

Curve = EC(0, 5, 2, 23981)
G = Curve.isPointOnEC([14967, 14215])
```

## Identity Element
```python
from ECCArithmetic.ec import *

O = ECPt.identity()
```

## Find All Points
```python
from ECCArithmetic.ec import *

Curve = EC(0, 5, 2, 23981)
all = Curve.enumerateAllPoints()

```

## Addition
```python
from ECCArithmetic.ec import *

Curve = EC(0, 5, 2, 23981)
P = Curve.pickPoint()
Q = Curve.pickPoint()

S = P + Q

```

## Subtraction
```python
from ECCArithmetic.ec import *

Curve = EC(0, 5, 2, 23981)
P = Curve.pickPoint()
Q = Curve.pickPoint()

S = P - Q
```

## Multiplication
```python
from ECCArithmetic.ec import *

Curve = EC(0, 5, 2, 23981)
P = Curve.pickPoint()
Q = Curve.pickPoint()

S = P * Q
```
