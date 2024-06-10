from src.worker import convert
def main():
    while True:
        usr_input = input("Enter the 한글 to convert (q to quit): ").lower()
        if usr_input.lower() == 'q':
            break
        res = convert(usr_input, sep='.')
        print(res)

if __name__ == '__main__':
    main()
