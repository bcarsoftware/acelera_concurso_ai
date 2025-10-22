from subprocess import run

from pyperclip import copy


def gen_secret_key() -> None:
    print("Generating Secret Key...")
    command = ["openssl", "rand", "-base64", "32"]

    result = run(command, capture_output=True, text=True, check=True).stdout
    print("Successfully generated secret key. Here's it:")
    print(result)
    copy(result)
    print("Successfully copied secret key to clipboard!")


if __name__ == '__main__':
    gen_secret_key()
