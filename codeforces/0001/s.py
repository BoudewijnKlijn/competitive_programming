n, m, a = map(int, input().split())
horizontal = n // a if n % a == 0 else n // a + 1
vertical = m // a if m % a == 0 else m // a + 1
print(horizontal * vertical)