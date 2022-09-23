import tkinter as tk
from tkinter import DISABLED, NORMAL as ENABLED
from typing import Optional


class AlwaysOnTopTextDisplay(tk.Toplevel):
    _text_component: tk.Text
    _text: str

    def __init__(self, master, *args, **kwargs) -> None:
        super(AlwaysOnTopTextDisplay, self).__init__(master, *args, **kwargs)
        self._text_component = tk.Text(self)
        self._text = ""

        self.attributes("-topmost", "true")
        self._text_component.pack()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self._text_component.config(state=ENABLED)
        self._text_component.delete(1.0, "end")
        self._text_component.insert("end", text)
        self._text_component.config(state=DISABLED)


class WITClipboardMonitor(tk.Frame):
    _display_window: Optional[AlwaysOnTopTextDisplay]
    _last_clipboard: str

    def __init__(self, master, *args, **kwargs):
        super(WITClipboardMonitor, self).__init__(master, *args, **kwargs)
        self._display_window = None
        self._last_clipboard = self._get_clipboard_content()

        self.pack()
        info_label = tk.Label(self, text="You can now minimize this window.")
        info_label.pack()

        self.after(250, self._check_clipboard_loop)

    def _check_clipboard_loop(self) -> None:
        clipboard_content = self._get_clipboard_content()
        if clipboard_content != self._last_clipboard:
            print("Clipboard changed!")
            if self._display_window is None or self._display_window.winfo_exists() == 0:
                self._display_window = AlwaysOnTopTextDisplay(self)
            self._display_window.text = clipboard_content
            self._last_clipboard = clipboard_content

        self.after(250, self._check_clipboard_loop)

    def _get_clipboard_content(self) -> Optional[str]:
        """
        Attempts retrieving the clipboard content as a string.

        :return: Returns the clipboard as a string, or None if it was something else (such as an image)
        """
        try:
            return self.clipboard_get()
        except tk.TclError:
            return None

    def open_top_level(self):
        if self._display_window is not None:
            self._display_window.destroy()
        self._display_window = AlwaysOnTopTextDisplay(self)

        # Make topLevelWindow remain on top until destroyed, or attribute changes.
        # def foo():


root = tk.Tk()
main = WITClipboardMonitor(root)
root.mainloop()
