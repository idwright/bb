import { Component, OnInit, Input } from '@angular/core';

import { Entities } from '../typescript-angular2-client/model/Entities';
import { Entity } from '../typescript-angular2-client/model/Entity';
import { Property } from '../typescript-angular2-client/model/Property';


import * as L from 'leaflet';
import 'leaflet.markercluster';

@Component({
  selector: 'app-entities-map',
  templateUrl: './entities-map.component.html',
  styleUrls: ['./entities-map.component.css']
})

export class EntitiesMapComponent {

  _entities: Entities;

  // Open Street Map Definition
  LAYER_OSM = {
    id: 'openstreetmap',
    name: 'Open Street Map',
    enabled: false,
    layer: L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: 'Open Street Map'
    })
  };

  // Values to bind to Leaflet Directive
  leaflet_layersControlOptions = { position: 'bottomright' };
  leaflet_baseLayers = {
    'Open Street Map': this.LAYER_OSM.layer
  };
  leaflet_options = {
    zoom: 3,
    center: L.latLng([-4.6991, 20.8422])
  };
  // Marker cluster stuff

  markers = new Map<string, L.Layer[]>();
  groups = new Map<string, L.MarkerClusterGroup>();
  map;

  @Input()
  set entities(entities: Entities) {
    this._entities = entities;
    //console.log(this._entities);
    if (entities) {
      entities.entities.forEach(entity => {
        let entityRow: any = {
          'entityId': entity.entity_id,
          'refs': entity.refs.length
        };
        let lat: number = null;
        let lng: number = null;
        let loc: string = '';
        let country: string = '';
        entity.values.forEach(prop => {
          if (prop.data_name == 'latitude') {
            lat = Number(prop.data_value);
          } else if (prop.data_name == 'longitude') {
            lng = Number(prop.data_value);
          } else if (prop.data_name == 'location' && loc == '') {
              loc = prop.data_value;
          } else if (prop.data_name == 'name') {
              loc = prop.data_value;
          } else if (prop.data_name == 'country') {
            country = prop.data_value;
          }
        });
        if (lat && lng) {
          this.addMarker(country, lat, lng, loc);
        }
      });

      this.markers.forEach((value: L.Layer[], key: string) => {
        let mcg = L.markerClusterGroup();
        mcg.clearLayers();
        mcg.addLayers(value);
        mcg.addTo(this.map);
      });

    }

  }

  onMapReady(map: L.Map) {
    this.map = map;
  }

  addMarker(country, lat, lng, marker_title) {
    let marker = L.marker(
      [lat, lng],
      {
        title: marker_title,
        icon: L.icon({
          iconSize: [25 * 0.5, 41 * 0.5],
          iconAnchor: [13 * 0.5, 0],
          iconUrl: 'assets/marker-icon.png',
          shadowUrl: 'assets/marker-shadow.png'
        })
      }
    );

    if (!this.markers.has(country)) {
      this.markers.set(country, []);
    }

    this.markers.get(country).push(marker);

  }

}
