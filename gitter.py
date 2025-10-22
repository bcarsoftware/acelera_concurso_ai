from os import system


def line(length: int = 44, char: str = "-") -> None:
    print(char * length)


def main() -> None:
    while True:
        line()

        print("Welcome to Gitter!")

        line()

        print("What would you like to do?")

        line()

        print("1. Create a new repository")

        print("2. Create a new repository and send to GitHub [TODO]")

        print("3. Make a Commit")

        print("4. Make a Push")

        print("5. Make a Pull Request")

        print("6. Add All Files")

        print("7. See Git Status")

        print("8. Make a Pull")

        print("9. Log Out!")

        line()

        option = input("What would you like to do? ")

        if not option.isnumeric():
            continue

        line()

        choice = int(option)

        if choice > 9 or choice < 1:
            continue

        if choice == 9:
            print("Thank you for using Gitter! See you later!")
            line()
            break

        function = {
            1: init_new_repo,
            3: make_a_commit,
            4: make_a_push,
            5: make_pull_request,
            6: add_all_files,
            7: see_status,
            8: make_a_pull,
        }.get(choice, None)

        if function is None:
            return

        function()


def init_new_repo() -> None:
    line()

    command = "git init"

    system(command)

    print("New Git Repository Created!")


def make_a_commit() -> None:
    line()

    print("Making a New Commit")

    line()

    print("1. Feature")
    print("2. Migrate")
    print("3. Chore")
    print("4. Infrastructure")
    print("5. Refactoring")
    print("6. Documentation")
    print("7. Exception")
    print("8. Fix")
    print("9. HotFix")

    line()
    option = input("What would you like to do? ")
    if not option.isnumeric():
        return

    option = int(option)

    if option > 9 or option < 1:
        return

    line()

    cm_type = {
        1: "feat: ",
        2: "migrate: ",
        3: "chore: ",
        4: "infra: ",
        5: "refact: ",
        6: "doc: ",
        7: "except: ",
        8: "fix: ",
        9: "hotfix: ",
    }.get(option)

    message = input("Commit Message: ").strip().lower()

    command = f'git commit -m "{cm_type}{message}"'

    line()

    system(command)


def make_a_push() -> None:
    line()

    command = "git push"

    system(command)


def add_all_files() -> None:
    line()

    command = "git add ."

    system(command)

    print("All Files added!")


def see_status() -> None:
    line()

    command = "git status"

    system(command)


def make_pull_request() -> None:
    line()

    command = "gh pr create"

    system(command)


def make_a_pull() -> None:
    line()

    command = "git pull"

    system(command)


if __name__ == "__main__":
    main()
