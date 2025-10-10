import argparse
from theme_build.css_builder import build_styles
from theme_build.yaml_builder import build_config

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Build YAML config with !include support")
  parser.add_argument("-i", "--input", help="Input YAML file with !include statements")
  parser.add_argument("-o", "--output", help="Output flattened YAML file")
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
