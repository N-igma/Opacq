# Interface + Integration: Jerome
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk

style_provider = Gtk.CssProvider ()

css = """
#MyWindow {
  background-color: #000;
}
""".encode()

style_provider.load_from_data (css)

Gtk.StyleContext.add_provider_for_screen (Gdk.Screen.get_default(), 
                                          style_provider,
                                          Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

class MyWindow(Gtk.Window):
  def __init__(self):
    super().__init__(title="Hello World",
                     name="MyWindow")

    self.top_bar = Gtk.Box(spacing=8, border_width=8)
    self.add(self.top_bar)

    self.top_bar.add_btn = Gtk.Image(file="assets/add.png")
    self.top_bar.add(self.top_bar.add_btn)

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
