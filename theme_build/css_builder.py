import os
import glob

def build_styles(theme: str, output: str):
    theme_dir = os.path.join("themes", theme)
    default_dir = os.path.join("themes", "default")

    base_css_default = os.path.join(default_dir, "_base.css")
    base_css_theme = os.path.join(theme_dir, "_base.css")

    lines = []
    if os.path.isfile(base_css_default):
      lines.append(f'@import "themes/default/_base.css";')
    else:
      raise FileNotFoundError("Default _base.css not found.")

    if theme != "default" and os.path.isfile(base_css_theme):
      lines.append(f'@import "themes/{theme}/_base.css";')

    default_styles_dir = os.path.join(default_dir, "styles")
    default_styles = sorted(glob.glob(os.path.join(default_styles_dir, "*.css")))

    for css_file in default_styles:
      filename = os.path.basename(css_file)
      lines.append(f'@import "themes/default/styles/{filename}";')

    if theme != "default":
      theme_styles_dir = os.path.join(theme_dir, "styles")
      if os.path.isdir(theme_styles_dir):
        theme_styles = sorted(glob.glob(os.path.join(theme_styles_dir, "*.css")))
        if theme_styles:
          for css_file in theme_styles:
            filename = os.path.basename(css_file)
            lines.append(f'@import "themes/{theme}/styles/{filename}";')
        else:
          print(f"Note: No theme CSS overrides found in '{theme_styles_dir}'.")
      else:
        print(f"Note: No theme styles directory found for '{theme}'. Only defaults will be included.")

    with open(output, "w", encoding="utf-8") as f:
      f.write("\n".join(lines) + "\n")