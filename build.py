import os
import yaml
import glob
import argparse

class IncludeLoader(yaml.SafeLoader):
  pass

def construct_include(loader, node):
  # Makes !include load YAML file contents
  filename = loader.construct_scalar(node)

  theme_path = os.path.join(loader.theme_dir, filename)
  default_path = os.path.join(loader.default_dir, filename)

  if os.path.isfile(theme_path):
    filepath = theme_path
  elif os.path.isfile(default_path):
    filepath = default_path
  else:
    raise FileNotFoundError(f"Included file not found in theme or default: {filename}")

  with open(filepath, "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=IncludeLoader)

  return data

IncludeLoader.add_constructor("!include", construct_include)

def merge_top_level(base, data):
  # Merge contents of top-level key '_merge'
  if "_merge" in data:
    merge_content = data.pop("_merge")
    if not isinstance(merge_content, dict):
      raise ValueError("_merge must be a mapping/dictionary")
    
    for k, v in merge_content.items():
      if k in base and isinstance(base[k], dict) and isinstance(v, dict):
        base[k] = merge_top_level(base[k], v)
      else:
        base[k] = v

  for k, v in data.items():
    base[k] = v
  return base

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

def build_config(theme: str, input: str, output: str):
  theme_dir = os.path.join("themes", theme)
  default_dir = os.path.join("themes", "default")

  if not os.path.isdir(theme_dir):
    print(f"Warning: Theme folder '{theme_dir}' does not exist. Falling back to default.")

  IncludeLoader.theme_dir = theme_dir
  IncludeLoader.default_dir = default_dir

  with open(input, "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=IncludeLoader)

  final_data = merge_top_level({}, data)

  with open(output, "w", encoding="utf-8") as f:
    yaml.dump(final_data, f, sort_keys=False)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Build YAML config with !include support")
  parser.add_argument("input", help="Input YAML file with !include statements")
  parser.add_argument("-o", "--output", required=True, help="Output flattened YAML file")
  parser.add_argument("-t", "--theme", default="default", help="Theme folder to use (fallback to default)")
  parser.add_argument("-c", "--css-output", help="Path to output built CSS file")
  args = parser.parse_args()
  
  if args.output:
    build_config(args.theme, args.input, args.output)
    print(f"Created `{args.output}`")

  if args.css_output:
    build_styles(args.theme, args.css_output)
    print(f"Created `{args.css_output}`")

  print(f"Finished building")
