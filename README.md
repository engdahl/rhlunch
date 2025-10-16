# Gourmedia Scraper

A command-line tool to scrape lunch menus from ISS restaurants, specifically designed for the Gourmedia restaurant in Stockholm.

## Features

- 🍽️ Get today's lunch menu with a simple `lunch` command
- 📅 View menus for specific dates
- 🥬 Filter for vegetarian options only
- 🥩 Filter for meat options only
- 🏢 Support for different ISS restaurant locations

## Installation

### Option 1: Install from source (Recommended for development)

1. Clone this repository:

```bash
git clone <repository-url>
cd gourmediascraper
```

2. Install the package in development mode:

```bash
pip install -e .
```

This will install the `lunch` command globally on your system.

### Option 2: Install dependencies manually

1. Clone this repository:

```bash
git clone <repository-url>
cd gourmediascraper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the CLI directly:

```bash
python -m gourmediascraper.cli
```

## Usage

### Basic Usage

Get today's lunch menu:

```bash
lunch
```

### Advanced Usage

Get menu for a specific date:

```bash
lunch -d 2024-01-15
```

Show only vegetarian options:

```bash
lunch -v
```

Show only meat options:

```bash
lunch -m
```

Get menu from a different restaurant:

```bash
lunch -r https://www.iss-menyer.se/restaurants/other-restaurant
```

### Command Options

- `-d, --date`: Date to get menu for (YYYY-MM-DD format). Defaults to today.
- `-r, --restaurant`: Restaurant URL to scrape. Defaults to Gourmedia.
- `-v, --vegetarian-only`: Show only vegetarian options.
- `-m, --meat-only`: Show only meat options.
- `--help`: Show help message.

## Example Output

```
🍽️  Lunch Menu for Monday, January 15, 2024
==================================================

🥬 Vegetarian Options:
  • Vegetariskt Spanska "köttbullar" med tomatsås, mojorojo samt ris

🥩 Meat Options:
  • Kött Dijon och persiljakyckling med ratatouille samt pommes rissole
```

## Development

### Project Structure

```
gourmediascraper/
├── gourmediascraper/
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   └── scraper.py      # Web scraping logic
├── requirements.txt     # Python dependencies
├── setup.py           # Package configuration
└── README.md          # This file
```

### Running Tests

To test the scraper manually:

```bash
python -c "from gourmediascraper.scraper import ISSMenuScraper; scraper = ISSMenuScraper('https://www.iss-menyer.se/restaurants/restaurang-gourmedia'); print(scraper.get_menu_for_day())"
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Troubleshooting

### Common Issues

**"No menu items found"**

- The restaurant might be closed on weekends
- The menu might not be updated yet
- There could be a temporary issue with the website

**"Failed to fetch menu"**

- Check your internet connection
- The ISS website might be temporarily down
- Try again later

**Installation issues**

- Make sure you have Python 3.8+ installed
- Use `pip3` instead of `pip` if needed
- Try installing with `--user` flag: `pip install -e . --user`

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open an issue on the GitHub repository.
