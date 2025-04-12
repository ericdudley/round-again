import os
import argparse
import subprocess
from app import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Round Again",
        description="Relationship management application",
    )
    parser.add_argument(
        "--tailwind",
        action="store_true",
        help="Run the Tailwind CLI in watch mode",
    )
    args = parser.parse_args()

    if args.tailwind:
        print("Starting tailwindcss process in watch mode...")
        tailwind_process = subprocess.Popen(
            [
                "npm",
                "run",
                "watch"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))