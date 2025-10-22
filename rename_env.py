import asyncio
import platform
from os import system


async def command(os_name: str) -> str:
    unix = "cp .env.example .env"
    dos = "Copy-Item .env.example .env"

    return {
        "LINUX": unix,
        "DARWIN": unix,
        "WINDOWS": dos
    }.get(os_name, unix)


async def main():
    print("Env File Renamed Copy")
    os_name = platform.system().upper()
    cmd_text = await command(os_name)
    print("------------------------")
    system(cmd_text)
    print("Env File Renamed!")


if __name__ == '__main__':
    asyncio.run(main())
