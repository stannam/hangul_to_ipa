from src.worker import convert


def main(word: str = None) -> None:
    if word is None:
        while True:
            usr_input = input("Enter the 한글 to convert (q to quit): ").lower()
            if usr_input.lower() == 'q':
                break
            res = convert(usr_input, sep='.')
            print(res)
    else:
        return convert(word, sep='.')

if __name__ == '__main__':
    print(main("굳이?"))
