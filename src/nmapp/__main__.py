import sys
from nmapp import util

def main():
    try:
        nmap_original_output = sys.stdin.read()
        print(util.reformat_to_markdown(nmap_original_output))
        sys.exit(0)
    except SystemExit:
        # Allow explicit sys.exit() to propagate
        raise
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
