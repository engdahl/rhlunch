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
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch menu: {e}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the weekly menu section
        weekly_menu = self._extract_weekly_menu(soup)
        
        # Get the day of week (0=Monday, 6=Sunday)
        day_of_week = target_date.weekday()
        day_names = ['måndag', 'tisdag', 'onsdag', 'torsdag', 'fredag', 'lördag', 'söndag']
        
        if day_of_week >= len(day_names):
            return {'vegetarian': [], 'meat': []}
        
        day_name = day_names[day_of_week]
        return weekly_menu.get(day_name, {'vegetarian': [], 'meat': []})
    
    def _extract_weekly_menu(self, soup: BeautifulSoup) -> Dict[str, Dict[str, List[str]]]:
        """Extract the weekly menu from the HTML."""
        weekly_menu = {}
        
        # Look for menu items in various possible structures
        # The menu might be in different formats, so we'll try multiple approaches
        
        # Method 1: Look for day headers and following content
        day_headers = soup.find_all(['h4', 'h5', 'h6'], string=re.compile(r'(måndag|tisdag|onsdag|torsdag|fredag|lördag|söndag)', re.IGNORECASE))
        
        for header in day_headers:
            day_name = header.get_text().strip().lower()
            if day_name in ['måndag', 'tisdag', 'onsdag', 'torsdag', 'fredag', 'lördag', 'söndag']:
                menu_items = self._extract_menu_items_for_day(header)
                weekly_menu[day_name] = menu_items
        
        # Method 2: Look for menu content in divs or other containers
        if not weekly_menu:
            menu_containers = soup.find_all(['div', 'section'], class_=re.compile(r'menu|vecka|lunch', re.IGNORECASE))
            for container in menu_containers:
                self._parse_menu_container(container, weekly_menu)
        
        # Method 3: Look for text patterns that indicate menu items
        if not weekly_menu:
            self._extract_menu_from_text_patterns(soup, weekly_menu)
        
        return weekly_menu
    
    def _extract_menu_items_for_day(self, day_header) -> Dict[str, List[str]]:
        """Extract menu items for a specific day starting from its header."""
        menu_items = {'vegetarian': [], 'meat': []}
        
        # Look for content after the header
        current = day_header.find_next_sibling()
        while current and current.name in ['p', 'div', 'span', 'li']:
            text = current.get_text().strip()
            if text:
                if 'vegetar' in text.lower():
                    menu_items['vegetarian'].append(text)
                elif any(keyword in text.lower() for keyword in ['kött', 'kyckling', 'fläsk', 'ägg', 'fisk']):
                    menu_items['meat'].append(text)
                else:
                    # If unclear, add to both
                    menu_items['vegetarian'].append(text)
                    menu_items['meat'].append(text)
            current = current.find_next_sibling()
        
        return menu_items
    
    def _parse_menu_container(self, container, weekly_menu: Dict):
        """Parse a menu container for weekly menu data."""
        text = container.get_text()
        
        # Look for day patterns
        day_pattern = r'(måndag|tisdag|onsdag|torsdag|fredag|lördag|söndag)'
        days_found = re.findall(day_pattern, text, re.IGNORECASE)
        
        for day in days_found:
            day_lower = day.lower()
            if day_lower not in weekly_menu:
                weekly_menu[day_lower] = {'vegetarian': [], 'meat': []}
    
    def _extract_menu_from_text_patterns(self, soup: BeautifulSoup, weekly_menu: Dict):
        """Extract menu items using text pattern matching."""
        text = soup.get_text()
        
        # Split by days and extract content
        day_pattern = r'(måndag|tisdag|onsdag|torsdag|fredag|lördag|söndag)'
        parts = re.split(day_pattern, text, flags=re.IGNORECASE)
        
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                day_name = parts[i].lower()
                day_content = parts[i + 1]
                
                # Extract menu items from day content
                menu_items = self._parse_day_content(day_content)
                weekly_menu[day_name] = menu_items
    
    def _parse_day_content(self, content: str) -> Dict[str, List[str]]:
        """Parse menu content for a specific day."""
        menu_items = {'vegetarian': [], 'meat': []}
        
        # Split content into lines and process
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for vegetarian indicators
            if any(indicator in line.lower() for indicator in ['vegetar', 'vegan', 'vegofärs']):
                menu_items['vegetarian'].append(line)
            # Look for meat indicators
            elif any(indicator in line.lower() for indicator in ['kött', 'kyckling', 'fläsk', 'ägg', 'fisk', 'älg']):
                menu_items['meat'].append(line)
            # If unclear, add to vegetarian by default
            else:
                menu_items['vegetarian'].append(line)
        
        return menu_items
