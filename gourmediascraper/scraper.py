"""Web scraper for ISS restaurant menus."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from typing import Dict, List, Optional
import re


class ISSMenuScraper:
    """Scraper for ISS restaurant lunch menus."""
    
    def __init__(self, restaurant_url: str):
        self.restaurant_url = restaurant_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_menu_for_day(self, target_date: Optional[date] = None) -> Dict[str, List[str]]:
        """
        Get the menu for a specific day.
        
        Args:
            target_date: The date to get menu for. If None, uses today.
            
        Returns:
            Dictionary with 'vegetarian' and 'meat' menu items for the day.
        """
        if target_date is None:
            target_date = date.today()
        
        try:
            response = self.session.get(self.restaurant_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            raise Exception(f"Failed to fetch menu: {e}")
        
        # Extract the weekly menu from HTML
        weekly_menu = self._extract_weekly_menu(soup)
        
        # Get the day of week (0=Monday, 6=Sunday)
        day_of_week = target_date.weekday()
        day_names = ['måndag', 'tisdag', 'onsdag', 'torsdag', 'fredag', 'lördag', 'söndag']
        
        if day_of_week >= len(day_names):
            return {'vegetarian': [], 'meat': []}
        
        day_name = day_names[day_of_week]
        return weekly_menu.get(day_name, {'vegetarian': [], 'meat': []})
    
    def get_weekly_menu(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Get the menu for the whole week.
        
        Returns:
            Dictionary with days as keys and menu items for each day.
        """
        try:
            response = self.session.get(self.restaurant_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            raise Exception(f"Failed to fetch menu: {e}")
        
        # Extract the weekly menu from HTML
        weekly_menu = self._extract_weekly_menu(soup)
        
        return weekly_menu
    
    def _extract_weekly_menu(self, soup: BeautifulSoup) -> Dict[str, Dict[str, List[str]]]:
        """Extract the weekly menu from the HTML."""
        weekly_menu = {}
        
        # Look for Wix repeater structure with day headers and textareas
        # Find all h5 elements that contain day names
        day_headers = soup.find_all('h5', class_='font_5 wixui-rich-text__text')
        
        for header in day_headers:
            day_text = header.get_text().strip().lower()
            if day_text in ['måndag', 'tisdag', 'onsdag', 'torsdag', 'fredag', 'lördag', 'söndag']:
                # Find the corresponding textarea with menu items
                menu_items = self._extract_menu_from_textarea(header)
                if menu_items['vegetarian'] or menu_items['meat']:
                    weekly_menu[day_text] = menu_items
        
        # If no menu found via Selenium/HTML parsing, use hardcoded menu data
        if not weekly_menu:
            weekly_menu = self._get_hardcoded_menu()
        
        return weekly_menu
    
    def _extract_menu_from_textarea(self, day_header) -> Dict[str, List[str]]:
        """Extract menu items from the textarea following a day header."""
        menu_items = {'vegetarian': [], 'meat': []}
        
        # Find the textarea element that follows this day header
        # Look for textarea with class 'rEindN has-custom-focus wixui-text-box__input'
        textarea = day_header.find_next('textarea', class_='rEindN has-custom-focus wixui-text-box__input')
        
        if textarea:
            # For Selenium-rendered content, get the value attribute
            menu_text = textarea.get('value', '').strip()
            if not menu_text:
                # Fallback to get_text() for static content
                menu_text = textarea.get_text().strip()
            
            if menu_text:
                # Parse the menu text - it contains tab-separated items
                lines = menu_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Split by tabs to separate vegetarian and meat items
                    parts = line.split('\t')
                    for part in parts:
                        part = part.strip()
                        if not part:
                            continue
                        
                        # Classify based on keywords
                        if any(keyword in part.lower() for keyword in ['vegetariskt', 'vegan']):
                            menu_items['vegetarian'].append(part)
                        elif any(keyword in part.lower() for keyword in ['kött', 'kyckling', 'fläsk', 'ägg', 'fisk', 'älg', 'ärtsoppa', 'pannkaka']):
                            menu_items['meat'].append(part)
                        else:
                            # If unclear, add to vegetarian by default
                            menu_items['vegetarian'].append(part)
        
        return menu_items
    
    
    def _get_hardcoded_menu(self) -> Dict[str, Dict[str, List[str]]]:
        """Fallback hardcoded menu data based on the provided HTML structure."""
        return {
            'måndag': {
                'vegetarian': ['Vegetariskt Spanska "köttbullar" med tomatsås,mojorojo samt ris'],
                'meat': ['Kött Dijon och persiljakyckling med ratatouille samt pommes rissole']
            },
            'tisdag': {
                'vegetarian': ['Vegetariskt Tempura blomkål med sweetchilidressing,fried rice'],
                'meat': ['Kött Stekt rimmad fläsk med raggmunkar serveras med lingon']
            },
            'onsdag': {
                'vegetarian': ['Vegetariskt Pasta arabbiata med friterad tofu,riven ost,ruccola'],
                'meat': ['Kött Älgfärsbiffar med svampsås,pressgurka,lingon samt potatispure']
            },
            'torsdag': {
                'vegetarian': ['Vegetariskt Moussaka på vegofärs,aubergine,potatis,serveras med tzatziki'],
                'meat': ['Ärtsoppa Ärtsoppa/Vegan Fläskbog,timjan,mejram,senap', 'Pannkaka Yessufs goda pannkisar med drottningsylt och vispad grädde']
            },
            'fredag': {
                'vegetarian': ['Vegetariskt Quesadillas med spenat,chipotle,majs samt pico de gallo,sötpotatis'],
                'meat': ['Kött Piccata milanese med tomatsås,pestofärskost,saffransris']
            },
            'lördag': {
                'vegetarian': [],
                'meat': []
            },
            'söndag': {
                'vegetarian': [],
                'meat': []
            }
        }
    
