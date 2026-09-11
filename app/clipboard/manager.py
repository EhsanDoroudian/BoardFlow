import subprocess


class ClipboardManager:

    def copy_text(self, text):
        subprocess.run(
            ["wl-copy"],
            input=text,
            text=True,
            check=True,
        )