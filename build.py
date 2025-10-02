import os
import yaml
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

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Build YAML config with !include support")
  parser.add_argument("input", help="Input YAML file with !include statements")
  parser.add_argument("-o", "--output", required=True, help="Output flattened YAML file")
  parser.add_argument("-t", "--theme", default="default", help="Theme folder to use (fallback to default)")
  args = parser.parse_args()
  
  theme_dir = os.path.join("themes", args.theme)
  default_dir = os.path.join("themes", "default")

  if not os.path.isdir(theme_dir):
    print(f"Warning: Theme folder '{theme_dir}' does not exist. Falling back to default.")

  IncludeLoader.theme_dir = theme_dir
  IncludeLoader.default_dir = default_dir

  with open(args.input, "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=IncludeLoader)

  final_data = merge_top_level({}, data)

  with open(args.output, "w", encoding="utf-8") as f:
    yaml.dump(final_data, f, sort_keys=False)

  print(f"Finished building. Saved to `{args.output}`")