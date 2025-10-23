import asyncio
import platform
from os import system


async def command(os_name: str) -> str:
    unix = "cp cors_origins.example.txt cors_origins.txt"
    dos = "Copy-Item cors_origins.example.txt cors_origins.txt"

    return {
        "LINUX": unix,
        "DARWIN": unix,
        "WINDOWS": dos
    }.get(os_name, unix)


async def main():
    print("Cors Origins Renamed Copy")
    os_name = platform.system().upper()
    cmd_text = await command(os_name)
    print("------------------------")
    system(cmd_text)
    print("Cors Origins Renamed!")


if __name__ == '__main__':
    asyncio.run(main())
