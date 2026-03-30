import sys

def main():
    lis = [1, 2, 3]
    lis[len(lis):] = [4]
    unter = [5, 6]
    lis[1] = unter
    unter[0] = 7
    print(lis)

if __name__ == '__main__':
    main()