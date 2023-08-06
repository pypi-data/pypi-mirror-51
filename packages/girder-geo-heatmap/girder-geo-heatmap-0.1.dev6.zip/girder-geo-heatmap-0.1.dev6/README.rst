==================
Girder Geo Heatmap
==================

A Girder plugin showing a heatmap of geospatial items.

Features
--------

At every level of the hierarchy widget, and at the list of collections and list of users, a heatmap is shown of available geospatial items.  The heatmap uses one point per geospatial item, using the centroid of the bounds reported in the geometa record.  The heatmap is fetched based on all items that the user has permissions to read.
