# Danger Noodle (dnd for short)

Python module for handling npm modules available on unpkg.com

# Install

```bash
pip install danger-noodle
```

# Usage

`dnd install`: Install all packages based on a snakeskin.txt

`dnd install <package-name>`: Install a package that best matches the provided package name and appends the package and version to snakeskin.txt

`dnd uninstall <package-name>`: Uninstall a package that best matches the provided package name and appends the package and version to snakeskin.txt

# Example commands

`dnd install bootstrap`

`dnd uninstall bootstrap`

`dnd install jquery@3.3.0`

`dnd uninstall jquery@3.3.0`
