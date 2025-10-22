"""Command line interface for the Gourmedia scraper."""

import click
from datetime import date, datetime
import logging
from .scraper import ISSMenuScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)


@click.command()
@click.option('--restaurant', '-r', 'restaurant_url',
              default='https://www.iss-menyer.se/restaurants/restaurang-gourmedia',
              help='Restaurant URL to scrape. Defaults to Gourmedia.')
@click.option('--vegetarian-only', '-v', is_flag=True,
              help='Show only vegetarian options.')
@click.option('--meat-only', '-m', is_flag=True,
              help='Show only meat options.')
@click.option('--week', '-w', is_flag=True,
              help='Show the whole week menu.')
@click.option('--debug', '-d', is_flag=True,
              help='Enable debug logging to show which date is being fetched.')
def main(restaurant_url, vegetarian_only, meat_only, week, debug):
    """
    Get lunch menu from ISS restaurants.
    
    Examples:
        lunch                    # Get today's menu
        lunch -v                # Show only vegetarian options
        lunch -m                # Show only meat options
        lunch -w                # Show whole week menu
        lunch -d                # Enable debug logging
    """
    # Enable debug logging if requested
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.debug("Debug logging enabled")
    
    try:
        # Create scraper instance
        scraper = ISSMenuScraper(restaurant_url)
        
        if week:
            # Get menu for the whole week
            weekly_menu = scraper.get_weekly_menu()
            display_weekly_menu(weekly_menu, vegetarian_only, meat_only)
        else:
            # Get menu for today
            menu = scraper.get_menu_for_day()
            display_menu(menu, vegetarian_only, meat_only)
        
    except Exception as e:
        click.echo("\n❌ Error fetching menu:", err=True)
        click.echo(f"   {e}", err=True)
        click.echo("\nPossible reasons:", err=True)
        click.echo("   • The website structure may have changed", err=True)
        click.echo("   • The menu may not be available yet", err=True)
        click.echo("   • Network connectivity issues", err=True)
        click.echo("\nTry running with --debug (-d) flag for more details.", err=True)
        raise click.Abort()


def display_menu(menu, vegetarian_only, meat_only):
    """Display the menu in a formatted way."""
    today = date.today()
    day_names = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    day_name = day_names[today.weekday()]
    
    click.echo(f"\n🍽️  Lunch Menu for {day_name}, {today.strftime('%B %d, %Y')}")
    click.echo("=" * 50)
    
    # Show vegetarian options
    if not meat_only and menu.get('vegetarian'):
        click.echo("\n🥬 Vegetarian Options:")
        for item in menu['vegetarian']:
            click.echo(f"  • {item}")
    
    # Show meat options
    if not vegetarian_only and menu.get('meat'):
        click.echo("\n🥩 Meat Options:")
        for item in menu['meat']:
            click.echo(f"  • {item}")
    
    # Handle case where no menu items found
    if not menu.get('vegetarian') and not menu.get('meat'):
        click.echo("\n❌ No menu items found for today.")
        click.echo("This might be because:")
        click.echo("  • It's a weekend (restaurant might be closed)")
        click.echo("  • The menu hasn't been updated yet")
        click.echo("  • There was an issue scraping the website")
    
    click.echo()


def display_weekly_menu(weekly_menu, vegetarian_only, meat_only):
    """Display the weekly menu in a formatted way."""
    click.echo(f"\n🍽️  Weekly Lunch Menu")
    click.echo("=" * 50)
    
    day_names = {
        'måndag': 'Monday',
        'tisdag': 'Tuesday', 
        'onsdag': 'Wednesday',
        'torsdag': 'Thursday',
        'fredag': 'Friday',
        'lördag': 'Saturday',
        'söndag': 'Sunday'
    }
    
    for day_key, day_name in day_names.items():
        if day_key in weekly_menu:
            menu = weekly_menu[day_key]
            
            # Skip if no menu items and it's a weekend
            if not menu.get('vegetarian') and not menu.get('meat'):
                if day_key in ['lördag', 'söndag']:
                    continue  # Skip empty weekends
            
            click.echo(f"\n📅 {day_name}")
            click.echo("-" * 20)
            
            # Show vegetarian options
            if not meat_only and menu.get('vegetarian'):
                click.echo("🥬 Vegetarian:")
                for item in menu['vegetarian']:
                    click.echo(f"  • {item}")
            
            # Show meat options
            if not vegetarian_only and menu.get('meat'):
                click.echo("🥩 Meat:")
                for item in menu['meat']:
                    click.echo(f"  • {item}")
            
            # Show message if no items found
            if not menu.get('vegetarian') and not menu.get('meat'):
                click.echo("  ❌ No menu available")
    
    click.echo()


if __name__ == '__main__':
    main()
