#!/usr/bin/env python3
"""
Script to populate the database with test poker session data.
This will help test the application with a larger dataset.
"""

import random
import sqlite3
from datetime import datetime, timedelta
from typing import List, Tuple

# Realistic poker session data
LOCATIONS = [
    "Aria Casino", "Bellagio", "Wynn Las Vegas", "Venetian", "MGM Grand",
    "Caesars Palace", "Borgata", "Foxwoods", "Mohegan Sun", "Parx Casino",
    "Commerce Casino", "Bicycle Hotel & Casino", "Hollywood Park Casino",
    "Lucky Chances Casino", "Bay 101", "Ocean's Eleven Casino",
    "Home Game - Mike's", "Home Game - Downtown", "Online - PokerStars",
    "Online - GGPoker", "Underground Club", "Private Game"
]

STAKE_LEVELS = [
    (0.25, 0.50),   # Micro stakes
    (0.50, 1.00),   # Small stakes
    (1.00, 2.00),   # Low stakes
    (1.00, 3.00),   # 1/3 mixed
    (2.00, 5.00),   # Mid stakes
    (5.00, 10.00),  # Higher stakes
    (10.00, 20.00), # High stakes
    (25.00, 50.00), # Very high stakes
]

NOTES_TEMPLATES = [
    "Tight table, waited for premium hands. Players were very conservative.",
    "Loose aggressive game. Lots of 3-betting and wide ranges.",
    "Hit a bad beat early but recovered well in the second half.",
    "Great read on villain in big pot. Trust the instincts.",
    "Ran card dead for first 2 hours, then caught fire.",
    "Table was very fishy. Several recreational players giving action.",
    "Tough reg-heavy game. Had to play very tight and patient.",
    "Short session due to family obligations, but profitable.",
    "Tilted a bit after losing AA vs KK all-in preflop.",
    "Perfect session - cards and decisions aligned perfectly.",
    "Bluffed way too much. Need to tighten up value betting.",
    "Great table selection - found the perfect game.",
    "Ran into a maniac who was betting everything. Adjusted well.",
    "Cold cards but made good laydowns. Damage control session.",
    "Hit a monster session - everything went right today.",
    "",  # Some sessions have no notes
    "Mental game was on point. Stayed focused throughout.",
    "Table broke early, had to find new game mid-session.",
    "Learned a lot about opponent tendencies today.",
    "Need to work on river betting for value."
]

def generate_random_session() -> Tuple:
    """Generate a random poker session with realistic data."""
    
    # Random date within the last 2 years
    start_date = datetime.now() - timedelta(days=730)
    random_days = random.randint(0, 730)
    session_date = start_date + timedelta(days=random_days)
    
    # Random location
    location = random.choice(LOCATIONS)
    
    # Random stake level
    sb_size, bb_size = random.choice(STAKE_LEVELS)
    
    # Random session length (1-12 hours, weighted toward 4-8 hours)
    hours = round(random.triangular(1, 12, 6), 1)
    
    # Random buy-in (typically 100-200 big blinds)
    buy_in_bb = random.randint(80, 250)
    buy_in = round(buy_in_bb * bb_size, 2)
    
    # Generate cash-out based on skill/luck factors
    # Simulate a slightly winning player with variance
    skill_edge = random.gauss(0.05, 0.1)  # 5% edge with variance
    luck_factor = random.gauss(0, 0.3)    # Luck/variance component
    
    total_factor = 1 + skill_edge + luck_factor
    cash_out = round(buy_in * total_factor, 2)
    
    # Ensure some minimum loss cap (can't lose more than buy-in + some rebuys)
    max_loss = buy_in * 2.5
    if cash_out < -max_loss:
        cash_out = round(-max_loss + random.uniform(0, max_loss * 0.3), 2)
    
    # Random notes (some sessions have no notes)
    notes = random.choice(NOTES_TEMPLATES)
    
    return (
        session_date.strftime('%Y-%m-%d'),
        location,
        sb_size,
        bb_size,
        buy_in,
        cash_out,
        hours,
        notes
    )

def create_test_sessions(num_sessions: int = 100) -> List[Tuple]:
    """Create a list of test sessions."""
    sessions = []
    for i in range(num_sessions):
        session = generate_random_session()
        sessions.append(session)
    
    # Sort by date to make it more realistic
    sessions.sort(key=lambda x: x[0])
    
    return sessions

def populate_database(sessions: List[Tuple]):
    """Populate the database with test sessions."""
    
    # Connect to the database
    conn = sqlite3.connect('bankroll.db')
    cursor = conn.cursor()
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("Clearing existing sessions...")
    cursor.execute("DELETE FROM sessions")
    
    # Insert test sessions
    print(f"Inserting {len(sessions)} test sessions...")
    
    insert_query = """
    INSERT INTO sessions (
        date, location, sb_size, bb_size, buy_in, cash_out, hours, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.executemany(insert_query, sessions)
    
    # Commit changes
    conn.commit()
    
    # Print summary statistics
    cursor.execute("SELECT COUNT(*) FROM sessions")
    total_sessions = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(cash_out - buy_in) FROM sessions")
    total_profit = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(hours) FROM sessions")
    total_hours = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT AVG((cash_out - buy_in) / bb_size / hours) FROM sessions WHERE hours > 0 AND bb_size > 0")
    avg_bb_hour = cursor.fetchone()[0] or 0
    
    conn.close()
    
    print(f"\n✅ Database populated successfully!")
    print(f"📊 Summary Statistics:")
    print(f"   Total Sessions: {total_sessions}")
    print(f"   Total Profit: ${total_profit:.2f}")
    print(f"   Total Hours: {total_hours:.1f}")
    print(f"   Average BB/hour: {avg_bb_hour:.2f}")
    print(f"   Hourly Rate: ${(total_profit/total_hours if total_hours > 0 else 0):.2f}/hour")

if __name__ == "__main__":
    print("🎰 Generating random poker session data...")
    
    # Generate test sessions
    test_sessions = create_test_sessions(100)
    
    # Populate database
    populate_database(test_sessions)
    
    print("\n🚀 Test data generation complete!")
    print("   Start your backend server and check the website!") 