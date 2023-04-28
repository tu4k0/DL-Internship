import sys

from application.application.app import CLI

if __name__ == "__main__":
    try:
        cli = CLI()
        cli.run()
    except KeyboardInterrupt:
        sys.exit('Stop collecting info')

