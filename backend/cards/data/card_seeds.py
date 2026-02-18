"""
Card seed data with popular credit cards and their benefits.
All amounts are in cents.
Covers: American Express, Chase, Capital One, Citi, Bank of America, US Bank
"""

CARD_SEEDS = [

    # ─────────────────────────────────────────
    # AMERICAN EXPRESS
    # ─────────────────────────────────────────
    {
        'bank': 'American Express',
        'name': 'Platinum Card',
        'annual_fee_cents': 89500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Hotel Credit',
                'description': 'Up to $300 semi-annually ($600/year) on prepaid Fine Hotels + Resorts or The Hotel Collection bookings via AmexTravel.com',
                'amount_cents': 30000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Resy Dining Credit',
                'description': 'Up to $100 per quarter ($400/year) at eligible U.S. Resy restaurants',
                'amount_cents': 10000,
                'frequency': 'quarterly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
            {
                'name': 'Lululemon Credit',
                'description': 'Up to $75 per quarter ($300/year) on lululemon purchases',
                'amount_cents': 7500,
                'frequency': 'quarterly',
                'period_type': 'calendar_year',
                'category': 'shopping',
            },
            {
                'name': 'Digital Entertainment Credit',
                'description': '$25/month ($300/year) for eligible streaming and digital services (Disney+, Hulu, ESPN+, Peacock, NYT, SiriusXM, etc.)',
                'amount_cents': 2500,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'entertainment',
            },
            {
                'name': 'Saks Fifth Avenue Credit',
                'description': 'Up to $50 semi-annually ($100/year) in statement credits at Saks Fifth Avenue',
                'amount_cents': 5000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'shopping',
            },
            {
                'name': 'Uber Cash',
                'description': '$15/month Uber Cash ($35 in December) for Uber rides or Uber Eats',
                'amount_cents': 1500,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'transportation',
            },
            {
                'name': 'Walmart+ Credit',
                'description': '$12.95/month statement credit covering the Walmart+ membership fee',
                'amount_cents': 1295,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'shopping',
            },
            {
                'name': 'Equinox Credit',
                'description': 'Up to $25/month ($300/year) toward Equinox club memberships or the Equinox+ app',
                'amount_cents': 2500,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'other',
            },
            {
                'name': 'Oura Ring Credit',
                'description': 'Up to $200 annually toward an Oura Ring purchase at ouraring.com',
                'amount_cents': 20000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'other',
            },
            {
                'name': 'Airline Fee Credit',
                'description': 'Up to $200 annually for incidental fees on one selected airline',
                'amount_cents': 20000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'CLEAR Plus Credit',
                'description': 'Up to $209 annually toward CLEAR Plus membership',
                'amount_cents': 20900,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck application (every 4 years)',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Gold Card',
        'annual_fee_cents': 32500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Dining Credit',
                'description': '$10/month ($120/year) at Grubhub, The Cheesecake Factory, Goldbelly, Wine.com, and Five Guys',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
            {
                'name': 'Uber Cash',
                'description': '$10/month ($120/year) Uber Cash for Uber Eats or Uber rides',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'transportation',
            },
            {
                'name': 'Dunkin\' Credit',
                'description': '$7/month ($84/year) statement credit at Dunkin\'',
                'amount_cents': 700,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
            {
                'name': 'Resy Credit',
                'description': 'Up to $50 semi-annually ($100/year) at eligible U.S. Resy restaurants',
                'amount_cents': 5000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Green Card',
        'annual_fee_cents': 15000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'CLEAR Plus Credit',
                'description': 'Up to $209 annually toward CLEAR Plus membership',
                'amount_cents': 20900,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'LoungeBuddy Credit',
                'description': 'Up to $100 annual credit for airport lounge access via LoungeBuddy',
                'amount_cents': 10000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Blue Cash Preferred',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Disney Bundle Credit',
                'description': 'Up to $10/month ($120/year) statement credit when you purchase Disney+, Hulu, or ESPN+ subscriptions',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'entertainment',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Blue Cash Everyday',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Disney Bundle Credit',
                'description': '$7/month statement credit on The Disney Bundle subscription',
                'amount_cents': 700,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'entertainment',
            },
            {
                'name': 'Home Chef Credit',
                'description': '$15/month credit for Home Chef meal kit subscription',
                'amount_cents': 1500,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Business Platinum Card',
        'annual_fee_cents': 89500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Hotel Credit',
                'description': 'Up to $300 semi-annually ($600/year) on prepaid Fine Hotels + Resorts or The Hotel Collection bookings via AmexTravel.com',
                'amount_cents': 30000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Dell Technologies Credit',
                'description': 'Up to $200 semi-annually ($400/year) toward Dell Technologies purchases',
                'amount_cents': 20000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'shopping',
            },
            {
                'name': 'Indeed Credit',
                'description': 'Up to $90 per quarter ($360/year) toward Indeed job postings',
                'amount_cents': 9000,
                'frequency': 'quarterly',
                'period_type': 'calendar_year',
                'category': 'other',
            },
            {
                'name': 'Adobe Credit',
                'description': 'Up to $150 annually toward eligible Adobe Creative Cloud subscriptions',
                'amount_cents': 15000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'other',
            },
            {
                'name': 'Hilton for Business Credit',
                'description': 'Up to $50 per quarter ($200/year) on eligible Hilton hotel stays via the Hilton for Business program',
                'amount_cents': 5000,
                'frequency': 'quarterly',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Wireless Credit',
                'description': 'Up to $120 annually ($10/month) for eligible U.S. wireless phone bills',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'other',
            },
            {
                'name': 'CLEAR Plus Credit',
                'description': 'Up to $209 annually toward CLEAR Plus membership',
                'amount_cents': 20900,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry application fee (every 4 years)',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Business Gold Card',
        'annual_fee_cents': 37500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Business Credit',
                'description': 'Up to $20/month ($240/year) at eligible FedEx, Grubhub, and office supply stores',
                'amount_cents': 2000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'other',
            },
            {
                'name': 'Walmart+ Credit',
                'description': 'Up to $12.95/month covering the Walmart+ membership fee',
                'amount_cents': 1295,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'shopping',
            },
            {
                'name': 'Squarespace Credit',
                'description': 'Up to $150 annually toward Squarespace website subscriptions',
                'amount_cents': 15000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'other',
            },
            {
                'name': 'Hotel Collection Credit',
                'description': 'Up to $150 annual credit on eligible Hotel Collection bookings',
                'amount_cents': 15000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Delta SkyMiles Gold',
        'annual_fee_cents': 15000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Delta Stays Credit',
                'description': 'Up to $100 annual credit on eligible Delta Stays hotel bookings',
                'amount_cents': 10000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'In-flight Credit',
                'description': 'Up to $200 annual credit for in-flight purchases on Delta',
                'amount_cents': 20000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Delta SkyMiles Platinum',
        'annual_fee_cents': 35000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Delta Stays Credit',
                'description': 'Up to $150 annual credit on eligible Delta Stays hotel bookings',
                'amount_cents': 15000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Rideshare Credit',
                'description': 'Up to $10/month ($120/year) as a statement credit on rideshare purchases (Uber, Lyft, etc.)',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'transportation',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck application',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'Resy Credit',
                'description': 'Up to $120 annually ($10/month) toward eligible Resy dining reservations',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Delta SkyMiles Reserve',
        'annual_fee_cents': 65000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Delta Stays Credit',
                'description': 'Up to $200 annual credit on eligible Delta Stays hotel bookings',
                'amount_cents': 20000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry application fee',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'Resy Credit',
                'description': 'Up to $240 annually ($20/month) toward eligible Resy dining reservations',
                'amount_cents': 2000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Hilton Honors',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'American Express',
        'name': 'Hilton Honors Surpass',
        'annual_fee_cents': 15000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Hilton Resort Credit',
                'description': 'Up to $200 semi-annual credit for purchases at Hilton Resorts',
                'amount_cents': 20000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Hilton Honors Aspire',
        'annual_fee_cents': 55000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Hilton Resort Credit',
                'description': 'Up to $200 semi-annual credit ($400/year) for purchases at Hilton Resorts',
                'amount_cents': 20000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Airline Fee Credit',
                'description': 'Up to $50 quarterly ($200/year) for incidental fees on one selected airline',
                'amount_cents': 5000,
                'frequency': 'quarterly',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Hilton Credit',
                'description': 'Up to $200 annual credit on eligible Hilton purchases',
                'amount_cents': 20000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'CLEAR Plus Credit',
                'description': 'Up to $209 annually toward CLEAR Plus membership',
                'amount_cents': 20900,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Marriott Bonvoy Brilliant',
        'annual_fee_cents': 65000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Dining Credit',
                'description': 'Up to $300 annually ($25/month) at restaurants worldwide',
                'amount_cents': 2500,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'American Express',
        'name': 'Marriott Bonvoy Bevy',
        'annual_fee_cents': 25000,
        'is_verified': True,
        'benefits': [],
    },

    # ─────────────────────────────────────────
    # CHASE
    # ─────────────────────────────────────────
    {
        'bank': 'Chase',
        'name': 'Sapphire Reserve',
        'annual_fee_cents': 79500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Travel Credit',
                'description': '$300 annual travel credit applied automatically to travel purchases (airlines, hotels, car rentals, etc.)',
                'amount_cents': 30000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'The Edit Hotel Credit',
                'description': 'Up to $250 semi-annually ($500/year) on prepaid 2-night+ stays at The Edit by Chase Travel hotels',
                'amount_cents': 25000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Dining Credit (Exclusive Tables)',
                'description': 'Up to $150 semi-annually ($300/year) at restaurants in the Sapphire Exclusive Tables program via OpenTable',
                'amount_cents': 15000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
            {
                'name': 'Entertainment Credit (StubHub)',
                'description': 'Up to $150 semi-annually ($300/year) on concert and event tickets on StubHub and viagogo',
                'amount_cents': 15000,
                'frequency': 'semi_annual',
                'period_type': 'calendar_year',
                'category': 'entertainment',
            },
            {
                'name': 'Lyft Credit',
                'description': 'Up to $10/month ($120/year) in Lyft in-app credits through September 2027',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'transportation',
            },
            {
                'name': 'Peloton Credit',
                'description': 'Up to $10/month ($120/year) toward Peloton app or equipment',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'other',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry, NEXUS, or TSA PreCheck application (every 4 years)',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'Sapphire Preferred',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Annual Travel Credit',
                'description': '$50 annual Ultimate Rewards Hotel Credit',
                'amount_cents': 5000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'DoorDash Credit',
                'description': '$10/month DashPass credit for DoorDash orders',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
            {
                'name': 'Lyft Credit',
                'description': 'Up to $10 quarterly in Lyft credits',
                'amount_cents': 1000,
                'frequency': 'quarterly',
                'period_type': 'calendar_year',
                'category': 'transportation',
            },
            {
                'name': 'Peloton Credit',
                'description': 'Up to $60 annually in Peloton app credits',
                'amount_cents': 6000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'other',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'Freedom Unlimited',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Chase',
        'name': 'Freedom Flex',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Cell Phone Protection',
                'description': 'Up to $800 per claim, $1,000 per year against damage or theft when you pay your phone bill with the card',
                'amount_cents': 80000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'other',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'Freedom Rise',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Chase',
        'name': 'Ink Business Preferred',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Cell Phone Protection',
                'description': 'Up to $1,000 per claim against damage or theft when you pay your phone bill with the card',
                'amount_cents': 100000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'other',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'Ink Business Unlimited',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Chase',
        'name': 'Ink Business Cash',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Chase',
        'name': 'United Explorer',
        'annual_fee_cents': 15000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'United Hotels Credit',
                'description': 'Up to $100 annually on prepaid hotel stays booked through United Hotels',
                'amount_cents': 10000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Rideshare Credit',
                'description': 'Up to $5/month ($60/year) as a statement credit on rideshare purchases (Uber, Lyft, etc.)',
                'amount_cents': 500,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'transportation',
            },
            {
                'name': 'Instacart Credit',
                'description': '$10/month ($120/year) Instacart credit for grocery delivery',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry, NEXUS, or TSA PreCheck (every 4 years)',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'United Club Infinite',
        'annual_fee_cents': 69500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'United Travel Credit',
                'description': 'Up to $100 annual credit on United purchases',
                'amount_cents': 10000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'Renowned Hotels Credit',
                'description': 'Up to $200 annually on prepaid hotel stays at Renowned Hotels & Resorts properties via Chase Travel',
                'amount_cents': 20000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Rideshare Credit',
                'description': 'Up to $150 annually ($12.50/month) as statement credits on rideshare purchases (Uber, Lyft, etc.)',
                'amount_cents': 1250,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'transportation',
            },
            {
                'name': 'Instacart Credit',
                'description': 'Up to $20/month ($240/year) in Instacart credits for grocery delivery',
                'amount_cents': 2000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck (every 4 years)',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'Marriott Bonvoy Boundless',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Free Night Award',
                'description': 'One free night award (up to 35,000 points) each account anniversary year',
                'amount_cents': 15000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'Marriott Bonvoy Bold',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Chase',
        'name': 'Southwest Rapid Rewards Priority',
        'annual_fee_cents': 22900,
        'is_verified': True,
        'benefits': [
            {
                'name': 'In-flight Credit',
                'description': 'Four $25 credits ($100 total) per year for in-flight Wi-Fi and purchases',
                'amount_cents': 2500,
                'frequency': 'quarterly',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'Southwest Rapid Rewards Premier',
        'annual_fee_cents': 9900,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Chase',
        'name': 'Southwest Rapid Rewards Plus',
        'annual_fee_cents': 6900,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Chase',
        'name': 'World of Hyatt',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Free Night Award',
                'description': 'One free night at a Category 1–4 Hyatt property each cardmember anniversary',
                'amount_cents': 15000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'IHG One Rewards Premier',
        'annual_fee_cents': 9900,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Annual Free Night',
                'description': 'One free night at an IHG property (up to 40,000 points) each anniversary',
                'amount_cents': 15000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Chase',
        'name': 'Amazon Prime Rewards Visa',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Chase',
        'name': 'British Airways Visa Signature',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Chase',
        'name': 'Aeroplan',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },

    # ─────────────────────────────────────────
    # CAPITAL ONE
    # ─────────────────────────────────────────
    {
        'bank': 'Capital One',
        'name': 'Venture X',
        'annual_fee_cents': 39500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Travel Credit',
                'description': '$300 annual credit for bookings through Capital One Travel',
                'amount_cents': 30000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'Anniversary Bonus Miles',
                'description': '10,000 bonus miles on each account anniversary (~$100 in travel)',
                'amount_cents': 10000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Capital One',
        'name': 'Venture',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck (every 4 years)',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Capital One',
        'name': 'VentureOne',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Capital One',
        'name': 'Savor',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Capital One',
        'name': 'SavorOne',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Capital One',
        'name': 'Quicksilver',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Capital One',
        'name': 'QuicksilverOne',
        'annual_fee_cents': 3900,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Capital One',
        'name': 'Spark Cash Plus',
        'annual_fee_cents': 15000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Annual Cash Bonus',
                'description': '$200 annual cash bonus when you spend $200,000+ per year',
                'amount_cents': 20000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'other',
            },
        ]
    },
    {
        'bank': 'Capital One',
        'name': 'Spark Miles',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Capital One',
        'name': 'Spark Cash Select',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Capital One',
        'name': 'Platinum',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },

    # ─────────────────────────────────────────
    # CITI
    # ─────────────────────────────────────────
    {
        'bank': 'Citi',
        'name': 'Double Cash',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Citi',
        'name': 'Custom Cash',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Citi',
        'name': 'Strata Premier',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Hotel Savings Benefit',
                'description': '$100 discount on a single hotel stay of $500+ booked through thankyou.com each calendar year',
                'amount_cents': 10000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Citi',
        'name': 'Prestige Card',
        'annual_fee_cents': 49500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Travel Credit',
                'description': '$250 annual travel credit for airlines, hotels, and travel agencies',
                'amount_cents': 25000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Citi',
        'name': 'AAdvantage Platinum Select',
        'annual_fee_cents': 9900,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Citi',
        'name': 'AAdvantage Executive World Elite',
        'annual_fee_cents': 59500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Admirals Club Membership',
                'description': 'Full Admirals Club membership ($850 value)',
                'amount_cents': 85000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'Lyft Credit',
                'description': 'Up to $10/month in Lyft credits',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'transportation',
            },
            {
                'name': 'Grubhub Credit',
                'description': 'Up to $10/month credit at Grubhub',
                'amount_cents': 1000,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'dining',
            },
        ]
    },
    {
        'bank': 'Citi',
        'name': 'AAdvantage MileUp',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Citi',
        'name': 'Rewards+',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Citi',
        'name': 'Simplicity',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Citi',
        'name': 'Diamond Preferred',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Citi',
        'name': 'Costco Anywhere Visa',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },

    # ─────────────────────────────────────────
    # BANK OF AMERICA
    # ─────────────────────────────────────────
    {
        'bank': 'Bank of America',
        'name': 'Premium Rewards',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Airline Incidental & TSA Credit',
                'description': 'Up to $100 annually for airline incidental fees and TSA PreCheck or Global Entry',
                'amount_cents': 10000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Bank of America',
        'name': 'Premium Rewards Elite',
        'annual_fee_cents': 55000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Travel Credit',
                'description': 'Up to $300 annually in credits for airline incidentals, seat upgrades, and baggage fees',
                'amount_cents': 30000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Lifestyle Credit',
                'description': 'Up to $150 annually for streaming, fitness, and food delivery services',
                'amount_cents': 15000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'other',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Bank of America',
        'name': 'Customized Cash Rewards',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Bank of America',
        'name': 'Unlimited Cash Rewards',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Bank of America',
        'name': 'Travel Rewards',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Bank of America',
        'name': 'Alaska Airlines Visa Signature',
        'annual_fee_cents': 7500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Companion Fare',
                'description': 'Annual companion fare from $122 ($99 fare + taxes/fees from $23) each account anniversary',
                'amount_cents': 15000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Bank of America',
        'name': 'BankAmericard',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },

    # ─────────────────────────────────────────
    # US BANK
    # ─────────────────────────────────────────
    {
        'bank': 'US Bank',
        'name': 'Altitude Reserve',
        'annual_fee_cents': 40000,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Travel and Dining Credit',
                'description': 'Up to $325 annually in credits for eligible travel and dining purchases',
                'amount_cents': 32500,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $120 credit for Global Entry or $85 for TSA PreCheck',
                'amount_cents': 12000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'US Bank',
        'name': 'Altitude Connect',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Global Entry / TSA PreCheck Credit',
                'description': 'Up to $100 credit for Global Entry or TSA PreCheck (every 4 years)',
                'amount_cents': 10000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
            {
                'name': 'Streaming Credit',
                'description': 'Up to $30 annually ($2.50/month) for eligible streaming service purchases',
                'amount_cents': 250,
                'frequency': 'monthly',
                'period_type': 'calendar_year',
                'category': 'entertainment',
            },
        ]
    },
    {
        'bank': 'US Bank',
        'name': 'Altitude Go',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Streaming Credit',
                'description': '$15 annual credit for eligible streaming services after 11 consecutive months of streaming purchases',
                'amount_cents': 1500,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'entertainment',
            },
        ]
    },
    {
        'bank': 'US Bank',
        'name': 'Cash+',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'US Bank',
        'name': 'Shopper Cash Rewards',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'US Bank',
        'name': 'Visa Platinum',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'US Bank',
        'name': 'Business Leverage',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'US Bank',
        'name': 'Business Triple Cash Rewards',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },

    # ─────────────────────────────────────────
    # WELLS FARGO
    # ─────────────────────────────────────────
    {
        'bank': 'Wells Fargo',
        'name': 'Autograph',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Cell Phone Protection',
                'description': 'Up to $600 per claim against damage or theft when you pay your phone bill with the card',
                'amount_cents': 60000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'other',
            },
        ]
    },
    {
        'bank': 'Wells Fargo',
        'name': 'Autograph Journey',
        'annual_fee_cents': 9500,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Hotel Credit',
                'description': '$50 annual statement credit toward hotel stays of $50+',
                'amount_cents': 5000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Airline Credit',
                'description': 'Up to $50 annually for airline incidental purchases',
                'amount_cents': 5000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'travel',
            },
            {
                'name': 'Cell Phone Protection',
                'description': 'Up to $1,000 per claim against damage or theft',
                'amount_cents': 100000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'other',
            },
        ]
    },
    {
        'bank': 'Wells Fargo',
        'name': 'Active Cash',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [
            {
                'name': 'Cell Phone Protection',
                'description': 'Up to $600 per claim against damage or theft when you pay your phone bill with the card',
                'amount_cents': 60000,
                'frequency': 'annual',
                'period_type': 'calendar_year',
                'category': 'other',
            },
        ]
    },
    {
        'bank': 'Wells Fargo',
        'name': 'Reflect',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },

    # ─────────────────────────────────────────
    # DISCOVER
    # ─────────────────────────────────────────
    {
        'bank': 'Discover',
        'name': 'it Cash Back',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Discover',
        'name': 'it Miles',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Discover',
        'name': 'it Chrome',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Discover',
        'name': 'it Secured',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },

    # ─────────────────────────────────────────
    # BARCLAYS
    # ─────────────────────────────────────────
    {
        'bank': 'Barclays',
        'name': 'Arrival Plus',
        'annual_fee_cents': 8900,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Barclays',
        'name': 'JetBlue Plus',
        'annual_fee_cents': 9900,
        'is_verified': True,
        'benefits': [
            {
                'name': 'In-flight Credit',
                'description': '$50 annual credit for JetBlue in-flight purchases',
                'amount_cents': 5000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },
    {
        'bank': 'Barclays',
        'name': 'JetBlue Business',
        'annual_fee_cents': 9900,
        'is_verified': True,
        'benefits': [
            {
                'name': 'In-flight Credit',
                'description': '$50 annual credit for JetBlue in-flight purchases',
                'amount_cents': 5000,
                'frequency': 'annual',
                'period_type': 'membership_year',
                'category': 'travel',
            },
        ]
    },

    # ─────────────────────────────────────────
    # SYNCHRONY / OTHER STORE CARDS
    # ─────────────────────────────────────────
    {
        'bank': 'Synchrony',
        'name': 'Amazon Store Card',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
    {
        'bank': 'Goldman Sachs',
        'name': 'Apple Card',
        'annual_fee_cents': 0,
        'is_verified': True,
        'benefits': [],
    },
]
