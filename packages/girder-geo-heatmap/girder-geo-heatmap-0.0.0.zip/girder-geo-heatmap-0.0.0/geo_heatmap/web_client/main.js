import { registerPluginNamespace } from '@girder/core/pluginUtils';

// imported for the side effects
import './GeoHeatmapWidget.js';

import * as geoHeatmap from './index.js';
registerPluginNamespace('geo_heatmap', geoHeatmap);
