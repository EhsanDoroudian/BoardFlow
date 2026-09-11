from app.clipboard.manager import ClipboardManager


manager = ClipboardManager()

manager.copy_text("Hello from BoardFlow")

print("Text copied to clipboard.")