# Changelog

All notable (feature) changes to this project will be documented in this file.

This project uses calendar versioning, https://calver.org/, and this log provides
a concise history of changes made.

## Latest

## 2025.07.26

- Changed formatting of the checklist protocol attributes to fix spacing and wrapping.
- Added Protocol TextChoice, mapping protocol codes to names used in eBird Portugal portal.

## 2025.07.22
- Add links to the News pages (Latest, Weekly, Monthly) so you can easily see the 
  news for a given county, state or country.

## 2025.07.17
- Updated regular expressions used to clean the name when a Location is added.

## 2025.07.15
- Added multi-select to fields when filtering by location. 
- Added pages for server errors and page not found errors.

## 2025.06.28
- Added separate layouts when lists are viewed on mobile devices.
- Changed page layout to reduce the amount of empty space.
- Changed filters so they are displayed in a sidebar on the left side of the page.
- Changed links to checklists so they go direct to eBird.org.

## 2025.06.26
- Added an About page, describing the site.
- Added a field to the Species page, so you can search for species, subspecies, etc.
- Added a Filter model for mapping Guineafowls, etc. to their domestic form.
- Added a page showing the list of Observations that were moderated.
- Fixed error where the species total was also counting subspecies, forms, etc.

## 2025.06.10
- Added a "What's New" page for describing changes to the site.
- Changed the list of High Counts so entries are ordered by date, then species.

## 2025.06.08
- Added form fields for editing translated text in the Django Admin.
- Added retries for eBird API calls and page loads.
- Added the Species page for showing year lists, site list, personal lists, etc.

## 2025.05.31
- Added notifications to the Latest News page.
- Added moderator comments to Observations.
- Added field to order by number of species seen to the Checklists search panel.
- Added field to order by number of species seen to the Observations search panel.
- Added contact page.
- Observation model - changed count to be non-null, with a default of zero.

## 2025.05.27
- Added the 'enabled' field to Observer so loading Checklists can be blocked.
- Added caching to the Latest, Weekly and Monthly News pages.
- Added date range fields to the Checklists search panel.
- Added filter for hotspots to the Checklists search panel.
- Added date range fields to the Observations search panel.

## 2025.05.21
- Added site logo.

## 2025.05.18
- Added a High Count table to the Latest, Weekly and Monthly News pages.

## 2025.05.17
- Added weekly news, showing all the statistics for a given week.
- Added monthly news, showing all the statistics for a given month.

## 2025.05.16
- Changed the News page so it shows news for the past 7 days, not the current week.
- Removed the year from the date on the Big Lists table.
- Removed the year from the date on the Big Days table.

## 2025.05.15
- Changed the search field on the Observations page to show separate fields for 
  Country (optional), State, County, Observer, and Species.

## 2025.05.14
- Added a Big Days table to the News page, showing the top ten observers who saw the most
  species in a day for that week. Each entry links to a page with the full list.
- Added a Year list page showing the complete list of species seen during the year.
- Added signal handler to remove coordinates, country code, and region from the 
  name when a Location is added.
- Added a signal handler to remove the company names (tour operators or guides), and 
  and any extra spaces from the name when an Observer is added.
- Changed the search field on the Checklists page to show separate fields for 
  Country (optional), State, County and Observer.

## 2025.04.17
This is the first formal/official release of the project where the ideas and code 
have stabilised sufficiently to start recording the changes made:
- Added the Observations page, showing a paginated list of all observations.
- Added the Checklists page, showing a paginated list of all checklists.
- Added the News page, showing, for a given week:
  - the number of species seen
  - the number of checklists submitted
  - the number of observers
  - the number of hours spent biding
  - a table top ten ebirders with the highest number of species seen
  - a table top ten ebirders with the highest number of checklists submitted
  - a table top ten ebirders with the highest number of hours spent birding
  - the list species added to the year list 
  - the top 10 checklists with the most species seen
