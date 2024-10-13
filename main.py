from complex import i

if __name__ == '__main__':
    z = i
    w = pow(z, 2)
    print(w)
    roots = z.roots(2)
    for root in roots:
        print(pow(root, 2))
    print(z.principal_root(2))
