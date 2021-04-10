import sys

if not __package__:
    sys.path[0] = sys.path[0][: sys.path[0].rfind("/")]

import arls


if __name__ == "__main__":
    sys.exit(arls.main())
