

# Technical requirements
- Backend APIs are in app/main.py
- Frontend specifications;
    - Use VueJS app using Vuetify and Vuerouter. 
    - The app shuold be contained within single HTML file. 
    Name that file index.html. It is stoed in app/static folder.
    - Each components should take full width of the container. 
    - Use latest VueJS. Use createApp mentod to create the app.
    - Do not use inline template in the component. Use HTML template. 


# User stories

## Customer/User Stories

### Account Management
- **As a new visitor**, I want to create an account with my personal details (name, email, address, phone) so I can make purchases and track my orders.
- **As a registered customer**, I want to log in to my account so I can access my purchase history and personal information.
- **As a customer**, I want to update my profile information (address, phone, email) so my account details stay current.
- **As a customer**, I want to view my assigned support representative's contact information so I can get help when needed.

### Music Discovery & Browsing
- **As a music lover**, I want to browse music by genre (Rock, Jazz, Metal, Alternative & Punk, etc.) so I can discover new music in my preferred styles.
- **As a customer**, I want to search for specific artists so I can find all their available music.
- **As a customer**, I want to view all albums by a specific artist so I can explore their discography.
- **As a customer**, I want to see track details (name, duration, composer, file size) before purchasing so I know what I'm buying.
- **As a customer**, I want to filter tracks by media type (MP3, AAC, video files) so I can find content in my preferred format.

### Playlist Management
- **As a registered user**, I want to create custom playlists so I can organize my favorite tracks.
- **As a user**, I want to add tracks to my playlists so I can curate my music collection.
- **As a user**, I want to browse existing playlists (Music, Movies, TV Shows, Audiobooks, 90's Music) to discover curated content.
- **As a user**, I want to remove tracks from my playlists so I can keep them updated.

### Shopping & Purchasing
- **As a customer**, I want to add individual tracks to my shopping cart so I can purchase only the songs I want.
- **As a customer**, I want to purchase entire albums so I can get all tracks from an artist's release.
- **As a customer**, I want to see the unit price of each track before adding to cart so I can make informed purchasing decisions.
- **As a customer**, I want to review my cart before checkout so I can modify my order if needed.
- **As a customer**, I want to specify my billing address during checkout so my purchase can be processed correctly.

### Order Management
- **As a customer**, I want to view my purchase history so I can see all my previous orders.
- **As a customer**, I want to see detailed invoice information (date, billing address, total amount) for each purchase.
- **As a customer**, I want to view line items for each invoice so I can see exactly what I purchased and at what price.
- **As a customer**, I want to download or re-access my purchased tracks so I can enjoy my music.

## Administrative Stories

### Content Management
- **As a store administrator**, I want to add new artists to the catalog so customers can discover new music.
- **As a store administrator**, I want to add new albums and associate them with artists so the catalog stays current.
- **As a store administrator**, I want to upload new tracks with all metadata (name, composer, duration, file size, price) so customers have complete information.
- **As a store administrator**, I want to manage genres so music can be properly categorized.
- **As a store administrator**, I want to set and update track prices so the store remains profitable.

### Customer Support
- **As a sales support agent**, I want to view my assigned customers so I can provide personalized service.
- **As a sales support agent**, I want to access customer purchase history so I can help resolve issues.
- **As a sales support agent**, I want to view customer contact information so I can reach out when needed.

### Business Intelligence
- **As a store manager**, I want to see sales reports by genre so I can understand customer preferences.
- **As a store manager**, I want to view top-selling artists and tracks so I can make inventory decisions.
- **As a store manager**, I want to analyze customer purchase patterns so I can improve marketing strategies.
- **As a store manager**, I want to see revenue reports by time period so I can track business performance.

### System Management
- **As a system administrator**, I want to manage employee accounts and roles so the right people have appropriate access.
- **As a system administrator**, I want to maintain the organizational hierarchy (employees reporting structure) so the company structure is properly reflected.
- **As a system administrator**, I want to manage media types so the system can handle different file formats.

## Technical User Stories

### Performance & Usability
- **As a customer**, I want fast search results so I can quickly find the music I'm looking for.
- **As a user**, I want the website to work on my mobile device so I can browse and purchase music anywhere.
- **As a customer**, I want to preview tracks before purchasing so I can make sure I like the music.

These user stories cover the full spectrum of functionality that the Chinook database schema supports, from basic e-commerce features to advanced music discovery and administrative capabilities.