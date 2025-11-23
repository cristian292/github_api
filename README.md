1. Create a bash file in /usr/local/bin
  sudo nano /usr/local/bin/github-activity
2. Write this in it
  #!/bin/bash
  python3 /path/to/script.py "$@"
3. Make it executable
  sudo chmod +x /usr/local/bin/github-activity


Now you can run it from anywhere
  example: github-activity kamranahmedse
