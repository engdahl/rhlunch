# RHLunch

A simple command-line tool to get lunch menus from ISS restaurants.

## Installation

### From GitHub

```bash
pip install git+https://github.com/engdahl/rhlunch.git
```

### From source

```bash
git clone https://github.com/engdahl/rhlunch.git
cd rhlunch
pip install -e .
```

This installs the `lunch` command globally on your system.

**Requirements:**

- Python 3.8 or higher

## Usage

Get today's lunch menu:

```bash
lunch
```

Show only vegetarian options:

```bash
lunch -v
```

Show only meat options:

```bash
lunch -m
```

Show the whole week menu:

```bash
lunch -w
```

Enable debug logging to troubleshoot issues:

```bash
lunch -d
```

## Example Output

```
🍽️  Lunch Menu for Today
==================================================

🥬 Vegetarian Options:
  • Vegetariskt Moussaka på vegofärs,aubergine,potatis,serveras med tzatziki

🥩 Meat Options:
  • Ärtsoppa Ärtsoppa/Vegan Fläskbog,timjan,mejram,senap
  • Pannkaka Yessufs goda pannkisar med drottningsylt och vispad grädde
```

## License

MIT License - see LICENSE file for details.
