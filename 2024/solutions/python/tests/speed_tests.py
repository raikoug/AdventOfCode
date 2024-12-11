from timeit import timeit


def split_string_by_half():
    a = 12345678901234567890
    l = len(str(a))
    h = l // 2
    s = str(a)
    b,c = int(s[:h]),int(s[h:])
    
def split_number_by_half():
    a = 12345678901234567890
    l = len(str(a))
    h = l // 2
    b,c = a//(10**h),a%(10**h)

print("split_string_by_half", f"{timeit(split_string_by_half, number=50000000)}")
print("split_number_by_half", f"{timeit(split_number_by_half, number=50000000)}")