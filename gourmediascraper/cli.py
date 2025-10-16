"""Command line interface for the Gourmedia scraper."""

import click
from datetime import date, datetime
from .scraper import ISSMenuScraper


@click.command()
@click.option('--date', '-d', 'target_date', 
              help='Date to get menu for (YYYY-MM-DD format). Defaults to today.',
              type=click.DateTime(formats=['%Y-%m-%d']))
@click.option('--restaurant', '-r', 'restaurant_url',
              default='https://www.iss-menyer.se/restaurants/restaurang-gourmedia',
              help='Restaurant URL to scrape. Defaults to Gourmedia.')
@click.option('--vegetarian-only', '-v', is_flag=True,
              help='Show only vegetarian options.')
@click.option('--meat-only', '-m', is_flag=True,
              help='Show only meat options.')
def main(target_date, restaurant_url, vegetarian_only, meat_only):
    """
    Get today's lunch menu from ISS restaurants.
    
    Examples:
        lunch                    # Get today's menu
        lunch -d 2024-01-15     # Get menu for specific date
        lunch -v                # Show only vegetarian options
        lunch -m                # Show only meat options
    """
    try:
        # Convert datetime to date if provided
        if target_date:
            target_date = target_date.date()
        
        # Create scraper instance
        scraper = ISSMenuScraper(restaurant_url)
        
        # Get menu for the specified date
        menu = scraper.get_menu_for_day(target_date)
        
        # Display the menu
        display_menu(menu, target_date, vegetarian_only, meat_only)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


def display_menu(menu, target_date, vegetarian_only, meat_only):
    """Display the menu in a formatted way."""
    if target_date:
        date_str = target_date.strftime('%A, %B %d, %Y')
    else:
        date_str = "Today"
    
    click.echo(f"\n🍽️  Lunch Menu for {date_str}")
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
        click.echo("\n❌ No menu items found for this date.")
        click.echo("This might be because:")
        click.echo("  • It's a weekend (restaurant might be closed)")
        click.echo("  • The menu hasn't been updated yet")
        click.echo("  • There was an issue scraping the website")
    
    click.echo()


if __name__ == '__main__':
    main()
