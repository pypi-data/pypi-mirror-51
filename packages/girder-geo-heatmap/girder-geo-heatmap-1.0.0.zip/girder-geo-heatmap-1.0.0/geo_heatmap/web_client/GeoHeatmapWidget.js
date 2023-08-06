import $ from 'jquery';
import _ from 'underscore';

import { wrap } from '@girder/core/utilities/PluginUtils';
import CollectionsView from '@girder/core/views/body/CollectionsView.js';
import HierarchyWidget from '@girder/core/views/widgets/HierarchyWidget.js';
import UsersView from '@girder/core/views/body/UsersView.js';
import View from '@girder/core/views/View';
import { restRequest } from '@girder/core/rest';

import geo from 'geojs/geo.js';

import GeoHeatmapWidgetTemplate from './GeoHeatmapWidget.pug';
import './GeoHeatmapWidget.styl';

/* HierarchyWidget */

wrap(HierarchyWidget, 'render', function (render) {
    render.call(this);
    if (this.geoHeatmap) {
        this.geoHeatmap.remove();
        delete this.geoHeatmap;
    }
    this.geoHeatmap = new GeoHeatmapWidget({
        el: $('<div>').insertAfter(this.$('.g-folder-metadata')),
        parentView: this
    });
});

wrap(HierarchyWidget, 'destroy', function (destroy) {
    if (this.geoHeatmap) {
        this.geoHeatmap.remove();
        delete this.geoHeatmap;
    }
    destroy.call(this);
});

/* CollectionsView */

wrap(CollectionsView, 'render', function (render) {
    render.call(this);
    if (this.geoHeatmap) {
        this.geoHeatmap.remove();
        delete this.geoHeatmap;
    }
    this.geoHeatmap = new GeoHeatmapWidget({
        el: $('<div>').appendTo(this.parentView.$el.find('#g-app-body-container')),
        parentView: this,
        model: 'collection'
    });
});

wrap(CollectionsView, 'destroy', function (destroy) {
    if (this.geoHeatmap) {
        this.geoHeatmap.remove();
        delete this.geoHeatmap;
    }
    destroy.call(this);
});

/* UsersView */

wrap(UsersView, 'render', function (render) {
    render.call(this);
    if (this.geoHeatmap) {
        this.geoHeatmap.remove();
        delete this.geoHeatmap;
    }
    this.geoHeatmap = new GeoHeatmapWidget({
        el: $('<div>').appendTo(this.parentView.$el.find('#g-app-body-container')),
        parentView: this,
        model: 'user'
    });
});

wrap(UsersView, 'destroy', function (destroy) {
    if (this.geoHeatmap) {
        this.geoHeatmap.remove();
        delete this.geoHeatmap;
    }
    destroy.call(this);
});

/* GeoHeatmapWidget */

var GeoHeatmapWidget = View.extend({
    initialize: function (settings) {
        // if this is the all-collection or all-user view, then we would
        // switch this to enumerate the reachable list of collections or users
        let parents = [];
        if (settings && settings.model) {
            parents.push({type: settings.model});
        }
        if (this.parentView.parentModel) {
            parents.push({
                type: this.parentView.parentModel.get('_modelType') || 'folder',
                id: this.parentView.parentModel.id
            });
        }
        this.geometaItems = [];
        this.geometaBounds = {};
        let promises = [];
        parents.forEach((parent) => promises.push(this.collectGeometa(parent, this.parentView)));
        Promise.all(promises).then(() => {
            if (this.removed || !this.geometaItems.length) {
                return;
            }
            this.render();
            return null;
        });
    },
    render: function () {
        this.$el.html(GeoHeatmapWidgetTemplate({}));
        if (!$('.g-geo-heatmap-widget').length || this.removed) {
            return;
        }
        this.map = geo.map({node: '.g-geo-heatmap-widget', max: 20});
        this.map.bounds(this.geometaBounds);
        this.map.zoom(this.map.zoom() - 0.25);
        this.map.createLayer('osm');
        this.featureLayer = this.map.createLayer('feature', {features: ['heatmap']});
        this.heatmap = this.featureLayer.createFeature('heatmap', {
            binned: 'auto',
            style: {
                blurRadius: 0,
                radius: 20,
                gaussian: true,
                color: {
                    0.00: {r: 0, g: 1, b: 1, a: 0.0},
                    0.25: {r: 0, g: 1, b: 1, a: 0.5},
                    0.75: {r: 1, g: 1, b: 0, a: 0.7},
                    1.00: {r: 1, g: 0, b: 0, a: 0.8}
                }
            }
        }).intensity(_.constant(1));
        this.heatmap.data(this.geometaItems).draw();
        return this;
    },
    remove: function () {
        this.removed = true;
        if (this.map) {
            this.map.exit();
        }
        View.prototype.remove.call(this);
    },
    collectGeometa(parent, parentView) {
        if (this.removed) {
            return Promise.resolve();
        }
        let promises = [];
        promises.push(new Promise((resolve, reject) => {
            restRequest({
                url: parent.id ? 'folder' : parent.type,
                data: {limit: 100000, parentType: parent.type, parentId: parent.id}
            }).done((result) => {
                result.reduce((prom1, folder) => prom1.then(() => {
                    return this.collectGeometa({type: parent.id ? 'folder' : parent.type, id: folder._id});
                }), Promise.resolve()).then(() => {
                    resolve();
                    return null;
                });
            }).fail((err) => {
                reject(new Error('fail', err));
            });
        }));
        if (parent.type === 'folder') {
            promises.push(new Promise((resolve, reject) => {
                restRequest({
                    url: 'item/find/geometa',
                    data: {limit: 100000, folderId: parent.id}
                }).done((result) => {
                    result.forEach((item) => {
                        if (!item.geometa || !item.geometa.bounds || !item.geometa.bounds.coordinates) {
                            return;
                        }
                        let entry = {
                            id: item._id,
                            coordinates: item.geometa.bounds.coordinates,
                            z: 0
                        };
                        let x = 0, y = 0, t = 0;
                        entry.coordinates.forEach((bound) => bound.slice(0, bound.length - 1).forEach((pt) => {
                            if (pt[1] >= 90 || pt[1] <= -90) {
                                x = NaN;
                                return;
                            }
                            t += 1;
                            x += pt[0];
                            y += pt[1];
                        }));
                        if (!t || !isFinite(x) || !isFinite(y)) {
                            return;
                        }
                        entry.x = x / t;
                        entry.y = y / t;
                        entry.coordinateCount = t;
                        entry.coordinates.forEach((bound) => bound.slice(0, bound.length - 1).forEach((pt) => {
                            if (this.geometaBounds.left === undefined || pt[0] < this.geometaBounds.left) {
                                this.geometaBounds.left = pt[0];
                            }
                            if (this.geometaBounds.top === undefined || pt[1] > this.geometaBounds.top) {
                                this.geometaBounds.top = pt[1];
                            }
                            if (this.geometaBounds.right === undefined || pt[0] > this.geometaBounds.right) {
                                this.geometaBounds.right = pt[0];
                            }
                            if (this.geometaBounds.bottom === undefined || pt[1] < this.geometaBounds.bottom) {
                                this.geometaBounds.bottom = pt[1];
                            }
                        }));
                        this.geometaItems.push(entry);
                    });
                    resolve();
                }).fail((err) => {
                    reject(new Error('fail', err));
                });
            }));
        }
        return Promise.all(promises);
    }
});

export default GeoHeatmapWidget;
